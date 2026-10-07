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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300..700&amp;display=swap">
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


def review_slots(root, n=3, heading=True):
    slot = ('<li class="review-slot ph"><div class="review-slot__stars">' + ICON["star"] * 5 + '</div>'
            '<div class="review-slot__lines"><span></span><span></span><span></span></div>'
            '<p class="review-slot__name">A real customer review goes here</p></li>')
    head_html = ('<div class="title-wrapper scroll-trigger animate--slide-in"><div><h2 id="reviews-title">What customers say</h2>'
                 '<p class="subtitle">We only show reviews customers actually wrote. Send us your Google or Facebook reviews and they go here, word for word.</p></div>'
                 f'<a class="link" href="{root}pages/reviews/">All reviews</a></div>') if heading else ""
    return f'<section class="section-padding color-scheme-2" aria-labelledby="reviews-title"><div class="page-width">{head_html}<ul class="review-slots">{slot * n}</ul></div></section>'


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


# ---------- Home (Twenty Twenty-Five "page-business-home" / "page-shop-home" composition) ----------

def vprice(handle, opts):
    for v in P[handle]["variants"]:
        if v["options"] == opts:
            return v["price"]
    return P[handle]["price_min"]


def wp_button(href, text, outline=False, attrs=""):
    cls = "wp-block-button is-style-outline" if outline else "wp-block-button"
    return f'<div class="{cls}"><a class="wp-block-button__link wp-element-button" href="{href}"{attrs}>{text}</a></div>'


def wp_banner_intro(root):
    """banner-intro-image (56% image column + centered text column); the image slot holds overlapped-images."""
    return f"""<div class="wp-block-group alignfull wp-section wp-section--banner">
  <div class="wp-block-columns alignwide wp-banner">
    <div class="wp-block-column wp-banner__media" style="flex-basis:56%">
      <div class="wp-overlapped">
        <figure class="wp-block-image size-full wp-overlapped__main">{img(root, "chair-after", "Dining chair after cleaning, the stain is gone", "(min-width: 782px) 40vw, 80vw", eager=True)}<figcaption class="wp-element-caption">After</figcaption></figure>
        <figure class="wp-block-image size-full wp-overlapped__small">{img(root, "chair-before", "The same chair before cleaning, with a stain on the fabric", "(min-width: 782px) 18vw, 40vw")}<figcaption class="wp-element-caption">Before</figcaption></figure>
      </div>
    </div>
    <div class="wp-block-column is-vertically-aligned-center wp-banner__text">
      <p class="is-style-text-annotation">Dallas-Fort Worth</p>
      <h1 class="wp-block-heading has-xx-large-font-size">Carpet, upholstery and home cleaning, with the price up front</h1>
      <p class="has-large-font-size">Choose what needs cleaning and you'll see the price before you book. We come to you and photograph the job before and after.</p>
      <div class="wp-block-buttons" data-hero-cta>{wp_button(root + "collections/all/", "See all prices")}{wp_button("tel:" + TEL, "Call " + PHONE, True)}</div>
    </div>
  </div>
</div>"""


