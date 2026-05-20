# App Store / Gumroad Screenshot Brief / スクショ作成用指示書（5枚構成）

本ファイルは、Gumroadおよび将来的なランディングページ等で使用する「購入意欲を高めるプロダクトスクリーンショット（5枚構成）」のデザイン・レイアウト指示書です。原稿プランナーの「悩み → 解決 → 買い切り明示」の黄金比率を踏襲しています。

---

## 共通デザインシステム（仮定）
* **アスペクト比**: 16:9 (横長)
* **背景**: 視認性の高いダークモード。背後に DaVinci Resolve の編集画面を少しぼかして配置し、手前に『[要確定: アプリ名]』のアプリ画面をシャドウ付きでフローティング配置（グラスモーフィズム風）。
* **フォント**: Outfit または Inter (英語) / Noto Sans JP (日本語)。
* **配色**: Blackmagic Designのブランドカラーである深みのあるブルー/パープルに、GeminiのAI感を表すシアン/マゼンタのグラデーション光彩をアクセントに加える。

---

## 1枚目：悩み（The Pain Point）

* **キャッチコピー（大）**:
  「また右クリックして新規フォルダーを作っていますか？」
  `[ENG] Still manually creating bins and timelines over and over?`
* **サブコピー（小）**:
  Bin作成、タイムライン整理、マーカー配置。動画編集の退屈なルーティン作業をすべて過去のものに。
  `[ENG] Automate the boring, mechanical post-production routine.`
* **画面レイアウト構成**:
  * 背景に、散らかったDaVinci Resolveのメディアプールと、無数に並んだ未整理の素材クリップ。
  * 手前に「手作業による消耗」を象徴する悲哀のあるグラフィック、または「毎日15分の手作業 ＝ 年間90時間の損失」といった警告バナー風の数値グラフィック。

---

## 2枚目：解決画面 1：AIとの接続と自然言語の命令（Command Input）

* **キャッチコピー（大）**:
  「プログラミング不要。日本語で指示するだけ」
  `[ENG] No coding required. Just speak natural language.`
* **サブコピー（小）**:
  AI（Gemini 2.5 Flash）があなたの指示を即座にPythonコードに変換し、Resolveを直接自動操縦。
  `[ENG] Gemini AI instantly translates your text into DaVinci Resolve API commands.`
* **画面レイアウト構成**:
  * アプリのクリーンなUIを中心に配置。
  * プロンプト入力欄に「A-Roll, B-Roll, Audio, SFXのBinを作成して、A-Rollの素材を新しいタイムラインに配置して」とテキストが入力され、まさに「実行(Run)」ボタンがホバー・クリックされている瞬間。
  * コマンド履歴（キーボードの `↑` `↓` マーク）がシンプルに視覚化されている。

---

## 3枚目：解決画面 2：Bin作成とスマートなタイムライン構築（Bulk Organizer）

* **キャッチコピー（大）**:
  「数秒で完了する素材整理とタイムライン構築」
  `[ENG] Bulk organize bins & assemble timelines in seconds.`
* **サブコピー（小）**:
  ワンプロンプトで完璧なBin階層を自動生成。素材の一括配置（Append）まで自動で走り、編集前の下準備をゼロにします。
  `[ENG] Build nested folder structures and auto-append footage to save hours of prep work.`
* **画面レイアウト構成**:
  * 画面左側にアプリの指示画面、右側に実際にDaVinci Resolveのメディアプール内に一瞬で生成された「A-Roll」「B-Roll」「Audio」といった美しいBin構造と、タイムライン上にきれいに一列に並んだクリップ群をスプリット画面で対比。
  * 「Bin生成完了！」「タイムライン作成完了！」のトースト通知が美しく浮き上がっている。

---

## 4枚目：解決画面 3：マーカー自動配置とバッチ書き出し（Intelligent Render）

* **キャッチコピー（大）**:
  「マーカーの bulk 投入と複数プリセットの一括レンダリング」
  `[ENG] Drop precision markers & enqueue batch rendering.`
* **サブコピー（小）**:
  指示書に沿った位置にメモ付きマーカーを自動配置。YouTubeとProResの同時バッチレンダー登録も瞬時に実行。
  `[ENG] Auto-place color-coded markers with notes. Send multiple export presets to Render Queue instantly.`
* **画面レイアウト構成**:
  * 背景に、DaVinci Resolveの「デリバー(Deliver)ページ」と、レンダーキューに複数自動追加されたジョブリスト。
  * 手前に、タイムライン上に美しく等間隔で配置されたカラーマーカーのクローズアップ画像。

---

## 5枚目：買い切りの明示と安全設計（Buy Once & Secure）

* **キャッチコピー（大）**:
  「月額サブスクなし。[要確定: 価格] 買い切りライセンス」
  `[ENG] [要確定: 価格] One-Time Purchase. No Monthly Subscriptions.`
* **サブコピー（小）**:
  APIキーはmacOS Keychainで安全に保護。危険なAIコードを弾くバリデーション機能を備えたセーフティ設計。
  `[ENG] Pure indie product. API key secured via Apple Keychain with built-in code validation safeguards.`
* **画面レイアウト構成**:
  * アプリの「APIキー設定画面」と、macOS Keychainの安全な盾のアイコンを融合した3Dグラフィック。
  * 「[要確定: 価格] 買い切り（Lifetime Access）」と大きく目立つバッジを中央右に配置し、Gumroadでの決済手段（クレジットカード、PayPal、Apple Pay対応ロゴ）を美しく並べる。
