FROM buildpack-deps:bookworm

LABEL org.opencontainers.image.source=https://github.com/rust-lang/docker-rust

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.85.0

RUN set -eux; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='c8d03f559a2335693379e1d3eaee76622b2a6580807e63bcd61faea709b9f664' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='fe8bc715bb116b86cb8c126bd4ad96efe9cb6f965c19a64e2aa8bd844c9e9ed5' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='46ccc85ca7f6c5ed28141cdc0a107c51a8ae71272899213a1f44820c7f6440b5' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='27ee6b6e0ca43a37ee4fcbe1ab2d5ad4fbf224bbfbbfda085345c2bfb63ab785' ;; \
        ppc64el) rustArch='powerpc64le-unknown-linux-gnu'; rustupSha256='570e9a36a9c981a67b7e44f28776f7ece60141e2b63ba279ff0989c6053f3c67' ;; \
        s390x) rustArch='s390x-unknown-linux-gnu'; rustupSha256='f48e2d5a41a057b758e4cb9daf60e9adfcfc555e83eff2d62caa2dc51f9bc6da' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.28.0/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;
