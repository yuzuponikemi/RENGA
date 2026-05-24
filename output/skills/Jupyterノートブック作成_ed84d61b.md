# 🔷 スキル定義: Jupyter教育用ノートブック作成

**説明**: 日本語教育用Jupyterノートブックを生成するスキルテンプレート
**ステータス**: ✅ 公開中 | **ソース数**: 25 件 | **カテゴリ**: Jupyterノートブック作成

---

## テンプレートプロンプト（抽象）

```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about {topic}. Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: {chapter_title}
- Difficulty: {difficulty} | {time_estimate}
- Prerequisites: {prerequisites}
- Learning objectives: {learning_objectives}
- Implementations: {implementations}

Structure (~{cell_count} cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty)
2. Table of contents
3. Setup cell (imports: {libraries}; Japanese font; device; seed={seed})
4. {section_1_title}
5. {section_2_title}
6. {section_3_title}
7. {section_4_title}
8. {section_5_title}
9. {section_6_title}
10. {section_7_title}
11. {section_8_title}
12. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Rich code comments.
Use {libraries}. {additional_notes}
Keep models small for educational purposes. CPU-friendly.
```

## 変数一覧

- `{{notebook_path}}`: ノートブックの保存先フルパス（例: /Users/{ユーザー名}/notebooks/chapter.ipynb）
- `{{topic}}`: ノートブックのテーマ（例: Diffusion Transformer (DiT)）
- `{{chapter_title}}`: 章タイトル（例: 第{数値}章: Diffusion Transformer (DiT) — U-NetからTransformerへ）
- `{{difficulty}}`: 難易度（★の数、例: ★★★★☆）
- `{{time_estimate}}`: 所要時間（例: 150-180分）
- `{{prerequisites}}`: 前提知識・前提ノートブック（例: Notebook {数値} (ViT), {数値}）
- `{{learning_objectives}}`: 学習目標（カンマ区切り、例: パッチ埋め込み / adaLN-Zero条件付け / DiTスクラッチ実装）
- `{{implementations}}`: 実装するクラス・関数（カンマ区切り、例: PatchEmbed, AdaLNZero, DiTBlock, DiT）
- `{{cell_count}}`: セル数（例: 45）
- `{{libraries}}`: 使用ライブラリ（例: torch, numpy, matplotlib）
- `{{seed}}`: 乱数シード（例: 42）
- `{{section_1_title}}`: セクション1のタイトル（例: U-NetからDiTへの進化の動機）
- `{{section_2_title}}`: セクション2のタイトル（例: PatchEmbed - 画像をトークン列に変換）
- `{{section_3_title}}`: セクション3のタイトル（例: adaLN-Zero条件付け）
- `{{section_4_title}}`: セクション4のタイトル（例: DiTBlock実装）
- `{{section_5_title}}`: セクション5のタイトル（例: DiT full model）
- `{{section_6_title}}`: セクション6のタイトル（例: 訓練・生成デモ）
- `{{section_7_title}}`: セクション7のタイトル（例: Soraとの技術的関連）
- `{{section_8_title}}`: セクション8のタイトル（例: まとめとクイズ）
- `{{additional_notes}}`: 追加の注意事項（例: 合成データのみ使用、ダウンロード不要）

## 活用シーン

- 機械学習・深層学習の教育カリキュラム用ノートブック作成
- 論文解説・技術調査結果のインタラクティブな教材化
- 社内勉強会やハンズオンセッション用の実装付き資料作成

---

# 🔶 具体インスタンス

### インスタンス 1: DiTノートブック

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook about Diffusion Transformer (DiT). Follo*

**変数の値**
  - `notebook_path`: {ノートブックのパス}
  - `topic`: Diffusion Transformer (DiT)
  - `chapter_title`: 第{数値}章: Diffusion Transformer (DiT) — U-NetからTransformerへ
  - `difficulty`: ★★★★☆
  - `time_estimate`: 150-180分
  - `prerequisites`: Notebook {数値} (ViT), {数値}, {数値} (Latent Diffusion)
  - `learning_objectives`: パッチ埋め込み / adaLN-Zero条件付け / DiTスクラッチ実装 / Soraの技術的基盤
  - `implementations`: PatchEmbed, AdaLNZero, DiTBlock, DiT (MNIST対応)
  - `cell_count`: 45
  - `libraries`: torch, numpy, matplotlib
  - `seed`: 42
  - `section_1_title`: U-NetからDiTへの進化の動機
  - `section_2_title`: PatchEmbed - 画像をトークン列に変換
  - `section_3_title`: adaLN-Zero条件付け - タイムステップとクラスの条件付け
  - `section_4_title`: DiTBlock - Transformer + adaLN-Zero
  - `section_5_title`: DiT full model (MNIST向け軽量版)
  - `section_6_title`: MNIST訓練・生成デモ (短いepoch数で教育目的)
  - `section_7_title`: Soraとの技術的関連
  - `section_8_title`: Summary + common errors + quiz (5 questions with details/summary answers)
  - `additional_notes`: Important implementation details:
