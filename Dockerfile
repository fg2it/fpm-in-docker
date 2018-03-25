#Build FPM
FROM debian:stretch as builder

ARG FPM_VERSION=1.9.3

RUN apt-get update       && \
    apt-get install -y      \
        gcc                 \
        libc-dev            \
        make                \
        ruby                \
        ruby-dev         && \
    gem install -N fpm   && \
    gem install -N --install-dir /tmp/gems fpm -v ${FPM_VERSION} && \
    mkdir -p /tmp/deb    && \
    cd /tmp/deb          && \
    find /tmp/gems/cache -name '*.gem' | xargs -rn1 fpm -d ruby -d rubygems --prefix $(gem environment gemdir) -s gem -t deb



FROM debian:stretch-slim

ARG BUILD_DATE
ARG VCS_REF

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.vcs-url="https://github.com/fg2it/fpm-in-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF

RUN apt-get update     && \
    apt-get install -y --no-install-recommends \
        binutils          \
        ruby           && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /tmp/deb/*.deb /tmp/

RUN cd /tmp/       && \
    dpkg -i *.deb  && \
    rm -rf  *.deb  

CMD ["/bin/bash"]

