FROM debian:stretch-slim

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.34.2

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        libc6-dev \
        wget \
        ; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='31c0581e3af128f7374d8439068475d11be60ce7b2301684a4cab81a39c76cb6' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='7fff409910faa28dc846547102a0a912020c357eb483b5b74e2740864b290896' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='168191448a932e13147686565e46803cca6b8d2b016a8761375c4d3ee3d2ac87' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='a6c7e20f71e13abd40917d76c023253501a35daacdeed31f9eaf8ecfd5d78286' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.18.2/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain $RUST_VERSION; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version; \
    apt-get remove -y --auto-remove \
        wget \
        ; \
    rm -rf /var/lib/apt/lists/*;