def wp_pricing(root):
    """pricing-3-col: bordered columns, title and description left, price right, full-width button."""
    sofa, loveseat, sect = P["sofa-cleaning"], P["loveseat-cleaning"], P["sectional-cleaning"]
    cols = [
        ("Upholstery", "Sofas, sectionals, chairs and mattresses. Pick the fabric, add pet urine treatment or sealant.",
         P["chair-barstool-cleaning"]["price_min"],
         [("Sofa", sofa["price_min"]), ("Loveseat", loveseat["price_min"]), ("Sectional", sect["price_min"]), ("Queen mattress", vprice("mattress-cleaning", ["Queen"]))],
         "collections/upholstery-cleaning/"),
        ("Carpet and tile", "Carpet is priced per 150 sq ft, tile and grout per 100 sq ft. Wool and natural stone welcome.",
         P["carpet-cleaning"]["price_min"],
         [("Carpet, per 150 sq ft", P["carpet-cleaning"]["price_min"]), ("Wool carpet, per 150 sq ft", vprice("carpet-cleaning", ["Wool", "no", "no"])),
          ("Tile and grout, per 100 sq ft", P["tile-grout-cleaning"]["price_min"]), ("Natural stone, per 100 sq ft", vprice("tile-grout-cleaning", ["Natural Stone", "no"]))],
         "collections/carpet-and-floors/"),
        ("Mobile detailing", "We come to you. Prices below are for a small or medium car; bigger vehicles cost a little more.",
         P["mobile-detailing"]["price_min"],
         [("Deluxe wash", vprice("mobile-detailing", ["Small/ Medium Car", "Deluxe Wash"])), ("Wash and wax", vprice("mobile-detailing", ["Small/ Medium Car", "Deluxe Wash & Wax"])),
          ("Interior restoration", vprice("mobile-detailing", ["Small/ Medium Car", "Interior Restoration"])), ("Full detail", vprice("mobile-detailing", ["Small/ Medium Car", "Full Detail"]))],
         "products/mobile-detailing/"),
    ]
    out = []
    for i, (t, d, frm, rows, href) in enumerate(cols):
        lis = "".join(f'<li><span>{esc(n)}</span><span>{money(pr)}</span></li>' for n, pr in rows)
        out.append(f"""<div class="wp-block-column has-border-color has-accent-6-border-color wp-price-col scroll-trigger animate--slide-in" style="--animation-order:{i}">
      <div class="wp-block-columns is-not-stacked-on-mobile wp-price-col__head">
        <div class="wp-block-column" style="flex-basis:64%"><h3 class="wp-block-heading has-large-font-size">{t}</h3><p class="has-small-font-size">{d}</p></div>
        <div class="wp-block-column"><p class="has-small-font-size has-text-align-right wp-price-col__from">from</p><h3 class="wp-block-heading has-text-align-right">{money(frm).replace(".00", "")}</h3></div>
      </div>
      <ul class="wp-block-list wp-price-list">{lis}</ul>
      <div class="wp-block-buttons">{wp_button(root + href, "See options").replace('class="wp-block-button"', 'class="wp-block-button has-custom-width wp-block-button__width-100"')}</div>
    </div>""")
    return f"""<div class="wp-block-group alignfull wp-section" id="pricing">
  <div class="wp-block-group alignwide wp-flex-between">
    <h2 class="wp-block-heading has-x-large-font-size">Prices, before you book</h2>
    <p class="is-style-text-annotation">Pricing</p>
  </div>
  <div class="wp-block-columns alignwide wp-price-cols">{"".join(out)}</div>
  <p class="alignwide has-small-font-size wp-muted wp-note">Stains like paint, oil, grease or ink that a normal clean won't lift are handled and billed separately. House, Airbnb, window and trash jobs start from a set price and we confirm the total with you.</p>
</div>"""


def wp_services(root):
    """services-3-col: 4:3 image, h3, medium paragraph. Two rows."""
    items = [("collections/upholstery-cleaning/", "sofa", "Upholstery and mattresses", "Sofas, sectionals, chairs, ottomans, mattresses and curtains, cleaned where they are."),
             ("collections/carpet-and-floors/", "tile", "Carpet, tile and grout", "Deep carpet cleaning, and tile and grout brought back after renovations."),
             ("products/residential-cleaning/", "residential", "House cleaning", "Regular, deep, move-out and post-construction cleans for homes and apartments."),
             ("products/airbnb-cleaning/", "airbnb", "Airbnb turnovers", "Beds made, bathrooms disinfected, kitchen reset and photos of every room."),
             ("products/mobile-detailing/", "detailing", "Mobile detailing", "From a deluxe wash to a full detail, done in your driveway."),
             ("collections/commercial-and-property/", "trash", "Commercial and trash removal", "Free on-site estimates for offices, plus haul-offs to the curb or the dump.")]
    cols = []
    for i, (h, k, t, d) in enumerate(items):
        cols.append(f"""<div class="wp-block-column wp-service scroll-trigger animate--slide-in" style="--animation-order:{i % 3}">
      <a href="{root}{h}"><figure class="wp-block-image size-full">{img(root, k, "", "(min-width: 782px) 30vw, 90vw", extra=' style="aspect-ratio:4/3;object-fit:cover"')}</figure>
      <h3 class="wp-block-heading">{t}</h3></a>
      <p class="has-medium-font-size">{d}</p>
    </div>""")
    return f"""<div class="wp-block-group alignfull wp-section is-style-section-1">
  <div class="wp-block-group alignwide wp-flex-between"><h2 class="wp-block-heading">What we clean</h2><a class="wp-more" href="{root}collections/all/">All services</a></div>
  <div class="wp-block-columns alignwide wp-services">{"".join(cols)}</div>
</div>"""


