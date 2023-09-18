#
# Ruby環境用ビルド
#
FROM ruby:3.2.2-bullseye

# 環境変数設定
ENV LANG=C.UTF-8 TZ=Asia/Tokyo

# パッケージ更新、脆弱性パッケージの削除
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get purge -y imagemagick imagemagick-6-common \
  && apt-get install -y lsb-release

# PostgreSQLクライアントのインストール
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list \
  && apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get install -y postgresql-client-14
