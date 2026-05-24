import json
from pathlib import Path

ADJECTIVES = ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Foxt", "Golf", "Hotel"]
NUMBERS = list(range(1, 100))


class ContributorRegistry:
    """user_id → 匿名ハンドル (#A1, #B3 ...) の変換。内部専用。公開しない。"""

    def __init__(self, path: str = "catalog/.contributors.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, str] = self._load()

    def _load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        with open(self.path) as f:
            return json.load(f)

    def _save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get_handle(self, user_id: str) -> str:
        if user_id not in self._data:
            n = len(self._data) + 1
            letter = chr(ord("A") + ((n - 1) // 9) % 26)
            number = ((n - 1) % 9) + 1
            self._data[user_id] = f"#{letter}{number}"
            self._save()
        return self._data[user_id]

    def resolve(self, handle: str) -> str | None:
        for uid, h in self._data.items():
            if h == handle:
                return uid
        return None
