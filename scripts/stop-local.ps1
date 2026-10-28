<#
.SYNOPSIS
  Stop local CivicShield AI Docker containers without deleting database volumes.
#>
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    docker compose down
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose shutdown failed.' }
    Write-Host 'Local demo stopped. The PostgreSQL volume was retained.'
    Write-Host 'Do NOT run docker compose down --volumes without an intentional backup.'
} finally {
    Pop-Location
}
