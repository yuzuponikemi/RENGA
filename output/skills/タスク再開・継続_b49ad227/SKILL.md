---
name: タスク再開・継続
skill_id: b49ad227-aa96-4652-ba0b-8428ba0d6a8e
version: 1.0.0
category: タスク再開・継続
status: public
source_count: 6
unique_user_count: 5
variables:
- タスク名
- コンテキスト情報
- 具体的な指示
- 実行手順やコマンド
triggers:
- 前回の続きをやって
- 中断したタスクを再開して
- 途中までやった作業を続けて
- 前回やっていた〜を再開
- 続きからお願い
---

# タスク再開・継続

**説明**: 中断した作業を再開・継続するためのスキル
**ステータス**: ✅ 公開中 | **ソース数**: 6 件 | **ユニークユーザー**: 5 人 | **カテゴリ**: タスク再開・継続

---

## テンプレートプロンプト

```
前回やっていた{タスク名}を再開してほしい

{コンテキスト情報}

{具体的な指示}

{実行手順やコマンド}
```

## 変数一覧

- `{{タスク名}}`: 再開したい作業の名前（例: 動画の強制アライメント実行）
- `{{コンテキスト情報}}`: 前回の進捗状況や既に完了したステップ（例: ☒ モジュールAの読み込み完了 ... ☐ 処理Bの実行）
- `{{具体的な指示}}`: 今回実行してほしい具体的な内容（例: 提供された歌詞を使って分析してほしい）
- `{{実行手順やコマンド}}`: 実行すべきコマンドや手順（例: python main.py process "{URL}" --lyrics-file lyrics.txt）

## 活用シーン

- 中断したデータ分析パイプラインの再実行
- 前回途中だったコードレビューの続き
- 途中まで書いたドキュメントの完成

## トリガーフレーズ

- `前回の続きをやって`
- `中断したタスクを再開して`
- `途中までやった作業を続けて`
- `前回やっていた〜を再開`
- `続きからお願い`

---

## 具体インスタンス

### インスタンス 1: 強制アライメント再開

> 元プロンプト: *前回やっていた　Run forced alignment on the Youtube Videoタスクを再開してほしい ✶ Running forced alignment… (esc to interrupt · 6m 59s · th*

**変数の値**
  - `タスク名`: 動画の強制アライメント実行
  - `コンテキスト情報`: ✶ Running forced alignment… (esc to interrupt · 6m 59s · thinking)
  ⎿  ☒ Read aligner.py to understand forced alignment implementation
     ☒ Read lyrics_fetcher.py for API lyrics fetching
     ☒ Update README.md with forced alignment documentation
     ☐ Run forced alignment on the YouTube video
  - `具体的な指示`: 今回の曲の歌詞を使って、force alignmentの手法で分析してほしい。まずREADMEを詳細にアップデートしてから、実際に実行してほしい
  - `実行手順やコマンド`: python main.py process "{URL}" --lyrics-file lyrics.txt --stages download --stages align
python main.py process "{URL}" --artist "{アーティスト名}" --song-title "{曲名}" --stages download --stages align

**実際のプロンプト**
```
前回やっていた{タスク名}を再開してほしい

今回の曲の歌詞は、[Verse 1]
Man, needs a birthright land
Always have a plan
Knowing where he stands
While I live another day
To find a voice of my own
Find another stone

[Refrain]
My heart (Flesh, blood and bones) beats with what I see
My soul (Come back to thee) holds the self I'll know

[Verse 2]
Gone, calm in changing paths
Don't go out enough
To know the midmost crowd
In life never satisfied
There's nothing I could find
To give me peace inside

[Refrain]
Come back to thee whole
Come back to thee whole
All I've come to know

ということでわかっています　これを使って、# Use forced alignment with lyrics file (maximum accuracy)
python main.py process "{URL}" --lyrics-file lyrics.txt --stages download --stages align

# Use artist and song name for API search
python main.py process "{URL}" --artist "{アーティスト名}" --song-title "{曲名}" --stages download --stages align
の手法で分析してほしいです　
今回このforce alignmentをできるようにしたので、まずREADMEを詳細にアップデートしてから、実際にやってみて
```

---

### インスタンス 2: 書籍構造調査再開

> 元プロンプト: *Explore the file {ファイルパス} thoroughly to understand its structure.  I need: 1. ALL top-level headings (# ...) with their *

**変数の値**
  - `タスク名`: 書籍構造調査
  - `コンテキスト情報`: 前回の進捗なし、新規調査
  - `具体的な指示`: ファイル {ファイルパス} の構造を徹底的に調査し、見出し・パート区切り・文字数・内容をマッピングしてほしい
  - `実行手順やコマンド`: 1. ALL top-level headings (# ...) with their line numbers
2. Search for any "Part" markers or section dividers
3. Approximate character count for each chapter
4. The first 10 lines after each # heading
5. Total character count of the file

**実際のプロンプト**
```
前回やっていた{タスク名}を再開してほしい

Explore the file {ファイルパス} thoroughly to understand its structure.

I need:
1. ALL top-level headings (# ...) with their line numbers
2. Search for any "Part" markers or section dividers (e.g., "Part 1", "Part 2", "PART", "Section", "---" separators between major sections)
3. Approximate character count for each chapter (between # headings)
4. The first 10 lines after each # heading to understand what that chapter covers
5. Total character count of the file

The goal is to figure out how to chunk this {ファイルサイズ} book into a reasonable number of parts (ideally {数値}) for an LLM analysis pipeline where each chunk is processed separately. The book apparently has {数値} "Parts" according to a navigation guide early in the text.

Return a complete mapping of: heading → line number → approximate length → brief description
```

---

### インスタンス 3: パイプライン調査再開

> 元プロンプト: *Survey the {プロジェクト名} project at {プロジェクトパス} to understand the full pipeline for ingesting books and podcasts and generati*

**変数の値**
  - `タスク名`: パイプライン調査
  - `コンテキスト情報`: 前回の進捗なし、新規調査
  - `具体的な指示`: {プロジェクト名}プロジェクトの全パイプライン（書籍・ポッドキャスト取り込みからブログ記事生成まで）を調査し、コマンド・手動/自動の区別・ギャップを報告してほしい
  - `実行手順やコマンド`: 1. CLIエントリーポイントの特定
2. パイプラインモジュールの読み込み
3. READMEやドキュメントの確認
4. ナイトリーパイプラインの有無確認
5. 書籍ガイド記事生成方法の確認
6. ポッドキャスト記事生成方法の確認

**実際のプロンプト**
```
前回やっていた{タスク名}を再開してほしい

Survey the {プロジェクト名} project at {プロジェクトパス} to understand the full pipeline for ingesting books and podcasts and generating blog articles.

Please find and read:
1. The main CLI entry points (scripts/, __main__.py, or pyproject.toml scripts section)
2. The pipeline modules under {プロジェクト名}/ — especially any "pipeline", "ingest", "guide", "article" related files
3. Any README or docs that describe the end-to-end flow
4. The nightly pipeline if it exists
5. How book guide articles are generated (the homupe .md format)
6. How podcast articles are generated

I want to know:
- What commands exist to run the full pipeline for a NEW book (from raw text → Neo4j KG → homupe article)?
- What commands exist for a NEW podcast (YouTube URL → transcript → Neo4j KG → homupe article)?
- What steps are manual vs automated?
- Are there any obvious gaps in the pipeline?

Report concisely: list the key scripts/commands, what each does, and identify gaps.
```
