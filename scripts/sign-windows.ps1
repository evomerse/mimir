<#
Signe les executables et DLL Windows de Mimir avec signtool (Authenticode, SHA-256, horodatage).

  -Path : un fichier (.exe, .dll, .msi), ou un dossier signe recursivement.

Variables d'environnement : MIMIR_SIGN_PFX (chemin du .pfx), MIMIR_SIGN_PASSWORD.
Smart App Control laisse passer les binaires signes par une autorite de confiance pour Windows ;
SmartScreen peut en plus exiger de la reputation (a verifier au moment du choix du certificat :
l'avantage automatique des certificats EV a ete retire). Azure Trusted Signing est une alternative
sans fichier .pfx.
Non teste ici : pas de certificat. Voir docs/BUILD.md.
#>
param([Parameter(Mandatory = $true)][string]$Path)
$ErrorActionPreference = "Stop"

if (-not $env:MIMIR_SIGN_PFX) { throw "MIMIR_SIGN_PFX n'est pas defini" }
$signtool = (Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\signtool.exe" |
    Sort-Object FullName -Descending | Select-Object -First 1).FullName
if (-not $signtool) { throw "signtool.exe introuvable (Windows SDK)" }

$timestamp = if ($env:MIMIR_SIGN_TIMESTAMP) { $env:MIMIR_SIGN_TIMESTAMP } else { "http://timestamp.digicert.com" }

if (Test-Path $Path -PathType Container) {
    $files = Get-ChildItem $Path -Recurse -Include *.exe, *.dll | Select-Object -ExpandProperty FullName
} else {
    $files = @((Resolve-Path $Path).Path)
}

# Les fichiers deja signes (DLL de Microsoft, par exemple) sont laisses tels quels.
$todo = $files | Where-Object { (Get-AuthenticodeSignature $_).Status -eq "NotSigned" }
Write-Host "signature de $($todo.Count) fichier(s) sur $($files.Count)"

$signArgs = @("sign", "/fd", "SHA256", "/td", "SHA256", "/tr", $timestamp, "/f", $env:MIMIR_SIGN_PFX)
if ($env:MIMIR_SIGN_PASSWORD) { $signArgs += @("/p", $env:MIMIR_SIGN_PASSWORD) }

# Par lots, pour ne pas depasser la longueur maximale d'une ligne de commande.
for ($i = 0; $i -lt $todo.Count; $i += 50) {
    $batch = $todo[$i..([Math]::Min($i + 49, $todo.Count - 1))]
    & $signtool @signArgs @batch
    if ($LASTEXITCODE -ne 0) { throw "signtool a echoue (code $LASTEXITCODE)" }
}
