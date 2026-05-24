---
name: Jupyterノートブック作成
skill_id: d829a050-ef3a-46bf-97dd-fbeba4229dd1
version: 1.0.0
category: Jupyterノートブック作成
status: public
source_count: 25
unique_user_count: 1
variables:
- notebook_path
- topic_title
- chapter_title
- difficulty_rating
- estimated_minutes
- prerequisites
- learning_objectives
- key_implementations
- cell_count
- libraries
- section1_title
- section1_content
- section2_title
- section2_content
- section3_title
- section3_content
- section4_title
- section4_content
- section5_title
- section5_content
- section6_title
- section6_content
- section7_title
- section7_content
- section8_title
- section8_content
- additional_notes
triggers:
- ノートブックを作成して
- Jupyterノートブックを書いて
- 教育用ノートブックを生成して
- チュートリアルノートブックを作って
- notebookを書いて
---

# Jupyterノートブック作成

**説明**: 教育用Jupyterノートブックを生成するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 25 件 | **ユニークユーザー**: 1 人 | **カテゴリ**: Jupyterノートブック作成

---

## テンプレートプロンプト

```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about {topic_title}. Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: {chapter_title}
- Difficulty: {difficulty_rating} | {estimated_minutes}分
- Prerequisites: {prerequisites}
- Learning objectives: {learning_objectives}
- Implementations: {key_implementations}

Structure (~{cell_count} cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty)
2. Table of contents
3. Setup cell (imports: {libraries}; Japanese font; device; seed=42)
4. Section 1: {section1_title}
   - {section1_content}
5. Section 2: {section2_title}
   - {section2_content}
6. Section 3: {section3_title}
   - {section3_content}
7. Section 4: {section4_title}
   - {section4_content}
8. Section 5: {section5_title}
   - {section5_content}
9. Section 6: {section6_title}
   - {section6_content}
10. Section 7: {section7_title}
    - {section7_content}
11. Section 8: {section8_title}
    - {section8_content}
12. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Rich code comments.
Use {libraries}. {additional_notes}
Keep models small for educational purposes. CPU-friendly with small data.
```

## 変数一覧

- `{{notebook_path}}`: ノートブックの保存先パス（例: /Users/{ユーザー名}/source/{リポジトリ名}/notebooks/{カテゴリ}/{ファイル名}.ipynb）
- `{{topic_title}}`: ノートブックのテーマ（例: DreamerV3 World Models）
- `{{chapter_title}}`: 章タイトル（例: 第{数値}章: {テーマ名} — {サブタイトル}）
- `{{difficulty_rating}}`: 難易度（例: ★★★★★）
- `{{estimated_minutes}}`: 推定所要時間（例: 180-240）
- `{{prerequisites}}`: 前提ノートブック（例: Notebook {番号}, {番号}）
- `{{learning_objectives}}`: 学習目標（カンマ区切り、例: RSSM / 3フェーズ学習 / Imagination Rollout）
- `{{key_implementations}}`: 実装するクラス・関数（例: RSSM, WorldModel, Actor, Critic）
- `{{cell_count}}`: セル数（例: 48）
- `{{libraries}}`: 使用ライブラリ（例: torch, numpy, matplotlib）
- `{{section1_title}}`: セクション1のタイトル
- `{{section1_content}}`: セクション1の内容説明
- `{{section2_title}}`: セクション2のタイトル
- `{{section2_content}}`: セクション2の内容説明
- `{{section3_title}}`: セクション3のタイトル
- `{{section3_content}}`: セクション3の内容説明
- `{{section4_title}}`: セクション4のタイトル
- `{{section4_content}}`: セクション4の内容説明
- `{{section5_title}}`: セクション5のタイトル
- `{{section5_content}}`: セクション5の内容説明
- `{{section6_title}}`: セクション6のタイトル
- `{{section6_content}}`: セクション6の内容説明
- `{{section7_title}}`: セクション7のタイトル
- `{{section7_content}}`: セクション7の内容説明
- `{{section8_title}}`: セクション8のタイトル
- `{{section8_content}}`: セクション8の内容説明
- `{{additional_notes}}`: 追加の注意事項（例: カスタム環境を使用。ダウンロード不要。）

