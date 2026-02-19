# 🤖 EONIX — Your Personal JARVIS

<div align="center">

![Eonix Banner](https://img.shields.io/badge/EONIX-Autonomous%20Intelligence-blue?style=for-the-badge&logo=android)

**"Just like JARVIS, but for your laptop"**

*An AI-powered autonomous desktop intelligence system with local LLM processing*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral-orange.svg)](https://ollama.ai/)
[![Electron](https://img.shields.io/badge/Electron-Latest-47848F.svg)](https://www.electronjs.org/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)

**"Sir, shall I run a full system diagnostic?" - Eonix, probably**

[Features](#-core-capabilities) • [Architecture](#-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Plugins](#-plugin-ecosystem)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Demo](#-demo--screenshots)
- [Core Capabilities](#-core-capabilities)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [AI Engine (Ollama/Mistral)](#-ai-engine---ollama--mistral-integration)
- [Frontend Architecture](#-frontend-architecture---jarvis-style-ui)
- [Backend Architecture](#-backend-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Plugin Ecosystem](#-plugin-ecosystem)
- [API Reference](#-api-reference)
- [Security & Privacy](#-security--privacy)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [FAQ](#-faq)

---

## 🚀 Overview

**Eonix** is a revolutionary autonomous desktop intelligence system inspired by JARVIS from Iron Man. It's not just an assistant—it's your personal AI that understands context, anticipates needs, and controls your entire system with natural language.

### 🎯 What is Eonix?

Imagine having Tony Stark's JARVIS, but running **100% locally** on your laptop using **Ollama + Mistral**. Eonix is:

- 🧠 **Your AI Brain** — Natural language understanding with Mistral LLM
- 🎮 **System Commander** — Complete control over your laptop (files, apps, processes)
- 🤖 **Autonomous Agent** — Executes multi-step workflows without supervision
- 🔒 **Privacy Guardian** — All processing happens locally, zero cloud dependency
- ⚡ **Lightning Fast** — Real-time responses with local inference
- 🎨 **Beautiful Interface** — Futuristic UI inspired by Tony Stark's workshop

### 💡 The Vision

```
Traditional Assistant          →          EONIX
──────────────────                        ──────
"Hey Siri, open Chrome"                   "Eonix, prepare my development environment"
Manual file organization                   "Clean up my downloads intelligently"
Switching between apps                     "Monitor my system and alert me of issues"
No context awareness                       "Continue where we left off yesterday"
Cloud-dependent                            "Works offline, data stays local"
Generic responses                          "Learns your preferences and adapts"
```

> **"Good morning, sir. Your system is running optimally. You have 3 pending tasks and 2 unread emails. Would you like me to prioritize them?"** - Eonix

---

## 🎥 Demo & Screenshots

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│  EONIX                                    ⚙️ Settings 🔌 Status │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🎤  "Eonix, what's my CPU usage?"                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🤖  CPU: 34% | RAM: 8.2GB/16GB | Disk: 256GB free   │  │
│  │      Temperature: 54°C | Network: 125 Mbps ↓         │  │
│  │      All systems optimal, sir. 🟢                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Quick Actions:                                       │  │
│  │  [📁 Organize Downloads]  [💻 Dev Mode]  [🧹 Cleanup] │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Active Tasks:                                              │
│  ⚡ Monitoring system resources                             │
│  📊 Syncing work files to backup                            │
│  🎵 Spotify playback optimization active                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Voice Interaction Panel

```
┌─────────────────────────────────────────┐
│  🎙️  VOICE COMMAND ACTIVE              │
│                                         │
│  "Open VS Code with my React project    │
│   and start the development server"     │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  🤖 Understood. Executing:      │   │
│  │  1. Opening VS Code ✓           │   │
│  │  2. Loading /projects/react-app ✓│  │
│  │  3. Starting dev server...      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### System Dashboard

```
┌──────────────────────────────────────────────────────┐
│  📊 SYSTEM OVERVIEW                                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  CPU Usage:    ████████░░░░░░░░░░  42%             │
│  Memory:       ██████████████░░░░  68% (10.9/16GB) │
│  Disk:         ████░░░░░░░░░░░░░░  23% (185GB free)│
│  Network:      ↓ 45 Mbps  ↑ 12 Mbps                │
│                                                      │
│  🔥 Top Processes:                                   │
│  1. Chrome        2.4 GB   18%                      │
│  2. VS Code       1.8 GB   12%                      │
│  3. Ollama        1.2 GB    8%                      │
│                                                      │
│  ⚡ Active Automations:                              │
│  • Battery Saver Mode (< 20%)                       │
│  • Auto File Organization                            │
│  • Smart Volume Control                             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## ⭐ Core Capabilities

### 🧠 Advanced AI Intelligence (Powered by Ollama + Mistral)

**Local LLM Processing** — Complete privacy, no internet required

- ✅ **Mistral 7B** — Fast, efficient for most tasks
- ✅ **Mistral 13B** — Advanced reasoning and complex workflows  
- ✅ **Llama 3** — Alternative model support
- ✅ **Custom Fine-tuned Models** — Train on your specific workflows

**Natural Language Understanding**

```python
# Examples of what Eonix understands:

"Find all my Python files from last week and organize them by project"
→ Scans filesystem, identifies files, creates folders, moves files

"I need to focus. Close distractions and enable Do Not Disturb"
→ Closes social media apps, mutes notifications, dims screen

"What's consuming my RAM? Kill unnecessary processes"
→ Analyzes memory usage, suggests processes to terminate, executes on confirmation

"Prepare my morning routine"
→ Opens email, calendar, news, todo list, starts coffee machine (if smart home integrated)

"Remind me to take a break every hour"
→ Sets recurring notification with smart pause detection (pauses during meetings)
```

**Contextual Memory**

- Remembers past conversations and preferences
- Learns from your behavior patterns
- Adapts responses based on context
- Multi-turn conversations with state persistence

**Intent Recognition**

```
User: "It's too bright in here"
Eonix: [Analyzes context]
       - Time: 11 PM
       - Screen brightness: 100%
       - Ambient light: Low
       
Action: Dims screen to 40%, suggests night mode
```

### ⚡ System-Level Automation

**File & Folder Management**

```bash
# Intelligent Organization
"Organize my Downloads folder"
→ Groups by: file type, date, project, size
→ Removes duplicates
→ Archives old files
→ Creates smart folders

# Smart Search
"Find that presentation from last month about AI"
→ Searches: filename, content, metadata
→ Returns: relevance-ranked results
→ Preview available

# Bulk Operations
"Rename all my screenshots with dates"
"Compress videos larger than 100MB"
"Delete temporary files older than 30 days"
```

**Application Control**

```javascript
// Launch & Control
eonix.app.launch("Visual Studio Code", {
  workspace: "/projects/eonix",
  extensions: ["prettier", "eslint"],
  terminal: "npm run dev"
});

// Window Management
eonix.window.arrange("split-screen", {
  left: "Chrome",
  right: "VS Code"
});

// Process Management
eonix.process.monitor("chrome", {
  maxMemory: "4GB",
  action: "alert"  // or "restart", "kill"
});
```

**System Monitoring**

```python
# Real-time Resource Tracking
- CPU usage per core
- RAM allocation by process
- Disk I/O statistics
- Network bandwidth monitoring
- Temperature sensors
- Battery health and predictions

# Intelligent Alerts
"CPU > 90% for 5 minutes" → Alert
"Disk < 10GB free" → Suggest cleanup
"Battery < 15%" → Enable power saving
"Unusual network activity" → Security check
```

**Automation Workflows**

```yaml
# Example: Developer Morning Routine
workflow:
  name: "Developer Startup"
  trigger: "weekday at 9:00 AM"
  steps:
    - check_system_health
    - open_terminal
    - start_docker_containers
    - open_vs_code:
        workspace: "last_active"
    - open_chrome:
        tabs:
          - "localhost:3000"
          - "github.com/notifications"
    - start_music:
        playlist: "Focus Deep Work"
        volume: 30
    - notify: "Good morning! Development environment ready."
```

### 🎙️ Multimodal Interaction

**Voice Commands**

- **Wake Word**: "Hey Eonix" or "Jarvis"
- **Continuous Listening**: Optional always-on mode
- **Noise Cancellation**: Filters background noise
- **Multi-language**: English, Spanish, French, German, Hindi, etc.

```
Voice Command Pipeline:
Audio Input → Speech-to-Text → Intent Analysis → Task Execution → Voice Feedback
```

**Text Interface**

- Discord-style chat UI
- Markdown support for rich formatting
- Code syntax highlighting
- File/image previews
- Command history with search

**Hotkeys**

```
Global Shortcuts:
Ctrl + Space      → Activate Eonix
Ctrl + Shift + E  → Quick command
Ctrl + Alt + V    → Voice mode toggle
Ctrl + Alt + D    → Show dashboard
Win + E           → System overview
```

**System Tray Integration**

```
Right-click Tray Icon:
├─ 🟢 Status: Active
├─ 📊 System Health
├─ ⚡ Quick Actions
│  ├─ Clean Downloads
│  ├─ Enable Focus Mode
│  └─ System Snapshot
├─ 🔧 Settings
└─ ❌ Exit Eonix
```

### 🔐 Privacy-First Architecture

**100% Local Processing**

```
┌─────────────────────────────────────┐
│  YOUR LAPTOP (100% Self-contained)  │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Eonix Frontend (Electron)   │  │
│  │  └─ React UI + IPC           │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │  Eonix Backend (Python)      │  │
│  │  └─ FastAPI + WebSockets     │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │  Ollama Service              │  │
│  │  └─ Mistral 7B/13B           │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Local Database (SQLite)     │  │
│  │  └─ Encrypted with AES-256   │  │
│  └──────────────────────────────┘  │
│                                     │
│  NO INTERNET REQUIRED               │
│  NO CLOUD DEPENDENCY                │
│  NO DATA TRANSMISSION               │
└─────────────────────────────────────┘
```

**Security Features**

- 🔐 **End-to-End Encryption** — All data encrypted at rest
- 🛡️ **Sandboxed Execution** — Isolated plugin environment
- 🔑 **Permission System** — User approval for sensitive operations
- 📝 **Audit Logs** — Complete activity tracking
- 🚫 **No Telemetry** — Zero data collection

### 🧩 Extensible Plugin System

**Built-in Plugins**

| Plugin | Description | Capabilities |
|--------|-------------|--------------|
| 📧 **Email Assistant** | Gmail, Outlook integration | Read, send, filter, smart replies |
| 💻 **Dev Tools** | Developer workflow automation | Git, Docker, npm, build tools |
| 📊 **Productivity** | Calendar, tasks, notes | Schedule management, reminders |
| 🎵 **Media Control** | Spotify, VLC, YouTube | Playback control, playlists |
| 🌐 **Browser** | Chrome, Firefox, Edge | Tab management, bookmarks |
| 📁 **Cloud Sync** | GDrive, Dropbox, OneDrive | File synchronization |
| 🏠 **Smart Home** | IoT device control | Lights, thermostat, cameras |
| 💬 **Communication** | Slack, Discord, Teams | Message management, status |

**Custom Plugin Development**

```python
# plugins/custom_plugin.py
from eonix.plugin import EonixPlugin, command

class MyCustomPlugin(EonixPlugin):
    """Custom automation for my workflow"""
    
    def __init__(self):
        super().__init__(
            name="My Plugin",
            version="1.0.0",
            description="Does awesome things"
        )
    
    @command(
        name="do_thing",
        description="Performs the thing",
        parameters=["param1", "param2"]
    )
    async def execute_thing(self, param1, param2):
        """
        This method is called when user says:
        "Eonix, do thing with X and Y"
        """
        result = await self.api.system.execute(
            f"custom_operation --p1={param1} --p2={param2}"
        )
        
        return {
            "status": "success",
            "message": f"Thing done with {param1} and {param2}",
            "data": result
        }
    
    @command(name="auto_backup")
    async def smart_backup(self):
        """Intelligent backup based on file changes"""
        files = await self.api.files.get_modified(since="24h")
        important = await self.ai.classify(files, "importance")
        
        for file in important:
            await self.api.files.backup(file, location="~/Backups")
        
        return f"Backed up {len(important)} important files"
```

**Plugin Marketplace** (Planned)

- Community-developed plugins
- One-click installation
- Automatic updates
- Rating and review system

---

## 🏗️ System Architecture

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                          EONIX ARCHITECTURE                          │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Electron + React)                     │
│  ┌────────────┐  ┌─────────────┐  ┌──────────┐  ┌────────────────┐ │
│  │  Main UI   │  │   Voice I/O  │  │Dashboard │  │  Settings &    │ │
│  │  Chat      │  │   STT/TTS    │  │Analytics │  │  Preferences   │ │
│  │  Interface │  │   Hotkeys    │  │Monitors  │  │                │ │
│  └─────┬──────┘  └──────┬──────┘  └────┬─────┘  └────────┬───────┘ │
└────────┼─────────────────┼──────────────┼─────────────────┼─────────┘
         │                 │              │                 │
         └─────────────────┴──────────────┴─────────────────┘
                                  │
                          ┌───────▼────────┐
                          │  IPC Bridge    │
                          │  (WebSocket +  │
                          │   Electron)    │
                          └───────┬────────┘
                                  │
┌─────────────────────────────────▼─────────────────────────────────────┐
│                    BACKEND (Python + FastAPI)                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    API Gateway Layer                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │ REST API │  │WebSocket │  │  gRPC    │  │  Events  │    │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │   │
│  └───────┼─────────────┼─────────────┼─────────────┼───────────┘   │
│          │             │             │             │                │
│  ┌───────▼─────────────▼─────────────▼─────────────▼───────────┐   │
│  │              Intelligence Orchestrator                       │   │
│  │  ┌──────────────┐    ┌─────────────┐    ┌────────────────┐ │   │
│  │  │   Intent     │───▶│   Context   │───▶│  Task Planner  │ │   │
│  │  │   Parser     │    │   Manager   │    │  & Executor    │ │   │
│  │  └──────┬───────┘    └──────┬──────┘    └───────┬────────┘ │   │
│  └─────────┼───────────────────┼────────────────────┼──────────┘   │
│            │                   │                    │               │
│  ┌─────────▼───────────────────▼────────────────────▼──────────┐   │
│  │                    AI Processing Layer                       │   │
│  │  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │   │
│  │  │  Ollama Client │  │   Embedding  │  │  Classification │ │   │
│  │  │  (Mistral LLM) │  │   Generator  │  │    & NER        │ │   │
│  │  └────────┬───────┘  └──────┬───────┘  └────────┬────────┘ │   │
│  └───────────┼──────────────────┼───────────────────┼──────────┘   │
│              │                  │                   │               │
│  ┌───────────▼──────────────────▼───────────────────▼──────────┐   │
│  │                   Execution Engine                           │   │
│  │  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌───────────┐  │   │
│  │  │  System  │  │   File    │  │  Process │  │   Plugin  │  │   │
│  │  │  Control │  │  Manager  │  │  Manager │  │  Runtime  │  │   │
│  │  └────┬─────┘  └─────┬─────┘  └────┬─────┘  └─────┬─────┘  │   │
│  └───────┼──────────────┼─────────────┼──────────────┼────────┘   │
│          │              │             │              │             │
│  ┌───────▼──────────────▼─────────────▼──────────────▼────────┐   │
│  │                  Data & Memory Layer                        │   │
│  │  ┌────────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐ │   │
│  │  │   SQLite   │  │   Vector  │  │   Cache  │  │  Logs   │ │   │
│  │  │  Database  │  │   Store   │  │  (Redis) │  │ (Files) │ │   │
│  │  └────────────┘  └───────────┘  └──────────┘  └─────────┘ │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬────────────────────────────────────┘
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│                     OPERATING SYSTEM LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   File   │  │ Process  │  │  Network │  │    Hardware      │ │
│  │  System  │  │ Manager  │  │  Stack   │  │   (CPU/RAM/GPU)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION FLOW                        │
└─────────────────────────────────────────────────────────────────┘

User Input (Voice/Text)
         │
         ▼
┌────────────────────┐
│  Speech-to-Text    │  (If voice command)
│  (Whisper / DeepSpeech)
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Input Validation  │
│  & Preprocessing   │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Intent Detection  │◄─────┐
│  (Mistral via      │      │ Context from
│   Ollama)          │      │ previous interactions
└────────┬───────────┘      │
         │                  │
         ▼                  │
┌────────────────────┐      │
│  Context Manager   │──────┘
│  (Retrieves history,
│   user preferences,
│   current state)
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Task Planner      │  Generates execution plan:
│  (Breaks complex   │  1. Open VS Code
│   commands into    │  2. Load workspace
│   atomic actions)  │  3. Start dev server
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Permission Check  │  Asks user if action is
│                    │  potentially destructive
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Execution Engine  │
│  (Orchestrates     │
│   system calls,    │
│   file operations, │
│   app control)     │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Action Executors  │
│  ┌──────────────┐  │
│  │ File Ops     │  │
│  │ Process Ctrl │  │
│  │ App Launch   │  │
│  │ System API   │  │
│  └──────────────┘  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Result Handler    │
│  (Collects outputs,│
│   formats response)│
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Response Gen      │  Natural language response
│  (Mistral LLM)     │  generated based on results
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Memory Update     │  Stores interaction for
│  (SQLite + Vector  │  future context
│   embeddings)      │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Text-to-Speech    │  (Optional voice response)
│  (piper-tts)       │
└────────┬───────────┘
         │
         ▼
   Display to User
```

---

## 🛠️ Technology Stack

### Frontend Stack

```yaml
Core Framework:
  - Electron: ^28.0.0          # Desktop app framework
  - React: ^18.2.0             # UI library
  - TypeScript: ^5.0.0         # Type safety

UI Components:
  - Tailwind CSS: ^3.3.0       # Styling
  - Framer Motion: ^10.0.0     # Animations
  - Radix UI: ^1.0.0           # Accessible components
  - Recharts: ^2.5.0           # Data visualization
  - React Flow: ^11.0.0        # Workflow builder

State Management:
  - Zustand: ^4.3.0            # Global state
  - React Query: ^4.0.0        # Server state
  - Jotai: ^2.0.0              # Atomic state

Real-time Communication:
  - Socket.io-client: ^4.5.0   # WebSocket client
  - Electron IPC                # Main/Renderer process communication

Voice/Audio:
  - Electron Media Device       # Microphone access
  - Web Audio API               # Audio processing
  - MediaRecorder API           # Recording

Build Tools:
  - Vite: ^4.3.0               # Fast dev server & bundler
  - Electron Builder: ^24.0.0  # App packaging
  - ESLint + Prettier          # Code quality
```

### Backend Stack

```yaml
Core Framework:
  - Python: ^3.10              # Primary language
  - FastAPI: ^0.104.0          # Web framework
  - Uvicorn: ^0.24.0           # ASGI server
  - Pydantic: ^2.0.0           # Data validation

AI/ML:
  - Ollama: latest             # LLM runtime
  - langchain: ^0.0.335        # LLM orchestration
  - sentence-transformers: ^2.2.0  # Embeddings
  - transformers: ^4.35.0      # Additional ML models

System Control:
  - psutil: ^5.9.0             # System monitoring
  - pyautogui: ^0.9.54         # GUI automation
  - pygetwindow: ^0.0.9        # Window management
  - keyboard: ^0.13.5          # Keyboard control
  - mouse: ^0.7.1              # Mouse control
  - pycaw: ^20231129           # Audio control (Windows)

File Operations:
  - watchdog: ^3.0.0           # File system monitoring
  - pathlib: built-in          # Path handling
  - shutil: built-in           # File operations
  - aiofiles: ^23.2.0          # Async file I/O

Database:
  - SQLAlchemy: ^2.0.0         # ORM
  - SQLite: ^3.40.0            # Local database
  - chromadb: ^0.4.0           # Vector database
  - redis: ^5.0.0              # Caching (optional)

Task Scheduling:
  - APScheduler: ^3.10.0       # Background jobs
  - asyncio: built-in          # Async operations
  - celery: ^5.3.0             # Distributed tasks (optional)

Communication:
  - websockets: ^12.0          # WebSocket server
  - httpx: ^0.25.0             # Async HTTP client
  - python-socketio: ^5.10.0   # Socket.io server

Voice Processing:
  - faster-whisper: ^0.9.0     # Speech-to-text
  - piper-tts: ^1.0.0          # Text-to-speech
  - pyaudio: ^0.2.14           # Audio I/O
  - sounddevice: ^0.4.6        # Audio recording

Security:
  - cryptography: ^41.0.0      # Encryption
  - python-jose: ^3.3.0        # JWT tokens
  - passlib: ^1.7.4            # Password hashing

Utilities:
  - python-dotenv: ^1.0.0      # Environment variables
  - pyyaml: ^6.0.1             # Config files
  - loguru: ^0.7.0             # Logging
  - typer: ^0.9.0              # CLI interface
```

### AI Models

```yaml
Primary LLM (via Ollama):
  - mistral:7b                 # Default, fast inference
  - mistral:13b                # Advanced reasoning
  - llama3:8b                  # Alternative model
  - codellama:7b               # Code-specific tasks

Embedding Models:
  - all-MiniLM-L6-v2           # Sentence embeddings
  - bge-small-en-v1.5          # Higher quality embeddings

Speech Models:
  - faster-whisper-base        # STT (Speech-to-Text)
  - piper-en_US-lessac         # TTS (Text-to-Speech)

Vision Models (Planned):
  - llava:7b                   # Multimodal (image + text)
  - bakllava:7b                # Alternative vision model
```

---

## 🤖 AI Engine - Ollama & Mistral Integration

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  EONIX AI ENGINE                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  User Input: "Organize my downloads by project"            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │    Intent Classification      │
         │                               │
         │  Input → Mistral Prompt:      │
         │  "Classify this command:      │
         │   Organize my downloads       │
         │                               │
         │  Categories:                  │
         │  - file_management            │
         │  - app_control                │
         │  - system_info                │
         │  - automation                 │
         │                               │
         │  Return JSON with intent,     │
         │  entities, and parameters"    │
         └──────────┬────────────────────┘
                    │
                    ▼
         ┌───────────────────────────────┐
         │   Ollama API Call             │
         │                               │
         │   POST localhost:11434/api/   │
         │   generate                    │
         │                               │
         │   {                           │
         │     "model": "mistral:7b",    │
         │     "prompt": "...",          │
         │     "stream": false           │
         │   }                           │
         └──────────┬────────────────────┘
                    │
                    ▼
         ┌───────────────────────────────┐
         │   Mistral Processing          │
         │   (Local Inference)           │
         │                               │
         │   ⚡ Latency: ~500ms          │
         │   💾 RAM: ~4GB                │
         │   🔒 100% Private             │
         └──────────┬────────────────────┘
                    │
                    ▼
         ┌───────────────────────────────┐
         │   Response                    │
         │                               │
         │   {                           │
         │     "intent": "file_organize",│
         │     "entities": {             │
         │       "location": "downloads",│
         │       "method": "by_project"  │
         │     },                        │
         │     "confidence": 0.95        │
         │   }                           │
         └──────────┬────────────────────┘
                    │
                    ▼
         ┌───────────────────────────────┐
         │   Task Execution              │
         │                               │
         │   1. Scan ~/Downloads         │
         │   2. Classify files           │
         │   3. Create project folders   │
         │   4. Move files               │
         │   5. Report results           │
         └───────────────────────────────┘
```

### Ollama Setup

**Installation**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral:7b        # ~4GB, recommended for most tasks
ollama pull mistral:13b       # ~7GB, for complex reasoning

# Optional models
ollama pull llama3:8b         # Meta's Llama 3
ollama pull codellama:7b      # Optimized for code

# Verify installation
ollama list

# Test the model
ollama run mistral:7b
>>> Hello! How do you work?
```

**Ollama Configuration**

```bash
# ~/.ollama/config.json
{
  "models_dir": "/home/user/.ollama/models",
  "server": {
    "host": "127.0.0.1",
    "port": 11434,
    "origins": ["http://localhost:*", "http://127.0.0.1:*"]
  },
  "gpu": {
    "enabled": true,          # Use GPU if available
    "layers": 33              # Number of layers to offload to GPU
  },
  "memory": {
    "max_ram": "8GB",         # Max RAM for model
    "context_length": 4096    # Token context window
  }
}
```

**Performance Optimization**

```python
# backend/ai/ollama_client.py
import ollama
from functools import lru_cache

class OllamaClient:
    def __init__(self):
        self.client = ollama.Client(host='http://localhost:11434')
        self.model = "mistral:7b"  # Default model
        
    @lru_cache(maxsize=100)
    async def generate(self, prompt: str, system: str = None) -> str:
        """
        Generate response with caching for repeated prompts
        """
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            system=system,
            options={
                "temperature": 0.7,      # Creativity (0-1)
                "top_p": 0.9,           # Nucleus sampling
                "top_k": 40,            # Top-k sampling
                "num_predict": 512,      # Max tokens to generate
                "num_ctx": 4096,        # Context window
                "repeat_penalty": 1.1,  # Avoid repetition
                "stop": ["User:", "###"] # Stop sequences
            }
        )
        return response['response']
    
    async def classify_intent(self, user_input: str) -> dict:
        """
        Classify user intent using structured prompt
        """
        system_prompt = """You are Eonix, an intelligent desktop assistant.
Classify the user's command and extract parameters.
Respond ONLY with valid JSON."""
        
        prompt = f"""
User command: "{user_input}"

Classify into one of these intents:
- file_operation (create, delete, move, organize, search)
- app_control (launch, close, switch, arrange)
- system_info (cpu, memory, disk, processes, network)
- automation (schedule, workflow, monitor, trigger)
- general_query (questions, help, conversation)

Response format:
{{
  "intent": "category_name",
  "action": "specific_action",
  "entities": {{"key": "value"}},
  "confidence": 0.0-1.0
}}
"""
        
        response = await self.generate(prompt, system=system_prompt)
        return json.loads(response)
    
    async def stream_generate(self, prompt: str):
        """
        Stream responses for real-time UI updates
        """
        stream = self.client.generate(
            model=self.model,
            prompt=prompt,
            stream=True
        )
        
        for chunk in stream:
            yield chunk['response']
```

### Prompt Engineering

**System Prompts**

```python
# backend/ai/prompts.py

SYSTEM_PROMPTS = {
    "assistant": """You are Eonix, an intelligent autonomous desktop assistant.
You help users automate tasks, manage their system, and improve productivity.

Personality traits:
- Professional yet friendly (like JARVIS)
- Concise and actionable
- Proactive in suggesting improvements
- Privacy-conscious

Guidelines:
- Always confirm destructive actions
- Provide clear status updates
- Suggest alternatives when requests are unclear
- Use natural, conversational language
""",
    
    "file_operations": """You are a file management expert.
Analyze file organization requests and create efficient strategies.

Consider:
- File type (documents, images, code, etc.)
- Date modified/created
- File size and duplicates
- Project/category associations
- User's past organization patterns
""",
    
    "code_assistant": """You are a programming assistant integrated into Eonix.
Help with development workflows, debugging, and automation.

Capabilities:
- Analyze code snippets
- Suggest optimizations
- Generate boilerplate
- Explain errors
- Recommend tools and libraries
""",
    
    "task_planner": """You are a task planning expert.
Break down complex requests into atomic, executable steps.

Output format:
{
  "steps": [
    {"action": "...", "params": {...}, "order": 1},
    {"action": "...", "params": {...}, "order": 2}
  ],
  "dependencies": [...],
  "estimated_time": "..."
}
"""
}
```

**Few-shot Examples**

```python
# backend/ai/examples.py

INTENT_CLASSIFICATION_EXAMPLES = [
    {
        "input": "Clean up my desktop",
        "output": {
            "intent": "file_operation",
            "action": "organize",
            "entities": {
                "location": "desktop",
                "method": "auto_categorize"
            },
            "confidence": 0.98
        }
    },
    {
        "input": "What's my RAM usage?",
        "output": {
            "intent": "system_info",
            "action": "get_memory",
            "entities": {},
            "confidence": 0.99
        }
    },
    {
        "input": "Open VS Code with my React project",
        "output": {
            "intent": "app_control",
            "action": "launch",
            "entities": {
                "application": "vscode",
                "workspace": "react_project"
            },
            "confidence": 0.95
        }
    }
]

# Use in prompts
def build_few_shot_prompt(user_input: str) -> str:
    examples = "\n\n".join([
        f"Input: {ex['input']}\nOutput: {json.dumps(ex['output'])}"
        for ex in INTENT_CLASSIFICATION_EXAMPLES
    ])
    
    return f"""
{examples}

Input: {user_input}
Output:
"""
```

### Model Selection Strategy

```python
# backend/ai/model_selector.py

class ModelSelector:
    """
    Intelligently select the right model for each task
    """
    
    MODEL_CAPABILITIES = {
        "mistral:7b": {
            "speed": "fast",           # ~500ms latency
            "quality": "good",
            "ram": "4GB",
            "use_cases": [
                "intent_classification",
                "entity_extraction",
                "simple_qa",
                "command_parsing"
            ]
        },
        "mistral:13b": {
            "speed": "medium",         # ~1.5s latency
            "quality": "excellent",
            "ram": "8GB",
            "use_cases": [
                "complex_reasoning",
                "code_analysis",
                "multi_step_planning",
                "detailed_explanations"
            ]
        },
        "codellama:7b": {
            "speed": "fast",
            "quality": "specialized",
            "ram": "4GB",
            "use_cases": [
                "code_generation",
                "debugging",
                "script_writing",
                "regex_patterns"
            ]
        }
    }
    
    def select_model(self, task_type: str, complexity: str) -> str:
        """
        Choose optimal model based on task
        """
        if task_type in ["code_gen", "debug"]:
            return "codellama:7b"
        
        if complexity == "high" or task_type == "planning":
            return "mistral:13b"
        
        return "mistral:7b"  # Default for speed
```

### Embeddings & Vector Search

```python
# backend/ai/embeddings.py
from sentence_transformers import SentenceTransformer
import chromadb

class EmbeddingManager:
    """
    Manage embeddings for semantic search and context retrieval
    """
    
    def __init__(self):
        # Lightweight embedding model (~80MB)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Vector database for similarity search
        self.chroma_client = chromadb.PersistentClient(
            path="./data/chroma"
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="eonix_memory",
            metadata={"hnsw:space": "cosine"}
        )
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding vector for text"""
        return self.model.encode(text).tolist()
    
    async def store_interaction(
        self,
        user_input: str,
        response: str,
        metadata: dict
    ):
        """Store conversation in vector DB for context"""
        embedding = self.embed_text(user_input)
        
        self.collection.add(
            embeddings=[embedding],
            documents=[user_input],
            metadatas=[{
                **metadata,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[str(uuid.uuid4())]
        )
    
    async def find_similar_interactions(
        self,
        query: str,
        limit: int = 5
    ) -> list:
        """Find similar past interactions for context"""
        query_embedding = self.embed_text(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )
        
        return results['metadatas'][0]
```

---

## 🎨 Frontend Architecture - JARVIS-Style UI

### Component Structure

```
frontend/
├── src/
│   ├── main/                      # Electron main process
│   │   ├── index.ts              # App entry point
│   │   ├── ipc-handlers.ts       # IPC communication
│   │   ├── tray.ts               # System tray
│   │   └── shortcuts.ts          # Global hotkeys
│   │
│   ├── renderer/                  # React app
│   │   ├── App.tsx               # Root component
│   │   ├── index.tsx             # Renderer entry
│   │   │
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   ├── InputBar.tsx
│   │   │   │   └── VoiceButton.tsx
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── SystemMetrics.tsx
│   │   │   │   ├── ProcessList.tsx
│   │   │   │   ├── ResourceGraph.tsx
│   │   │   │   └── QuickActions.tsx
│   │   │   │
│   │   │   ├── Voice/
│   │   │   │   ├── VoicePanel.tsx
│   │   │   │   ├── WaveformVisualizer.tsx
│   │   │   │   └── SpeechIndicator.tsx
│   │   │   │
│   │   │   ├── Automation/
│   │   │   │   ├── WorkflowBuilder.tsx
│   │   │   │   ├── TaskScheduler.tsx
│   │   │   │   └── TriggerConfig.tsx
│   │   │   │
│   │   │   └── Common/
│   │   │       ├── Sidebar.tsx
│   │   │       ├── Header.tsx
│   │   │       └── StatusBar.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts    # Real-time connection
│   │   │   ├── useVoiceInput.ts   # Voice recording
│   │   │   ├── useSystemStats.ts  # Resource monitoring
│   │   │   └── useCommands.ts     # Command execution
│   │   │
│   │   ├── store/
│   │   │   ├── chatStore.ts       # Chat state
│   │   │   ├── systemStore.ts     # System metrics
│   │   │   └── settingsStore.ts   # User preferences
│   │   │
│   │   ├── api/
│   │   │   ├── backend.ts         # API client
│   │   │   ├── websocket.ts       # WebSocket client
│   │   │   └── ipc.ts             # Electron IPC
│   │   │
│   │   └── styles/
│   │       ├── globals.css
│   │       └── themes.ts
│   │
│   └── preload/
│       └── index.ts               # Preload script (security)
│
├── electron-builder.json
├── vite.config.ts
└── package.json
```

### UI Components (Code Examples)

**Main Chat Interface**

```typescript
// frontend/src/renderer/components/Chat/ChatInterface.tsx
import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '@/store/chatStore';
import { useWebSocket } from '@/hooks/useWebSocket';
import MessageBubble from './MessageBubble';
import InputBar from './InputBar';
import VoiceButton from './VoiceButton';

export default function ChatInterface() {
  const { messages, addMessage } = useChatStore();
  const { sendMessage, isConnected } = useWebSocket();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSendMessage = async (text: string) => {
    // Add user message to UI
    addMessage({
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date()
    });
    
    // Send to backend
    const response = await sendMessage({
      type: 'command',
      content: text
    });
    
    // Add AI response
    addMessage({
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: response.content,
      timestamp: new Date(),
      metadata: response.metadata
    });
  };
  
  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Header */}
      <div className="bg-black/30 backdrop-blur-md border-b border-blue-500/30 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <span className="text-xl">🤖</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">EONIX</h1>
              <div className="flex items-center gap-2 text-xs text-gray-300">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
                <span>{isConnected ? 'Online' : 'Offline'}</span>
              </div>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 rounded-lg transition-colors">
              <span>⚙️</span>
            </button>
          </div>
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Bar */}
      <div className="p-4 bg-black/30 backdrop-blur-md border-t border-blue-500/30">
        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <InputBar onSend={handleSendMessage} />
          </div>
          <VoiceButton onTranscript={handleSendMessage} />
        </div>
      </div>
    </div>
  );
}
```

**Message Bubble Component**

```typescript
// frontend/src/renderer/components/Chat/MessageBubble.tsx
import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    executionTime?: number;
    actions?: Array<{name: string; status: string}>;
  };
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-2xl ${isUser ? 'order-2' : 'order-1'}`}>
        <div className={`
          rounded-2xl p-4 shadow-lg
          ${isUser 
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
            : 'bg-gray-800/80 backdrop-blur-md border border-gray-700 text-gray-100'
          }
        `}>
          <ReactMarkdown
            components={{
              code({node, inline, className, children, ...props}) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
          
          {/* Action indicators */}
          {message.metadata?.actions && (
            <div className="mt-3 pt-3 border-t border-white/20 space-y-1">
              {message.metadata.actions.map((action, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm">
                  <span className={action.status === 'success' ? '✅' : '⏳'}>
                    {action.name}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="text-xs text-gray-400 mt-1 px-2">
          {message.timestamp.toLocaleTimeString()}
          {message.metadata?.executionTime && (
            <span className="ml-2">• {message.metadata.executionTime}ms</span>
          )}
        </div>
      </div>
      
      {/* Avatar */}
      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${isUser ? 'order-1 ml-3' : 'order-2 mr-3'}`}>
        {isUser ? (
          <div className="w-full h-full bg-gradient-to-br from-gray-600 to-gray-800 rounded-full flex items-center justify-center text-xl">
            👤
          </div>
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-xl animate-pulse">
            🤖
          </div>
        )}
      </div>
    </motion.div>
  );
}
```

**Voice Input Component**

```typescript
// frontend/src/renderer/components/Chat/VoiceButton.tsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useVoiceInput } from '@/hooks/useVoiceInput';

export default function VoiceButton({ 
  onTranscript 
}: { 
  onTranscript: (text: string) => void 
}) {
  const { isListening, startListening, stopListening, transcript } = useVoiceInput();
  const [isProcessing, setIsProcessing] = useState(false);
  
  const handleToggle = async () => {
    if (isListening) {
      setIsProcessing(true);
      const finalTranscript = await stopListening();
      if (finalTranscript) {
        onTranscript(finalTranscript);
      }
      setIsProcessing(false);
    } else {
      startListening();
    }
  };
  
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleToggle}
      disabled={isProcessing}
      className={`
        relative w-14 h-14 rounded-full flex items-center justify-center
        transition-all duration-300 overflow-hidden
        ${isListening 
          ? 'bg-gradient-to-br from-red-500 to-pink-600 shadow-lg shadow-red-500/50' 
          : 'bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg shadow-blue-500/50'
        }
        ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      {/* Pulse animation when listening */}
      {isListening && (
        <motion.div
          className="absolute inset-0 bg-red-400 rounded-full"
          initial={{ scale: 1, opacity: 0.7 }}
          animate={{ scale: 1.5, opacity: 0 }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      )}
      
      <span className="text-2xl relative z-10">
        {isProcessing ? '⏳' : isListening ? '⏹️' : '🎤'}
      </span>
      
      {/* Waveform visualization */}
      {isListening && (
        <div className="absolute bottom-0 left-0 right-0 flex justify-center gap-0.5 pb-2">
          {[...Array(5)].map((_, i) => (
            <motion.div
              key={i}
              className="w-0.5 bg-white rounded-full"
              animate={{
                height: [4, 12, 4],
              }}
              transition={{
                duration: 0.5,
                repeat: Infinity,
                delay: i * 0.1,
              }}
            />
          ))}
        </div>
      )}
    </motion.button>
  );
}
```

**System Dashboard**

```typescript
// frontend/src/renderer/components/Dashboard/SystemMetrics.tsx
import React from 'react';
import { motion } from 'framer-motion';
import { useSystemStats } from '@/hooks/useSystemStats';
import { Line } from 'react-chartjs-2';

export default function SystemMetrics() {
  const { cpu, memory, disk, network, history } = useSystemStats();
  
  const cpuData = {
    labels: history.timestamps,
    datasets: [
      {
        label: 'CPU',
        data: history.cpu,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };
  
  const memoryData = {
    labels: history.timestamps,
    datasets: [
      {
        label: 'RAM',
        data: history.memory,
        borderColor: 'rgb(168, 85, 247)',
        backgroundColor: 'rgba(168, 85, 247, 0.1)',
        tension: 0.4,
      },
    ],
  };
  
  return (
    <div className="grid grid-cols-2 gap-6 p-6">
      {/* CPU Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-xl p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">CPU Usage</h3>
          <span className={`text-2xl font-bold ${cpu > 80 ? 'text-red-400' : 'text-blue-400'}`}>
            {cpu.toFixed(1)}%
          </span>
        </div>
        
        <div className="h-32 mb-4">
          <Line data={cpuData} options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { min: 0, max: 100 },
            },
          }} />
        </div>
        
        {/* Progress bar */}
        <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
          <motion.div
            className={`h-full ${cpu > 80 ? 'bg-gradient-to-r from-red-500 to-pink-600' : 'bg-gradient-to-r from-blue-500 to-purple-600'}`}
            initial={{ width: 0 }}
            animate={{ width: `${cpu}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </motion.div>
      
      {/* Memory Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-xl p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Memory</h3>
          <span className="text-2xl font-bold text-purple-400">
            {memory.used}GB / {memory.total}GB
          </span>
        </div>
        
        <div className="h-32 mb-4">
          <Line data={memoryData} options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { min: 0, max: 100 },
            },
          }} />
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-purple-500 to-pink-600"
            initial={{ width: 0 }}
            animate={{ width: `${memory.percentage}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </motion.div>
      
      {/* Disk Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-xl p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Disk Space</h3>
          <span className="text-2xl font-bold text-green-400">
            {disk.free}GB free
          </span>
        </div>
        
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-gray-300">
            <span>Used: {disk.used}GB</span>
            <span>Total: {disk.total}GB</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-500 to-emerald-600"
              style={{ width: `${disk.percentage}%` }}
            />
          </div>
        </div>
      </motion.div>
      
      {/* Network Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-4">Network</h3>
        
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">↓ Download</span>
            <span className="text-lg font-semibold text-blue-400">
              {network.download} Mbps
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-300">↑ Upload</span>
            <span className="text-lg font-semibold text-green-400">
              {network.upload} Mbps
            </span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
```

### WebSocket Communication

```typescript
// frontend/src/renderer/hooks/useWebSocket.ts
import { useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

export function useWebSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  
  useEffect(() => {
    const newSocket = io('http://localhost:8000', {
      transports: ['websocket'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });
    
    newSocket.on('connect', () => {
      console.log('✅ Connected to backend');
      setIsConnected(true);
    });
    
    newSocket.on('disconnect', () => {
      console.log('❌ Disconnected from backend');
      setIsConnected(false);
    });
    
    newSocket.on('system_update', (data) => {
      // Handle real-time system updates
      console.log('System update:', data);
    });
    
    newSocket.on('task_progress', (data) => {
      // Handle task execution progress
      console.log('Task progress:', data);
    });
    
    setSocket(newSocket);
    
    return () => {
      newSocket.close();
    };
  }, []);
  
  const sendMessage = useCallback(async (message: any) => {
    if (!socket) throw new Error('Socket not connected');
    
    return new Promise((resolve) => {
      socket.emit('command', message, (response: any) => {
        resolve(response);
      });
    });
  }, [socket]);
  
  return { socket, isConnected, sendMessage };
}
```

---

## 🔧 Backend Architecture

### Project Structure

```
backend/
├── main.py                        # Application entry point
├── config.py                      # Configuration management
├── requirements.txt               # Python dependencies
│
├── api/
│   ├── __init__.py
│   ├── routes.py                  # FastAPI routes
│   ├── websocket.py               # WebSocket handlers
│   └── middleware.py              # Custom middleware
│
├── ai/
│   ├── __init__.py
│   ├── ollama_client.py           # Ollama integration
│   ├── prompts.py                 # System prompts
│   ├── embeddings.py              # Vector embeddings
│   ├── intent_classifier.py       # Intent recognition
│   └── task_planner.py            # Task decomposition
│
├── core/
│   ├── __init__.py
│   ├── context_manager.py         # Conversation context
│   ├── memory.py                  # Long-term memory
│   └── orchestrator.py            # Main control flow
│
├── execution/
│   ├── __init__.py
│   ├── file_manager.py            # File operations
│   ├── process_manager.py         # Process control
│   ├── app_controller.py          # Application control
│   ├── system_monitor.py          # Resource monitoring
│   └── automation_engine.py       # Workflow automation
│
├── plugins/
│   ├── __init__.py
│   ├── base.py                    # Plugin base class
│   ├── loader.py                  # Plugin loader
│   └── builtin/
│       ├── email_assistant.py
│       ├── dev_tools.py
│       └── media_control.py
│
├── database/
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy models
│   ├── crud.py                    # Database operations
│   └── migrations/
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                  # Logging setup
│   ├── security.py                # Encryption/auth
│   └── helpers.py                 # Utility functions
│
└── tests/
    ├── test_ai.py
    ├── test_execution.py
    └── test_plugins.py
```

### Core Backend Code

**Main Application**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import router
from api.websocket import setup_websocket
from core.orchestrator import Orchestrator
from database.models import init_db
from utils.logger import setup_logger

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    # Startup
    logger.info("🚀 Starting Eonix Backend...")
    
    # Initialize database
    await init_db()
    
    # Initialize AI engine
    app.state.orchestrator = Orchestrator()
    await app.state.orchestrator.initialize()
    
    logger.info("✅ Eonix Backend Ready")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down Eonix...")
    await app.state.orchestrator.cleanup()

# Create FastAPI app
app = FastAPI(
    title="Eonix Backend",
    description="Autonomous Desktop Intelligence API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Setup WebSocket
setup_websocket(app)

@app.get("/")
async def root():
    return {
        "name": "Eonix",
        "version": "1.0.0",
        "status": "online",
        "ai_model": "mistral:7b"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ollama": await app.state.orchestrator.ai.check_health(),
        "database": "connected"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development only
        log_level="info"
    )
```

**API Routes**

```python
# backend/api/routes.py
from fastAPI import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from core.orchestrator import get_orchestrator
from database.crud import save_interaction
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

class CommandRequest(BaseModel):
    command: str
    context: Optional[dict] = None

class CommandResponse(BaseModel):
    status: str
    response: str
    actions: list[dict]
    execution_time: float

@router.post("/command", response_model=CommandResponse)
async def execute_command(
    request: CommandRequest,
    background_tasks: BackgroundTasks,
    orchestrator = Depends(get_orchestrator)
):
    """
    Execute a user command
    """
    try:
        result = await orchestrator.process_command(
            command=request.command,
            context=request.context
        )
        
        # Save interaction in background
        background_tasks.add_task(
            save_interaction,
            user_input=request.command,
            response=result['response'],
            metadata=result['metadata']
        )
        
        return CommandResponse(**result)
        
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/stats")
async def get_system_stats(orchestrator = Depends(get_orchestrator)):
    """
    Get current system statistics
    """
    return await orchestrator.system_monitor.get_stats()

@router.get("/system/processes")
async def get_processes(orchestrator = Depends(get_orchestrator)):
    """
    Get running processes
    """
    return await orchestrator.process_manager.list_processes()

@router.post("/automation/create")
async def create_automation(
    workflow: dict,
    orchestrator = Depends(get_orchestrator)
):
    """
    Create new automation workflow
    """
    return await orchestrator.automation_engine.create_workflow(workflow)

@router.get("/automation/list")
async def list_automations(orchestrator = Depends(get_orchestrator)):
    """
    List all automation workflows
    """
    return await orchestrator.automation_engine.list_workflows()

@router.post("/plugins/install")
async def install_plugin(
    plugin_url: str,
    orchestrator = Depends(get_orchestrator)
):
    """
    Install a plugin from URL or local path
    """
    return await orchestrator.plugin_manager.install(plugin_url)

@router.get("/plugins/list")
async def list_plugins(orchestrator = Depends(get_orchestrator)):
    """
    List installed plugins
    """
    return await orchestrator.plugin_manager.list()
```

**WebSocket Handler**

```python
# backend/api/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
import socketio
import asyncio

from core.orchestrator import Orchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)

# Active connections
connections: dict[str, WebSocket] = {}

def setup_websocket(app):
    """Setup WebSocket handlers"""
    
    @sio.event
    async def connect(sid, environ):
        logger.info(f"Client connected: {sid}")
    
    @sio.event
    async def disconnect(sid):
        logger.info(f"Client disconnected: {sid}")
    
    @sio.event
    async def command(sid, data, callback):
        """Handle command from client"""
        logger.info(f"Received command: {data}")
        
        try:
            orchestrator = Orchestrator()
            
            # Stream execution updates
            async for update in orchestrator.process_command_stream(data['content']):
                await sio.emit('task_progress', update, room=sid)
            
            # Send final response
            result = await orchestrator.get_final_result()
            callback(result)
            
        except Exception as e:
            logger.error(f"Command failed: {e}")
            callback({"status": "error", "message": str(e)})
    
    @sio.event
    async def voice_input(sid, audio_data):
        """Handle voice input"""
        logger.info("Processing voice input...")
        
        orchestrator = Orchestrator()
        transcript = await orchestrator.speech_to_text(audio_data)
        
        await sio.emit('transcript', transcript, room=sid)
    
    # Attach Socket.IO to FastAPI
    socket_app = socketio.ASGIApp(sio)
    app.mount('/ws', socket_app)
    
    # Background task: broadcast system updates
    async def broadcast_system_stats():
        while True:
            try:
                orchestrator = Orchestrator()
                stats = await orchestrator.system_monitor.get_stats()
                await sio.emit('system_update', stats)
            except Exception as e:
                logger.error(f"Stats broadcast failed: {e}")
            
            await asyncio.sleep(2)  # Update every 2 seconds
    
    asyncio.create_task(broadcast_system_stats())
```

**Orchestrator** (Main Control Logic)

```python
# backend/core/orchestrator.py
import asyncio
from typing import AsyncIterator

from ai.ollama_client import OllamaClient
from ai.intent_classifier import IntentClassifier
from ai.task_planner import TaskPlanner
from core.context_manager import ContextManager
from core.memory import MemoryManager
from execution.file_manager import FileManager
from execution.process_manager import ProcessManager
from execution.app_controller import AppController
from execution.system_monitor import SystemMonitor
from execution.automation_engine import AutomationEngine
from plugins.loader import PluginLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    """
    Main orchestrator that coordinates all Eonix components
    """
    
    def __init__(self):
        # AI Components
        self.ai = OllamaClient()
        self.intent_classifier = IntentClassifier(self.ai)
        self.task_planner = TaskPlanner(self.ai)
        
        # Core Components
        self.context_manager = ContextManager()
        self.memory = MemoryManager()
        
        # Execution Components
        self.file_manager = FileManager()
        self.process_manager = ProcessManager()
        self.app_controller = AppController()
        self.system_monitor = SystemMonitor()
        self.automation_engine = AutomationEngine()
        
        # Plugin System
        self.plugin_manager = PluginLoader()
    
    async def initialize(self):
        """Initialize all components"""
        logger.info("Initializing Eonix Orchestrator...")
        
        # Check Ollama connection
        if not await self.ai.check_health():
            raise Exception("Ollama is not running. Please start Ollama first.")
        
        # Load plugins
        await self.plugin_manager.load_all()
        
        # Start system monitoring
        await self.system_monitor.start()
        
        # Start automation engine
        await self.automation_engine.start()
        
        logger.info("✅ Orchestrator initialized")
    
    async def process_command(
        self,
        command: str,
        context: dict = None
    ) -> dict:
        """
        Process a user command end-to-end
        
        Pipeline:
        1. Classify intent
        2. Retrieve context
        3. Plan tasks
        4. Execute actions
        5. Generate response
        6. Update memory
        """
        start_time = asyncio.get_event_loop().time()
        
        # Step 1: Classify intent
        intent_result = await self.intent_classifier.classify(command)
        logger.info(f"Intent: {intent_result['intent']} ({intent_result['confidence']:.2f})")
        
        # Step 2: Retrieve relevant context
        context = await self.context_manager.get_context(command, intent_result)
        
        # Step 3: Plan execution
        task_plan = await self.task_planner.plan(
            command=command,
            intent=intent_result,
            context=context
        )
        
        # Step 4: Execute tasks
        execution_results = []
        for task in task_plan['tasks']:
            result = await self._execute_task(task)
            execution_results.append(result)
        
        # Step 5: Generate natural language response
        response = await self.ai.generate_response(
            command=command,
            intent=intent_result,
            execution_results=execution_results
        )
        
        # Step 6: Update memory
        await self.memory.store_interaction(
            user_input=command,
            response=response,
            intent=intent_result,
            actions=execution_results
        )
        
        execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        return {
            "status": "success",
            "response": response,
            "actions": execution_results,
            "execution_time": execution_time,
            "metadata": {
                "intent": intent_result,
                "tasks_executed": len(execution_results)
            }
        }
    
    async def _execute_task(self, task: dict) -> dict:
        """Execute a single task"""
        action = task['action']
        params = task['params']
        
        try:
            if action.startswith('file_'):
                result = await self.file_manager.execute(action, params)
            elif action.startswith('app_'):
                result = await self.app_controller.execute(action, params)
            elif action.startswith('process_'):
                result = await self.process_manager.execute(action, params)
            elif action.startswith('plugin_'):
                plugin_name = params.get('plugin')
                result = await self.plugin_manager.execute(plugin_name, action, params)
            else:
                raise ValueError(f"Unknown action: {action}")
            
            return {
                "task": task['id'],
                "action": action,
                "status": "success",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {
                "task": task['id'],
                "action": action,
                "status": "error",
                "error": str(e)
            }
    
    async def process_command_stream(
        self,
        command: str
    ) -> AsyncIterator[dict]:
        """
        Stream execution updates in real-time
        """
        yield {"type": "start", "message": "Processing command..."}
        
        # Intent classification
        intent = await self.intent_classifier.classify(command)
        yield {"type": "intent", "data": intent}
        
        # Task planning
        plan = await self.task_planner.plan(command, intent, {})
        yield {"type": "plan", "data": plan}
        
        # Execute tasks
        for i, task in enumerate(plan['tasks']):
            yield {
                "type": "task_start",
                "task": task['id'],
                "progress": f"{i+1}/{len(plan['tasks'])}"
            }
            
            result = await self._execute_task(task)
            
            yield {
                "type": "task_complete",
                "task": task['id'],
                "result": result
            }
        
        yield {"type": "complete", "message": "All tasks executed"}
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up Orchestrator...")
        await self.system_monitor.stop()
        await self.automation_engine.stop()
```

Continue to Part 2...

# EONIX README - Part 2

## 📥 Installation

### Prerequisites

Before installing Eonix, ensure you have:

```bash
# System Requirements
- OS: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- RAM: Minimum 8GB (16GB recommended)
- Disk: 20GB free space
- CPU: 4+ cores recommended
- GPU: Optional (for faster inference)

# Software Requirements
- Python 3.10 or higher
- Node.js 18 or higher
- Git
- Ollama (for local LLM)
```

### Step 1: Install Ollama

```bash
# Linux / macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download

# Verify installation
ollama --version

# Pull Mistral model (required)
ollama pull mistral:7b

# Optional: Pull advanced models
ollama pull mistral:13b
ollama pull llama3:8b
ollama pull codellama:7b

# Start Ollama service (runs on localhost:11434)
ollama serve
```

### Step 2: Clone Eonix Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/eonix.git
cd eonix

# Project structure
eonix/
├── frontend/          # Electron + React app
├── backend/           # Python FastAPI server
├── plugins/           # Plugin directory
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env file
nano .env
```

**.env Configuration:**

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# Database
DATABASE_URL=sqlite:///./data/eonix.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ENCRYPTION_KEY=your-encryption-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/eonix.log

# Voice (Optional)
ENABLE_VOICE=true
STT_MODEL=faster-whisper-base
TTS_MODEL=piper-en_US-lessac

# System Permissions
ALLOW_SYSTEM_CONTROL=true
REQUIRE_CONFIRMATION=true  # Ask before destructive actions

# Performance
MAX_CONCURRENT_TASKS=5
CACHE_SIZE=1000

# Features
ENABLE_PLUGINS=true
ENABLE_AUTOMATION=true
ENABLE_WEB_SEARCH=false  # Future feature
```

**Initialize Database:**

```bash
# Run database migrations
python -m alembic upgrade head

# Or use the initialization script
python scripts/init_db.py
```

**Start Backend Server:**

```bash
# Development mode (with auto-reload)
python main.py

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# You should see:
# ✅ Ollama connection: healthy
# ✅ Database initialized
# ✅ Eonix Backend Ready
# 🚀 Server running on http://localhost:8000
```

### Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev

# You should see:
# ⚡ Vite dev server running
# 🖥️  Electron app starting...
# ✅ Connected to backend
```

**Build for Production:**

```bash
# Build and package Eonix
npm run build

# Platform-specific builds
npm run build:win     # Windows .exe
npm run build:mac     # macOS .dmg
npm run build:linux   # Linux .AppImage

# Output in: frontend/dist/
```

### Step 5: Verify Installation

```bash
# Test backend health
curl http://localhost:8000/health

# Response:
# {
#   "status": "healthy",
#   "ollama": "connected",
#   "database": "ready"
# }

# Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "Say hello",
  "stream": false
}'
```

---

## ⚙️ Configuration

### User Preferences

Eonix stores user preferences in `~/.eonix/config.yaml`:

```yaml
# ~/.eonix/config.yaml

user:
  name: "User"
  timezone: "America/New_York"
  language: "en"

ui:
  theme: "dark"  # dark, light, auto
  accent_color: "#3B82F6"
  font_size: 14
  animations: true
  compact_mode: false

voice:
  enabled: true
  wake_word: "hey eonix"
  voice_speed: 1.0
  volume: 0.8
  auto_listen: false

notifications:
  enabled: true
  sound: true
  position: "bottom-right"  # top-right, bottom-right, etc.
  duration: 5  # seconds

hotkeys:
  activate: "Ctrl+Space"
  voice_mode: "Ctrl+Alt+V"
  dashboard: "Ctrl+Alt+D"
  quick_command: "Ctrl+Shift+E"

ai:
  model: "mistral:7b"
  temperature: 0.7
  max_tokens: 512
  stream_responses: true

automation:
  enabled: true
  auto_organize: true
  smart_scheduling: true
  background_monitoring: true

privacy:
  store_history: true
  history_retention: 90  # days
  anonymize_data: false
  telemetry: false

system:
  startup_on_boot: true
  minimize_to_tray: true
  check_updates: true
```

### Plugin Configuration

Each plugin can have its own configuration:

```yaml
# ~/.eonix/plugins/email_assistant.yaml

plugin: email_assistant
enabled: true

gmail:
  enabled: true
  email: "your.email@gmail.com"
  credentials_file: "~/.eonix/secrets/gmail_token.json"
  check_interval: 300  # seconds
  auto_filter: true
  priority_senders:
    - "boss@company.com"
    - "important@client.com"

outlook:
  enabled: false
  # ... outlook config

actions:
  auto_reply_oonvacation: true
  mark_spam: true
  categorize_emails: true
```

### Automation Rules

Define custom automation in `~/.eonix/automations/`:

```yaml
# ~/.eonix/automations/morning_routine.yaml

name: "Morning Routine"
description: "Prepare my workspace every morning"
enabled: true

triggers:
  - type: "time"
    schedule: "weekday at 9:00 AM"
  - type: "event"
    condition: "user_login and time_is_morning"

conditions:
  - "is_weekday"
  - "time >= 08:00 and time <= 10:00"

actions:
  - action: "system.notify"
    params:
      title: "Good morning! 🌅"
      message: "Starting your morning routine..."

  - action: "system.check_health"
    params:
      notify_if_issue: true

  - action: "app.launch"
    params:
      apps:
        - name: "chrome"
          windows:
            - url: "gmail.com"
            - url: "calendar.google.com"
        - name: "vscode"
          workspace: "~/projects/current"
        - name: "terminal"
          command: "cd ~/projects && git status"

  - action: "audio.play"
    params:
      playlist: "Focus Music"
      volume: 0.3

  - action: "system.notify"
    params:
      title: "Workspace Ready ✅"
      message: "You're all set to start working!"

on_error:
  action: "system.notify"
  params:
    title: "Morning Routine Failed"
    message: "Some tasks couldn't complete. Check logs."
```

---

## 🎮 Usage

### Basic Commands

```bash
# File Management
"Organize my Downloads folder"
"Find all PDFs from last month"
"Delete duplicate images in my Photos"
"Create a backup of my Documents"

# Application Control
"Open Visual Studio Code"
"Close all Chrome tabs"
"Launch my development environment"
"Switch to Spotify"

# System Information
"What's my CPU usage?"
"How much RAM am I using?"
"Show me my disk space"
"List all running processes"

# Automation
"Run my morning routine"
"Schedule a system cleanup for tonight"
"Monitor my CPU and alert if it's too high"
"Enable Focus Mode"

# General Queries
"How do I create a React component?"
"Explain this error message: [paste error]"
"Suggest some productivity tips"
```

### Advanced Usage

**Multi-step Workflows:**

```
User: "I need to prepare for my presentation tomorrow"

Eonix: "I'll help you prepare. I'm going to:
1. Search for your latest presentation files
2. Create a backup
3. Check if PowerPoint is installed
4. Organize related resources
5. Set a reminder for tomorrow

Proceed? (yes/no)"

User: "yes"

Eonix: [Executes all steps]
"Done! I found your presentation 'Q4_Sales.pptx', 
created a backup, and set a reminder for 9 AM tomorrow. 
Your resources are in ~/Desktop/Presentation_Materials/"
```

**Context-Aware Assistance:**

```
User: "The server isn't responding"

Eonix: [Analyzes context - you're in VS Code, have terminal open]
"I see you're running a development server on port 3000. 
Let me check... The process is running but consuming 100% CPU.

Would you like me to:
1. Restart the server
2. Check the logs
3. Kill the process
4. Check for port conflicts"

User: "Check the logs"

Eonix: [Executes: tail -f server.log]
"Found the issue: Database connection timeout. 
Your Postgres container isn't running.

Should I start it? docker start postgres-dev"
```

**Smart Suggestions:**

```
Eonix: [Proactive notification]
"I noticed you've been running VS Code for 3 hours 
without saving. Would you like me to:
- Enable auto-save?
- Create a backup now?
- Remind you every 30 minutes?"
```

### Voice Control

**Wake Word Activation:**

```
User: "Hey Eonix"
Eonix: "Yes, I'm listening."

User: "What's the weather like?"
Eonix: "It's currently 72°F and sunny in New York. 
Perfect day to go outside!"

User: "Thanks, that's all"
Eonix: "You're welcome! Let me know if you need anything else."
```

**Continuous Conversation:**

```
User: "Hey Eonix, find my tax documents"
Eonix: "I found 15 files containing 'tax' in your Documents. 
The most recent is '2024_Tax_Return.pdf' from last week."

User: "Email it to my accountant"
Eonix: "I'll send '2024_Tax_Return.pdf' to john@accounting.com. 
Should I include a message?"

User: "Yes, say it's ready for review"
Eonix: "Email sent! ✅"
```

### Keyboard Shortcuts

```
Ctrl + Space              Activate Eonix (quick command)
Ctrl + Alt + V            Toggle voice mode
Ctrl + Alt + D            Show dashboard
Ctrl + Shift + E          Execute last command
Win + E                   System overview
Ctrl + Shift + A          Automation panel
Esc                       Cancel current operation
```

### System Tray Menu

Right-click the Eonix icon in system tray:

```
┌─────────────────────────────┐
│ 🟢 Eonix Active             │
├─────────────────────────────┤
│ 📊 CPU: 23% | RAM: 8.2GB    │
│ 🌐 Ollama: Connected        │
├─────────────────────────────┤
│ ⚡ Quick Actions             │
│  ├─ Clean Downloads         │
│  ├─ Enable Focus Mode       │
│  ├─ System Snapshot         │
│  └─ Morning Routine         │
├─────────────────────────────┤
│ 🎙️ Voice Mode: Off           │
│ 🤖 AI Model: Mistral 7B     │
│ 📦 Active Plugins: 6        │
├─────────────────────────────┤
│ 🔧 Settings                 │
│ 📚 Documentation            │
│ 🐛 Report Issue             │
│ ℹ️  About Eonix              │
├─────────────────────────────┤
│ ❌ Exit Eonix                │
└─────────────────────────────┘
```

---

## 🧩 Plugin Ecosystem

### Built-in Plugins

#### 1. Email Assistant

```python
# Features:
- Read, send, filter emails
- Smart categorization
- Auto-responses
- Priority inbox
- Meeting extraction

# Usage:
"Check my emails"
"Send an email to john@example.com saying the project is done"
"Show me unread emails from my boss"
"Archive all promotional emails"
```

#### 2. Developer Tools

```python
# Features:
- Git operations
- Docker management
- npm/pip commands
- IDE integration
- Code snippets

# Usage:
"Git status"
"Start my Docker containers"
"Install lodash package"
"Create a new React component called Button"
```

#### 3. Media Control

```python
# Features:
- Spotify integration
- YouTube playback
- VLC control
- Volume management
- Playlist creation

# Usage:
"Play my Focus playlist on Spotify"
"Skip this song"
"Set volume to 50%"
"Find jazz music on YouTube"
```

#### 4. Productivity Suite

```python
# Features:
- Calendar management
- Todo lists
- Note-taking
- Reminders
- Time tracking

# Usage:
"What's on my calendar today?"
"Add 'finish report' to my todo list"
"Create a note about the meeting"
"Remind me to call mom at 5 PM"
```

### Creating Custom Plugins

**Plugin Structure:**

```python
# plugins/custom/my_plugin.py

from eonix.plugin import EonixPlugin, command, schedule
from typing import Dict, Any

class MyCustomPlugin(EonixPlugin):
    """
    Custom plugin for specific automation needs
    """
    
    def __init__(self):
        super().__init__(
            name="My Custom Plugin",
            version="1.0.0",
            description="Does amazing things",
            author="Your Name",
            requires=["requests", "beautifulsoup4"]  # Dependencies
        )
        
        # Plugin-specific initialization
        self.api_key = self.config.get("api_key")
        self.cache = {}
    
    async def initialize(self):
        """Called when plugin is loaded"""
        self.logger.info(f"Initializing {self.name}")
        # Setup connections, load data, etc.
    
    @command(
        name="my_command",
        description="Does something useful",
        parameters={
            "param1": {"type": "string", "required": True},
            "param2": {"type": "int", "default": 10}
        },
        examples=[
            "do my thing with value",
            "execute my command using 25"
        ]
    )
    async def execute_my_command(
        self,
        param1: str,
        param2: int = 10
    ) -> Dict[str, Any]:
        """
        Execute the custom command
        
        This method is called when user says:
        "Eonix, do my thing with hello"
        """
        self.logger.info(f"Executing with {param1}, {param2}")
        
        try:
            # Your logic here
            result = await self.do_something(param1, param2)
            
            # Access Eonix APIs
            await self.api.notify(
                title="Task Complete",
                message=f"Processed {param1} successfully!"
            )
            
            return {
                "status": "success",
                "result": result,
                "message": "Operation completed"
            }
            
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    @schedule(cron="0 9 * * *")  # Every day at 9 AM
    async def daily_task(self):
        """Scheduled background task"""
        self.logger.info("Running daily task")
        # Automated operations
    
    @command(name="search_api")
    async def search_external_api(self, query: str):
        """Call external API"""
        async with self.http_client.get(
            f"https://api.example.com/search?q={query}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        ) as response:
            data = await response.json()
            return data
    
    async def cleanup(self):
        """Called when plugin is unloaded"""
        # Close connections, save state, etc.
        self.logger.info(f"Cleaning up {self.name}")

# Export plugin class
Plugin = MyCustomPlugin
```

**Plugin Configuration File:**

```yaml
# plugins/custom/my_plugin.yaml

plugin: my_plugin
enabled: true
version: 1.0.0

settings:
  api_key: "your-api-key-here"
  timeout: 30
  cache_size: 1000
  debug_mode: false

permissions:
  - network.http
  - system.notify
  - file.read

triggers:
  - on_startup
  - on_user_login
  - scheduled

dependencies:
  python:
    - requests>=2.28.0
    - beautifulsoup4>=4.11.0
  system:
    - curl
```

**Eonix Plugin API:**

```python
# Available in plugin via self.api

# File Operations
await self.api.file.read(path)
await self.api.file.write(path, content)
await self.api.file.delete(path)
await self.api.file.search(pattern, location)
await self.api.file.organize(folder, method)

# Application Control
await self.api.app.launch(name, params)
await self.api.app.close(name)
await self.api.app.focus(name)
await self.api.app.list()

# Process Management
await self.api.process.list()
await self.api.process.kill(pid)
await self.api.process.resource_usage(pid)

# System
await self.api.system.notify(title, message, icon)
await self.api.system.execute(command)
await self.api.system.stats()

# AI
await self.api.ai.generate(prompt, model)
await self.api.ai.classify(text, categories)
await self.api.ai.embed(text)

# Database
await self.api.db.query(sql)
await self.api.db.insert(table, data)
await self.api.db.update(table, where, data)

# Network
async with self.api.http.get(url) as response:
    data = await response.json()
```

**Installing Custom Plugin:**

```bash
# From local directory
eonix plugin install /path/to/my_plugin

# From git repository
eonix plugin install https://github.com/user/eonix-plugin

# From plugin marketplace (future feature)
eonix plugin install marketplace:weather-plugin

# List installed plugins
eonix plugin list

# Enable/disable
eonix plugin enable my_plugin
eonix plugin disable my_plugin

# Uninstall
eonix plugin uninstall my_plugin
```

---

## 📡 API Reference

### REST API

**Base URL:** `http://localhost:8000/api`

#### Execute Command

```http
POST /api/command
Content-Type: application/json

{
  "command": "organize my downloads",
  "context": {
    "user_id": "12345",
    "session_id": "abc-def"
  }
}

Response:
{
  "status": "success",
  "response": "I've organized your Downloads folder into 5 categories...",
  "actions": [
    {
      "action": "file_organize",
      "status": "success",
      "result": {
        "files_moved": 45,
        "folders_created": 5
      }
    }
  ],
  "execution_time": 1234.5
}
```

#### System Stats

```http
GET /api/system/stats

Response:
{
  "cpu": {
    "percent": 34.5,
    "cores": 8,
    "frequency": 2400
  },
  "memory": {
    "total": 16000000000,
    "used": 8200000000,
    "percent": 51.2
  },
  "disk": {
    "total": 512000000000,
    "used": 256000000000,
    "free": 256000000000,
    "percent": 50.0
  },
  "network": {
    "download_mbps": 45.3,
    "upload_mbps": 12.1
  }
}
```

#### List Processes

```http
GET /api/system/processes

Response:
[
  {
    "pid": 1234,
    "name": "chrome",
    "cpu_percent": 15.2,
    "memory_percent": 18.5,
    "status": "running"
  },
  ...
]
```

#### Create Automation

```http
POST /api/automation/create
Content-Type: application/json

{
  "name": "Auto Backup",
  "trigger": {
    "type": "schedule",
    "cron": "0 18 * * *"
  },
  "actions": [
    {
      "action": "file_backup",
      "params": {
        "source": "~/Documents",
        "destination": "/backup/drive"
      }
    }
  ]
}

Response:
{
  "id": "auto_123",
  "name": "Auto Backup",
  "status": "active",
  "next_run": "2024-02-17T18:00:00Z"
}
```

### WebSocket API

**Connection:** `ws://localhost:8000/ws`

**Events from Client:**

```javascript
// Command execution
socket.emit('command', {
  content: "what's my RAM usage?",
  user_id: "12345"
}, (response) => {
  console.log(response);
});

// Voice input
socket.emit('voice_input', audioBlob);

// Subscribe to system updates
socket.emit('subscribe', {
  events: ['system_update', 'task_progress']
});
```

**Events from Server:**

```javascript
// System updates (every 2 seconds)
socket.on('system_update', (data) => {
  console.log('CPU:', data.cpu);
  console.log('RAM:', data.memory);
});

// Task execution progress
socket.on('task_progress', (data) => {
  console.log('Step:', data.step);
  console.log('Progress:', data.percentage);
});

// Transcript from voice input
socket.on('transcript', (text) => {
  console.log('You said:', text);
});

// Notifications
socket.on('notification', (notification) => {
  console.log(notification.title, notification.message);
});
```

---

## 🔒 Security & Privacy

### Privacy Guarantees

1. **100% Local Processing**
   - All AI inference happens on your machine via Ollama
   - No data sent to external servers
   - Works completely offline

2. **Encrypted Storage**
   - Database encrypted with AES-256
   - Sensitive config files protected
   - Credentials stored in system keychain

3. **No Telemetry**
   - Zero usage tracking
   - No analytics collection
   - No crash reporting (unless you enable it)

4. **Open Source**
   - Full code transparency
   - Community audited
   - Self-hostable

### Security Features

**Permission System:**

```python
# Eonix asks before executing sensitive operations

User: "Delete all files in Downloads"

Eonix: "⚠️  This will permanently delete 156 files (2.4 GB).
        This action cannot be undone.
        
        Are you sure? (yes/no/show files)"

User: "show files"

Eonix: [Lists files]

User: "no, just delete the old ones"

Eonix: "Okay, I'll only delete files older than 30 days.
        That's 43 files (450 MB). Proceed? (yes/no)"
```

**Sandboxed Plugins:**

- Plugins run in isolated environments
- Explicit permission requests
- Resource limitations
- Can be disabled individually

**Audit Logs:**

```bash
# View all Eonix actions
cat ~/.eonix/logs/audit.log

# Example entries:
[2024-02-16 10:23:45] COMMAND | user_input="organize downloads" | status=success
[2024-02-16 10:23:47] FILE_OP | action=move | count=45 | status=success
[2024-02-16 10:30:12] APP_LAUNCH | app=chrome | status=success
[2024-02-16 11:15:33] PROCESS_KILL | pid=5432 | name=firefox | status=success
```

**Network Isolation:**

- Ollama only accessible locally
- No external API calls (unless plugin enabled)
- Firewall-friendly
- VPN compatible

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/eonix.git
cd eonix

# Backend development
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .  # Editable install

# Frontend development
cd ../frontend
npm install
npm run dev

# Run tests
npm run test          # Frontend tests
pytest                # Backend tests
```

### Project Structure (Detailed)

```
eonix/
├── frontend/
│   ├── src/
│   │   ├── main/              # Electron main process
│   │   │   ├── index.ts
│   │   │   ├── ipc.ts
│   │   │   ├── tray.ts
│   │   │   └── menu.ts
│   │   ├── renderer/          # React app
│   │   │   ├── App.tsx
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── store/
│   │   │   ├── api/
│   │   │   ├── utils/
│   │   │   └── styles/
│   │   └── preload/
│   │       └── index.ts
│   ├── public/
│   ├── electron-builder.json
│   ├── vite.config.ts
│   └── package.json
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── api/
│   │   ├── routes.py
│   │   ├── websocket.py
│   │   └── middleware.py
│   ├── ai/
│   │   ├── ollama_client.py
│   │   ├── prompts.py
│   │   ├── embeddings.py
│   │   └── ...
│   ├── core/
│   │   ├── orchestrator.py
│   │   ├── context_manager.py
│   │   └── memory.py
│   ├── execution/
│   │   ├── file_manager.py
│   │   ├── process_manager.py
│   │   └── ...
│   ├── plugins/
│   │   ├── base.py
│   │   ├── loader.py
│   │   └── builtin/
│   ├── database/
│   │   ├── models.py
│   │   └── crud.py
│   └── tests/
│
├── plugins/           # User plugins
│   ├── custom/
│   └── community/
│
├── docs/
│   ├── installation.md
│   ├── api-reference.md
│   ├── plugin-development.md
│   └── architecture.md
│
├── scripts/
│   ├── install.sh
│   ├── init_db.py
│   └── build.py
│
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── release.yml
│
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Specific test file
pytest tests/test_ai.py -v

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e

# Lint
npm run lint
python -m flake8 backend/
```

### Building from Source

```bash
# Build backend
cd backend
python setup.py bdist_wheel

# Build frontend
cd frontend
npm run build

# Build for all platforms
npm run build:all

# Output:
# eonix-1.0.0-win.exe
# eonix-1.0.0-mac.dmg
# eonix-1.0.0-linux.AppImage
```

---

## 🗺️ Roadmap

### Version 1.0 (Current)

- ✅ Core desktop automation
- ✅ Ollama/Mistral integration
- ✅ Natural language commands
- ✅ Basic plugin system
- ✅ System monitoring
- ✅ File management
- ✅ Voice control

### Version 1.1 (Q2 2024)

- 🔲 Vision capabilities (screen understanding)
- 🔲 Web browser automation (Selenium integration)
- 🔲 Advanced workflow builder (visual editor)
- 🔲 Cloud backup (optional)
- 🔲 Mobile companion app
- 🔲 Plugin marketplace

### Version 1.2 (Q3 2024)

- 🔲 Multi-device synchronization
- 🔲 Collaborative features
- 🔲 Advanced analytics
- 🔲 Custom model fine-tuning
- 🔲 API for third-party integration
- 🔲 Enterprise features

### Version 2.0 (Q4 2024)

- 🔲 Fully autonomous decision making
- 🔲 Self-learning capabilities
- 🔲 Cross-platform mobile support
- 🔲 Smart home integration
- 🔲 Advanced security features
- 🔲 Performance optimizations

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Write/update tests**
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Be respectful and constructive

### Areas We Need Help

- 🐛 Bug fixes
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🔌 Plugin development
- 🌍 Translations
- 🧪 Testing and QA

---

## ❓ FAQ

**Q: Does Eonix require internet?**
A: No! Eonix works 100% offline using local Ollama models.

**Q: How much RAM does it use?**
A: ~4-6 GB with Mistral 7B, ~8-10 GB with Mistral 13B.

**Q: Can I use GPT-4 instead of Mistral?**
A: Yes, but it requires API key and internet. Eonix supports cloud LLMs as optional fallback.

**Q: Is my data safe?**
A: Absolutely. Everything stays on your machine, encrypted at rest.

**Q: Can I use Eonix on multiple computers?**
A: Yes, but currently each instance is independent. Sync is coming in v1.2.

**Q: How do I report bugs?**
A: Open an issue on GitHub with details and logs.

**Q: Can I sell plugins?**
A: Yes! Plugin marketplace (coming soon) will support paid plugins.

**Q: What about Windows Defender / antivirus?**
A: Eonix may be flagged due to system-level access. It's safe - you can whitelist it or check the source code.

---

## 📜 License

```
MIT License

Copyright (c) 2024 Eonix Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🌟 Acknowledgments

- **Ollama** - Local LLM runtime
- **Mistral AI** - Powerful open-source models
- **Electron** - Cross-platform desktop framework
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **The Open Source Community** - For making this possible

---

## 📞 Support

- 📚 **Documentation**: https://eonix.dev/docs
- 💬 **Discord**: https://discord.gg/eonix
- 🐛 **Issues**: https://github.com/youruser/eonix/issues
- 📧 **Email**: support@eonix.dev
- 🐦 **Twitter**: @EonixAI

---

<div align="center">

**Made with ❤️ by the Eonix Team**

*"Your personal JARVIS, running locally on your laptop"*

⭐ **Star this repo if you find it useful!** ⭐

[Website](https://eonix.dev) • [Documentation](https://docs.eonix.dev) • [Community](https://discord.gg/eonix)

</div>

---

## 🎬 Final Notes

Thank you for choosing Eonix! We're building the future of human-computer interaction, one command at a time.

**Remember:**
- Start with simple commands
- Explore the plugin ecosystem
- Customize to your workflow
- Share your experience
- Contribute if you can

**"Good morning, sir. Shall we begin?"** 🤖

---

**Quick Start:**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral:7b

# 2. Clone and install Eonix
git clone https://github.com/youruser/eonix.git
cd eonix
./scripts/install.sh

# 3. Start Eonix
npm run start

# 4. Say: "Hey Eonix, introduce yourself"
```

**You're ready to go! Welcome to the future. 🚀**
