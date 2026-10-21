FROM alpine:3.22

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

RUN apk add --no-cache \
        ca-certificates \
        musl-dev \
        gcc

ARG RUST_VERSION=nightly
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=${RUST_VERSION}

RUN set -eux; \
    \
    arch="$(apk --print-arch)"; \
    case "$arch" in \
        'x86_64') \
            rustArch='x86_64-unknown-linux-musl'; \
            rustupSha256='2ba97d668c06dc4b1884f2a3fa6f4cf14b9bd0c1db379af7e4f87a705ff19edd'; \
            ;; \
        'aarch64') \
            rustArch='aarch64-unknown-linux-musl'; \
            rustupSha256='7fdbb23acf6495efee2e371580c52b365917551b4835090a225c44ac30915235'; \
            ;; \
        'ppc64le') \
            rustArch='powerpc64le-unknown-linux-musl'; \
            rustupSha256='d0f97151d3ed165ca11c68b460cabf1b828dc605525ce68bb0ef8f62f78ac8b6'; \
            ;; \
        'riscv64') \
            rustArch='riscv64gc-unknown-linux-musl'; \
            rustupSha256='4890a2396b60d0479a77917b05a78bdd7aa0ef5d29d44b8892314b5ffe2c1d5b'; \
            ;; \
        *) \
            echo >&2 "unsupported architecture: $arch"; \
            exit 1; \
            ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.29.2/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    \
    rustup --version; \
    cargo --version; \
    rustc --version;
