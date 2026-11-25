// Service worker tối giản để trình duyệt (Chrome/Samsung Internet trên Android) cho "Cài đặt ứng dụng" / "Thêm vào màn hình chính".
// KHÔNG lưu đệm gì: mọi yêu cầu đi thẳng ra mạng, nên sửa index.html / bản vẽ trên Drive là thấy ngay, không bị bản cũ.
// (Bản vẽ đã giải mã vẫn được trang lưu đệm riêng trong IndexedDB như trước.)
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => { });
