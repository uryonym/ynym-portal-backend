FROM python:3.12-slim-bookworm

# uv パッケージマネージャーをインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv の環境変数を設定
ENV PATH="/app/.venv/bin:$PATH" \
  UV_COMPILE_BYTECODE=1

# アプリケーションをコンテナにコピー
COPY . /app

# 依存パッケージをインストール
WORKDIR /app
RUN uv sync --locked --no-cache

# アプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
