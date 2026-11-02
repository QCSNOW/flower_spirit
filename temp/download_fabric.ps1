# Multi-threaded Fabric maven downloader
# Downloads all required Fabric packages in parallel and puts them in Gradle cache

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$baseUrl = "https://maven.fabricmc.net"
$cacheDir = "C:\Users\Administrato\.gradle\caches\modules-2\files-2.1"
$tempDir = "D:\mcmod\mytestmod\temp\dl"
$maxThreads = 6

if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

# Package list: group, artifact, version, [classifier]
$packages = @(
    # Loom plugin + tools (build-time)
    @{ G="net.fabricmc"; A="fabric-loom"; V="1.4.1" },
    @{ G="net.fabricmc"; A="mercury"; V="0.4.0" },
    @{ G="net.fabricmc"; A="stitch"; V="0.6.2" },
    @{ G="net.fabricmc"; A="tiny-remapper"; V="0.8.9" },
    @{ G="net.fabricmc"; A="access-widener"; V="2.1.0" },
    @{ G="net.fabricmc"; A="mapping-io"; V="0.4.2" },
    @{ G="net.fabricmc"; A="lorenz-tiny"; V="4.0.2" },
    @{ G="net.fabricmc"; A="sponge-mixin"; V="0.12.5+mixin.0.8.5" },
    # Project dependencies
    @{ G="net.fabricmc"; A="fabric-loader"; V="0.15.11" },
    @{ G="net.fabricmc"; A="yarn"; V="1.20.1+build.1"; C="v2" },
    @{ G="net.fabricmc"; A="intermediary"; V="1.20.1" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-api"; V="0.92.1+1.20.1" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-api-base"; V="0.4.29+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-biome-api-v1"; V="13.0.2+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-block-api-v1"; V="10.3.3+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-blockrenderlayer-v1"; V="1.1.39+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-client-tags-api-v1"; V="1.1.1+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-command-api-v2"; V="2.2.11+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-content-registries-v0"; V="4.0.7+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-crash-report-info-v1"; V="2.0.14+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-data-generation-api-v1"; V="12.1.7+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-dimensions-v1"; V="2.1.50+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-entity-events-v1"; V="1.5.20+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-events-interaction-v0"; V="0.4.34+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-events-lifecycle-v0"; V="0.2.60+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-game-rule-api-v1"; V="3.0.23+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-gametest-api-v1"; V="1.2.13+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-item-api-v1"; V="2.1.24+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-item-group-api-v1"; V="4.0.9+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-key-binding-api-v1"; V="1.0.35+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-lifecycle-events-v1"; V="2.2.20+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-loot-api-v2"; V="1.1.37+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-mining-level-api-v1"; V="2.1.46+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-model-loading-api-v1"; V="1.0.3+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-networking-api-v1"; V="1.3.8+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-object-builder-api-v1"; V="11.1.0+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-particles-v1"; V="1.1.1+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-recipe-api-v1"; V="1.6.13+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-registry-sync-v0"; V="2.2.8+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-renderer-api-v1"; V="3.1.1+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-renderer-indigo"; V="1.4.1+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-rendering-fluids-v1"; V="3.0.27+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-rendering-v1"; V="3.0.6+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-resource-conditions-api-v1"; V="2.3.5+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-resource-loader-v0"; V="0.11.7+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-screen-api-v1"; V="2.0.7+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-sound-api-v1"; V="1.0.11+4a21948677" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-transfer-api-v1"; V="3.2.3+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-transitive-access-wideners-v1"; V="4.2.0+77f1c7b377" },
    @{ G="net.fabricmc.fabric-api"; A="fabric-weakeners"; V="1.0.0+77f1c7b377" }
)

Write-Host "=== Fabric Multi-thread Downloader ===" -ForegroundColor Cyan
Write-Host "Packages to download: $($packages.Count)"
Write-Host "Threads: $maxThreads"
Write-Host ""

# Download function for a single package (runs in job)
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
    
    $groupCachePath = $group -replace '\', '\'
    $groupCachePath = $group -replace '\.', '\'
    
    function Copy-ToCache($filePath, $ext) {
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
        
        $baseName = if ($classifier -and $ext -eq "jar") { "$artifact-$version-$classifier" } else { "$artifact-$version" }
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
    $jarTemp = Join-Path $tempDir "$artifact-$version.jar"
    try {
        Invoke-WebRequest -Uri $jarUrl -OutFile $jarTemp -UseBasicParsing -TimeoutSec 600 -ErrorAction Stop
        if (Copy-ToCache $jarTemp "jar") { $added++ }
    } catch {
        $failed++
        Write-Output "FAIL jar: $artifact-$version - $($_.Exception.Message)"
    }
    
    # Download POM
    $pomTemp = Join-Path $tempDir "$artifact-$version.pom"
    try {
        Invoke-WebRequest -Uri $pomUrl -OutFile $pomTemp -UseBasicParsing -TimeoutSec 300 -ErrorAction Stop
        if (Copy-ToCache $pomTemp "pom") { $added++ }
    } catch {
        $failed++
        Write-Output "FAIL pom: $artifact-$version - $($_.Exception.Message)"
    }
    
    Write-Output "DONE: $artifact-$version (added=$added, failed=$failed)"
}

# Clean up old jobs
Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue

$active = 0
$completed = 0
$total = $packages.Count

foreach ($pkg in $packages) {
    # Wait if we have too many active jobs
    while ($active -ge $maxThreads) {
        Start-Sleep -Seconds 3
        $running = Get-Job -State Running | Measure-Object | ForEach-Object { $_.Count }
        $active = $running
    }
    
    # Start new job
    $null = Start-Job -ScriptBlock $downloadFunc -ArgumentList $pkg, $baseUrl, $cacheDir, $tempDir
    $active++
    Write-Host "  [START] $($pkg.A)-$($pkg.V) (active: $active/$maxThreads)"
}

# Wait for all jobs to finish
Write-Host ""
Write-Host "Waiting for all downloads to finish..." -ForegroundColor Yellow

while ((Get-Job -State Running).Count -gt 0) {
    Start-Sleep -Seconds 5
    
    # Print completed jobs output
    $doneJobs = Get-Job -State Completed
    foreach ($job in $doneJobs) {
        $output = Receive-Job $job
        $output | ForEach-Object { Write-Host "  $_" }
        Remove-Job $job
        $completed++
    }
    
    $running = (Get-Job -State Running).Count
    Write-Host "Progress: $completed/$total done, $running running" -ForegroundColor Cyan
}

# Final check
$remaining = Get-Job
foreach ($job in $remaining) {
    $output = Receive-Job $job
    $output | ForEach-Object { Write-Host "  $_" }
    Remove-Job $job
    $completed++
}

Write-Host ""
Write-Host "=== ALL DONE: $completed/$total ===" -ForegroundColor Green
