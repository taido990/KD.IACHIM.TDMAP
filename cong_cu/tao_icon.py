# Bộ icon cài màn hình chính cho KD.IACHIM.TDMAP: logo tdmap sạch (cong_cu/logo_sach.ico) + nhãn LABEL
# Chạy: python cong_cu/tao_icon.py   → ghi icon-192/512, icon-maskable-512, apple-touch-icon.png, app-icon.ico vào thư mục dự án
# Làm cho xã khác: sửa LABEL (ngắn, ~7 ký tự).
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)   # mặc định: thư mục dự án (cha của cong_cu)
LABEL = 'IA CHIM'
FB = 'C:/Windows/Fonts/segoeuib.ttf'

src = Image.open(os.path.join(HERE, 'logo_sach.ico')).convert('RGBA')
a = np.asarray(src)
ys, xs = np.where(a[..., 3] > 10)
logo = src.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def make(size, pad=0.03, bg=None, safe=1.0):
    """Logo tròn căn giữa ô vuông; bg=None → nền trong suốt; safe<1 → thu nhỏ vào vùng an toàn (maskable)."""
    S = 1024
    im = Image.new('RGBA', (S, S), bg or (0, 0, 0, 0))
    w = int(S * (1 - 2 * pad) * safe)
    lg = logo.resize((w, int(w * logo.height / logo.width)), Image.LANCZOS)
    x0, y0 = (S - lg.width) // 2, (S - lg.height) // 2
    im.alpha_composite(lg, (x0, y0))
    d = ImageDraw.Draw(im)
    fs = int(lg.width * 0.102)
    f = ImageFont.truetype(FB, fs)
    cx, cy = S / 2, y0 + lg.height * 0.872   # dưới dòng "Tài Đỗ Map", trong vòng tròn
    d.text((cx, cy), LABEL, font=f, fill=(230, 20, 30), anchor='mm', stroke_width=max(2, fs // 12), stroke_fill='white')
    return im.resize((size, size), Image.LANCZOS)


make(192).save(os.path.join(D, 'icon-192.png'))
make(512).save(os.path.join(D, 'icon-512.png'))
# Maskable (Android cắt theo hình tròn / bo góc): nền xanh đậm phủ kín, logo nằm trong vùng an toàn 80%
make(512, pad=0, bg=(10, 40, 100, 255), safe=0.8).save(os.path.join(D, 'icon-maskable-512.png'))
# iOS không nhận nền trong suốt → nền trắng
make(180, bg=(255, 255, 255, 255)).convert('RGB').save(os.path.join(D, 'apple-touch-icon.png'))
# Favicon nhiều kích thước
make(256).save(os.path.join(D, 'app-icon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print('xong')
