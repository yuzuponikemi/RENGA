# 🔷 スキル定義: コードベース探索スキル

**説明**: 特定の機能やアーキテクチャを理解するためのコードベース探索
**ステータス**: ✅ 公開中 | **ソース数**: 8 件 | **カテゴリ**: コードベース探索

---

## テンプレートプロンプト（抽象）

```
I need to understand the current {project_name} codebase to plan a {feature_name} feature.

Please explore:

1. **{first_component_name}**: Read {first_file_path} to understand {first_aspect}
2. **{second_component_name}**: Read {second_file_path} to understand {second_aspect}
3. **{third_component_name}**: Read {third_file_path} to understand {third_aspect}
4. **{fourth_component_name}**: Read {fourth_file_path} to see the {fourth_aspect}
5. **{fifth_component_name}**: Read {fifth_file_path} to understand {fifth_aspect}
6. **{sixth_component_name}**: Read {sixth_file_path} to understand {sixth_aspect}
7. **{seventh_component_name}**: Read {seventh_file_path} to understand {seventh_aspect}

Focus on understanding the data structures that flow between stages, especially the {key_data_format} format, so we can design the {feature_name} stage properly.
```

## 変数一覧

- `{{project_name}}`: 探索対象のプロジェクト名
- `{{feature_name}}`: 実装予定の機能名
- `{{first_component_name}}`: 最初に探索するコンポーネント名
- `{{first_file_path}}`: 最初に読むファイルのパス
- `{{first_aspect}}`: 最初のファイルで理解すべき内容
- `{{second_component_name}}`: 2番目に探索するコンポーネント名
- `{{second_file_path}}`: 2番目に読むファイルのパス
- `{{second_aspect}}`: 2番目のファイルで理解すべき内容
- `{{third_component_name}}`: 3番目に探索するコンポーネント名
- `{{third_file_path}}`: 3番目に読むファイルのパス
- `{{third_aspect}}`: 3番目のファイルで理解すべき内容
- `{{fourth_component_name}}`: 4番目に探索するコンポーネント名
- `{{fourth_file_path}}`: 4番目に読むファイルのパス
- `{{fourth_aspect}}`: 4番目のファイルで理解すべき内容
- `{{fifth_component_name}}`: 5番目に探索するコンポーネント名
- `{{fifth_file_path}}`: 5番目に読むファイルのパス
- `{{fifth_aspect}}`: 5番目のファイルで理解すべき内容
- `{{sixth_component_name}}`: 6番目に探索するコンポーネント名
- `{{sixth_file_path}}`: 6番目に読むファイルのパス
- `{{sixth_aspect}}`: 6番目のファイルで理解すべき内容
- `{{seventh_component_name}}`: 7番目に探索するコンポーネント名
- `{{seventh_file_path}}`: 7番目に読むファイルのパス
- `{{seventh_aspect}}`: 7番目のファイルで理解すべき内容
- `{{key_data_format}}`: 特に注目すべきデータ形式

## 活用シーン

- 新機能追加前に既存コードベースのアーキテクチャを理解する
- 既存のデータフローやAPIを調査してリファクタリング計画を立てる
- 特定のコンポーネントの実装方法を調査する

---

# 🔶 具体インスタンス

### インスタンス 1: TTS機能実装調査

> 元プロンプト: *I need to understand the current Project Cogito codebase to plan a text-to-speech (TTS) feature that converts generated *

**変数の値**
  - `project_name`: Project Cogito
  - `feature_name`: text-to-speech (TTS)
  - `first_component_name`: Script output format
  - `first_file_path`: data/run_20260210_180656/05_scripts.md and data/run_20260210_180656/05_scripts.json
  - `first_aspect`: the exact structure of generated scripts (speakers, dialogue lines, opening/closing, etc.)
  - `second_component_name`: Pipeline architecture
  - `second_file_path`: main.py
  - `second_aspect`: how pipeline stages are chained and how a new "audio generation" stage would fit in
  - `third_component_name`: Existing models/config
  - `third_file_path`: src/models.py and config/personas.yaml
  - `third_aspect`: persona structure and whether voice mappings could be added
  - `fourth_component_name`: Book config
  - `fourth_file_path`: config/books/descartes_discourse.yaml
  - `fourth_aspect`: the config pattern
  - `fifth_component_name`: Requirements
  - `fifth_file_path`: requirements.txt
  - `fifth_aspect`: current dependencies
  - `sixth_component_name`: 
  - `sixth_file_path`: 
  - `sixth_aspect`: 
  - `seventh_component_name`: 
  - `seventh_file_path`: 
  - `seventh_aspect`: 
  - `key_data_format`: script JSON

**実際のプロンプト**
```
I need to understand the current {project_name} codebase to plan a {feature_name} feature that converts generated podcast scripts into audio files.

Please explore:

1. **{first_component_name}**: Read {first_file_path} to understand the exact structure of generated scripts (speakers, dialogue lines, opening/closing, etc.)

2. **{second_component_name}**: Read {second_file_path} to understand how pipeline stages are chained and how a new "audio generation" stage would fit in

3. **{third_component_name}**: Read {third_file_path} to understand persona structure and whether voice mappings could be added

4. **{fourth_component_name}**: Read {fourth_file_path} to see the config pattern

5. **{fifth_component_name}**: Read {fifth_file_path} to see current dependencies

Focus on understanding the data structures that flow between stages, especially the {key_data_format} format, so we can design the TTS stage properly.
```

