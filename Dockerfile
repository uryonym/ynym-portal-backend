#
# Rubyベース用ビルド
#
FROM ruby:3.2.2 AS ruby-base
WORKDIR /app
ENV BUNDLE_PATH vendor/bundle


#
# Rubyモジュール用ビルド
#
FROM ruby-base AS build-ruby-gems
COPY Gemfile* /app/
RUN bundle install


#
# 本番用ビルド
#
FROM ruby-base
ENV LANG ja_JP.UTF-8
ENV RUBY_YJIT_ENABLE 1
ENV RAILS_ENV production
ENV RAILS_SERVE_STATIC_FILES true
ENV LD_LIBRARY_PATH /usr/local/lib

WORKDIR /app
COPY --from=build-ruby-gems /app/vendor vendor/

COPY . /app
