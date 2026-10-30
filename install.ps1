# Instala la skill docs-a-medida en Claude Code y/o Codex CLI (Windows).
# Uso:  powershell -ExecutionPolicy Bypass -File install.ps1
#       powershell -ExecutionPolicy Bypass -File install.ps1 -Destino "C:\otra\carpeta\skills"
param([string]$Destino = "")

$ErrorActionPreference = "Stop"
$nombre = "docs-a-medida"
$origen = $PSScriptRoot
$archivos = @("SKILL.md", "references", "templates", "scripts")

$destinos = @()
if ($Destino) {
    $destinos += $Destino
} else {
    if (Test-Path "$HOME\.claude") { $destinos += "$HOME\.claude\skills" }
    if (Test-Path "$HOME\.codex")  { $destinos += "$HOME\.codex\skills" }
}
if ($destinos.Count -eq 0) {
    Write-Host "No se encontro Claude Code (~\.claude) ni Codex (~\.codex)."
    Write-Host "Indica la carpeta de skills de tu agente con:  install.ps1 -Destino <carpeta>"
    exit 1
}

foreach ($base in $destinos) {
    $carpeta = Join-Path $base $nombre
    New-Item -ItemType Directory -Force -Path $carpeta | Out-Null
    foreach ($item in $archivos) {
        Copy-Item -Path (Join-Path $origen $item) -Destination $carpeta -Recurse -Force
    }
    Write-Host "Instalada en $carpeta"
}

# Dependencia del generador de PDF (opcional: sin ella la skill igual redacta en Markdown).
$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
if ($python) {
    & $python.Source -m pip install --quiet --user markdown
    Write-Host "Paquete markdown de Python instalado."
} else {
    Write-Host "No se encontro Python: la skill funciona, pero para generar PDF instala Python y ejecuta 'pip install markdown'."
}
Write-Host "Listo. Reinicia tu agente y pidele un documento."