---

### インスタンス 2: コードベース全体探索

> 元プロンプト: *Very thorough exploration of the Project Cogito codebase at /Users/ikmx/source/personal/book-research. I need to underst*

**変数の値**
  - `project_name`: Project Cogito
  - `feature_name`: comprehensive architecture understanding
  - `first_component_name`: Graph wiring
  - `first_file_path`: src/graph.py
  - `first_aspect`: how the LangGraph pipeline is wired
  - `second_component_name`: Node implementations
  - `second_file_path`: all node implementations under src/ (reader, director, researcher, critic, audio, etc.)
  - `second_aspect`: their roles
  - `third_component_name`: Config system
  - `third_file_path`: config/books/*.yaml examples and config/personas.yaml
  - `third_aspect`: the config structure
  - `fourth_component_name`: LLM calls
  - `fourth_file_path`: the relevant files
  - `fourth_aspect`: ChatOllama patterns and model selection
  - `fifth_component_name`: Audio pipeline
  - `fifth_file_path`: the audio-related files
  - `fifth_aspect`: VOICEVOX integration
  - `sixth_component_name`: Translation pipeline
  - `sixth_file_path`: the translation-related files
  - `sixth_aspect`: the translation pipeline
  - `seventh_component_name`: Research pipeline
  - `seventh_file_path`: the research/critique/enrichment pipeline files
  - `seventh_aspect`: data flow
  - `key_data_format`: state schema

**実際のプロンプト**
```
I need to understand the current {project_name} codebase to plan a comprehensive architecture understanding.

Please explore:

1. **{first_component_name}**: Read {first_file_path} to understand how the LangGraph pipeline is wired
2. **{second_component_name}**: Read {second_file_path} to understand their roles
3. **{third_component_name}**: Read {third_file_path} to understand the config structure
4. **{fourth_component_name}**: Read {fourth_file_path} to understand ChatOllama patterns and model selection
5. **{fifth_component_name}**: Read {fifth_file_path} to understand VOICEVOX integration
6. **{sixth_component_name}**: Read {sixth_file_path} to understand the translation pipeline
7. **{seventh_component_name}**: Read {seventh_file_path} to understand data flow
8. **State schema**: Read the state schema files to understand data flow between nodes
9. **Book configs**: Read existing book configs to understand supported book types
10. **Prompt templates**: Read the prompt template files to understand the prompts used

Focus on understanding the data structures that flow between stages, especially the {key_data_format} format, so we can design the comprehensive architecture understanding stage properly.
```

---

### インスタンス 3: トレーニングパイプライン調査

> 元プロンプト: *Explore the current training pipeline for the GomokuGPT Transformer model. I need to understand:*

**変数の値**
  - `project_name`: GomokuGPT
  - `feature_name`: winner-only training masking
  - `first_component_name`: Data format
  - `first_file_path`: training_data.jsonl
  - `first_aspect`: the schema, especially the "winner" field
  - `second_component_name`: Model config defaults
  - `second_file_path`: model.py
  - `second_aspect`: GomokuGPTConfig defaults (n_layer, n_head, n_embd, max_seq_len, vocab_size, etc.)
  - `third_component_name`: Dataset class
  - `third_file_path`: train.py
  - `third_aspect`: GomokuDataset class - how it creates input/target pairs, and the collate_fn
  - `fourth_component_name`: Training functions
  - `fourth_file_path`: train.py
  - `fourth_aspect`: train_epoch and evaluate functions - how loss is computed
  - `fifth_component_name`: Forward method
  - `fifth_file_path`: model.py
  - `fifth_aspect`: GomokuGPT forward method - how loss is computed (look for cross_entropy or similar)
  - `sixth_component_name`: Augmentation functions
  - `sixth_file_path`: train.py
  - `sixth_aspect`: augmentation functions already in train.py (augment_moves, _SYMMETRY_TABLES etc.)
  - `seventh_component_name`: 
  - `seventh_file_path`: 
  - `seventh_aspect`: 
  - `key_data_format`: loss computation

**実際のプロンプト**
```
I need to understand the current {project_name} codebase to plan a winner-only training masking feature.

Please explore:

1. **{first_component_name}**: Read {first_file_path} (read a few lines to see the schema, especially the "winner" field) to understand the data format
2. **{second_component_name}**: Read {second_file_path} to understand GomokuGPTConfig defaults (n_layer, n_head, n_embd, max_seq_len, vocab_size, etc.)
3. **{third_component_name}**: Read {third_file_path} to understand GomokuDataset class - how it creates input/target pairs, and the collate_fn
4. **{fourth_component_name}**: Read {fourth_file_path} to understand train_epoch and evaluate functions - how loss is computed
5. **{fifth_component_name}**: Read {fifth_file_path} to understand GomokuGPT forward method - how loss is computed (look for cross_entropy or similar)
6. **{sixth_component_name}**: Read {sixth_file_path} to understand augmentation functions already in train.py (augment_moves, _SYMMETRY_TABLES etc.)

Focus on understanding the data structures that flow between stages, especially the {key_data_format} format, so we can design the winner-only training masking stage properly.
```
