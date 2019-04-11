FROM buildpack-deps:stretch

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.34.0

RUN set -eux; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='ce09d3de51432b34a8ff73c7aaa1edb64871b2541d2eb474441cedb8bf14c5fa' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='bf140b03a49abb87a601ad29ca326b4e6721be39868c90ad17cd0b76014f1789' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='76010a472d90714f781d5a4ce618f0e1f8ce3a8b8476ce35a34b2f6ab67a8026' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='bde10f3e1a267923224792bb26b605b1189733c9d0c806da955e5c5c45b2868c' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.17.0/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain $RUST_VERSION; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;
