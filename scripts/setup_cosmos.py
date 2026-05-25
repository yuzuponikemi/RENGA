"""Cosmos DB のデータベースと 5 コンテナを idempotent に作成する。

使い方:
  export COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
  export COSMOS_KEY=<master key>
  uv run --extra org python scripts/setup_cosmos.py

スキーマ詳細: docs/db_schema.md
"""
import os
import sys

try:
    from azure.cosmos import CosmosClient, PartitionKey, ThroughputProperties
    from azure.cosmos import exceptions as cex
except ImportError:
    sys.exit("azure-cosmos が必要です: uv sync --extra org を実行してください")


CONTAINERS = [
    {
        "id": "skills",
        "partition_key": "/category",
        "description": "公開スキル（embedding マージ済み）",
    },
    {
        "id": "contributor_mappings",
        "partition_key": "/handle",
        "description": "user_id ↔ handle 対応表（管理者 RBAC で保護）",
    },
    {
        "id": "usage_events",
        "partition_key": "/skill_id",
        "description": "スキル利用イベントの不変ログ",
        "ttl": 60 * 60 * 24 * 90,  # 90 日
    },
    {
        "id": "contributor_reports",
        "partition_key": "/handle",
        "description": "個人レポート集計キャッシュ",
    },
    {
        "id": "gift_events",
        "partition_key": "/giver_handle",
        "description": "贈与マイルストーンイベント",
        "ttl": 60 * 60 * 24 * 180,  # 180 日
    },
]


def main() -> None:
    endpoint = os.environ.get("COSMOS_ENDPOINT")
    key = os.environ.get("COSMOS_KEY")
    db_name = os.environ.get("COSMOS_DB", "skill-hub")
    throughput = int(os.environ.get("COSMOS_THROUGHPUT", "400"))

    if not endpoint or not key:
        sys.exit("COSMOS_ENDPOINT と COSMOS_KEY を環境変数にセットしてください")

    print(f"Connecting to {endpoint}")
    client = CosmosClient(endpoint, key)

    # データベース
    print(f"Creating database '{db_name}' (shared throughput {throughput} RU/s)...")
    try:
        db = client.create_database_if_not_exists(
            id=db_name,
            offer_throughput=throughput,
        )
        print(f"  ✅ database ready: {db.id}")
    except cex.CosmosHttpResponseError as e:
        sys.exit(f"  ❌ database creation failed: {e.message}")

    # コンテナ
    for spec in CONTAINERS:
        print(f"Creating container '{spec['id']}' (pk={spec['partition_key']})...")
        kwargs = {
            "id": spec["id"],
            "partition_key": PartitionKey(path=spec["partition_key"]),
        }
        if "ttl" in spec:
            kwargs["default_ttl"] = spec["ttl"]
        try:
            container = db.create_container_if_not_exists(**kwargs)
            print(f"  ✅ {container.id}: {spec['description']}")
            if "ttl" in spec:
                days = spec["ttl"] // 86400
                print(f"     TTL: {days} 日")
        except cex.CosmosHttpResponseError as e:
            print(f"  ❌ failed: {e.message}", file=sys.stderr)

    print("\n✨ セットアップ完了")
    print(f"   ダッシュボードで確認: {endpoint.rstrip('/')}/_explorer")


if __name__ == "__main__":
    main()
