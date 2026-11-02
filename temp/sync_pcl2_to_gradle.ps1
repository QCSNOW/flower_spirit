# ===================== PCL2 → Gradle 缓存同步脚本 =====================
# 把 PCL2 里已有的 Minecraft + Fabric 库文件复制到 Gradle 缓存
# 这样 Loom 就不用从国外慢下载了
# =====================================================================

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# ---- 路径配置 ----
$pclLibraries = "D:\我的世界mod\.minecraft\libraries"
$pclVersions = "D:\我的世界mod\.minecraft\versions"
$gradleModules = "C:\Users\Administrato\.gradle\caches\modules-2\files-2.1"
$gradleJars = "C:\Users\Administrato\.gradle\caches\jars-9"

Write-Host "=== PCL2 -> Gradle 缓存同步 ===" -ForegroundColor Cyan
Write-Host "PCL libraries: $pclLibraries"
Write-Host "Gradle cache:   $gradleModules"
Write-Host ""

# ---- 计算文件哈希（Gradle 用 SHA1 做路径） ----
function Get-SHA1($file) {
    $sha1 = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha1.ComputeHash([System.IO.File]::ReadAllBytes($file))
    $sha1.Dispose()
    return [BitConverter]::ToString($bytes).Replace("-", "").ToLower()
}

# ---- 复制单个 jar 到 Gradle modules-2 缓存 ----
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
        Write-Host "  [OK] $artifact-$version.jar ($([math]::Round((Get-Item $jarPath).Length/1KB,0))KB)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [已有] $artifact-$version.jar" -ForegroundColor Gray
        return $false
    }
}

# ---- 同步 PCL2 libraries 里的所有 jar ----
$copied = 0
$skipped = 0

Write-Host "--- 同步 libraries ---" -ForegroundColor Yellow

# 遍历 PCL2 的 libraries 目录
$allJars = Get-ChildItem $pclLibraries -Recurse -Filter "*.jar" -ErrorAction SilentlyContinue
Write-Host "PCL2 中找到 $($allJars.Count) 个 jar 文件"
Write-Host ""

foreach ($jar in $allJars) {
    # 从路径解析 group:artifact:version
    # 路径格式: libraries\net\fabricmc\fabric-loader\0.19.5\fabric-loader-0.19.5.jar
    $relPath = $jar.FullName.Substring($pclLibraries.Length + 1)
    $parts = $relPath -split '\\'

    if ($parts.Count -ge 4) {
        $version = $parts[-2]
        $artifact = $parts[-3]
        $groupParts = $parts[0..($parts.Count - 4)]
        $group = $groupParts -join '.'
        $groupPath = $groupParts -join '\'

        $result = Copy-ToGradleCache $jar.FullName $groupPath $artifact $version
        if ($result) { $copied++ } else { $skipped++ }
    }
}

Write-Host ""
Write-Host "同步完成: 新增 $copied 个, 跳过 $skipped 个" -ForegroundColor Cyan

# ---- 也把 Minecraft client.jar 放进去（Loom 需要） ----
Write-Host ""
Write-Host "--- 同步 Minecraft client.jar ---" -ForegroundColor Yellow

$clientJar = Get-ChildItem $pclVersions -Recurse -Filter "*.jar" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "*1.20.1*" } |
    Sort-Object Length -Descending |
    Select-Object -First 1

if ($clientJar) {
    Write-Host "找到: $($clientJar.Name) ($([math]::Round($clientJar.Length/1MB,1))MB)"
    $result = Copy-ToGradleCache $clientJar.FullName "com\mojang" "minecraft" "1.20.1"
    if ($result) { $copied++ }
} else {
    Write-Host "未找到 1.20.1 client.jar" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== 全部完成 ===" -ForegroundColor Cyan
Write-Host "共新增 $copied 个 jar 到 Gradle 缓存"
