ARG RUBY_VERSION=3.3.0-bookworm

FROM ruby:${RUBY_VERSION}

RUN apt-get update -qq && \
    export DEBIAN_FRONTEND=noninteractive && \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    apt-get purge -y imagemagick imagemagick-6-common && \
    apt-get install --no-install-recommends -y libvips ffmpeg poppler-utils postgresql-client
