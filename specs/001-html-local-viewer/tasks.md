# Tasks: Cloudflare Pages HTML 外部公開

**Input**: Design documents from `specs/001-html-local-viewer/`

**Prerequisites**: plan.md ✅ / spec.md ✅ / research.md ✅ / quickstart.md ✅

**Organization**: タスクはユーザーストーリー単位で整理されています。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並行実行可能（異なるファイル、依存なし）
- **[Story]**: 対応するユーザーストーリー（US1/US2/US3）

---

## Phase 1: Setup（環境準備）

**Purpose**: ツールのインストールと基本環境の確認

- [x] T001 Node.js がインストールされていることを確認する（`node -v` を実行）
- [x] T002 Wrangler CLI をインストールする（`npm install -g wrangler`）

**Checkpoint**: `wrangler --version` でバージョンが表示されれば完了

---

## Phase 2: Foundational（ブロッキング前提条件）

**Purpose**: デプロイに必須の認証とディレクトリ構造の準備

**⚠️ CRITICAL**: このフェーズが完了するまで、どのユーザーストーリーの作業も開始できない

- [x] T003 Cloudflare アカウントで認証する（`wrangler login`）
- [x] T004 プロジェクトルートに `deploy/` ディレクトリを作成する

**Checkpoint**: `deploy/` ディレクトリが存在し、`wrangler whoami` でアカウントが表示されれば完了

---

## Phase 3: User Story 1 - 外部URLでHTMLページにアクセスする（Priority: P1）🎯 MVP

**Goal**: `kgi-sales-tasks.html` がパブリックURLでブラウザから閲覧できる状態にする

**Independent Test**: 発行された `*.pages.dev` URLをブラウザで開き、サイドバー・スタイル・フォントが正しく表示される

### Implementation for User Story 1

- [x] T005 [US1] `marketing/kgi_strategy/kgi-sales-tasks.html` を `deploy/index.html` としてコピーする
- [x] T006 [US1] Cloudflare Pages プロジェクトを作成して初回デプロイを実行する（`wrangler pages deploy deploy/ --project-name highlite-sales-tasks`）
- [x] T007 [US1] 発行されたパブリックURL（`*.pages.dev`）をブラウザで開き、表示を確認する
- [x] T008 [US1] ページ内の全要素（サイドバー・カード・Noto Sans JPフォント）が正しくレンダリングされていることを確認する

**Checkpoint**: パブリックURLで `kgi-sales-tasks.html` が完全に表示されれば User Story 1 完了（MVP達成）

---

## Phase 4: User Story 2 - ファイル更新を再デプロイで反映する（Priority: P2）

**Goal**: HTMLファイルを編集した後、再デプロイで変更がパブリックURLに反映される仕組みを確立する

**Independent Test**: HTMLファイルに変更を加えて再デプロイし、5分以内にパブリックURLに変更が反映されることを確認する

### Implementation for User Story 2

- [ ] T009 [US2] `kgi-sales-tasks.html` にテスト用の変更を加える（例: タイトルテキストを一時変更）
- [ ] T010 [US2] 変更したファイルを `deploy/index.html` に上書きコピーする
- [ ] T011 [US2] 再デプロイを実行する（`wrangler pages deploy deploy/ --project-name highlite-sales-tasks`）
- [ ] T012 [US2] パブリックURLをリロードして変更が反映されていることを確認する（キャッシュクリアが必要な場合あり）
- [ ] T013 [US2] テスト用変更を元に戻して再デプロイし、最終状態に戻す

**Checkpoint**: 編集→コピー→デプロイの3ステップで変更が反映されれば User Story 2 完了

---

## Phase 5: User Story 3 - デプロイ前にローカルで確認する（Priority: P3）

**Goal**: 公開前にローカルブラウザでプレビューできる状態を作る

**Independent Test**: `wrangler pages dev deploy/` を実行し、`localhost` のURLでページが表示される

### Implementation for User Story 3

- [ ] T014 [US3] ローカルプレビューを起動する（`wrangler pages dev deploy/`）
- [ ] T015 [US3] ブラウザで `http://localhost:8788`（または表示されたURL）にアクセスしてページが表示されることを確認する
- [ ] T016 [US3] ローカルプレビューの表示とパブリックURLの表示が一致することを確認する

**Checkpoint**: `wrangler pages dev` コマンドでローカルプレビューが動作すれば User Story 3 完了

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 継続的な運用のための整備

- [x] T017 [P] `deploy/` ディレクトリを `.gitignore` に追加する（自動生成ファイルのため）
- [ ] T018 `specs/001-html-local-viewer/quickstart.md` の手順を実際の操作結果と照合して更新する
- [ ] T019 [P] 発行されたパブリックURLをメモ・チームに共有する

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup（Phase 1）**: 依存なし — 即座に開始可能
- **Foundational（Phase 2）**: Phase 1 完了後 — 全ユーザーストーリーをブロック
- **User Story 1（Phase 3）**: Phase 2 完了後 — 依存なし（MVP）
- **User Story 2（Phase 4）**: Phase 3 完了後（デプロイ済みプロジェクトが必要）
- **User Story 3（Phase 5）**: Phase 2 完了後（Phase 3 と並行可能）
- **Polish（Phase 6）**: 希望するストーリーが全て完了後

### User Story Dependencies

- **US1（P1）**: Phase 2 完了後すぐ開始可能 — 他ストーリーへの依存なし
- **US2（P2）**: US1 完了後（デプロイ済みプロジェクトが前提）
- **US3（P3）**: Phase 2 完了後すぐ開始可能（US1 と並行可能）

---

## Parallel Example: Phase 1 & 2

```bash
# Phase 2 完了後、US1 と US3 を並行開始できる:
Task A: "T005〜T008 [US1] 初回デプロイとURL確認"
Task B: "T014〜T016 [US3] ローカルプレビュー確認"
```

---

## Implementation Strategy

### MVP First（User Story 1 のみ）

1. Phase 1: Setup 完了（T001〜T002）
2. Phase 2: Foundational 完了（T003〜T004）— **全ストーリーのブロッカー**
3. Phase 3: User Story 1 完了（T005〜T008）
4. **STOP & VALIDATE**: パブリックURLで表示確認
5. **MVP達成** — 外部公開完了

### Incremental Delivery

1. Setup + Foundational → デプロイ基盤完成
2. User Story 1 → パブリックURL発行（MVP）
3. User Story 2 → 更新フロー確立
4. User Story 3 → ローカルプレビュー追加
5. Polish → 運用整備

---

## Notes

- `[P]` タスクは別ファイル・依存なしで並行実行可能
- `[Story]` ラベルでタスクを仕様書のユーザーストーリーと紐付け
- 各フェーズのCheckpointで独立テストを実施してから次フェーズへ
- `wrangler pages dev` のデフォルトポートは `8788`（使用中の場合は自動変更）
