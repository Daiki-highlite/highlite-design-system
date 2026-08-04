# 「Figma株7%下落」から4カ月 ― Claude Design、Reddit"総スカン"からのカムバック劇に見るAI時代の勝ち筋

*Highliteトレンド記事 #020 | 2026-08-05 | テーマ: AIデザイン・AIサイト制作ツール*
*ソース: [Fast Company「Anthropic launches Claude Design, its hyper-intuitive design tool」](https://www.fastcompany.com/91528198/anthropic-claude-design-ai-design-tool) / [Fast Company「Anthropic's updated Claude Design gives vibe coders more control」](https://www.fastcompany.com/91561193/anthropics-updated-claude-design-gives-vibe-coders-and-their-design-overlords-more-control) / [VentureBeat「Anthropic just launched Claude Design...challenges Figma」](https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma) / [VentureBeat「Anthropic ships major Claude Design overhaul」](https://venturebeat.com/technology/anthropic-ships-major-claude-design-overhaul-with-design-system-imports-code-round-trips-and-a-fix-for-its-token-burning-problem) / [TechCrunch「Anthropic launches Claude Design, a new product for creating quick visuals」](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/) / [The Neuron Daily「Anthropic's Claude Design launched, and Reddit has thoughts」](https://www.theneurondaily.com/p/anthropic-s-claude-design-launched-and-reddit-has-thoughts/) / [Startup Stash「Claude Design Just Killed The Mockup. Figma's Stock Dropped 7% in One Day」](https://blog.startupstash.com/claude-design-just-killed-the-mockup-figmas-stock-dropped-7-in-one-day-634394ec6c0e) / [AI Weekly「Claude Design Gains GitHub Import and Claude Code Handoff」](https://aiweekly.co/alerts/claude-design-gains-github-import-and-claude-code-handoff) / [Zenn「Claude Design がclaudeアプリに対応したので触ってみた」](https://zenn.dev/91works/articles/bb03f5adb45dea) / [AIpedia「Claude Designの業務活用10事例」](https://ai-pedia.jp/guides/claude-design-real-examples/) / [週末起業ラボ「Claude DesignでLPを生成してみた」](https://shumatsu-lab.com/claude-design-lp-generation/) + Web横断調査(直近30日中心)*

---

## 結論サマリー(3行)

1. Anthropicが2026年4月17日に投入した「Claude Design」は、発表から24時間でFigma株が7%、Adobe株が2.7%、Wix株が4.7%下落するという異例の市場反応を引き起こした一方、Reddit(r/ClaudeAI)のデザイナーからは「どれも同じ顔」という"総スカン"評価を受けた。
2. その後Anthropicは、GitHub経由で自社デザインシステムを取り込む機能や、Claude Codeへのコード受け渡し(往復編集)、トークン消費過多の修正など、"AIっぽさ"問題への技術的な回答を積み上げてきた。
3. 日本でもLPや提案資料づくりに実利用する事例が増えており、勝敗を分けるのは「素のAI感」を消せるかどうか。中小企業の自作が進むほど、"自社のデザイントークンをAIに食わせる"仕組みを整備できる制作会社の価値が上がる。

---

## 1. 発表当日に株価が動いた「異例」のローンチ

2026年4月17日、AnthropicはClaude Pro/Max/Team/Enterpriseの契約者向けに「Claude Design」を投入した。自然言語の指示だけでスライド・LP・ピッチデック・一枚ページ・モックアップを生成し、PDF・PowerPoint・共有URLで書き出せるほか、Canvaへの引き渡しにも対応する。想定ユーザーはFigmaを日常的に開かない創業者・PM・マーケターで、モデルは長時間の複雑タスクに強いOpus 4.7系。

反応は市場でも即座に表れた。発表から24時間のうちにFigma株は7%、Adobe株は2.7%、Wix株は4.7%それぞれ下落したと報じられている。象徴的なのは、Anthropic CPOのマイク・クリーガー氏がこのローンチに先立ちFigmaの取締役会を退任していたという事実で、"デザインツール市場への正面対決"を印象づけた。一方でCanvaのCEOはローンチ時に連携を歓迎する姿勢を示すなど、業界内の反応は一枚岩ではなかった。

## 2. Redditの反応は「総スカン」―"container soup"問題

しかし現場のデザイナーコミュニティの温度は市場の熱狂とは対照的だった。The Neuron Dailyによれば、r/ClaudeAIでの反応は「resounding meh(完全に微妙)」。批判の核心は「生成されるアプリがどれも同じ顔になる」ことで、同じセリフ体フォント、点滅するステータスドット、カラーのアクセントバー、そして「pillとcardの"container soup(コンテナのごった煮)」といった具体的な指摘が並んだ。ユーザーが参照スクリーンショットや自社のデザイントークンをアップロードしない限り、出力は「Claudeに1回投げただけ感が丸出し」というのが共通見解だった。

これは2026年7月17日の本連載記事(#001)でも触れた「AIデザインは全部同じ顔になる」問題そのものであり、生成AI全般に共通する構造的な課題であることを裏付ける格好の実例となった。

## 3. 半年での正常進化 ― デザインシステム取り込みとコード往復

Anthropicはこの批判に技術的に応答している。2026年6月には、GitHubリポジトリから自社のデザインシステムを丸ごと取り込める機能を追加。ユーザーは公開リポジトリのURLを貼るだけで、Claudeが `design-system-spec.json` を読み込み、コンポーネントをインデックス化し、出力を実在のコンポーネントに自動補正してから提示するようになった。

さらにVentureBeatが報じた大型アップデートでは、デザインシステムのインポート、Claude Codeとのコード往復編集、ドラッグ・リサイズ・整列などの細かい編集コントロール、そしてトークンを消費しすぎる問題への修正、production利用に向けた「数百のバグ修正」が投入された。AI Weeklyはこれを「AIデザインツールが実際の開発ワークフローに定着できなかった理由に応えるもの」と評している。国内のZenn記事でも「Claudeアプリに統合されて触ってみた」という実践レポートが上がり、FigmaでのFix運用とClaude Designの往復ワークフローに手応えを感じる声が紹介されている。

## 4. 日本の現場では実利用が進む ― LP・資料制作のコスト構造

国内でも実利用の記事が急増している。週末起業ラボの実測レポートでは実際にLPを生成して所要時間を検証し、AIpediaはLP・提案資料・社内スライド・管理画面UI・メールHTMLなど10分野の活用例をプロンプト付きで公開している。ある記事では「Claude Pro(月額約3,000円)でこの用途を週1回でも回せれば元は取れる」という損益ラインが示されており、従来デザイナー依頼からワイヤー→デザイン→修正で3〜5日かかっていた工程が、社内担当者のプロンプト作業に置き換わり始めていることを示す。

## Highliteへの示唆

1. **「デザイントークンをAIに食わせる」仕組みを商品化する** ― Claude DesignのGitHub連携型デザインシステム取り込みは、"AIっぽさ"を消す最有力ルート。クライアントの既存ブランド資産をClaude Design対応形式に構造化する"AI設計基盤づくり"は、Web制作の新しい提案メニューになる。
2. **「自作の限界」を可視化する比較コンテンツの好機** ― Reddit発の"container soup"批判は、経営者に「自作AIデザインはどこで頭打ちになるか」を説明する具体的な材料。月額3,000円との比較で"プロの磨き込み"の価値を語れる。
3. **往復編集ワークフローへの追随** ― Claude Codeとのコード往復編集は、Highliteが目指す「AIで下書き+プロが仕上げる」構造そのもの。自社の制作フローに同様の往復ステップを組み込み、クライアントに"仕上がりの差"として提示できる。

---

*余談: Figma取締役会を退任してから約1カ月後に競合製品を出したAnthropic CPOの動きは、シリコンバレー的には珍しくないとはいえ、デザイナーコミュニティでは「筋を通していない」という声も一部で見られた。市場は数字で反応し、現場は使い勝手で判断する ― この温度差そのものが、AIツール選定を任される中小企業の経営者が最も惑わされやすい落とし穴でもある。*
