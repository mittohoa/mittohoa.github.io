# -*- coding: utf-8 -*-
"""
Hiệu ứng ngày lễ cho trang chủ — mỗi dịp một bản sắc riêng.

Ngày dương lịch khai thẳng ("09-02"). Ngày âm lịch khai theo âm lịch
("01-01" là mùng 1 Tết) rồi trang tự quy ra dương lịch cho đúng năm đang
xem, nên không phải sửa tay mỗi năm.

Xem thử một dịp bất kỳ: thêm ?festive=<id> vào địa chỉ, ví dụ
    https://mittohoa.github.io/?festive=tet
Tắt hẳn: ?festive=off
"""


# ======================= BẢNG MÀU & BỘ HẠT DÙNG CHUNG =======================
# Mỗi dịp bốc ngẫu nhiên một "look" trong danh sách looks của nó, nên vào trang
# hai lần có thể thấy hai diện mạo khác nhau.
PALETTES = {
    "hong":     ("#ff4f93", ["#ff2d7e", "#ff6fa5", "#ffab5e"],
                 ["#ff4f93", "#ff8fb8", "#ffb3cd", "#ffd6e4", "#ffc46b"]),
    "do_hong":  ("#e8356d", ["#b3124a", "#e8356d", "#ff9ec4"],
                 ["#e8356d", "#ff9ec4", "#ffd0e0", "#ffffff", "#ffc46b"]),
    "tim":      ("#c661e8", ["#9b2fd1", "#c661e8", "#ff8fb8"],
                 ["#c661e8", "#e3a8f5", "#ff8fb8", "#ffd6e4", "#ffc46b"]),
    "do_vang":  ("#e8352f", ["#c81e1e", "#e8352f", "#f2b705"],
                 ["#f2b705", "#ffd95e", "#e8352f", "#ff7a7a", "#ffe9a8"]),
    "co_do":    ("#e11d2e", ["#b91122", "#e11d2e", "#ffd23f"],
                 ["#ffd23f", "#e11d2e", "#ff8a8a", "#ffe9a8", "#ffffff"]),
    "cam":      ("#f08c00", ["#d9480f", "#f08c00", "#ffd43b"],
                 ["#ffd43b", "#f08c00", "#ff922b", "#ffe8a3", "#ff6b6b"]),
    "nau_dong": ("#c2410c", ["#7c2d12", "#c2410c", "#d8a657"],
                 ["#d8a657", "#c2410c", "#e8c07d", "#8b5e34", "#f0d9a8"]),
    "xanh_bien":("#5b8cff", ["#2b4fd8", "#5b8cff", "#8ad4ff"],
                 ["#8ad4ff", "#5b8cff", "#c9e4ff", "#ffd36b", "#ffffff"]),
    "ngoc":     ("#22a6b3", ["#0ea5a5", "#22c3d6", "#ffd166"],
                 ["#ff6b6b", "#ffd166", "#22c3d6", "#a0e86f", "#c77dff"]),
    "luc":      ("#2f8f6b", ["#166b4e", "#2f8f6b", "#8ed6a8"],
                 ["#8ed6a8", "#2f8f6b", "#cdeedb", "#ffd166", "#ffffff"]),
    "noel":     ("#1f9254", ["#0f6b3a", "#1f9254", "#e03131"],
                 ["#ffffff", "#e8f7ff", "#e03131", "#1f9254", "#ffd43b"]),
    "vang_kim": ("#d4a017", ["#8a6d1a", "#d4a017", "#ffe08a"],
                 ["#ffe08a", "#d4a017", "#fff3c4", "#c2410c", "#ffffff"]),
    "do_tim":   ("#e0245e", ["#a31545", "#e0245e", "#ff7aa8"],
                 ["#e0245e", "#ff7aa8", "#ffd0e0", "#ffffff", "#c2185b"]),
    "cam_bi":   ("#e8590c", ["#7c2d12", "#e8590c", "#ffa94d"],
                 ["#e8590c", "#ffa94d", "#ffd8a8", "#2b2b2b", "#845ef7"]),
    "lam":      ("#1e6091", ["#0b3954", "#1e6091", "#64b6ac"],
                 ["#64b6ac", "#1e6091", "#a8dadc", "#f1faee", "#ffd166"]),
    "sen":      ("#d6336c", ["#9c1f4d", "#d6336c", "#ffc9de"],
                 ["#ffc9de", "#d6336c", "#ffe3ee", "#8ed6a8", "#ffffff"]),
    "tuyet":    ("#7fb3ff", ["#2b4fd8", "#7fb3ff", "#ffffff"],
                 ["#ffffff", "#dbeafe", "#7fb3ff", "#bfdbfe", "#e0f2fe"]),
}


def look(palette, shape, direction, emoji):
    """Một diện mạo: bảng màu + hình hạt + hướng bay + biểu tượng."""
    accent, grad, colors = PALETTES[palette]
    return {"accent": accent, "grad": grad, "colors": colors,
            "shape": shape, "dir": direction, "emoji": emoji}


# Kiểu popup. Mỗi dịp có thể giới hạn bằng khoá "skins".
SKINS = ["card", "splash", "ticket", "neon", "postcard", "scroll"]


