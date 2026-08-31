---
doc_id: brandri-slack-app-setup
confidentiality: internal
purpose: Brandri Bot（Slackアプリ）の作成・設置手順
---

# Brandri Bot セットアップ手順

自動処理を、2名の人間とは別人格の「bot」として動かすためのアプリを作る。
これがないと、承認（👍）と自動処理の区別がつかず状態判定が壊れる。

## 1. アプリを作る

1. https://api.slack.com/apps を開く
2. **Create New App** → **From an app manifest**
3. ワークスペース（highlite-brand）を選択
4. `setup/slack-app-manifest.yaml` の中身を貼り付けて **Create**

## 2. ワークスペースにインストール

1. 左メニュー **Install App** → **Install to Workspace** → 許可
2. 表示される **Bot User OAuth Token**（`xoxb-...`）を控える
   - これは秘密情報。GitHub等のコードに直接書かない。
     環境変数 `SLACK_BOT_TOKEN` かリポジトリのSecretに入れる

## 3. チャンネルに招待

`#int-brandri` で以下を実行：

```
/invite @brandri-bot
```

private チャンネルなので、招待しないとbotは投稿もリアクションも読めない。

## 4. bot_user_id を取得して config に入れる

インストール後、以下のいずれかで bot の user ID（`U...`）を確認する：

- api.slack.com → 該当アプリ → **App Home** → Bot User の下に表示される Member ID
- または `auth.test` API をトークン付きで叩く：
  ```bash
  curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    https://slack.com/api/auth.test | python3 -m json.tool
  # → "user_id": "U..." が bot_user_id
  ```

得られた値を `config/brandri-pipeline.config.yaml` の
`slack.bot_user_id` に設定する。

## 5. 動作確認（トークン発行後にこちらで実行可能）

トークンを安全な形で渡してもらえれば、以下の疎通を確認する：
- botとしてテスト投稿 → リアクション付与 → 読み取り → 削除
- 1サイクル分のドライラン（実チャンネルを汚さない形で）

## 補足：なぜ個人アカウント経由ではダメか

現在のSlack連携は古川さん本人（U09N09GM0GK）として動く。
古川さんはレビュアー本人でもあるため、自動処理を本人名義で走らせると：
- botの👍と古川さんの承認👍が区別できない
- 自動修正の返信と古川さんのレビューコメントが同じ名義になり、未処理判定が壊れる

専用botを別人格として立てることで、この2つが構造的に解決する。