## 活用シーン

- 機械学習の教育カリキュラム用ノートブック作成
- 論文実装のチュートリアルノートブック作成
- 社内勉強会用のハンズオンノートブック作成

## トリガーフレーズ

- `ノートブックを作成して`
- `Jupyterノートブックを書いて`
- `教育用ノートブックを生成して`
- `チュートリアルノートブックを作って`
- `notebookを書いて`

---

## 具体インスタンス

### インスタンス 1: DreamerV3ノートブック

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook about DreamerV3 world models. Follow exa*

**変数の値**
  - `notebook_path`: /Users/{ユーザー名}/source/{リポジトリ名}/notebooks/world-models/{番号}_dreamerv3_world_model_v1.ipynb
  - `topic_title`: DreamerV3 world models
  - `chapter_title`: 第{数値}章: DreamerV3 — 夢の中で数千回試行する世界モデル
  - `difficulty_rating`: ★★★★★
  - `estimated_minutes`: 180-240
  - `prerequisites`: Notebook {番号}, {番号} (VAE/PyTorch), {番号} (JEPA)
  - `learning_objectives`: RSSM（確定的+確率的状態遷移）/ 3フェーズ学習（世界モデル→想像→データ収集）/ Imagination Rollout / Actor-Critic
  - `key_implementations`: RSSM, WorldModel, Actor, Critic, SimpleDreamer, imagine_rollout, 「夢」の可視化
  - `cell_count`: 48
  - `libraries`: torch, numpy, matplotlib
  - `section1_title`: DreamerV3の全体像
  - `section1_content`: Three-phase learning: World Model → Imagination → Data Collection. Diagram showing the three phases. Why "dreaming" works: learn policies in imagined trajectories. Connection to human dreaming/mental simulation.
  - `section2_title`: RSSM (Recurrent State Space Model)
  - `section2_content`: Deterministic state h_t (captures history) via GRU. Stochastic state z_t (captures uncertainty) via learned distribution. Combined state s_t = (h_t, z_t). Prior: p(z_t | h_t) - predicted without observation. Posterior: q(z_t | h_t, o_t) - with observation. RSSM class implementation with GRU for deterministic path, MLP for prior and posterior.
  - `section3_title`: WorldModel
  - `section3_content`: Observation encoder: small CNN → latent. Observation decoder: latent → reconstructed observation. Reward predictor: state → reward. Continue predictor: state → done probability. WorldModel class combining RSSM + encoder + decoder + reward + continue. Loss: reconstruction + reward + KL divergence.
  - `section4_title`: 世界モデルの訓練
  - `section4_content`: Simple environment: BouncingBall1D. State: (position, velocity), observation: position as 1D "image" (32-dim vector). Action: push left/right. Reward: stay near center. Collect random trajectories (500 episodes). Train world model on collected data (20 epochs). Show reconstruction quality, KL divergence curve.
  - `section5_title`: Imagination Rollout
  - `section5_content`: imagine_rollout function: given initial state, roll out world model with actor. Generate imagined trajectories of length H=15. Visualize imagined vs real trajectories. Show how model captures dynamics.
  - `section6_title`: Actor-Critic in Imagination
  - `section6_content`: Actor: state → action distribution (simple MLP). Critic: state → value estimate (simple MLP). Train Actor-Critic on imagined trajectories (policy gradient). SimpleDreamer class: combines world model + actor + critic. Training loop: alternate data collection, world model update, policy update.
  - `section7_title`: 「夢」の可視化
  - `section7_content`: Visualize imagined rollouts as frame sequences. Compare imagined trajectories vs real environment. Show how policy improves through imagination. Plot: real reward improvement over training iterations.
  - `section8_title`: DreamerV3の技術的革新
  - `section8_content`: Symlog predictions. Discrete latent states (categorical). Scaling across diverse domains. Comparison table: DreamerV1 vs V2 vs V3.
  - `additional_notes`: No gymnasium needed - use custom simple environment. All data synthetic, no downloads.

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about DreamerV3 world models. Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: 第{数値}章: DreamerV3 — 夢の中で数千回試行する世界モデル
- Difficulty: ★★★★★ | 180-240分
- Prerequisites: Notebook {番号}, {番号} (VAE/PyTorch), {番号} (JEPA)
- Learning objectives: RSSM（確定的+確率的状態遷移）/ 3フェーズ学習（世界モデル→想像→データ収集）/ Imagination Rollout / Actor-Critic
- Implementations: RSSM, WorldModel, Actor, Critic, SimpleDreamer, imagine_rollout, 「夢」の可視化

