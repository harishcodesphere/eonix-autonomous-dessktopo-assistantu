from plugins.manager import PluginManager
from plugins.base import PluginBase

class MockPlugin(PluginBase):
    name = "Mock Plugin"
    description = "For testing"
    
    async def execute(self, action, params):
        if action == "test":
            return {"status": "ok"}
        return None

def test_plugin_loading(mocker):
    manager = PluginManager()
    # Manually register a mock plugin since we can't easily load from disk in unit test without complex setup
    manager.plugins["mock"] = MockPlugin()
    
    plugin = manager.get_plugin("mock")
    assert plugin is not None
    assert plugin.name == "Mock Plugin"

# Integration test would involve writing a dummy plugin file and loading it
