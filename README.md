# OpenCTI PyCTI ツールセット

このリポジトリには、OpenCTIプラットフォームとPyCTIライブラリを使用して、脅威インテリジェンスデータを作成・管理するためのPythonスクリプト群が含まれています。

## 概要

OpenCTIは、サイバー脅威インテリジェンス（CTI）を構造化し、分析するためのオープンソースプラットフォームです。このツールセットは、PyCTI（OpenCTIのPythonクライアントライブラリ）を使用して、OpenCTIプラットフォームとプログラム的に対話するためのスクリプトを提供します。

## 含まれるスクリプト

### 1. create_report_only.py

レポートのみを作成するシンプルなスクリプトです。

```bash
python create_report_only.py --name "レポート名" --description "レポートの説明"
```

### 2. create_observable.py

Observableを作成するスクリプトです。IPアドレス、URL、ファイルハッシュなどの観測可能なデータを作成できます。

```bash
python create_observable.py --type "IPv4-Addr" --value "8.8.8.8" --description "テスト用IPアドレス"
```

### 3. create_indicator.py

Indicatorを作成するスクリプトです。STIXパターンを使用して、悪意のある活動を示す指標を作成できます。

```bash
python create_indicator.py --name "悪意のあるIPアドレス指標" --pattern "[ipv4-addr:value = '8.8.8.8']"
```

### 4. create_report_with_relationships.py

レポート、Observable、Indicator、およびそれらの関係性を一度に作成するスクリプトです。これにより、完全な脅威インテリジェンスレポートを作成できます。

```bash
python create_report_with_relationships.py --report-name "マルウェア分析レポート" --ip "8.8.8.8" --url "https://malicious-example.com"
```

### 5. config.py

OpenCTI APIの設定を一元管理するための設定ファイルです。すべてのスクリプトはこのファイルから設定を読み込みます。

## 機能

- レポートの作成
- Observableの作成（IPアドレス、URL、ファイルハッシュなど）
- Indicatorの作成（STIXパターンを使用）
- ObservableとIndicator間の関係性の作成
- すべてのエンティティをレポートに関連付け

## 必要条件

- Python 3.6以上
- PyCTIライブラリ
- OpenCTIプラットフォームへのアクセス権とAPIキー

## インストール

1. 必要なライブラリをインストールします：

```bash
pip install pycti
```

2. `config.py`ファイル内のAPI設定を更新します：

```python
# OpenCTI APIの設定
API_URL = "https://your-opencti-instance.com"  # OpenCTIのURLを設定
API_KEY = "your-api-key"  # OpenCTIのAPIキーを設定

# デフォルト設定
DEFAULT_CONFIDENCE = 75  # 信頼度のデフォルト値
DEFAULT_TLP = "TLP:AMBER"  # TLPマーキングのデフォルト値
DEFAULT_VALID_DAYS = 30  # Indicatorの有効期間（日数）
```

## 使用例

### 完全な脅威レポートの作成

```bash
python create_report_with_relationships.py --report-name "APT攻撃分析レポート" --ip "10.0.0.1" --url "https://malicious-site.example.com"
```

このコマンドは以下を実行します：
1. 「APT攻撃分析レポート」という名前のレポートを作成
2. IPアドレス（10.0.0.1）とURL（https://malicious-site.example.com）のObservableを作成
3. 各Observableに対応するIndicatorを作成
4. ObservableとIndicator間の関係性を設定
5. すべてのエンティティをレポートに関連付け

## 設定のカスタマイズ

`config.py`ファイルでは、以下の設定をカスタマイズできます：

- `API_URL`: OpenCTIインスタンスのURL
- `API_KEY`: OpenCTIのAPIキー
- `DEFAULT_CONFIDENCE`: 信頼度のデフォルト値（0-100）
- `DEFAULT_TLP`: TLPマーキングのデフォルト値（TLP:WHITE, TLP:GREEN, TLP:AMBER, TLP:RED）
- `DEFAULT_VALID_DAYS`: Indicatorの有効期間（日数）

## テスト

このプロジェクトには、各スクリプトの機能をテストするための単体テストが含まれています。テストは、実際のOpenCTI環境に接続せずに実行できるように、モックを使用しています。

### テストの実行

すべてのテストを実行するには、以下のコマンドを使用します：

```bash
python run_tests.py
```

特定のテストのみを実行するには、以下のコマンドを使用します：

```bash
python -m unittest tests/test_create_report.py
python -m unittest tests/test_create_observable.py
python -m unittest tests/test_create_indicator.py
python -m unittest tests/test_create_report_with_relationships.py
```

### テストの構造

テストは以下のディレクトリとファイルで構成されています：

- `tests/`: テストディレクトリ
  - `test_config.py`: テスト用の設定ファイル
  - `mock_opencti.py`: OpenCTI APIのモック
  - `test_create_report.py`: レポート作成のテスト
  - `test_create_observable.py`: Observable作成のテスト
  - `test_create_indicator.py`: Indicator作成のテスト
  - `test_create_report_with_relationships.py`: 関係性を含むレポート作成のテスト

### テスト駆動開発（TDD）

このプロジェクトでは、テスト駆動開発（TDD）の原則に従って開発を進めることができます。新しい機能を追加する場合は、以下の手順に従ってください：

1. 新しい機能のテストを作成する
2. テストが失敗することを確認する
3. テストが通るように機能を実装する
4. テストが通ることを確認する
5. コードをリファクタリングする（テストが引き続き通ることを確認）

## 注意事項

- OpenCTIのデモ環境では、一部の機能が制限されている場合があります
- APIの使用方法はOpenCTIのバージョンによって異なる場合があります
- 実際の環境で使用する前に、テスト環境でスクリプトをテストすることをお勧めします

## トラブルシューティング

エラーが発生した場合は、以下を確認してください：

1. OpenCTI APIのURLとAPIキーが正しいこと
2. OpenCTIサーバーが稼働していること
3. APIキーに適切な権限があること
4. ネットワーク接続に問題がないこと

## 参考資料

- [OpenCTI公式ドキュメント](https://filigran.notion.site/OpenCTI-Public-Knowledge-Base-d411e5e477734c59887dad3649f20518)
- [PyCTI GitHub リポジトリ](https://github.com/OpenCTI-Platform/client-python) 