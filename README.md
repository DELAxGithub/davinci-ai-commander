# DaVinci AI Commander

**自然言語でDaVinci Resolveを操作する、プロフェッショナル向け自動化ツール**

<img src="https://img.shields.io/badge/DaVinci_Resolve-19+-blue.svg" alt="DaVinci Resolve 19+"> <img src="https://img.shields.io/badge/Platform-macOS-lightgrey.svg" alt="macOS">

DaVinci AI Commanderは、DaVinci Resolve Scripting APIの力を最大限に引き出し、面倒な「仕込み」「整理」「書き出し」作業をチャット感覚で自動化するMacアプリケーションです。

「ビンを日付ごとに整理して」「すべてのタイムラインをYouTube用プリセットで書き出して」――そんな指示をタイプするだけで、AIがPythonスクリプトを生成し、即座に実行します。

## 主な機能

- **自然言語コントロール**: Google Gemini 1.5 Flash を搭載し、曖昧な指示も正確なAPIコードに変換。
- **安全設計**: 映像の中身やピクセルデータには干渉しない「安全な操作（整理・管理）」に特化。
- **スタンドアロン動作**: 複雑なPython環境構築は不要。配布された `.app` を起動するだけでAPIに接続します。

## ドキュメント

プロの現場で役立つ具体的なユースケースや活用ガイドを用意しました。

- **[プロフェッショナル・オートメーション・ガイド (pro_reference.md)](pro_reference.md)**  
  アシスタントエディター業務を自動化するための運用ガイド。
- **[ユースケース一覧 (use_cases.md)](use_cases.md)**  
  DaVinci Resolve APIで「できること・できないこと」の詳細リスト。

## インストールと起動

1. **DaVinci Resolve を起動する**
   プロジェクトを開いた状態にしてください。

2. **アプリを配置する**
   `dist/DaVinci AI Commander.app` をアプリケーションフォルダなどに移動します。

3. **起動する**
   ダブルクリックして起動します。
   *初回起動時のみ、Google Gemini APIキーの設定が必要です（右下の "Set API Key" ボタン）。*

## 開発者向け情報

### セットアップ

Python 3.10+ 環境が必要です。

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# アプリの起動（開発モード）
./launch_app.sh
```

### ビルド（パッケージング）

PyInstallerを使用して `.app` を生成します。

```bash
./build_app.sh
```

## ライセンス

[MIT License](LICENSE)
