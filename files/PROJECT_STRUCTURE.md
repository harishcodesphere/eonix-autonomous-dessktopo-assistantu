# Eonix Project Structure

This document shows the complete file structure for the Eonix project.

```
eonix/
│
├── README.md                          # Main documentation (you're reading this!)
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore file
│
├── frontend/                          # Electron + React Desktop App
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── electron-builder.json
│   │
│   ├── public/                        # Static assets
│   │   ├── icon.png
│   │   ├── icon.icns
│   │   └── icon.ico
│   │
│   └── src/
│       ├── main/                      # Electron Main Process
│       │   ├── index.ts               # App entry point
│       │   ├── window.ts              # Window management
│       │   ├── tray.ts                # System tray
│       │   ├── menu.ts                # Application menu
│       │   ├── ipc-handlers.ts        # IPC communication
│       │   ├── shortcuts.ts           # Global shortcuts
│       │   └── updater.ts             # Auto-update logic
│       │
│       ├── preload/                   # Preload Scripts
│       │   └── index.ts               # Bridge between main and renderer
│       │
│       └── renderer/                  # React Application
│           ├── index.html
│           ├── index.tsx
│           ├── App.tsx
│           ├── vite-env.d.ts
│           │
│           ├── components/            # React Components
│           │   ├── Chat/
│           │   │   ├── ChatInterface.tsx
│           │   │   ├── MessageBubble.tsx
│           │   │   ├── InputBar.tsx
│           │   │   ├── VoiceButton.tsx
│           │   │   └── index.ts
│           │   │
│           │   ├── Dashboard/
│           │   │   ├── SystemMetrics.tsx
│           │   │   ├── ProcessList.tsx
│           │   │   ├── ResourceGraph.tsx
│           │   │   ├── QuickActions.tsx
│           │   │   ├── ActiveTasks.tsx
│           │   │   └── index.ts
│           │   │
│           │   ├── Voice/
│           │   │   ├── VoicePanel.tsx
│           │   │   ├── WaveformVisualizer.tsx
│           │   │   ├── SpeechIndicator.tsx
│           │   │   └── index.ts
│           │   │
│           │   ├── Automation/
│           │   │   ├── WorkflowBuilder.tsx
│           │   │   ├── WorkflowCard.tsx
│           │   │   ├── TaskScheduler.tsx
│           │   │   ├── TriggerConfig.tsx
│           │   │   └── index.ts
│           │   │
│           │   ├── Settings/
│           │   │   ├── SettingsPanel.tsx
│           │   │   ├── GeneralSettings.tsx
│           │   │   ├── VoiceSettings.tsx
│           │   │   ├── AISettings.tsx
│           │   │   ├── PluginSettings.tsx
│           │   │   └── index.ts
│           │   │
│           │   ├── Plugins/
│           │   │   ├── PluginManager.tsx
│           │   │   ├── PluginCard.tsx
│           │   │   ├── PluginDetails.tsx
│           │   │   └── index.ts
│           │   │
│           │   └── Common/
│           │       ├── Sidebar.tsx
│           │       ├── Header.tsx
│           │       ├── StatusBar.tsx
│           │       ├── Button.tsx
│           │       ├── Input.tsx
│           │       ├── Modal.tsx
│           │       ├── Loader.tsx
│           │       └── index.ts
│           │
│           ├── hooks/                 # Custom React Hooks
│           │   ├── useWebSocket.ts
│           │   ├── useVoiceInput.ts
│           │   ├── useSystemStats.ts
│           │   ├── useCommands.ts
│           │   ├── useTheme.ts
│           │   ├── useSettings.ts
│           │   └── index.ts
│           │
│           ├── store/                 # State Management (Zustand)
│           │   ├── chatStore.ts
│           │   ├── systemStore.ts
│           │   ├── settingsStore.ts
│           │   ├── pluginStore.ts
│           │   ├── automationStore.ts
│           │   └── index.ts
│           │
│           ├── api/                   # API Clients
│           │   ├── backend.ts         # REST API client
│           │   ├── websocket.ts       # WebSocket client
│           │   ├── ipc.ts             # Electron IPC wrapper
│           │   └── index.ts
│           │
│           ├── utils/                 # Utility Functions
│           │   ├── formatters.ts
│           │   ├── validators.ts
│           │   ├── helpers.ts
│           │   └── index.ts
│           │
│           ├── types/                 # TypeScript Types
│           │   ├── chat.ts
│           │   ├── system.ts
│           │   ├── plugin.ts
│           │   ├── automation.ts
│           │   └── index.ts
│           │
│           └── styles/                # Styling
│               ├── globals.css
│               ├── themes.ts
│               └── tailwind.config.js
│
├── backend/                           # Python FastAPI Server
│   ├── main.py                        # Application entry point
│   ├── config.py                      # Configuration management
│   ├── requirements.txt               # Python dependencies
│   ├── requirements-dev.txt           # Development dependencies
│   ├── setup.py                       # Package setup
│   ├── .env.example                   # Example environment variables
│   │
│   ├── api/                           # API Layer
│   │   ├── __init__.py
│   │   ├── routes.py                  # REST API routes
│   │   ├── websocket.py               # WebSocket handlers
│   │   ├── middleware.py              # Custom middleware
│   │   └── dependencies.py            # Dependency injection
│   │
│   ├── ai/                            # AI/ML Layer
│   │   ├── __init__.py
│   │   ├── ollama_client.py           # Ollama integration
│   │   ├── prompts.py                 # System prompts
│   │   ├── embeddings.py              # Vector embeddings
│   │   ├── intent_classifier.py       # Intent detection
│   │   ├── task_planner.py            # Task decomposition
│   │   ├── entity_extractor.py        # Named entity recognition
│   │   └── response_generator.py      # Natural language generation
│   │
│   ├── core/                          # Core Business Logic
│   │   ├── __init__.py
│   │   ├── orchestrator.py            # Main orchestrator
│   │   ├── context_manager.py         # Conversation context
│   │   ├── memory.py                  # Long-term memory
│   │   └── permission_manager.py      # Permission system
│   │
│   ├── execution/                     # System Execution Layer
│   │   ├── __init__.py
│   │   ├── file_manager.py            # File operations
│   │   ├── process_manager.py         # Process control
│   │   ├── app_controller.py          # Application control
│   │   ├── system_monitor.py          # Resource monitoring
│   │   ├── window_manager.py          # Window management
│   │   ├── automation_engine.py       # Workflow automation
│   │   └── scheduler.py               # Task scheduling
│   │
│   ├── voice/                         # Voice Processing
│   │   ├── __init__.py
│   │   ├── speech_to_text.py          # STT with Whisper
│   │   ├── text_to_speech.py          # TTS with Piper
│   │   ├── wake_word.py               # Wake word detection
│   │   └── audio_processor.py         # Audio processing
│   │
│   ├── plugins/                       # Plugin System
│   │   ├── __init__.py
│   │   ├── base.py                    # Plugin base class
│   │   ├── loader.py                  # Plugin loader
│   │   ├── manager.py                 # Plugin manager
│   │   │
│   │   └── builtin/                   # Built-in Plugins
│   │       ├── __init__.py
│   │       ├── email_assistant.py
│   │       ├── dev_tools.py
│   │       ├── media_control.py
│   │       ├── productivity.py
│   │       ├── browser_automation.py
│   │       └── cloud_sync.py
│   │
│   ├── database/                      # Database Layer
│   │   ├── __init__.py
│   │   ├── models.py                  # SQLAlchemy models
│   │   ├── crud.py                    # CRUD operations
│   │   ├── connection.py              # Database connection
│   │   │
│   │   └── migrations/                # Alembic migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │
│   ├── utils/                         # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py                  # Logging setup
│   │   ├── security.py                # Encryption/auth
│   │   ├── helpers.py                 # Helper functions
│   │   └── decorators.py              # Custom decorators
│   │
│   └── tests/                         # Test Suite
│       ├── __init__.py
│       ├── conftest.py                # Pytest configuration
│       ├── test_api.py
│       ├── test_ai.py
│       ├── test_execution.py
│       ├── test_plugins.py
│       └── test_database.py
│
├── plugins/                           # User Plugins Directory
│   ├── custom/                        # Custom user plugins
│   │   └── .gitkeep
│   │
│   └── community/                     # Community plugins
│       └── .gitkeep
│
├── scripts/                           # Utility Scripts
│   ├── install.sh                     # Installation script
│   ├── install.bat                    # Windows installation
│   ├── init_db.py                     # Database initialization
│   ├── build.py                       # Build script
│   ├── test.sh                        # Test runner
│   └── deploy.sh                      # Deployment script
│
├── docs/                              # Documentation
│   ├── installation.md
│   ├── quickstart.md
│   ├── api-reference.md
│   ├── plugin-development.md
│   ├── architecture.md
│   ├── contributing.md
│   │
│   ├── images/
│   │   ├── logo.png
│   │   ├── screenshot-main.png
│   │   └── architecture-diagram.png
│   │
│   └── examples/
│       ├── basic-commands.md
│       ├── automation-examples.md
│       └── plugin-examples.md
│
├── config/                            # Configuration Files
│   ├── default-config.yaml
│   ├── automation-examples.yaml
│   └── plugin-examples.yaml
│
├── data/                              # Data Directory (runtime)
│   ├── .gitignore
│   ├── database/
│   │   └── eonix.db
│   ├── chroma/                        # Vector database
│   ├── cache/
│   └── logs/
│       ├── eonix.log
│       └── audit.log
│
├── .github/                           # GitHub Configuration
│   ├── workflows/
│   │   ├── test.yml                   # CI tests
│   │   ├── build.yml                  # Build workflow
│   │   └── release.yml                # Release workflow
│   │
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── plugin_submission.md
│   │
│   └── PULL_REQUEST_TEMPLATE.md
│
└── .vscode/                           # VS Code Configuration
    ├── settings.json
    ├── launch.json
    ├── tasks.json
    └── extensions.json
```

