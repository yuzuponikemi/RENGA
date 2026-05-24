---
name: ノートブック日本語プロット翻訳
skill_id: de0fc4d6-fdf2-41fe-9ba1-dff161fa5b47
version: 1.0.0
category: プロット要素の日英翻訳
status: pending
source_count: 10
unique_user_count: 2
variables:
- target_files
- translation_patterns
triggers:
- ノートブックの日本語を英語に翻訳して
- プロットの日本語ラベルを英語に変換
- Jupyterの日本語プロット要素を英訳
- ノートブックの日本語テキストを英語に
- matplotlibの日本語を英語に置換
---

# ノートブック日本語プロット翻訳

**説明**: Jupyterノートブックのプロット要素の日本語を英語に翻訳する
**ステータス**: 🔒 審査中 | **ソース数**: 10 件 | **ユニークユーザー**: 2 人 | **カテゴリ**: プロット要素の日英翻訳

---

## テンプレートプロンプト

```
以下のJupyterノートブックファイルにおいて、コードセル内のmatplotlib/seabornプロット要素（タイトル、軸ラベル、凡例、注釈、テキスト）に含まれる日本語テキストをすべて英語に翻訳してください。

【重要ルール】
- 修正対象はCODEセルのみ、markdownセルは変更しない
- プロット関連関数（set_title, set_xlabel, set_ylabel, suptitle, .text(), label=, annotate, Patch(, axhline, legend, fig.text, set_xticklabels, plt.title, plt.xlabel, plt.ylabel）の引数内の文字列のみを変更
- コメント（#で始まる行）やprint()文は変更しない
- docstringは変更しない
- コード構造は完全に維持し、日本語文字列のみを英語に変更
- japanize_matplotlibは使用しない

【処理対象ファイル】
{target_files}

【アプローチ】
1. 各ノートブックをJSONとして読み込む
2. コードセルをイテレートし、プロット関連行の日本語文字列を検出
3. 日本語→英語の翻訳マップを作成し、置換を実行
4. ノートブックをJSONとして保存

【翻訳パターン（例）】
{translation_patterns}

【確認】
スクリプト実行後、各ノートブックのプロット行に残っている日本語をカウントし、0になるまで再実行してください。
```

## 変数一覧

- `{{target_files}}`: 処理対象のノートブックファイルのリスト（パスとインスタンス数を含む）。例: ['1. /path/to/notebook1.ipynb (71 instances)', '2. /path/to/notebook2.ipynb (70 instances)']
- `{{translation_patterns}}`: 日本語から英語への翻訳パターン一覧。例: '- 受容野 -> Receptive Field\n- 層/レイヤー -> Layer\n- 入力 -> Input'

## 活用シーン

- 機械学習の教育用ノートブックを英語化して国際公開する
- 日本語混在の研究用ノートブックを英語論文用に整備する
- チーム内で共有するノートブックの言語を統一する

## トリガーフレーズ

- `ノートブックの日本語を英語に翻訳して`
- `プロットの日本語ラベルを英語に変換`
- `Jupyterの日本語プロット要素を英訳`
- `ノートブックの日本語テキストを英語に`
- `matplotlibの日本語を英語に置換`

---

## 具体インスタンス

### インスタンス 1: World Models翻訳

> 元プロンプト: *You need to translate Japanese text in matplotlib/seaborn plot elements to English in Jupyter notebooks.  IMPORTANT RULE*

**変数の値**
  - `target_files`: 1. {プロジェクトルート}/notebooks/world-models/140_representation_learning_for_prediction_v1.ipynb (71 instances)
2. {プロジェクトルート}/notebooks/world-models/142_model_based_rl_fundamentals_v1.ipynb (70 instances)
3. {プロジェクトルート}/notebooks/world-models/143_dreamerv3_world_model_v1.ipynb (29 instances)
4. {プロジェクトルート}/notebooks/world-models/144_genie_interactive_worlds_v1.ipynb (43 instances)
5. {プロジェクトルート}/notebooks/world-models/145_grid_world_agent_v1.ipynb (32 instances)
6. {プロジェクトルート}/notebooks/world-models/146_world_models_synthesis_v1.ipynb (43 instances)
  - `translation_patterns`: - 受容野 -> Receptive Field
- 層/レイヤー -> Layer
- 入力 -> Input
- 出力 -> Output
- 畳み込み -> Convolution
- 全結合 -> Fully Connected
- 重み共有 -> Weight Sharing
- カーネル -> Kernel
- パディング -> Padding
- ストライド -> Stride
- 特徴マップ -> Feature Map
- ダウンサンプリング -> Downsampling
- パラメータ -> Parameter(s)
- 精度/正確度 -> Accuracy
- 損失 -> Loss
- 計算量 -> Computation Cost
- データ量 -> Data Size
- 帰納バイアス -> Inductive Bias
- 並行移動不変性 -> Translation Invariance
- 並行移動等変性 -> Translation Equivariance
- 局所性 -> Locality
- 階層的特徴抽象化 -> Hierarchical Feature Abstraction
- 活性化 -> Activation
- 解像度 -> Resolution
- 空間次元 -> Spatial Dimension

