"""Claude Code の JSONL セッションログを CopilotLog に変換するリーダー。

~/.claude/projects/<project>/*.jsonl を走査し、
user→assistant のペアを抽出して CopilotLog に変換する。

フィールドのマッピング:
  prompt          = user メッセージのテキスト
  response        = assistant の text ブロック（なければ tool call のサマリー）
  accepted        = 直後の user メッセージが訂正でなければ True
  follow_up_count = 同セッション内でのフォローアップ数
  task_category   = cwd のプロジェクト名（最後のパスコンポーネント）
  user_id         = USER_ID 環境変数 > git config user.email の SHA-256 > セッションID先頭8文字
"""
import json
from pathlib import Path
from datetime import datetime
from .base import LogReader
from ._utils import resolve_user_id as _resolve_user_id, is_correction as _is_correction, is_system_message as _is_system_message
from ..models import CopilotLog


def _extract_text(content: list | str) -> str:
    if isinstance(content, str):
        return content
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            return block.get("text", "")
    return ""


def _extract_response(content: list | str) -> str:
    """text ブロックがなければ tool_use のサマリーを返す。"""
    if isinstance(content, str):
        return content
    text_parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
    if text_parts:
        return " ".join(text_parts).strip()
    tools = [b.get("name", "tool") for b in content if isinstance(b, dict) and b.get("type") == "tool_use"]
    if tools:
        return f"[Tool calls: {', '.join(tools)}]"
    return ""


def _project_name(cwd: str) -> str:
    return Path(cwd).name if cwd else "unknown"


def _follow_chain(asst_by_parent: dict[str, dict], start_uuid: str) -> dict | None:
    """thinking-only な先頭 assistant を辿り、text/tool_use を持つ末尾エントリを返す。"""
    current = asst_by_parent.get(start_uuid)
    if not current:
        return None
    seen: set[str] = set()
    while True:
        cur_uuid = current.get("uuid", "")
        if not cur_uuid or cur_uuid in seen:
            break
        seen.add(cur_uuid)
        nxt = asst_by_parent.get(cur_uuid)
        if nxt is None:
            break
        current = nxt
    return current


class ClaudeCodeLogReader(LogReader):
    """
    Parameters
    ----------
    projects_dir : str | list[str]
        ~/.claude/projects/ のようなディレクトリ。複数指定可（リストまたはコロン区切り文字列）。
        例: "~/.claude/projects:~/pc2-logs/projects"
    project_filter : str | None
        特定プロジェクト名だけに絞る場合に指定。
    min_response_len : int
        テキストレスポンスが短すぎる場合に除外（tool call レスポンスは対象外）。
    """

    def __init__(
        self,
        projects_dir: str | list[str] = "~/.claude/projects",
        project_filter: str | None = None,
        min_response_len: int = 50,
    ):
        if isinstance(projects_dir, str):
            # コロン区切りで複数ディレクトリを指定できる
            self.projects_dirs = [Path(p).expanduser() for p in projects_dir.split(":")]
        else:
            self.projects_dirs = [Path(p).expanduser() for p in projects_dir]
        self.project_filter = project_filter
        self.min_response_len = min_response_len

    def read(self) -> list[CopilotLog]:
        logs: list[CopilotLog] = []
        for projects_dir in self.projects_dirs:
            if not projects_dir.exists():
                continue
            for jsonl_path in sorted(projects_dir.rglob("*.jsonl")):
                if self.project_filter and self.project_filter not in str(jsonl_path):
                    continue
                logs.extend(self._parse_session(jsonl_path))
        return logs

    def _parse_session(self, path: Path) -> list[CopilotLog]:
        try:
            lines = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        except Exception:
            return []

        user_entries = [l for l in lines if l.get("type") == "user" and "uuid" in l]
        asst_entries = [l for l in lines if l.get("type") == "assistant" and "uuid" in l]

        # parentUuid でペアリング（assistant チェーンも辿れるよう全 assistant を登録）
        asst_by_parent: dict[str, dict] = {}
        for a in asst_entries:
            pid = a.get("parentUuid")
            if pid:
                asst_by_parent[pid] = a

        results: list[CopilotLog] = []
        for i, user in enumerate(user_entries):
            uuid = user["uuid"]
            # extended thinking 時の thinking-only 先頭エントリを辿る
            asst = _follow_chain(asst_by_parent, uuid)
            if not asst:
                continue

            prompt = _extract_text(user.get("message", {}).get("content", ""))
            asst_content = asst.get("message", {}).get("content", [])
            response = _extract_response(asst_content)

            if not prompt or _is_system_message(prompt):
                continue
            # tool call レスポンスは長さ不問で受け入れ；テキストのみ最低文字数を適用
            if not response.startswith("[Tool calls:") and len(response) < self.min_response_len:
                continue

            # accepted: 次の user メッセージが訂正でなければ True
            next_user = user_entries[i + 1] if i + 1 < len(user_entries) else None
            if next_user is None:
                accepted = True
                follow_up = 0
            else:
                next_text = _extract_text(next_user.get("message", {}).get("content", ""))
                accepted = not _is_correction(next_text)
                follow_up = 0 if accepted else 1

            cwd = user.get("cwd", "")
            session_id = user.get("sessionId", path.stem)

            results.append(CopilotLog(
                user_id=_resolve_user_id(session_id),
                timestamp=user.get("timestamp", datetime.utcnow().isoformat()),
                prompt=prompt,
                response=response,
                accepted=accepted,
                follow_up_count=follow_up,
                task_category=_project_name(cwd),
            ))

        return results
