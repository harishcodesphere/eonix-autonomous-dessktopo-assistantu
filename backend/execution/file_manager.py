import os
import shutil
import pathlib
from typing import List, Dict
from loguru import logger

class FileManager:
    @staticmethod
    def list_files(directory: str) -> List[Dict]:
        try:
            path = pathlib.Path(directory)
            if not path.exists():
                return []
            
            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": item.stat().st_mtime
                })
            return items
        except Exception as e:
            logger.error(f"File manager error: {e}")
            return []

    @staticmethod
    def create_directory(directory: str) -> bool:
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_item(path: str) -> bool:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True
        except Exception:
            return False
