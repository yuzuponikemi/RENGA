"""Azure Functions v2 エントリーポイント。
FastAPI アプリを ASGI 経由でラップする。
"""
import azure.functions as func
from api import app

func_app = func.AsgiFunctionApp(app=app, http_auth_level=func.AuthLevel.ANONYMOUS)
