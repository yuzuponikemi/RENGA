"""Azure Function v2: GitHub の個人 skills.json を Cosmos DB に集約する。

トリガー:
  - Timer: 1時間ごとに自動 aggregate
  - HTTP:  POST /api/aggregate で手動実行（デモ・E2E 用）

実装ロジックは core.py に分離してある（E2E テストから直接 import する用途）。
"""
import json
import logging

import azure.functions as func

from core import _aggregate

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.timer_trigger(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def aggregate_timer(timer: func.TimerRequest) -> None:
    """毎時 0分 に集約を実行。"""
    result = _aggregate()
    logging.info(f"[timer] aggregate result: {result}")


@app.route(route="aggregate", methods=["POST"])
def aggregate_http(req: func.HttpRequest) -> func.HttpResponse:
    """手動トリガー: POST /api/aggregate"""
    result = _aggregate()
    return func.HttpResponse(json.dumps(result), mimetype="application/json")


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "alive", "function": "skill-hub-aggregator"}),
        mimetype="application/json",
    )
