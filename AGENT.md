# Coding Agent Guidelines for AtCoder Project

このプロジェクトは、AtCoderの問題を解くためのPythonコードを管理するものです。
コーディングエージェントは以下のガイドラインに従って作業してください。

## 1. 応答言語
- **必ず日本語で応答してください。**

## 2. コーディング規約
- **Ruff:** `ruff.toml` の設定に従ってください。
    - 現在の設定: `quote-style = "single"`, `inline-quotes = "single"`, `select = ["Q"]`
    - `ruff.toml` に記載のない項目については、Ruffのデフォルト設定に従ってください。
- **Lint/Formatの実行:**
    - `uv run ruff check .`
    - `uv run ruff format .`

## 3. ツール・実行環境
- **uv:** プロジェクトの依存関係と環境は `uv` で管理されています。
- **実行:** コードの実行は必ず `uv run` を介して行ってください。
    - 例: `uv run python src/atcoder/common/execute.py`

## 4. プロジェクト構成
- `src/atcoder/common/`: 共通ユーティリティや実行スクリプト。
- `src/atcoder/contests/`: 各コンテストごとの回答コード。
    - `intro_heuristics/`: ヒューリスティック問題用のディレクトリ例。
    - `sample_contest/`: サンプルコンテスト用のディレクトリ例。

## 5. 開発フロー
1.  **実装:** 問題に対する回答やユーティリティを記述。
2.  **検証:** `uv run python <file_path>` で動作確認。
3.  **規約チェック:** `uv run ruff check` でコード品質を確認。

## 6. 最新コードの参照
- ユーザーが随時コードを修正する可能性があるため、**コードを更新する前には必ず最新のファイル内容を読み取り、現在の状態を確認してください。**
- 自身の記憶や以前の出力に基づいた、古い情報での上書きを避けてください。