# Mỗi mục:
#   id       : tên để xem thử qua ?festive=<id>
#   solar    : "MM-DD" theo dương lịch   | lunar: "MM-DD" theo âm lịch
#   before/after : số ngày hiện thêm trước/sau ngày chính
#   theme    : accent (màu chủ đạo), grad (băng rôn), colors (hạt),
#              shape (petal|star|dot|lantern), dir (down|up), emoji
#   art      : chữ lớn trong popup
FESTIVE = [
    {
        "id": "tet-duong-lich",
        "solar": "01-01",
        "before": 0, "after": 0,
        "art": "01·01",
        "looks": [look("xanh_bien", "star", "down", "🎆"), look("tuyet", "dot", "down", "❄️"), look("xanh_bien", "star", "fireworks", "🎇")],
        "vi": {"bar": "Chúc mừng năm mới",
               "title": "Chúc mừng năm mới",
               "sub": "Một năm mới gọn gàng, nhiều việc hay và ít việc phải sửa lại.",
               "run": "Năm mới bình an · nhiều sức khoẻ · nhiều điều tử tế 🎆 ",
               "ok": "Cảm ơn 🎆"},
        "en": {"bar": "Happy New Year",
               "title": "Happy New Year",
               "sub": "Wishing you a tidy year with plenty of good work and few rollbacks.",
               "run": "Peace · health · kindness for the year ahead 🎆 ",
               "ok": "Thank you 🎆"},
    },
    {
        "id": "tet",
        "lunar": "01-01",
        "before": 2, "after": 3,
        "art": "Tết",
        "looks": [look("do_vang", "petal", "down", "🧧"), look("vang_kim", "dot", "up", "✨"), look("do_vang", "confetti", "fireworks", "🎆")],
        "vi": {"bar": "Chúc mừng năm mới — An khang thịnh vượng",
               "title": "Chúc mừng năm mới",
               "sub": "Chúc cả nhà một năm mới an khang, thuận lợi và nhiều niềm vui.",
               "run": "An khang · Thịnh vượng · Vạn sự như ý 🧧 Chúc mừng năm mới 🧧 ",
               "ok": "Chúc mừng năm mới 🧧"},
        "en": {"bar": "Happy Lunar New Year",
               "title": "Happy Lunar New Year",
               "sub": "Wishing you and your family a peaceful, prosperous and joyful year.",
               "run": "Peace · Prosperity · Every wish fulfilled 🧧 Happy Lunar New Year 🧧 ",
               "ok": "Happy New Year 🧧"},
    },
    {
        "id": "8-3",
        "solar": "03-08",
        "before": 0, "after": 0,
        "art": "08·03",
        "looks": [look("tim", "petal", "down", "💐"), look("do_hong", "dot", "up", "💗")],
        "vi": {"bar": "8/3 — Chúc mừng Ngày Quốc tế Phụ nữ",
               "title": "Chúc mừng Ngày Quốc tế Phụ nữ",
               "sub": "Gửi tới những người phụ nữ quanh mình một ngày thật nhẹ nhàng.",
               "run": "Chúc các chị em luôn mạnh khoẻ, rực rỡ và được yêu thương 💐 ",
               "ok": "Cảm ơn 💐"},
        "en": {"bar": "8 Mar — Happy International Women's Day",
               "title": "Happy International Women's Day",
               "sub": "To all the women around us — have a lovely day.",
               "run": "Health, joy and plenty of love 💐 ",
               "ok": "Thank you 💐"},
    },
    {
        "id": "gio-to",
        "lunar": "03-10",
        "before": 0, "after": 0,
        "art": "10·3",
        "looks": [look("nau_dong", "dot", "down", "🪷"), look("vang_kim", "star", "down", "🪘")],
        "vi": {"bar": "Giỗ Tổ Hùng Vương — mùng 10 tháng 3",
               "title": "Giỗ Tổ Hùng Vương",
               "sub": "Dù ai đi ngược về xuôi, nhớ ngày Giỗ Tổ mùng mười tháng ba.",
               "run": "Con Lạc cháu Hồng · Uống nước nhớ nguồn 🪷 ",
               "ok": "Ghi nhớ 🪷"},
        "en": {"bar": "Hung Kings Commemoration Day",
               "title": "Hung Kings Commemoration Day",
               "sub": "A day to remember the founders of the country.",
               "run": "Remembering where we came from 🪷 ",
               "ok": "Noted 🪷"},
    },
    {
        "id": "30-4",
        "solar": "04-30",
        "before": 0, "after": 1,
        "art": "30·4",
        "looks": [look("co_do", "star", "down", "🇻🇳"), look("do_vang", "dot", "up", "🎉"), look("co_do", "confetti", "fireworks", "🎆")],
        "vi": {"bar": "30/4 — 1/5 · Chúc mừng ngày lễ lớn",
               "title": "Ngày Giải phóng miền Nam & Quốc tế Lao động",
               "sub": "Chúc mọi người kỳ nghỉ vui vẻ, đi chơi an toàn và nghỉ ngơi thật đã.",
               "run": "30/4 Thống nhất đất nước · 1/5 Quốc tế Lao động 🇻🇳 ",
               "ok": "Nghỉ lễ vui 🇻🇳"},
        "en": {"bar": "30 Apr — 1 May · National holidays",
               "title": "Reunification Day & International Workers' Day",
               "sub": "Enjoy the long weekend, travel safely and get some real rest.",
               "run": "30 Apr Reunification · 1 May Workers' Day 🇻🇳 ",
               "ok": "Happy holidays 🇻🇳"},
    },
    {
        "id": "1-6",
        "solar": "06-01",
        "before": 0, "after": 0,
        "art": "01·06",
        "looks": [look("ngoc", "dot", "up", "🎈"), look("hong", "star", "up", "🍭")],
        "vi": {"bar": "1/6 — Quốc tế Thiếu nhi",
               "title": "Quốc tế Thiếu nhi",
               "sub": "Chúc các bạn nhỏ một ngày đầy bóng bay, kem và tiếng cười.",
               "run": "Chúc các bé luôn khoẻ, học vui và chơi thật thoả 🎈 ",
               "ok": "Yeah 🎈"},
        "en": {"bar": "1 Jun — Children's Day",
               "title": "International Children's Day",
               "sub": "A day of balloons, ice cream and laughter for the little ones.",
               "run": "Health, fun and plenty of playtime 🎈 ",
               "ok": "Yay 🎈"},
    },
    {
        "id": "trung-thu",
        "lunar": "08-15",
        "before": 1, "after": 0,
        "art": "Trung thu",
        "looks": [look("cam", "lantern", "up", "🏮"), look("vang_kim", "dot", "up", "🌕")],
        "vi": {"bar": "Tết Trung thu — rằm tháng tám",
               "title": "Chúc mừng Tết Trung thu",
               "sub": "Chúc cả nhà một đêm rằm sáng trăng, đủ đầy và quây quần.",
               "run": "Trăng tròn · Đèn sáng · Bánh ngon 🏮 Vui Tết Trung thu 🏮 ",
               "ok": "Vui Trung thu 🏮"},
        "en": {"bar": "Mid-Autumn Festival",
               "title": "Happy Mid-Autumn Festival",
               "sub": "A bright full moon and a warm evening with the people you love.",
               "run": "Full moon · Bright lanterns · Good mooncakes 🏮 ",
               "ok": "Thank you 🏮"},
    },
    {
        "id": "2-9",
        "solar": "09-02",
        "before": 0, "after": 0,
        "art": "02·09",
        "looks": [look("co_do", "star", "down", "⭐"), look("do_vang", "star", "up", "🎆"), look("co_do", "star", "fireworks", "🎇")],
        "vi": {"bar": "2/9 — Chúc mừng Quốc khánh",
               "title": "Chúc mừng Quốc khánh",
               "sub": "Chúc mọi người một ngày lễ bình an bên gia đình.",
               "run": "Quốc khánh nước Cộng hoà Xã hội Chủ nghĩa Việt Nam ⭐ ",
               "ok": "Cảm ơn ⭐"},
        "en": {"bar": "2 Sep — Vietnam National Day",
               "title": "Vietnam National Day",
               "sub": "Wishing everyone a peaceful holiday with family.",
               "run": "National Day of Vietnam ⭐ ",
               "ok": "Thank you ⭐"},
    },
    {
        "id": "20-10",
        "solar": "10-20",
        "before": 0, "after": 0,
        "art": "20·10",
        "looks": [look("hong", "petal", "down", "🌸"), look("do_hong", "dot", "up", "💗"), look("tim", "star", "down", "💜")],
        "vi": {"bar": "20/10 — Chúc mừng Ngày Phụ nữ Việt Nam",
               "title": "Chúc mừng Ngày Phụ nữ Việt Nam",
               "sub": "Gửi tới những người phụ nữ quanh mình — mẹ, chị, em, đồng nghiệp — một ngày thật nhẹ nhàng.",
               "run": "Chúc các chị em luôn mạnh khoẻ, rực rỡ và được yêu thương 🌸 ",
               "ok": "Cảm ơn 🌸"},
        "en": {"bar": "20 Oct — Happy Vietnamese Women's Day",
               "title": "Happy Vietnamese Women's Day",
               "sub": "To all the women around us — mothers, sisters, colleagues — have a lovely day.",
               "run": "Wishing you health, joy and plenty of love 🌸 ",
               "ok": "Thank you 🌸"},
    },
    {
        "id": "20-11",
        "solar": "11-20",
        "before": 0, "after": 0,
        "art": "20·11",
        "looks": [look("luc", "petal", "down", "🎓"), look("xanh_bien", "dot", "down", "📘")],
        "vi": {"bar": "20/11 — Chúc mừng Ngày Nhà giáo Việt Nam",
               "title": "Chúc mừng Ngày Nhà giáo Việt Nam",
               "sub": "Cảm ơn những người đã dạy mình cách học, chứ không chỉ dạy bài.",
               "run": "Tri ân thầy cô 🎓 Chúc thầy cô nhiều sức khoẻ và niềm vui 🎓 ",
               "ok": "Tri ân 🎓"},
        "en": {"bar": "20 Nov — Vietnamese Teachers' Day",
               "title": "Happy Vietnamese Teachers' Day",
               "sub": "Thank you to everyone who taught us how to learn, not just what to learn.",
               "run": "With gratitude to our teachers 🎓 ",
               "ok": "Thank you 🎓"},
    },
    {
        "id": "noel",
        "solar": "12-24",
        "before": 0, "after": 1,
        "art": "Noel",
        "looks": [look("noel", "dot", "down", "🎄"), look("tuyet", "dot", "down", "❄️")],
        "vi": {"bar": "Giáng sinh an lành",
               "title": "Giáng sinh an lành",
               "sub": "Chúc một mùa Giáng sinh ấm áp bên những người thương.",
               "run": "Merry Christmas 🎄 Giáng sinh an lành 🎄 ",
               "ok": "Cảm ơn 🎄"},
        "en": {"bar": "Merry Christmas",
               "title": "Merry Christmas",
               "sub": "Wishing you a warm Christmas with the people you love.",
               "run": "Merry Christmas 🎄 ",
               "ok": "Thank you 🎄"},
    },
    {
        "id": "ong-tao",
        "lunar": "12-23",
        "before": 0, "after": 0,
        "art": "23 Chạp",
        "looks": [look("cam", "coin", "up", "\U0001F41F"), look("vang_kim", "coin", "up", "\U0001F9E8")],
        "vi": {"bar": "23 th\u00e1ng Ch\u1EA1p \u2014 \u00d4ng C\u00f4ng \u00d4ng T\u00e1o v\u1EC1 tr\u1EDDi",
               "title": "Ti\u1EC5n \u00d4ng T\u00e1o v\u1EC1 tr\u1EDDi",
               "sub": "D\u1ECDn nh\u00e0, d\u1ECDn lu\u00f4n m\u1EA5y nh\u00e1nh code t\u1EA1m b\u1EE3 \u0111\u1EC3 \u0111\u00f3n n\u0103m m\u1EDBi cho nh\u1EB9.",
               "run": "C\u00e1 ch\u00e9p ho\u00e1 r\u1ED3ng \u00b7 B\u1EBFp \u1EA5m nh\u00e0 vui \U0001F41F ",
               "ok": "Ti\u1EC5n T\u00e1o \U0001F41F"},
        "en": {"bar": "Kitchen Gods Day",
               "title": "Farewell to the Kitchen Gods",
               "sub": "Tidy the house \u2014 and those temporary branches \u2014 before the new year.",
               "run": "Carp turns into dragon \u00b7 A warm kitchen, a happy home \U0001F41F ",
               "ok": "Farewell \U0001F41F"},
    },
    {
        "id": "nguyen-tieu",
        "lunar": "01-15",
        "before": 0, "after": 0,
        "art": "Nguy\u00ean ti\u00eau",
        "looks": [look("vang_kim", "lantern", "up", "\U0001F315"), look("do_vang", "coin", "up", "\U0001F3EE")],
        "vi": {"bar": "R\u1EB1m th\u00e1ng Gi\u00eang \u2014 T\u1EBFt Nguy\u00ean ti\u00eau",
               "title": "T\u1EBFt Nguy\u00ean ti\u00eau",
               "sub": "C\u00fang c\u1EA3 n\u0103m kh\u00f4ng b\u1EB1ng r\u1EB1m th\u00e1ng Gi\u00eang \u2014 ch\u00fac m\u1ED9t n\u0103m \u0111\u1EE7 \u0111\u1EA7y.",
               "run": "Tr\u0103ng tr\u00f2n \u0111\u1EA7u n\u0103m \u00b7 V\u1EA1n s\u1EF1 hanh th\u00f4ng \U0001F315 ",
               "ok": "An l\u00e0nh \U0001F315"},
        "en": {"bar": "Lantern Festival \u2014 first full moon",
               "title": "Lantern Festival",
               "sub": "The first full moon of the lunar year \u2014 may it be a full one.",
               "run": "First full moon \u00b7 May everything go smoothly \U0001F315 ",
               "ok": "Thank you \U0001F315"},
    },
    {
        "id": "valentine",
        "solar": "02-14",
        "before": 0, "after": 0,
        "art": "14\u00b702",
        "looks": [look("do_tim", "heart", "up", "\u2764\ufe0f"), look("hong", "heart", "down", "\U0001F49E"),
                  look("do_hong", "confetti", "down", "\U0001F498")],
        "vi": {"bar": "14/2 \u2014 Valentine",
               "title": "Ch\u00fac m\u1EEBng Valentine",
               "sub": "Ch\u00fac m\u1ECDi ng\u01B0\u1EDDi m\u1ED9t ng\u00e0y ng\u1ECDt ng\u00e0o \u2014 k\u1EC3 c\u1EA3 khi crush v\u1EABn ch\u01B0a rep.",
               "run": "Y\u00eau th\u01B0\u01A1ng g\u1EEDi \u0111i r\u1ED3i s\u1EBD quay v\u1EC1 \u2764\ufe0f ",
               "ok": "C\u1EA3m \u01A1n \u2764\ufe0f"},
        "en": {"bar": "14 Feb \u2014 Valentine's Day",
               "title": "Happy Valentine's Day",
               "sub": "Have a sweet day \u2014 even if your crush still has not replied.",
               "run": "Love sent out always finds its way back \u2764\ufe0f ",
               "ok": "Thank you \u2764\ufe0f"},
    },
    {
        "id": "thay-thuoc",
        "solar": "02-27",
        "before": 0, "after": 0,
        "art": "27\u00b702",
        "looks": [look("lam", "heart", "up", "\U0001FA7A"), look("ngoc", "dot", "down", "\U0001F499")],
        "vi": {"bar": "27/2 \u2014 Ng\u00e0y Th\u1EA7y thu\u1ED1c Vi\u1EC7t Nam",
               "title": "Ng\u00e0y Th\u1EA7y thu\u1ED1c Vi\u1EC7t Nam",
               "sub": "C\u1EA3m \u01A1n nh\u1EEFng ng\u01B0\u1EDDi tr\u1EF1c \u0111\u00eam \u0111\u1EC3 ng\u01B0\u1EDDi kh\u00e1c \u0111\u01B0\u1EE3c ng\u1EE7 y\u00ean.",
               "run": "L\u01B0\u01A1ng y nh\u01B0 t\u1EEB m\u1EABu \U0001FA7A Ch\u00fac c\u00e1c y b\u00e1c s\u0129 nhi\u1EC1u s\u1EE9c kho\u1EBB \U0001FA7A ",
               "ok": "Tri \u00e2n \U0001FA7A"},
        "en": {"bar": "27 Feb \u2014 Vietnamese Doctors' Day",
               "title": "Vietnamese Doctors' Day",
               "sub": "Thank you to everyone who works the night shift so others can sleep.",
               "run": "With gratitude to our doctors and nurses \U0001FA7A ",
               "ok": "Thank you \U0001FA7A"},
    },
    {
        "id": "doan-ngo",
        "lunar": "05-05",
        "before": 0, "after": 0,
        "art": "5\u00b75",
        "looks": [look("luc", "dot", "down", "\U0001F348"), look("cam", "confetti", "down", "\U0001F33F")],
        "vi": {"bar": "M\u00f9ng 5 th\u00e1ng 5 \u2014 T\u1EBFt \u0110oan Ng\u1ECD",
               "title": "T\u1EBFt \u0110oan Ng\u1ECD",
               "sub": "Ng\u00e0y gi\u1EBFt s\u00e2u b\u1ECD \u2014 ch\u00fac m\u1ECDi ng\u01B0\u1EDDi s\u1EA1ch b\u1EC7nh, s\u1EA1ch bug.",
               "run": "C\u01A1m r\u01B0\u1EE3u \u00b7 B\u00e1nh tro \u00b7 Hoa qu\u1EA3 \u0111\u1EA7u m\u00f9a \U0001F33F ",
               "ok": "M\u00e1t l\u00e0nh \U0001F33F"},
        "en": {"bar": "Doan Ngo Festival",
               "title": "Doan Ngo Festival",
               "sub": "The day for clearing out pests \u2014 and bugs.",
               "run": "Sweet fermented rice \u00b7 Ash cakes \u00b7 First fruits \U0001F33F ",
               "ok": "Thank you \U0001F33F"},
    },
    {
        "id": "gia-dinh",
        "solar": "06-28",
        "before": 0, "after": 0,
        "art": "28\u00b706",
        "looks": [look("sen", "heart", "up", "\U0001F3E1"), look("ngoc", "dot", "float", "\U0001F46A")],
        "vi": {"bar": "28/6 \u2014 Ng\u00e0y Gia \u0111\u00ecnh Vi\u1EC7t Nam",
               "title": "Ng\u00e0y Gia \u0111\u00ecnh Vi\u1EC7t Nam",
               "sub": "T\u1EAFt m\u00e1y s\u1EDBm m\u1ED9t h\u00f4m, v\u1EC1 nh\u00e0 \u0103n c\u01A1m c\u00f9ng c\u1EA3 nh\u00e0.",
               "run": "V\u1EC1 nh\u00e0 \u0103n c\u01A1m \U0001F3E1 Gia \u0111\u00ecnh l\u00e0 n\u01A1i \u0111\u1EC3 quay v\u1EC1 \U0001F3E1 ",
               "ok": "V\u1EC1 nh\u00e0 \U0001F3E1"},
        "en": {"bar": "28 Jun \u2014 Vietnamese Family Day",
               "title": "Vietnamese Family Day",
               "sub": "Log off early today and have dinner with the family.",
               "run": "Home is where you come back to \U0001F3E1 ",
               "ok": "Thank you \U0001F3E1"},
    },
    {
        "id": "vu-lan",
        "lunar": "07-15",
        "before": 0, "after": 0,
        "art": "Vu Lan",
        "looks": [look("sen", "petal", "float", "\U0001FAB7"), look("vang_kim", "lantern", "up", "\U0001F56F\ufe0f")],
        "vi": {"bar": "R\u1EB1m th\u00e1ng B\u1EA3y \u2014 L\u1EC5 Vu Lan b\u00e1o hi\u1EBFu",
               "title": "L\u1EC5 Vu Lan",
               "sub": "Ai c\u00f2n m\u1EB9 xin \u0111\u1EEBng l\u00e0m m\u1EB9 kh\u00f3c \u2014 h\u00f4m nay nh\u1EDB g\u1ECDi v\u1EC1 nh\u00e0 m\u1ED9t cu\u1ED9c.",
               "run": "B\u00f4ng h\u1ED3ng c\u00e0i \u00e1o \U0001FAB7 Vu Lan b\u00e1o hi\u1EBFu \U0001FAB7 ",
               "ok": "Nh\u1EDB nh\u00e0 \U0001FAB7"},
        "en": {"bar": "Vu Lan \u2014 Parents' Day",
               "title": "Vu Lan Festival",
               "sub": "A day for gratitude to our parents \u2014 call home today.",
               "run": "A rose for those who still have their mother \U0001FAB7 ",
               "ok": "Thank you \U0001FAB7"},
    },
    {
        "id": "halloween",
        "solar": "10-31",
        "before": 0, "after": 0,
        "art": "31\u00b710",
        "looks": [look("cam_bi", "star", "float", "\U0001F383"), look("cam_bi", "confetti", "down", "\U0001F47B")],
        "skins": ["neon", "card", "ticket"],
        "vi": {"bar": "31/10 \u2014 Halloween",
               "title": "Happy Halloween",
               "sub": "Trick or treat \u2014 ho\u1EB7c ch\u1ECDn c\u00e1ch th\u1EE9 ba: \u1EDF nh\u00e0 deploy.",
               "run": "Trick or treat \U0001F383 \u0110\u00eam nay c\u00f3 g\u00ec \u0111\u00f3 h\u01A1i l\u1EA1 \U0001F47B ",
               "ok": "H\u00fa h\u1ED3n \U0001F383"},
        "en": {"bar": "31 Oct \u2014 Halloween",
               "title": "Happy Halloween",
               "sub": "Trick or treat \u2014 or option three: stay home and deploy.",
               "run": "Trick or treat \U0001F383 Something feels off tonight \U0001F47B ",
               "ok": "Boo \U0001F383"},
    },
    {
        "id": "qdnd",
        "solar": "12-22",
        "before": 0, "after": 0,
        "art": "22\u00b712",
        "looks": [look("co_do", "star", "down", "\u2B50"), look("luc", "star", "down", "\U0001F396\ufe0f")],
        "vi": {"bar": "22/12 \u2014 Ng\u00e0y th\u00e0nh l\u1EADp Qu\u00e2n \u0111\u1ED9i nh\u00e2n d\u00e2n Vi\u1EC7t Nam",
               "title": "Ng\u00e0y th\u00e0nh l\u1EADp Qu\u00e2n \u0111\u1ED9i nh\u00e2n d\u00e2n Vi\u1EC7t Nam",
               "sub": "G\u1EEDi l\u1EDDi tri \u00e2n t\u1EDBi nh\u1EEFng ng\u01B0\u1EDDi gi\u1EEF b\u00ecnh y\u00ean cho ng\u00e0y th\u01B0\u1EDDng c\u1EE7a ch\u00fang ta.",
               "run": "Tri \u00e2n ng\u01B0\u1EDDi l\u00ednh \u2B50 22/12 \u2B50 ",
               "ok": "Tri \u00e2n \u2B50"},
        "en": {"bar": "22 Dec \u2014 Vietnam People's Army Day",
               "title": "Vietnam People's Army Day",
               "sub": "With gratitude to those who keep our ordinary days peaceful.",
               "run": "Honouring our soldiers \u2B50 ",
               "ok": "Thank you \u2B50"},
    },
]


