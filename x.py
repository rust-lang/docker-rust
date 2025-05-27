#!/usr/bin/env python3

from collections import namedtuple
from urllib import request
import os
import subprocess
import sys

rustup_version = "1.28.2"

Channel = namedtuple("Channel", ["name", "rust_version"])
stable = Channel("stable", "1.90.0")
nightly = Channel("nightly", "nightly")
supported_channels = [
    stable,
    nightly
]

DebianArch = namedtuple("DebianArch", ["bashbrew", "dpkg", "qemu", "rust"])

debian_lts_arches = [
    DebianArch("amd64", "amd64", "linux/amd64", "x86_64-unknown-linux-gnu"),
    DebianArch("arm32v7", "armhf", "linux/arm/v7", "armv7-unknown-linux-gnueabihf"),
    DebianArch("arm64v8", "arm64", "linux/arm64", "aarch64-unknown-linux-gnu"),
    DebianArch("i386", "i386", "linux/386", "i686-unknown-linux-gnu"),
]

debian_non_lts_arches = [
    DebianArch("ppc64le", "ppc64el", "linux/ppc64le", "powerpc64le-unknown-linux-gnu"),
    DebianArch("s390x", "s390x", "linux/s390x", "s390x-unknown-linux-gnu"),
]

debian_trixie_arches = [
    DebianArch("riscv64", "riscv64", "linux/riscv64", "riscv64gc-unknown-linux-gnu"),
]

latest_debian_release = "trixie"

DebianRelease = namedtuple("DebianRelease", ["name", "arches"])
 
debian_releases = [
    DebianRelease("bullseye", debian_lts_arches),
    DebianRelease("bookworm", debian_lts_arches + debian_non_lts_arches),
    DebianRelease(latest_debian_release, debian_lts_arches + debian_non_lts_arches + debian_trixie_arches),
]

AlpineArch = namedtuple("AlpineArch", ["bashbrew", "apk", "qemu", "rust"])

alpine_arches = [
    AlpineArch("amd64", "x86_64", "linux/amd64", "x86_64-unknown-linux-musl"),
    AlpineArch("arm64v8", "aarch64", "linux/arm64", "aarch64-unknown-linux-musl"),
    AlpineArch("ppc64le", "ppc64le", "linux/ppc64le", "powerpc64le-unknown-linux-musl"),
]

latest_alpine_version = "3.22"
alpine_versions = [
    "3.20",
    "3.21",
    latest_alpine_version,
]

def rustup_hash(arch):
    url = f"https://static.rust-lang.org/rustup/archive/{rustup_version}/{arch}/rustup-init.sha256"
    with request.urlopen(url) as f:
        return f.read().decode('utf-8').split()[0]

def read_file(file):
    with open(file, "r") as f:
        return f.read()

def write_file(file, contents):
    dir = os.path.dirname(file)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    with open(file, "w") as f:
        f.write(contents)

def update_debian():
    for release in debian_releases:
        arch_cases_str = arch_cases_start("$(dpkg --print-architecture)")
        for debian_arch in release.arches:
            arch_cases_str += arch_case(debian_arch.dpkg, debian_arch.rust)
        arch_cases_str += arch_cases_end()

        for channel in supported_channels:
            render_template(
                "Dockerfile-debian.template",
                channel.rust_version,
                release.name,
                arch_cases_str,
                f"{channel.name}/{release.name}/Dockerfile",
            )

            render_template(
                "Dockerfile-slim.template",
                channel.rust_version,
                release.name,
                arch_cases_str,
                f"{channel.name}/{release.name}/slim/Dockerfile",
            )

def update_alpine():
    arch_cases_str = arch_cases_start("$(apk --print-arch)")
    for arch in alpine_arches:
        arch_cases_str += arch_case(arch.apk, arch.rust)
    arch_cases_str += arch_cases_end()

    for version in alpine_versions:
        for channel in supported_channels:
            render_template(
                "Dockerfile-alpine.template",
                channel.rust_version,
                version,
                arch_cases_str,
                f"{channel.name}/alpine{version}/Dockerfile",
            )

def arch_cases_start(arch_cmd):
    start = f'arch="{arch_cmd}"; \\\n'
    start += '    case "$arch" in \\\n'
    return start

def arch_cases_end():
    end = '        *) echo >&2 "unsupported architecture: $arch"; exit 1 ;; \\\n'
    end += '    esac'
    return end

def arch_case(distro_arch, rust_arch):
    rustup_sha256 = rustup_hash(rust_arch)
    return f"        {distro_arch}) rustArch='{rust_arch}'; rustupSha256='{rustup_sha256}' ;; \\\n"

def render_template(
    template_path,
    rust_version,
    docker_tag,
    arch_cases,
    rendered_path
):
    template = read_file(template_path)
    rendered = template \
        .replace("%%TAG%%", docker_tag) \
        .replace("%%RUST-VERSION%%", rust_version) \
        .replace("%%RUSTUP-VERSION%%", rustup_version) \
        .replace("%%ARCH-CASE%%", arch_cases)
    write_file(rendered_path, rendered)

def update_ci():
    file = ".github/workflows/ci.yml"
    config = read_file(file)

    marker = "#RUST_VERSION\n"
    split = config.split(marker)
    rendered = split[0] + marker + f"      RUST_VERSION: {stable.rust_version}\n" + marker + split[2]

    versions = ""
    for release in debian_releases:
        versions += f"          - name: {release.name}\n"
        versions += f"            variant: {release.name}\n"
        versions += f"          - name: slim-{release.name}\n"
        versions += f"            variant: {release.name}/slim\n"

    for version in alpine_versions:
        versions += f"          - name: alpine{version}\n"
        versions += f"            variant: alpine{version}\n"

    marker = "#VERSIONS\n"
    split = rendered.split(marker)
    rendered = split[0] + marker + versions + marker + split[2]
    write_file(file, rendered)

