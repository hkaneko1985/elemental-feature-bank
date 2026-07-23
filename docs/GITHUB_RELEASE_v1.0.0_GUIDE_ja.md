# GitHub Release v1.0.1 作成手順

対象リポジトリ：

```text
https://github.com/hkaneko1985/elemental-feature-bank
```

Release asset：

```text
elemental-feature-bank-v1.0.1-data.zip
```

予定SHA-256：

```text
c9399ecd0b730416f673019ace07a9f5af3c7dc58b61ffda7b5f7ff6292d000d
```

## 1. リポジトリ本体をmainへpushする

Windows PowerShellまたはGit Bashで、解凍したリポジトリのルートへ移動する。

```bash
git init
git branch -M main
git add .
git commit -m "Release Elemental Feature Bank v1.0.1"
git remote add origin https://github.com/hkaneko1985/elemental-feature-bank.git
git push -u origin main
```

すでにremoteが登録されている場合、`git remote add`は不要である。

## 2. タグを作成してpushする

```bash
git tag -a v1.0.1 -m "Elemental Feature Bank v1.0.1"
git push origin v1.0.1
```

`.github/workflows/validate.yml`は`v*`タグのpushで実行される。

## 3. GitHub Actionsを確認する

1. リポジトリの`Actions`を開く。
2. `Validate public dataset snapshot`を選択する。
3. `v1.0.1`のrunがSuccessであることを確認する。
4. run画面下部のartifact `validation-evidence-v1.0.1`を保存する。
5. run URL、commit SHA、artifactをTV-039の証拠として保存する。

## 4. Releaseを作成する

1. リポジトリ右側の`Releases`を開く。
2. `Draft a new release`を選択する。
3. `Choose a tag`で既存タグ`v1.0.1`を選択する。
4. Release titleを`Elemental Feature Bank v1.0.1`とする。
5. `RELEASE_NOTES_v1.0.1.md`の内容をRelease notesへ貼り付ける。
6. `Attach binaries by dropping them here or selecting them.`へ
   `elemental-feature-bank-v1.0.1-data.zip`を添付する。
7. `Set as the latest release`を有効にする。
8. pre-releaseにはしない。
9. `Publish release`を選択する。

## 5. 公開後に確認する

Release URL：

```text
https://github.com/hkaneko1985/elemental-feature-bank/releases/tag/v1.0.1
```

assetの想定URL：

```text
https://github.com/hkaneko1985/elemental-feature-bank/releases/download/v1.0.1/elemental-feature-bank-v1.0.1-data.zip
```

公開後、assetを再ダウンロードし、SHA-256が予定値と一致することを確認する。

## 6. Zenodo

GitHub Releaseへ添付したものと同じZIPを、変更・再圧縮せずにZenodo Datasetへ登録する。
GitHubとZenodoからそれぞれ再ダウンロードしたZIPのSHA-256を比較し、TV-040を完了する。
