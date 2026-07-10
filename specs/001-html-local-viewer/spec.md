# Feature Specification: Cloudflare Pages による HTML 外部公開

**Feature Branch**: `001-html-cloudflare-deploy`

**Created**: 2026-06-19

**Status**: Draft

**Input**: User description: "kgi-sales-tasks.htmlをCloudflare Pagesで外部公開できる環境を構築する"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 外部URLでHTMLページにアクセスする (Priority: P1)

Yutoまたは共有相手が、Cloudflare Pagesが発行するパブリックURLを開くと、`kgi-sales-tasks.html` が正しくレンダリングされる。

**Why this priority**: 外部公開URLが存在することがこのフィーチャーの本質的な価値。

**Independent Test**: 発行されたCloudflare PagesのURL（例: `https://xxx.pages.dev/marketing/kgi_strategy/kgi-sales-tasks.html`）をブラウザで開き、スタイル・フォント・インタラクションが正しく表示されることを確認できる。

**Acceptance Scenarios**:

1. **Given** Cloudflare Pagesへのデプロイが完了している状態で、**When** 発行されたパブリックURLにアクセスしたとき、**Then** kgi-sales-tasks.html が正しくレンダリングされる
2. **Given** Google Fonts等の外部リソースがある状態で、**When** ページを開いたとき、**Then** フォントが正しく適用されて表示される
3. **Given** スマートフォンやタブレットのブラウザで、**When** パブリックURLにアクセスしたとき、**Then** ページが表示される

---

### User Story 2 - ファイル更新を再デプロイで反映する (Priority: P2)

HTMLファイルを編集した後、再デプロイを実行することで変更内容がパブリックURLに反映される。

**Why this priority**: ファイルを更新するたびに手動で公開できることが、継続的な運用に必要。

**Independent Test**: ファイルを編集し再デプロイコマンドを実行した後、パブリックURLをリロードすると変更内容が表示される。

**Acceptance Scenarios**:

1. **Given** HTMLファイルを編集・保存した状態で、**When** 再デプロイを実行したとき、**Then** 数分以内にパブリックURLに変更が反映される

---

### User Story 3 - デプロイ前にローカルで確認する (Priority: P3)

公開前にローカル環境でページの見た目を確認できる。

**Why this priority**: 本番公開前のミスを防ぐための品質確認ステップ。

**Independent Test**: ローカルプレビューコマンドを実行し、`http://localhost:xxxx` でページが表示される。

**Acceptance Scenarios**:

1. **Given** ローカルプレビューを起動した状態で、**When** ブラウザでローカルURLにアクセスしたとき、**Then** kgi-sales-tasks.html が表示される

---

### Edge Cases

- HTMLファイルが参照する外部リソース（Google Fonts）はインターネット経由で配信されるため、表示には接続が必要
- デプロイ後のキャッシュにより変更反映に数分かかる場合がある
- Cloudflare Pagesのファイルサイズ制限（25MB/ファイル）を超えるファイルは配信できない

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `kgi-sales-tasks.html` がCloudflare Pagesを通じてパブリックURLで閲覧可能でなければならない
- **FR-002**: デプロイはプロジェクトのルートディレクトリから実行できなければならない
- **FR-003**: ファイルを更新した後、再デプロイにより変更がパブリックURLに反映されなければならない
- **FR-004**: HTMLファイル内の外部リソース（Google Fonts）が正しく読み込まれなければならない
- **FR-005**: デプロイ前にローカル環境でプレビューできなければならない

### Key Entities

- **HTMLファイル**: `marketing/kgi_strategy/kgi-sales-tasks.html` — 営業タスク管理画面（静的HTML）
- **Cloudflare Pages プロジェクト**: 静的ファイルをホスティングするデプロイ先
- **パブリックURL**: Cloudflareが発行する `*.pages.dev` ドメインのURL

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: デプロイ完了後、パブリックURLでページが1分以内に表示される
- **SC-002**: ページ内の全スタイル・フォント・インタラクションが意図通りに表示される
- **SC-003**: ファイル更新後の再デプロイで、5分以内にパブリックURLに変更が反映される
- **SC-004**: デプロイ手順が3ステップ以内で完結する

## Assumptions

- Cloudflareアカウントが取得済みである（または新規作成する）
- `kgi-sales-tasks.html` はバックエンド処理を必要としない純粋な静的HTMLである
- デプロイ対象はこのHTMLファイル単体（プロジェクト全体の公開は対象外）
- Google Fonts等の外部リソースはCloudflare CDN経由ではなくGoogle経由で配信される
- アクセス制御（パスワード保護等）は初期スコープ外
