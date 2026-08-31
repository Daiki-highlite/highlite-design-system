# t29 監査レポート:クローラー / AEO 基盤の実態調査

> **作成**: 2026-07-17 | **調査者**: Claude Code(本番サイトの実データを直接取得して検証)
> **対象タスク**: t29「highlite.co.jp / brandri.jp の robots.txt を是正する(AI・検索クローラーへのアクセス許可)」
> **結論**: t29の前提(「両サイトとも全クローラーを拒否」)は**現状と不一致**。robots.txt・llms.txt・schema・sitemap はすべて実装済みで、AEO基盤は高水準。**t29は事実上完了扱いにすべき**。

---

## 1. 検証サマリー(両サイト横断)

| 項目 | highlite.co.jp | brandri.jp | 判定 |
|---|---|---|---|
| robots.txt クローラー許可 | 全許可(`/wp-admin/`のみ除外) | 全許可(`/design-system.html`のみ除外) | ✅ 開放済み |
| AI bot 個別ブロック(GPTBot/ClaudeBot等) | なし | なし | ✅ 遮断なし |
| X-Robots-Tag HTTPヘッダ | なし | なし | ✅ 問題なし |
| meta robots noindex | なし(`max-image-preview:large`=正の指定) | なし | ✅ 問題なし |
| llms.txt(AEO用) | 設置済み(自動生成) | 設置済み(手作り・高品質) | ✅ あり |
| JSON-LD 構造化データ | 1ブロック・大型@graph | 2ブロック | ✅ あり |
| sitemap.xml | サイトマップインデックス(8サブ) | 512 URL | ✅ 有効 |

**引き継ぎ文書(kgi-handoff-20260711.md §4)の「現状、両サイトとも全クローラーを拒否する設定」は誤り、または7/11以降に解消済み。** 下流タスク(brandri記事公開 t07/t10/t20、SEO/AEO施策全般)は既にブロック解除されている。

---

## 2. サイト別の詳細診断

### highlite.co.jp(WordPress + All in One SEO)

**robots.txt** — WordPress標準。健全。
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Sitemap: https://highlite.co.jp/sitemap.xml
Sitemap: https://highlite.co.jp/sitemap.rss
```

**JSON-LD schema** — ⭐ 非常に強い。単一@graph内に:
- `Organization` + `ProfessionalService`(二重型)。name / legalName / slogan / logo / founder / address(渋谷区150-0045)/ knowsAbout / contactPoint / hasOfferCatalog / sameAs
- `Service` × 10(ブランディングコンサル、VI・ロゴ、Web制作、UI/UX、グラフィック、写真動画、新規事業、マーケ、WS、リサーチ。各々に説明文つき)
- `WebSite` / `WebPage` / `BreadcrumbList`
- → 検索・AIに対してサービス内容と会社実体を明確に提示できている。

**llms.txt** — ⚠️ All in One SEO プラグインの自動生成。投稿・実績の各エントリは良質な説明つきだが、**カテゴリ/タグ/固定ページの約15項目が同じ定型文を繰り返し**ており、LLMにとってはノイズ。実質「第2のサイトマップ」。害はないが最適化されていない。

**sitemap** — サイトマップインデックス(post / page / works / archive / category の8サブ)。健全。

### brandri.jp(静的サイト・ナレッジメディア)

**llms.txt** — ⭐⭐ 手作りで模範的。llms.txt仕様に忠実:
- タイトル + 要約(「経営課題から引けるブランディングのナレッジインフラ」)
- ブランディングの定義、AI時代のエンティティ/可視性への言及
- 主要リソースを説明つきで列挙(用語集337語、AI×ブランディングハブ 等)
- **「運営・専門家(相談先)」= Highlite への導線 + 問い合わせリンク**(エンティティ関係の明示 + CV導線)

**JSON-LD schema** — ⭐ 良好。`WebSite` / `DefinedTerm`(ブランディング)/ `Organization`(Highlite Inc.、sameAs→highlite.co.jp で**サイト間エンティティ連結**)/ `Service` / `ItemList`(Brandri Daily Briefing)。

**sitemap** — 512 URL(用語集337語 + 記事群)。非常に厚いコンテンツ基盤。

---

## 3. 本当の改善余地(「設置済み」≠「最適」)

t29自体は完了水準。ただしAEOをもう一段引き上げるなら以下が効く(いずれも小工数):

| # | 施策 | 対象 | 効果 | 工数 |
|---|---|---|---|---|
| A29-1 | **エンティティ sameAs の拡充** — OrganizationのsameAsが薄い(highliteはX @Shiroitori_lite のみ)。LinkedIn会社ページ・Instagram・Wantedly・Googleビジネスプロフィール等の検証済みプロフィールを追加 | 両サイト | AIのエンティティ同定精度↑(brandri自身が「一貫した実体」の重要性を明言している通り) | 小 |
| A29-2 | **双方向エンティティ連結** — brandri→highlite の連結はあるが、highlite側のschemaにbrandriへの参照がない。highliteのOrganizationに `subjectOf` / 関連サイトとしてbrandriを追加 | highlite | 2サイトのエンティティクラスタを相互補強 | 小 |
| A29-3 | **highlite llms.txt のノイズ削減** — カテゴリ/タグ/固定ページの定型文重複を抑制。ただしAll in One SEOプラグイン生成のため、ファイル直編集ではなくプラグイン設定での制御が必要 | highlite | LLM取り込み時のS/N比↑ | 中 |
| A29-4 | **軸1公開先の確認** — 日次記事(軸1)の公開先が brandri.jp/knowledge.html(既に "Daily Briefing" ItemList schema あり)なら、記事は最適化済み構造に自動で収まる。公開パスを確定 | brandri | 軸1と既存AEO基盤の接続確認 | 小 |

---

## 4. 作業環境に関する注意

- **highlite.co.jp** = WordPress。修正は WordPress管理画面 / テーマファイル / All in One SEO設定 で行う(このリポジトリには含まれない)。
- **brandri.jp** = 512ページの静的サイト。ソースは別リポジトリ/ホストにあると推測(このリポジトリには未収録)。
- → schema/llms.txt の実ファイル修正には、各サイトのホスティング環境へのアクセスが必要。本監査はその前段の「何をどう直すか」の設計図。

---

## 5. タスク台帳への反映(提案)

- **t29 → 完了(Done)**。理由:robots.txt開放・llms.txt・schema・sitemap すべて実装確認済み。前提が既に解消。
- 改善施策 A29-1〜A29-4 は t29の後継として**任意の最適化タスク**に格上げ(優先度は中〜低。ブロッカーではない)。
- これにより Phase 0 のブロッカーは **t30(Crysta 01許可取得)のみ**に絞られる。