## User Data Directory Structure

When Eonix is installed, it creates configuration in the user's home directory:

```
~/.eonix/                              # User Data Directory
│
├── config.yaml                        # Main configuration
├── secrets.yaml                       # Encrypted secrets
│
├── plugins/                           # Plugin configurations
│   ├── email_assistant.yaml
│   ├── dev_tools.yaml
│   ├── media_control.yaml
│   └── custom_plugin.yaml
│
├── automations/                       # Automation workflows
│   ├── morning_routine.yaml
│   ├── auto_backup.yaml
│   └── focus_mode.yaml
│
├── data/                              # Runtime data
│   ├── eonix.db                       # SQLite database
│   ├── chroma/                        # Vector embeddings
│   ├── cache/                         # Temporary cache
│   └── plugin_state/                  # Plugin state files
│
├── logs/                              # Log files
│   ├── eonix.log                      # Main log
│   ├── audit.log                      # Audit trail
│   └── error.log                      # Error log
│
├── backups/                           # Automated backups
│   ├── 2024-02-16_config_backup.tar.gz
│   └── 2024-02-16_db_backup.db
│
└── secrets/                           # API keys & credentials
    ├── gmail_token.json
    ├── github_token.txt
    └── .gitignore
```

## Development Environment Files

Additional files for development:

