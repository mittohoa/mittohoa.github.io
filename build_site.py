# -*- coding: utf-8 -*-
"""
Sinh index.html cho trang gốc mittohoa.github.io — trang cá nhân song ngữ Việt/Anh.

Dữ liệu dự án lấy tự động:
  - danh sách repo + mô tả  : gh api
  - tên app thật + logo     : đọc <title> và <link rel=icon> của chính trang app
                              (cache ở site-data.json, làm mới bằng --refresh)

Chạy:
  python build_site.py             dựng lại index.html từ cache
  python build_site.py --refresh   đọc lại tên/logo từ các trang app rồi dựng
  python build_site.py --dry       chỉ in danh sách, không ghi file
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

OWNER = "mittohoa"
CACHE = "site-data.json"
PHOTO = "me.jpg"           # chân dung tròn đầu trang
OG = "og.jpg"              # ảnh 1200x630 hiện khi chia sẻ link lên FB/Zalo/LinkedIn
ICON = "icon-180.png"      # favicon + icon khi lưu trang ra màn hình chính

# ======================= THÔNG TIN CÁ NHÂN — SỬA Ở ĐÂY =======================
# Các chỗ đánh dấu TODO là placeholder, cần thay bằng thông tin thật.
ME = {
    "name": "Dương Minh Hòa",
    "handle": "Mít tờ HÒA",
    "email": "mittohoa@gmail.com",
    "tagline": {
        "vi": "Lập trình viên · Ứng dụng Android, Windows & Web",
        "en": "Software Developer · Android, Windows & Web apps",
    },
    # Giữ lại câu chủ đạo của trang cũ hoaduong.github.io
    "slogan": {
        "lead": {"vi": "Mình làm phần mềm nhỏ", "en": "I build small software"},
        "accent": {"vi": "bằng sự tò mò lớn", "en": "with big curiosity"},
    },
    "intro": {
        "vi": "Mình làm ứng dụng nhỏ cho những việc hằng ngày — đi lại, học hành, "
              "dọn thư viện ảnh, chơi cờ. Phần lớn chạy offline ngay trên máy bạn, "
              "không thu thập dữ liệu.",
        "en": "I build small apps for everyday things — commuting, learning, photo "
              "cleanup, chess. Most of them run fully offline on your device and "
              "collect nothing.",
    },
    "about": {
        "vi": "Mình làm phần mềm ở TP.HCM, mạnh nhất là ứng dụng đa nền tảng với "
              "Flutter và .NET. Nhưng dân IT không nhất thiết phải khô khan: ngoài "
              "giờ code thì mình ôm đàn, chơi cờ, và hay bị đẩy lên làm người hoạt "
              "náo mỗi khi có sự kiện đông người. Thói quen của mình đơn giản — thấy "
              "việc gì cứ lặp đi lặp lại và phiền phiền là về làm luôn một cái app "
              "cho nhẹ đầu; phần lớn thứ trên trang này ra đời kiểu đó. Có gì cần "
              "hỏi về Android, Windows hay web thì cứ nhắn, mình trả lời nhiệt tình.",
        "en": "I build software in Ho Chi Minh City, mostly cross-platform apps with "
              "Flutter and .NET. But developers don't have to be the quiet type: off "
              "the clock I'm the one with a guitar, a chessboard, and a microphone "
              "whenever a room needs someone to liven it up. My habit is simple — "
              "whenever something repetitive annoys me, I go home and turn it into an "
              "app. That is how most of the things on this page were born. Questions "
              "about Android, Windows or the web? Message me, I answer with real "
              "enthusiasm.",
    },
    # Thứ tự hiện trên trang. Link đầu tiên được tô đậm.
    "links": [
        ("GitHub", "https://github.com/mittohoa"),
        ("YouTube", "https://www.youtube.com/@mittoHOA"),
        ("Fanpage", "https://www.facebook.com/MrHoaOfficial"),
        # ("LinkedIn", "https://linkedin.com/in/TODO"),      # bỏ # nếu có
    ],
}

# ============================== PHÂN NHÓM DỰ ÁN ==============================
GROUPS = {
    "doisong": {"vi": "Đi lại & đời sống", "en": "Everyday life"},
    "hoctap":  {"vi": "Học & luyện tập", "en": "Learn & practice"},
    "congcu":  {"vi": "Ảnh & công cụ máy tính", "en": "Photos & desktop tools"},
    "game":    {"vi": "Game", "en": "Games"},
    "khac":    {"vi": "Khác", "en": "Others"},
}
GROUP_ORDER = ["doisong", "hoctap", "congcu", "game", "khac"]

CURATED = {
    "toidi": "doisong", "xaxi-wallet": "doisong", "gio-chuan": "doisong",
    "nhipnha": "doisong",

    "vung-dat-tri-thuc": "hoctap", "zone-game": "hoctap", "rubik-resolved": "hoctap",
    "uke-flow": "hoctap", "el-coach": "hoctap", "examlab-web": "hoctap",

    "media-kit": "congcu", "media-tool": "congcu", "cam-coach-web": "congcu",
    "veo-kam": "congcu", "news-hub-releases": "congcu",

    "chinese-chess-web": "game", "chess-game-web": "game",
}

# Repo không hiện: trang gốc, kho dữ liệu, kênh phát hành, repo chỉ chứa policy
SKIP = {"mittohoa.github.io", "toidi-data", "fidgy-release", "human-app", "ytb-web"}

# Mô tả tiếng Anh. Thiếu repo nào thì bản EN dùng tạm mô tả tiếng Việt.
DESC_EN = {
    "toidi": "Buses and metro in Ho Chi Minh City and Hanoi: website, policies, downloads.",
    "xaxi-wallet": "Personal expense tracking on web, Windows and Android. Offline, your data stays on your device.",
    "gio-chuan": "An accurate clock for web, Android and Windows. It measures and publishes its own real sync error.",
    "nhipnha": "Web app and public pages (privacy policy, account deletion). Source code lives in a private repo.",
    "vung-dat-tri-thuc": "Landing page and privacy policy for the Vùng Đất Tri Thức game.",
    "zone-game": "A Vietnamese educational game for ages 3-6. APK download and overview.",
    "rubik-resolved": "Landing and download page for the 3x3 Rubik learn, solve and practice app.",
    "uke-flow": "A Vietnamese ukulele learning app. Landing page and installers.",
    "el-coach": "Public pages for the English Coach Android app.",
    "examlab-web": "Prebuilt web version of ExamLab. Source in a private repo, updated by CI.",
    "media-kit": "Tidies your photo library and points out which shots could look better. All analysis runs on device.",
    "media-tool": "Winnow for Windows: finds duplicate photos, even the ones stripped of their metadata.",
    "cam-coach-web": "Overview, downloads and update channel.",
    "veo-kam": "Control a Windows PC from an Android phone over the local network.",
    "news-hub-releases": "Downloads and releases. A personal app that pulls GitHub repos and tech news into one feed.",
    "chinese-chess-web": "Vietnamese chess (Cờ Tướng): landing page, play in browser, releases.",
    "chess-game-web": "Chess in Vietnamese: landing page and releases.",
}

# Chuỗi giao diện
UI = {
    "about":    {"vi": "Về mình", "en": "About"},
    "projects": {"vi": "Dự án", "en": "Projects"},
    "view":     {"vi": "Xem trang &rarr;", "en": "Visit &rarr;"},
    "contact":  {"vi": "Liên hệ", "en": "Contact"},
    "stat1":    {"vi": "ứng dụng đang phát hành", "en": "apps published"},
    "stat2":    {"vi": "nền tảng: Android · Windows · Web", "en": "platforms: Android · Windows · Web"},
    "stat3":    {"vi": "dữ liệu nằm trên máy bạn", "en": "your data stays on your device"},
    "offline":  {"vi": "Offline", "en": "Offline"},
    "auto":     {"vi": "Trang tự sinh từ danh sách repo công khai.",
                 "en": "This page is generated from the public repository list."},
}


# ================================ LẤY DỮ LIỆU ================================
def gh_repos():
    out = subprocess.run(
        ["gh", "api", "users/%s/repos?per_page=100&sort=pushed" % OWNER],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    return json.loads(out)


def fetch_meta(url):
    """Lấy tên app và logo từ chính trang của app đó."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "build_site/1.0"})
        html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", "ignore")
    except Exception as e:
        print("  ! khong doc duoc %s (%s)" % (url, e.__class__.__name__))
        return {}

    out = {}
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    if m:
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        for sep in ("—", "·", "|", " - ", ":"):
            if sep in t:
                t = t.split(sep)[0].strip()
                break
        out["title"] = t

    # ưu tiên icon vuông; og:image thường là banner ngang, nhét vào ô 44x44 sẽ méo
    for pat in (r'<link[^>]+rel=["\']apple-touch-icon["\'][^>]+href=["\']([^"\']+)',
                r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]+href=["\']([^"\']+)',
                r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)'):
        m = re.search(pat, html, re.I)
        if m:
            out["icon"] = urllib.parse.urljoin(url, m.group(1))
            break
    return out


