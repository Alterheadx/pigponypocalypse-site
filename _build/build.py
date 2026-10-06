# собирает сайт на всех языках: python3 _build/build.py
# en — в корне (/, /presskit/), остальные — в /<код>/ и /<код>/presskit/
import json, os, re, sys
B = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(B)
sys.path.insert(0, B)
from i18n_ru_zh import RU, ZH
from i18n_ja_ko import JA, KO

EN = json.load(open(os.path.join(B, "i18n", "en.json"), encoding="utf-8"))
SITE = "https://pigponypocalypse.com"
LANGS = [  # код папки, lang, подпись, шрифт для CJK
    ("", "en", "EN", None, EN),
    ("zh", "zh-Hans", "中文", "SYSTEM-ZH", ZH),
    ("ja", "ja", "日本語", "Noto+Sans+JP", JA),
    ("ko", "ko", "한국어", "Noto+Sans+KR", KO),
    ("ru", "ru", "RU", None, RU),
]
PAGES = [("landing.html", ""), ("presskit.html", "presskit/")]

LANG_CSS = """<style>
.langs{position:absolute;top:calc(env(safe-area-inset-top,0px) + 16px);right:clamp(16px,3vw,32px);z-index:5;display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.langs a{font:500 14px/1 var(--label);letter-spacing:.06em;color:var(--lav);text-decoration:none;padding:7px 9px;border-radius:4px;background:rgba(18,10,24,.55)}
.langs a:hover{color:#fff;background:rgba(230,21,122,.35)}
.langs a[aria-current]{color:#fff;background:var(--pink)}
html[lang="ru"] .tag,html[lang="ru"] .tagline{max-width:none}
html[lang="ru"] .tag b,html[lang="ru"] .tagline em{display:block}
%s
</style>"""

CJK_CSS = """html{--display:"Bebas Neue",%(f)s,sans-serif;--label:"Oswald",%(f)s,sans-serif;--body:"Roboto",%(f)s,sans-serif}
h2,h3,.tag,.tagline,.menu a,.final h2{font-weight:900;letter-spacing:.01em;font-synthesis:none;line-height:1.2}
.menu a{font-size:clamp(28px,3.2vw,38px)}
.tag,.tagline{max-width:none}
.tag b,.tagline em{display:block}
html[lang="ko"] body{word-break:keep-all}
html[lang="ja"] body{line-break:strict}"""

# первый заход на английскую главную: язык браузера → своя версия (выбор пользователя запоминается)
REDIRECT = """<script>
(function(){try{
  var saved=localStorage.getItem("ppp_lang");
  if(saved===null){var l=(navigator.language||"").toLowerCase();
    var m=l.indexOf("zh")===0?"zh":l.indexOf("ja")===0?"ja":l.indexOf("ko")===0?"ko":l.indexOf("ru")===0?"ru":"";
    if(m)location.replace("/"+m+"/");}
}catch(e){}})();
</script>"""

REMEMBER = """<script>
document.querySelectorAll(".langs a").forEach(function(a){a.addEventListener("click",function(){try{localStorage.setItem("ppp_lang",a.dataset.lang)}catch(e){}})});
</script>"""


def url(code, sub):
    return "/" + (code + "/" if code else "") + sub


def render(tpl, sub, code, lang, label, font, strings):
    out = tpl
    missing = []
    def sub_key(m):
        k = m.group(1)
        if k == "base":
            return "/" + code if code else ""
        v = strings.get(k)
        if v is None:
            missing.append(k)
            v = EN[k]
        return v
    out = re.sub(r"\{\{([a-z0-9_]+)\}\}", sub_key, out)
    if missing:
        print(f"  [{lang}] нет перевода: {', '.join(sorted(set(missing)))}")
    out = out.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    # og:url и hreflang
    out = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}{url(code, sub)}">', out)
    alt = "".join(f'\n<link rel="alternate" hreflang="{l}" href="{SITE}{url(c, sub)}">' for c, l, *_ in LANGS)
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{url("", sub)}">'
    head_extra = alt
    if font and font != "SYSTEM-ZH":
        head_extra += f'\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={font}:wght@400;700;900&display=swap">'
    fam = '"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC"' if font == "SYSTEM-ZH" else (f'"{font.replace("+", " ")}"' if font else "")
    head_extra += "\n" + LANG_CSS % (CJK_CSS % {"f": fam} if font else "")
    if not code and sub == "":
        head_extra += "\n" + REDIRECT
    out = out.replace("</head>", head_extra + "\n</head>", 1)
    # переключатель языка — в шапку
    links = "".join(
        f'<a href="{url(c, sub)}" hreflang="{l}" lang="{l}" data-lang="{c or "en"}"{" aria-current=\"page\"" if c == code else ""}>{lb}</a>'
        for c, l, lb, *_ in LANGS)
    nav = f'\n  <nav class="langs" aria-label="Language">{links}</nav>'
    out = re.sub(r'(<header class="(?:stage|hero)">)', r"\1" + nav.replace("\\", "\\\\"), out, count=1)
    out = out.replace("</body>", REMEMBER + "\n</body>", 1)
    return out


for tpl_name, sub in PAGES:
    tpl = open(os.path.join(B, tpl_name), encoding="utf-8").read()
    for code, lang, label, font, strings in LANGS:
        html = render(tpl, sub, code, lang, label, font, strings)
        d = os.path.join(ROOT, code, sub) if code else os.path.join(ROOT, sub)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
        print("ok", os.path.relpath(os.path.join(d, "index.html"), ROOT))
