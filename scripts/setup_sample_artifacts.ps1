# ACA Runtime sample artifacts setup script
# This script extracts the bundled ACA v0.3 runtime artifacts into ./artifacts.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\scripts\setup_sample_artifacts.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$BundlePath = Join-Path $RepoRoot "artifacts_bundles\aca_artifacts_v0.3_runtime_bundle.zip"
$ArtifactsPath = Join-Path $RepoRoot "artifacts"

if (!(Test-Path $BundlePath)) {
    Write-Error "Artifacts bundle not found: $BundlePath"
    exit 1
}

if (Test-Path $ArtifactsPath) {
    Write-Host "Existing artifacts folder found: $ArtifactsPath"
    Write-Host "Removing existing artifacts folder before extraction..."
    Remove-Item $ArtifactsPath -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $ArtifactsPath | Out-Null

Write-Host "Extracting ACA artifacts bundle..."
Expand-Archive -Path $BundlePath -DestinationPath $ArtifactsPath -Force

$ManifestPath = Join-Path $ArtifactsPath "triaxial\manifest.json"

if (!(Test-Path $ManifestPath)) {
    Write-Error "Extraction finished, but triaxial manifest was not found: $ManifestPath"
    exit 1
}

Write-Host "ACA sample artifacts installed successfully."
Write-Host "Artifacts path: $ArtifactsPath"
Write-Host ""
Write-Host "Optional PowerShell environment variable:"
Write-Host "`$env:ACA_ARTIFACTS_PATH=`"$ArtifactsPath`""
Write-Host ""
Write-Host "Validation command:"
Write-Host "python -m aca_runtime.runtime.atlas_loader_v2"