def collect(refresh=False):
    cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
    groups = {}
    for r in gh_repos():
        if r["name"] in SKIP or r["fork"] or r["archived"]:
            continue
        if not r["has_pages"] or not (r.get("description") or "").strip():
            continue

        url = "https://%s.github.io/%s/" % (OWNER, r["name"])
        meta = cache.get(r["name"])
        if meta is None or refresh:
            print("  doc trang %s ..." % r["name"])
            meta = fetch_meta(url)
            cache[r["name"]] = meta

        desc_vi = r["description"].strip()
        title = meta.get("title") or r["name"].replace("-", " ").title()
        for sep in ("—", " - ", ":"):
            if desc_vi.startswith(title) and sep in desc_vi:
                desc_vi = desc_vi.split(sep, 1)[1].strip()
                break

        groups.setdefault(CURATED.get(r["name"], "khac"), []).append({
            "title": title,
            "vi": desc_vi,
            "en": DESC_EN.get(r["name"], desc_vi),
            "icon": meta.get("icon", ""),
            "url": url,
            "pushed": r["pushed_at"][:10],
        })

    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)
    return groups


# ================================== HTML ====================================
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def t(el, key, tag="span", cls=""):
    """Thẻ song ngữ: hiện tiếng Việt, giữ bản tiếng Anh ở data-en để nút VI/EN đổi."""
    cls = ' class="%s"' % cls if cls else ""
    return '<%s%s data-en="%s">%s</%s>' % (tag, cls, esc(el[key]["en"]), esc(el[key]["vi"]), tag)


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f7f8fa; --surface:#fff; --line:#e4e8ee;
  --ink:#171a20; --muted:#646c7a; --accent:#2f5fd0; --accent-soft:#eaf0fd;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0e1116; --surface:#161a22; --line:#242a35;
    --ink:#e9edf3; --muted:#949db0; --accent:#7aa2f7; --accent-soft:#1b2436;
  }
}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased
}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}
a{color:var(--accent)}

