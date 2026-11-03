FROM alpine:3.23

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

RUN apk add --no-cache \
        ca-certificates \
        musl-dev \
        gcc

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.99.1

RUN set -eux; \
    \
    arch="$(apk --print-arch)"; \
    case "$arch" in \
        'x86_64') \
            rustArch='x86_64-unknown-linux-musl'; \
            rustupSha256='1552169aba2836777136ccff7a381e95c17233b5d8250cd5e10ae3cb971bfcfc'; \
            ;; \
        'aarch64') \
            rustArch='aarch64-unknown-linux-musl'; \
            rustupSha256='956deacdc27ab82ae7ac821d5d3e9e95e4795d476d17efe99743bb8531ca1031'; \
            ;; \
        'ppc64le') \
            rustArch='powerpc64le-unknown-linux-musl'; \
            rustupSha256='334e1e79626a20a31f5cbc4d16e0386b280cc77e46da90bf5db68045b2012a74'; \
            ;; \
        'riscv64') \
            rustArch='riscv64gc-unknown-linux-musl'; \
            rustupSha256='3d87288288b166938b770e86a96f412b21413465b093ebee1efa71c6b9efd294'; \
            ;; \
        *) \
            echo >&2 "unsupported architecture: $arch"; \
            exit 1; \
            ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.29.3/${rustArch}/rustup-init"; \
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
