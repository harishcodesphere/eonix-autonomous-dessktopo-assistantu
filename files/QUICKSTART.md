# 🚀 Eonix - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Install Ollama (2 minutes)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model (this will download ~4GB)
ollama pull mistral:7b

# Verify it's working
ollama run mistral:7b
>>> Hello! How are you?
>>> [Should get a response]
>>> /bye
```

### 2. Setup Eonix Backend (2 minutes)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b
DATABASE_URL=sqlite:///./data/eonix.db
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
LOG_LEVEL=INFO
ENABLE_VOICE=true
ALLOW_SYSTEM_CONTROL=true
REQUIRE_CONFIRMATION=true
EOF

# Initialize database
python -c "from database.models import init_db; import asyncio; asyncio.run(init_db())"

# Start backend
python main.py
# Should see: "✅ Eonix Backend Ready" on http://localhost:8000
```

### 3. Setup Eonix Frontend (1 minute)

```bash
cd frontend

# Install dependencies
npm install

# Start the app
npm run dev

# Electron window should open
```

## 🎯 First Commands to Try

Once Eonix is running, try these commands:

### System Information
```
"What's my CPU usage?"
"Show me system stats"
"How much RAM am I using?"
"What's my disk space?"
```

### File Management
```
"List files in my Downloads folder"
"Find all PDFs in my Documents"
"What's the largest file on my desktop?"
```

### Application Control
```
"Open Visual Studio Code"
"Close all Chrome windows"
"List running applications"
```

### Simple Automation
```
"Remind me to take a break in 30 minutes"
"Create a folder called TestProject on my desktop"
```

## 🎙️ Voice Control

1. Click the microphone button or press `Ctrl+Alt+V`
2. Say: "Hey Eonix"
3. Wait for the listening indicator (red pulse)
4. Give your command
5. Eonix will respond with voice and text

## 🔧 Quick Configuration

Edit `~/.eonix/config.yaml` to customize:

```yaml
ui:
  theme: "dark"  # or "light"
  
voice:
  wake_word: "hey eonix"  # or "jarvis", "computer"
  
hotkeys:
  activate: "Ctrl+Space"
  
ai:
  model: "mistral:7b"  # or "mistral:13b" for better quality
```

## 🆘 Troubleshooting

**Eonix can't connect to Ollama:**
```bash
# Make sure Ollama is running
ollama serve

# Check if it's accessible
curl http://localhost:11434/api/tags
```

**Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use a different port
uvicorn main:app --port 8001
```

**Voice not working:**
```bash
# Check microphone permissions
# Linux: make sure pulseaudio/pipewire is running
# macOS: System Preferences > Security > Microphone > Allow Eonix
# Windows: Settings > Privacy > Microphone > Allow apps
```

## 📚 Next Steps

1. **Explore the Dashboard** - Check system metrics and running tasks
2. **Try Automation** - Create your first automated workflow
3. **Install Plugins** - Browse built-in and community plugins
4. **Voice Commands** - Practice using voice for hands-free control
5. **Custom Plugin** - Build your first plugin for specific needs

## 🎯 Example Workflows

### Developer Morning Routine
```
"Hey Eonix, run my morning routine"

Actions:
1. Open VS Code with yesterday's project
2. Start Docker containers
3. Open Chrome with dev tools
4. Start Spotify (Focus playlist)
5. Show today's GitHub notifications
```

### File Organization
```
"Organize my Downloads by type and date"

Actions:
1. Scan Downloads folder
2. Group by: Images, Documents, Videos, Archives, Other
3. Create dated subfolders
4. Move files
5. Remove duplicates
6. Report results
```

### System Health Check
```
"Check my system health"

Actions:
1. CPU usage analysis
2. Memory check
3. Disk space review
4. Temperature monitoring
5. Process optimization suggestions
6. Recommend cleanup actions
```

## 💡 Pro Tips

1. **Use Natural Language** - Don't worry about exact syntax
   - ✅ "find my python files from last week"
   - ✅ "where are my python files from the past 7 days"
   - ✅ "show python stuff I worked on recently"

2. **Context Matters** - Eonix remembers your conversation
   - "Find my tax documents"
   - "Email them to my accountant"
   - "Also include the receipts from January"

3. **Ask for Confirmation** - Eonix asks before destructive actions
   - "Delete old downloads"
   - Eonix: "I found 45 files older than 30 days (2.3 GB). Delete? (yes/no/show)"

4. **Keyboard Shortcuts** - Faster than mouse
   - `Ctrl+Space` - Quick command
   - `Ctrl+Alt+V` - Voice mode
   - `Ctrl+Alt+D` - Dashboard

5. **System Tray** - Right-click for quick actions
   - Quick system stats
   - Enable focus mode
   - Run saved workflows

## 🎓 Learning Resources

- **Full Documentation**: See README.md for complete details
- **Plugin Development**: Check `docs/plugin-development.md`
- **API Reference**: See `docs/api-reference.md`
- **Community Discord**: Join for support and tips

---

## 🚀 You're Ready!

```bash
# Start your JARVIS experience
npm run start

# Say: "Hey Eonix, what can you do?"
```

**Welcome to the future of personal computing! 🤖**
