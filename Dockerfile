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
RUN apt-get update     && \
    apt-get install -y    \
        binutils          \
        ruby
COPY --from=builder /tmp/deb/*.deb /tmp/
RUN cd /tmp/ && dpkg -i *.deb
CMD ["/bin/bash"]

