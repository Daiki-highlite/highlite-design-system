# トレンド記事・マーケ施策 運用フロー

> **作成**: 2026-07-17 | **更新トリガー**: フロー変更時
> 日次トレンドリサーチを基盤に、「記事公開(軸1)」と「トレンド起点のマーケ施策(軸2)」の二軸を回すための運用ドキュメント。

## 全体像

```
【基盤】毎朝7:00 クラウドルーティンが自動実行
  ├─ トレンドリサーチ(Web横断・テーマ自動選定)
  ├─ 内部記事生成 → marketing/articles/YYYY-MM-DD-<slug>.md
  └─ HTML版生成   → marketing/articles/html/YYYY-MM-DD-<slug>.html
       ↓ 蓄積(週7本)
【軸1】週1回: /publish-article        【軸2】週1回(月曜推奨): /trend-digest
  7本から1本厳選 → 公開用リライト        7本を横断分析 → 来ている流れ3つ
  → brandri + LinkedIn で公開            → 施策提案3案 + 今週のアクション1つ
  (受動系・10月以降の販路づくり)          (能動系・今月動く即効薬)
```

## 定常オペレーション

| タイミング | 作業 | 所要 | コマンド |
|---|---|---|---|
| 毎朝(自動) | 記事+HTML生成、branch_yutoへプッシュ | 0分 | (クラウドルーティン) |
| 週1回 | 記事を取り込む: `git pull origin branch_yuto` | 1分 | - |
| 週1回 | 公開記事の選定→リライト→brandri/LinkedIn投稿 | 30分 | `/publish-article` |
| 週1回(月曜推奨) | トレンドダイジェスト+施策提案の生成→レビュー | 20分 | `/trend-digest` |
| 月1回 | 週次ダイジェスト4本を見ながら翌月の施策1〜2本を確定 | セッションで相談 | - |

## ディレクトリ構成

- `marketing/articles/` — 日次内部記事(.md)。「Highliteへの示唆」付き・非公開
- `marketing/articles/html/` — 同HTML版(ブラウザ閲覧用・非公開)
- `marketing/articles/public/` — 公開用リライト版 + LinkedIn投稿文(/publish-articleが生成)
- `marketing/kgi_strategy/weekly-digest/` — 週次トレンドダイジェスト(/trend-digestが生成)

## 管理リンク

- クラウドルーティン管理: https://claude.ai/code/routines/trig_012RpgjXvghG9c91NJNbDwFL
- 記事(GitHub): https://github.com/musickappa/highlite-design-system/tree/branch_yuto/marketing/articles

## 前提条件・ブロッカー

- **t29 robots.txt是正(最優先)**: brandri.jp / highlite.co.jp は全クローラー拒否設定のまま。完了までは公開記事のSEO/AEO効果ゼロ(LinkedIn等からの直リンク流入は有効)。軸1の資産価値を立ち上げるにはt29完了が必須。
- 公開の最終判断は常に人間が行う(自動公開はしない)。
- 内部情報(KGI・クライアント名・社内戦略)は公開版に含めない。
