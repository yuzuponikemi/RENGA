---
name: LangGraphアーキテクチャ設計レビュー
skill_id: d8fa2e3c-8118-47eb-ac76-7a91cf645308
version: 1.0.0
category: アーキテクチャ設計レビュー
status: public
source_count: 5
unique_user_count: 3
variables:
- framework
- state_management
- data_format
- components
- current_issues
- future_expansion
- traceability_requirements
- design_philosophy
- review_focus
triggers:
- アーキテクチャ設計をレビューして
- LangGraphの設計が適切か確認して
- 状態管理の設計を改善して
- コンポーネント間の連携を見直して
- この設計どう思う？
---

# LangGraphアーキテクチャ設計レビュー

**説明**: LangGraphの状態管理と連携設計をレビュー・改善するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 5 件 | **ユニークユーザー**: 3 人 | **カテゴリ**: アーキテクチャ設計レビュー

---

## テンプレートプロンプト

```
以下のアーキテクチャ設計についてレビュー・改善提案を行ってください。

【現在の設計】
- 使用フレームワーク: {framework}
- 状態管理方式: {state_management}
- データ連携形式: {data_format}
- コンポーネント構成: {components}
- 現在の課題: {current_issues}

【目指すべき方向性】
- 将来的な拡張性: {future_expansion}
- トレーサビリティ要件: {traceability_requirements}
- 優先する設計思想: {design_philosophy}

上記を踏まえ、{review_focus}の観点から具体的な改善案を提示してください。
```

## 変数一覧

- `{{framework}}`: 使用しているフレームワーク名（例: LangGraph, LangChain）
- `{{state_management}}`: 現在の状態管理方式（例: LangGraphのState, 独自管理）
- `{{data_format}}`: コンポーネント間のデータ連携形式（例: JSON, オブジェクト参照）
- `{{components}}`: システムを構成する主要コンポーネント（例: モジュールA, モジュールB）
- `{{current_issues}}`: 現在直面している課題（例: 連携の喪失, トレース困難）
- `{{future_expansion}}`: 将来的に想定する拡張（例: 特定機能の追加, グラフ再構築）
- `{{traceability_requirements}}`: トレーサビリティに関する要件（例: 全体の流れの可視化）
- `{{design_philosophy}}`: 優先する設計思想（例: 拡張性重視, 保守性重視）
- `{{review_focus}}`: レビューの焦点（例: アーキテクチャ全体, 状態管理方式）

## 活用シーン

- リファクタリング後のアーキテクチャ整合性チェック
- 特定フレームワーク導入前の設計レビュー
- サービス分割後の連携設計見直し

## トリガーフレーズ

- `アーキテクチャ設計をレビューして`
- `LangGraphの設計が適切か確認して`
- `状態管理の設計を改善して`
- `コンポーネント間の連携を見直して`
- `この設計どう思う？`

---

## 具体インスタンス

### インスタンス 1: リファクタリング後連携喪失問題

> 元プロンプト: *今回リファクタリングしたけど、その結果サービスとして分割が進んだ、それはいいけど、逆にlanggraphとしての連携を失ってしまった？？*

**変数の値**
  - `framework`: LangGraph
  - `state_management`: 独自のJSONベース管理
  - `data_format`: JSON
  - `components`: サービス分割された複数モジュール
  - `current_issues`: リファクタリングによりサービス分割が進んだが、{framework}としての連携を失った
  - `future_expansion`: 特定コンポーネント作成後のreflection、グラフの再構築
  - `traceability_requirements`: 全体の流れのトレースのしやすさ
  - `design_philosophy`: 拡張性とトレーサビリティの両立
  - `review_focus`: アーキテクチャ全体

**実際のプロンプト**
```
以下のアーキテクチャ設計についてレビュー・改善提案を行ってください。

【現在の設計】
- 使用フレームワーク: {framework}
- 状態管理方式: 独自のJSONベース管理
- データ連携形式: JSON
- コンポーネント構成: サービス分割された複数モジュール
- 現在の課題: リファクタリングによりサービス分割が進んだが、{framework}としての連携を失った

【目指すべき方向性】
- 将来的な拡張性: 特定コンポーネント作成後のreflection、グラフの再構築
- トレーサビリティ要件: 全体の流れのトレースのしやすさ
- 優先する設計思想: 拡張性とトレーサビリティの両立

上記を踏まえ、アーキテクチャ全体の観点から具体的な改善案を提示してください。
```

---

### インスタンス 2: LangGraph化リライト指示

> 元プロンプト: *ではlanggraph化する方向で書き直してください*

**変数の値**
  - `framework`: LangGraph
  - `state_management`: 未定義
  - `data_format`: 未定義
  - `components`: 未定義
  - `current_issues`: {framework}を導入したいが現状の設計が不明
  - `future_expansion`: 将来的な機能追加や変更に柔軟に対応できること
  - `traceability_requirements`: 処理フローの可視化と追跡が容易であること
  - `design_philosophy`: {framework}の特性を活かした設計
  - `review_focus`: {framework}化する方向での書き直し

**実際のプロンプト**
```
以下のアーキテクチャ設計についてレビュー・改善提案を行ってください。

【現在の設計】
- 使用フレームワーク: 未導入
- 状態管理方式: 未定義
- データ連携形式: 未定義
- コンポーネント構成: 未定義
- 現在の課題: {framework}を導入したいが現状の設計が不明

【目指すべき方向性】
- 将来的な拡張性: 将来的な機能追加や変更に柔軟に対応できること
- トレーサビリティ要件: 処理フローの可視化と追跡が容易であること
- 優先する設計思想: {framework}の特性を活かした設計

上記を踏まえ、{framework}化する方向で書き直すための具体的な設計案を提示してください。
```

---

### インスタンス 3: Reflectionワークフロー設計

> 元プロンプト: *ブラウザで見えました　もう少し複雑な例で、どういうふうに記録がなされるのかみてみたいです　langgraphを使った、非常にシンプルなreflectionのワークフローを作成し、哲学的な問いに対して実際の実験プランを考えてみるような目的でプ*

**変数の値**
  - `framework`: LangGraph
  - `state_management`: {framework}のState
  - `data_format`: オブジェクト参照
  - `components`: シンプルなreflectionワークフロー
  - `current_issues`: 特定の問いに対して実験プランを考える目的での設計
  - `future_expansion`: 複雑なreflectionパターンへの拡張
  - `traceability_requirements`: 各ステップの記録と可視化
  - `design_philosophy`: シンプルさと拡張性のバランス
  - `review_focus`: 非常にシンプルなreflectionワークフローの設計

**実際のプロンプト**
```
以下のアーキテクチャ設計についてレビュー・改善提案を行ってください。

【現在の設計】
- 使用フレームワーク: {framework}
- 状態管理方式: {framework}のState
- データ連携形式: オブジェクト参照
- コンポーネント構成: シンプルなreflectionワークフロー
- 現在の課題: 特定の問いに対して実験プランを考える目的での設計

【目指すべき方向性】
- 将来的な拡張性: 複雑なreflectionパターンへの拡張
- トレーサビリティ要件: 各ステップの記録と可視化
- 優先する設計思想: シンプルさと拡張性のバランス

上記を踏まえ、非常にシンプルなreflectionワークフローを設計し、具体的な記録のされ方も含めて提示してください。
```