- PatchEmbed: Conv2d with kernel_size=patch_size, stride=patch_size
- adaLN-Zero: LayerNorm with learnable scale/shift from condition embedding, plus gate
- DiTBlock: Pre-norm Transformer block with adaLN-Zero instead of standard LayerNorm
- DiT model: PatchEmbed → positional embedding → N × DiTBlock → unpatchify
- Training on MNIST (28x28 padded to 32x32), simple diffusion with cosine schedule
- Keep model small for educational purposes (4 layers, dim=128, 4 heads)

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about Diffusion Transformer (DiT). Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: 第{数値}章: Diffusion Transformer (DiT) — U-NetからTransformerへ
- Difficulty: ★★★★☆ | 150-180分
- Prerequisites: Notebook {数値} (ViT), {数値}, {数値} (Latent Diffusion)
- Learning objectives: パッチ埋め込み / adaLN-Zero条件付け / DiTスクラッチ実装 / Soraの技術的基盤
- Implementations: PatchEmbed, AdaLNZero, DiTBlock, DiT (MNIST対応)

Structure (~45 cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty)
2. Table of contents
3. Setup cell (imports: torch, numpy, matplotlib; Japanese font; device; seed=42)
4. U-NetからDiTへの進化の動機
5. PatchEmbed - 画像をトークン列に変換
6. adaLN-Zero条件付け - タイムステップとクラスの条件付け
7. DiTBlock - Transformer + adaLN-Zero
8. DiT full model (MNIST向け軽量版)
9. MNIST訓練・生成デモ (短いepoch数で教育目的)
10. Soraとの技術的関連
11. Summary + common errors + quiz (5 questions with details/summary answers)

All markdown in Japanese. Rich code comments.
Use torch, numpy, matplotlib. Japanese font setup same as other notebooks.
Use plt.rcParams for figure sizing. Visualizations with proper titles/labels in Japanese.

Important implementation details:
- PatchEmbed: Conv2d with kernel_size=patch_size, stride=patch_size
- adaLN-Zero: LayerNorm with learnable scale/shift from condition embedding, plus gate
- DiTBlock: Pre-norm Transformer block with adaLN-Zero instead of standard LayerNorm
- DiT model: PatchEmbed → positional embedding → N × DiTBlock → unpatchify
- Training on MNIST (28x28 padded to 32x32), simple diffusion with cosine schedule
- Keep model small for educational purposes (4 layers, dim=128, 4 heads)
```

---

### インスタンス 2: DreamerV3ノートブック

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook about DreamerV3 world models. Follow exa*

**変数の値**
  - `notebook_path`: {ノートブックのパス}
  - `topic`: DreamerV3 world models
  - `chapter_title`: 第{数値}章: DreamerV3 — 夢の中で数千回試行する世界モデル
  - `difficulty`: ★★★★★
  - `time_estimate`: 180-240分
  - `prerequisites`: Notebook {数値}, {数値} (VAE/PyTorch), {数値} (JEPA)
  - `learning_objectives`: RSSM（確定的+確率的状態遷移）/ 3フェーズ学習（世界モデル→想像→データ収集）/ Imagination Rollout / Actor-Critic
  - `implementations`: RSSM, WorldModel, Actor, Critic, SimpleDreamer, imagine_rollout, 「夢」の可視化
  - `cell_count`: 48
  - `libraries`: torch, numpy, matplotlib
  - `seed`: 42
  - `section_1_title`: DreamerV3の全体像
  - `section_2_title`: RSSM (Recurrent State Space Model)
  - `section_3_title`: WorldModel
  - `section_4_title`: 世界モデルの訓練
  - `section_5_title`: Imagination Rollout
  - `section_6_title`: Actor-Critic in Imagination
  - `section_7_title`: 「夢」の可視化
  - `section_8_title`: DreamerV3の技術的革新
  - `additional_notes`: No gymnasium needed - use custom simple environment. Keep models small (dim=64, 2-3 layers). Educational focus. All data synthetic, no downloads.

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about DreamerV3 world models. Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: 第{数値}章: DreamerV3 — 夢の中で数千回試行する世界モデル
- Difficulty: ★★★★★ | 180-240分
- Prerequisites: Notebook {数値}, {数値} (VAE/PyTorch), {数値} (JEPA)
- Learning objectives: RSSM（確定的+確率的状態遷移）/ 3フェーズ学習（世界モデル→想像→データ収集）/ Imagination Rollout / Actor-Critic
- Implementations: RSSM, WorldModel, Actor, Critic, SimpleDreamer, imagine_rollout, 「夢」の可視化

Structure (~48 cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty ★★★★★)
2. Table of contents
3. Setup cell (torch, numpy, matplotlib, warnings; Japanese font; device; seed=42)
4. DreamerV3の全体像
5. RSSM (Recurrent State Space Model)
6. WorldModel
7. 世界モデルの訓練
8. Imagination Rollout
9. Actor-Critic in Imagination
10. 「夢」の可視化
11. DreamerV3の技術的革新
12. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Rich code comments.
Use torch, numpy, matplotlib. No gymnasium needed - use custom simple environment.
Keep models small (dim=64, 2-3 layers). Educational focus.
All data synthetic, no downloads.
```