def update_mirror_stable_ci():
    file = ".github/workflows/mirror_stable.yml"
    config = read_file(file)

    versions = ""
    for version in alpine_versions:
        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-alpine{version}")
        tags.append(f"alpine{version}")
        if version == latest_alpine_version:
            for version_tag in version_tags():
                tags.append(f"{version_tag}-alpine")
            tags.append("alpine")

        versions += f"          - name: alpine{version}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}\n"

    for release in debian_releases:
        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-{release.name}")
        tags.append(release.name)
        if release.name == latest_debian_release:
            for version_tag in version_tags():
                tags.append(version_tag)
            tags.append("latest")

        versions += f"          - name: {release.name}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}\n"

        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-slim-{release.name}")
        tags.append(f"slim-{release.name}")
        if release.name == latest_debian_release:
            for version_tag in version_tags():
                tags.append(f"{version_tag}-slim")
            tags.append("slim")
        
        versions += f"          - name: slim-{release.name}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}\n" 

    marker = "#VERSIONS\n"
    split = config.split(marker)
    rendered = split[0] + marker + versions + marker + split[2]
    write_file(file, rendered)


def update_nightly_ci():
    file = ".github/workflows/nightly.yml"
    config = read_file(file)


    versions = ""
    for release in debian_releases:
        platforms = []
        for arch in release.arches:
            platforms.append(f"{arch.qemu}")
        platforms = ",".join(platforms)

        tags = [f"nightly-{release.name}"]
        if release.name == latest_debian_release:
            tags.append("nightly")

        versions += f"          - name: {release.name}\n"
        versions += f"            context: nightly/{release.name}\n"
        versions += f"            platforms: {platforms}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}\n"

        versions += f"          - name: slim-{release.name}\n"
        versions += f"            context: nightly/{release.name}/slim\n"
        versions += f"            platforms: {platforms}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}-slim\n"

    for version in alpine_versions:
        platforms = []
        for arch in alpine_arches:
            platforms.append(f"{arch.qemu}")
        platforms = ",".join(platforms)

        tags = [f"nightly-alpine{version}"]
        if version == latest_alpine_version:
            tags.append("nightly-alpine")

        versions += f"          - name: alpine{version}\n"
        versions += f"            context: nightly/alpine{version}\n"
        versions += f"            platforms: {platforms}\n"
        versions += "            tags: |\n"
        for tag in tags:
            versions += f"              {tag}\n"

    marker = "#VERSIONS\n"
    split = config.split(marker)
    rendered = split[0] + marker + versions + marker + split[2]
    write_file(file, rendered)

def file_commit(file):
    return subprocess.run(
            ["git", "log", "-1", "--format=%H", "HEAD", "--", file],
            capture_output = True) \
        .stdout \
        .decode('utf-8') \
        .strip()

def version_tags():
    parts = stable.rust_version.split(".")
    tags = []
    for i in range(len(parts)):
        tags.append(".".join(parts[:i + 1]))
    return tags

def single_library(tags, architectures, dir):
    return f"""
Tags: {", ".join(tags)}
Architectures: {", ".join(architectures)}
GitCommit: {file_commit(os.path.join(dir, "Dockerfile"))}
Directory: {dir}
"""

def generate_stackbrew_library():
    commit = file_commit("x.py")

    library = f"""\
# this file is generated via https://github.com/rust-lang/docker-rust/blob/{commit}/x.py

Maintainers: Steven Fackler <sfackler@gmail.com> (@sfackler),
             Scott Schafer <schaferjscott@gmail.com> (@Muscraft),
             Jakub Beránek <berykubik@gmail.com> (@kobzol)
GitRepo: https://github.com/rust-lang/docker-rust.git
"""

    for release in debian_releases:
        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-{release.name}")
        tags.append(release.name)
        if release.name == latest_debian_release:
            for version_tag in version_tags():
                tags.append(version_tag)
            tags.append("latest")

        arches = release.arches[:]

        library += single_library(
                tags,
                map(lambda a: a.bashbrew, arches),
                os.path.join(stable.name, release.name))

        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-slim-{release.name}")
        tags.append(f"slim-{release.name}")
        if release.name == latest_debian_release:
            for version_tag in version_tags():
                tags.append(f"{version_tag}-slim")
            tags.append("slim")

        library += single_library(
                tags,
                map(lambda a: a.bashbrew, arches),
                os.path.join(stable.name, release.name, "slim"))

    for version in alpine_versions:
        tags = []
        for version_tag in version_tags():
            tags.append(f"{version_tag}-alpine{version}")
        tags.append(f"alpine{version}")
        if version == latest_alpine_version:
            for version_tag in version_tags():
                tags.append(f"{version_tag}-alpine")
            tags.append("alpine")

        library += single_library(
            tags,
            map(lambda a: a.bashbrew, alpine_arches),
            os.path.join(stable.name, f"alpine{version}"))

    print(library)

def usage():
    print(f"Usage: {sys.argv[0]} update|generate-stackbrew-library")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    task = sys.argv[1]
    if task == "update":
        update_debian()
        update_alpine()
        update_ci()
        update_mirror_stable_ci()
        update_nightly_ci() 
    elif task == "generate-stackbrew-library":
        generate_stackbrew_library()
    else:
        usage()
