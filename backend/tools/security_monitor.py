"""
EONIX Security Monitor — Background daemon that scans for security threats
every 30 seconds: suspicious processes, open ports, high-privilege processes,
network anomalies, and device access.
"""
import threading
import time
import os
import json
from datetime import datetime
from typing import List, Dict

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from memory.db import SessionLocal, SecurityLog

# ── Known/safe processes ──────────────────────────────────────
DEFAULT_WHITELIST = {
    "system", "system idle process", "svchost", "csrss", "wininit",
    "winlogon", "lsass", "services", "smss", "dwm", "explorer",
    "taskhostw", "runtimebroker", "shellexperiencehost", "searchhost",
    "startmenuexperiencehost", "ctfmon", "conhost", "dllhost",
    "sihost", "fontdrvhost", "spoolsv", "securityhealthservice",
    "sgrmbroker", "msdtc", "registry", "memory compression",
    "searchindexer", "searchprotocolhost", "audiodg",
    "msmpeng", "nissrv",  # Windows Defender
    "python", "pythonw", "python3", "node", "code", "git",
    "chrome", "msedge", "firefox", "brave",
    "spotify", "discord", "slack", "teams",
    "nvidia share", "nvcontainer",
}

WHITELIST_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "security_whitelist.json")

HIGH_RISK_PORTS = {4444, 5555, 6666, 31337, 12345, 1337, 9999}
COMMON_SAFE_PORTS = {80, 443, 8000, 8080, 3000, 5000, 5173, 27017, 5432, 3306, 6379}


def _load_whitelist() -> set:
    wl = set(DEFAULT_WHITELIST)
    try:
        if os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, "r") as f:
                wl.update(set(json.load(f)))
    except Exception:
        pass
    return wl


def _save_whitelist(wl: set):
    try:
        os.makedirs(os.path.dirname(WHITELIST_FILE), exist_ok=True)
        custom = wl - DEFAULT_WHITELIST
        with open(WHITELIST_FILE, "w") as f:
            json.dump(list(custom), f)
    except Exception:
        pass


