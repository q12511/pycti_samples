FROM python:3.8.10-slim

WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 設定ファイルのサンプルをコピー
RUN cp config.py config.sample.py

# 実行時の環境変数
ENV PYTHONUNBUFFERED=1

# コンテナ起動時のコマンド
CMD ["python", "create_report_with_relationships.py"] 