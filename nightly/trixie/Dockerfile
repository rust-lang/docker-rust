FROM buildpack-deps:trixie

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

ARG RUST_VERSION=nightly
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=${RUST_VERSION}

RUN set -eux; \
    \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        'amd64') \
            rustArch='x86_64-unknown-linux-gnu'; \
            rustupSha256='b1c8cb14e30889e7e2999e6b69e62d9e9b9ffc0f4df8180564d306d9680e6c55'; \
            ;; \
        'armhf') \
            rustArch='armv7-unknown-linux-gnueabihf'; \
            rustupSha256='3d5771c716551ee55368be40e02859705f06d725b31df07c15e3593be2d2a5de'; \
            ;; \
        'arm64') \
            rustArch='aarch64-unknown-linux-gnu'; \
            rustupSha256='9f608c142e0e38a78957d0661ba1dfaf0b6fb37184cfaa4b9a0aa57af6184282'; \
            ;; \
        'i386') \
            rustArch='i686-unknown-linux-gnu'; \
            rustupSha256='ef58377096e940ed8ba0d7f8841e6d125922d9d218e04897a05b7f667cf6f5c5'; \
            ;; \
        'ppc64el') \
            rustArch='powerpc64le-unknown-linux-gnu'; \
            rustupSha256='d5b321db031525fbee38b736846f07a16df22b354a1964bbb79ff83495dbc0c9'; \
            ;; \
        's390x') \
            rustArch='s390x-unknown-linux-gnu'; \
            rustupSha256='df1762614062280a326ac988019ed1f8ceebeafa5fac95164a7201ff10e31d4b'; \
            ;; \
        'riscv64') \
            rustArch='riscv64gc-unknown-linux-gnu'; \
            rustupSha256='e4a960952692ac3dfb5fa4f74e593517241b83e43a93fbdcf2213c811748f1ae'; \
            ;; \
        *) \
            echo >&2 "unsupported architecture: $arch"; \
            exit 1; \
            ;; \
    esac; \
    \
    url="https://static.rust-lang.org/rustup/archive/1.29.3/${rustArch}/rustup-init"; \
    wget --progress=dot:giga "$url"; \
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
