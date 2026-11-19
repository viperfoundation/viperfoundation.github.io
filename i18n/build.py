#!/usr/bin/env python3
"""Build the localized landing pages from the English index.html.

index.html is the only template: edit English there, then run `python3 i18n/build.py`.
It fills the <!--i18n:...--> blocks (hreflang links, language switcher, footer languages
line) in index.html and writes <dir>/index.html for every other language, swapping each
English string from en.txt for its translation in <lang>.txt.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://viperfoundation.github.io/"
# (strings file, folder, html lang / hreflang). Order = order in the switcher.
LANGS = [("en", "", "en"), ("ru", "ru", "ru"), ("pt-br", "pt-br", "pt-BR"), ("es", "es", "es-MX"), ("uk", "uk", "uk")]
APP_LANGS = "English, Русский"  # Viper/Localizable.xcstrings: source en, only ru localized
# FLAG: set True once the build with es/uk/pt-BR UI (branch l10n-es-uk-pt) is live on the App Store,
# then rebuild. Until then the footer keeps the two shipped app languages.
APP_L10N_SHIPPED = False
if APP_L10N_SHIPPED:
    APP_LANGS = "English, Русский, Español, Українська, Português"
# Languages the App Store description is localized in (Apple lookup API, 2026-11-19).
STORE_LANGS = "English, Русский, Português (Brasil), Español (México), Українська"
# Pages that use app screenshots in their own language: img/<folder>/iphone-*.jpg
LOCAL_SHOTS = {"ru"}
# Gallery on these pages: localized app screens in frames (screenshots-1.5.34/<locale>-l10n/) for
# profile, chat, AI draft and notes -> img/<lang>/l10n-framed-*; Route and People Nearby have no
# localized screen yet, so they stay English screens with translated headlines -> img/<lang>/framed-*.
# The hero chat is the localized raw screen (img/<lang>/iphone-4-chat.jpg); the TON Drop radar stays English.
FRAMED_SHOTS = {"es", "uk", "pt-br"}
L10N_GALLERY = ("1-profile", "4-chat", "6-ai-draft", "8-notes")
HERO_L10N = ("4-chat", "5-ai-answer", "6-ai-draft", "8-notes")
# App Store storefront per page (all five carry the app: iTunes lookup, 2026-11-19).
STOREFRONT = {"": "us", "ru": "ru", "pt-br": "br", "es": "mx", "uk": "ua"}
GLOBE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>')


def load(name):
    out = {}
    for line in open(os.path.join(ROOT, "i18n", name + ".txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line and not line.startswith("#"):
            k, v = line.split(" = ", 1)
            out[k] = v
    return out


def fill(html, block, content):
    pat = re.compile(r"<!--i18n:%s-->.*?<!--/i18n:%s-->" % (block, block), re.S)
    assert len(pat.findall(html)) == 1, block
    return pat.sub(lambda m: "<!--i18n:%s-->%s<!--/i18n:%s-->" % (block, content, block), html)


def page(template, en, t, folder, code):
    up = "../" if folder else ""
    html = template
    for k in sorted(en, key=lambda k: -len(en[k])):  # longest first, so short keys never cut into long ones
        if k.startswith("_"):
            continue
        assert en[k] in html, "not in index.html: " + k
        html = html.replace(en[k], t[k])
    html = html.replace('<html lang="en">', '<html lang="%s">' % code, 1)
    if folder:
        for attr in ('src="', 'href="', 'data-lottie="'):
            for d in ("img/", "lotties/", "js/"):
                html = html.replace(attr + d, attr + up + d)
    html = html.replace("apps.apple.com/us/app/", "apps.apple.com/%s/app/" % STOREFRONT[folder])
    if folder in FRAMED_SHOTS:
        g = '<figure><div class="phone"><img loading="lazy" src="../img/'
        assert html.count(g + "iphone-") == 6
        for n in L10N_GALLERY:
            html = html.replace(g + "iphone-" + n, g + folder + "/l10n-framed-" + n)
        html = html.replace(g + "iphone-", g + folder + "/framed-")
        # Hero carousel: localized raw screens (screenshots-1.5.34/src/screens/<locale>-iphone-*.png at 600 px);
        # People Nearby has no localized screen yet, so slide 2 stays English.
        for n in HERO_L10N:
            s = 'src="../img/iphone-%s.jpg"' % n  # also matches data-src (slides 2-5)
            assert html.count(s) == 1, n  # only the hero uses these
            html = html.replace(s, 'src="../img/%s/iphone-%s.jpg"' % (folder, n))
    # Mac AI Chat screenshot in the page's language (replica: viper-marketing/appstore/mac-ai-chat-l10n/replica).
    mac = 'src="%simg/en/mac-ai-chat' % up  # AI section and hero (-window.jpg)
    assert html.count(mac) == 2
    html = html.replace(mac, 'src="%simg/%s/mac-ai-chat' % (up, folder or "en"))
    if folder == "ru":  # the original session is Russian: no "translated" line
        html = html.replace('\n      <p class="note mac-tr"></p>', "")
        assert "mac-tr" not in html
    if folder in LOCAL_SHOTS:
        html = html.replace('src="../img/iphone-', 'src="../img/%s/iphone-' % folder)
    links = ['<link rel="canonical" href="%s%s">' % (SITE, folder + "/" if folder else "")]
    items = []
    for name, f, c in LANGS:
        lt = load(name)
        links.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (c, SITE, f + "/" if f else ""))
        href = up + (f + "/" if f else "") or "./"
        cur = ' aria-current="page"' if f == folder else ""
        items.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (href, c, c, cur, lt["_name"]))
    links.append('<link rel="alternate" hreflang="x-default" href="%s">' % SITE)
    html = fill(html, "links", "\n" + "\n".join(links) + "\n")
    html = fill(html, "switcher", '<details class="lang"><summary aria-label="%s: %s">%s%s</summary>'
                '<div class="menu">%s</div></details>' % (t["_lang"], t["_name"], GLOBE, t["_code"], "".join(items)))
    html = fill(html, "langs", "<p>%s: %s · %s: %s</p>" % (t["_app"], APP_LANGS, t["_store"], STORE_LANGS))
    return html


def main():
    en = load("en")
    path = os.path.join(ROOT, "index.html")
    template = open(path, encoding="utf-8").read()
    for name, folder, code in LANGS:
        t = load(name)
        missing = set(en) - set(t)
        assert not missing, (name, sorted(missing))
        html = page(template, en, t, folder, code)
        out = os.path.join(ROOT, folder, "index.html") if folder else path
        if folder:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            assert "img/" not in html.replace("../img/", "").replace("io/img/", ""), name
        if name != "en":
            left = [k for k in en if not k.startswith("_") and en[k] in html and en[k] not in t[k]]
            assert not left, (name, left)  # every English string got replaced
        open(out, "w", encoding="utf-8").write(html)
        print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