/* nút đổi ngôn ngữ */
#lang{
  position:fixed;top:16px;right:16px;z-index:9;
  padding:7px 14px;border:1px solid var(--line);border-radius:999px;
  background:var(--surface);color:var(--ink);font:600 13px/1 inherit;cursor:pointer
}
#lang:hover{border-color:var(--accent);color:var(--accent)}

/* hero */
header{padding:72px 0 42px}
.hero{display:flex;gap:30px;align-items:flex-start;flex-wrap:wrap}
.portrait{
  width:132px;height:132px;flex:0 0 132px;border-radius:50%;object-fit:cover;
  border:3px solid var(--surface);box-shadow:0 2px 18px rgba(0,0,0,.14)
}
.hero-text{flex:1 1 380px;min-width:280px}
.eyebrow{font-size:12.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent);margin:0 0 10px}
h1{margin:0 0 4px;font-size:clamp(32px,6vw,46px);line-height:1.1;letter-spacing:-.02em}
.sub{margin:0 0 14px;font-size:16px;color:var(--muted)}
.slogan{margin:0 0 18px;font-size:clamp(19px,2.6vw,25px);line-height:1.35;letter-spacing:-.01em}
.slogan em{color:var(--accent);font-style:italic}
.intro{margin:0 0 24px;max-width:60ch;font-size:16.5px}
.links{display:flex;flex-wrap:wrap;gap:10px}
.links a{
  display:inline-block;padding:8px 16px;border:1px solid var(--line);border-radius:999px;
  background:var(--surface);color:var(--ink);text-decoration:none;font-size:14px;font-weight:600;
  transition:border-color .15s,color .15s
}
.links a:hover{border-color:var(--accent);color:var(--accent)}
.links a.primary{background:var(--accent);border-color:var(--accent);color:#fff}

/* stats */
.stats{display:flex;flex-wrap:wrap;gap:34px;margin-top:42px;padding-top:26px;border-top:1px solid var(--line)}
.stat b{display:block;font-size:26px;line-height:1.2;letter-spacing:-.01em}
.stat span{font-size:13px;color:var(--muted)}

/* nội dung */
section{padding:44px 0 0}
h2{margin:0;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.about p{margin:14px 0 0;max-width:64ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin-top:16px}
.card{
  display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);
  border-radius:12px;padding:18px 18px 15px;text-decoration:none;color:inherit;
  transition:border-color .15s,transform .15s
}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card .head{display:flex;align-items:center;gap:11px;margin:0 0 10px}
.card .ico{width:44px;height:44px;flex:0 0 44px;border-radius:11px;object-fit:cover;
  background:var(--accent-soft);border:1px solid var(--line)}
.card .ico.ph{display:flex;align-items:center;justify-content:center;font-weight:700;font-size:19px;color:var(--accent)}
.card h3{margin:0;font-size:16.5px;letter-spacing:-.01em}
.card p{margin:0 0 14px;font-size:14px;color:var(--muted);line-height:1.55;flex:1}
.card .go{font-size:13px;font-weight:600;color:var(--accent)}

footer{margin-top:58px;padding:26px 0 56px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
footer a{color:var(--accent);text-decoration:none}
footer a:hover{text-decoration:underline}
.note{margin-top:8px;font-size:12.5px}
"""

JS = """
(function(){
  var btn=document.getElementById('lang');
  function apply(l){
    document.documentElement.lang=l;
    document.querySelectorAll('[data-en]').forEach(function(e){
      if(e.dataset.vi===undefined) e.dataset.vi=e.textContent;
      e.textContent = (l==='en') ? e.dataset.en : e.dataset.vi;
    });
    btn.textContent = (l==='en') ? 'Tiếng Việt' : 'English';
    try{ localStorage.setItem('lang',l); }catch(e){}
  }
  var saved=null;
  try{ saved=localStorage.getItem('lang'); }catch(e){}
  apply(saved || ((navigator.language||'').slice(0,2)==='vi' ? 'vi' : 'en'));
  btn.addEventListener('click',function(){
    apply(document.documentElement.lang==='en' ? 'vi' : 'en');
  });
})();
"""


def render(groups):
    total = sum(len(v) for v in groups.values())
    has_photo = os.path.exists(PHOTO)

    links = []
    for i, (label, url) in enumerate(ME["links"]):
        cls = ' class="primary"' if i == 0 else ""
        links.append('<a%s href="%s" rel="me noopener">%s</a>' % (cls, esc(url), esc(label)))
    links.append('<a href="mailto:%s">Email</a>' % esc(ME["email"]))

    body = []
    for key in GROUP_ORDER:
        items = groups.get(key)
        if not items:
            continue
        cards = []
        for it in sorted(items, key=lambda x: x["pushed"], reverse=True):
            icon = ('<img class="ico" src="%s" alt="" loading="lazy" width="44" height="44">'
                    % esc(it["icon"])) if it["icon"] else \
                   ('<span class="ico ph">%s</span>' % esc(it["title"][:1].upper()))
            cards.append(
                '        <a class="card" href="%s">\n'
                '          <div class="head">%s<h3>%s</h3></div>\n'
                '          <p data-en="%s">%s</p>\n'
                '          <span class="go" data-en="%s">%s</span>\n'
                '        </a>'
                % (esc(it["url"]), icon, esc(it["title"]),
                   esc(it["en"]), esc(it["vi"]),
                   UI["view"]["en"], UI["view"]["vi"])
            )
        body.append(
            '    <section>\n      %s\n      <div class="grid">\n%s\n      </div>\n    </section>'
            % (t(GROUPS, key, "h2"), "\n".join(cards))
        )

    photo_tag = ('<img class="portrait" src="%s" alt="%s" width="132" height="132">'
                 % (PHOTO, esc(ME["name"]))) if has_photo else ""
    og_image = ('\n<meta property="og:image" content="https://%s.github.io/%s">'
                '\n<meta property="og:image:width" content="1200">'
                '\n<meta property="og:image:height" content="630">'
                '\n<meta name="twitter:card" content="summary_large_image">'
                % (OWNER, OG)) if os.path.exists(OG) else ""
    return """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(name)s — %(tagline_vi)s</title>
<meta name="description" content="%(intro_short)s">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="%(icon)s">
<link rel="apple-touch-icon" href="%(icon)s">
<link rel="canonical" href="https://%(owner)s.github.io/">
<meta property="og:title" content="%(name)s — %(slogan_full)s">
<meta property="og:description" content="%(intro_short)s">
<meta property="og:url" content="https://%(owner)s.github.io/">
<meta property="og:type" content="website">%(og_image)s
<style>%(css)s</style>
</head>
<body>
<button id="lang" type="button">English</button>
<div class="wrap">
  <header>
    <div class="hero">
      %(photo)s
      <div class="hero-text">
        <p class="eyebrow" data-en="%(tagline_en)s">%(tagline_vi)s</p>
        <h1>%(name)s</h1>
        <p class="sub">%(handle)s</p>
        <p class="slogan"><span data-en="%(slogan_lead_en)s">%(slogan_lead_vi)s</span>
          <em data-en="%(slogan_accent_en)s">%(slogan_accent_vi)s</em></p>
        <p class="intro" data-en="%(intro_en)s">%(intro_vi)s</p>
        <nav class="links">%(links)s</nav>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><b>%(total)d</b><span data-en="%(stat1_en)s">%(stat1_vi)s</span></div>
      <div class="stat"><b>3</b><span data-en="%(stat2_en)s">%(stat2_vi)s</span></div>
      <div class="stat"><b data-en="%(offline_en)s">%(offline_vi)s</b><span data-en="%(stat3_en)s">%(stat3_vi)s</span></div>
    </div>
  </header>

  <section class="about">
    %(about_h)s
    <p data-en="%(about_en)s">%(about_vi)s</p>
  </section>

%(body)s

  <footer>
    <span data-en="%(contact_en)s">%(contact_vi)s</span>:
    <a href="mailto:%(email)s">%(email)s</a> ·
    <a href="https://github.com/%(owner)s">github.com/%(owner)s</a>
    <div class="note" data-en="%(auto_en)s">%(auto_vi)s</div>
  </footer>
</div>
<script>%(js)s</script>
</body>
</html>
""" % {
        "name": esc(ME["name"]), "handle": esc(ME["handle"]), "email": esc(ME["email"]),
        "tagline_vi": esc(ME["tagline"]["vi"]), "tagline_en": esc(ME["tagline"]["en"]),
        "intro_vi": esc(ME["intro"]["vi"]), "intro_en": esc(ME["intro"]["en"]),
        "intro_short": esc(ME["intro"]["vi"][:150]),
        "slogan_lead_vi": esc(ME["slogan"]["lead"]["vi"]),
        "slogan_lead_en": esc(ME["slogan"]["lead"]["en"]),
        "slogan_accent_vi": esc(ME["slogan"]["accent"]["vi"]),
        "slogan_accent_en": esc(ME["slogan"]["accent"]["en"]),
        "about_h": t(UI, "about", "h2"),
        "about_vi": esc(ME["about"]["vi"]), "about_en": esc(ME["about"]["en"]),
        "stat1_vi": esc(UI["stat1"]["vi"]), "stat1_en": esc(UI["stat1"]["en"]),
        "stat2_vi": esc(UI["stat2"]["vi"]), "stat2_en": esc(UI["stat2"]["en"]),
        "stat3_vi": esc(UI["stat3"]["vi"]), "stat3_en": esc(UI["stat3"]["en"]),
        "offline_vi": esc(UI["offline"]["vi"]), "offline_en": esc(UI["offline"]["en"]),
        "contact_vi": esc(UI["contact"]["vi"]), "contact_en": esc(UI["contact"]["en"]),
        "auto_vi": esc(UI["auto"]["vi"]), "auto_en": esc(UI["auto"]["en"]),
        "slogan_full": esc(ME["slogan"]["lead"]["vi"] + " " + ME["slogan"]["accent"]["vi"]),
        "owner": OWNER, "css": CSS, "js": JS, "links": "".join(links),
        "total": total, "body": "\n\n".join(body),
        "photo": photo_tag, "og_image": og_image, "icon": ICON,
    }


if __name__ == "__main__":
    groups = collect(refresh="--refresh" in sys.argv)
    for key in GROUP_ORDER:
        for it in groups.get(key, []):
            print("%-24s %-22s %s" % (GROUPS[key]["vi"], it["title"], it["url"]))
    print("\nTong cong: %d du an" % sum(len(v) for v in groups.values()))

    todo = [k for k, v in {"email": ME["email"], "about": ME["about"]["vi"]}.items()
            if "TODO" in v] + \
           [n for n, u in ME["links"] if "TODO" in u]
    if todo:
        print("CON PLACEHOLDER CAN THAY: " + ", ".join(todo))
    if not os.path.exists(PHOTO):
        print("CHUA CO ANH: dat file '%s' vao thu muc nay" % PHOTO)

    if "--dry" not in sys.argv:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(render(groups))
        print("Da ghi index.html")
