# Tạo lại mã QR (ảnh đơn + poster) cho WebGIS KD.IACHIM.TDMAP
# Chạy: python cong_cu/tao_qr.py   (cần: pip install qrcode pillow) → ghi qr_KD_IACHIM_TDMAP.png / _poster.jpg vào thư mục dự án
# Làm cho xã khác: sửa URL, SHORT, chữ tiêu đề và tên file ảnh bên dưới.
import sys, os, qrcode
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # mặc định: thư mục dự án
URL = 'https://taido990.github.io/KD.IACHIM.TDMAP/'
SHORT = 'taido990.github.io/KD.IACHIM.TDMAP/'
F = 'C:/Windows/Fonts/'
B, R, SB = F + 'segoeuib.ttf', F + 'segoeui.ttf', F + 'seguisb.ttf'
GREEN, YEL, ORG = (14, 122, 62), (240, 230, 140), (196, 74, 20)


def font(path, size): return ImageFont.truetype(path, size)


def fit(d, text, path, size, maxw):
    while size > 10 and d.textlength(text, font=font(path, size)) > maxw: size -= 1
    return font(path, size)


def center(d, y, text, f, fill, W):
    d.text((W / 2, y), text, font=f, fill=fill, anchor='mm')


def qr_img(px):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=1)
    q.add_data(URL); q.make(fit=True)
    m = q.get_matrix(); n = len(m); s = px // n
    im = Image.new('RGB', (n * s, n * s), 'white'); d = ImageDraw.Draw(im)
    for r in range(n):
        for c in range(n):
            if m[r][c]: d.rectangle([c * s, r * s, c * s + s - 1, r * s + s - 1], fill='black')
    return im


# ---- Ảnh QR đơn (888 x 1268) ----
W, H = 888, 1268
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
center(d, 68, 'Khu vực đo Xã Ia Chim', fit(d, 'Khu vực đo Xã Ia Chim', B, 62, W - 60), 'black', W)
center(d, 138, 'Tỉnh Quảng Ngãi · TDMAP.PRO.VN', fit(d, 'Tỉnh Quảng Ngãi · TDMAP.PRO.VN', B, 40, W - 60), 'black', W)
q = qr_img(700); im.paste(q, ((W - q.width) // 2, 614 - q.height // 2))
center(d, 1108, 'QUÉT MÃ', font(B, 90), 'black', W)
t = 'để mở bản đồ  ·  ' + SHORT
center(d, 1182, t, fit(d, t, R, 30, W - 50), (40, 40, 40), W)
im.save(os.path.join(OUT, 'qr_KD_IACHIM_TDMAP.png'))

# ---- Poster (1080 x 1640) ----
W, H = 1080, 1640
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 250], fill=GREEN)
center(d, 82, 'TRA CỨU BẢN ĐỒ ĐỊA CHÍNH', fit(d, 'TRA CỨU BẢN ĐỒ ĐỊA CHÍNH', B, 62, W - 80), 'white', W)
t = 'KHU VỰC ĐO XÃ IA CHIM - TỈNH QUẢNG NGÃI'
center(d, 158, t, fit(d, t, B, 50, W - 70), YEL, W)
center(d, 215, 'TDMAP.PRO.VN', font(R, 30), 'white', W)
d.rounded_rectangle([195, 278, 885, 968], radius=22, outline=GREEN, width=5, fill='white')
q = qr_img(522); im.paste(q, ((W - q.width) // 2, 623 - q.height // 2))
t = 'MỞ ZALO  →  QUÉT MÃ QR ĐỂ XEM BẢN ĐỒ'
center(d, 1027, t, fit(d, t, B, 42, W - 90), GREEN, W)
d.rounded_rectangle([60, 1077, 1020, 1402], radius=20, fill=(233, 244, 238))
steps = ['Mở Zalo (biểu tượng quét QR) hoặc Camera điện thoại',
         'Quét mã — hoặc nhấn giữ ảnh này → "Quét mã QR"',
         'Bấm nút "Lớp" (góc phải trên) để bật / tắt lớp',
         'Bấm nút ghim để xem vị trí đang đứng']
for i, s in enumerate(steps):
    y = 1126 + i * 74
    d.ellipse([94, y - 24, 142, y + 24], fill=GREEN)
    d.text((118, y), str(i + 1), font=font(B, 28), fill='white', anchor='mm')
    d.text((165, y), s, font=fit(d, s, R, 31, 830), fill=(28, 38, 40), anchor='lm')
center(d, 1456, 'Định vị không chạy trong Zalo? Bấm "..." → Mở bằng trình duyệt', font(R, 27), ORG, W)
d.rectangle([0, 1550, W, H], fill=GREEN)
center(d, 1596, SHORT, fit(d, SHORT, B, 38, W - 80), 'white', W)
im.save(os.path.join(OUT, 'qr_KD_IACHIM_TDMAP_poster.jpg'), quality=95)
print('xong')
