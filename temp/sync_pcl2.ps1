# PCL2 libraries -> Gradle modules-2 cache sync script
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$pclLibraries = "D:\我的世界mod\.minecraft\libraries"
$pclVersions = "D:\我的世界mod\.minecraft\versions"
$gradleModules = "C:\Users\Administrato\.gradle\caches\modules-2\files-2.1"

Write-Host "=== PCL2 -> Gradle Cache Sync ===" -ForegroundColor Cyan

function Get-SHA1($file) {
    $sha1 = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha1.ComputeHash([System.IO.File]::ReadAllBytes($file))
    $sha1.Dispose()
    return [BitConverter]::ToString($bytes).Replace("-", "").ToLower()
}

function Copy-ToGradleCache($jarPath, $groupPath, $artifact, $version) {
    if (-not (Test-Path $jarPath)) { return $false }

    $sha1 = Get-SHA1 $jarPath
    $destDir = Join-Path $gradleModules "$groupPath\$artifact\$version\$sha1"

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    $destFile = Join-Path $destDir "$artifact-$version.jar"
    if (-not (Test-Path $destFile)) {
        Copy-Item $jarPath $destFile -Force
        $sizeKB = [math]::Round((Get-Item $jarPath).Length/1KB, 0)
        Write-Host "  [ADD] $artifact-$version.jar ($sizeKB KB)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [SKIP] $artifact-$version.jar" -ForegroundColor Gray
        return $false
    }
}

$copied = 0
$skipped = 0

Write-Host ""
Write-Host "--- Syncing libraries ---" -ForegroundColor Yellow
$allJars = Get-ChildItem $pclLibraries -Recurse -Filter "*.jar" -ErrorAction SilentlyContinue
Write-Host "Found $($allJars.Count) jars in PCL2"
Write-Host ""

foreach ($jar in $allJars) {
    $relPath = $jar.FullName.Substring($pclLibraries.Length + 1)
    $parts = $relPath -split '\\'

    if ($parts.Count -ge 4) {
        $version = $parts[-2]
        $artifact = $parts[-3]
        $groupParts = $parts[0..($parts.Count - 4)]
        $groupPath = $groupParts -join '\'

        $result = Copy-ToGradleCache $jar.FullName $groupPath $artifact $version
        if ($result) { $copied++ } else { $skipped++ }
    }
}

Write-Host ""
Write-Host "--- Syncing Minecraft client.jar ---" -ForegroundColor Yellow

$clientJars = Get-ChildItem $pclVersions -Recurse -Filter "*.jar" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "*1.20.1*" -and $_.Length -gt 5MB } |
    Sort-Object Length -Descending

if ($clientJars) {
    $clientJar = $clientJars[0]
    $sizeMB = [math]::Round($clientJar.Length / 1MB, 1)
    Write-Host "Found: $($clientJar.Name) ($sizeMB MB)"
    $result = Copy-ToGradleCache $clientJar.FullName "com\mojang" "minecraft" "1.20.1"
    if ($result) { $copied++ }
} else {
    Write-Host "No 1.20.1 client.jar found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host "Added: $copied, Skipped: $skipped"