def wp_process(root):
    """heading-and-paragraph-with-image: text column, image column."""
    steps = "".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in P["sofa-cleaning"]["steps"])
    return f"""<div class="wp-block-group alignfull wp-section">
  <div class="wp-block-columns alignwide are-vertically-aligned-center wp-gap-80">
    <div class="wp-block-column">
      <p class="is-style-text-annotation">How a visit goes</p>
      <h2 class="wp-block-heading">Photos at the start, a walk-through at the end</h2>
      <p>Every upholstery, carpet and tile job follows the same five steps, so you always know where we are.</p>
      <ol class="wp-block-list wp-steps">{steps}</ol>
    </div>
    <div class="wp-block-column">
      <figure class="wp-block-image size-full">{img(root, "tile", "Tile and grout after a renovation, dirty on the left and clean on the right", "(min-width: 782px) 50vw, 100vw")}<figcaption class="wp-element-caption">Tile and grout after a renovation: before on the left, after on the right.</figcaption></figure>
    </div>
  </div>
</div>"""


def wp_testimonial(root):
    """testimonials-large: annotation heading, large plain quote, citation. Placeholder until real reviews arrive."""
    return f"""<div class="wp-block-group alignfull wp-section is-style-section-1">
  <div class="wp-block-group alignwide wp-testimonial">
    <h2 class="wp-block-heading is-style-text-annotation">What customers say</h2>
    <blockquote class="wp-block-quote is-style-plain has-x-large-font-size ph"><p>A real review from one of your customers goes here, word for word, with their name and the service they booked.</p><cite>Google or Facebook review</cite></blockquote>
    <p class="has-small-font-size wp-muted">We only show reviews customers actually wrote. <a href="{root}pages/reviews/">Leave a review</a></p>
  </div>
</div>"""


FAQS = [
    ("Is the price on the page what I pay?", "For upholstery, carpet, tile, mattresses and detailing, yes. Stains like paint, oil, grease or ink that a normal clean won't lift are billed separately."),
    ("Can you deal with pet accidents?", "Yes. Add pet urine treatment when you pick your options. It's there for carpet and every piece of upholstery."),
    ("Do you clean offices?", "Yes. Commercial cleaning starts with a free estimate on site, so the price fits your space."),
    ("Do you do post-construction cleans?", "Yes, as part of house cleaning. Extra paint or QuickSet removal is billed separately."),
]


def wp_faqs(root):
    """text-faqs: two columns of question groups with a top border."""
    def grp(q, a):
        return f'<div class="wp-block-group wp-faq"><h3 class="wp-block-heading">{q}</h3><p>{a}</p></div>'
    rows = "".join(f'<div class="wp-block-columns">{"".join(grp(q, a) for q, a in FAQS[i:i + 2])}</div>' for i in range(0, len(FAQS), 2))
    return f"""<div class="wp-block-group alignfull wp-section">
  <div class="wp-block-group alignwide"><h2 class="wp-block-heading has-x-large-font-size">Frequently asked questions</h2>{rows}</div>
</div>"""


def cta_centered(root, title="See every price before you book", text="Pick the piece, the fabric and any add-ons. The cart keeps it together, and you check out when you're ready."):
    """cta-centered-heading."""
    return f"""<div class="wp-block-group alignfull wp-section wp-cta" data-carpet>
  <canvas class="carpet-canvas" aria-hidden="true"></canvas>
  <div class="wp-block-group wp-cta__inner">
    <h2 class="wp-block-heading has-text-align-center has-xx-large-font-size">{title}</h2>
    <p class="has-text-align-center">{text}</p>
    <div class="wp-block-buttons is-content-justification-center">{wp_button(root + "collections/all/", "Shop all services")}{wp_button("tel:" + TEL, "Call " + PHONE, True)}</div>
  </div>
</div>"""


def home(root):
    return f"""<div class="wp-site-blocks">
{wp_banner_intro(root)}
{wp_pricing(root)}
{wp_services(root)}
{wp_process(root)}
{wp_testimonial(root)}
{wp_faqs(root)}
{cta_centered(root)}
</div>"""


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
{cta_centered(root)}"""


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
