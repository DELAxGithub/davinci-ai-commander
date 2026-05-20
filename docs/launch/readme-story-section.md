# README Story Section / README用ストーリーセクション（英日両対応）

This file provides a copy-pasteable markdown section for the project's root `README.md`. It explains the "Why", "Who", and "Differences" of the project to build empathy and trust with developers and users alike.
本ファイルは、プロジェクトのルートにある `README.md` に追加するためのストーリーセクションです。開発者やエンドユーザーに対して、なぜこのプロジェクトが存在するのか（開発背景）、誰のためなのか、他ツールとの違いは何なのかを説明し、共感と信頼を獲得するための設計になっています。

---

# JAPANESE VERSION (日本語版)

```markdown
## ストーリー：なぜ作ったのか？ (The Story)

### 開発背景 (Why this exists)
動画編集は極めてクリエイティブなプロセスであるべきです。しかし、実際の編集現場では「撮影素材を入れるBin（フォルダー）を毎回同じ構造で手動作成する」「タイムラインに素材を1つずつ配置する」「指示書のメモに沿ってタイムラインにマーカーを打つ」「複数の書き出しプリセットを毎回ポチポチ適用する」といった、退屈で機械的なルーティンワークに多くの時間が奪われています。

「Pythonのスクリプトを組めば自動化できることは知っている。しかし、多忙を極める映像クリエイターにコードを学んだり環境構築をする時間はない。」

この課題を解決するために作られたのが、AIの力で DaVinci Resolve を直接自動操縦する macOS アプリ『[要確定: アプリ名]』です。

### 誰のためのものか？ (Who it is for)
* **プロの映像エディター**: 毎日のルーティンワーク（Bin作成、レンダー設定、タイムライン管理）に疲れ果て、自動化の手段を探している方。
* **技術に興味はあるがコードを書きたくない人**: Python自動化の利便性は享受したいけれど、スクリプト作成や環境構築に時間をかけたくない方。
* **安全で持続可能なツールを求めている人**: 自分のGoogle Gemini APIキーを利用し、サブスクなしの適正な買い切り価格で、業務環境に安全に導入できる自動化ツールを探している方。

### 他のツールとの違い (How it differs)
1. **プログラミング知識は一切不要**: 自然な日本語（または英語）で「A-RollとAudioのBinを作って」と入力するだけで、AIが背後でAPIコードを自動生成して実行します。
2. **完全なるプライバシーとセキュリティ**: APIキーは暗号化され、macOS標準の「Keychain」に保管されます。開発者のサーバーを一切経由しないローカルファースト設計です。
3. **安全設計のバリデーター**: AIが万が一意図しない危険な処理（ローカルファイルの削除など）を生成した場合、実行前にコードを検知して自動ブロックするセーフガードを搭載しています。
4. **月額課金なしの買い切りモデル**: 道具（Tool）は長く愛用できるものであるべきという信念から、サブスクリプションを廃し、「[要確定: 価格] 買い切り」で提供しています。
```

---

# ENGLISH VERSION (英語版)

```markdown
## The Story: Why This Project Exists

### Motivation (Why this exists)
Video editing should be a deeply creative process. However, in the real-world post-production environment, editors spend hours on tedious, mechanical routine tasks: creating identical folder (bin) structures for every shoot, hand-aligning raw footages onto timelines, placing marker flags based on client request spreadsheets, and manually applying multiple render profiles.

"We know Python scripts can automate DaVinci Resolve. But busy creators don’t have the time to learn programming, set up developer environments, or debug API code."

This gap inspired the creation of 『[要確定: アプリ名]』— a lightweight macOS companion app that lets you autopilot DaVinci Resolve using natural language.

### Who is it for?
* **Professional Editors & DITs**: Who want to skip mundane prep and delivery workflows (bin organization, rendering presets, marker batch imports).
* **Non-Coders Seeking Automation**: Who want the power of DaVinci Resolve Python scripting without typing a single line of code.
* **Security & Privacy-Conscious Teams**: Who need a clean, local-first app that runs directly on their Mac using their own API key, without recurring monthly subscription overhead.

### How it Differs from Other Tools
1. **Zero Scripting Required**: Simply type "Create a bin for A-Roll and Music, then append all raw files to a new timeline." The AI translates your request to DaVinci Resolve native API calls instantly.
2. **100% Privacy & Security**: Your Google Gemini API key is securely encrypted inside the macOS Keychain. Zero developer servers in between — your files and data remain strictly local.
3. **Built-in Safe-Guard Validator**: A local code inspector analyzes the AI-generated scripts in real-time, blocking any harmful patterns (like system file deletions) before execution.
4. **Subscription-Free Lifetime Access**: We believe utility tools should be owned, not rented. That is why we chose a transparent "[要確定: 価格] Buy-Once" model over monthly SaaS fees.
```
