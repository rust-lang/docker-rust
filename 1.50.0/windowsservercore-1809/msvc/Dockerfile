# escape=`

# IMAGES BUILT FROM THIS DOCKERFILE ARE NOT TO BE SHARED ON PUBLIC DOCKER HUBs.
#
# WARNING: NON-FREE AND DISTRIBUTION RESTRICTED ENCUMBERED SOFTWARE IN IMAGE.
#
# The VS Build Tools are very encumbered.
#
# IMAGE SHOULD ONLY BE BUILT BY USERS WHO CAN FOLLOW THESE TERMS:
# https://visualstudio.microsoft.com/license-terms/mlt553512/
#
# See the fourth paragraph of this blog post for a warning from a Microsoftie:
# https://blogs.msdn.microsoft.com/vcblog/2018/08/13/using-msvc-in-a-docker-container-for-your-c-projects/
#
# """
# The VS Build Tools are licensed as a supplement to your existing Visual Studio license.
# Any images built with these tools should be for your personal use or for use in your
# organization in accordance with your existing Visual Studio and Windows licenses.
# Please don’t share these images on a public Docker hub.
# """
#
# That said, this Dockerfile will be built in a CI system for validation and testing in the project
# but most definitely will skip deployment.

FROM mcr.microsoft.com/windows/servercore:1809

SHELL ["powershell.exe", "-NoLogo", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

RUN $url = 'https://download.visualstudio.microsoft.com/download/pr/20130c62-1bc8-43d6-b4f0-c20bb7c79113/7276a7355219f7988c480d198e23c2973bbb7ab971c4f0415c26cab2955344e5/vs_BuildTools.exe'; `
    $sha256 = '7276A7355219F7988C480D198E23C2973BBB7AB971C4F0415C26CAB2955344E5'; `
    Invoke-WebRequest -Uri $url -OutFile C:\vs_BuildTools.exe; `
    $actual256 = (Get-FileHash vs_BuildTools.exe -Algorithm sha256).Hash; `
    if ($actual256 -ne $sha256) { `
       Write-Host 'FAILED!'; `
       Write-Host ('expected: {0}' -f $sha256); `
       Write-Host ('got:      {0}' -f $actual256); `
       exit 1; `
    }; `
    Start-Process -filepath C:\vs_BuildTools.exe -wait -argumentlist ' `
        --quiet --wait --norestart --nocache `
        --installPath C:\BuildTools `
        --add Microsoft.Component.MSBuild `
        --add Microsoft.VisualStudio.Component.Windows10SDK.17763 `
        --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64'; `
    Remove-Item 'C:\\vs_BuildTools.exe'; `
    Remove-Item -Force -Recurse 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer'; `
    [Environment]::SetEnvironmentVariable('__VSCMD_ARG_NO_LOGO', '1', [EnvironmentVariableTarget]::Machine)

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
    C:\rustup-init.exe -y -v --no-modify-path --default-toolchain ${env:RUST_VERSION} --default-host x86_64-pc-windows-msvc; `
    Remove-Item C:\rustup-init.exe; `
    rustup -V; `
    cargo -V; `
    rustc -V
