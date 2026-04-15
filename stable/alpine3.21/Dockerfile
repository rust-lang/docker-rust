FROM alpine:3.21

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

RUN apk add --no-cache \
        ca-certificates \
        musl-dev \
        gcc

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.98.1

RUN set -eux; \
    \
    arch="$(apk --print-arch)"; \
    case "$arch" in \
        'x86_64') \
            rustArch='x86_64-unknown-linux-musl'; \
            rustupSha256='331228566cc931f32cd684f9bebc5956a5e5d7394c8d5de595f196a658ab98e6'; \
            ;; \
        'aarch64') \
            rustArch='aarch64-unknown-linux-musl'; \
            rustupSha256='1ddf36182ac5d1782dbeefcb9bea7f5f9412d88f4a0d5047b1564a223624e8c6'; \
            ;; \
        'ppc64le') \
            rustArch='powerpc64le-unknown-linux-musl'; \
            rustupSha256='8bee6e9158cbfba278df2b28941e64450be4b4aac423881ee380d3e85f774deb'; \
            ;; \
        'riscv64') \
            rustArch='riscv64gc-unknown-linux-musl'; \
            rustupSha256='e29a1d528186309c19710c40a70ca4aa3bec975cbbeaa6b65493728e4366c89d'; \
            ;; \
        *) \
            echo >&2 "unsupported architecture: $arch"; \
            exit 1; \
            ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.29.1/${rustArch}/rustup-init"; \
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
