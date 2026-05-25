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
            "triggers": s.triggers,
            "contributor_handles": s.contributor_handles,
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
    """匿名コントリビューションダッシュボード（Copilot ライク検索UI）"""
    s = catalog.stats()
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Skill Hub</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0f1117; --surface: #1a1d2e; --border: #2a2d3e; --accent: #7c3aed;
      --accent2: #a78bfa; --text: #e2e8f0; --muted: #94a3b8; --code-bg: #12141f;
    }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg); color: var(--text); min-height: 100vh; }}
    header {{ padding: 1.5rem 2rem 0; max-width: 1100px; margin: 0 auto; }}
    .brand {{ display: flex; align-items: baseline; gap: 0.6rem; margin-bottom: 0.25rem; }}
    .brand h1 {{ font-size: 1.4rem; font-weight: 700; color: #f8fafc; }}
    .brand span {{ font-size: 0.8rem; color: var(--muted); }}
    .stats-row {{ display: flex; gap: 1.5rem; margin: 0.75rem 0 1.5rem; flex-wrap: wrap; }}
    .stat {{ font-size: 0.8rem; color: var(--muted); }}
    .stat b {{ color: var(--accent2); font-size: 1rem; }}

    /* Search */
    .search-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem 1.5rem; }}
    .search-box {{ position: relative; }}
    .search-box input {{
      width: 100%; padding: 0.875rem 3rem 0.875rem 1.25rem;
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      color: var(--text); font-size: 1rem; outline: none; transition: border-color 0.15s;
    }}
    .search-box input:focus {{ border-color: var(--accent); }}
    .search-box input::placeholder {{ color: var(--muted); }}
    .search-box .clear {{ position: absolute; right: 1rem; top: 50%; transform: translateY(-50%);
                          background: none; border: none; color: var(--muted); font-size: 1.1rem;
                          cursor: pointer; display: none; padding: 0; line-height: 1; }}
    .filter-row {{ display: flex; gap: 0.5rem; margin-top: 0.75rem; flex-wrap: wrap; }}
    .cat-chip {{
      padding: 0.3rem 0.75rem; border-radius: 999px; border: 1px solid var(--border);
      background: none; color: var(--muted); font-size: 0.78rem; cursor: pointer;
      transition: all 0.12s;
    }}
    .cat-chip:hover {{ border-color: var(--accent2); color: var(--accent2); }}
    .cat-chip.active {{ background: #312e81; border-color: var(--accent); color: var(--accent2); }}

    /* Results */
    #result-info {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem 0.75rem;
                    font-size: 0.8rem; color: var(--muted); }}
    #cards {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem 3rem;
              display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
              gap: 1rem; }}

    /* Skill card */
    .card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
      padding: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;
      transition: border-color 0.15s;
    }}
    .card:hover {{ border-color: #4a3f7a; }}
    .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; }}
    .card-name {{ font-weight: 600; font-size: 0.95rem; color: #f1f5f9; line-height: 1.3; }}
    .cat-badge {{ background: #1e1b4b; color: var(--accent2); padding: 0.15rem 0.55rem;
                  border-radius: 999px; font-size: 0.7rem; white-space: nowrap; flex-shrink: 0; }}
    .card-desc {{ font-size: 0.82rem; color: var(--muted); line-height: 1.5; }}

    /* Template prompt block */
    .prompt-block {{ background: var(--code-bg); border: 1px solid var(--border);
                     border-radius: 8px; padding: 0.75rem; position: relative; }}
    .prompt-label {{ font-size: 0.68rem; color: var(--muted); text-transform: uppercase;
                     letter-spacing: 0.06em; margin-bottom: 0.4rem; }}
    .prompt-text {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 0.78rem;
                    color: #c4b5fd; line-height: 1.6; white-space: pre-wrap;
                    word-break: break-all; max-height: 5.5rem; overflow: hidden;
                    position: relative; }}
    .prompt-text.expanded {{ max-height: none; }}
    .copy-btn {{
      position: absolute; top: 0.5rem; right: 0.5rem;
      background: #2d2b52; border: 1px solid var(--border); border-radius: 6px;
      color: var(--accent2); font-size: 0.7rem; padding: 0.2rem 0.5rem; cursor: pointer;
      transition: background 0.12s;
    }}
    .copy-btn:hover {{ background: #3d3a70; }}
    .copy-btn.copied {{ color: #34d399; border-color: #34d399; }}

    /* Variables */
    .vars {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
    .var-tag {{ background: #1e293b; color: #7dd3fc; border: 1px solid #1e4068;
                border-radius: 6px; font-size: 0.7rem; padding: 0.15rem 0.45rem;
                font-family: monospace; }}

    /* Triggers */
    .triggers {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
    .trigger-tag {{ background: #0f2921; color: #6ee7b7; border: 1px solid #134e3a;
                    border-radius: 6px; font-size: 0.7rem; padding: 0.15rem 0.45rem; }}
    .section-label {{ font-size: 0.68rem; color: var(--muted); text-transform: uppercase;
                      letter-spacing: 0.06em; margin-bottom: 0.3rem; }}

    /* Meta row */
    .card-meta {{ display: flex; gap: 1rem; font-size: 0.72rem; color: var(--muted);
                  padding-top: 0.5rem; border-top: 1px solid var(--border); }}
    .card-meta span {{ display: flex; align-items: center; gap: 0.25rem; }}

    /* Empty state */
    #empty {{ max-width: 1100px; margin: 3rem auto; text-align: center; color: var(--muted);
              padding: 0 2rem; display: none; }}
    #empty .icon {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}

    footer {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem 2rem;
              font-size: 0.72rem; color: #4a5568; }}
  </style>
</head>
<body>

<header>
  <div class="brand">
    <h1>🔮 Skill Hub</h1>
    <span>匿名スキル循環カタログ</span>
  </div>
  <div class="stats-row">
    <div class="stat"><b>{s['public']}</b> 公開スキル</div>
    <div class="stat"><b>{s['pending']}</b> 審査中</div>
    <div class="stat"><b>{s['total_usage']}</b> 総利用回数</div>
  </div>
</header>

<div class="search-wrap">
  <div class="search-box">
    <input id="q" type="text" placeholder="何をしたいですか？　例: コードを解析してドキュメント化したい" autocomplete="off" />
    <button class="clear" id="clear-btn" title="クリア">✕</button>
  </div>
  <div class="filter-row" id="cat-filters"></div>
</div>

<div id="result-info"></div>
<div id="cards"></div>
<div id="empty"><div class="icon">🔍</div><div>「<span id="empty-q"></span>」に一致するスキルが見つかりませんでした</div></div>

<footer>コントリビューターは本人と管理者にのみ識別可能です。</footer>

<script>
let ALL = [];
let activeCat = null;

async function load() {{
  const res = await fetch('/skills');
  ALL = await res.json();
  buildCatFilters();
  render('');
}}

function buildCatFilters() {{
  const counts = {{}};
  ALL.forEach(s => counts[s.category] = (counts[s.category] || 0) + 1);
  const cats = Object.entries(counts).sort((a,b) => b[1]-a[1]);
  const row = document.getElementById('cat-filters');
  row.innerHTML = '';
  cats.forEach(([cat, n]) => {{
    const btn = document.createElement('button');
    btn.className = 'cat-chip';
    btn.textContent = cat + ' ' + n;
    btn.dataset.cat = cat;
    btn.onclick = () => toggleCat(cat);
    row.appendChild(btn);
  }});
}}

function toggleCat(cat) {{
  activeCat = activeCat === cat ? null : cat;
  document.querySelectorAll('.cat-chip').forEach(b => {{
    b.classList.toggle('active', b.dataset.cat === activeCat);
  }});
  render(document.getElementById('q').value);
}}

function score(s, q) {{
  if (!q) return 1;
  const haystack = [s.name, s.description || '', s.category,
    (s.template_prompt || ''), ...(s.variables || [])].join(' ').toLowerCase();
  const words = q.toLowerCase().split(/\s+/).filter(Boolean);
  return words.every(w => haystack.includes(w)) ? 1 : 0;
}}

function render(q) {{
  let items = ALL.filter(s => score(s, q) && (!activeCat || s.category === activeCat));
  const info = document.getElementById('result-info');
  const empty = document.getElementById('empty');
  const cards = document.getElementById('cards');

  if (items.length === 0) {{
    cards.innerHTML = '';
    empty.style.display = 'block';
    document.getElementById('empty-q').textContent = q || activeCat || '';
    info.textContent = '';
    return;
  }}
  empty.style.display = 'none';
  info.textContent = items.length + ' 件';
  cards.innerHTML = items.map(s => cardHTML(s)).join('');
}}

function esc(str) {{
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function cardHTML(s) {{
  const vars = (s.variables || []).map(v => `<span class="var-tag">&#123;&#123;${{esc(v)}}&#125;&#125;</span>`).join('');
  // derive triggers from template prompt keywords (use usage_count proxy)
  const handles = s.contributor_handles && s.contributor_handles.length
    ? s.contributor_handles.map(h => `<span style="color:#a78bfa;font-family:monospace;font-size:0.75rem">${{esc(h)}}</span>`).join(' ')
    : '<span style="color:#4a5568">—</span>';
  const prompt = esc(s.template_prompt || '');
  const sid = 'p-' + s.skill_id.replace(/-/g,'');
  return `
<div class="card">
  <div class="card-head">
    <div class="card-name">${{esc(s.name)}}</div>
    <span class="cat-badge">${{esc(s.category)}}</span>
  </div>
  ${{s.description ? `<div class="card-desc">${{esc(s.description)}}</div>` : ''}}
  <div class="prompt-block">
    <div class="prompt-label">テンプレートプロンプト</div>
    <div class="prompt-text" id="${{sid}}">${{prompt}}</div>
    <button class="copy-btn" onclick="copyPrompt('${{s.skill_id}}', this)">📋 コピー</button>
  </div>
  ${{vars ? `<div><div class="section-label">変数</div><div class="vars">${{vars}}</div></div>` : ''}}
  <div class="card-meta">
    <span>🔥 ${{s.usage_count}} 回利用</span>
    <span>📄 ${{s.source_count}} ソース</span>
    <span>👤 ${{handles}}</span>
  </div>
</div>`;
}}

// Raw prompt store for copy
const prompts = {{}};
async function getPrompts() {{
  if (Object.keys(prompts).length) return;
  ALL.forEach(s => prompts[s.skill_id] = s.template_prompt || '');
}}

async function copyPrompt(id, btn) {{
  await getPrompts();
  await navigator.clipboard.writeText(prompts[id] || '');
  btn.textContent = '✅ コピー済';
  btn.classList.add('copied');
  setTimeout(() => {{ btn.textContent = '📋 コピー'; btn.classList.remove('copied'); }}, 2000);
}}

const input = document.getElementById('q');
const clearBtn = document.getElementById('clear-btn');
input.addEventListener('input', () => {{
  clearBtn.style.display = input.value ? 'block' : 'none';
  render(input.value);
}});
clearBtn.addEventListener('click', () => {{
  input.value = ''; clearBtn.style.display = 'none'; input.focus(); render('');
}});

load();
</script>
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
