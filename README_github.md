# Khu vực đo Xã Ia Chim, tỉnh Quảng Ngãi - TDMAP.PRO.VN

WebGIS xem bản vẽ địa chính DGN trên nền ảnh vệ tinh, chạy hoàn toàn trên trình duyệt.

- Bản vẽ đọc trực tiếp từ thư mục Google Drive (Drive API v3, thư mục chia sẻ "Bất kỳ ai có đường liên kết").
- Lần đầu: giải mã DGN (V7/V8) → GeoJSON WGS-84, lưu đệm trên trình duyệt. Lần sau file không đổi → nạp GeoJSON, nhanh hơn.
- Hệ tọa độ mặc định VN-2000 múi 3°, KTT 108°00′ (xã Ia Chim, mã 23326, tỉnh Quảng Ngãi).
- Bảng bật/tắt lớp (nút ☰ Lớp), nút vị trí của tôi (GPS).

## Các file

| File | Vai trò |
|---|---|
| `index.html` | Toàn bộ ứng dụng (thư viện ký hiệu, bảng KTT, bộ đọc DGN đã nhúng sẵn) |
| `manifest.json`, `sw.js` | Khai báo ứng dụng + service worker (không lưu đệm) để cài lên màn hình chính |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` | Icon Android (bản maskable cho launcher cắt tròn / bo góc) |
| `apple-touch-icon.png`, `app-icon.ico` | Icon iPhone/iPad (nền trắng) và favicon trình duyệt |
| `.nojekyll` | GitHub Pages phục vụ nguyên file, không qua Jekyll |

## Cách tổ chức kho

Kho [KD.IACHIM.TDMAP](https://github.com/taido990/KD.IACHIM.TDMAP) có 2 nhánh:

| Nhánh | Nội dung |
|---|---|
| `main` | Trang web chạy trên GitHub Pages: chỉ các file ở bảng trên. **Không sửa tay**: script `day_len_github.ps1` ghi đè toàn bộ nhánh này. |
| `source` | Mã nguồn: `RKD_IACHIM.html`, `KTT_VN2000/`, `THUVIEN/`, `cong_cu/`, các script đóng gói… |

Trang chạy tại <https://taido990.github.io/KD.IACHIM.TDMAP/>. GitHub Pages chạy https nên nút vị trí (GPS) dùng được trên điện thoại.

## Cập nhật trang web (script `day_len_github.ps1`)

Mỗi lần sửa web, làm trong thư mục mã nguồn (`Web_RKD_IACHIM`):

1. Sửa `RKD_IACHIM.html` (hoặc icon, `manifest.json`, `sw.js`, `README_github.md`).
2. Commit:

   ```
   git add -A
   git commit -m "Mô tả thay đổi"
   ```

3. Chạy:

   ```
   powershell -ExecutionPolicy Bypass -File day_len_github.ps1
   ```

4. Sau 1–2 phút mở lại trang (trên điện thoại: kéo xuống để tải lại, hoặc đóng hẳn ứng dụng rồi mở lại).

Script làm lần lượt:

1. Đẩy mã nguồn đã commit lên nhánh `source`.
2. Chạy `dong_goi_github.ps1` để tạo lại thư mục `github\` (`index.html` = `RKD_IACHIM.html`, kèm manifest, service worker, icon, README này).
3. Lấy nhánh `main` về thư mục tạm, thay toàn bộ nội dung bằng `github\` (file đã bỏ khỏi gói cũng bị xoá trên trang), commit, push, rồi xoá thư mục tạm.

Nếu trang trên GitHub đã giống bản mới, script báo *"không có gì để đẩy"* và không tạo commit.

Tùy chọn:

| Tham số | Tác dụng |
|---|---|
| `-Message "Sửa màu thửa đất"` | Nội dung commit trên nhánh `main`. Mặc định lấy theo commit mới nhất của mã nguồn, kèm mã commit, ví dụ `Đổi KTT… (nguồn 0f8e1aa)`. |
| `-KhongDayNguon` | Bỏ qua bước đẩy nhánh `source`. |
| `-ChoPhepChuaCommit` | Vẫn đưa lên khi file của trang web còn sửa chưa commit. Mặc định script dừng lại, để trang web luôn khớp một commit trong lịch sử mã nguồn. |

Yêu cầu: máy có `git`, đã đăng nhập GitHub (lần push đầu tiên Git Credential Manager sẽ mở cửa sổ đăng nhập), và repo mã nguồn có remote `origin` trỏ tới kho trên.

Lần đầu nối repo mã nguồn trên máy mới:

```
git remote add origin https://github.com/taido990/KD.IACHIM.TDMAP.git
git config remote.origin.push refs/heads/main:refs/heads/source
```

Dòng thứ hai để lệnh `git push` không tham số luôn đẩy vào nhánh `source`, không ghi đè trang web.

## Tạo kho mới từ đầu (khi làm cho xã khác)

1. Tạo kho mới trên GitHub (Public), sửa `$repoUrl` và `$pagesUrl` đầu file `day_len_github.ps1`.
2. **Add file › Upload files** → kéo thả tất cả file trong thư mục `github\` (kể cả `.nojekyll`) → **Commit changes**. Sau đó dùng script như trên.
3. **Settings › Pages** → *Source*: **Deploy from a branch** → *Branch*: `main` / `/ (root)` → **Save**.
4. Sau 1–2 phút trang chạy tại `https://<tên-tài-khoản>.github.io/<tên-kho>/`.

## Cài lên màn hình chính

- **Android (Chrome):** mở trang › menu ⋮ › **Cài đặt ứng dụng** / **Thêm vào màn hình chính**.
- **iPhone (Safari):** mở trang › nút Chia sẻ › **Thêm vào MH chính**.
- Trong Zalo không cài được: bấm "…" › **Mở bằng trình duyệt** rồi làm như trên.

## Lưu ý

- Google API Key nằm (dạng che giấu) trong `index.html`. Nên giới hạn key theo **HTTP referrer** trong Google Cloud Console
  (APIs & Services › Credentials), thêm `https://<tên-tài-khoản>.github.io/*`.
- Thư mục Drive nên chia sẻ quyền **Người xem** (không cần quyền chỉnh sửa).
