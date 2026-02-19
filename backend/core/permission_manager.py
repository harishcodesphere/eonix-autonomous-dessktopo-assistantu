"""
Eonix Permission Manager
Controls user authorization for sensitive system operations.
"""
from loguru import logger
from config import settings


class PermissionManager:
    """
    Manages permissions for system operations.
    Ensures destructive or sensitive actions require confirmation.
    """

    # Actions that always require explicit user confirmation
    DANGEROUS_ACTIONS = {
        "file_delete", "file_move", "file_organize",
        "process_kill",
        "app_close",
        "system_shutdown", "system_restart",
    }

    # Actions that are always allowed
    SAFE_ACTIONS = {
        "system_stats", "process_list", "file_list", "file_search",
        "ai_respond", "notify_user",
    }

    def __init__(self):
        self.require_confirmation = settings.REQUIRE_CONFIRMATION
        self.allow_system_control = settings.ALLOW_SYSTEM_CONTROL
        self._pending_confirmations: dict[str, dict] = {}

    def check_permission(self, action: str, params: dict = None) -> dict:
        """
        Check if an action is permitted.
        Returns: {allowed: bool, requires_confirmation: bool, message: str}
        """
        if not self.allow_system_control and action not in self.SAFE_ACTIONS:
            return {
                "allowed": False,
                "requires_confirmation": False,
                "message": f"System control is disabled. Cannot execute: {action}",
            }

        if action in self.SAFE_ACTIONS:
            return {"allowed": True, "requires_confirmation": False, "message": "OK"}

        if action in self.DANGEROUS_ACTIONS and self.require_confirmation:
            return {
                "allowed": True,
                "requires_confirmation": True,
                "message": f"Action '{action}' requires user confirmation.",
            }

        return {"allowed": True, "requires_confirmation": False, "message": "OK"}

    def request_confirmation(self, action_id: str, action: str, description: str) -> dict:
        """Register a pending confirmation request."""
        self._pending_confirmations[action_id] = {
            "action": action,
            "description": description,
            "status": "pending",
        }
        logger.info(f"Confirmation requested for: {action} — {description}")
        return {
            "action_id": action_id,
            "message": f"⚠️ {description}\nDo you want to proceed? (yes/no)",
        }

    def confirm(self, action_id: str) -> bool:
        """Confirm a pending action."""
        if action_id in self._pending_confirmations:
            self._pending_confirmations[action_id]["status"] = "confirmed"
            logger.info(f"Action confirmed: {action_id}")
            return True
        return False

    def deny(self, action_id: str) -> bool:
        """Deny a pending action."""
        if action_id in self._pending_confirmations:
            self._pending_confirmations[action_id]["status"] = "denied"
            logger.info(f"Action denied: {action_id}")
            return True
        return False