**実際のプロンプト**
```
以下のJupyterノートブックファイルにおいて、コードセル内のmatplotlib/seabornプロット要素（タイトル、軸ラベル、凡例、注釈、テキスト）に含まれる日本語テキストをすべて英語に翻訳してください。

【重要ルール】
- 修正対象はCODEセルのみ、markdownセルは変更しない
- プロット関連関数（set_title, set_xlabel, set_ylabel, suptitle, .text(), label=, annotate, Patch(, axhline, legend, fig.text, set_xticklabels, plt.title, plt.xlabel, plt.ylabel）の引数内の文字列のみを変更
- コメント（#で始まる行）やprint()文は変更しない
- docstringは変更しない
- コード構造は完全に維持し、日本語文字列のみを英語に変更
- japanize_matplotlibは使用しない

【処理対象ファイル】
{target_files}

【アプローチ】
1. 各ノートブックをJSONとして読み込む
2. コードセルをイテレートし、プロット関連行の日本語文字列を検出
3. 日本語→英語の翻訳マップを作成し、置換を実行
4. ノートブックをJSONとして保存

【翻訳パターン（例）】
{translation_patterns}

【確認】
スクリプト実行後、各ノートブックのプロット行に残っている日本語をカウントし、0になるまで再実行してください。
```

---

### インスタンス 2: Spatial CNN前半翻訳

> 元プロンプト: *In these 4 Jupyter notebook files, replace ALL Japanese text in code cells that appears in matplotlib/seaborn plot eleme*

**変数の値**
  - `target_files`: 1. {プロジェクトルート}/notebooks/spatial-cnn/80_what_is_convolution_v1.ipynb
2. {プロジェクトルート}/notebooks/spatial-cnn/81_convolution_math_v1.ipynb
3. {プロジェクトルート}/notebooks/spatial-cnn/82_convolution_numpy_basic_v1.ipynb
4. {プロジェクトルート}/notebooks/spatial-cnn/83_convolution_numpy_fast_v1.ipynb
  - `translation_patterns`: - 畳み込み -> Convolution, 入力 -> Input, 出力 -> Output
- カーネル -> Kernel, パディング -> Padding, ストライド -> Stride
- 元画像/元の画像 -> Original Image, テスト画像 -> Test Image
- 入力画像 -> Input Image, 出力画像 -> Output Image
- 計算時間 -> Computation Time, 画像サイズ -> Image Size
- ぼかし -> Blur, エッジ検出 -> Edge Detection
- 信号 -> Signal, 位置 -> Position, 値 -> Value
- 生データ -> Raw Data, 移動平均 -> Moving Average
- 日/日数 -> Days, 株価 -> Stock Price
- 重み/重み値 -> Weight(s), 密度 -> Density
- フィルタ -> Filter, 高速化率 -> Speedup Ratio
- 愚直版 -> Naive, ベクトル化版 -> Vectorized, im2col版 -> im2col
- 反転 -> Flip/Inversion, 相関 -> Correlation
- パディング領域 -> Padding Region, 元データ -> Original Data
- 出力が縮小 -> Output Shrinks, 出力サイズ維持 -> Maintains Output Size
- ゼロパディング -> Zero Padding, 反射パディング -> Reflect Padding
- 断面 -> Cross-Section, 境界 -> Boundary
- 対数スケール -> Log Scale, 線形スケール -> Linear Scale

**実際のプロンプト**
```
以下のJupyterノートブックファイルにおいて、コードセル内のmatplotlib/seabornプロット要素（タイトル、軸ラベル、凡例、注釈、テキスト）に含まれる日本語テキストをすべて英語に翻訳してください。

【重要ルール】
- 修正対象はCODEセルのみ、markdownセルは変更しない
- プロット関連関数（set_title, set_xlabel, set_ylabel, suptitle, .text(), label=, annotate, Patch(, axhline, legend, fig.text, set_xticklabels, plt.title, plt.xlabel, plt.ylabel）の引数内の文字列のみを変更
- コメント（#で始まる行）やprint()文は変更しない
- docstringは変更しない
- コード構造は完全に維持し、日本語文字列のみを英語に変更
- japanize_matplotlibは使用しない

【処理対象ファイル】
{target_files}

【アプローチ】
1. 各ノートブックをJSONとして読み込む
2. コードセルをイテレートし、プロット関連行の日本語文字列を検出
3. 日本語→英語の翻訳マップを作成し、置換を実行
4. ノートブックをJSONとして保存

【翻訳パターン（例）】
{translation_patterns}

【確認】
スクリプト実行後、各ノートブックのプロット行に残っている日本語をカウントし、0になるまで再実行してください。
```

---

### インスタンス 3: japanize_matplotlib削除

> 元プロンプト: *Remove all `import japanize_matplotlib` and `japanize_matplotlib` references from these {数値} notebook files. The import *

**変数の値**
  - `target_files`: - {プロジェクトルート}/notebooks/world-models/145_grid_world_agent_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/102_future_outlook_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/101_synthesis_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/100_applications_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/99_skip_connections_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/98_feature_pyramid_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/97_unet_architecture_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/96_semantic_segmentation_intro_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/95_beyond_cnn_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/94_when_cnn_fails_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/93_cnn_vs_mlp_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/92_translation_equivariance_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/91_weight_sharing_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/90_inductive_bias_intro_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/89_receptive_field_3dgs_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/88_downsampling_v1.ipynb
- {プロジェクトルート}/notebooks/spatial-cnn/87_receptive_field_depth_v1.ipynb
  - `translation_patterns`: （このインスタンスでは翻訳パターンは不要。代わりに削除処理を指定）

**実際のプロンプト**
```
以下の{数値}個のノートブックファイルから、`import japanize_matplotlib` および `japanize_matplotlib` の参照をすべて削除してください。import行は完全に削除（コメントアウトではなく）してください。

【処理対象ファイル】
{target_files}

【アプローチ】
各ノートブックに対してPythonスクリプトを使用し：
1. .ipynb JSONを読み込む
2. コードセルのソースから `import japanize_matplotlib` を含む行を検索して削除
3. 削除後に空行のみが残る場合はその空行も削除
4. ファイルを保存

単一のPythonスクリプトですべてのファイルを一括処理してください。
```