Structure (~48 cells):
1. Title + metadata (learning objectives, prerequisites, time, difficulty ★★★★★)
2. Table of contents
3. Setup cell (torch, numpy, matplotlib, warnings; Japanese font; device; seed=42)
4. Section 1: DreamerV3の全体像
   - Three-phase learning: World Model → Imagination → Data Collection
   - Diagram showing the three phases
   - Why "dreaming" works: learn policies in imagined trajectories
   - Connection to human dreaming/mental simulation
5. Section 2: RSSM (Recurrent State Space Model)
   - Deterministic state h_t (captures history) via GRU
   - Stochastic state z_t (captures uncertainty) via learned distribution
   - Combined state s_t = (h_t, z_t)
   - Prior: p(z_t | h_t) - predicted without observation
   - Posterior: q(z_t | h_t, o_t) - with observation
   - RSSM class implementation:
     - GRU for deterministic path
     - MLP for prior (h_t → z_t distribution)
     - MLP for posterior (h_t, o_t → z_t distribution)
   - Use simple Gaussian with dim=16 for stochastic state
   - Deterministic state dim=64
6. Section 3: WorldModel
   - Observation encoder: small CNN → latent
   - Observation decoder: latent → reconstructed observation
   - Reward predictor: state → reward
   - Continue predictor: state → done probability
   - WorldModel class combining RSSM + encoder + decoder + reward + continue
   - Loss: reconstruction + reward + KL divergence
7. Section 4: 世界モデルの訓練
   - Simple environment: CartPole-like (or custom simple env with numpy)
   - Actually, use a simple custom env: BouncingBall1D
     - State: (position, velocity), observation: position as 1D "image" (32-dim vector)
     - Action: push left/right
     - Reward: stay near center
   - Collect random trajectories (500 episodes)
   - Train world model on collected data (20 epochs)
   - Show reconstruction quality, KL divergence curve
8. Section 5: Imagination Rollout
   - imagine_rollout function: given initial state, roll out world model with actor
   - Generate imagined trajectories of length H=15
   - Visualize imagined vs real trajectories
   - Show how model captures dynamics
9. Section 6: Actor-Critic in Imagination
   - Actor: state → action distribution (simple MLP)
   - Critic: state → value estimate (simple MLP)
   - Train Actor-Critic on imagined trajectories (policy gradient)
   - SimpleDreamer class: combines world model + actor + critic
   - Training loop: alternate data collection, world model update, policy update
10. Section 7: 「夢」の可視化
    - Visualize imagined rollouts as frame sequences
    - Compare imagined trajectories vs real environment
    - Show how policy improves through imagination
    - Plot: real reward improvement over training iterations
11. Section 8: DreamerV3の技術的革新
    - Symlog predictions
    - Discrete latent states (categorical)
    - Scaling across diverse domains
    - Comparison table: DreamerV1 vs V2 vs V3
12. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Rich code comments.
Use torch, numpy, matplotlib. No gymnasium needed - use custom simple environment.
Keep models small (dim=64, 2-3 layers). Educational focus.
All data synthetic, no downloads.
```

---

### インスタンス 2: DiTノートブック

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook about Diffusion Transformer (DiT). Follo*

**変数の値**
  - `notebook_path`: /Users/{ユーザー名}/source/{リポジトリ名}/notebooks/spatiotemporal/{番号}_diffusion_transformer_dit_v1.ipynb
  - `topic_title`: Diffusion Transformer (DiT)
  - `chapter_title`: 第{数値}章: Diffusion Transformer (DiT) — U-NetからTransformerへ
  - `difficulty_rating`: ★★★★☆
  - `estimated_minutes`: 150-180
  - `prerequisites`: Notebook {番号} (ViT), {番号}, {番号} (Latent Diffusion)
  - `learning_objectives`: パッチ埋め込み / adaLN-Zero条件付け / DiTスクラッチ実装 / Soraの技術的基盤
  - `key_implementations`: PatchEmbed, AdaLNZero, DiTBlock, DiT (MNIST対応)
  - `cell_count`: 45
  - `libraries`: torch, numpy, matplotlib
  - `section1_title`: U-NetからDiTへの進化の動機
  - `section1_content`: Why DiT? - U-Net limitations, Transformer scaling advantages
  - `section2_title`: PatchEmbed - 画像をトークン列に変換
  - `section2_content`: Patch Embedding for images - dividing images into patches, linear projection. Conv2d with kernel_size=patch_size, stride=patch_size
  - `section3_title`: adaLN-Zero条件付け - タイムステップとクラスの条件付け
  - `section3_content`: AdaLN-Zero conditioning mechanism - how to inject timestep/class info. LayerNorm with learnable scale/shift from condition embedding, plus gate
  - `section4_title`: DiTBlock - Transformer + adaLN-Zero
  - `section4_content`: DiTBlock implementation - self-attention + FFN with adaLN-Zero. Pre-norm Transformer block with adaLN-Zero instead of standard LayerNorm
  - `section5_title`: DiT full model (MNIST向け軽量版)
  - `section5_content`: Full DiT model for MNIST - complete model: PatchEmbed → positional embedding → N × DiTBlock → unpatchify
  - `section6_title`: MNIST訓練・生成デモ
  - `section6_content`: Training on MNIST (28x28 padded to 32x32), simple diffusion with cosine schedule. Short epochs for educational purposes
  - `section7_title`: Soraとの技術的関連
  - `section7_content`: Connection to Sora and modern video generation. How DiT forms the technical foundation for Sora
  - `section8_title`: Summary + common errors + quiz
  - `section8_content`: Summary, common errors (3), 5 quiz questions with details/summary answers
  - `additional_notes`: Use plt.rcParams for figure sizing. Visualizations with proper titles/labels in Japanese. Keep model small for educational purposes (4 layers, dim=128, 4 heads).

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook about Diffusion Transformer (DiT). Follow the exact same JSON format as existing notebooks in this repo (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements from the plan:
- Title: 第{数値}章: Diffusion Transformer (DiT) — U-NetからTransformerへ
- Difficulty: ★★★★☆ | 150-180分
- Prerequisites: Notebook {番号} (ViT), {番号}, {番号} (Latent Diffusion)
- Learning objectives: パッチ埋め込み / adaLN-Zero条件付け / DiTスクラッチ実装 / Soraの技術的基盤
- Implementations: PatchEmbed, AdaLNZero, DiTBlock, DiT (MNIST対応)

Structure (follow NOTEBOOK_GUIDELINES.md):
1. Title + metadata cell (learning objectives, prerequisites, time, difficulty)
2. Table of contents
3. Setup cell (imports, Japanese font, device, seed)
4. Section 1: U-NetからDiTへの進化の動機
5. Section 2: PatchEmbed - 画像をトークン列に変換
6. Section 3: adaLN-Zero条件付け - タイムステップとクラスの条件付け
7. Section 4: DiTBlock - Transformer + adaLN-Zero
8. Section 5: DiT full model (MNIST向け軽量版)
9. Section 6: MNIST訓練・生成デモ (短いepoch数で教育目的)
10. Section 7: Soraとの技術的関連
11. Summary + common errors + quiz (5 questions with details/summary answers)

All markdown in Japanese. Rich comments in code cells. ~45 cells total, ~400 lines of code.
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

### インスタンス 3: GridWorldエージェント

> 元プロンプト: *Write the file {notebook_path}  This is a Japanese educational Jupyter notebook - the Phase 7 CAPSTONE about a grid worl*

**変数の値**
  - `notebook_path`: /Users/{ユーザー名}/source/{リポジトリ名}/notebooks/world-models/{番号}_grid_world_agent_v1.ipynb
  - `topic_title`: Grid World Agent with learned world models
  - `chapter_title`: 第{数値}章: グリッドワールドの知能体 — 学習した世界モデルで計画する (Capstone)
  - `difficulty_rating`: ★★★★★
  - `estimated_minutes`: 300-360
  - `prerequisites`: Notebook {番号}-{番号}全て, {番号} (Training loop), {番号} (Adam)
  - `learning_objectives`: 観測のみからルール学習 / 世界モデル内Planning / 実環境ゼロで迷路解決 / モデル精度と計画成功率の関係 / エンドツーエンドパイプライン
  - `key_implementations`: KeyDoorGridWorld, ObservationEncoder, TransitionModel, RewardModel, ObservationDecoder, ModelPredictiveControl, WorldModelAgent, Q-Learning baseline
  - `cell_count`: 55
  - `libraries`: torch, numpy, matplotlib, tqdm
  - `section1_title`: キャップストーンの目標
  - `section1_content`: Build an agent that learns world rules from observation only. Plan in the learned world model to solve a maze. Compare with model-free Q-learning baseline. End-to-end pipeline diagram.
  - `section2_title`: KeyDoorGridWorld環境
  - `section2_content`: 7x7 grid with: walls (gray), key (yellow), door (blue, locked until key), goal (green). Agent (red) starts at (1,1). Must pick up key → open door → reach goal. Observation: 7x7x3 RGB image. Actions: 0=up, 1=down, 2=left, 3=right. Rewards: -0.1 per step, +1 pick key, +5 goal, -1 hit wall.
  - `section3_title`: データ収集 — ランダム探索
  - `section3_content`: Random agent collects 5000 transitions (s, a, r, s', done). Store as dataset of (obs, action, reward, next_obs, done). Show sample transitions.
  - `section4_title`: ObservationEncoder & Decoder
  - `section4_content`: Encoder: Conv layers → flatten → Linear → 64-dim. Decoder: Linear → unflatten → ConvTranspose → 7x7x3. Train as autoencoder first, show reconstruction quality.
  - `section5_title`: TransitionModel & RewardModel
  - `section5_content`: TransitionModel: MLP (latent_dim + action_onehot → latent_dim). RewardModel: MLP (latent_dim + action_onehot → 1). Train on collected transitions. Show prediction accuracy.
  - `section6_title`: 世界モデルの精度評価
  - `section6_content`: Multi-step rollout in model vs real environment. Compare imagined vs real trajectories. Reconstruction of imagined observations. Model accuracy metrics.
  - `section7_title`: ModelPredictiveControl (MPC)
  - `section7_content`: Random shooting: sample K=50 random action sequences of length H=10. Roll out each in the world model. Pick sequence with highest cumulative reward. Execute first action, replan. MPC class implementation.
  - `section8_title`: WorldModelAgent — 4フェーズ統合
  - `section8_content`: Phase 1: Random exploration. Phase 2: Train world model. Phase 3: Plan with MPC. Phase 4: Execute plan. Iterate phases 1-4 for refinement. Full training loop with progress visualization.
  - `additional_notes`: No gymnasium. All environments are custom pure Python. No downloads. Keep neural networks small but functional. CPU-friendly. This is the most comprehensive notebook - be thorough in implementation.

**実際のプロンプト**
```
Write the file {notebook_path}

