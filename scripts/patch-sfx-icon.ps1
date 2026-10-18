<#
Remplace l'icone et le nom de produit du module SFX (7zSD.Win32.sfx) qui enveloppe l'installeur Windows.
Le module est un binaire precompile de Mozilla : son icone Firefox est une ressource, modifiee ici avec rcedit
(MIT, https://github.com/electron/rcedit). On modifie le module AVANT d'y accrocher l'archive : retoucher
l'installeur fini supprimerait l'archive. Resultat : overlay/other-licenses/7zstub/firefox/7zSD.Win32.sfx
Usage (PowerShell, a lancer une fois ; le resultat est versionne) :
  scripts/patch-sfx-icon.ps1 -Sfx <7zSD.Win32.sfx d'origine> -Ico <setup.ico> -Out <fichier de sortie>
#>
param(
    [Parameter(Mandatory)] [string] $Sfx,
    [Parameter(Mandatory)] [string] $Ico,
    [Parameter(Mandatory)] [string] $Out
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$rcedit = Join-Path $env:TEMP "rcedit-x64.exe"
if (-not (Test-Path $rcedit)) {
    Invoke-WebRequest "https://github.com/electron/rcedit/releases/download/v2.0.0/rcedit-x64.exe" -OutFile $rcedit
}
Copy-Item $Sfx $Out -Force
& $rcedit $Out --set-icon $Ico `
    --set-version-string ProductName "Mimir" `
    --set-version-string FileDescription "Installeur de Mimir" `
    --set-version-string CompanyName "Mimir" `
    --set-version-string LegalCopyright "MPL-2.0"
if ($LASTEXITCODE -ne 0) { throw "rcedit a echoue : $LASTEXITCODE" }
"ecrit $Out ($((Get-Item $Out).Length) octets)"
