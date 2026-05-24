"""既存の synthetic_logs.json 形式（JSON配列）を読むリーダー。"""
import json
from pathlib import Path
from .base import LogReader
from ..models import CopilotLog


class FolderLogReader(LogReader):
    def __init__(self, path: str):
        self.path = Path(path)

    def read(self) -> list[CopilotLog]:
        logs = []
        files = (
            [self.path] if self.path.is_file()
            else sorted(self.path.glob("*.json"))
        )
        for f in files:
            raw = json.loads(f.read_text())
            items = raw if isinstance(raw, list) else [raw]
            for item in items:
                try:
                    logs.append(CopilotLog(**item))
                except Exception:
                    pass
        return logs
