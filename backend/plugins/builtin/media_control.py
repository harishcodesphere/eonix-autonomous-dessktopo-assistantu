import os
import sys
# Add parent to path to import PluginBase
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loader import PluginBase

class MediaControlPlugin(PluginBase):
    def __init__(self):
        super().__init__("Media Control")

    async def initialize(self):
        print("Media Control Plugin Initialized")

    async def execute(self, action: str, params: dict):
        if action == "volume_up":
            # Mock volume increase
            return {"status": "success", "message": "Volume increased"}
        elif action == "play_pause":
            return {"status": "success", "message": "Playback toggled"}
        return {"status": "error", "message": "Action not found"}

Plugin = MediaControlPlugin
