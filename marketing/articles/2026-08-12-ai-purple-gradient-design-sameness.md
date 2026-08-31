# 「bg-indigo-500、謝罪します」― Tailwind創業者のポスト150万表示が暴いた、AIサイトが"全部同じ顔"になる構造的な理由

*Highliteトレンド記事 #027 | 2026-08-12 | テーマ: Webデザイン最新手法・UI/UXトレンド*
*ソース: [Hacker News「AI Keeps Building the Same Purple Gradient Website」](https://news.ycombinator.com/item?id=46532362) / [Adam Wathan(Tailwind CSS共同創業者)Xポスト](https://x.com/adamwathan/status/1953510802159219096) / [Manish Kumar氏Xポスト](https://x.com/Manixh02/status/2012387306683146646) / [prg.sh「Why Your AI Keeps Building the Same Purple Gradient Website」](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) / [DEV Community「Why Every AI-Built Website Looks the Same (Blame Tailwind's Indigo-500)」](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p) / [blockchain.news「AI Website Builders Hit $6.3B Market but Professionalism Gap Persists」](https://blockchain.news/news/ai-website-builders-market-professionalism-gap-2026) / [Euronews「2025 was the year AI slop went mainstream」](https://euronews.com/next/2025/12/28/2025-was-the-year-ai-slop-went-mainstream-is-the-internet-ready-to-grow-up-now) + Web横断調査(直近30日中心)*

---

## 結論サマリー(3行)

1. AIが作るサイトが「パープルグラデーション+Interフォント+3カード」に収束する現象が、Tailwind CSS創業者Adam Wathan氏の"謝罪"ポスト(150万表示)をきっかけに一気に可視化された。
2. 原因はAIの好みではなく学習データの偏り。Tailwind UIの初期デフォルト色`bg-indigo-500`が大量のチュートリアル・OSS・ブログに拡散し、AIが「Web上で最も多い色=正解」と学習してしまった。
3. 抜け出す鍵は「禁止リスト型プロンプト」。GitHub2.5万スター超のtaste-skillのような"何を使わないか"を指定する手法が急速に支持を集めており、プロと素人を分ける新しい技術になりつつある。

---

## 1. 「これ、全部同じサイトじゃない?」から始まった議論

きっかけはHacker Newsのスレッド「AI Keeps Building the Same Purple Gradient Website」だった。CursorやClaude Code、v0にランディングページを作らせると、判で押したように同じ画面が出てくる ― パープルのグラデーションがかかったヒーローセクション、太字のInterフォントで中央に置かれた見出し、その下に等幅で並ぶ3つのカード(細いラインアイコン+4語のタイトル+一文の説明+「Get Started」ボタン)。

X(旧Twitter)でもManish Kumar氏の投稿が話題になった。「なぜAIが作るサイトは全部同じに見えるのか? パープルグラデーション。Interフォント。3つの箱。角丸。これは"悪いデザイン"じゃない。統計的平均のデザインだ。LLMにセンスはない。学習データのパターンを再現しているだけだ」。この投稿は多くの共感を集め、"AIスロップ(AI slop)"という言葉が2026年のデザイン業界の共通語になった。

## 2. 犯人は「bg-indigo-500」― Tailwind創業者の謝罪ポスト

なぜ「パープル」に収束するのか。その答えを本人が明かして話題になったのが、Tailwind CSS共同創業者Adam Wathan氏のポストだ。「5年前、Tailwind UIのすべてのボタンを`bg-indigo-500`にしたことを正式に謝罪します。それが地球上のすべてのAI生成UIをインディゴ色にした原因です」。このポストは150万表示を記録し、開発者コミュニティで大きな反響を呼んだ。

背景はこうだ。Tailwind CSSはユーティリティCSSフレームワークとして世界的に普及し、無数のチュートリアル・スターターテンプレート・OSSリポジトリがTailwind UIのコンポーネントをそのままコピーして使ってきた。その結果、`bg-indigo-500`のボタンや`from-indigo-500 to-purple-600`のグラデーションが学習データ上で圧倒的多数派になった。生成AIは「Web上で最も頻出するパターン=最も"良い"デザイン」と学習し、指示さえすれば同じ色を返し続ける。しかもAIが生成したサイトが増えるほど、そのサイト自体が次のAIの学習データになり、パープルへの収束がさらに強化される ― という再帰的なループが懸念されている。

## 3. 数字で見る「AIスロップ疲れ」

この現象は単なるネタでは済まない規模になっている。

- AI搭載のウェブサイトビルダー市場は2026年に約63億ドル規模に到達し、前年比26%増と急成長中。一方で調査は「スピードは出せても、素人サイトとプロサイトを分ける戦略的な思考が一貫して欠けている」という"プロフェッショナリズムギャップ"を指摘する。
- ネット上での「AIスロップ」という言葉への言及は2024年から2025年にかけて9倍に増加し、ネガティブな感情を示す投稿の割合は最大54%に達したと報じられている。

日本国内のデザイントレンド解説でも同様の"揺り戻し"が語られている。生成AIで誰でも「それっぽい」ビジュアルを一瞬で作れるようになったからこそ、逆に手描きの揺らぎやアナログなノイズ、物理的な質感を感じさせるデザインに惹かれる層が増えている、という指摘だ。「完璧すぎる」ことが、もはや強みではなく既視感の合図になりつつある。

## 4. 抜け出し方:「禁止リスト」プロンプトとtaste-skill

この問題への実践的な処方箋として注目を集めているのが、"制約を与えるプロンプト"という考え方だ。AIに「いい感じにして」と丸投げするのではなく、「Interは使わない。パープルは使わない。3カードレイアウトは禁止」のように、使わないもの・避けるものを明示的に指定する。AIは実行力は高いがセンス(taste)は持たないため、選択肢を人間側が絞り込んでやる必要がある、という理屈だ。

この考え方を実装したオープンソースツール「taste-skill」(開発者Leon Lin氏、2026年2月公開、MITライセンス)はGitHubで2.5万スターを超える支持を集めている。長期的には、W3Cが2026年1月に「Generative UI Community Group」の設立を提案するなど、AIが実行時にUIを再構成する"生成UI"の標準化に向けた動きも始まっており、業界全体が「AIにどう指示するか」を設計課題として本格的に扱い始めている。

## Highliteへの示唆

1. **「禁止リスト」プロンプトの型化とサービス化** ― taste-skillのような制約ベースの指示は、Highliteが提案時に「なぜAI任せの制作会社と違うのか」を具体的に説明できる技術的な差別化ポイントになる。
2. **「AIスロップ度診断」のようなリード獲得コンテンツ** ― 自社サイトが「パープル+Inter+3カード」の量産型テンプレートに陥っていないかを無料診断するコンテンツは、AI導入済み中小企業(87%)にとって刺さりやすい入口になる。
3. **数字を使った説得材料が増えた** ― 市場63億ドル・前年比26%増でもなお「プロフェッショナリズムギャップ」が指摘されている事実は、「早く作れること」と「選ばれるサイトであること」が別問題だと経営者に伝える際の裏付けとして使える。
