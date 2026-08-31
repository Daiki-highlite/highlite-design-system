# 「作れるが、保てない」― バイブコーディング製アプリ5,600件調査で58%に重大脆弱性、"速さ"だけで選ぶ時代の終わり

*Highliteトレンド記事 #026 | 2026-08-11 | テーマ: Web制作業界・フリーランス/制作会社の動向*
*ソース: [VentureBeat「5,000 vibe-coded apps just proved shadow AI is the new S3 bucket crisis」](https://venturebeat.com/security/vibe-coded-apps-shadow-ai-s3-bucket-crisis-ciso-audit-framework) / [Escape.tech「The State of Security of Vibe Coded Apps」](https://escape.tech/state-of-security-of-vibe-coded-apps) / [Escape.tech「Methodology: 2k+ Vulnerabilities in Vibe-Coded Apps」](https://escape.tech/blog/methodology-how-we-discovered-vulnerabilities-apps-built-with-vibe-coding/) / [GitGuardian「The State of Secrets Sprawl 2026」](https://www.gitguardian.com/state-of-secrets-sprawl-report-2026) / [GitGuardian Blog「AI-Service Leaks Surge 81% and 29M Secrets Hit Public GitHub」](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) / [The Hacker News「The State of Secrets Sprawl 2026: 9 Takeaways for CISOs」](https://thehackernews.com/2026/03/the-state-of-secrets-sprawl-2026-9.html) / [Stack Overflow「2025 Developer Survey Reveals Trust in AI at an All Time Low」](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/) / [Stack Overflow Blog「Developers remain willing but reluctant to use AI」](https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/) / [Cloud Security Alliance「Vibe Coding's Security Debt: The AI-Generated CVE Surge」](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-vulnerability-surge-2026/) / [SaaStr「We've Built 12+ Vibe Coded Apps Used 800,000+ Times. I Love It, But I Still Have to Maintain Them Every Single Day」](https://www.saastr.com/weve-built-12-vibe-coded-apps-used-800000-times-i-love-it-but-i-still-have-to-maintain-them-every-single-day/) / [Hacker News「How vibe coding is killing open source」](https://news.ycombinator.com/item?id=46876455) / [TechTarget「Research shows the vibe coding security crisis CIOs can't ignore」](https://www.techtarget.com/searchcio/feature/vibe-coding-security-crisis-CIOs-cant-ignore) + Web横断調査(直近30日中心)*

---

## 結論サマリー(3行)

1. セキュリティ企業Escape.techが公開中のAI生成(バイブコーディング)アプリ5,600件を調査したところ、58%に何らかのセキュリティ問題、2,000件超の重大脆弱性、400件超のシークレット流出、175件の個人情報露出(医療記録・銀行口座情報を含む)が確認された。RedAccessは同種の公開資産38万件のうち約5,000件に企業の機微データが含まれると報告している。
2. GitGuardianの年次調査では、2025年に公開GitHubへ新規流出したシークレットが2,865万件(前年比34%増)に達し、AIがコミットに関与した場合の漏洩率はベースラインの約2倍。Stack Overflow調査でも開発者のAI利用率は84%まで伸びた一方、「AIの出力を信頼する」は40%→29%へ低下し、"使うほど信じない"という逆転現象が起きている。
3. SaaStr創業者が「80万回以上使われた12本のアプリを作ったが、今も毎日メンテナンスしている」と告白するなど、現場の実感としても「作れるが、保てない」という壁が可視化されつつある。Webサイトや業務アプリを外注する中小企業にとって、"速さ"だけでツールやパートナーを選ぶリスクが増している。

---

## 1. 「作れることの価値」から「保てることの価値」へ

Lovable、Bolt、v0、Replit、Cursorといった自然言語指示だけでアプリを生成する"バイブコーディング"は、この1〜2年で非エンジニアの手にも渡った。個人開発者が週末でSaaSを立ち上げ、中小企業の担当者が業務ツールを内製する光景は珍しくなくなった。しかし2026年に入り、話題の中心は「作れるかどうか」から「本番運用に耐えられるかどうか」へと明確に移った。データが示すのは、量産されたアプリの多くが公開直後から無防備な状態に置かれているという現実だ。

## 2. データが暴いた実態:5,600アプリ調査と"シークレット2倍漏洩"

セキュリティ企業Escape.techは、公開されているバイブコーディング製アプリ5,600件をスキャンし、2,000件超の重大な脆弱性、400件超の露出したAPIキー・アクセストークン、175件の個人情報露出(医療記録や銀行口座番号を含む)を発見した。発見された脆弱性はいずれも稼働中の本番システムに存在し、数時間以内に発見可能な状態だったという。別の調査会社RedAccessも、同種プラットフォーム経由で公開されている資産38万件のうち約5,000件に企業の機微データが含まれると報告している。

GitGuardianの年次レポート「State of Secrets Sprawl 2026」(2026年3月17日発表)は、より広い母集団でこの傾向を裏付ける。2025年に公開GitHubへ新規流出したハードコードされたシークレットは2,865万件で前年比34%増、単年として過去最大の増加幅を記録した。特にAIがコミットに関与した場合の漏洩率は全体平均のおよそ2倍に達しており、AI活用が「速さ」と引き換えに「漏洩リスク」を積み増している構図が数字として現れている。

## 3. 開発者自身も「使うほど、信じていない」

興味深いのは、AIコード生成を最も使い込んでいる開発者自身が、その出力を最も信用していないという逆説だ。Stack Overflowの「2025年度Developer Survey」によれば、AIツールを利用する開発者の割合は84%(前年76%)まで拡大した一方、「AIの出力が正確だと信頼する」割合は前年の40%から29%へ低下。「AIの出力を積極的に信頼しない」開発者(46%)が「信頼する」(33%)を上回った。Cloud Security Allianceの調査ノートも、AI生成コードに起因するCVE登録件数が2026年1月の6件から2月15件、3月35件へと急増していることを指摘しており、「使われるほど点検対象が増える」局面に入っている。

## 4. 現場の本音:「毎日メンテナンスしている」

この温度感は、バイブコーディングの伝道者的存在からも聞こえてくる。SaaS業界カンファレンス「SaaStr」創業者のJason Lemkin氏は、自身のブログで「私たちは12本以上のアプリをバイブコーディングで作り、合計80万回以上使われている。とても気に入っているが、今も毎日メンテナンスをしている」と明かした。Hacker Newsでも「バイブコーディングがオープンソースを蝕んでいる」といったスレッドが継続的に立ち、"作った後"の運用負担が開発者コミュニティ共通の悩みとして語られている。「プロトタイプはAIで一瞬。しかし本番でユーザーを抱えた瞬間から、保守は人間の仕事に戻る」というのが現場の共通認識になりつつある。

## 5. 日本の中小企業が陥りやすい罠

日本国内でも、ノーコード・AI制作ツールによる自社サイトやLPの内製化は着実に広がっている。コスト削減や意思決定の速さという利点は本物だが、上記の調査結果は「誰がセキュリティとメンテナンスの責任を持つか」を決めずに公開してしまうリスクを裏付けている。フォーム経由の個人情報や決済情報を扱うサイトほど、露出したシークレットや脆弱性がそのまま経営リスクに直結する。TechTargetもCISO向けに「バイブコーディングのセキュリティ危機はもはや無視できない経営課題」だと警鐘を鳴らしており、専任のセキュリティ担当者を置けない中小企業にこそ重くのしかかる問題だ。

## Highliteへの示唆

1. **「作って終わり」ではなく運用保守込みの提案を明示する** ― データが示す通り、価値の重心は「初速」から「保守できるか」へ移っている。公開後のセキュリティチェック・アップデート体制をパッケージに組み込み、言語化して伝える価値が高まっている。
2. **AI活用の"見える化"を差別化の武器にする** ― どの工程をAIで生成し、どこを人間がレビューしたかを提案時に明示することで、「速いが危ういAI任せ」との違いを客観的に示せる。セキュリティチェック工程自体をセールスポイントにできる。
3. **"自作したいが不安"な層への教育コンテンツの好機** ― バイブコーディングの認知が広がるほど、「自社で作るか、プロに任せるか」で迷う中小企業の経営者・担当者は増える。今回のような具体的な脆弱性データは、比較検討コンテンツやセミナー資料の材料として説得力を持つ。
