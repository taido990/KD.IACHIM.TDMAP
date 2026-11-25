# Đóng gói RKD_IACHIM.html thành thư mục "github" (index.html + manifest + sw.js + icon) để đưa lên GitHub Pages (repo KD.IACHIM.TDMAP).
# Chạy lại mỗi khi sửa RKD_IACHIM.html:  powershell -ExecutionPolicy Bypass -File dong_goi_github.ps1
$ErrorActionPreference = 'Stop'
$src = $PSScriptRoot
$out = Join-Path $src 'github'
$utf8 = New-Object System.Text.UTF8Encoding($false)   # UTF-8 không BOM

New-Item -ItemType Directory -Force $out | Out-Null

# index.html = RKD_IACHIM.html (đã có sẵn khai báo manifest / icon / service worker để cài lên màn hình chính)
$html = [IO.File]::ReadAllText((Join-Path $src 'RKD_IACHIM.html'), $utf8)
if ($html -notmatch 'rel="manifest"') { throw 'RKD_IACHIM.html thiếu <link rel="manifest"> — không cài được lên màn hình chính' }
[IO.File]::WriteAllText((Join-Path $out 'index.html'), $html, $utf8)

# Các file phục vụ cài đặt ra màn hình chính (PWA)
$pwa = 'manifest.json', 'sw.js', 'app-icon.ico', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'
foreach ($f in $pwa) { Copy-Item (Join-Path $src $f) $out -Force }
# GitHub Pages: không xử lý Jekyll, phục vụ nguyên file
[IO.File]::WriteAllText((Join-Path $out '.nojekyll'), '', $utf8)
Copy-Item (Join-Path $src 'README_github.md') (Join-Path $out 'README.md') -Force

Get-ChildItem -Force $out | Select-Object Name, Length | Format-Table -AutoSize
Write-Host "Xong: $out"