This is a Japanese educational Jupyter notebook - the Phase 7 CAPSTONE about a grid world agent using a learned world model. Follow exact JSON notebook format (nbformat 4, nbformat_minor 4, kernelspec Python 3).

Requirements:
- Title: 第{数値}章: グリッドワールドの知能体 — 学習した世界モデルで計画する (Capstone)
- Difficulty: ★★★★★ | 300-360分
- Prerequisites: Notebook {番号}-{番号}全て, {番号} (Training loop), {番号} (Adam)
- Learning objectives: 観測のみからルール学習 / 世界モデル内Planning / 実環境ゼロで迷路解決 / モデル精度と計画成功率の関係 / エンドツーエンドパイプライン

Implementations required:
1. KeyDoorGridWorld: 7x7 grid (walls/key/door/goal), pixel observation 7x7x3 RGB
2. ObservationEncoder: CNN → 64-dim latent
3. TransitionModel: (latent, action) → next latent
4. RewardModel: (latent, action) → reward
5. ObservationDecoder: latent → image reconstruction
6. ModelPredictiveControl: K=50 random shooting paths MPC planning
7. WorldModelAgent: 4-phase integration (explore→learn→plan→execute)
8. Q-Learning baseline comparison

Structure (~55 cells for capstone):
1. Title + metadata
2. Table of contents
3. Setup cell (torch, numpy, matplotlib, tqdm, warnings; Japanese font; device; seed=42)
4. Section 1: キャップストーンの目標
   - Build an agent that learns world rules from observation only
   - Plan in the learned world model to solve a maze
   - Compare with model-free Q-learning baseline
   - End-to-end pipeline diagram
