# Launch Story Kit — DaVinci AI Commander

このファイルは Antigravity（デリバリー担当）向けの作業指示書。Claude Code（開発担当）と並行して、リリースに必要なマーケ素材一式を生成する。

**前提**: Launch Story Kit Phase 0-7 の最初の実弾（手作業フルセット試作）。完成したら別プロジェクト用にテンプレ化する。

---

## プロジェクト事実（変更不可）

| 項目 | 内容 |
|---|---|
| プロダクト名 | DaVinci AI Commander |
| 種別 | macOS 単体アプリ（.app / .dmg 配布） |
| 配布チャネル | Gumroad（**App Store ではない**：動的コード実行が審査に通らないため） |
| 価格帯 | **$19–29 買い切り**（Dela が最終確定） |
| 対象プラットフォーム | macOS 11 (Big Sur) 以降 |
| 必須環境 | DaVinci Resolve 19+ / Google Gemini API Key |
| AIモデル | Google Gemini 2.5 Flash |
| ライセンス | MIT |
| 開発元 | DELAX Studio (© 2026) |
| 商標リスク | 「DaVinci」は Blackmagic Design の商標。**アプリ名要再考の可能性あり**（Dela 判断） |

## 主要機能（実装済み）

| カテゴリ | 機能 |
|---|---|
| Bin Management | bin の bulk 作成・削除・リネーム |
| Timeline | timeline 作成、clip append、情報読み取り |
| Markers | マーカー追加・列挙・削除（メモ付き） |
| Metadata | clip metadata・project settings の読み書き |
| Rendering | レンダーキュー投入、プリセット適用、バッチ書き出し |
| Clip Properties | clip color・flag 変更 |

## 出来ないこと（透明性ブロック用）

- 映像コンテンツの編集（カット・トリム・分割）
- エフェクト適用・カラーグレーディング
- 映像/音声の解析
- Resolve UI の直接操作

## 安全設計

- 構造操作のみ（bin / timeline / marker / metadata）
- AI 生成コードを実行前に危険パターン検査
- API Key は macOS Keychain に保管（平文保存なし）
- ユーザー自身の Gemini API key を使う設計（**開発者側にサーバーコスト無し**）

---

## Dela 確定済 (2026-05-20)

| # | 項目 | 確定値 |
|---|---|---|
| 1 | ターゲット 1 文 | **Resolve のルーチン作業に消耗してる映像エディター** (プロ/セミプロ、価格感受容性高め) |
| 2 | 開発動機 | Claude が memory (`user_profile` / `user_indie_dev_interest` / `project_davinci_commander_product` 等) からドラフト → Dela レビュー前提で各ファイルに記述済 |
| 3 | 価格 | **$19** (Gumroad 買い切り、低浮力で初期レビューと広がりを優先) |
| 4 | アプリ名 | **DaVinci AI Commander** を維持 (商標は README 末尾 disclaimer で吸収、SEO ストレートに効かせる) |
| 5 | 透明性ブロック | Claude が memory ベースでドラフト → Dela レビュー前提 (Resolve/macOS update 追従 + 安全設計維持 + 広告/サブスク/データ販売しない宣言) |

**残タスク**: 各ファイルの Phase 1 (開発動機) / Phase 3 (透明性ブロック) を Dela が一度通読、自分の声に近づけるリライト 1 周。それ以外は ready-to-publish 状態。

---

## 作業内容: Launch Story Kit Phase 0-7（骨格テンプレ）

原稿プランナー @takasa_works の note 構造を骨格として転用。長尺 (購入直前の人向け) と短縮版 (認知向け) の **2 バージョン** 用意する。

