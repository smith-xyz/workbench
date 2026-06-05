import json
import time
from pathlib import Path


class HealthWriter:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write_ok(self) -> None:
        self._write({"status": "ok", "timestamp": time.time()})

    def write_error(self, msg: str) -> None:
        self._write({"status": "error", "error": msg, "timestamp": time.time()})

    def _write(self, data: dict) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.rename(self.path)
