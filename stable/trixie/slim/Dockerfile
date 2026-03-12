FROM debian:trixie-slim

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.94.0

RUN set -eux; \
    \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        libc6-dev \
        wget \
        ; \
    \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        'amd64') \
            rustArch='x86_64-unknown-linux-gnu'; \
            rustupSha256='4acc9acc76d5079515b46346a485974457b5a79893cfb01112423c89aeb5aa10'; \
            ;; \
        'armhf') \
            rustArch='armv7-unknown-linux-gnueabihf'; \
            rustupSha256='124e02253af9128f9e27ea1ac929cbb73cf44cf35469d0f594a1b62f7b71fea1'; \
            ;; \
        'arm64') \
            rustArch='aarch64-unknown-linux-gnu'; \
            rustupSha256='9732d6c5e2a098d3521fca8145d826ae0aaa067ef2385ead08e6feac88fa5792'; \
            ;; \
        'i386') \
            rustArch='i686-unknown-linux-gnu'; \
            rustupSha256='5140e82096f96d1d8077f00eb312648e0e5106d101c9918d086f72cbc69bb3a1'; \
            ;; \
        'ppc64el') \
            rustArch='powerpc64le-unknown-linux-gnu'; \
            rustupSha256='4bfff85bd3967d988e14567aa9cc6ab0ea386f0ffeff0f9f14d23f0103bf1f97'; \
            ;; \
        's390x') \
            rustArch='s390x-unknown-linux-gnu'; \
            rustupSha256='66c2c132428b6b77803facb02cbdf33b89d20c00bd20da142be8cb651f2e7cd8'; \
            ;; \
        'riscv64') \
            rustArch='riscv64gc-unknown-linux-gnu'; \
            rustupSha256='7e43f2b2e6307d61da17a4dff61e6bceef408b8189822df64e1094590d2a70f9'; \
            ;; \
        *) \
            echo >&2 "unsupported architecture: $arch"; \
            exit 1; \
            ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.29.0/${rustArch}/rustup-init"; \
    wget --progress=dot:giga "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    \
    apt-get remove -y --auto-remove \
        wget \
        ; \
    rm -rf /var/lib/apt/lists/*; \
    \
    rustup --version; \
    cargo --version; \
    rustc --version;
