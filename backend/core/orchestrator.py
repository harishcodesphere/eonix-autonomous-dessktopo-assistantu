"""
Eonix Orchestrator
Central coordinator that processes commands through the full AI pipeline:
Intent Classification → Task Planning → Execution → Response Generation.
"""
import json
from loguru import logger
from ai.ollama_client import OllamaClient
from ai.intent_classifier import IntentClassifier
from ai.task_planner import TaskPlanner
from ai.entity_extractor import EntityExtractor
from ai.response_generator import ResponseGenerator
from core.context_manager import ContextManager
from core.permission_manager import PermissionManager
from execution.file_manager import FileManager
from execution.process_manager import ProcessManager
from execution.app_controller import AppController
from execution.system_monitor import SystemMonitor
from execution.automation_engine import AutomationEngine

class Orchestrator:
    """Main orchestrator — the brain of Eonix."""

    def __init__(self):
        self.ai = OllamaClient()
        self.intent_classifier = IntentClassifier(self.ai)
        self.task_planner = TaskPlanner(self.ai)
        self.entity_extractor = EntityExtractor(self.ai)
        self.response_generator = ResponseGenerator(self.ai)
        self.context = ContextManager()
        self.permissions = PermissionManager()
        self.file_manager = FileManager()
        self.process_manager = ProcessManager()
        self.app_controller = AppController()
        self.system_monitor = SystemMonitor()
        self.automation_engine = AutomationEngine()

    async def process_command(self, command: str) -> dict:
        """
        Process a user command through the full pipeline.
        Returns a structured response with status, data, and message.
        """
        logger.info(f"Processing command: {command}")

        try:
            # Step 1: Classify intent
            intent = await self.intent_classifier.classify(command)
            logger.info(f"Intent: {intent.get('intent')} (confidence: {intent.get('confidence', 0)})")

            # Step 2: Get context
            context = await self.context.get_context(command, intent)

            # Step 3: Execute based on intent
            result = await self._execute_intent(command, intent, context)

            # Step 4: Store interaction in context
            response_text = result.get("message", result.get("response", "Done."))
            self.context.add_interaction(command, response_text, intent)

            return result

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {"status": "error", "message": f"Something went wrong: {str(e)}"}

    async def _execute_intent(self, command: str, intent: dict, context: dict) -> dict:
        """Route and execute based on classified intent."""
        intent_type = intent.get("intent", "general_query")

        handlers = {
            "system_info": self._handle_system_info,
            "file_operation": self._handle_file_operation,
            "app_control": self._handle_app_control,
            "general_query": self._handle_general_query,
            "automation": self._handle_automation,
            "settings": self._handle_settings,
            "macro": self._handle_macro, # Support for multi-step macros
        }

        handler = handlers.get(intent_type, self._handle_general_query)
        return await handler(command, intent, context)

    async def _handle_automation(self, command: str, intent: dict, context: dict) -> dict:
        """Handle automation tasks like typing."""
        action = intent.get("action", "type")
        entities = intent.get("entities", {})
        
        # Extract text/key from entities or infer from command
        if action == "type":
            text = entities.get("text")
            if not text:
                 # Fallback: remove "type" keyword from command
                 text = command.lower().replace("type", "", 1).strip()
            
            return await self.automation_engine.type_text(text)
            
        elif action == "press":
            key = entities.get("key")
            return await self.automation_engine.press_key(key)

        return {"status": "error", "message": f"Unknown automation action: {action}"}

    async def _handle_macro(self, command: str, intent: dict, context: dict) -> dict:
        """Handle multi-step macro intents."""
        steps = intent.get("actions", [])
        results = []
        last_app_name = None

        for step_intent in steps:
            # Recursive execution for each step
            res = await self._execute_intent(command, step_intent, context)
            results.append(res)
            
            # If this step launched an app, track its name
            if res.get("intent") == "app_control" and res.get("app_name"):
                last_app_name = res.get("app_name")

            # Delay logic
            import asyncio
            if res.get("intent") == "app_control" and res.get("status") == "success":
                logger.info("Waiting for app to initialize...")
                await asyncio.sleep(3.0)
                
                # Attempt to focus the app if we know its name
                if last_app_name:
                    logger.info(f"Ensuring focus on {last_app_name}...")
                    await self.app_controller.focus(last_app_name)
                    await asyncio.sleep(0.5) # Wait a bit after focusing
            else:
                await asyncio.sleep(0.5)
            
        return {
            "status": "success", 
            "intent": "macro", 
            "message": f"Executed {len(results)} steps.",
            "steps": results
        }

    async def _handle_system_info(self, command: str, intent: dict, context: dict) -> dict:
        """Handle system information requests."""
        stats = await self.system_monitor.get_stats()
        return {
            "status": "success",
            "intent": "system_info",
            "data": stats,
            "message": self._format_stats(stats),
        }

    async def _handle_file_operation(self, command: str, intent: dict, context: dict) -> dict:
        """Handle file operations."""
        action = intent.get("action", "list")
        entities = intent.get("entities", {})
        path = entities.get("file_path", entities.get("path", "."))

        perm = self.permissions.check_permission(f"file_{action}")
        if not perm["allowed"]:
            return {"status": "denied", "message": perm["message"]}

        if perm.get("requires_confirmation"):
            return {
                "status": "confirmation_required",
                "message": f"⚠️ {action} on '{path}' requires confirmation. Proceed?",
                "action": f"file_{action}",
                "params": {"path": path},
            }

        if action in ("list", "search", "inferred"):
            files = self.file_manager.list_files(path)
            return {
                "status": "success",
                "intent": "file_operation",
                "data": files,
                "message": f"Found {len(files)} items in {path}",
            }

        return {"status": "success", "message": f"File operation '{action}' acknowledged."}

    async def _handle_app_control(self, command: str, intent: dict, context: dict) -> dict:
        """Handle application control."""
        action = intent.get("action", "launch")
        entities = intent.get("entities", {})
        app_name = entities.get("app_name", "")

        if action in ("launch", "open", "start", "inferred"):
            if app_name:
                result = await self.app_controller.launch(app_name)
                return {"status": result["status"], "intent": "app_control", "message": result["message"]}
            else:
                # Fall through to AI for clarification
                response = await self.ai.generate_response(command)
                return {"status": "success", "response": response}

        if action in ("close", "quit"):
            result = await self.app_controller.close(app_name)
            return {"status": result["status"], "intent": "app_control", "message": result["message"]}

        return {"status": "success", "message": f"App control '{action}' for '{app_name}' acknowledged."}

    async def _handle_general_query(self, command: str, intent: dict, context: dict) -> dict:
        """Handle general conversation queries."""
        from ai.prompts import get_prompt
        system_prompt = get_prompt("assistant")

        # Include recent context in the prompt
        context_str = ""
        if context.get("recent_history"):
            context_str = "\n\nRecent conversation:\n"
            for h in context["recent_history"][-3:]:
                context_str += f"User: {h['user_input']}\nEonix: {h['response']}\n"

        full_prompt = f"{context_str}\nUser: {command}"
        response = await self.ai.generate_response(full_prompt, system_prompt=system_prompt)

        return {"status": "success", "intent": "general_query", "response": response}

    async def _handle_automation(self, command: str, intent: dict, context: dict) -> dict:
        """Handle automation requests."""
        return {
            "status": "success",
            "intent": "automation",
            "message": "Automation capability registered. Use the Automation panel to configure.",
        }

    async def _handle_settings(self, command: str, intent: dict, context: dict) -> dict:
        """Handle settings changes."""
        return {
            "status": "success",
            "intent": "settings",
            "message": "Settings can be configured from the Settings panel.",
        }

    def _format_stats(self, stats: dict) -> str:
        """Format system stats into a readable summary."""
        cpu = stats.get("cpu", {})
        mem = stats.get("memory", {})
        disk = stats.get("disk", {})

        parts = [
            f"CPU: {cpu.get('percent', 0)}% ({cpu.get('cores', 0)} cores)",
            f"RAM: {mem.get('used_gb', 0)}/{mem.get('total_gb', 0)} GB ({mem.get('percent', 0)}%)",
            f"Disk: {disk.get('used_gb', 0)}/{disk.get('total_gb', 0)} GB ({disk.get('percent', 0)}%)",
        ]

        battery = stats.get("battery")
        if battery:
            parts.append(f"Battery: {battery['percent']}% {'🔌' if battery['plugged'] else '🔋'}")

        return " | ".join(parts)


# Singleton instance
orchestrator = Orchestrator()
