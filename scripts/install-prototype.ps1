<#
  Mimir - installe la configuration prototype (phase 0) dans un Firefox existant.
  Copie distribution\ vers le dossier d'installation de Firefox. Droits admin requis.
  Usage : .\install-prototype.ps1 [-FirefoxDir "C:\Program Files\Mozilla Firefox"] [-Yes]
  Pour annuler : supprimer <Firefox>\distribution\policies.json,
  <Firefox>\defaults\pref\autoconfig.js et <Firefox>\mimir.cfg.
#>
param(
    [string]$FirefoxDir = "C:\Program Files\Mozilla Firefox",
    [switch]$Yes
)

$ErrorActionPreference = "Stop"
$src = Join-Path (Split-Path $PSScriptRoot -Parent) "distribution"

if (-not (Test-Path (Join-Path $FirefoxDir "firefox.exe"))) {
    throw "firefox.exe introuvable dans '$FirefoxDir'. Installe Firefox ESR ou passe -FirefoxDir."
}

$files = @(
    @{ From = "policies.json";               To = "distribution\policies.json" },
    @{ From = "defaults\pref\autoconfig.js"; To = "defaults\pref\autoconfig.js" },
    @{ From = "mimir.cfg";                   To = "mimir.cfg" }
)

Write-Host "Mimir va copier dans '$FirefoxDir' :"
foreach ($f in $files) { Write-Host "  $($f.From) -> $($f.To)" }
if (-not $Yes) {
    $answer = Read-Host "Continuer ? (o/N)"
    if ($answer -notin @("o", "O", "y", "Y")) { Write-Host "Annule."; exit 1 }
}

foreach ($f in $files) {
    $dest = Join-Path $FirefoxDir $f.To
    New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent) | Out-Null
    Copy-Item -Force (Join-Path $src $f.From) $dest
}
Write-Host "Termine. Relance Firefox puis verifie about:policies et about:addons."
