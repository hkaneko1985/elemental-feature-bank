# Elemental Feature Bank（元素特徴量バンク）

[English README](README.md)

## 2026年10月改訂：分類監査の説明訂正と利用例

基礎データはv1.0.1（118元素、解釈可能822列、その他944列）のままです。
DOI: https://doi.org/10.5281/zenodo.21509504
追加資料は [revision_support/20261010/](revision_support/20261010/) にあります。
新しいパッケージのタグ案はv1.0.2ですが、数値データの版はv1.0.1を維持します。

**訂正：** 過去の「盲検第二評価」「独立評価者」という表現を撤回します。
規則の開発時に初回Tierラベルが参照可能でした。正確にはAI支援型の規則ベース整合性監査であり、
独立した人間評価者間の信頼性を検証したものではありません。一致率97.69%、κ=0.9607306は
関連するラベル集合間の記述的な整合性指標です。

改訂時の検証状態は34 PASS、4 PASS WITH NOTE、2 DEFERRED、0 FAILです。
TV-036の独立評価要件とTV-040の両ホストからの新規ダウンロード照合は未完了です。
TV-039は公開されたタグ付き実行のSuccessを確認しています。
以下に残る旧報告書・旧説明・40試験の記録は履歴資料です。矛盾する過去の記述より本訂正を優先します。

追加資料は分類規則の再現、3組成の記述子作成例と8テスト、全元素ラベル付き図、維持管理方針を含みます。
物性予測ベンチマークや新しい元素値の追加はありません。
新Zenodo版公開後に、そのDOIを「改訂補足資料DOI」として追記し、元DOIは「基礎データDOI」として残してください。


本リポジトリは、マテリアルズインフォマティクスで利用する元素特徴量を、**出典・版・条件・解釈可能性・再配布判定**とともに整理したデータセットです。公開版は118元素を対象とし、`GREEN`判定の出典だけから構成されています。

## 公開データ

| ファイル | 元素数 | 特徴量数 | 内容 |
|---|---:|---:|---|
| `element_data_interpretable.csv` | 118 | 822 | 直接量、条件依存直接量、透明な派生量 |
| `element_data_others.csv` | 118 | 944 | 補助量、経験尺度、学習済み・符号化表現 |
| **合計** | **118** | **1,766** | 2ファイル間で特徴量名の重複なし |

行順はH～Ogです。欠損値は空欄のまま保持し、補完、標準化、PCA等は実施していません。

## 読み込み例

```python
import pandas as pd

interpretable = pd.read_csv("element_data_interpretable.csv", index_col=0)
others = pd.read_csv("element_data_others.csv", index_col=0)
metadata = pd.read_csv("element_feature_metadata.csv")
```

本データは「全列を一括投入する最終学習行列」ではなく、目的に応じて特徴量ブロックを選択するための特徴量バンクです。欠損補完、標準化、特徴選択、次元削減は交差検証の各学習fold内で実施してください。

## メタデータと出典

- `element_feature_metadata.csv`：公開1,766列の列単位メタデータ
- `element_feature_block_summary.csv`：ブロック別の列数・被覆率
- `element_source_registry.csv`：公開対象となった26件の`GREEN`出典
- `source_license_policy.csv`：全44出典の公開判定
- `excluded_sources.csv`：公開版から除外した18出典
- `excluded_features.csv`：公開版から除外した3,434列

詳細は [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) と [`docs/LICENSING.md`](docs/LICENSING.md) を参照してください。

## AMBER/HOLD特徴量のローカル再構築

AMBER/HOLD由来の3,434特徴量の値は、公開CSVには含めていません。利用者が元配布物へ正当にアクセスできる場合に限り、`scripts/`の取得・再構築スクリプトをローカルで使用できます。再構築した値は、アセット単位の再配布権を別途確認しない限り、GitHubへ再コミットしないでください。

詳細手順：[`docs/OPTIONAL_FEATURES.md`](docs/OPTIONAL_FEATURES.md)

## Technical Validation

40項目の事前定義試験を実行しました。

| 判定 | 件数 |
|---|---:|
| PASS | 33 |
| PASS WITH NOTE | 5 |
| DEFERRED | 2 |
| FAIL | 0 |

- 直接ソース/API照合：107,950件、失敗0
- 任意特徴量のローカル再構築照合：405,212セル、不一致0
- 公開値のpre-filter版との保持確認：208,388セル、不一致0

主な検証資料は `validation/` にあります。通常のpush/pull requestでは、標準ライブラリのみで実行できる軽量検証をGitHub Actionsで実行します。

```bash
python scripts/validate_repository_snapshot.py --repo-root .
```

全40項目の再実行には、公開していない元アセットとpre-filter版が必要です。詳細は [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) を参照してください。

## 著者・研究費

- **著者:** Hiromasa Kaneko（金子 弘昌）、明治大学 理工学部 応用化学科
- **リポジトリ:** https://github.com/hkaneko1985/elemental-feature-bank
- **Funding:** This work was supported by Grants-in-Aid for Scientific Research (KAKENHI) (Grant Numbers 24K08152 and 24K01234) from the Japan Society for the Promotion of Science.

詳細は [`AUTHORS.md`](AUTHORS.md) と [`FUNDING.md`](FUNDING.md) を参照してください。

## 引用

release v1.0.1用の [`CITATION.cff`](CITATION.cff) を収録しています。データセットを用いた論文では、Data Descriptor、使用したデータ版、実際に用いた特徴量ブロックの原典を引用してください。アーカイブDOI取得後に `CITATION.cff` と `.zenodo.json` へ追記してください。

## ライセンス

本リポジトリ全体へ一律のライセンスを適用したとはみなしません。

- 独自コード：著作権者名を記入済みの`LICENSE_CODE.template`を収録しています。MIT Licenseを正式採用する場合に限り`LICENSE`へ変更
- データ権利の説明：`DATA_LICENSE.md`
- 第三者出典：`THIRD_PARTY_LICENSES.md`
- 科学的引用：`ATTRIBUTION.md`

ライセンス監査は研究データ公開に向けたデューデリジェンスであり、法的助言ではありません。公開前に所属機関の知財・法務・研究データ担当による確認を推奨します。

## 貢献

誤値の報告、新規出典の提案、メタデータ改善は歓迎します。手順は [`CONTRIBUTING.md`](CONTRIBUTING.md) を参照してください。

## Tier分類レビュー

全5,200特徴量について、初回Tierと行列分割を入力から除外したAI支援型の盲検第二評価を実施しました。完全一致率は**97.69%**、7分類のCohenのκは**0.9607**でした。裁定の結果、Mendeleev由来のMiedemaモデル量3列を解釈可能行列からその他行列へ移しました。値自体は変更していません。

本評価は二人目の独立した人間評価者ではありません。論文で人間評価者間一致を主張する前に、専門家による確認を推奨します。機械可読の証拠は[`validation/tier_review/`](validation/tier_review/)にあります。
