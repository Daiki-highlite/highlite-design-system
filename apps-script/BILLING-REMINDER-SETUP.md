
# 請求書リマインダーの設定

月次の請求書送付リマインドを Slack チャンネルに自動投稿する GAS スクリプトのセットアップ手順です。

## 動作概要

| 日付 | 動作 |
|------|------|
| 毎月22日 9:00 (JST) | チャンネル `#all-highlite` にメインリマインドを投稿 |
| 毎月24日 9:00 (JST) | 22日の投稿に返信スレッドで最終リマインドを投稿 |
| 締切 | 毎月27日 |

## セットアップ手順

### 1. Slack Bot トークンを取得

1. [Slack API](https://api.slack.com/apps) にアクセスし、対象の Slack App を開く
2. **OAuth & Permissions** → **Bot Token Scopes** に `chat:write` を追加
3. アプリを Workspace にインストールし、`Bot User OAuth Token`（`xoxb-...`）をコピー

### 2. Script Properties に追加

GAS エディタで **プロジェクトの設定 → スクリプト プロパティ** を開き、以下を追加：

| プロパティ名 | 値 |
|---|---|
| `SLACK_BOT_TOKEN` | `xoxb-xxxx-xxxx-xxxx` |

### 3. タイムゾーンの確認

GAS エディタで **プロジェクトの設定** を開き、タイムゾーンが **(GMT+09:00) 東京（Asia/Tokyo）** になっていることを確認。

### 4. トリガーのインストール（1回だけ実行）

GAS エディタで `setupBillingReminderTrigger` 関数を選択して実行。


### 実行テキスト
投稿するテキストは以下をテンプレートにしてください
MMは適切な月の数値、URLは"こちら"にリンクとしてつけて表示は省略してください。
___
:kotori:請求書送付のご案内　2026年MM月分:nushi:

Highlite協力者、Lapidaristの皆さま、お疲れ様です！

委託対象者の皆さまへ、MM月稼働分の請求書および経費申請についてのリマインドです
Gフォームでの送付をお願いいたします:love:

以下フォームにて請求書をお送りください。
不明点あったらSlackで返信いただいて！
お手数ですが、よろしくお願いします。

:engineko-tsurime:【請求書送付フォームは→こちら（https://docs.google.com/forms/d/e/1FAIpQLSd-j1SlKcpjell6kJH2B-N9SWOBciGgIBG-GnRpN58Pjxu-8w/viewform）】
締切：MM/27まで


## トラブルシューティング

| 症状 | 確認事項 |
|------|---------|
| メッセージが投稿されない | `SLACK_BOT_TOKEN` が正しいか確認 |
| 24日の返信が届かない | `BILLING_REMINDER_TS_{YEAR}_{MONTH}` が Script Properties に存在するか確認 |
| 時間がずれる | スクリプトのタイムゾーンが `Asia/Tokyo` か確認 |
| `not_in_channel` エラー | Bot をチャンネルに招待する（`/invite @BotName`） |
