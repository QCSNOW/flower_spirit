# Multi-threaded Fabric maven downloader - Phase 1: Core packages
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$baseUrl = "https://maven.fabricmc.net"
$cacheDir = "C:\Users\Administrato\.gradle\caches\modules-2\files-2.1"
$tempDir = "D:\mcmod\mytestmod\temp\dl"
$maxThreads = 6

if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

# Core packages with known versions
$packages = @(
    @{ G="net.fabricmc"; A="fabric-loom"; V="1.4.1" },
    @{ G="net.fabricmc"; A="mercury"; V="0.4.0" },
    @{ G="net.fabricmc"; A="stitch"; V="0.6.2" },
    @{ G="net.fabricmc"; A="tiny-remapper"; V="0.8.9" },
    @{ G="net.fabricmc"; A="access-widener"; V="2.1.0" },
    @{ G="net.fabricmc"; A="mapping-io"; V="0.4.2" },
    @{ G="net.fabricmc"; A="lorenz-tiny"; V="4.0.2" },
    @{ G="net.fabricmc"; A="sponge-mixin"; V="0.12.5+mixin.0.8.5" },
    @{ G="net.fabricmc"; A="fabric-loader"; V="0.15.11" },
    @{ G="net.fabricmc"; A="yarn"; V="1.20.1+build.1"; C="v2" },
    @{ G="net.fabricmc"; A="intermediary"; V="1.20.1" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-api"; V="0.92.1+1.20.1" }
)

Write-Host "=== Phase 1: Core Fabric Packages ===" -ForegroundColor Cyan
Write-Host "Packages: $($packages.Count), Threads: $maxThreads"
Write-Host ""

$downloadFunc = {
    param($pkg, $baseUrl, $cacheDir, $tempDir)
    
    $group = $pkg.G
    $artifact = $pkg.A
    $version = $pkg.V
    $classifier = $pkg.C
    
    $groupPath = $group -replace '\.', '/'
    $jarName = if ($classifier) { "$artifact-$version-$classifier.jar" } else { "$artifact-$version.jar" }
    $pomName = "$artifact-$version.pom"
    
    $jarUrl = "$baseUrl/$groupPath/$artifact/$version/$jarName"
    $pomUrl = "$baseUrl/$groupPath/$artifact/$version/$pomName"
    
    $groupCachePath = $group -replace '\.', '\'
    
    function Copy-ToCache($filePath, $baseName, $ext) {
        if (-not (Test-Path $filePath)) { return $false }
        $fi = Get-Item $filePath
        if ($fi.Length -eq 0) { return $false }
        
        $sha1 = [System.Security.Cryptography.SHA1]::Create()
        $bytes = $sha1.ComputeHash([System.IO.File]::ReadAllBytes($filePath))
        $sha1.Dispose()
        $hash = [BitConverter]::ToString($bytes).Replace("-", "").ToLower()
        
        $destDir = Join-Path $cacheDir "$groupCachePath\$artifact\$version\$hash"
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        $destFile = Join-Path $destDir "$baseName.$ext"
        if (-not (Test-Path $destFile)) {
            Copy-Item $filePath $destFile -Force
            return $true
        }
        return $false
    }
    
    $added = 0
    $failed = 0
    
    # Download JAR
    $jarBase = if ($classifier) { "$artifact-$version-$classifier" } else { "$artifact-$version" }
    $jarTemp = Join-Path $tempDir "$jarBase.jar"
    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        Invoke-WebRequest -Uri $jarUrl -OutFile $jarTemp -UseBasicParsing -TimeoutSec 600 -ErrorAction Stop
        $sw.Stop()
        $sizeKB = [math]::Round((Get-Item $jarTemp).Length / 1KB, 1)
        if (Copy-ToCache $jarTemp $jarBase "jar") { 
            $added++ 
            "OK JAR: $artifact-$version ($sizeKB KB, $([math]::Round($sw.Elapsed.TotalSeconds,1))s)"
        } else {
            "SKIP JAR: $artifact-$version"
        }
    } catch {
        $failed++
        "FAIL JAR: $artifact-$version - $($_.Exception.Message.Substring(0, [Math]::Min(80, $_.Exception.Message.Length)))"
    }
    
    # Download POM
    $pomBase = "$artifact-$version"
    $pomTemp = Join-Path $tempDir "$pomBase.pom"
    try {
        Invoke-WebRequest -Uri $pomUrl -OutFile $pomTemp -UseBasicParsing -TimeoutSec 300 -ErrorAction Stop
        if (Copy-ToCache $pomTemp $pomBase "pom") { $added++ }
    } catch {
        $failed++
        "FAIL POM: $artifact-$version"
    }
    
    "DONE: $artifact-$version (added=$added, failed=$failed)"
}

# Clean old jobs
Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue

$active = 0
$total = $packages.Count
$started = 0

foreach ($pkg in $packages) {
    while ($active -ge $maxThreads) {
        Start-Sleep -Seconds 2
        $active = (Get-Job -State Running | Measure-Object).Count
        
        # Collect completed
        $doneJobs = Get-Job -State Completed
        foreach ($job in $doneJobs) {
            $out = Receive-Job $job
            $out | ForEach-Object { "  $_" }
            Remove-Job $job
        }
    }
    
    Start-Job -ScriptBlock $downloadFunc -ArgumentList $pkg, $baseUrl, $cacheDir, $tempDir | Out-Null
    $started++
    $active++
    "  [START $started/$total] $($pkg.A)-$($pkg.V)"
}

Write-Host ""
Write-Host "All started. Waiting for completion..." -ForegroundColor Yellow
Write-Host ""

$prevCount = 0
while ((Get-Job).Count -gt 0) {
    Start-Sleep -Seconds 5
    
    $doneJobs = Get-Job -State Completed
    foreach ($job in $doneJobs) {
        $out = Receive-Job $job
        $out | ForEach-Object { Write-Host "  $_" }
        Remove-Job $job
    }
    
    $running = (Get-Job -State Running).Count
    $done = $total - $running - (Get-Job -State Running).Count
    Write-Host "Running: $running, Remaining: $running" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== PHASE 1 COMPLETE ===" -ForegroundColor Green
