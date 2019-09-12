FROM alpine:3.10

RUN apk add --no-cache \
        ca-certificates \
        gcc

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.37.0

RUN set -eux; \
    url="https://static.rust-lang.org/rustup/archive/1.19.0/x86_64-unknown-linux-musl/rustup-init"; \
    wget "$url"; \
    echo "b535be813cd89000044764806f569a8c1428417d4226f16ee9993867f0c4ea4e *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain $RUST_VERSION; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;