| Phase | 役割 | DaVinci AI Commander での書き方 |
|---|---|---|
| 0. フック | ターゲット 3 層 + 短縮版リンク | 「自動化を探してる人 / Resolve スクリプティング気になる人 / 買うか迷ってる人」+ 短縮版へのリンク |
| 1. 原体験ストーリー | 既存ツール不満 → 自分の痛み → 気づき | 番組制作の一人法人として毎週繰り返してた Bin/marker/render 作業 → Python 自動化を試みたが Resolve Scripting API + LLM 出力の相性が悪く本末転倒 → AI に API 癖を内蔵させた自分用ツール → 製品化 |
| 2. プロダクト提示 | 名前・価格・課金モデル即提示 | `DaVinci AI Commander` / **$19 買い切り** / Gumroad |
| 3. 透明性ブロック | 「なぜ無料じゃないか」先回り告白 | Gemini API key はユーザー持ち = 開発者側サーバーコスト無し、それでも $19 にする理由 = Resolve/macOS update 追従 + 安全設計維持 + 広告/サブスク/データ販売しない宣言 + 買った人と一緒に育てる関係 |
| 4. 機能ツアー（中核） | 使う順番ナラティブ 0→1→2→3→4→5 | 例: API key 設定 → bin 作成 → timeline 整理 → marker 一括投入 → batch render → 履歴で繰り返す |
| 5. 補助機能 A-E | メイン外の効くやつをアルファベットで | コマンド履歴 (↑↓)、code validation、Keychain 保管、日本語/英語対応 |
| 6. クロージング | 課金モデル再掲 + フィードバック導線 + 作者の祈り | 買い切り再強調 + X & Gumroad コメント + 「良い編集ライフを」 |
| 7. CTA + 続報 + タグ | リンク再掲、続報、SEO タグ | Gumroad URL + 今後の更新予告 + `#DaVinciResolve #PostProduction #VideoEditing` 等 |

## 求める成果物（出力先: このディレクトリ `docs/launch/` 配下）

1. `note-long.md` — note.com 用長文記事ドラフト（Phase 0-7 フル）
2. `note-short.md` — 短縮版（認知向け、Phase 0-3 + 6-7 中心）
3. `x-post.md` — X 告知投稿 3 種（① リリース、② 機能スレッド、③ 1 週後フォロー）
4. `gumroad-product.md` — Gumroad 商品ページ用テキスト（タイトル / サブタイトル / 説明文 / バレットポイント）
5. `screenshot-brief.md` — スクショ 5 枚構成（1=悩み、2-4=解決画面、5=買い切り明示）
6. `readme-story-section.md` — README に追記する Story セクション（なぜ作ったか / 誰のため / 他ツールとの違い）

## ライティングルール

- **言語**: 日本語ベース（note は完全日本語、README Story / Gumroad は英日 2 バージョン推奨）
- **トーン**: インディー開発者の一人称、過剰な煽りなし、誇張なし
- **防御的言い回し**: 「医療助言ではありません」的な防御文言は **内部に閉じる**（feedback_defensive-internal-vs-natural-ui に準拠）
- **5つの再利用要素を必ず盛り込む**:
  1. 二段スキーム（短尺 + 長尺の両方）
  2. 三層ターゲット定義（探してる人 / 気になる人 / 迷ってる人）
  3. 透明性ブロック
  4. 機能ツアー = 使う順番ナラティブ（性能順や重要度順 NG）
  5. 作者の祈り（「良い編集ライフを」みたいな一行）
- **画像穴埋め**: スクショ予定箇所には `[SCREENSHOT: <内容説明>]` で placeholder

## リレールール

- 進捗・完了は `gh issue comment 11 -R DELAxGithub/claude-config` で報告
- 中間生成物はこのディレクトリにファイルとして置く（Claude Code も同じパスを見る）
- `[要確定]` で詰まったら Issue にコメントして Dela に判断を仰ぐ（推測で埋めない）
- commit メッセージは英語、`Co-Authored-By` で Antigravity を明記

## 関連参照

- 親 memory: Launch Story Kit の Phase 0-7 完全版（Claude Code 側のみ）
- お手本: 原稿プランナー note 完全版 https://note.com/takasa_works/n/n2e08cbee6931
- お手本短縮版: https://note.com/takasa_works/n/n4ff021ebcf25
