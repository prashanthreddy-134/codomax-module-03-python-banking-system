import json
from pathlib import Path
class JSONStorage:
    """Small JSON persistence adapter for the educational application."""
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    def load(self):
        if not self.file_path.exists():
            return {"accounts": [], "next_account_number": 1001}
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Bank data file is not valid JSON: {exc}") from exc
        if not isinstance(data, dict) or "accounts" not in data:
            raise RuntimeError("Bank data file has an invalid structure.")
        return data
    def save(self, data):
        temporary = self.file_path.with_suffix(self.file_path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        temporary.replace(self.file_path)
