"""
Example Plugin — Hello World
Demonstrates the EONIX plugin system.
"""
__version__ = "1.0"

def register(tools):
    """Register this plugin's tools with the ToolRegistry."""
    # This is an example plugin — it doesn't add real tools.
    # To add a tool, do something like:
    # tools._tools["my_custom_tool"] = my_handler_function
    print("📦 Example plugin loaded (no tools registered)")
