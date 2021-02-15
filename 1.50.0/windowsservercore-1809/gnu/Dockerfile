# escape=`

FROM mcr.microsoft.com/windows/servercore:1809

SHELL ["powershell.exe", "-NoLogo", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

ENV RUSTUP_HOME=C:\rustup `
    CARGO_HOME=C:\cargo `
    RUST_VERSION=1.50.0

RUN [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12; `
    $url = 'https://static.rust-lang.org/rustup/archive/1.23.1/x86_64-pc-windows-msvc/rustup-init.exe'; `
    $sha256 = 'a586cf9de3e4aa791fd5796b6a5f99ca05591ccef8bb94e53af5b69f0261fb03'; `
    Invoke-WebRequest -Uri $url -OutFile C:\rustup-init.exe; `
    $actual256 = (Get-FileHash rustup-init.exe -Algorithm sha256).Hash; `
    if ($actual256 -ne $sha256) { `
       Write-Host 'FAILED!'; `
       Write-Host ('expected: {0}' -f $sha256); `
       Write-Host ('got:      {0}' -f $actual256); `
       exit 1; `
    }; `
    New-Item ${env:CARGO_HOME}\bin -type directory | Out-Null; `
    $newPath = ('{0}\bin;{1}' -f ${env:CARGO_HOME}, ${env:PATH}); `
    [Environment]::SetEnvironmentVariable('PATH', $newPath, [EnvironmentVariableTarget]::Machine); `
    [Environment]::SetEnvironmentVariable('PATH', $newPath, [EnvironmentVariableTarget]::Process); `
    C:\rustup-init.exe -y -v --no-modify-path --default-toolchain ${env:RUST_VERSION} --default-host x86_64-pc-windows-gnu; `
    Remove-Item C:\rustup-init.exe; `
    rustup -V; `
    cargo -V; `
    rustc -V