FESTIVE_CSS = """
/* Chỉ bật khi <html> có class festive — ngoài ngày lễ thì trang y như cũ.
   Màu lấy từ biến --fes-* do JS gán theo từng dịp. */
html.festive{--accent:var(--fes-accent);--accent-soft:var(--fes-soft)}

#petals{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:4;
  transform:translateZ(0)}

#festive{
  display:none;position:relative;z-index:5;align-items:center;justify-content:center;
  gap:12px;padding:14px 56px 14px 20px;text-align:center;color:#fff;font-weight:600;
  font-size:15px;letter-spacing:.01em;
  background:linear-gradient(100deg,var(--fes-g1),var(--fes-g2) 42%,var(--fes-g3));
  box-shadow:0 2px 18px var(--fes-soft)
}
#festive.on{display:flex}
#festive .em{font-size:20px;line-height:1;animation:sway 2.6s ease-in-out infinite}
@keyframes sway{0%,100%{transform:rotate(-12deg)}50%{transform:rotate(12deg)}}
#festive .hint{font-weight:400;opacity:.85;font-size:13px}
#festive .x{
  position:absolute;right:14px;top:50%;transform:translateY(-50%);
  border:0;background:transparent;color:#fff;opacity:.8;
  cursor:pointer;font-size:20px;line-height:1;padding:2px 6px
}
#festive .x:hover{opacity:1}

html.festive .portrait{
  border-color:var(--fes-accent);
  box-shadow:0 0 0 6px var(--fes-soft),0 10px 34px var(--fes-glow)
}
html.festive .slogan em{text-shadow:0 0 24px var(--fes-glow)}
html.festive #lang{top:70px}

/* ---------- popup ngày lễ ---------- */
#fmodal{
  position:fixed;inset:0;z-index:10;display:none;align-items:center;justify-content:center;
  padding:20px;background:rgba(8,6,12,.62);backdrop-filter:blur(7px)
}
#fmodal.on{display:flex}
.fm-card{
  position:relative;width:min(540px,100%);padding:38px 30px 30px;text-align:center;
  border-radius:22px;background:var(--surface);
  border:1px solid var(--fes-accent);box-shadow:0 24px 70px #00000066,0 0 60px var(--fes-soft);
  animation:pop .45s cubic-bezier(.2,.9,.3,1.25) both
}
@keyframes pop{
  0%{opacity:0;transform:scale(1.4);filter:blur(14px)}
  55%{opacity:1;filter:blur(0)}
  75%{transform:scale(.97)}
  100%{transform:scale(1)}
}
/* quầng sáng loé lên phía sau thẻ ngay khi mở */
.fm-card::before{
  content:"";position:absolute;inset:-40% -25%;z-index:-1;border-radius:50%;
  background:radial-gradient(circle,var(--fes-glow),transparent 62%);
  animation:flash .9s ease-out both
}
@keyframes flash{0%{opacity:0;transform:scale(.4)}35%{opacity:1}100%{opacity:.25;transform:scale(1)}}
.fm-art{
  font-size:clamp(50px,12vw,98px);font-weight:800;line-height:.95;letter-spacing:-.03em;
  background:linear-gradient(100deg,var(--fes-g1),var(--fes-g2),var(--fes-g3),var(--fes-g1));
  background-size:300% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent;
  animation:shimmer 5.5s linear infinite
}
@keyframes shimmer{to{background-position:300% 0}}
/* h2 của trang là nhãn mục nhỏ (in hoa, xám) — tiêu đề popup phải tự khai lại */
.fm-title{
  margin:10px 0 10px;font-size:clamp(19px,4.4vw,25px);line-height:1.3;
  letter-spacing:-.01em;text-transform:none;color:var(--ink);font-weight:700
}
.fm-title span{display:inline-block;opacity:0;transform:translateY(16px);
  animation:rise .5s cubic-bezier(.2,.9,.3,1.2) forwards}
@keyframes rise{to{opacity:1;transform:none}}
.fm-sub{margin:0 auto 18px;max-width:40ch;font-size:14.5px;color:var(--muted);line-height:1.6}
.fm-run{
  overflow:hidden;white-space:nowrap;margin:0 -30px 20px;padding:9px 0;
  border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  font-size:13px;color:var(--fes-accent);font-weight:600;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)
}
.fm-run span{display:inline-block;padding-left:100%;animation:run 17s linear infinite}
@keyframes run{to{transform:translateX(-100%)}}
.fm-ok{
  border:0;border-radius:999px;padding:12px 30px;cursor:pointer;
  font:700 15px/1 inherit;color:#fff;
  background:linear-gradient(100deg,var(--fes-g1),var(--fes-g3));
  box-shadow:0 8px 22px var(--fes-soft)
}
.fm-ok:hover{filter:brightness(1.07)}
.fm-x{
  position:absolute;right:14px;top:12px;border:0;background:transparent;cursor:pointer;
  color:var(--muted);font-size:22px;line-height:1;padding:4px 8px
}
.fm-x:hover{color:var(--ink)}

/* ===== kiểu SPLASH: tràn màn hình, chữ ART khổng lồ, không khung thẻ ===== */
#fmodal.skin-splash{
  background:linear-gradient(140deg,var(--fes-g1),var(--fes-g2) 48%,var(--fes-g3));
  backdrop-filter:none
}
.skin-splash .fm-card{
  background:transparent;border:0;box-shadow:none;width:min(760px,100%);padding:20px
}
.skin-splash .fm-card::before{display:none}
.skin-splash .fm-art{
  font-size:clamp(76px,20vw,180px);background:none;-webkit-text-fill-color:#fff;color:#fff;
  text-shadow:0 10px 40px rgba(0,0,0,.28);animation:none
}
.skin-splash .fm-title{color:#fff;font-size:clamp(22px,5vw,34px)}
.skin-splash .fm-sub{color:rgba(255,255,255,.88);max-width:46ch;font-size:16px}
.skin-splash .fm-run{
  color:#fff;border-color:rgba(255,255,255,.35);margin-left:-20px;margin-right:-20px
}
.skin-splash .fm-ok{background:#fff;color:var(--fes-accent);box-shadow:0 10px 30px rgba(0,0,0,.25)}
.skin-splash .fm-x{position:fixed;top:16px;right:20px;font-size:26px;color:rgba(255,255,255,.85)}
.skin-splash .fm-x:hover{color:#fff}

/* ===== kiểu TICKET: như tấm vé / bao lì xì, có răng cưa hai bên ===== */
.skin-ticket .fm-card{
  padding:34px 28px 28px;border:0;border-radius:18px;
  background:
    radial-gradient(circle at 0 54%,transparent 13px,var(--surface) 13px) left/51% 100% no-repeat,
    radial-gradient(circle at 100% 54%,transparent 13px,var(--surface) 13px) right/51% 100% no-repeat;
  filter:drop-shadow(0 20px 50px rgba(0,0,0,.4)) drop-shadow(0 0 30px var(--fes-soft))
}
.skin-ticket .fm-art{
  display:inline-block;padding:0 26px 10px;border-bottom:2px dashed var(--line)
}
.skin-ticket .fm-run{
  margin:0 -28px 18px;border-top:2px dashed var(--line);border-bottom:2px dashed var(--line)
}
.skin-ticket .fm-ok{border-radius:10px}

/* ===== kiểu NEON: thẻ kính tối, viền phát sáng, chữ ART đổ quầng neon ===== */
.skin-neon .fm-card{
  background:rgba(12,10,18,.82);border:1px solid var(--fes-accent);
  box-shadow:0 0 0 1px var(--fes-soft),0 0 48px var(--fes-glow),inset 0 0 60px rgba(0,0,0,.6);
  backdrop-filter:blur(4px)
}
.skin-neon .fm-art{
  background:none;-webkit-text-fill-color:#fff;color:#fff;letter-spacing:.04em;
  text-shadow:0 0 10px #fff,0 0 28px var(--fes-accent),0 0 60px var(--fes-accent);
  animation:neon 2.4s ease-in-out infinite
}
@keyframes neon{50%{opacity:.78}}
.skin-neon .fm-title,.skin-neon .fm-sub{color:#fff}
.skin-neon .fm-sub{opacity:.75}
.skin-neon .fm-run{border-color:var(--fes-soft)}
.skin-neon .fm-x{color:rgba(255,255,255,.7)}

/* ===== kiểu POSTCARD: tấm bưu thiếp, có tem và dấu bưu điện ===== */
.skin-postcard .fm-card{
  padding:26px 26px 24px;border-radius:6px;border:1px solid var(--line);
  background:var(--surface);
  box-shadow:0 20px 50px rgba(0,0,0,.4),inset 0 0 0 6px var(--surface),
             inset 0 0 0 7px var(--fes-soft)
}
.skin-postcard .fm-card::after{             /* con tem góc phải */
  content:attr(data-stamp);position:absolute;top:16px;right:16px;
  width:54px;height:62px;display:flex;align-items:center;justify-content:center;
  font-size:22px;border:2px dashed var(--fes-accent);border-radius:3px;
  background:var(--accent-soft);transform:rotate(4deg)
}
.skin-postcard .fm-art{
  font-size:clamp(40px,9vw,70px);text-align:left;padding-left:4px
}
.skin-postcard .fm-title,.skin-postcard .fm-sub{text-align:left}
.skin-postcard .fm-sub{margin-left:0}
.skin-postcard .fm-run{margin:14px -26px 18px}
.skin-postcard .fm-ok{float:left}
.skin-postcard .fm-card::before{display:none}
.skin-postcard .fm-x{right:82px;top:22px}

/* ===== kiểu SCROLL: câu đối dọc hai bên, chữ ART ở giữa ===== */
.skin-scroll .fm-card{
  padding:34px 74px 28px;border:0;border-radius:14px;
  background:
    linear-gradient(var(--fes-g1),var(--fes-g2)) left/26px 100% no-repeat,
    linear-gradient(var(--fes-g2),var(--fes-g1)) right/26px 100% no-repeat,
    var(--surface);
  box-shadow:0 20px 56px rgba(0,0,0,.45)
}
.skin-scroll .fm-art{letter-spacing:.06em}
.skin-scroll .fm-run{margin:0 -74px 18px}

@media (prefers-reduced-motion:reduce){
  #petals{display:none}
  #festive .em,.fm-art,.fm-run span{animation:none}
  .fm-card,.fm-card::before{animation:none}
  .fm-title span{opacity:1;transform:none;animation:none}
}
@media (max-width:620px){
  #festive{font-size:13.5px;padding:12px 44px 12px 14px}
  #festive .hint{display:none}
}
"""


