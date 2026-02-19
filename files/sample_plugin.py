# Sample Eonix Plugin Template

"""
This is a template for creating custom Eonix plugins.
Copy this file and modify it for your specific needs.
"""

from eonix.plugin import EonixPlugin, command, schedule, event
from typing import Dict, Any, Optional
import asyncio

class SamplePlugin(EonixPlugin):
    """
    Sample Plugin - Template for creating custom Eonix plugins
    
    This plugin demonstrates:
    - Basic command handling
    - Scheduled tasks
    - Event listeners
    - API access
    - Configuration management
    - Error handling
    """
    
    def __init__(self):
        super().__init__(
            name="Sample Plugin",
            version="1.0.0",
            description="A template plugin demonstrating Eonix capabilities",
            author="Your Name",
            requires=[
                "requests>=2.28.0",  # External dependencies
                "python-dateutil>=2.8.0"
            ]
        )
        
        # Plugin-specific state
        self.task_counter = 0
        self.last_execution = None
        self.cache = {}
    
    async def initialize(self):
        """
        Called when plugin is loaded.
        Use this for:
        - Loading configuration
        - Establishing connections
        - Initializing resources
        - Setting up state
        """
        self.logger.info(f"Initializing {self.name} v{self.version}")
        
        # Load configuration from ~/.eonix/plugins/sample_plugin.yaml
        self.api_key = self.config.get("api_key", "")
        self.timeout = self.config.get("timeout", 30)
        self.enabled_features = self.config.get("features", [])
        
        # Initialize any connections
        self.db_connection = await self._setup_database()
        
        self.logger.info(f"✅ {self.name} initialized successfully")
    
    @command(
        name="hello",
        description="Say hello to the user",
        parameters={
            "name": {
                "type": "string",
                "required": False,
                "default": "there",
                "description": "Name to greet"
            }
        },
        examples=[
            "say hello",
            "hello John",
            "greet me"
        ]
    )
    async def say_hello(self, name: str = "there") -> Dict[str, Any]:
        """
        Simple command example
        
        User can trigger this by saying:
        - "Eonix, say hello"
        - "Eonix, hello John"
        - "Eonix, greet me"
        """
        self.logger.info(f"Saying hello to {name}")
        
        greeting = f"Hello, {name}! I'm Eonix, your autonomous assistant. How can I help you today?"
        
        # Send a notification
        await self.api.notify(
            title="Greeting",
            message=greeting,
            icon="👋"
        )
        
        self.task_counter += 1
        
        return {
            "status": "success",
            "message": greeting,
            "metadata": {
                "name": name,
                "execution_count": self.task_counter
            }
        }
    
    @command(
        name="analyze_files",
        description="Analyze files in a directory",
        parameters={
            "directory": {
                "type": "string",
                "required": True,
                "description": "Path to directory"
            },
            "pattern": {
                "type": "string",
                "required": False,
                "default": "*",
                "description": "File pattern to match"
            }
        },
        examples=[
            "analyze files in my Documents",
            "analyze Python files in my projects folder"
        ]
    )
    async def analyze_directory(
        self,
        directory: str,
        pattern: str = "*"
    ) -> Dict[str, Any]:
        """
        More complex command demonstrating file operations
        """
        self.logger.info(f"Analyzing {directory} with pattern {pattern}")
        
        try:
            # Use Eonix File API to search for files
            files = await self.api.file.search(
                pattern=pattern,
                location=directory,
                recursive=True
            )
            
            # Analyze the files
            total_size = 0
            file_types = {}
            
            for file_path in files:
                # Get file info
                info = await self.api.file.info(file_path)
                total_size += info['size']
                
                # Count file types
                ext = info['extension']
                file_types[ext] = file_types.get(ext, 0) + 1
            
            # Generate report
            report = {
                "total_files": len(files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_types": file_types,
                "directory": directory
            }
            
            # Use AI to generate natural language summary
            summary = await self.api.ai.generate(
                prompt=f"Summarize this file analysis in one sentence: {report}",
                model="mistral:7b"
            )
            
            return {
                "status": "success",
                "summary": summary,
                "details": report,
                "files": files[:10]  # Return first 10 files
            }
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    @command(
        name="web_search",
        description="Search the web for information",
        parameters={
            "query": {
                "type": "string",
                "required": True,
                "description": "Search query"
            },
            "limit": {
                "type": "int",
                "default": 5,
                "description": "Number of results"
            }
        }
    )
    async def search_web(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Example of making external API calls
        """
        self.logger.info(f"Searching for: {query}")
        
        try:
            # Use the HTTP client from Eonix API
            async with self.api.http.get(
                url=f"https://api.example.com/search",
                params={"q": query, "limit": limit},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout
            ) as response:
                data = await response.json()
            
            # Cache the results
            self.cache[query] = data
            
            return {
                "status": "success",
                "query": query,
                "results": data['results'],
                "count": len(data['results'])
            }
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            
            # Check cache
            if query in self.cache:
                return {
                    "status": "success",
                    "query": query,
                    "results": self.cache[query]['results'],
                    "source": "cache"
                }
            
            return {
                "status": "error",
                "error": str(e)
            }
    
    @schedule(cron="0 9 * * *")  # Every day at 9 AM
    async def daily_task(self):
        """
        Scheduled background task
        
        Cron format: minute hour day month weekday
        Examples:
        - "0 9 * * *"        - 9 AM daily
        - "*/15 * * * *"     - Every 15 minutes
        - "0 9 * * 1"        - 9 AM every Monday
        - "0 0 1 * *"        - Midnight on 1st of month
        """
        self.logger.info("Running daily scheduled task")
        
        # Example: Clean up old cache entries
        self.cache.clear()
        
        # Notify user
        await self.api.notify(
            title="Daily Task Complete",
            message="Cache cleaned and system optimized"
        )
    
    @event(on="user_login")
    async def on_user_login(self, event_data: Dict):
        """
        Event listener - triggered when user logs in
        
        Available events:
        - user_login
        - user_logout
        - system_startup
        - system_shutdown
        - file_created
        - file_modified
        - file_deleted
        - app_launched
        - app_closed
        - custom events from other plugins
        """
        self.logger.info(f"User logged in: {event_data}")
        
        # Example: Show a welcome message
        await self.api.notify(
            title="Welcome back!",
            message=f"Good to see you again at {event_data['time']}"
        )
    
    @command(name="database_operation")
    async def database_example(self) -> Dict[str, Any]:
        """
        Example of database operations
        """
        try:
            # Insert data
            await self.api.db.insert(
                table="plugin_data",
                data={
                    "plugin_name": self.name,
                    "action": "example",
                    "timestamp": "2024-02-16T10:00:00"
                }
            )
            
            # Query data
            results = await self.api.db.query(
                """
                SELECT * FROM plugin_data 
                WHERE plugin_name = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
                """,
                params=[self.name]
            )
            
            return {
                "status": "success",
                "records": results
            }
            
        except Exception as e:
            self.logger.error(f"Database operation failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    @command(name="system_control")
    async def system_control_example(self) -> Dict[str, Any]:
        """
        Example of system-level operations
        """
        try:
            # Get system stats
            stats = await self.api.system.stats()
            
            # Execute system command
            result = await self.api.system.execute(
                command="echo 'Hello from plugin'",
                shell=True
            )
            
            # Launch application
            await self.api.app.launch(
                name="notepad",  # or "code", "chrome", etc.
                params={"file": "/path/to/file.txt"}
            )
            
            # Manage processes
            processes = await self.api.process.list()
            high_cpu = [p for p in processes if p['cpu_percent'] > 50]
            
            return {
                "status": "success",
                "stats": stats,
                "command_output": result,
                "high_cpu_processes": high_cpu
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    @command(name="ai_operations")
    async def ai_examples(self, text: str) -> Dict[str, Any]:
        """
        Example of AI operations
        """
        try:
            # Generate text
            response = await self.api.ai.generate(
                prompt=f"Analyze this text: {text}",
                model="mistral:7b"
            )
            
            # Classify text
            categories = ["positive", "negative", "neutral"]
            classification = await self.api.ai.classify(
                text=text,
                categories=categories
            )
            
            # Generate embeddings for similarity search
            embedding = await self.api.ai.embed(text)
            
            return {
                "status": "success",
                "analysis": response,
                "sentiment": classification,
                "embedding_size": len(embedding)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _setup_database(self):
        """
        Private method for internal use
        """
        # Create plugin-specific database table
        await self.api.db.execute(
            """
            CREATE TABLE IF NOT EXISTS plugin_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plugin_name TEXT,
                action TEXT,
                timestamp TEXT
            )
            """
        )
        return True
    
    async def cleanup(self):
        """
        Called when plugin is unloaded
        Use this for:
        - Closing connections
        - Saving state
        - Cleaning up resources
        """
        self.logger.info(f"Cleaning up {self.name}")
        
        # Save state
        await self._save_state()
        
        # Close connections
        if self.db_connection:
            await self.db_connection.close()
        
        self.logger.info(f"✅ {self.name} cleaned up successfully")
    
    async def _save_state(self):
        """Save plugin state to disk"""
        state = {
            "task_counter": self.task_counter,
            "last_execution": self.last_execution,
            "cache_size": len(self.cache)
        }
        
        await self.api.file.write(
            path="~/.eonix/plugin_state/sample_plugin.json",
            content=json.dumps(state, indent=2)
        )

# Required: Export the plugin class
Plugin = SamplePlugin


# ============================================
# Plugin Configuration File
# ============================================
"""
Create this file at: ~/.eonix/plugins/sample_plugin.yaml

plugin: sample_plugin
enabled: true
version: 1.0.0

settings:
  api_key: "your-api-key-here"
  timeout: 30
  features:
    - web_search
    - daily_tasks
    - notifications

permissions:
  - network.http       # Allow HTTP requests
  - system.notify      # Show notifications
  - file.read          # Read files
  - file.write         # Write files
  - system.execute     # Execute system commands
  - database.access    # Access database

triggers:
  - on_startup         # Run on Eonix startup
  - on_user_login      # Run on user login
  - scheduled          # Enable scheduled tasks

dependencies:
  python:
    - requests>=2.28.0
    - python-dateutil>=2.8.0
  system:
    - curl             # Optional system dependencies
"""


# ============================================
# Installation Instructions
# ============================================
"""
1. Save this file as: plugins/custom/sample_plugin.py

2. Create config file: ~/.eonix/plugins/sample_plugin.yaml

3. Install the plugin:
   ```bash
   eonix plugin install ./plugins/custom/sample_plugin.py
   ```

4. Enable the plugin:
   ```bash
   eonix plugin enable sample_plugin
   ```

5. Test the plugin:
   ```bash
   # Through Eonix chat
   "Eonix, say hello"
   "Eonix, analyze files in my Documents"
   
   # Through API
   curl -X POST http://localhost:8000/api/plugin/sample/hello \
     -H "Content-Type: application/json" \
     -d '{"name": "John"}'
   ```

6. Check logs:
   ```bash
   tail -f ~/.eonix/logs/eonix.log
   ```
"""


# ============================================
# Plugin Development Tips
# ============================================
"""
1. Use descriptive command names and parameters
2. Add comprehensive examples for each command
3. Handle errors gracefully with try/except
4. Use self.logger for debugging
5. Cache expensive operations
6. Use async/await for non-blocking operations
7. Document your code with docstrings
8. Test thoroughly before deployment
9. Version your plugin properly
10. Keep plugins focused on one task/domain

Best Practices:
- Keep commands simple and focused
- Use natural language in descriptions
- Provide helpful error messages
- Cache API responses when possible
- Clean up resources in cleanup()
- Use configuration for flexibility
- Log important events
- Handle edge cases
- Test with different inputs
- Follow Python best practices
"""
