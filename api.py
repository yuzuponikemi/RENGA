import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from openai import OpenAI
from pydantic import BaseModel

from src.skill_hub.agents.recommender import RecommenderAgent
from src.skill_hub.agents.search import EmbeddingSearchIndex
from src.skill_hub.mcpify import export_yamls
from src.skill_hub.models import SkillStatus
from src.skill_hub.storage import make_catalog

load_dotenv()

catalog = make_catalog()
_client: OpenAI | None = None
_deployment: str = ""
_search_index: EmbeddingSearchIndex = EmbeddingSearchIndex()


def get_client() -> tuple[OpenAI, str]:
    global _client, _deployment
    if _client is None:
        endpoint = os.environ["AZURE_FOUNDRY_ENDPOINT"]
        api_key = os.environ["AZURE_FOUNDRY_API_KEY"]
        _deployment = os.environ.get("AZURE_FOUNDRY_DEPLOYMENT", "DeepSeek-V4-Flash")
        _client = OpenAI(base_url=endpoint, api_key=api_key)
    return _client, _deployment


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Build search index once on startup so the first /recommend isn't slow
    public_skills = catalog.get_public()
    if public_skills:
        _search_index.build(public_skills)
        print(f"[startup] Search index built: {len(public_skills)} public skills")
    yield


app = FastAPI(
    title="Skill Hub Agent API",
    description="社内AIスキル循環エージェント — Copilot Studio 連携エンドポイント",
    version="0.1.0",
    lifespan=lifespan,
)


# ── Request / Response schemas ──────────────────────────────────────────────

class RecommendRequest(BaseModel):
    query: str
    user_id: str = "anonymous"

class RecommendResult(BaseModel):
    skill_id: str
    name: str
    reason: str
    adapted_prompt: str

class UseSkillRequest(BaseModel):
    skill_id: str
    user_id: str = "anonymous"


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.post("/recommend", response_model=list[RecommendResult])
def recommend(req: RecommendRequest):
    """ユーザーの質問に合ったスキルを推薦する（Copilot Studio から呼ぶメインエンドポイント）"""
    try:
        client, deployment = get_client()
        agent = RecommenderAgent(client=client, model=deployment, catalog=catalog,
                                 index=_search_index)
        results = agent.recommend(req.query)
        if not results:
            return []
        for r in results:
            catalog.increment_usage(r["skill_id"])
        return [RecommendResult(**r) for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/skills")
def list_skills():
    """公開スキル一覧を返す"""
    return [
        {
            "skill_id": s.skill_id,
            "name": s.name,
            "description": s.description,
            "category": s.category,
            "template_prompt": s.template_prompt,
            "variables": s.variables,
            "usage_count": s.usage_count,
            "source_count": s.source_count,
        }
        for s in catalog.get_public()
    ]


@app.get("/stats")
def stats():
    """カタログ統計"""
    return catalog.stats()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """匿名コントリビューションダッシュボード"""
    skills = catalog.get_public()
    stats = catalog.stats()

    rows = ""
    for s in sorted(skills, key=lambda x: x.usage_count, reverse=True):
        handles = ", ".join(s.contributor_handles) if s.contributor_handles else "—"
        rows += f"""
        <tr>
          <td>{s.name}</td>
          <td><span class="badge">{s.category}</span></td>
          <td class="num">{s.usage_count}</td>
          <td class="num">{s.source_count}</td>
          <td class="handles">{handles}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Skill Hub — 匿名コントリビューションダッシュボード</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 2rem; }}
    h1 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; color: #f8fafc; }}
    .subtitle {{ color: #94a3b8; font-size: 0.875rem; margin-bottom: 2rem; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }}
    .stat-card {{ background: #1e2130; border: 1px solid #2d3748; border-radius: 12px;
                  padding: 1.25rem; text-align: center; }}
    .stat-card .num {{ font-size: 2rem; font-weight: 700; color: #7c3aed; }}
    .stat-card .label {{ font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem; }}
    table {{ width: 100%; border-collapse: collapse; background: #1e2130;
             border: 1px solid #2d3748; border-radius: 12px; overflow: hidden; }}
    th {{ background: #2d3748; color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;
          letter-spacing: 0.05em; padding: 0.75rem 1rem; text-align: left; }}
    td {{ padding: 0.875rem 1rem; border-top: 1px solid #2d3748; font-size: 0.875rem; }}
    tr:hover td {{ background: #252d3d; }}
    .badge {{ background: #312e81; color: #a5b4fc; padding: 0.2rem 0.6rem;
              border-radius: 999px; font-size: 0.75rem; }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .handles {{ color: #7c3aed; font-family: monospace; font-size: 0.8rem; }}
    .footer {{ margin-top: 1.5rem; font-size: 0.75rem; color: #4a5568; text-align: center; }}
  </style>
</head>
<body>
  <h1>🔮 Skill Hub</h1>
  <p class="subtitle">個人の善意を、AIが代わりに可視化する。貢献者は匿名のまま記録されます。</p>

  <div class="stats-grid">
    <div class="stat-card"><div class="num">{stats['total']}</div><div class="label">総スキル数</div></div>
    <div class="stat-card"><div class="num">{stats['public']}</div><div class="label">公開中</div></div>
    <div class="stat-card"><div class="num">{stats['pending']}</div><div class="label">審査中</div></div>
    <div class="stat-card"><div class="num">{stats['total_usage']}</div><div class="label">総利用回数</div></div>
  </div>

  <table>
    <thead>
      <tr>
        <th>スキル名</th>
        <th>カテゴリ</th>
        <th style="text-align:right">利用回数</th>
        <th style="text-align:right">ソース数</th>
        <th>匿名コントリビューター</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>

  <p class="footer">コントリビューターは本人と管理者にのみ識別可能です。</p>
</body>
</html>"""


@app.post("/mcpify")
def mcpify():
    """公開スキルを Copilot Studio トピック YAML に変換して保存する"""
    skills = catalog.get_public()
    if not skills:
        raise HTTPException(status_code=404, detail="No public skills in catalog")
    _search_index.build(skills)
    paths = export_yamls(skills)
    return {"generated": [str(p) for p in paths]}


@app.post("/index/rebuild")
def rebuild_index():
    """検索インデックスを再構築する（カタログ更新後に呼ぶ）"""
    skills = catalog.get_public()
    _search_index.build(skills)
    return {"indexed": len(skills)}


@app.get("/contributor/{handle}/report")
def contributor_report(handle: str):
    """匿名コントリビューターの貢献レポート。

    自分のハンドル（本人のみ知る `#A1` など）で呼ぶと、
    貢献したスキル数・累積利用回数・トップスキルを返す。
    """
    skills = catalog.load_all()
    contributed = [s for s in skills if handle in s.contributor_handles]
    if not contributed:
        return {"handle": handle, "found": False}
    public_count = sum(1 for s in contributed if s.status == SkillStatus.PUBLIC)
    return {
        "handle": handle,
        "found": True,
        "contributed_skills": len(contributed),
        "public_skills": public_count,
        "total_usage": sum(s.usage_count for s in contributed),
        "top_skills": [
            {
                "skill_id": s.skill_id,
                "name": s.name,
                "category": s.category,
                "usage_count": s.usage_count,
                "status": s.status.value,
            }
            for s in sorted(contributed, key=lambda x: -x.usage_count)[:5]
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
