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

## Đưa lên GitHub Pages

1. Tạo kho mới trên GitHub (Public).
2. **Add file › Upload files** → kéo thả tất cả file trong thư mục này (kể cả `.nojekyll`) → **Commit changes**.
3. **Settings › Pages** → *Source*: **Deploy from a branch** → *Branch*: `main` / `/ (root)` → **Save**.
4. Sau 1–2 phút trang chạy tại `https://<tên-tài-khoản>.github.io/<tên-kho>/`.

GitHub Pages chạy https nên nút vị trí (GPS) dùng được trên điện thoại.

## Cài lên màn hình chính

- **Android (Chrome):** mở trang › menu ⋮ › **Cài đặt ứng dụng** / **Thêm vào màn hình chính**.
- **iPhone (Safari):** mở trang › nút Chia sẻ › **Thêm vào MH chính**.
- Trong Zalo không cài được: bấm "…" › **Mở bằng trình duyệt** rồi làm như trên.

## Lưu ý

- Google API Key nằm (dạng che giấu) trong `index.html`. Nên giới hạn key theo **HTTP referrer** trong Google Cloud Console
  (APIs & Services › Credentials), thêm `https://<tên-tài-khoản>.github.io/*`.
- Thư mục Drive nên chia sẻ quyền **Người xem** (không cần quyền chỉnh sửa).
