ARG RUBY_VERSION=3.2.2

FROM ruby:${RUBY_VERSION}-slim as base

# 環境変数設定
ENV LANG="C.UTF-8" \
    TZ="Asia/Tokyo" \
    RAILS_ENV="development" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle"

FROM base as build

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential git libpq-dev \
      libvips pkg-config curl libvips postgresql-client
