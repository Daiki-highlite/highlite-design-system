# 「通報1件で"いいね468件"消滅」は誤解だった ― Xがアルゴリズムを丸ごと公開し、"シャドウバン"を初めて公式に認めた8月

*Highliteトレンド記事 #037 | 2026-08-24 | テーマ: 中小企業の集客・SNSマーケティング*
*ソース: [TechCrunch「X open sources its ranking algorithm, letting users see if they've been 'shadowbanned'」](https://techcrunch.com/2026/08/13/x-open-sources-its-ranking-algorithm-letting-users-see-if-theyve-been-shadowbanned/) / [GitHub「xai-org/x-algorithm」](https://github.com/xai-org/x-algorithm) / [explainx.ai「X Discloses Ranking Weights: A Report Costs 468 Likes」](https://explainx.ai/blog/x-algorithm-for-you-timeline-open-source-ranking-weights-august-2026) / [Blockchain.News「X Algorithm Update Clarifies Ranking Weights」](https://blockchain.news/ainews/x-algorithm-update-clarifies-ranking-weights) / [TechRound「X Just Open-Sourced Its Algorithm And Added A Shadowban Checker – Real Transparency Or PR Theatre?」](https://techround.co.uk/business/x-just-open-sourced-its-algorithm-and-added-a-shadowban-checker-real-transparency-or-pr-theatre/) / [カチプロ「【2026年8月最新版】Xアルゴリズムの変更点とは?公開コードと具体的な運用方法を解説」](https://pro-marketing.jp/sns-marketing/x/x-algorithm-202608/) / [neworder inc.「【2026年8月更新】Xのおすすめアルゴリズムとは?企業投稿は『目的・対象・内容・反応』で設計する」](https://www.neworder.co.jp/2026/08/20/x-for-you-algorithm-2026/) / [Cryptul Insights「Xのアルゴリズムを徹底解析|xAIが公開した『For You』推薦システムのコードを読み解く」](https://cryptul.co.jp/insights/articles/154-x-algorithm-analysis) + Web横断調査(直近30日中心)*

---

## 結論サマリー(3行)

1. 2026年8月13日、Xは「For You(おすすめ)」タイムラインを動かすアルゴリズムのコードをGitHub(xai-org/x-algorithm)で大幅拡充公開した(Apache v2ライセンス、コード規模は従来の約10〜15倍)。返信・いいね・通報など行動ごとの重み(例:通報は-234点)まで開示し、"シャドウバン"の存在を実質的に公式が初めて認める格好になった。
2. ところが翌14日、X自身が「通報1件がいいね468件分を帳消しにする」という広まった解釈は誤りだと訂正した。重みは"実際の行動回数"ではなく"予測確率"に掛け合わされる値であり、単純な倍率換算はできないという説明だ。数字が独り歩きするスピードの速さも同時に露呈した。
3. 同時導入された"シャドウバン確認"機能「Under the Hood」は、アカウント開設1年以上・月10投稿以上という条件付きの試験提供で、しかも出力は月次集計のJSONファイル。使い勝手の悪さから海外メディアには早くも「PR芝居ではないか」との声も出ている。中小企業のX運用担当者が今押さえるべきは、公開された数字そのものより「一貫したテーマ発信」という運用原則の再確認だ。

---

## 1. Xが自ら"ブラックボックス"のふたを開けた

2026年8月13日、XはFor Youタイムラインを動かす推薦アルゴリズムのコードをGitHub(xai-org/x-algorithm)で公開した。以前から一部コードは公開されていたが、今回は候補投稿の取得(Phoenix Retrieval)、コミュニティクラスタリング(SimClusters)、ランキング、フィルタリングまでを含む大幅拡張版で、コードベースは従来の約10〜15倍に膨らんだ。VP of ProductのKeith Coleman氏は「Xアルゴリズムのかつてない水準の透明性」と説明している。

公開されたコードには、返信(+5〜+20点)、いいね(+0.5点)、通報(-234点)など、行動ごとにモデルが予測した確率へ掛け合わされる「重み」も含まれていた。長年ユーザーの間で噂されてきた「シャドウバン」についても、投稿を非フォロワーのおすすめ表示から除外する"SPAM_HIGH_RECALL"などのラベルの存在がコードから確認でき、Xが公式に"見えない制限"の仕組みを認めた形になった。

## 2. 「通報1件=いいね468件」はなぜ誤解だったのか

数字が公開されるとすぐに、「通報の重み-234はいいね(+0.5)の468倍だから、1通報で468いいね分が帳消しになる」という解釈がSNS上で急速に広まった。しかし翌8月14日、Xはこの解釈を明確に否定する説明を追記した。重みは実際に発生した行動の"回数"にかかるのではなく、モデルが予測した"行動確率"に掛け合わされる値であり、単純な倍率換算はできないというのがXの立場だ。

この一件は、アルゴリズムの数字が公開されたからといって、それを"正しく読む"難易度が下がるわけではないことを示している。むしろ数字が独り歩きする速さは、運用担当者が一次情報の訂正まで追いかける必要性を裏付けた。

## 3. "シャドウバン確認"は本物の透明性か

同時に試験提供が始まった「Under the Hood」は、設定画面から自分のアカウントや投稿に制限ラベルが付いていたかを月次で確認できる機能だ。ただし対象はアカウント開設1年以上・過去1カ月に10投稿以上という条件付きで、出力は特定の投稿ではなく1カ月分集計のJSONファイル。「なぜ先週のあの投稿が伸びなかったのか」には答えてくれない。この使い勝手の悪さから、海外メディアTechRoundは「本物の説明責任というより"PR芝居"ではないか」と評した。広告システムや、Xが"悪用され得る"と判断した情報は今回も非公開のままだ。

## 4. Highliteへの示唆

1. **「テーマの一貫性」を顧客への提案軸にする** — 日本語解説記事群が共通して指摘するのは、SimClusters(約14.5万のコミュニティ分類)によってアカウントの発信テーマが機械的に判定されるという点。話題がバラバラなアカウントは的確なクラスターに紐付かずリーチが伸びにくい。Highliteが中小企業のSNS運用を支援する際、「投稿カレンダーをテーマ軸で統一する」ことの重要性を、今回のアルゴリズム公開という一次情報で裏付けて説明できる。
2. **"数字の独り歩き"への警戒を顧客教育コンテンツに** — 「通報468倍」の誤解が一日で広まった一件は、SNS上の"バズった解釈"を鵜呑みにする危うさの好例。顧客企業向けに「アルゴリズム系の噂は一次ソースで裏取りしてから運用を変える」という基本姿勢を伝えるコンテンツの題材になる。
3. **プラットフォームの"透明性ごっこ"を見極める視点を持つ** — Under the Hoodのように、話題性はあっても実務的な使い勝手が伴わない機能は今後も各SNSで増える見込み。Highlite自身が新機能に安易に飛びつかず、「実際に中小企業の運用改善につながるか」を検証してから顧客に推奨する姿勢が、他の制作会社との差別化になる。