5. Section 2: KeyDoorGridWorld環境
   - 7x7 grid with: walls (gray), key (yellow), door (blue, locked until key), goal (green)
   - Agent (red) starts at (1,1)
   - Must pick up key → open door → reach goal
   - Observation: 7x7x3 RGB image (each cell is one pixel with color)
   - Actions: 0=up, 1=down, 2=left, 3=right
   - Rewards: -0.1 per step, +1 pick key, +5 goal, -1 hit wall
   - render() method returning colored grid
   - Visualize the environment layout
6. Section 3: データ収集 — ランダム探索
   - Random agent collects 5000 transitions (s, a, r, s', done)
   - Store as dataset of (obs, action, reward, next_obs, done)
   - Show sample transitions
7. Section 4: ObservationEncoder & Decoder
   - Encoder: Conv layers → flatten → Linear → 64-dim
   - Decoder: Linear → unflatten → ConvTranspose → 7x7x3
   - Train as autoencoder first, show reconstruction quality
8. Section 5: TransitionModel & RewardModel
   - TransitionModel: MLP (latent_dim + action_onehot → latent_dim)
   - RewardModel: MLP (latent_dim + action_onehot → 1)
   - Train on collected transitions
   - Show prediction accuracy: next-state cosine similarity, reward MSE
9. Section 6: 世界モデルの精度評価
   - Multi-step rollout in model vs real environment
   - Compare imagined vs real trajectories
   - Reconstruction of imagined observations
   - Model accuracy metrics
10. Section 7: ModelPredictiveControl (MPC)
    - Random shooting: sample K=50 random action sequences of length H=10
    - Roll out each in the world model
    - Pick sequence with highest cumulative reward
    - Execute first action, replan
    - MPC class implementation
11. Section 8: WorldModelAgent — 4フェーズ統合
    - Phase 1: Random exploration (collect data)
    - Phase 2: Train world model (encoder, transition, reward, decoder)
    - Phase 3: Plan with MPC in world model
    - Phase 4: Execute plan in real environment
    - Iterate phases 1-4 for refinement
    - Full training loop with progress visualization
12. Section 9: Q-Learningベースライン
    - Simple tabular Q-learning on same environment
    - Train for same number of real environment steps
    - Compare learning curves: WorldModel agent vs Q-Learning
13. Section 10: 比較分析
    - Learning efficiency: episodes to solve maze
    - Sample efficiency: real environment interactions needed
    - Final performance comparison
    - Bar chart + learning curve comparison
    - Model accuracy vs planning success scatter plot
14. Section 11: モデル精度と計画成功率の関係
    - Deliberately degrade model (add noise to transition model)
    - Show planning success rate drops as model accuracy decreases
    - Plot: model MSE vs success rate
15. Summary + common errors (3) + quiz (5 questions)

All markdown in Japanese. Very rich code comments (this is a capstone).
Use torch, numpy, matplotlib, tqdm. No gymnasium.
All environments are custom pure Python. No downloads.
Keep neural networks small but functional. CPU-friendly.
This is the most comprehensive notebook - be thorough in implementation.
```
