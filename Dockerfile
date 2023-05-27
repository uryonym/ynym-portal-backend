FROM ruby:3.2.2 AS ruby-base
WORKDIR /app
ENV BUNDLE_PATH vendor/bundle


FROM ruby-base AS build-ruby-gems
COPY Gemfile* /app/
RUN bundle install


FROM ruby-base
WORKDIR /app
ENV LANG ja_JP.UTF-8
ENV RAILS_ENV production

COPY --from=build-ruby-gems /app/vendor vendor/

COPY . /app
