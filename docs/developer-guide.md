# Eonix Developer Guide

## Plugin Development

Eonix supports a plugin system to extend functionality.

### Plugin Structure
Create a new file in `backend/plugins/user/my_plugin.py`:

```python
from plugins.base import PluginBase

class MyPlugin(PluginBase):
    name = "My Plugin"
    description = "Does something cool"
    
    async def execute(self, action: str, params: dict):
        if action == "hello":
            return {"message": "Hello from plugin!"}
        return {"error": "Unknown action"}
        
    def get_commands(self):
        return [
            {"name": "hello", "description": "Say hello"}
        ]

Plugin = MyPlugin
```

### API Reference

#### REST API (`http://localhost:8000`)
-   `POST /api/command`: Execute natural language command.
-   `GET /api/system/stats`: Get current system metrics.
-   `GET /api/plugins`: List available plugins.

#### WebSocket Events
-   **Emit**: `command` ({content: "..."})
-   **Listen**: `response` ({response: "...", intent: "..."})
-   **Listen**: `system_stats` ({cpu: {...}, memory: {...}})
