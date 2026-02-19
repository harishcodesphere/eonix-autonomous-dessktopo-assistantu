"""
EONIX Security API — Score, alerts, processes, whitelist.
"""
from fastapi import APIRouter
from tools.security_monitor import security_monitor_bg

router = APIRouter()


@router.get("/security/score")
async def security_score():
    """Current security score + breakdown."""
    return security_monitor_bg.get_score_breakdown()


@router.get("/security/alerts")
async def security_alerts(limit: int = 50):
    """Recent security alerts."""
    return {"alerts": security_monitor_bg.get_recent_alerts(limit)}


@router.get("/security/processes")
async def security_processes():
    """Running processes with risk levels."""
    procs = security_monitor_bg.get_processes_with_risk()
    return {
        "processes": procs[:100],
        "total": len(procs),
        "unknown_count": sum(1 for p in procs if p['risk'] == 'unknown'),
        "warning_count": sum(1 for p in procs if p['risk'] == 'warning'),
    }


@router.post("/security/whitelist/{process}")
async def whitelist_process(process: str):
    """Add a process name to the security whitelist."""
    security_monitor_bg.whitelist_process(process)
    return {"message": f"'{process}' added to whitelist", "process": process}
