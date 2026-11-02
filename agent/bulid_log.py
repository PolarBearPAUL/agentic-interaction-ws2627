"""One JSONL file per run. Exact payload fields still need the Moodle specification."""

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class RunLog:
    def __init__(self, root: Path):
        self.run_id = uuid4().hex
        self.model = None
        folder = root / "logs"
        folder.mkdir(exist_ok=True)
        self.path = folder / f"{self.run_id}.jsonl"
        self.path.touch(exist_ok=False)

    def write(self, event, *, ok=True, duration_ms=0, tool=None, args=None):
        # Payload names (task/result/answer/message) are provisional until Moodle is checked.
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
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
