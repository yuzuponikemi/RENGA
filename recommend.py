import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from src.skill_hub.agents.recommender import RecommenderAgent
from src.skill_hub.catalog import SkillCatalog

load_dotenv()


def build_client() -> tuple[OpenAI, str]:
    endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
    api_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
    deployment = os.environ.get("AZURE_FOUNDRY_DEPLOYMENT", "DeepSeek-V4-Flash")
    if not endpoint or not api_key:
        print("Error: .env not configured", file=sys.stderr)
        sys.exit(1)
    return OpenAI(base_url=endpoint, api_key=api_key), deployment


def main() -> None:
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not query:
        query = input("何を手伝ってほしいですか？ > ")

    client, deployment = build_client()
    catalog = SkillCatalog()
    agent = RecommenderAgent(client=client, model=deployment, catalog=catalog)

    print(f"\n🔍 「{query}」に関連するスキルを検索中...\n")
    results = agent.recommend(query)

    if not results:
        print("該当するスキルが見つかりませんでした。")
        return

    for i, r in enumerate(results, 1):
        print(f"{'─'*50}")
        print(f"#{i} {r['name']}")
        print(f"理由: {r['reason']}")
        print(f"\n使用例:\n{r['adapted_prompt']}")
    print(f"{'─'*50}")


if __name__ == "__main__":
    main()
