"""Log runs in JSONL format. Um die Aufrufe der Agenten zu protokollieren."""

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

class RunLog:
    def __init__(self, root: Path):
            self.run_id = uuid4().hex   # eine ID pro Lauf, steht in jeder Zeile
            self.model = None           # wird gesetzt, sobald die Config geladen ist
            folder = root / "logs"
            folder.mkdir(exist_ok=True)  # Ordner anlegen, falls er fehlt
            self.path = folder / f"{self.run_id}.jsonl"  # eine eigene Datei pro Lauf


    def write(self, event, *, ok=True, tool=None, args=None, duration_ms=0):
        record = {
                "ts": datetime.now(timezone.utc).isoformat(),  # ISO 8601
                "run_id": self.run_id,
                "event": event,
                "tool": tool,
                "args": args,
                "ok": ok,
                "model": self.model,
                "duration_ms": duration_ms,
            }
        with self.path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")