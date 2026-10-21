# mittohoa.github.io

Trang cá nhân của Dương Minh Hòa (Mít tờ HÒA) — https://mittohoa.github.io/

Song ngữ Việt/Anh, giới thiệu bản thân và các app đang phát hành.

## ⚠️ Đừng xoá `.well-known/assetlinks.json`

File đó xác minh **Android App Links** cho app **TÔI ĐI**
(`com.mittohoa.toidi_app`) — chứa cả khoá ký của Google Play lẫn khoá ký bản
APK trên GitHub Releases. Xoá hoặc sửa sai là link `https://mittohoa.github.io/toidi/app/?…`
thôi mở thẳng trong app với mọi người đã cài.

Trang giới thiệu app TÔI ĐI nằm ở repo riêng (`mittohoa/toidi`), phục vụ tại
`/toidi/`, không liên quan tới `index.html` ở đây.

## Dựng lại trang

```bash
python build_site.py             # dựng từ cache, nhanh
python build_site.py --refresh   # đọc lại tên + logo từ trang của từng app
python build_site.py --dry       # chỉ in danh sách, không ghi file
```

Cần `gh` CLI đã đăng nhập tài khoản `mittohoa`.

Script tự lấy:

- **app nào đã lên Google Play** từ trang nhà phát triển (`PLAY_DEV`) — không
  tin link Play đặt trên trang app, vì link đó có thể trỏ vào gói đã gỡ;

- **danh sách repo + mô tả** qua `gh api` — repo nào bật GitHub Pages và có
  `description` thì tự lên trang, không phải sửa code;
- **tên app thật + logo** bằng cách đọc `<title>` và `<link rel="icon">` của
  chính trang app đó, lưu cache ở `site-data.json`.

Muốn xếp app vào đúng nhóm thì thêm một dòng vào `CURATED` trong
`build_site.py`; không khai báo thì app rơi vào nhóm "Khác". Repo không muốn
hiện thì thêm vào `SKIP`.

Thông tin cá nhân (tên, slogan, giới thiệu, link mạng xã hội) nằm trong khối
`ME` ở đầu `build_site.py`.

## Hiệu ứng ngày lễ

`festive.py` giữ danh sách 11 dịp lễ Việt Nam, mỗi dịp một bản sắc riêng
(màu chủ đạo, kiểu hạt rơi, biểu tượng, lời chúc song ngữ). Ngày dương lịch khai
thẳng, ngày âm lịch (Tết, Giỗ Tổ, Trung thu) được quy đổi ngay trên trình duyệt
bằng thuật toán âm lịch Hồ Ngọc Đức nên không phải sửa tay mỗi năm.

Xem thử một dịp bất kỳ mà không cần đợi tới ngày:

```
https://mittohoa.github.io/?festive=tet
https://mittohoa.github.io/?festive=trung-thu
https://mittohoa.github.io/?festive=off      # tắt hẳn
```

Thêm dịp mới: chèn một mục vào danh sách `FESTIVE` rồi chạy lại `build_site.py`.

## Ảnh

| File | Kích thước | Dùng cho |
|---|---|---|
| `me.jpg` | 440×440 | Chân dung tròn đầu trang |
| `og.jpg` | 1200×630 | Ảnh hiện khi chia sẻ link lên Facebook/Zalo/LinkedIn |
| `icon-180.png` | 180×180 | Favicon, icon khi lưu trang ra màn hình chính |
| `avatar-512.png` | 512×512 | Avatar dự phòng |

Ảnh gốc độ phân giải cao **để ngoài repo** cho nhẹ (tổng 22 MB). Khi thay ảnh,
nhớ nén lại trước khi commit — cả trang hiện chỉ khoảng 400 KB.
