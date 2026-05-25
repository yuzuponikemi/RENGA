"""VSCode の GitHub Copilot Chat ログを CopilotLog に変換するリーダー。

ストレージレイアウト:
  <workspaceStorage>/<workspace_hash>/
    chatSessions/<session_uuid>.json
    workspace.json    ← ワークスペースのフォルダパス情報

デフォルトパス (OS 別):
  macOS   ~/Library/Application Support/Code/User/workspaceStorage
  Linux   ~/.config/Code/User/workspaceStorage
  Windows %APPDATA%/Code/User/workspaceStorage

フィールドのマッピング:
  prompt          = requests[i].message.text
  response        = requests[i].response の markdown 部分（なければ tool 呼び出しのサマリー）
  accepted        = not isCanceled かつ 直後のリクエストが訂正系でない
  follow_up_count = accepted=False のとき 1
  task_category   = ワークスペースのフォルダ名（取得できなければ hash 先頭8桁）
  user_id         = USER_ID env > git email hash > sessionId 先頭8桁
"""
import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from .base import LogReader
from ._utils import resolve_user_id, is_correction, is_system_message
from ..models import CopilotLog

_MIN_RESPONSE_LEN = 50


def _default_workspace_storage() -> str:
    if sys.platform == "darwin":
        return "~/Library/Application Support/Code/User/workspaceStorage"
    if sys.platform == "win32":
        return os.path.expandvars(r"%APPDATA%\Code\User\workspaceStorage")
    return "~/.config/Code/User/workspaceStorage"


class VSCodeCopilotChatLogReader(LogReader):
    """
    Parameters
    ----------
    workspace_storage_dir : str | list[str] | None
        VSCode の workspaceStorage ディレクトリ。コロン区切りで複数指定可。
        None なら OS 既定パスを使用。
    workspace_filter : str | None
        ワークスペース名にこの文字列が含まれるものだけ対象。
    include_canceled : bool
        True なら isCanceled なリクエストも accepted=False で残す（既定 False）。
    """

    def __init__(
        self,
        workspace_storage_dir: str | list[str] | None = None,
        workspace_filter: str | None = None,
        include_canceled: bool = False,
        min_response_len: int = _MIN_RESPONSE_LEN,
    ):
        if workspace_storage_dir is None:
            workspace_storage_dir = _default_workspace_storage()
        if isinstance(workspace_storage_dir, str):
            self.dirs = [Path(p).expanduser() for p in workspace_storage_dir.split(":")]
        else:
            self.dirs = [Path(p).expanduser() for p in workspace_storage_dir]
        self.workspace_filter = workspace_filter
        self.include_canceled = include_canceled
        self.min_response_len = min_response_len

    def read(self) -> list[CopilotLog]:
        logs: list[CopilotLog] = []
        for storage_dir in self.dirs:
            if not storage_dir.exists():
                continue
            for ws_dir in sorted(storage_dir.iterdir()):
                if not ws_dir.is_dir():
                    continue
                sessions_dir = ws_dir / "chatSessions"
                if not sessions_dir.exists() or not sessions_dir.is_dir():
                    continue
                ws_name = self._workspace_name(ws_dir)
                if self.workspace_filter and self.workspace_filter not in ws_name:
                    continue
                for session_file in sorted(sessions_dir.glob("*.json")):
                    logs.extend(self._parse_session(session_file, ws_name))
        return logs

    # ── helpers ────────────────────────────────────────────────────

    @staticmethod
    def _workspace_name(ws_dir: Path) -> str:
        ws_json = ws_dir / "workspace.json"
        if ws_json.exists():
            try:
                data = json.loads(ws_json.read_text(encoding="utf-8"))
                folder = data.get("folder") or data.get("configuration") or ""
                if folder:
                    parsed = urlparse(folder)
                    path = unquote(parsed.path or folder.replace("file://", ""))
                    name = Path(path).name
                    if name:
                        return name
            except Exception:
                pass
        return ws_dir.name[:8]

    @staticmethod
    def _extract_response(response_items) -> str:
        """response 配列から表示テキストを抽出。markdown が無ければ tool 呼び出しサマリー。"""
        if isinstance(response_items, str):
            return response_items
        if not isinstance(response_items, list):
            return ""

        text_parts: list[str] = []
        tool_ids: list[str] = []
        for item in response_items:
            if not isinstance(item, dict):
                continue
            kind = item.get("kind", "") or ""
            # markdownContent / markdownVulnerability / textEdit など text を含むもの
            value = item.get("value")
            text = item.get("text")
            if isinstance(value, dict):
                v = value.get("value") or value.get("text")
                if v:
                    text_parts.append(str(v))
            elif isinstance(value, str) and value:
                text_parts.append(value)
            elif isinstance(text, str) and text:
                text_parts.append(text)
            elif "toolInvocation" in kind or item.get("toolCallId") or item.get("toolId"):
                tool_ids.append(str(item.get("toolId") or item.get("toolCallId") or "tool"))
        if text_parts:
            return " ".join(text_parts).strip()
        if tool_ids:
            uniq = sorted(set(tool_ids))
            return f"[Tool calls: {', '.join(uniq)}]"
        return ""

    @staticmethod
    def _timestamp(session_data: dict) -> str:
        ts = session_data.get("creationDate") or session_data.get("lastMessageDate")
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).isoformat()
        if isinstance(ts, str) and ts:
            return ts
        return datetime.now(timezone.utc).isoformat()

    def _parse_session(self, path: Path, ws_name: str) -> list[CopilotLog]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []
        requests = data.get("requests") or []
        if not isinstance(requests, list):
            return []
        session_id = data.get("sessionId", path.stem)
        timestamp = self._timestamp(data)
        user_id = resolve_user_id(session_id)

        results: list[CopilotLog] = []
        for i, req in enumerate(requests):
            if not isinstance(req, dict):
                continue
            msg = req.get("message")
            if isinstance(msg, dict):
                prompt = msg.get("text", "") or ""
            elif isinstance(msg, str):
                prompt = msg
            else:
                prompt = ""
            prompt = prompt.strip()
            if not prompt or is_system_message(prompt):
                continue

            response = self._extract_response(req.get("response", []))
            if not response.startswith("[Tool calls:") and len(response) < self.min_response_len:
                continue

            canceled = bool(req.get("isCanceled"))
            if canceled and not self.include_canceled:
                continue

            next_text = ""
            if i + 1 < len(requests):
                nxt = requests[i + 1]
                if isinstance(nxt, dict):
                    nxt_msg = nxt.get("message")
                    if isinstance(nxt_msg, dict):
                        next_text = nxt_msg.get("text", "") or ""
                    elif isinstance(nxt_msg, str):
                        next_text = nxt_msg
            accepted = (not canceled) and not is_correction(next_text)
            follow_up = 0 if accepted else 1

            results.append(CopilotLog(
                user_id=user_id,
                timestamp=timestamp,
                prompt=prompt,
                response=response,
                accepted=accepted,
                follow_up_count=follow_up,
                task_category=ws_name,
            ))
        return results
