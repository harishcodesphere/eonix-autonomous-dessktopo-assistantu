"""
Debug script for System Monitor.
Instantiates the monitor and simulates alerts.
"""
import asyncio
import sys
import os

# Adjust path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.monitor import SystemMonitor

async def mock_push_alert(alert):
    print(f"\n[MOCK WEBSOCKET] Sending Alert:")
    print(f"Title: {alert.get('title')}")
    print(f"Severity: {alert.get('severity')}")
    print(f"Message: {alert.get('message')}")
    print("-" * 30)

async def test_monitor():
    print("Initializing System Monitor...")
    monitor = SystemMonitor(check_interval=2) # Fast check for debug
    monitor.on_alert(mock_push_alert)
    
    # Mock psutil to force alerts (monkey patching)
    import psutil
    
    # Force high Memory
    original_vm = psutil.virtual_memory
    class MockMem:
        percent = 95.0
    psutil.virtual_memory = lambda: MockMem()
    
    print("Starting Monitor Loop (Run for 5 seconds)...")
    asyncio.create_task(monitor.start())
    
    await asyncio.sleep(5)
    
    print("Stopping Monitor...")
    monitor.stop()
    
    # Restore
    psutil.virtual_memory = original_vm
    print("Test Complete.")

if __name__ == "__main__":
    try:
        asyncio.run(test_monitor())
    except KeyboardInterrupt:
        pass
