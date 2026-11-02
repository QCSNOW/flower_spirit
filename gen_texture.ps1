Add-Type -AssemblyName System.Drawing

$src = "D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_crystal_gen.jpg"
$dst = "D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_crystal.png"

$srcBmp = [System.Drawing.Bitmap]::FromFile($src)

# 裁剪中心 55% 区域
$cx = $srcBmp.Width / 2
$cy = $srcBmp.Height / 2
$size = [int]($srcBmp.Width * 0.55)
$cropRect = New-Object System.Drawing.Rectangle($cx - $size/2, $cy - $size/2, $size, $size)
$cropped = $srcBmp.Clone($cropRect, $srcBmp.PixelFormat)

# 缩放到 16x16
$small = New-Object System.Drawing.Bitmap(16, 16, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($small)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
$g.DrawImage($cropped, 0, 0, 16, 16)
$g.Dispose()

# 白色背景变透明
for ($y = 0; $y -lt 16; $y++) {
    for ($x = 0; $x -lt 16; $x++) {
        $c = $small.GetPixel($x, $y)
        if ($c.R -gt 220 -and $c.G -gt 220 -and $c.B -gt 220) {
            $small.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, $c.R, $c.G, $c.B))
        }
    }
}

$small.Save($dst, [System.Drawing.Imaging.ImageFormat]::Png)
$small.Dispose()
$cropped.Dispose()
$srcBmp.Dispose()

Write-Host "繁花结晶贴图已生成: $dst"