---

### インスタンス 3: JEPAノートブック

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook about JEPA (Joint Embedding Predictive A*

**変数の値**
  - `notebook_path`: {ノートブックのパス}
  - `topic`: JEPA (Joint Embedding Predictive Architecture)
  - `chapter_title`: 第{数値}章: JEPA — Joint Embedding Predictive Architecture
  - `difficulty`: ★★★★☆
  - `time_estimate`: 150-180分
  - `prerequisites`: Notebook {数値}, {数値} (ViT), {数値} (Temporal Attention)
  - `learning_objectives`: I-JEPAの非対称マスキング / Context/Target Encoder + Predictor / EMA更新 / MAEとの違い / V-JEPAへの拡張
  - `implementations`: MultiBlockMasking, ContextEncoder, TargetEncoder, Predictor, IJEPA, ema_update
  - `cell_count`: 45
  - `libraries`: torch, numpy, matplotlib
  - `seed`: 42
  - `section_1_title`: JEPAの思想 — なぜピクセル再構成ではダメなのか
  - `section_2_title`: I-JEPA アーキテクチャの解剖
  - `section_3_title`: MultiBlockMasking の実装
  - `section_4_title`: エンコーダとプレディクタの実装
  - `section_5_title`: EMA更新の実装と理解
  - `section_6_title`: I-JEPA訓練ループ
  - `section_7_title`: 学習済み表現の評価
  - `section_8_title`: V-JEPAへの拡張（概念）
  - `additional_notes`: Use torchvision for datasets. Keep models small for educational purposes. CPU-friendly with small data.

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about JEPA (Joint Embedding Predictive Architecture). Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: 第{数値}章: JEPA — Joint Embedding Predictive Architecture
- Difficulty: ★★★★☆ | 150-180分
- Prerequisites: Notebook {数値}, {数値} (ViT), {数値} (Temporal Attention)
- Learning objectives: I-JEPAの非対称マスキング / Context/Target Encoder + Predictor / EMA更新 / MAEとの違い / V-JEPAへの拡張
- Implementations: MultiBlockMasking, ContextEncoder, TargetEncoder, Predictor, IJEPA, ema_update

Structure (~45 cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty ★★★★☆)
2. Table of contents
3. Setup cell (torch, numpy, matplotlib, warnings; Japanese font; device; seed=42)
4. JEPAの思想 — なぜピクセル再構成ではダメなのか
5. I-JEPA アーキテクチャの解剖
6. MultiBlockMasking の実装
7. エンコーダとプレディクタの実装
8. EMA更新の実装と理解
9. I-JEPA訓練ループ
10. 学習済み表現の評価
11. V-JEPAへの拡張（概念）
12. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Rich code comments.
Use torch, numpy, matplotlib. Use torchvision for datasets.
Keep models small for educational purposes. CPU-friendly with small data.
```
