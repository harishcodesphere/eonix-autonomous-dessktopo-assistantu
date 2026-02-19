# Eonix (JARVIS)

Eonix is a local-first, AI-powered desktop assistant built with Python (FastAPI), Electron (React), and Ollama.

## Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 16+**
- **Ollama** running locally (`ollama serve`)

### Installation

Run the automated installer:
```cmd
scripts\install.bat
```

Or manually:
1. **Backend**: `cd backend && pip install -r requirements.txt`
2. **Frontend**: `cd frontend && npm install`

### Running

Launch the entire system:
```cmd
run_eonix.bat
```

This will:
1. Start the Python backend on port 8000
2. Launch the Electron frontend app

## Architecture

- **Backend**: FastAPI, SQLAlchemy, Ollama, PyAudio
- **Frontend**: Electron, React, Tailwind CSS, Zustand
- **Communication**: WebSocket (Socket.IO)

## Configuration

Edit `config/default-config.yaml` to change:
- AI Model (default: `llama3`)
- Voice settings
- Permissions

## Verification

Check `walkthrough.md` for detailed verification steps.
