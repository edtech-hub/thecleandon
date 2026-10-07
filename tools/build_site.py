#!/usr/bin/env python3
"""The Clean Don prototype generator. Usage: python3 tools/build_site.py .
Section structure and class names follow Shopify's Dawn theme (see sources.md). Output is plain HTML
with Shopify-style URLs (/collections/..., /products/..., /cart, /pages/...) so it maps onto a theme rebuild."""
import hashlib, html, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (P, COLLECTIONS, PRO_SHOP, JOBS, label, vlabel, money, by_collection, col_min)

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
BASE_URL = "https://thecleandon.whitephoenixconsulting.com/"
STORE = "https://thecleandon.com/"
PHONE = "(469) 283-8431"
TEL = "+14692838431"
EMAIL = "Info@TheCleanDon.com"
FACEBOOK = "https://www.facebook.com/TheCleanDon/"
BUILD = time.strftime("%Y%m%d%H%M%S")
META = json.load(open(os.path.join(OUT, "tools", "img-meta.json")))
LOGO_W, LOGO_H = META["logo"]["w"], META["logo"]["h"]
esc = html.escape


def ver(rel):
    with open(os.path.join(OUT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def svg(paths, cls="icon", vb="0 0 24 24", sw="1.8", fill="none"):
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{fill}" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>')


ICON = {
    "cart": svg('<path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7a3 3 0 0 1 6 0"/>'),
    "menu": svg('<path d="M3 6h18M3 12h18M3 18h18"/>'),
    "close": svg('<path d="M18 6 6 18M6 6l12 12"/>'),
    "phone": svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "caret": svg('<path d="m6 9 6 6 6-6"/>', "icon icon-caret", sw="2"),
    "minus": svg('<path d="M5 12h14"/>', sw="2"),
    "plus": svg('<path d="M12 5v14M5 12h14"/>', sw="2"),
    "trash": svg('<path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/>'),
    "check": svg('<path d="M20 6 9 17l-5-5"/>', sw="2.2"),
    "camera": svg('<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>'),
    "tag": svg('<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
    "van": svg('<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>'),
    "error": svg('<circle cx="12" cy="12" r="10"/><path d="M12 7v6M12 17h.01"/>', sw="2"),
    "facebook": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M14 8V6.2c0-.8.2-1.2 1.4-1.2H17V2h-2.6C11.6 2 10.6 3.4 10.6 5.8V8H8.5v3h2.1v11H14V11h2.6l.4-3z"/></svg>',
    "star": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2.5l2.94 5.96 6.56.95-4.75 4.63 1.12 6.54L12 17.5l-5.87 3.08 1.12-6.54L2.5 9.41l6.56-.95z"/></svg>',
    "pin": svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
}
PLACEHOLDER = ('<svg class="placeholder-svg" viewBox="0 0 120 120" aria-hidden="true" focusable="false"><rect x="38" y="44" width="44" height="32" rx="3" '
               'fill="none" stroke="currentColor" stroke-width="2"/><circle cx="50" cy="55" r="4" fill="currentColor"/><path d="M40 74l14-12 9 8 7-5 12 9" fill="none" stroke="currentColor" stroke-width="2"/></svg>')


def srcset(root, key):
    m = META[key]
    return ", ".join(f"{root}assets/img/{key}-{w}.webp {w if w <= m['w'] else m['w']}w" for w in m["widths"])


def img(root, key, alt, sizes, eager=False, extra=""):
    m = META[key]
    default = m["widths"][-1] if len(m["widths"]) < 3 else m["widths"][1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    h = round(m["h"] * (min(default, m["w"]) / m["w"]))
    return (f'<img src="{root}assets/img/{key}-{default}.webp" srcset="{srcset(root, key)}" sizes="{sizes}" '
            f'width="{min(default, m["w"])}" height="{h}" alt="{esc(alt)}" {load} decoding="async"{extra}>')


def media(root, key, alt, sizes, cls="media--square", contain=False, eager=False, extra=""):
    if not key:
        return f'<div class="media media--transparent {cls} ph" title="Photo needed">{PLACEHOLDER}</div>'
    c = " media--transparent media--contain" if contain else ""
    return f'<div class="media {cls}{c}">{img(root, key, alt, sizes, eager, extra)}</div>'


def price_html(p, large=False):
    cls = "price price--large" if large else "price"
    multi = len({v["price"] for v in p["variants"]}) > 1 or p.get("calc")
    if p.get("estimate"):
        return f'<div class="{cls}"><span class="price-item price-item--regular">Free estimate</span></div>'
    if multi:
        return (f'<div class="{cls}"><span class="visually-hidden">Regular price</span><span class="price__from">From</span>'
                f'<span class="price-item price-item--regular" data-price>{money(p["price_min"])}</span></div>')
    return f'<div class="{cls}"><span class="visually-hidden">Regular price</span><span class="price-item price-item--regular" data-price>{money(p["price_min"])}</span></div>'


def purl(root, p):
    return f'{root}products/{p["handle"]}/'


def card_button(p):
    if p.get("estimate"):
        return "Book a free estimate"
    if p["options"] or p.get("calc"):
        return "Choose options"
    return "Add to cart"


def product_card(root, p, order=0, heading="h3"):
    alt = p["title"]
    return f"""<li class="grid__item scroll-trigger animate--slide-in" style="--animation-order:{order % 4}">
  <div class="card-wrapper product-card-wrapper" data-vt-key="p-{p['handle']}">
    <div class="card__media">{media(root, p.get("img"), alt, "(min-width: 990px) 280px, (min-width: 750px) 30vw, 46vw", "media--square media--hover-effect", p.get("contain"))}</div>
    <div class="card-information">
      <{heading} class="card__heading"><a href="{purl(root, p)}" data-vt="p-{p['handle']}">{esc(p['title'])}</a></{heading}>
      <p class="card__caption">{esc(p['card'])}</p>
      {price_html(p)}
    </div>
  </div>
</li>"""


def head(root, title, desc, path, extra=""):
    full = f"{title} | The Clean Don" if title != "The Clean Don" else "The Clean Don | Carpet, upholstery and home cleaning in Dallas-Fort Worth"
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<!-- Prototype preview. Remove this noindex line at launch. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#10144a">
<meta property="og:site_name" content="The Clean Don">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&amp;display=swap">
<link rel="stylesheet" href="{root}assets/css/theme.css?v={ver('assets/css/theme.css')}">
<meta name="site-build" content="{BUILD}">
<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");window.ROOT="{root}";</script>
{VT_HEAD}
{SELF_HEAL.replace("ROOT", root).replace("BUILD", BUILD)}
<script type="speculationrules">{json.dumps(SPECULATION)}</script>
{extra}<script src="{root}assets/js/catalog.js?v={ver('assets/js/catalog.js')}" defer></script>
<script src="{root}assets/js/theme.js?v={ver('assets/js/theme.js')}" defer></script>
</head>"""


SPECULATION = {"prerender": [{"source": "document", "where": {"and": [{"href_matches": "/*"},
               {"not": {"href_matches": "/*\\?*"}}, {"not": {"selector_matches": "[data-no-prerender]"}}]}, "eagerness": "moderate"}]}
SELF_HEAL = ('<script>(function(){if(!window.fetch)return;fetch("ROOTversion.json",{cache:"no-store"})'
             '.then(function(r){return r.json()}).then(function(v){if(v.build&&v.build!=="BUILD"){var k="reload-"+v.build;'
             'try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1")}catch(e){}location.reload()}}).catch(function(){})})();</script>')
# Element expands into the next page: names the matching element on the new page before first render.
VT_HEAD = r"""<script>window.addEventListener("pagereveal",function(e){if(!e.viewTransition)return;var d;try{d=JSON.parse(sessionStorage.getItem("vt")||"null");sessionStorage.removeItem("vt")}catch(x){}if(!d||Date.now()-d.t>4000)return;var el=document.querySelector('[data-vt-target="'+d.key+'"]');if(!el)return;el.style.viewTransitionName="expand";e.viewTransition.finished.finally(function(){el.style.viewTransitionName=""})});</script>"""


def preview_bar():
    return ('<div class="preview-bar" role="note"><span><strong>Preview</strong> made by White Phoenix for The Clean Don. Prices and options come from your current store.</span>'
            '<span class="ph-chip">Dashed boxes</span><span>mark details we still need from you.</span></div>')


def announcement(root):
    return (f'<div class="announcement-bar" role="region" aria-label="Announcement"><p class="announcement-bar__message">'
            f'Every price is on the page before you book. Questions? Call <a href="tel:{TEL}">{PHONE}</a></p></div>')


NAV = [("Home", ""), ("Services", "collections/all/"), ("Pro shop", "collections/pro-shop/"), ("About", "pages/about/"), ("Contact", "pages/contact/")]


def mega(root):
    cards = "".join(
        f'<li><a class="mega-menu__card" href="{root}collections/{c["handle"]}/">{media(root, c["img"], "", "220px", "", c["contain"])}'
        f'<strong>{esc(c["short"])}</strong><span>{"From " + money(col_min(c["handle"])) if col_min(c["handle"]) else "Free estimates"}</span></a></li>'
        for c in COLLECTIONS)
    return (f'<div class="mega-menu__content" id="MegaMenu-services"><ul class="mega-menu__list page-width list-unstyled">{cards}</ul>'
            f'<div class="mega-menu__foot page-width"><span>Not sure which one you need? Call <a href="tel:{TEL}">{PHONE}</a>.</span>'
            f'<a href="{root}collections/all/" class="animate-arrow">Shop all services {ICON["arrow"]}</a></div></div>')


def header(root, active):
    items = []
    for l, h in NAV:
        cur = ' aria-current="page"' if active == h else ""
        if h == "collections/all/":
            items.append(f'<li class="mega-menu" data-mega><button type="button" class="header__menu-item" aria-expanded="false" aria-controls="MegaMenu-services"{cur}>'
                         f'<span>{l}</span>{ICON["caret"]}</button>{mega(root)}</li>')
        else:
            items.append(f'<li><a href="{root}{h}" class="header__menu-item"{cur}><span>{l}</span></a></li>' if h else
                         f'<li><a href="{root or "./"}" class="header__menu-item"{cur}><span>{l}</span></a></li>')
    sub = "".join(f'<li><a href="{root}collections/{c["handle"]}/">{esc(c["title"])}</a></li>' for c in COLLECTIONS)
    drawer = []
    for l, h in NAV:
        cur = ' aria-current="page"' if active == h else ""
        href = f"{root}{h}" if h else (root or "./")
        extra = f'<ul class="menu-drawer__submenu list-unstyled">{sub}<li><a href="{root}collections/all/">Shop all services</a></li></ul>' if h == "collections/all/" else ""
        drawer.append(f'<li><a class="menu-drawer__menu-item" href="{href}"{cur}>{l}</a>{extra}</li>')
    drawer.append(f'<li><a class="menu-drawer__menu-item" href="{root}pages/reviews/">Reviews</a></li><li><a class="menu-drawer__menu-item" href="{root}pages/careers/">Careers</a></li>')
    home = root or "./"
    return f"""<a class="skip-to-content-link button visually-hidden" href="#MainContent">Skip to content</a>
{preview_bar()}
{announcement(root)}
<div class="section-header">
  <header class="header page-width">
    <button type="button" class="header__icon header__icon--menu" aria-label="Menu" aria-expanded="false" aria-controls="menu-drawer" data-menu-open>{ICON["menu"]}</button>
    <div class="header__heading"><a href="{home}" class="header__heading-link" aria-label="The Clean Don, home" data-logo><img class="header__heading-logo" src="{root}assets/img/logo.webp" width="{LOGO_W}" height="{LOGO_H}" alt="The Clean Don"></a></div>
    <nav class="header__inline-menu" aria-label="Main"><ul class="list-menu list-menu--inline list-unstyled">{"".join(items)}</ul></nav>
    <div class="header__icons">
      <a class="header__phone" href="tel:{TEL}">{ICON["phone"].replace('class="icon"', 'class="icon" width="18" height="18"')}{PHONE}</a>
      <a class="header__icon header__icon--call" href="tel:{TEL}" aria-label="Call {PHONE}">{ICON["phone"]}</a>
      <a class="header__icon header__icon--cart" id="cart-icon-bubble" href="{root}cart/" aria-label="Cart" data-cart-open>{ICON["cart"]}<span class="cart-count-bubble" data-cart-count hidden>0</span></a>
    </div>
  </header>
</div>
<div class="menu-drawer" id="menu-drawer" aria-hidden="true">
  <div class="menu-drawer__overlay" data-menu-close></div>
  <div class="menu-drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="menu-drawer__head"><img src="{root}assets/img/logo.webp" width="{LOGO_W}" height="{LOGO_H}" alt="The Clean Don" loading="lazy"><button type="button" class="drawer__close" aria-label="Close menu" data-menu-close>{ICON["close"]}</button></div>
    <ul class="menu-drawer__menu list-unstyled">{"".join(drawer)}</ul>
    <div class="menu-drawer__utility"><a class="button" href="{root}collections/all/">Shop all services</a><p>Or call <a class="link" href="tel:{TEL}">{PHONE}</a></p></div>
  </div>
</div>"""


def cart_drawer(root):
    return f"""<div class="cart-drawer" id="CartDrawer" aria-hidden="true">
  <div class="cart-drawer__overlay" data-cart-close></div>
  <div class="drawer__inner" role="dialog" aria-modal="true" aria-labelledby="CartDrawer-heading" tabindex="-1">
    <div class="drawer__header"><h2 class="drawer__heading" id="CartDrawer-heading">Your cart</h2><button class="drawer__close" type="button" aria-label="Close" data-cart-close>{ICON["close"]}</button></div>
    <div class="drawer__contents" data-cart-items></div>
    <div class="drawer__inner-empty" data-cart-empty hidden>
      <p class="cart__empty-text">Your cart is empty</p>
      <p class="muted">As clean as it gets. Let's find something that isn't.</p>
      <a class="button" href="{root}collections/all/">Continue shopping</a>
    </div>
    <div class="drawer__footer" data-cart-footer hidden>
      <div class="totals"><h3 class="totals__total">Estimated total</h3><p class="totals__total-value" data-cart-total>$0.00</p></div>
      <p class="tax-note" data-cart-note>Taxes, discounts and travel calculated at checkout.</p>
      <div class="cart__ctas"><button type="button" class="button button--full-width" data-checkout>Check out</button><a class="button button--secondary button--full-width" href="{root}cart/">View cart</a></div>
    </div>
  </div>
</div>
<div class="modal" id="CheckoutModal" aria-hidden="true">
  <div class="modal__overlay" data-modal-close></div>
  <div class="modal__content" role="dialog" aria-modal="true" aria-labelledby="CheckoutModal-title">
    <button type="button" class="drawer__close modal__close" aria-label="Close" data-modal-close>{ICON["close"]}</button>
    <h2 class="h3" id="CheckoutModal-title">This is where Shopify checkout opens</h2>
    <p>On the live store, this button takes you to Shopify's secure checkout: Shop Pay, cards, your service address and contact details. Nothing is charged in this preview.</p>
    <p class="muted" data-modal-summary></p>
    <div class="buttons"><button type="button" class="button" data-modal-close>Back to the store</button></div>
  </div>
</div>"""


def footer(root):
    cols = "".join(f'<li><a href="{root}collections/{c["handle"]}/">{esc(c["short"])}</a></li>' for c in COLLECTIONS)
    return f"""<footer class="footer">
  <div class="page-width">
    <div class="footer__blocks">
      <div class="footer__brand">
        <a class="footer__logo" href="{root or './'}"><img src="{root}assets/img/logo.webp" width="{LOGO_W}" height="{LOGO_H}" alt="The Clean Don" loading="lazy"></a>
        <p>Carpet, upholstery, home and car cleaning across Dallas-Fort Worth.</p>
        <ul class="list-social list-unstyled"><li><a class="list-social__link" href="{FACEBOOK}" target="_blank" rel="noopener">{ICON["facebook"]}<span class="visually-hidden">Facebook</span></a></li></ul>
      </div>
      <div><h2 class="footer-block__heading">Services</h2><ul class="footer-block__details-content list-unstyled">{cols}<li><a href="{root}collections/all/">Shop all</a></li></ul></div>
      <div><h2 class="footer-block__heading">Company</h2><ul class="footer-block__details-content list-unstyled">
        <li><a href="{root}pages/about/">About us</a></li><li><a href="{root}pages/reviews/">Reviews</a></li>
        <li><a href="{root}pages/careers/">Careers</a></li><li><a href="{root}collections/pro-shop/">Pro shop</a></li>
        <li><a href="{root}pages/contact/">Contact</a></li><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
      <div class="footer__newsletter">
        <h2 class="footer-block__heading">Subscribe to our emails</h2>
        <p>Seasonal offers and the odd cleaning tip. No spam.</p>
        <form class="newsletter-form" data-newsletter novalidate>
          <div class="field"><input class="field__input" id="NewsletterForm" type="email" name="email" placeholder="Email" autocomplete="email" required><label class="field__label" for="NewsletterForm">Email</label>
          <button type="submit" class="newsletter-form__button" aria-label="Subscribe">{ICON["arrow"]}</button></div>
          <p class="form__message" data-newsletter-msg hidden></p>
        </form>
      </div>
    </div>
    <div class="footer__content-bottom">
      <p>&copy; <span data-year>2026</span>, The Clean Don. THECLEANDON INC. <a href="{STORE}policies/terms-of-service">Terms of service</a> &middot; <a href="{STORE}policies/refund-policy">Refund policy</a></p>
      <button type="button" class="footer__stain" data-stain title="Click me">Stains on this page: <span data-stain-count>0</span><span class="stain-dot" aria-hidden="true"></span></button>
    </div>
  </div>
</footer>"""


def mobile_actions(root):
    return (f'<div class="mobile-actions" role="region" aria-label="Quick actions"><a class="button button--secondary" href="tel:{TEL}">{ICON["phone"]}Call</a>'
            f'<a class="button" href="{root}collections/all/" data-mobile-primary>Shop services</a></div>')


def page(path, title, desc, active, body, depth=None, actions=True, extra_head="", body_class="", root=None):
    depth = path.count("/") if depth is None else depth
    root = "../" * depth if root is None else root
    doc = f"""{head(root, title, desc, path, extra_head)}
<body class="{body_class}{' has-mobile-actions' if actions else ''}">
{header(root, active)}
<main id="MainContent" class="content-for-layout" role="main" tabindex="-1">
{body(root)}
</main>
{footer(root)}
{cart_drawer(root)}
{mobile_actions(root) if actions else ''}
</body>
</html>
"""
    target = os.path.join(OUT, path, "index.html") if path and not path.endswith(".html") else os.path.join(OUT, path or "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as f:
        f.write(doc)
    print("wrote", os.path.relpath(target, OUT))


# ---------- shared sections ----------

def breadcrumbs(root, *crumbs):
    parts = [f'<a href="{root or "./"}">Home</a>']
    for i, (t, h) in enumerate(crumbs):
        parts.append(f'<a href="{root}{h}">{esc(t)}</a>' if h else f'<span aria-current="page">{esc(t)}</span>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumbs">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'


def trust(root):
    art = {
        "price": '<svg class="multicolumn-card__icon" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#eceaf7"/><path d="M14 16h17l12 12-15 15-14-14z" fill="#1a22c4"/><circle cx="21" cy="23" r="3" fill="#eceaf7"/><path d="M27 33.5c1 1.2 2.4 1.8 3.9 1.6 1.5-.2 2.4-1.1 2.3-2.2-.1-1.3-1.4-1.7-3-2.1-1.6-.4-3-1-3.1-2.5-.1-1.3 1-2.3 2.6-2.5 1.3-.1 2.5.4 3.2 1.3M30.6 23.6v1.7M30.8 35.2v1.6" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>',
        "photos": '<svg class="multicolumn-card__icon" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#eceaf7"/><rect x="9" y="17" width="19" height="22" rx="2" fill="#fff" stroke="#10144a" stroke-width="1.6"/><path d="M12 35l4.5-5 3 3 2.5-2.5 4 4.5" fill="none" stroke="#7b4a2a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="23" r="2.4" fill="#7b4a2a"/><rect x="28" y="17" width="19" height="22" rx="2" fill="#1a22c4"/><path d="M31 35l4.5-5 3 3 2.5-2.5 4 4.5" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M39.5 21.5l1 2.2 2.3.3-1.7 1.6.4 2.3-2-1.1-2 1.1.4-2.3-1.7-1.6 2.3-.3z" fill="#e8501f"/></svg>',
        "van": '<svg class="multicolumn-card__icon" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#eceaf7"/><path d="M8 20h24v16H8z" fill="#1a22c4"/><path d="M32 24h7l6 6v6H32z" fill="#10144a"/><path d="M34 26h4.4l3.6 3.8H34z" fill="#eceaf7"/><circle cx="15" cy="37" r="4" fill="#10144a" stroke="#eceaf7" stroke-width="2"/><circle cx="38" cy="37" r="4" fill="#10144a" stroke="#eceaf7" stroke-width="2"/><path d="M12 28h12" stroke="#e8501f" stroke-width="2.4" stroke-linecap="round"/><path d="M4 42h48" stroke="#10144a" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="2 4"/></svg>',
        "paw": '<svg class="multicolumn-card__icon" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#eceaf7"/><path d="M12 34c0-5 4-8 9-8h14c5 0 9 3 9 8v5H12z" fill="#1a22c4"/><rect x="10" y="31" width="5" height="11" rx="2.5" fill="#10144a"/><rect x="41" y="31" width="5" height="11" rx="2.5" fill="#10144a"/><g fill="#e8501f"><ellipse cx="28" cy="16.5" rx="3.6" ry="3"/><circle cx="22.6" cy="12" r="1.6"/><circle cx="26.2" cy="9.6" r="1.6"/><circle cx="29.8" cy="9.6" r="1.6"/><circle cx="33.4" cy="12" r="1.6"/></g></svg>',
    }
    items = [("price", "See the price first", "Every service has its price on the page. No waiting on a callback to find out."),
             ("photos", "Before and after photos", "We photograph the job when we arrive and again when we're done."),
             ("van", "We come to you", "Your home, your rental, your office, even your driveway for detailing."),
             ("paw", "Pets and stains welcome", "Pet urine treatment and fabric sealant are simple add-ons.")]
    lis = "".join(f'<li class="multicolumn-card scroll-trigger animate--slide-in" style="--animation-order:{i}">{art[k]}<h3>{t}</h3><p>{d}</p></li>'
                  for i, (k, t, d) in enumerate(items))
    return f'<section class="multicolumn multicolumn--trust" aria-label="Why book with us"><div class="page-width"><ul class="multicolumn-list">{lis}</ul></div></section>'


def collection_list(root, heading=True):
    lis = []
    for i, c in enumerate(COLLECTIONS):
        m = col_min(c["handle"])
        frm = f"From {money(m)}" if m else "Free estimates"
        lis.append(f'<li class="scroll-trigger animate--slide-in" style="--animation-order:{i}"><a class="collection-card" href="{root}collections/{c["handle"]}/">'
                   f'{media(root, c["img"], "", "(min-width: 990px) 230px, 46vw", "", c["contain"])}'
                   f'<span class="collection-card__title">{esc(c["title"])}{ICON["arrow"]}</span><span class="collection-card__from">{frm}</span></a></li>')
    head_html = ('<div class="title-wrapper scroll-trigger animate--slide-in"><div><h2>Shop by service</h2>'
                 '<p class="subtitle">Five kinds of cleaning, one company. Open one to see every option and price.</p></div>'
                 f'<a class="link animate-arrow" href="{root}collections/all/">View all</a></div>') if heading else ""
    head_html = head_html.replace("<h2>", '<h2 id="collections-title">', 1)
    return f'<section class="section-padding" aria-labelledby="collections-title"><div class="page-width">{head_html}<ul class="collection-list">{"".join(lis)}</ul></div></section>'


def review_slots(root, n=3, heading=True):
    slot = ('<li class="review-slot ph"><div class="review-slot__stars">' + ICON["star"] * 5 + '</div>'
            '<div class="review-slot__lines"><span></span><span></span><span></span></div>'
            '<p class="review-slot__name">A real customer review goes here</p></li>')
    head_html = ('<div class="title-wrapper scroll-trigger animate--slide-in"><div><h2 id="reviews-title">What customers say</h2>'
                 '<p class="subtitle">We only show reviews customers actually wrote. Send us your Google or Facebook reviews and they go here, word for word.</p></div>'
                 f'<a class="link" href="{root}pages/reviews/">All reviews</a></div>') if heading else ""
    return f'<section class="section-padding color-scheme-2" aria-labelledby="reviews-title"><div class="page-width">{head_html}<ul class="review-slots">{slot * n}</ul></div></section>'


FAQS = [
    ("Is the price on the page what I pay?",
     "For upholstery, carpet, tile, mattresses and detailing, yes: the price for the options you pick is the price. Stains like paint, oil, grease or ink that a normal clean won't lift are handled and billed separately. House, Airbnb, window, curtain and trash jobs show a starting price, and we confirm the total with you before the visit."),
    ("How is carpet priced?", "Per 150 sq ft, roughly a 12 by 12 room. Tile and grout is per 100 sq ft. Set the quantity to match your space."),
    ("Can you deal with pet accidents?", "Yes. Add pet urine treatment when you pick your options. It's there for carpet and every piece of upholstery."),
    ("What does the sealant do?", "It's a protectant we put on after cleaning. Add it as an option on carpet, upholstery, or tile and grout (clear or colored)."),
    ("Do you clean offices?", "Yes. Commercial cleaning starts with a free estimate on site."),
    ("Do you come to me for car detailing?", "Yes. Mobile detailing comes to you. Pick your vehicle size and package for the price."),
    ("Do you do post-construction cleans?", "Yes, as part of house cleaning. Extra paint or QuickSet removal is billed separately."),
]


def accordion(items, open_first=False):
    out = []
    for i, (q, a) in enumerate(items):
        o = " open" if open_first and i == 0 else ""
        out.append(f'<div class="accordion"><details{o}><summary><h3 class="accordion__title">{q}</h3>{ICON["caret"]}</summary><div class="accordion__content rte"><p>{a}</p></div></details></div>')
    return "".join(out)


def faq(root):
    return f"""<section class="section-padding" aria-labelledby="faq-title">
  <div class="page-width collapsible-content__grid">
    <div class="scroll-trigger animate--slide-in"><h2 id="faq-title">Questions people ask</h2><p class="subtitle" style="margin-top:1.4rem">Something else? Call <a class="link" href="tel:{TEL}">{PHONE}</a> or <a class="link" href="{root}pages/contact/">send a message</a>.</p></div>
    <div class="scroll-trigger animate--slide-in" style="--animation-order:1">{accordion(FAQS, True)}</div>
  </div>
</section>"""


def carpet_band(root):
    return f"""<section class="rich-text color-scheme-3 section-padding" aria-labelledby="band-title" data-carpet>
  <canvas class="carpet-canvas" aria-hidden="true"></canvas>
  <div class="rich-text__blocks page-width">
    <h2 class="h1" id="band-title">Find your service and see the price</h2>
    <p class="subtitle">Pick the piece, the fabric and any add-ons. The price updates as you go, and the cart keeps it all together.</p>
    <div class="buttons"><a class="button" href="{root}collections/all/">Shop all services</a><a class="button button--secondary" href="tel:{TEL}">{ICON["phone"]}Call {PHONE}</a></div>
    <p class="carpet-hint">Go on, run the vacuum over this carpet.</p>
  </div>
</section>"""


# ---------- product form pieces ----------

def pills(p, opt_index, opt, prefix):
    name = f"{prefix}-{opt_index}"
    lab = label(opt["name"])
    radios = "".join(
        f'<input type="radio" id="{name}-{j}" name="{name}" value="{esc(v)}"{" checked" if j == 0 else ""} data-option-index="{opt_index}">'
        f'<label for="{name}-{j}">{esc(vlabel(v))}</label>'
        for j, v in enumerate(opt["values"]))
    return (f'<fieldset class="js product-form__input product-form__input--pill"><legend class="form__label">{lab}: '
            f'<span class="form__label-value" data-option-value="{opt_index}">{esc(vlabel(opt["values"][0]))}</span></legend><div class="pills">{radios}</div></fieldset>')


def qty(p, prefix):
    lab = p.get("qty_label", "Quantity")
    return (f'<div class="product-form__quantity"><label class="form__label" for="{prefix}-qty">{lab}</label>'
            f'<div class="quantity"><button class="quantity__button" type="button" name="minus" aria-label="Decrease quantity for {esc(p["title"])}">{ICON["minus"]}</button>'
            f'<input class="quantity__input" type="number" id="{prefix}-qty" name="quantity" value="1" min="1" max="50" inputmode="numeric">'
            f'<button class="quantity__button" type="button" name="plus" aria-label="Increase quantity for {esc(p["title"])}">{ICON["plus"]}</button></div></div>')


def calc_fields(p, prefix):
    out = []
    for key, lab, kind in p.get("fields", []):
        fid = f"{prefix}-{key}"
        full = " field--full" if kind == "text" else ""
        if kind.startswith("select:"):
            opts = "".join(f'<option>{esc(o)}</option>' for o in kind[7:].split(","))
            ctrl = f'<select class="field__input" id="{fid}" name="properties[{esc(lab)}]">{opts}</select>'
        else:
            t = {"number": 'type="number" min="1" inputmode="numeric"', "time": 'type="time"', "text": 'type="text"'}[kind]
            ctrl = f'<input class="field__input" id="{fid}" name="properties[{esc(lab)}]" {t} placeholder="{esc(lab)}">'
        out.append(f'<div class="field{full}">{ctrl}<label class="field__label" for="{fid}">{esc(lab)}</label></div>')
    return f'<div class="product-form__fields">{"".join(out)}</div>' if out else ""


def product_form(root, p, prefix="product"):
    if p.get("estimate"):
        return (f'<div class="product-form__buttons"><a class="button button--full-width" href="{root}pages/contact/?topic=commercial">Book a free estimate</a>'
                f'<a class="button button--secondary button--full-width" href="tel:{TEL}">{ICON["phone"]}Call {PHONE}</a></div>')
    parts = [pills(p, i, o, prefix) for i, o in enumerate(p["options"])]
    if p.get("calc"):
        parts.append(f'<div><p class="form__label">Tell us about the job</p>{calc_fields(p, prefix)}</div>')
    show_qty = not p.get("calc") and not p.get("digital") and not p.get("pickup")
    if show_qty:
        parts.append(qty(p, prefix))
    buy = '<button type="button" class="shopify-payment-button__button" data-buy-now>Buy it now</button>' if not p.get("calc") else ""
    parts.append(f'<div class="product-form__buttons"><button type="submit" class="button button--full-width product-form__submit" data-add>'
                 f'<span>Add to cart</span></button>{buy}</div>')
    return f'<form class="product-form" data-product-form data-handle="{p["handle"]}" novalidate>{"".join(parts)}</form>'


# ---------- Home ----------

HERO_ITEMS = ["sofa-cleaning", "loveseat-cleaning", "sectional-cleaning", "armchair-cleaning", "ottoman-cleaning", "chair-barstool-cleaning"]
HERO_SHORT = {"sofa-cleaning": "Sofa", "loveseat-cleaning": "Loveseat", "sectional-cleaning": "Sectional", "armchair-cleaning": "Armchair",
              "ottoman-cleaning": "Ottoman", "chair-barstool-cleaning": "Chair or barstool"}


def hero(root):
    first = P[HERO_ITEMS[0]]
    items = "".join(
        f'<input type="radio" id="hero-item-{i}" name="hero-item" value="{h}"{" checked" if i == 0 else ""}><label for="hero-item-{i}">{HERO_SHORT[h]}</label>'
        for i, h in enumerate(HERO_ITEMS))
    opts = "".join(pills(first, i, o, "hero") for i, o in enumerate(first["options"]))
    m = META["sofa"]
    points = [("tag", "Prices listed online"), ("camera", "Before and after photos"), ("van", "Homes, Airbnbs and offices")]
    pts = "".join(f'<li>{ICON[k]}{t}</li>' for k, t in points)
    return f"""<section class="hero" aria-labelledby="hero-title">
  <div class="page-width hero__grid">
    <div class="hero__copy">
      <p class="hero__eyebrow caption-with-letter-spacing">Dallas-Fort Worth</p>
      <h1 class="h0" id="hero-title">Carpet, upholstery and home cleaning, priced before you book</h1>
      <p class="hero__text">Pick what needs cleaning, see the price, and add it to your cart. We come to you, take photos before and after, and walk you through the result.</p>
      <div class="buttons" data-hero-cta><a class="button" href="{root}collections/all/">Shop all services</a><a class="button button--secondary" href="tel:{TEL}">{ICON["phone"]}Call {PHONE}</a></div>
      <ul class="hero__points">{pts}</ul>
    </div>
    <div class="featured-product-card" data-hero-picker>
      <div class="featured-product-card__head">
        <div><p class="caption-with-letter-spacing muted">Price your clean</p><h2 class="h3" style="margin-top:.4rem" data-hero-title>{esc(first["title"])}</h2></div>
        <div class="featured-product-card__media media media--transparent media--contain"><img src="{root}assets/img/sofa-400.webp" width="400" height="{round(m['h'] * 400 / m['w'])}" alt="" data-hero-img fetchpriority="high"></div>
      </div>
      <form class="product-form" data-product-form data-handle="{first['handle']}" data-hero novalidate>
        <fieldset class="product-form__input product-form__input--pill"><legend class="form__label">What needs cleaning?</legend><div class="pills">{items}</div></fieldset>
        <div data-hero-options>{opts}</div>
        <div class="featured-product-card__price"><span class="caption muted">Your price</span><div class="price price--large" aria-live="polite"><span class="visually-hidden">Price</span><span class="price-item price-item--regular" data-price>{money(first['variants'][0]['price'])}</span></div></div>
        <div class="featured-product-card__buy">
          <div class="quantity"><button class="quantity__button" type="button" name="minus" aria-label="Decrease quantity">{ICON["minus"]}</button><input class="quantity__input" type="number" id="hero-qty" name="quantity" value="1" min="1" max="50" inputmode="numeric" aria-label="Quantity"><button class="quantity__button" type="button" name="plus" aria-label="Increase quantity">{ICON["plus"]}</button></div>
          <button type="submit" class="button product-form__submit" data-add><span>Add to cart</span></button>
        </div>
      </form>
      <a class="product__view-details link animate-arrow" href="{purl(root, first)}" data-hero-link>View full details {ICON["arrow"]}</a>
    </div>
  </div>
</section>"""


def home(root):
    feat = ["sofa-cleaning", "sectional-cleaning", "carpet-cleaning", "tile-grout-cleaning", "mattress-cleaning", "airbnb-cleaning", "mobile-detailing", "loveseat-cleaning"]
    cards = "".join(product_card(root, P[h], i) for i, h in enumerate(feat))
    airbnb_list = "".join(f"<li>{t}</li>" for t in ["Beds made, linen changed if you ask", "Bathrooms cleaned and disinfected",
                                                     "Counters, stove top, and the microwave inside and out", "Floors vacuumed and mopped, stairs too",
                                                     "Trash out, dishwasher loaded", "Before and after photos of every room"])
    steps = "".join(f"<li><strong>{t}</strong><span class=\"muted\">{d}</span></li>" for t, d in P["sofa-cleaning"]["steps"])
    return f"""
{hero(root)}
{trust(root)}
{collection_list(root)}
<section class="section-padding" style="padding-top:0" aria-labelledby="featured-title">
  <div class="page-width">
    <div class="title-wrapper scroll-trigger animate--slide-in"><div><h2 id="featured-title">Popular cleans</h2><p class="subtitle">Prices are the starting point. Open one to choose your options.</p></div><a class="link" href="{root}collections/all/">View all</a></div>
    <ul class="product-grid product-grid--4 list-unstyled">{cards}</ul>
  </div>
</section>
<section class="section-padding color-scheme-2" aria-labelledby="proof-title">
  <div class="page-width image-with-text__grid">
    <div class="image-with-text__media-item scroll-trigger animate--fade-in">
      <div class="collage">
        <figure class="collage__item"><span class="badge collage__label">Before</span>{media(root, "chair-before", "Dining chair with a stain on the fabric, before cleaning", "(min-width: 750px) 25vw, 46vw", "")}</figure>
        <figure class="collage__item"><span class="badge badge--orange collage__label">After</span>{media(root, "chair-after", "The same chair after cleaning, stain gone", "(min-width: 750px) 25vw, 46vw", "")}</figure>
        <figure class="collage__item collage__item--wide"><span class="badge collage__label">Before</span><span class="badge badge--orange collage__label collage__label--right">After</span>{media(root, "tile", "Tile and grout after a renovation, dirty on the left and cleaned on the right", "(min-width: 750px) 50vw, 100vw", "")}</figure>
      </div>
    </div>
    <div class="image-with-text__content scroll-trigger animate--slide-in">
      <p class="caption-with-letter-spacing muted">From our own jobs</p>
      <h2 id="proof-title">What a visit looks like</h2>
      <p class="subtitle">A stained dining chair, then the same chair after cleaning. Below it, tile and grout after a renovation. Every upholstery and carpet job follows the same five steps.</p>
      <ol class="steps-list">{steps}</ol>
      <div class="buttons"><a class="button" href="{root}collections/upholstery-cleaning/">Shop upholstery</a></div>
    </div>
  </div>
</section>
<section class="section-padding" aria-labelledby="hosts-title">
  <div class="page-width image-with-text__grid image-with-text__grid--reverse">
    <div class="image-with-text__media-item scroll-trigger animate--fade-in"><div class="image-with-text__media">{media(root, "airbnb", "Kitchen and breakfast bar in a short-term rental", "(min-width: 750px) 50vw, 100vw", "")}</div></div>
    <div class="image-with-text__content scroll-trigger animate--slide-in">
      <p class="caption-with-letter-spacing muted">For hosts and property managers</p>
      <h2 id="hosts-title">Turnovers between guests</h2>
      <p class="subtitle">Airbnb cleans start at {money(P["airbnb-cleaning"]["price_min"])}. Tell us the bedrooms and checkout time and we'll confirm the rest.</p>
      <ul class="check-list check-list--2">{airbnb_list}</ul>
      <div class="buttons"><a class="button" href="{purl(root, P["airbnb-cleaning"])}">Book an Airbnb clean</a><a class="button button--secondary" href="{purl(root, P["trash-removal-dumpster-to-dump"])}">Trash removal</a></div>
    </div>
  </div>
</section>
{review_slots(root)}
{faq(root)}
{carpet_band(root)}
"""


# ---------- Collections ----------

def collection_page(c, items, all_page=False):
    def body(root):
        cards = "".join(product_card(root, p, i, "h2") for i, p in enumerate(items))
        chips = [f'<a class="facet-chip" href="{root}collections/all/"{" aria-current=page" if all_page else ""}>All <span class="facet-chip__count">{len([p for p in P.values() if p["collection"] != "pro-shop"])}</span></a>']
        for cc in COLLECTIONS:
            cur = ' aria-current="page"' if cc["handle"] == c["handle"] else ""
            chips.append(f'<a class="facet-chip" href="{root}collections/{cc["handle"]}/"{cur}>{esc(cc["short"])} <span class="facet-chip__count">{len(by_collection(cc["handle"]))}</span></a>')
        has_img = not all_page
        img_html = f'<div class="scroll-trigger animate--fade-in">{media(root, c["img"], "", "(min-width: 990px) 400px, 100vw", "", c["contain"], eager=True)}</div>' if has_img else ""
        also = ""
        if c["handle"] != "pro-shop":
            also = (f'<div class="collection-also"><div class="title-wrapper"><div><h2 class="h3">Also from The Clean Don</h2>'
                    f'<p class="subtitle">Training and tools in the <a class="link" href="{root}collections/pro-shop/">Pro shop</a>, and open roles on our <a class="link" href="{root}pages/careers/">careers page</a>.</p></div></div></div>')
        return f"""<div class="collection-hero">
  <div class="page-width collection-hero__inner{' collection-hero__inner--image' if has_img else ''}">
    <div>{breadcrumbs(root, (c['title'], None))}<h1>{esc(c['title'])}</h1><p class="collection-hero__description">{esc(c['desc'])}</p></div>
    {img_html}
  </div>
</div>
<div class="page-width">
  <div class="facets-container">
    {'<nav class="facets__form" aria-label="Filter"><span class="facets__heading">Filter:</span><div class="facet-chips">' + "".join(chips) + '</div></nav>' if c['handle'] != 'pro-shop' else '<span></span>'}
    <div class="facets__sort"><label for="SortBy">Sort by:</label><div class="select"><select id="SortBy" class="select__select" data-sort><option value="featured">Featured</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option><option value="title-asc">Alphabetically, A-Z</option></select></div><span class="product-count" data-count>{len(items)} {'product' if len(items) == 1 else 'products'}</span></div>
  </div>
  <ul class="product-grid product-grid--4 list-unstyled" data-grid>{cards}</ul>
  {also}
</div>
<div style="height:var(--spacing-sections)"></div>"""
    return body


# ---------- Product ----------

def product_page(p):
    def body(root):
        imgs = []
        if p.get("img"):
            cap = f'<figcaption>{esc(p["caption"])}</figcaption>' if p.get("caption") else ""
            imgs.append(f'<li class="product__media-item" data-vt-target="p-{p["handle"]}">{media(root, p["img"], p["title"], "(min-width: 750px) 55vw, 100vw", "", p.get("contain"), eager=True)}{cap}</li>')
        else:
            imgs.append(f'<li class="product__media-item" data-vt-target="p-{p["handle"]}">{media(root, None, "", "")}<figcaption>We need a photo of this service from you.</figcaption></li>')
        extra_alt = {"chair-before": "A stained chair before cleaning", "chair-after": "The same chair after cleaning",
                     "engine": "Engine bay being wiped down", "window-2": "Tall living room windows", "window-3": "Kitchen window above the sink"}
        extra_cap = {"chair-before": "Before, from one of our jobs", "chair-after": "After"}
        for k in p.get("extra_imgs", []):
            cap = f'<figcaption>{extra_cap[k]}</figcaption>' if k in extra_cap else ""
            imgs.append(f'<li class="product__media-item">{media(root, k, extra_alt.get(k, ""), "(min-width: 750px) 27vw, 50vw", "")}{cap}</li>')
        tabs = []
        if p.get("steps"):
            tabs.append(("How your visit goes", '<ol class="steps-list">' + "".join(f"<li><strong>{t}</strong><span class=\"muted\">{d}</span></li>" for t, d in p["steps"]) + "</ol>"))
        if p.get("included"):
            tabs.append(("What's included", '<ul class="check-list">' + "".join(f"<li>{t}</li>" for t in p["included"]) + "</ul>"))
        if p.get("packages"):
            pk = "".join(f'<h4 class="h4" style="margin-top:1.6rem">{n}</h4><ul class="check-list" style="margin-top:.8rem">' + "".join(f"<li>{t}</li>" for t in items) + "</ul>" for n, items in p["packages"])
            tabs.append(("What each package includes", pk + '<p class="muted" style="margin-top:1.6rem">Engine clean is also available on its own.</p>'))
        if p.get("notes"):
            tabs.append(("Good to know", "<ul>" + "".join(f"<li>{n}</li>" for n in p["notes"]) + "</ul>"))
        if p.get("stock"):
            tabs.append(("About the photo", '<p class="ph" style="padding:.4rem .6rem">This photo is from the current store and may be a stock image. We\'d swap in one of your own jobs.</p>'))
        tab_html = "".join(f'<div class="accordion product__accordion"><details{" open" if i == 0 else ""}><summary><h2 class="accordion__title">{t}</h2>{ICON["caret"]}</summary><div class="accordion__content rte">{c}</div></details></div>' for i, (t, c) in enumerate(tabs))
        pickup = (f'<div class="product__pickup">{ICON["check"]}<div><strong>Local pickup only</strong><br><span class="muted">Pickup in the Dallas area. We\'ll arrange a time after checkout.</span></div></div>') if p.get("pickup") else ""
        tax = "Taxes calculated at checkout." if not p.get("estimate") else ""
        assurance = ""
        if p["collection"] not in ("pro-shop",):
            assurance = (f'<ul class="product__assurance">'
                         f'<li>{ICON["camera"]}<span>Photos before and after the job</span></li>'
                         f'<li>{ICON["van"]}<span>We come to you, anywhere in Dallas-Fort Worth</span></li>'
                         f'<li>{ICON["phone"]}<span>Questions first? Call <a class="link" href="tel:{TEL}">{PHONE}</a></span></li></ul>')
        related = [q for q in by_collection(p["collection"]) if q["handle"] != p["handle"]][:4]
        if len(related) < 4:
            related += [q for q in P.values() if q["collection"] not in (p["collection"], "pro-shop") and q not in related][:4 - len(related)]
        rel = "".join(product_card(root, q, i) for i, q in enumerate(related))
        coll = next((c for c in COLLECTIONS if c["handle"] == p["collection"]), PRO_SHOP)
        data = json.dumps({"handle": p["handle"]})
        return f"""<section class="page-width" style="padding-top:2.4rem">
  {breadcrumbs(root, (coll['title'], 'collections/' + coll['handle'] + '/'), (p['title'], None))}
  <div class="product" data-product='{data}'>
    <div class="product__media-wrapper"><ul class="product__media-list list-unstyled">{"".join(imgs)}</ul></div>
    <div class="product__info-wrapper">
      <div class="product__info-container">
        <p class="product__text caption-with-letter-spacing">The Clean Don</p>
        <div class="product__title"><h1>{esc(p['title'])}</h1></div>
        <div>{price_html(p, True)}<p class="product__tax">{tax}</p></div>
        <div class="product__description rte"><p>{esc(p['summary'])}</p></div>
        {pickup}
        {product_form(root, p)}
        {assurance}
        <div>{tab_html}</div>
      </div>
    </div>
  </div>
</section>
<section class="section-padding" aria-labelledby="related-title">
  <div class="page-width">
    <div class="title-wrapper"><h2 class="h3" id="related-title">You may also like</h2></div>
    <ul class="product-grid product-grid--4 list-unstyled">{rel}</ul>
  </div>
</section>"""
    return body


# ---------- Cart ----------

def cart(root):
    return f"""<section class="page-width section-padding" style="padding-top:4rem">
  <div class="cart-page">
    <div>
      <div class="cart-page__head"><h1>Your cart</h1><a class="link" href="{root}collections/all/">Continue shopping</a></div>
      <div class="cart-page__items" data-cart-items data-cart-page></div>
      <div class="drawer__inner-empty" data-cart-empty hidden style="padding:6rem 0">
        <p class="cart__empty-text">Your cart is empty</p><p class="muted">As clean as it gets. Let's find something that isn't.</p>
        <div><a class="button" href="{root}collections/all/">Continue shopping</a></div>
      </div>
    </div>
    <aside class="cart-footer" data-cart-footer hidden aria-label="Order summary">
      <h2>Your visit</h2>
      <div class="cart-attributes">
        <div class="field"><input class="field__input" id="Cart-zip" name="attributes[Service ZIP]" type="text" inputmode="numeric" maxlength="5" placeholder="Service ZIP code" autocomplete="postal-code"><label class="field__label" for="Cart-zip">Service ZIP code</label></div>
        <div class="field"><input class="field__input" id="Cart-date" name="attributes[Preferred date]" type="date" placeholder="Preferred date"><label class="field__label" for="Cart-date">Preferred date</label></div>
        <div class="field"><select class="field__input" id="Cart-time" name="attributes[Time window]"><option>Morning</option><option>Afternoon</option><option>Any time</option></select><label class="field__label" for="Cart-time">Time window</label></div>
        <div class="field"><textarea class="text-area field__input" id="Cart-note" name="note" placeholder="Order special instructions"></textarea><label class="field__label" for="Cart-note">Order special instructions</label></div>
      </div>
      <div class="totals"><h3 class="totals__total">Estimated total</h3><p class="totals__total-value" data-cart-total>$0.00</p></div>
      <p class="tax-note" data-cart-note>Taxes, discounts and travel calculated at checkout.</p>
      <button type="button" class="button button--full-width" data-checkout>Check out</button>
      <p class="caption muted">Gate codes, pets at home, parking: put it in the instructions and the tech will see it.</p>
    </aside>
  </div>
</section>"""


# ---------- Pages ----------

def page_banner(root, title, lede, crumb=None):
    return (f'<div class="collection-hero"><div class="page-width">{breadcrumbs(root, (crumb or title, None))}'
            f'<h1>{title}</h1><p class="collection-hero__description">{lede}</p></div></div>')


def about(root):
    values = [("Photos before and after", "Techs take at least six before photos of each room and add-on, and six after. You see exactly what changed."),
              ("We tell you what we spot", "If we notice damage or pests while we're cleaning, we tell you. You'd want to know."),
              ("Your details stay private", "Your address, your name and what's in your home stay between us."),
              ("The corners count", "Vacuuming, sweeping and mopping, with the corners getting the same attention as the middle of the room.")]
    vl = "".join(f'<li class="scroll-trigger animate--slide-in" style="--animation-order:{i}"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(values))
    return f"""{page_banner(root, "About The Clean Don", "We clean homes, rentals, offices and cars across Dallas-Fort Worth. The aim is simple: put the customer first and treat every one like family.", "About us")}
<section class="section-padding">
  <div class="page-width image-with-text__grid">
    <div class="image-with-text__media-item"><div class="media media--portrait media--transparent ph" title="Owner photo needed">{PLACEHOLDER}</div></div>
    <div class="image-with-text__content">
      <p class="caption-with-letter-spacing muted">The family business</p>
      <h2>Cleaning that feels like family</h2>
      <p class="subtitle">That's how we put it on our first website, and it still holds. You get a price before you book, a crew that shows up and does the corners, and photos so you can see the difference.</p>
      <p class="ph" style="padding:.6rem .8rem">Owner's name, how The Clean Don started and the year it opened go here. We'll write it with you.</p>
      <div class="buttons"><a class="button" href="{root}collections/all/">Shop all services</a><a class="button button--secondary" href="{root}pages/contact/">Contact us</a></div>
    </div>
  </div>
</section>
<section class="section-padding color-scheme-2">
  <div class="page-width"><div class="title-wrapper"><div><h2>How we work</h2><p class="subtitle">Straight from the job descriptions every tech works to.</p></div></div><ul class="value-list">{vl}</ul></div>
</section>
{trust(root)}
{carpet_band(root)}"""


def reviews(root):
    return f"""{page_banner(root, "Reviews", "Real reviews from real customers, word for word. We're collecting them now.")}
{review_slots(root, 6, False)}
<section class="section-padding">
  <div class="page-width page-width--narrow" style="text-align:center">
    <h2>Had us out recently?</h2>
    <p class="subtitle" style="margin:1.4rem auto 0;max-width:52ch">A short review helps other people in Dallas-Fort Worth find us. It takes a minute.</p>
    <div class="buttons" style="justify-content:center;margin-top:2.8rem"><a class="button" href="{FACEBOOK}reviews" target="_blank" rel="noopener">Review us on Facebook</a><span class="button button--secondary ph" aria-disabled="true">Google review link goes here</span></div>
  </div>
</section>"""


def contact(root):
    return f"""{page_banner(root, "Contact", "Call, email or send the form. If it's about a specific clean, the service pages have prices and options too.")}
<section class="section-padding">
  <div class="page-width page-columns">
    <div>
      <ul class="contact-details">
        <li><span>Phone</span><a href="tel:{TEL}">{PHONE}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Area</span><p style="font-size:2rem;font-weight:600">Dallas-Fort Worth, Texas</p><p class="muted">Including Dallas, Fort Worth, Plano, Rowlett, DeSoto and Forney.</p></li>
        <li class="ph" style="padding:.6rem .8rem"><span>Hours</span><p class="muted">Your opening hours go here.</p></li>
      </ul>
    </div>
    <div class="contact">
      <h2 class="h3" style="margin-bottom:2rem">Send us a message</h2>
      <form data-contact-form novalidate>
        <div class="form-status form-status--error" role="alert" data-form-error hidden>Please adjust the following: the fields marked below.</div>
        <div class="contact__fields">
          <div class="field"><input class="field__input" id="ContactForm-name" name="name" type="text" autocomplete="name" placeholder="Name" required><label class="field__label" for="ContactForm-name">Name</label></div>
          <div class="field"><input class="field__input" id="ContactForm-phone" name="phone" type="tel" autocomplete="tel" placeholder="Phone number"><label class="field__label" for="ContactForm-phone">Phone number</label></div>
          <div class="field field--full"><input class="field__input" id="ContactForm-email" name="email" type="email" autocomplete="email" placeholder="Email" required><label class="field__label" for="ContactForm-email">Email <span aria-hidden="true">*</span></label></div>
          <div class="field field--full"><select class="field__input" id="ContactForm-topic" name="topic"><option value="general">A question</option><option value="commercial">Free commercial estimate</option><option value="house">House or Airbnb cleaning</option><option value="careers">Working with us</option><option value="other">Something else</option></select><label class="field__label" for="ContactForm-topic">What's it about?</label></div>
          <div class="field field--full"><textarea class="text-area field__input" id="ContactForm-body" name="body" placeholder="Comment" required></textarea><label class="field__label" for="ContactForm-body">Comment</label></div>
        </div>
        <div class="contact__button"><button type="submit" class="button">Send</button></div>
      </form>
      <div class="form-status form-status--success" role="status" data-form-success hidden><h3 class="h3">Thanks for contacting us<span data-first-name></span>.</h3><p style="margin-top:.6rem">We'll get back to you as soon as possible. In a hurry? Call <a class="link" href="tel:{TEL}">{PHONE}</a>.</p></div>
    </div>
  </div>
</section>"""


def careers(root):
    jobs = []
    for handle, title, where, tasks in JOBS:
        t = "".join(f"<li>{x}</li>" for x in tasks)
        subj = title.replace(" ", "%20").replace(",", "")
        jobs.append((f'{title}<span class="job-meta"><span class="badge">{where}</span></span>',
                     f'<ul class="check-list">{t}</ul><div class="buttons" style="margin-top:2rem"><a class="button" href="mailto:{EMAIL}?subject=Application:%20{subj}">Apply by email</a></div>'))
    acc = "".join(f'<div class="accordion"><details{" open" if i == 0 else ""}><summary><h2 class="accordion__title">{q}</h2>{ICON["caret"]}</summary><div class="accordion__content">{a}</div></details></div>' for i, (q, a) in enumerate(jobs))
    return f"""{page_banner(root, "Careers", "We're hiring across cleaning, renovation and pool service. Every role comes down to the same three things: professionalism, attention to detail and integrity.")}
<section class="section-padding">
  <div class="page-width collapsible-content__grid">
    <div><h2>Open roles</h2><p class="subtitle" style="margin-top:1.4rem">Send your details to <a class="link" href="mailto:{EMAIL}">{EMAIL}</a> with the role in the subject line.</p></div>
    <div>{acc}</div>
  </div>
</section>"""


def notfound(root):
    return f"""<section class="main-404 page-width">
  <div class="rug" tabindex="0" aria-label="A rug. Hover to lift the corner." data-rug>
    <svg viewBox="0 0 340 170" aria-hidden="true" focusable="false">
      <text x="170" y="118" text-anchor="middle" font-family="Archivo, sans-serif" font-size="78" font-weight="800" fill="#10144a" opacity=".85">404</text>
      <g class="rug__body"><rect x="20" y="70" width="300" height="80" rx="4" fill="#1a22c4"/><rect x="34" y="82" width="272" height="56" rx="2" fill="none" stroke="#e8501f" stroke-width="3"/><path d="M60 110h220" stroke="#fff" stroke-width="2" stroke-dasharray="6 8" opacity=".6"/></g>
      <g class="rug__corner"><path d="M20 70h110v80H20z" fill="#1a22c4"/><path d="M34 82h96M34 82v56h96" fill="none" stroke="#e8501f" stroke-width="3"/></g>
      <g stroke="#10144a" stroke-width="2" stroke-linecap="round" opacity=".5"><path d="M24 150v10M40 150v10M56 150v10M72 150v10M88 150v10M104 150v10M120 150v10M136 150v10M152 150v10M168 150v10M184 150v10M200 150v10M216 150v10M232 150v10M248 150v10M264 150v10M280 150v10M296 150v10M312 150v10"/></g>
    </svg>
  </div>
  <p class="caption-with-letter-spacing muted">404</p>
  <h1>Page not found</h1>
  <p class="subtitle" style="margin:1.4rem auto 0;max-width:44ch">Looks like this one got swept under the rug. Try the services, or give us a call.</p>
  <div class="buttons"><a class="button" href="{root}collections/all/">Continue shopping</a><a class="button button--secondary" href="tel:{TEL}">{ICON["phone"]}Call {PHONE}</a></div>
</section>"""


def write_catalog_js():
    data = {}
    for h, p in P.items():
        data[h] = {"t": p["title"], "img": p.get("img"), "c": bool(p.get("contain")), "o": [{"n": label(o["name"]), "v": o["values"],
                   "l": [vlabel(v) for v in o["values"]]} for o in p["options"]], "v": [[v["options"], v["price"]] for v in p["variants"]],
                   "min": p["price_min"], "iw": META[p["img"]]["widths"][0] if p.get("img") else 0, "calc": bool(p.get("calc")), "pet": any("Urine" in o["name"] for o in p["options"])}
    with open(os.path.join(OUT, "assets/js/catalog.js"), "w") as f:
        f.write("/* Generated by tools/build_site.py from data/products.json (the store's published prices). */\nwindow.CATALOG=" + json.dumps(data, separators=(",", ":")) + ";\n")


def main():
    write_catalog_js()
    with open(os.path.join(OUT, "version.json"), "w") as f:
        json.dump({"build": BUILD}, f)
    page("", "The Clean Don", "Carpet, upholstery, home and car cleaning across Dallas-Fort Worth. Pick your service, see the price, and book online.", "", home)
    services = [p for p in P.values() if p["collection"] != "pro-shop"]
    order = {c["handle"]: i for i, c in enumerate(COLLECTIONS)}
    services.sort(key=lambda p: order[p["collection"]])
    page("collections/all/", "All services", "Every cleaning service The Clean Don offers, with prices.", "collections/all/",
         collection_page({"handle": "all", "title": "All services", "desc": "Everything we clean, with the starting price for each. Filter by type, or sort by price.", "img": None, "contain": False}, services, True))
    for c in COLLECTIONS:
        page(f"collections/{c['handle']}/", c["title"], c["desc"], "collections/all/", collection_page(c, by_collection(c["handle"])))
    page("collections/pro-shop/", "Pro shop", PRO_SHOP["desc"], "collections/pro-shop/", collection_page(PRO_SHOP, by_collection("pro-shop")))
    for p in P.values():
        active = "collections/pro-shop/" if p["collection"] == "pro-shop" else "collections/all/"
        page(f"products/{p['handle']}/", p["title"], p["summary"][:155], active, product_page(p))
    page("cart/", "Your cart", "Your cart at The Clean Don.", "none", cart, actions=False)
    page("pages/about/", "About us", "The Clean Don cleans homes, rentals, offices and cars across Dallas-Fort Worth.", "pages/about/", about)
    page("pages/reviews/", "Reviews", "Reviews from customers of The Clean Don.", "none", reviews)
    page("pages/contact/", "Contact", "Call, email or message The Clean Don.", "pages/contact/", contact)
    page("pages/careers/", "Careers", "Jobs at The Clean Don: cleaning technicians, contractors and pool technicians.", "none", careers)
    page("404.html", "Page not found", "This page could not be found.", "none", notfound, depth=0, root="/")


if __name__ == "__main__":
    main()
