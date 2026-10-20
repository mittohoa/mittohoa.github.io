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

FEATURED = 3               # số app đưa lên khu Nổi bật, chọn theo lượt tải thật
MIN_DOWNLOADS = 50         # dưới mức này thì không hiện huy hiệu lượt tải

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
    "congviec": {"vi": "Công việc & tổ chức", "en": "Work & organising"},
    "doisong":  {"vi": "Đi lại & đời sống", "en": "Everyday life"},
    "media":    {"vi": "Ảnh, nhạc & video", "en": "Photos, music & video"},
    "hoctap":   {"vi": "Học & luyện tập", "en": "Learn & practice"},
    "game":     {"vi": "Game", "en": "Games"},
    "congcu":   {"vi": "Công cụ máy tính", "en": "Desktop tools"},
    "khac":     {"vi": "Khác", "en": "Others"},
}
GROUP_ORDER = ["congviec", "doisong", "media", "hoctap", "game", "congcu", "khac"]

CURATED = {
    "workpilot-app": "congviec", "tudu-app": "congviec", "khomi-app": "congviec",
    "memora-app": "congviec", "munneh-app": "congviec",
    "meanything-app": "congviec",

    "toidi": "doisong", "xaxi-app": "doisong", "gio-chuan": "doisong",
    "nhipnha": "doisong", "homeassistant-app": "doisong",

    "media-kit": "media", "media-tool": "media", "cam-coach-web": "media",
    "lyra-player": "media", "ghienmuzik-app": "media", "ytb-web": "media",

    "vung-dat-tri-thuc": "hoctap", "zone-game": "hoctap", "rubik-resolved": "hoctap",
    "uke-flow": "hoctap", "el-coach": "hoctap", "examlab-web": "hoctap",

    "chinese-chess-web": "game", "chess-game-web": "game", "starvelocity": "game",

    "veo-kam": "congcu", "news-hub-releases": "congcu",
}

# Repo không hiện: trang gốc, kho dữ liệu, kênh phát hành, repo chỉ chứa policy
SKIP = {
    "mittohoa.github.io", "toidi-data", "fidgy-release", "human-app",
    # Trùng sản phẩm — giữ bản mới nhất, bỏ các bản cũ. Đổi nếu chọn repo khác.
    "xaxi-wallet",                              # trùng xaxi-app (mới hơn, có lượt tải)
    "media-app", "mediahub_app", "mediahub-app",  # trùng media-tool (Media Hub)
}

# Mô tả tiếng Anh. Thiếu repo nào thì bản EN dùng tạm mô tả tiếng Việt.
DESC_EN = {
    "workpilot-app": "Work timer, quantity logging and AI reports, synced across devices in realtime and offline-first. Android and Windows.",
    "munneh-app": "A cross-platform personal hub: tasks, AI, finances, health, notification analysis, smart home. Local-first and private.",
    "khomi-app": "Khomi keeps links, messages, photos, files and notes in one store on your own device, then helps you find them again.",
    "memora-app": "Throw anything in and Memora reads, analyses, sorts it and reminds you to look again. A personal archive with AI.",
    "tudu-app": "TMA handles tasks and team collaboration: subtasks, projects, deadlines and an AI-assisted input box. Flutter and Supabase.",
    "meanything-app": "A cross-platform personal app that saves, summarises and finds anything with AI: video, audio, images, memes, films.",

    "xaxi-app": "A personal expense book built for speed: very fast entry, multi-currency, cloud sync, works offline.",
    "toidi": "Bus and metro directions for Ho Chi Minh City and Hanoi: stop alerts, multi-leg routes, nearby places, works without a signal.",
    "nhipnha": "FAM Health - keeping track of your family's health.",
    "homeassistant-app": "Keeps track of where your household things really are. Offline-first, AI, QR codes, warranties, sync. Find anything in under 10 seconds.",
    "gio-chuan": "An accurate clock synced to atomic time, every time zone at hand, working even when you are offline.",

    "ytb-web": "A personal app for YouTube creators: track video performance, diagnose problems and get alerts at thresholds you set.",
    "lyra-player": "AURA floats song lyrics over the screen for music playing in any app, and doubles as a full music player. Windows and Android.",
    "media-kit": "Tidies your photo library and shows you which shots could look better. Every bit of analysis runs on your device.",
    "cam-coach-web": "A camera app that tells you what to adjust while you are still holding the phone up. Six modes, fully on-device.",
    "media-tool": "Two tools for photo libraries: Winnow finds duplicates on Windows, Media Hub manages photos, video and music on Android.",
    "ghienmuzik-app": "A multi-source Flutter music player for Android: local files, streaming, radio, podcasts and a free AI assistant.",

    "rubik-resolved": "An Android app that teaches 3x3 Rubik solving step by step, reads a real cube from a photo, and times your speedsolves.",
    "uke-flow": "Learn ukulele in Vietnamese on Android. A path for absolute beginners, 28 chords with finger-by-finger guidance.",
    "zone-game": "8 games and 96 stages to get ready for first grade. No ads, no in-app purchases, no internet needed, no data collected.",
    "examlab-web": "Multiple-choice practice across courses and difficulty levels. Take tests on your phone or in a browser, offline included.",
    "vung-dat-tri-thuc": "A 3D adventure game where children aged 6 to 11 learn while they play.",
    "el-coach": "Public pages for the English Coach Android app.",

    "chess-game-web": "Chess in Vietnamese: a three-dimensional board, full FIDE rules, 8 engine levels, 5000 tactics puzzles, game analysis.",
    "chinese-chess-web": "Vietnamese chess in Vietnamese: learn the rules from scratch, 8 engine levels, play over the local network. No account, no ads.",
    "starvelocity": "Ranking open source by total stars keeps the same decade-old projects on top forever. StarVelocity measures how fast a project is growing instead.",

    "news-hub-releases": "A personal app that pulls GitHub repositories and news on tech, programming, AI and digital transformation into one feed.",
    "veo-kam": "Veo-Kam controls a Windows PC from an Android phone over the local network. TLS encrypted, and the PIN never leaves your devices.",
}

