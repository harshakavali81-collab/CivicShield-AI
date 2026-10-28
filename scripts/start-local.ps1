<#
.SYNOPSIS
  Safely prepare a local CivicShield AI Docker demo on Windows.
.DESCRIPTION
  Generates a local-only PostgreSQL password if none exists, never overwrites
  an existing nonempty secret, and starts the LOCAL research demo only.
  Requires installed Docker Desktop with Compose and Linux containers.
.EXAMPLE
  powershell -File .\scripts\start-local.ps1
.EXAMPLE
  pwsh -File .\scripts\start-local.ps1 -PrepareOnly
#>
[CmdletBinding()]
param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    $envPath = Join-Path $repo '.env'
    $example = Join-Path $repo '.env.example'
    if (-not (Test-Path $example)) { throw 'Missing .env.example in repository.' }
    if (-not (Test-Path $envPath)) {
        Copy-Item -LiteralPath $example -Destination $envPath
        Write-Host 'Created gitignored local .env from .env.example.'
    }
    $raw = [System.IO.File]::ReadAllText($envPath)
    $present = [regex]::Match($raw, '(?m)^POSTGRES_PASSWORD=(.*)$')
    if (-not $present.Success -or [string]::IsNullOrWhiteSpace($present.Groups[1].Value)) {
        $bytes = New-Object byte[] 24
        $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        try { $generator.GetBytes($bytes) } finally { $generator.Dispose() }
        $password = ([BitConverter]::ToString($bytes)).Replace('-', '').ToLowerInvariant()
        if ($present.Success) {
            $raw = [regex]::Replace($raw, '(?m)^POSTGRES_PASSWORD=.*$', "POSTGRES_PASSWORD=$password")
        } else {
            $raw = $raw.TrimEnd() + [Environment]::NewLine + "POSTGRES_PASSWORD=$password" + [Environment]::NewLine
        }
        $encoding = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($envPath, $raw, $encoding)
        Write-Host 'Generated a private local database password. The value is not displayed.'
    } else {
        if ($present.Groups[1].Value.Length -lt 24) {
            throw 'Existing local POSTGRES_PASSWORD is too short; set a stronger private value (24+ characters) in .env.'
        }
        Write-Host 'Retaining the existing local database password.'
    }
    if ($PrepareOnly) {
        Write-Host 'Preparation complete. Run docker compose up --build -d when ready.'
        exit 0
    }
    docker compose version | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose is not available. Install/start Docker Desktop.' }
    docker compose up --build -d --wait --wait-timeout 120
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose startup failed; run docker compose logs for details.' }
    Write-Host 'Local research demo containers started and reported healthy.'
    Write-Host 'Dashboard: http://localhost:5173'
    Write-Host 'API docs: http://localhost:8000/docs'
    Write-Host 'Run python -m scripts.smoke_demo for read-only API checks if Python is installed.'
    Write-Host 'Important: This is NOT a real government alert or emergency service.'
} finally {
    Pop-Location
}
