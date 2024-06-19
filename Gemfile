# frozen_string_literal: true

source "https://rubygems.org"
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby "3.3.3"

gem "active_model_serializers"
gem "bootsnap", require: false
gem "dotenv-rails"
gem "jwt"
gem "pg", "~> 1.1"
gem "puma"
gem "rack-cors"
gem "rails", "7.1.3.4"
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]

group :development, :test do
  gem "debug", platforms: [:mri, :mingw, :x64_mingw]
  gem "faker", require: false
end

group :development do
  gem "rubocop", require: false
  gem "rubocop-performance", require: false
  gem "rubocop-rails", require: false
  gem "rubocop-rspec", require: false
  gem "rubocop-shopify", require: false
  gem "web-console"
end