FESTIVE_JS = """
(function(){
  var EVENTS = __FESTIVE__, SKINS = __SKINS__;
  function pick(a){ return a[(Math.random() * a.length) | 0]; }

  /* ============ âm lịch Việt Nam (thuật toán Hồ Ngọc Đức, múi giờ +7) ============ */
  var TZ = 7;
  function jdFromDate(dd, mm, yy){
    var a = Math.floor((14 - mm) / 12), y = yy + 4800 - a, m = mm + 12 * a - 3;
    var jd = dd + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4)
           - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
    if (jd < 2299161) {
      jd = dd + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - 32083;
    }
    return jd;
  }
  function jdToDate(jd){
    var a, b, c, d, e, m, day, month, year;
    if (jd > 2299160) {
      a = jd + 32044; b = Math.floor((4 * a + 3) / 146097); c = a - Math.floor((b * 146097) / 4);
    } else { b = 0; c = jd + 32082; }
    d = Math.floor((4 * c + 3) / 1461);
    e = c - Math.floor((1461 * d) / 4);
    m = Math.floor((5 * e + 2) / 153);
    day = e - Math.floor((153 * m + 2) / 5) + 1;
    month = m + 3 - 12 * Math.floor(m / 10);
    year = b * 100 + d - 4800 + Math.floor(m / 10);
    return [day, month, year];
  }
  function newMoon(k){
    var T = k / 1236.85, T2 = T * T, T3 = T2 * T, dr = Math.PI / 180;
    var Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3;
    Jd1 += 0.00033 * Math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr);
    var M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3;
    var Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3;
    var F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3;
    var C1 = (0.1734 - 0.000393 * T) * Math.sin(M * dr) + 0.0021 * Math.sin(2 * dr * M);
    C1 = C1 - 0.4068 * Math.sin(Mpr * dr) + 0.0161 * Math.sin(dr * 2 * Mpr);
    C1 = C1 - 0.0004 * Math.sin(dr * 3 * Mpr);
    C1 = C1 + 0.0104 * Math.sin(dr * 2 * F) - 0.0051 * Math.sin(dr * (M + Mpr));
    C1 = C1 - 0.0074 * Math.sin(dr * (M - Mpr)) + 0.0004 * Math.sin(dr * (2 * F + M));
    C1 = C1 - 0.0004 * Math.sin(dr * (2 * F - M)) - 0.0006 * Math.sin(dr * (2 * F + Mpr));
    C1 = C1 + 0.0010 * Math.sin(dr * (2 * F - Mpr)) + 0.0005 * Math.sin(dr * (2 * Mpr + M));
    var deltat = T < -11
      ? 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
      : -0.000278 + 0.000265 * T + 0.000262 * T2;
    return Jd1 + C1 - deltat;
  }
  function sunLongitude(jdn){
    var T = (jdn - 2451545.0) / 36525, T2 = T * T, dr = Math.PI / 180;
    var M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2;
    var L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2;
    var DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * Math.sin(dr * M);
    DL += (0.019993 - 0.000101 * T) * Math.sin(dr * 2 * M) + 0.000290 * Math.sin(dr * 3 * M);
    var L = L0 + DL;
    L = L * dr; L = L - Math.PI * 2 * Math.floor(L / (Math.PI * 2));
    return L;
  }
  function getSunLongitude(dayNumber, tz){
    return Math.floor(sunLongitude(dayNumber - 0.5 - tz / 24) / Math.PI * 6);
  }
  function getNewMoonDay(k, tz){ return Math.floor(newMoon(k) + 0.5 + tz / 24); }
  function getLunarMonth11(yy, tz){
    var off = jdFromDate(31, 12, yy) - 2415021;
    var k = Math.floor(off / 29.530588853);
    var nm = getNewMoonDay(k, tz);
    if (getSunLongitude(nm, tz) >= 9) nm = getNewMoonDay(k - 1, tz);
    return nm;
  }
  function getLeapMonthOffset(a11, tz){
    var k = Math.floor((a11 - 2415021.076998695) / 29.530588853 + 0.5);
    var last, i = 1, arc = getSunLongitude(getNewMoonDay(k + 1, tz), tz);
    do { last = arc; i++; arc = getSunLongitude(getNewMoonDay(k + i, tz), tz); }
    while (arc != last && i < 14);
    return i - 1;
  }
  /* mùng lD tháng lM âm lịch của năm âm lY -> [ngày, tháng, năm] dương lịch */
  function lunarToSolar(lD, lM, lY, tz){
    var a11, b11, off, leapOff, leapMonth, k;
    if (lM < 11) { a11 = getLunarMonth11(lY - 1, tz); b11 = getLunarMonth11(lY, tz); }
    else { a11 = getLunarMonth11(lY, tz); b11 = getLunarMonth11(lY + 1, tz); }
    off = lM - 11;
    if (off < 0) off += 12;
    if (b11 - a11 > 365) {
      leapOff = getLeapMonthOffset(a11, tz);
      leapMonth = leapOff - 2;
      if (leapMonth < 0) leapMonth += 12;
      if (off >= leapOff) off += 1;
    }
    k = Math.floor(0.5 + (a11 - 2415021.076998695) / 29.530588853);
    return jdToDate(getNewMoonDay(k + off, tz) + lD - 1);
  }

  /* ============ chọn dịp của hôm nay ============ */
  function dayStart(y, m, d){ return new Date(y, m - 1, d, 0, 0, 0, 0).getTime(); }
  function windowOf(ev, year){
    var d, m;
    if (ev.lunar) {
      var p = ev.lunar.split('-');
      var s = lunarToSolar(parseInt(p[1], 10), parseInt(p[0], 10), year, TZ);
      d = s[0]; m = s[1]; year = s[2];
    } else {
      var q = ev.solar.split('-');
      m = parseInt(q[0], 10); d = parseInt(q[1], 10);
    }
    var base = dayStart(year, m, d);
    var DAY = 86400000;
    return [base - (ev.before || 0) * DAY, base + ((ev.after || 0) + 1) * DAY - 1];
  }

  var forced = null, off = false, wantSkin = null, wantLook = null;
  try {
    var qs = new URLSearchParams(location.search);
    var q = qs.get('festive');
    if (q === 'off') off = true; else if (q) forced = q;
    wantSkin = qs.get('skin');
    wantLook = qs.get('look');
  } catch(e){}
  if (off) return;

  var now = Date.now(), yr = new Date().getFullYear(), day = null, key = '';
  for (var i = 0; i < EVENTS.length && !day; i++) {
    var ev = EVENTS[i];
    if (forced) { if (ev.id === forced) { day = ev; key = 'preview-' + ev.id; } continue; }
    /* xét cả năm trước và năm sau: Tết âm lịch có thể rơi sát giao thừa dương lịch */
    for (var y = yr - 1; y <= yr + 1 && !day; y++) {
      var w = windowOf(ev, y);
      if (now >= w[0] && now <= w[1]) { day = ev; key = ev.id + '-' + y; }
    }
  }
  if (!day) return;

  /* ============ bốc ngẫu nhiên diện mạo + kiểu popup ============ */
  var th = (wantLook !== null && day.looks[wantLook]) ? day.looks[wantLook] : pick(day.looks);
  var skin = wantSkin || pick(day.skins || SKINS);
  var root = document.documentElement, S = root.style;
  S.setProperty('--fes-accent', th.accent);
  S.setProperty('--fes-soft', th.accent + '2b');
  S.setProperty('--fes-glow', th.accent + '66');
  S.setProperty('--fes-g1', th.grad[0]);
  S.setProperty('--fes-g2', th.grad[1]);
  S.setProperty('--fes-g3', th.grad[2]);
  root.classList.add('festive');

  function lang(){ return root.lang === 'en' ? 'en' : 'vi'; }
  function txt(){ return day[lang()]; }

  /* ---- băng rôn ---- */
  var bar = document.getElementById('festive');
  var msg = bar.querySelector('.msg');
  bar.querySelector('.em').textContent = th.emoji;
  function fillBar(){
    msg.innerHTML = txt().bar;
    msg.dataset.vi = day.vi.bar;
    var tmp = document.createElement('span');
    tmp.innerHTML = day.en.bar;
    msg.dataset.en = tmp.textContent;
  }
  fillBar();
  if (sessionStorage.getItem('festive-off') !== key) bar.classList.add('on');
  bar.querySelector('.x').addEventListener('click', function(){
    bar.classList.remove('on');
    root.classList.remove('festive');
    stop();
    try { sessionStorage.setItem('festive-off', key); } catch(e){}
  });

  /* ---- popup ập đến khi vào trang ---- */
  var modal = document.getElementById('fmodal');
  var mArt = modal.querySelector('.fm-art'), mTitle = modal.querySelector('.fm-title'),
      mSub = modal.querySelector('.fm-sub'), mRun = modal.querySelector('.fm-run span'),
      mOk = modal.querySelector('.fm-ok');
  function fill(){
    var t = txt();
    mArt.textContent = day.art;
    mTitle.textContent = '';
    /* từng chữ cái nổi lên lệch nhau một nhịp */
    t.title.split('').forEach(function(ch, i){
      var sp = document.createElement('span');
      sp.textContent = ch === ' ' ? '\\u00a0' : ch;
      sp.style.animationDelay = (0.25 + i * 0.022).toFixed(3) + 's';
      mTitle.appendChild(sp);
    });
    mSub.textContent = t.sub;
    mRun.textContent = t.run + t.run + t.run;
    mOk.textContent = t.ok;
  }
  function openModal(){
    if (!forced && sessionStorage.getItem('festive-modal') === key) return;
    fill();
    modal.className = 'skin-' + skin + ' on';
    modal.querySelector('.fm-card').setAttribute('data-stamp', th.emoji);
    var mx = innerWidth / 2, my = innerHeight / 2;
    burst(mx, my, 30);
    setTimeout(function(){ burst(mx - 160, my - 40, 16); }, 130);
    setTimeout(function(){ burst(mx + 160, my - 20, 16); }, 260);
  }
  function closeModal(){
    modal.classList.remove('on');
    try { sessionStorage.setItem('festive-modal', key); } catch(e){}
  }
  modal.querySelector('.fm-x').addEventListener('click', closeModal);
  mOk.addEventListener('click', function(ev){
    var r = ev.currentTarget.getBoundingClientRect();
    burst(r.left + r.width / 2, r.top + r.height / 2, 22);
    closeModal();
  });
  modal.addEventListener('click', function(ev){ if (ev.target === modal) closeModal(); });
  addEventListener('keydown', function(ev){ if (ev.key === 'Escape') closeModal(); });
  var langBtn = document.getElementById('lang');
  if (langBtn) langBtn.addEventListener('click', function(){
    setTimeout(function(){ if (modal.classList.contains('on')) fill(); }, 0);
  });

  /* ---- hạt rơi / bay lên, hình dạng theo từng dịp ---- */
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv = document.getElementById('petals'), cx = cv.getContext('2d');
  var W, H, bits = [], raf = null, DPR = Math.min(devicePixelRatio || 1, 2);
  var COLORS = th.colors, SHAPE = th.shape;
  var MODE = th.dir;                       /* down | up | float | fireworks */
  var UP = MODE === 'up' || MODE === 'float';

  function size(){
    W = cv.width = innerWidth * DPR;
    H = cv.height = innerHeight * DPR;
  }
  function spawn(edge){
    /* edge = true: thả từ ngoài màn hình; ngược lại rải sẵn khắp màn hình */
    var y;
    if (edge) y = UP ? H + Math.random() * 40 * DPR : -Math.random() * 40 * DPR;
    else y = Math.random() * H * 1.15 - H * 0.15;
    return {
      x: Math.random() * W, y: y,
      r: (5 + Math.random() * 7) * DPR,
      vx: 0,
      vy: (UP ? -1 : 1) * (MODE === 'float' ? 0.18 + Math.random() * 0.3
                                            : 0.45 + Math.random() * 0.95) * DPR,
      sway: (MODE === 'float' ? 1.6 + Math.random() * 1.8 : 0.6 + Math.random() * 1.4),
      phase: Math.random() * 6.283,
      spin: (Math.random() - 0.5) * (SHAPE === 'lantern' ? 0.012 : 0.05),
      ang: SHAPE === 'lantern' ? 0 : Math.random() * 6.283,
      c: COLORS[(Math.random() * COLORS.length) | 0],
      a: 0.6 + Math.random() * 0.4, life: 0
    };
  }
  function burst(px, py, n){
    for (var i = 0; i < (n || 16); i++){
      var ang = Math.random() * 6.283, sp = (1.5 + Math.random() * 4) * DPR;
      bits.push({
        x: px * DPR, y: py * DPR, r: (4 + Math.random() * 7) * DPR,
        vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp - 1.5 * DPR,
        sway: 0.4 + Math.random(), phase: Math.random() * 6.283,
        spin: (Math.random() - 0.5) * 0.3, ang: ang,
        c: COLORS[(Math.random() * COLORS.length) | 0], a: 1, life: 1
      });
    }
    if (!raf) start();
  }
  function shapePath(p){
    var r = p.r;
    if (SHAPE === 'dot'){ cx.beginPath(); cx.arc(0, 0, r * 0.75, 0, 6.283); cx.fill(); return; }
    if (SHAPE === 'star'){
      cx.beginPath();
      for (var i = 0; i < 10; i++){
        var rad = i % 2 ? r * 0.44 : r, a = Math.PI / 5 * i - Math.PI / 2;
        cx[i ? 'lineTo' : 'moveTo'](Math.cos(a) * rad, Math.sin(a) * rad);
      }
      cx.closePath(); cx.fill(); return;
    }
    if (SHAPE === 'heart'){
      cx.beginPath();
      cx.moveTo(0, r * 0.75);
      cx.bezierCurveTo(-r * 1.3, -r * 0.3, -r * 0.5, -r * 1.1, 0, -r * 0.45);
      cx.bezierCurveTo(r * 0.5, -r * 1.1, r * 1.3, -r * 0.3, 0, r * 0.75);
      cx.fill(); return;
    }
    if (SHAPE === 'confetti'){
      /* mảnh kim tuyến lật qua lật lại như rơi trong không khí */
      cx.scale(Math.cos(p.phase * 2.2), 1);
      cx.fillRect(-r * 0.45, -r * 0.8, r * 0.9, r * 1.6);
      return;
    }
    if (SHAPE === 'snow'){
      cx.strokeStyle = p.c; cx.lineWidth = Math.max(1, r * 0.16); cx.lineCap = 'round';
      cx.beginPath();
      for (var s6 = 0; s6 < 6; s6++){
        var a6 = Math.PI / 3 * s6;
        cx.moveTo(0, 0); cx.lineTo(Math.cos(a6) * r, Math.sin(a6) * r);
        cx.moveTo(Math.cos(a6) * r * 0.6, Math.sin(a6) * r * 0.6);
        cx.lineTo(Math.cos(a6 + 0.5) * r * 0.85, Math.sin(a6 + 0.5) * r * 0.85);
      }
      cx.stroke(); return;
    }
    if (SHAPE === 'coin'){
      cx.beginPath(); cx.ellipse(0, 0, r * Math.abs(Math.cos(p.phase * 1.6)) + r * 0.12, r, 0, 0, 6.283);
      cx.fill();
      cx.globalAlpha = p.a * 0.5; cx.fillStyle = '#fff';
      cx.beginPath(); cx.ellipse(-r * 0.2, -r * 0.25, r * 0.18, r * 0.3, 0, 0, 6.283); cx.fill();
      return;
    }
    if (SHAPE === 'lantern'){
      cx.beginPath();
      cx.ellipse(0, 0, r * 0.72, r, 0, 0, 6.283);
      cx.fill();
      cx.globalAlpha = p.a * 0.35;                 /* quầng sáng quanh đèn */
      cx.beginPath(); cx.arc(0, 0, r * 1.7, 0, 6.283); cx.fill();
      return;
    }
    /* petal: hai đường cong khép lại */
    cx.beginPath();
    cx.moveTo(0, -r);
    cx.bezierCurveTo(r, -r * 0.5, r * 0.75, r * 0.75, 0, r);
    cx.bezierCurveTo(-r * 0.75, r * 0.75, -r, -r * 0.5, 0, -r);
    cx.fill();
  }
  function draw(p){
    cx.save();
    cx.translate(p.x, p.y);
    cx.rotate(p.ang);
    cx.globalAlpha = p.a;
    cx.fillStyle = p.c;
    shapePath(p);
    cx.restore();
  }
  function tick(){
    cx.clearRect(0, 0, W, H);
    for (var i = bits.length - 1; i >= 0; i--){
      var p = bits[i];
      p.phase += 0.016;
      p.ang += p.spin;
      if (p.life){                      /* hạt bung ra: bay rồi rơi và nhạt dần */
        p.vy += 0.12 * DPR; p.vx *= 0.985;
        p.x += p.vx; p.y += p.vy; p.a -= 0.012;
        if (p.a <= 0 || p.y - p.r > H) { bits.splice(i, 1); continue; }
      } else {
        p.y += p.vy;
        p.x += Math.sin(p.phase) * p.sway * DPR;
        var gone = UP ? (p.y + p.r < 0) : (p.y - p.r > H);
        if (gone) bits[i] = spawn(true);
      }
      draw(bits[i]);
    }
    raf = requestAnimationFrame(tick);
  }
  function start(){
    if (raf) return;
    size();
    if (!bits.length && !reduce && MODE !== 'fireworks'){
      var n = Math.min(44, Math.round(innerWidth / 28));
      for (var i = 0; i < n; i++) bits.push(spawn(false));
    }
    raf = requestAnimationFrame(tick);
  }
  function stop(){ if (raf) { cancelAnimationFrame(raf); raf = null; } cx.clearRect(0, 0, W || 0, H || 0); }

  addEventListener('resize', function(){ stop(); bits = []; start(); });
  /* tab ẩn thì dừng hẳn, khỏi ngốn pin */
  addEventListener('visibilitychange', function(){ document.hidden ? stop() : start(); });
  /* bấm vào chỗ trống -> hạt bung ra tại đó; bấm vào link thì để yên */
  addEventListener('click', function(ev){
    if (!root.classList.contains('festive')) return;
    if (ev.target.closest('a,button,input')) return;
    burst(ev.clientX, ev.clientY);
  });
  if (!reduce) start();
  /* pháo hoa: tự bắn từng chùm ở vị trí ngẫu nhiên phía trên màn hình */
  if (MODE === 'fireworks' && !reduce){
    setInterval(function(){
      if (document.hidden || !root.classList.contains('festive')) return;
      burst(innerWidth * (0.15 + Math.random() * 0.7),
            innerHeight * (0.12 + Math.random() * 0.4), 18);
    }, 1400);
  }
  setTimeout(openModal, 180);
})();
"""