```
.env                                   # Local environment variables
.env.example                           # Example environment file
.gitignore                             # Git ignore patterns
.eslintrc.json                         # ESLint configuration
.prettierrc                            # Prettier configuration
.flake8                                # Python linting
pytest.ini                             # Pytest configuration
mypy.ini                               # Type checking
```

## Build Output Directory

After building the application:

```
frontend/dist/                         # Distribution builds
├── eonix-1.0.0-win.exe               # Windows installer
├── eonix-1.0.0-mac.dmg               # macOS disk image
├── eonix-1.0.0-linux.AppImage        # Linux AppImage
└── latest.yml                         # Update metadata
```

## Key Files Explained

### Configuration Files

- **frontend/package.json** - Node.js dependencies and scripts
- **backend/requirements.txt** - Python dependencies
- **backend/config.py** - Application configuration
- **.env** - Environment variables (not committed)
- **config.yaml** - User preferences

### Entry Points

- **frontend/src/main/index.ts** - Electron app entry
- **frontend/src/renderer/index.tsx** - React app entry
- **backend/main.py** - FastAPI server entry

### Core Components

- **backend/core/orchestrator.py** - Main control flow
- **backend/ai/ollama_client.py** - LLM integration
- **frontend/src/components/Chat/ChatInterface.tsx** - Main UI
- **backend/execution/** - System operations

### Plugin System

- **backend/plugins/base.py** - Plugin base class
- **backend/plugins/loader.py** - Plugin loading logic
- **backend/plugins/builtin/** - Pre-installed plugins

### Database

- **backend/database/models.py** - Database schema
- **backend/database/crud.py** - Database operations
- **data/eonix.db** - SQLite database file

## File Naming Conventions

### Python Files
- `snake_case.py` for modules
- `PascalCase` for classes
- `snake_case` for functions/methods

### TypeScript/React Files
- `PascalCase.tsx` for components
- `camelCase.ts` for utilities
- `index.ts` for barrel exports

### Configuration Files
- `kebab-case.yaml` for config
- `kebab-case.json` for JSON
- `.lowercase` for dotfiles

## Important Notes

1. **Never commit** `.env` or `secrets.yaml` files
2. **Always update** `requirements.txt` when adding Python packages
3. **Run tests** before committing changes
4. **Update docs** when adding new features
5. **Version plugins** properly for compatibility

## Quick Navigation

- Configuration: `backend/config.py`, `~/.eonix/config.yaml`
- Main UI: `frontend/src/renderer/components/Chat/ChatInterface.tsx`
- AI Engine: `backend/ai/ollama_client.py`
- System Control: `backend/execution/`
- Plugin Development: `backend/plugins/base.py`, `docs/plugin-development.md`
- Database: `backend/database/models.py`
- Tests: `backend/tests/`, `frontend/src/**/*.test.tsx`

## Getting Started

1. Clone the repository
2. Install dependencies (see README.md)
3. Copy `.env.example` to `.env`
4. Run `python scripts/init_db.py`
5. Start backend: `python main.py`
6. Start frontend: `npm run dev`

---

**This structure is designed for:**
- 📦 Modularity - Easy to add features
- 🧪 Testability - Comprehensive test coverage
- 📚 Maintainability - Clear organization
- 🔌 Extensibility - Plugin system
- 🚀 Scalability - Ready for growth