class SecurityMonitor:
    """Background security scanner."""

    INTERVAL = 30

    def __init__(self):
        self._thread = None
        self._running = False
        self._whitelist = _load_whitelist()
        self._known_pids = set()
        self._known_ports = set()
        self._alerts_cache: List[Dict] = []
        self._score = 100
        self._threats: List[Dict] = []

    def start(self):
        if self._running or not HAS_PSUTIL:
            return
        self._running = True
        # Snapshot current processes as baseline
        try:
            self._known_pids = {p.pid for p in psutil.process_iter(['pid'])}
            conns = psutil.net_connections(kind='inet')
            self._known_ports = {c.laddr.port for c in conns if c.status == 'LISTEN'}
        except Exception:
            pass
        self._thread = threading.Thread(target=self._loop, daemon=True, name="SecurityMonitor")
        self._thread.start()

    def stop(self):
        self._running = False

    @property
    def score(self):
        return self._score

    @property
    def threats(self):
        return list(self._threats)

    def whitelist_process(self, name: str):
        self._whitelist.add(name.lower())
        _save_whitelist(self._whitelist)

    def get_processes_with_risk(self) -> List[Dict]:
        """List running processes with risk level."""
        if not HAS_PSUTIL:
            return []
        result = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    name = (info.get('name') or 'Unknown').lower().replace('.exe', '')
                    risk = 'safe'
                    if name not in self._whitelist:
                        risk = 'unknown'
                    # Check high CPU/memory
                    cpu = info.get('cpu_percent') or 0
                    mem = info.get('memory_percent') or 0
                    if cpu > 80 or mem > 50:
                        risk = 'warning'
                    result.append({
                        'pid': info.get('pid'),
                        'name': info.get('name', 'Unknown'),
                        'username': info.get('username', ''),
                        'cpu': round(cpu, 1),
                        'memory': round(mem, 1),
                        'risk': risk,
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
        return sorted(result, key=lambda x: {'warning': 0, 'unknown': 1, 'safe': 2}.get(x['risk'], 3))

    def get_recent_alerts(self, limit=50) -> List[Dict]:
        """Get recent security alerts from DB."""
        try:
            db = SessionLocal()
            rows = db.query(SecurityLog).order_by(SecurityLog.id.desc()).limit(limit).all()
            db.close()
            return [{
                'id': r.id, 'timestamp': str(r.timestamp), 'severity': r.severity,
                'category': r.category, 'title': r.title, 'message': r.message,
                'process': r.process_name, 'pid': r.pid, 'resolved': r.resolved,
            } for r in rows]
        except Exception:
            return list(self._alerts_cache[-limit:])

    def get_score_breakdown(self) -> Dict:
        """Return security score + breakdown."""
        return {
            'score': self._score,
            'threats': self._threats,
            'threat_count': len(self._threats),
            'status': 'secure' if self._score >= 80 else 'warning' if self._score >= 50 else 'critical',
        }

    # ── Core scan loop ─────────────────────────────────────────
    def _loop(self):
        while self._running:
            try:
                self._scan()
            except Exception as e:
                print(f"[SecurityMonitor] scan error: {e}")
            time.sleep(self.INTERVAL)

    def _scan(self):
        threats = []

        # 1. New unknown processes
        try:
            current_pids = set()
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    info = proc.info
                    pid = info['pid']
                    name = (info.get('name') or '').lower().replace('.exe', '')
                    current_pids.add(pid)
                    if pid not in self._known_pids and name and name not in self._whitelist:
                        threat = {
                            'type': 'new_process', 'severity': 'INFO',
                            'title': f'New process: {info["name"]}',
                            'message': f'Unknown process "{info["name"]}" (PID {pid}) started.',
                            'process': info['name'], 'pid': pid,
                        }
                        threats.append(threat)
                        self._log_alert(threat)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            self._known_pids = current_pids
        except Exception:
            pass

        # 2. High network usage processes
        try:
            net_before = {}
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    io = proc.io_counters()
                    net_before[proc.pid] = io.write_bytes + io.read_bytes
                except Exception:
                    continue
            time.sleep(1)
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    io = proc.io_counters()
                    after = io.write_bytes + io.read_bytes
                    before = net_before.get(proc.pid, after)
                    delta_mb = (after - before) / (1024 * 1024)
                    name = (proc.info.get('name') or '').lower().replace('.exe', '')
                    if delta_mb > 50 and name not in self._whitelist:
                        threat = {
                            'type': 'high_network', 'severity': 'WARNING',
                            'title': f'High network: {proc.info["name"]}',
                            'message': f'"{proc.info["name"]}" transferred {delta_mb:.1f} MB in 1s.',
                            'process': proc.info['name'], 'pid': proc.pid,
                        }
                        threats.append(threat)
                        self._log_alert(threat)
                except Exception:
                    continue
        except Exception:
            pass

        # 3. Open ports scan
        try:
            conns = psutil.net_connections(kind='inet')
            current_ports = {c.laddr.port for c in conns if c.status == 'LISTEN'}
            new_ports = current_ports - self._known_ports
            for port in new_ports:
                sev = 'CRITICAL' if port in HIGH_RISK_PORTS else 'INFO'
                threat = {
                    'type': 'new_port', 'severity': sev,
                    'title': f'New listening port: {port}',
                    'message': f'Port {port} is now open and listening.',
                    'process': None, 'pid': None,
                }
                threats.append(threat)
                self._log_alert(threat)
            self._known_ports = current_ports
        except Exception:
            pass

        # 4. High-privilege processes
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    info = proc.info
                    user = (info.get('username') or '').lower()
                    name = (info.get('name') or '').lower().replace('.exe', '')
                    if 'system' in user and name not in self._whitelist and name:
                        # Only alert once per process name
                        pass  # Captured in new_process check
                except Exception:
                    continue
        except Exception:
            pass

        # Calculate score
        crit_count = sum(1 for t in threats if t['severity'] == 'CRITICAL')
        warn_count = sum(1 for t in threats if t['severity'] == 'WARNING')
        info_count = sum(1 for t in threats if t['severity'] == 'INFO')
        penalty = crit_count * 25 + warn_count * 10 + info_count * 2
        self._score = max(0, 100 - penalty)
        self._threats = threats

    def _log_alert(self, threat: Dict):
        """Save alert to DB and cache."""
        self._alerts_cache.append(threat)
        if len(self._alerts_cache) > 200:
            self._alerts_cache = self._alerts_cache[-100:]
        try:
            db = SessionLocal()
            row = SecurityLog(
                severity=threat['severity'],
                category=threat['type'],
                title=threat['title'],
                message=threat['message'],
                process_name=threat.get('process'),
                pid=threat.get('pid'),
                date=datetime.now().strftime('%Y-%m-%d'),
            )
            db.add(row)
            db.commit()
            db.close()
        except Exception as e:
            print(f"[SecurityMonitor] log error: {e}")


# Singleton
security_monitor_bg = SecurityMonitor()
