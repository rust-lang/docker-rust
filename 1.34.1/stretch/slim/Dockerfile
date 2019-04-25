FROM debian:stretch-slim

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.34.1

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
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='7d610882f67ec4e53a56a8177d7862501a043f80be7ba13b6e325cc9921f23b8' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='3bc5c5fff32113dc20284bd605eb2a6f7070de0c69c742b00b0ca4511a8fbc4c' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='cff57e155046439896004d7eb66fcbebe436f00298b1dacef426aef0a109a866' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='2d82bf50439c6ec74af4a5642a004fe8915921b52d3ec54032e0dc10476718c1' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.18.1/${rustArch}/rustup-init"; \
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
