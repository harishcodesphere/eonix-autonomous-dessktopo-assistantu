import os
import shutil
import time
import json
import asyncio
from typing import List, Dict, Any, Optional
from .tool_result import ToolResult

class FileOrganizer:
    """
    AI-powered file organizer.
    Scans a directory, analyzes files, and suggestions structure.
    """

    def __init__(self):
        self.last_plan = []
        # Common text extensions to read
        self.text_extensions = {
            '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', 
            '.csv', '.log', '.ini', '.cfg', '.yaml', '.yml', '.c', '.cpp', 
            '.h', '.java', '.go', '.rs', '.php', '.rb', '.sh', '.bat'
        }

    def scan_directory(self, path: str) -> Dict[str, Any]:
        """Scans directory and returns file list with context."""
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if not os.path.isdir(path):
            return {"error": f"Not a directory: {path}"}

        files_data = []
        try:
            # Non-recursive scan for safety
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        name = entry.name
                        # Skip hidden files
                        if name.startswith('.'): continue
                        
                        ext = os.path.splitext(name)[1].lower()
                        context = ""
                        
                        # Read snippet for text files
                        if ext in self.text_extensions:
                            try:
                                with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
                                    context = f.read(500).replace('\n', ' ')
                            except Exception:
                                context = "[Error reading file]"
                        
                        files_data.append({
                            "name": name,
                            "extension": ext,
                            "context": context
                        })
        except Exception as e:
            return {"error": str(e)}

        return {"path": path, "files": files_data}

    def execute_move(self, base_path: str, plan: List[Dict[str, str]]) -> ToolResult:
        """Executes the specific move plan."""
        success_count = 0
        errors = []

        for item in plan:
            filename = item.get('filename')
            target_folder = item.get('target_folder')
            
            if not filename or not target_folder:
                continue

            source = os.path.join(base_path, filename)
            target_dir = os.path.join(base_path, target_folder)
            target_file = os.path.join(target_dir, filename)

            if not os.path.exists(source):
                errors.append(f"File not found: {filename}")
                continue

            try:
                # Create folder if needed
                os.makedirs(target_dir, exist_ok=True)
                
                # Handle dupe names
                if os.path.exists(target_file):
                    base, ext = os.path.splitext(filename)
                    timestamp = int(time.time())
                    new_name = f"{base}_{timestamp}{ext}"
                    target_file = os.path.join(target_dir, new_name)

                shutil.move(source, target_file)
                success_count += 1
            except Exception as e:
                errors.append(f"Error moving {filename}: {str(e)}")

        msg = f"Moved {success_count} files."
        if errors:
            msg += f" Errors: {'; '.join(errors[:3])}"
        
        return ToolResult(success=True, message=msg)

    def organize(self, path: str, auto_confirm: bool = False) -> ToolResult:
        """
        Orchestrates the organization. 
        """
        scan_data = self.scan_directory(path)
        if "error" in scan_data:
            return ToolResult(success=False, message=scan_data["error"])

        files = scan_data["files"]
        if not files:
            return ToolResult(success=True, message=f"No files found in {path} to organize.")

        if len(files) > 50:
            files = files[:50]
            scan_data["warning"] = "Capped at 50 files for safety."

        try:
            from brains.gemini_brain import GeminiBrain
            from brains.claude_brain import ClaudeBrain
            
            brain = None
            
            # Prefer Claude
            try:
                claude = ClaudeBrain()
                if claude.is_available():
                    brain = claude
            except Exception:
                pass
            
            # Fallback to Gemini
            if not brain:
                try:
                    gemini = GeminiBrain()
                    if gemini.is_available():
                        brain = gemini
                except Exception:
                    pass
            
            if not brain:
                return ToolResult(success=False, message="No AI brain available (Claude or Gemini) to organize files.")

            prompt = f"""
            Analyze these files and suggest a folder structure to organize them.
            Group by extension, content type, or project.
            Return ONLY a JSON array of objects: {{"filename": "string", "target_folder": "string", "reason": "string"}}
            
            Files:
            {json.dumps(files, indent=2)}
            """
            
            if isinstance(brain, ClaudeBrain):
                 # Claude's chat is async, run in event loop
                 response = asyncio.run(brain.chat([{"role": "user", "content": prompt}]))
            else:
                 response = brain.generate(prompt)
            
            cleaned = response.replace('```json', '').replace('```', '').strip()
            plan = json.loads(cleaned)
            
            if auto_confirm:
                return self.execute_move(path, plan)
            else:
                self.last_plan = plan 
                return ToolResult(success=True, message="Plan generated. Review required.", data={"path": path, "plan": plan})

        except Exception as e:
            return ToolResult(success=False, message=f"Failed to generate organization plan: {str(e)}")
