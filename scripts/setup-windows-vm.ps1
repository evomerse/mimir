<#
Prepare une machine Windows (VM jetable ou CI) pour compiler Mimir :
  Git, Visual Studio 2022 Build Tools (C++ + SDK + ATL), MozillaBuild, source de Firefox ESR.
A lancer en administrateur. Journal : C:\Users\<utilisateur>\setup-windows-vm.log
Cree C:\ff\SETUP_DONE a la fin. Duree : 30 a 60 min, surtout du telechargement.
Les outils Rust et le compilateur Clang sont installes ensuite par `mach bootstrap`.
#>
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
Start-Transcript -Path "$env:USERPROFILE\setup-windows-vm.log" -Append | Out-Null

$FirefoxTag = "FIREFOX_153_5_0esr_BUILD1"
$Source = "C:\ff\esr153"
$Git = "C:\Program Files\Git\cmd\git.exe"

function Step($text) { "`n=== $(Get-Date -Format HH:mm:ss) $text" }

Step "Chemins longs"
New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem -Name LongPathsEnabled -Value 1 -PropertyType DWord -Force | Out-Null

if (-not (Test-Path $Git)) {
    Step "Git"
    winget install --id Git.Git -e --source winget --silent --disable-interactivity --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget (Git) a echoue : $LASTEXITCODE" }
}
# Les patchs sont en fins de ligne LF : pas de conversion CRLF a la copie.
& $Git config --system core.autocrlf false
& $Git config --system core.longpaths true

$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (-not ((Test-Path $vswhere) -and (& $vswhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath))) {
    Step "Visual Studio 2022 Build Tools (long)"
    $override = "--quiet --wait --norestart --nocache " +
        "--add Microsoft.VisualStudio.Workload.VCTools " +
        "--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 " +
        "--add Microsoft.VisualStudio.Component.Windows11SDK.22621 " +
        "--add Microsoft.VisualStudio.Component.VC.ATL"
    winget install --id Microsoft.VisualStudio.2022.BuildTools -e --source winget --silent --disable-interactivity --accept-source-agreements --accept-package-agreements --override $override
    if ($LASTEXITCODE -ne 0) { throw "winget (Build Tools) a echoue : $LASTEXITCODE" }
}

if (-not (Test-Path C:\mozilla-build\start-shell.bat)) {
    Step "MozillaBuild"
    $exe = "$env:TEMP\MozillaBuildSetup.exe"
    Invoke-WebRequest "https://ftp.mozilla.org/pub/mozilla/libraries/win32/MozillaBuildSetup-Latest.exe" -OutFile $exe
    Start-Process $exe -ArgumentList "/S" -Wait
}

if (-not (Test-Path "$Source\mach")) {
    Step "Source Firefox ESR $FirefoxTag"
    New-Item -ItemType Directory -Force C:\ff | Out-Null
    & $Git clone --depth 1 --branch $FirefoxTag https://github.com/mozilla-firefox/firefox.git $Source
    if ($LASTEXITCODE -ne 0) { throw "git clone a echoue" }
}

Step "Verification"
"git          : " + (Test-Path $Git)
"MozillaBuild : " + (Test-Path C:\mozilla-build\start-shell.bat)
"VS           : " + (& $vswhere -products * -property installationPath)
"source       : " + (Test-Path "$Source\mach")
Set-Content C:\ff\SETUP_DONE (Get-Date -Format s)
Step "Termine"
Stop-Transcript | Out-Null
