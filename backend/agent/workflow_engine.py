"""
Workflow Engine - Executes node-based automation workflows.
"""
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from memory.db import get_db, Workflow
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self):
        self.running_workflows = {}
        self.active_workflows = []

    def load_workflows(self):
        """Load active workflows from the database."""
        db = get_db()
        try:
            self.active_workflows = db.query(Workflow).filter(Workflow.active == True).all()
            logger.info(f"Loaded {len(self.active_workflows)} active workflows.")
        except Exception as e:
            logger.error(f"Failed to load workflows: {e}")
        finally:
            db.close()

    async def run_workflow(self, workflow_id: int):
        """Execute a workflow by ID."""
        logger.info(f"Starting workflow {workflow_id}...")
        db = get_db()
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                logger.error(f"Workflow {workflow_id} not found.")
                return

            data = json.loads(workflow.workflow_json)
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])
            
            # Build simple adjacency list
            graph = {node["id"]: [] for node in nodes}
            for edge in edges:
                graph[edge["source"]].append(edge["target"])

            # Find start nodes (no incoming edges or explicitly marked)
            # For simplicity, we assume triggers are start nodes
            start_nodes = [n for n in nodes if n["type"] == "trigger"]
            
            for node in start_nodes:
                await self.process_node(node, nodes, graph, {})

            logger.info(f"Workflow {workflow_id} completed.")

        except Exception as e:
            logger.error(f"Error running workflow {workflow_id}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()

    async def process_node(self, node: Dict, all_nodes: List[Dict], graph: Dict, context: Dict):
        """Process a single node and recursively process its children."""
        node_type = node["type"]
        node_id = node["id"]
        data = node.get("data", {})
        
        logger.info(f"Processing node {node_id} ({node_type})")
        
        # 1. Execute Node Logic
        if node_type == "action":
            await self._execute_action(data, context)
        elif node_type == "delay":
            await self._execute_delay(data)
        elif node_type == "condition":
            if not self._evaluate_condition(data, context):
                return # Stop branch if false

        # 2. Process Next Nodes
        children_ids = graph.get(node_id, [])
        for child_id in children_ids:
            child_node = next((n for n in all_nodes if n["id"] == child_id), None)
            if child_node:
                await self.process_node(child_node, all_nodes, graph, context)

    # ── Node Executors ─────────────────────────────────────────────

    async def _execute_action(self, data: Dict, context: Dict):
        """Execute an action node."""
        action_type = data.get("actionType", "tool")
        
        if action_type == "tool":
            tool_name = data.get("toolName")
            args = data.get("linkArgs", {})
            logger.info(f"Executing Tool: {tool_name} with {args}")
            
            # Import here to avoid circular dependencies
            from agent.orchestrator import orchestrator
            # We construct a fake plan step for the orchestrator tools
            # This is a simplification; ideally we access tools directly
            # For now, let's just print/log validation
            if tool_name == "push_notification":
                 from api.routes_ws import push_alert
                 await push_alert({
                     "type": "alert",
                     "severity": "info",
                     "title": "Workflow Action",
                     "message": args.get("message", "Workflow Executed")
                 })
            # Add more specific tool handlers or dynamic dispatch here
            
        elif action_type == "script":
            script = data.get("script", "")
            logger.info(f"Running Script: {script}")
            # Security risk: verify before running in production
            # exec(script) - DISABLED for safety in this demo

    async def _execute_delay(self, data: Dict):
        """Execute a delay node."""
        seconds = int(data.get("seconds", 0))
        logger.info(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)

    def _evaluate_condition(self, data: Dict, context: Dict) -> bool:
        """Evaluate a condition node."""
        # Simple implementation
        return True

# Global Instance
workflow_engine = WorkflowEngine()
