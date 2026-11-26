# Đưa bản web mới lên GitHub Pages (repo KD.IACHIM.TDMAP, nhánh main) trong 1 lệnh:
#   1. (mặc định) đẩy mã nguồn đã commit lên nhánh "source"
#   2. chạy dong_goi_github.ps1 để tạo lại thư mục github\
#   3. clone nhánh main vào thư mục tạm, thay toàn bộ nội dung bằng github\, commit, push
#
# Chạy:  powershell -ExecutionPolicy Bypass -File day_len_github.ps1
#        powershell -ExecutionPolicy Bypass -File day_len_github.ps1 -Message "Sửa màu thửa đất"
# Tham số:
#   -Message "..."   nội dung commit trên nhánh main (mặc định: lấy theo commit mới nhất của mã nguồn)
#   -KhongDayNguon   không đẩy nhánh source
#   -ChoPhepChuaCommit  vẫn đưa lên khi RKD_IACHIM.html còn sửa chưa commit (mặc định: dừng lại)
param(
    [string]$Message = '',
    [switch]$KhongDayNguon,
    [switch]$ChoPhepChuaCommit
)
$ErrorActionPreference = 'Stop'
$src = $PSScriptRoot
$repoUrl = 'https://github.com/taido990/KD.IACHIM.TDMAP.git'
$pagesUrl = 'https://taido990.github.io/KD.IACHIM.TDMAP/'
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Gọi git, dừng khi lỗi (không dùng 2>&1 vì PowerShell 5.1 coi stderr của git là lỗi)
function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    $old = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    & git @GitArgs
    $code = $LASTEXITCODE; $ErrorActionPreference = $old
    if ($code -ne 0) { throw "git $($GitArgs -join ' ') thất bại (mã $code)" }
}
function Get-GitOut {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    $old = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $o = & git @GitArgs
    $code = $LASTEXITCODE; $ErrorActionPreference = $old
    if ($code -ne 0) { throw "git $($GitArgs -join ' ') thất bại (mã $code)" }
    return $o
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Không tìm thấy git trong PATH' }
Push-Location $src
try {
    # 1. Kiểm tra mã nguồn
    $dirty = Get-GitOut status --porcelain
    if ($dirty) {
        Write-Host 'Mã nguồn còn thay đổi chưa commit:' -ForegroundColor Yellow
        $dirty | ForEach-Object { Write-Host "  $_" }
        if (($dirty | Where-Object { $_ -match 'RKD_IACHIM\.html|README_github\.md|manifest\.json|sw\.js|icon|\.ico' }) -and -not $ChoPhepChuaCommit) {
            throw 'File của trang web chưa commit — hãy commit trước (hoặc chạy lại với -ChoPhepChuaCommit)'
        }
    }
    $srcHash = (Get-GitOut rev-parse --short HEAD) | Select-Object -First 1
    $srcSubj = (Get-GitOut log -1 --format=%s) | Select-Object -First 1

    if (-not $KhongDayNguon) {
        Write-Host "`n[1/3] Đẩy mã nguồn lên nhánh source..." -ForegroundColor Cyan
        Invoke-Git push origin refs/heads/main:refs/heads/source
    }

    # 2. Đóng gói
    Write-Host "`n[2/3] Đóng gói thư mục github\..." -ForegroundColor Cyan
    & (Join-Path $src 'dong_goi_github.ps1')
    $pkg = Join-Path $src 'github'
    if (-not (Test-Path (Join-Path $pkg 'index.html'))) { throw 'Thiếu github\index.html sau khi đóng gói' }
}
finally { Pop-Location }

# 3. Đưa lên nhánh main
Write-Host "`n[3/3] Đưa github\ lên nhánh main..." -ForegroundColor Cyan
$tmp = Join-Path $env:TEMP ('kd_iachim_pages_' + [guid]::NewGuid().ToString('N').Substring(0, 8))
try {
    Invoke-Git clone -q --depth 1 --branch main $repoUrl $tmp
    Push-Location $tmp
    try {
        # Thay toàn bộ nội dung (giữ .git) bằng gói mới — file đã xoá khỏi gói cũng bị xoá trên trang
        Get-ChildItem -Force $tmp | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force
        Get-ChildItem -Force $pkg | Copy-Item -Destination $tmp -Recurse -Force
        Invoke-Git add -A
        $changes = Get-GitOut status --porcelain
        if (-not $changes) {
            Write-Host "`nTrang trên GitHub đã giống bản mới — không có gì để đẩy." -ForegroundColor Green
            return
        }
        Write-Host 'Thay đổi:'; $changes | ForEach-Object { Write-Host "  $_" }
        if (-not $Message) { $Message = "$srcSubj (nguồn $srcHash)" }
        # Ghi nội dung commit ra file UTF-8 để giữ dấu tiếng Việt (truyền qua tham số dòng lệnh dễ lỗi mã hoá)
        $msgFile = Join-Path $env:TEMP 'kd_iachim_commit_msg.txt'
        [IO.File]::WriteAllText($msgFile, $Message + "`n", $utf8)
        Invoke-Git commit -q -F $msgFile
        Remove-Item $msgFile -Force
        Invoke-Git push origin main
        $h = (Get-GitOut rev-parse --short HEAD) | Select-Object -First 1
        Write-Host "`nXong: nhánh main = $h. Trang cập nhật sau 1–2 phút: $pagesUrl" -ForegroundColor Green
    }
    finally { Pop-Location }
}
finally {
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
}