# Chuỗi giao diện
UI = {
    "about":    {"vi": "Về mình", "en": "About"},
    "projects": {"vi": "Dự án", "en": "Projects"},
    "view":     {"vi": "Xem trang &rarr;", "en": "Visit &rarr;"},
    "contact":  {"vi": "Liên hệ", "en": "Contact"},
    "featured": {"vi": "Nổi bật", "en": "Featured"},
    "downloads": {"vi": "lượt tải", "en": "downloads"},
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


def url_ok(u):
    """Icon trỏ vào file không tồn tại thì trang sẽ hiện ô ảnh vỡ — kiểm trước."""
    try:
        req = urllib.request.Request(u, method="HEAD",
                                     headers={"User-Agent": "build_site/1.0"})
        return urllib.request.urlopen(req, timeout=8).status == 200
    except Exception:
        return False


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

    # ưu tiên icon vuông; og:image thường là banner ngang, nhét vào ô 44x44 sẽ méo.
    # (["\'])(.*?)\2 bám đúng dấu nháy bao ngoài — data-URI hay chứa nháy bên trong
    for pat in (r'<link[^>]+rel=(["\'])apple-touch-icon\1[^>]+href=(["\'])(.*?)\2',
                r'<link[^>]+rel=(["\'])(?:shortcut )?icon\1[^>]+href=(["\'])(.*?)\2',
                r'<meta[^>]+property=(["\'])og:image\1[^>]+content=(["\'])(.*?)\2'):
        m = re.search(pat, html, re.I | re.S)
        if m:
            icon = urllib.parse.urljoin(url, m.group(3).strip())
            if icon.startswith("data:") or url_ok(icon):
                out["icon"] = icon
                break

    # mô tả dự phòng cho repo bỏ trống description
    for pat in (r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)'):
        m = re.search(pat, html, re.I)
        if m:
            out["desc"] = re.sub(r"\s+", " ", m.group(1)).strip()
            break

    m = re.search(r"play\.google\.com/store/apps/details\?id=([\w\.]+)", html)
    if m:
        out["play"] = m.group(1)
    return out


def fetch_downloads(repo):
    """Tổng lượt tải của mọi file đính kèm trong tất cả release."""
    rels = gh_json("repos/%s/%s/releases?per_page=100" % (OWNER, repo)) or []
    return sum(a.get("download_count", 0) for rel in rels for a in rel.get("assets", []))


def gh_json(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True,
                       encoding="utf-8")
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def collect(refresh=False):
    cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
    groups = {}
    for r in gh_repos():
        if r["name"] in SKIP or r["fork"] or r["archived"]:
            continue
        if not r["has_pages"]:
            continue

        url = "https://%s.github.io/%s/" % (OWNER, r["name"])
        meta = cache.get(r["name"])
        if meta is None or refresh:
            print("  doc trang %s ..." % r["name"])
            meta = fetch_meta(url)
            meta["downloads"] = fetch_downloads(r["name"])
            cache[r["name"]] = meta

        # mô tả: ưu tiên meta description của trang app vì đó là lời giới thiệu
        # sản phẩm; description của repo nhiều khi chỉ ghi "trang công khai, policy"
        desc_vi = meta.get("desc", "").strip() or (r.get("description") or "").strip()
        if not desc_vi:
            continue

        title = meta.get("title") or r["name"].replace("-", " ").title()
        # bỏ phần "Tên app — " lặp ở đầu mô tả, nhưng chỉ khi nó đúng là tiền tố;
        # tách bừa ở dấu ":" giữa câu sẽ xén mất nội dung
        m = re.match(r"\s*%s\s*[—–\-:]\s+" % re.escape(title), desc_vi)
        if m:
            desc_vi = desc_vi[m.end():]
        desc_vi = desc_vi[:1].upper() + desc_vi[1:]

        groups.setdefault(CURATED.get(r["name"], "khac"), []).append({
            "title": title,
            "vi": desc_vi,
            "en": DESC_EN.get(r["name"], desc_vi),
            "icon": meta.get("icon", ""),
            "play": meta.get("play", ""),
            "downloads": meta.get("downloads", 0),
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

/* huy hiệu lượt tải / Google Play */
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.badge{
  font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:999px;
  background:var(--accent-soft);color:var(--accent);white-space:nowrap
}
.badge.play{background:#1a7f3718;color:#1a9e45}

/* khu Nổi bật: thẻ to hơn, logo lớn hơn */
.grid.big{grid-template-columns:1fr}
@media (min-width:620px){.grid.big{grid-template-columns:repeat(3,1fr)}}
.grid.big .card{padding:22px 22px 18px;border-color:var(--accent);
  background:linear-gradient(180deg,var(--accent-soft) 0%,var(--surface) 46%)}
.grid.big .ico{width:58px;height:58px;flex:0 0 58px;border-radius:14px}
.grid.big h3{font-size:19px}
.grid.big p{font-size:14.5px}

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


def card(it):
    icon = ('<img class="ico" src="%s" alt="" loading="lazy" width="44" height="44">'
            % esc(it["icon"])) if it["icon"] else (
            '<span class="ico ph">%s</span>' % esc(it["title"][:1].upper()))

    badges = []
    if it["downloads"] >= MIN_DOWNLOADS:
        badges.append('<span class="badge" data-en="%d %s">%d %s</span>'
                      % (it["downloads"], UI["downloads"]["en"],
                         it["downloads"], UI["downloads"]["vi"]))
    if it["play"]:
        badges.append('<span class="badge play">Google Play</span>')
    badges = ('<div class="badges">%s</div>' % "".join(badges)) if badges else ""

    return ('        <a class="card" href="%s">\n'
            '          <div class="head">%s<h3>%s</h3></div>\n'
            '          %s<p data-en="%s">%s</p>\n'
            '          <span class="go" data-en="%s">%s</span>\n'
            '        </a>'
            % (esc(it["url"]), icon, esc(it["title"]), badges,
               esc(it["en"]), esc(it["vi"]),
               UI["view"]["en"], UI["view"]["vi"]))


def render(groups):
    total = sum(len(v) for v in groups.values())
    has_photo = os.path.exists(PHOTO)

    links = []
    for i, (label, url) in enumerate(ME["links"]):
        cls = ' class="primary"' if i == 0 else ""
        links.append('<a%s href="%s" rel="me noopener">%s</a>' % (cls, esc(url), esc(label)))
    links.append('<a href="mailto:%s">Email</a>' % esc(ME["email"]))

    # Nổi bật = nhiều lượt tải nhất; app đã lên Google Play thắng khi bằng điểm
    allitems = [it for v in groups.values() for it in v]
    top = sorted(allitems, key=lambda x: (x["downloads"], bool(x["play"])),
                 reverse=True)[:FEATURED]
    top = [it for it in top if it["downloads"] > 0]
    topurls = {it["url"] for it in top}
    for key in groups:
        groups[key] = [it for it in groups[key] if it["url"] not in topurls]

    body = []
    if top:
        body.append(
            '    <section>\n      %s\n      <div class="grid big">\n%s\n'
            '      </div>\n    </section>'
            % (t(UI, "featured", "h2"), "\n".join(card(it) for it in top)))

    for key in GROUP_ORDER:
        items = groups.get(key)
        if not items:
            continue
        # trong nhóm: app nhiều lượt tải lên trước, rồi tới app vừa cập nhật
        cards = [card(it) for it in sorted(
            items, key=lambda x: (x["downloads"], x["pushed"]), reverse=True)]
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
