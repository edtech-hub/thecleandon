/* The Clean Don theme script. No dependencies.
   Behaviour follows Dawn: variant pills update price and ?variant=, Add to cart opens the cart drawer,
   cart page with cart attributes and note. The cart lives in localStorage (prototype only; on Shopify
   this becomes /cart/add.js and /cart.js). */
(function () {
  "use strict";
  var C = window.CATALOG || {};
  var ROOT = window.ROOT || "";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var KEY = "tcd-cart-v1";

  function money(c) { return "$" + (c / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------- cart store ---------- */
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; } }
  function save(items) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* private mode: cart lasts for this page only */ } memory = items; }
  var memory = load();
  function items() { return memory; }

  function variantPrice(handle, opts) {
    var p = C[handle];
    if (!p) return 0;
    if (!p.v.length) return p.min;
    for (var i = 0; i < p.v.length; i++) {
      if (p.v[i][0].join("|") === opts.join("|")) return p.v[i][1];
    }
    return p.min;
  }
  function optLabel(handle, opts) {
    var p = C[handle];
    return opts.map(function (v, i) { var o = p.o[i]; return o.n + ": " + o.l[o.v.indexOf(v)]; });
  }
  function imgSrc(p) { return p.img ? ROOT + "assets/img/" + p.img + "-" + p.iw + ".webp" : ""; }

  function addItem(handle, opts, props, qty) {
    var list = items().slice();
    var key = handle + "::" + opts.join("|") + "::" + JSON.stringify(props);
    var found = list.filter(function (x) { return x.key === key; })[0];
    if (found) found.q = Math.min(50, found.q + qty);
    else list.push({ key: key, h: handle, o: opts, props: props, q: qty });
    save(list);
    renderCart();
  }
  function setQty(key, q) {
    var list = items().slice().map(function (x) { if (x.key === key) x.q = q; return x; }).filter(function (x) { return x.q > 0; });
    save(list);
    renderCart();
  }

  /* ---------- cart rendering (drawer + /cart page) ---------- */
  function lineHTML(x) {
    var p = C[x.h];
    if (!p) return "";
    var price = variantPrice(x.h, x.o);
    var meta = optLabel(x.h, x.o);
    Object.keys(x.props || {}).forEach(function (k) { if (x.props[k]) meta.push(k + ": " + x.props[k]); });
    var media = p.img ? '<img src="' + imgSrc(p) + '" alt="" loading="lazy" width="200" height="200">' : "";
    var from = p.calc ? '<span class="price__from">From </span>' : "";
    return '<div class="cart-item" data-key="' + esc(x.key) + '">' +
      '<a class="cart-item__media" href="' + ROOT + 'products/' + x.h + '/" tabindex="-1" aria-hidden="true"><div class="media media--square' + (p.c ? " media--transparent media--contain" : "") + '">' + media + '</div></a>' +
      '<div class="cart-item__details"><a class="cart-item__name" href="' + ROOT + 'products/' + x.h + '/">' + esc(p.t) + '</a>' +
      '<div class="product-option">' + from + money(price) + (p.calc ? " (we confirm the total)" : "") + '</div>' +
      meta.map(function (m) { return '<div class="product-option">' + esc(m) + '</div>'; }).join("") + '</div>' +
      '<div class="cart-item__totals">' + money(price * x.q) + '</div>' +
      '<div class="cart-item__quantity"><div class="quantity quantity--small">' +
      '<button class="quantity__button" type="button" data-q="-1" aria-label="Decrease quantity for ' + esc(p.t) + '"' + (p.calc ? " disabled" : "") + '><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14"/></svg></button>' +
      '<input class="quantity__input" type="number" value="' + x.q + '" min="0" max="50" aria-label="Quantity for ' + esc(p.t) + '"' + (p.calc ? " readonly" : "") + '>' +
      '<button class="quantity__button" type="button" data-q="1" aria-label="Increase quantity for ' + esc(p.t) + '"' + (p.calc ? " disabled" : "") + '><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></button></div>' +
      '<button type="button" class="cart-remove-button" data-remove aria-label="Remove ' + esc(p.t) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/></svg></button></div></div>';
  }
  function renderCart() {
    var list = items();
    var count = list.reduce(function (n, x) { return n + x.q; }, 0);
    var total = list.reduce(function (n, x) { return n + variantPrice(x.h, x.o) * x.q; }, 0);
    var anyFrom = list.some(function (x) { return C[x.h] && C[x.h].calc; });
    $$("[data-cart-count]").forEach(function (b) { b.textContent = count; b.hidden = !count; });
    $$("[data-cart-items]").forEach(function (box) { box.innerHTML = list.map(lineHTML).join(""); box.hidden = !list.length; });
    $$("[data-cart-empty]").forEach(function (el) { el.hidden = !!list.length; });
    $$("[data-cart-footer]").forEach(function (el) { el.hidden = !list.length; });
    $$("[data-cart-total]").forEach(function (el) { el.textContent = (anyFrom ? "From " : "") + money(total); });
    $$("[data-cart-note]").forEach(function (el) {
      el.textContent = anyFrom ? "Some jobs start from a set price, and we confirm the total with you before the visit. Taxes calculated at checkout."
        : "Taxes, discounts and travel calculated at checkout.";
    });
    var primary = $("[data-mobile-primary]");
    if (primary) primary.textContent = count ? "View cart (" + count + ")" : "Shop services";
    if (primary) primary.setAttribute("href", count ? ROOT + "cart/" : ROOT + "collections/all/");
  }
  document.addEventListener("click", function (e) {
    var line = e.target.closest(".cart-item");
    if (!line) return;
    var key = line.getAttribute("data-key");
    var x = items().filter(function (i) { return i.key === key; })[0];
    if (!x) return;
    if (e.target.closest("[data-remove]")) setQty(key, 0);
    var b = e.target.closest("[data-q]");
    if (b) setQty(key, Math.max(0, Math.min(50, x.q + parseInt(b.getAttribute("data-q"), 10))));
  });
  document.addEventListener("change", function (e) {
    var input = e.target.closest(".cart-item .quantity__input");
    if (input) setQty(input.closest(".cart-item").getAttribute("data-key"), Math.max(0, Math.min(50, parseInt(input.value, 10) || 0)));
  });

  /* ---------- drawers and modal ---------- */
  var lastFocus = null;
  function openDrawer(el, focusSel) {
    lastFocus = document.activeElement;
    el.classList.add("active", "is-open");
    el.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("overflow-hidden");
    var f = $(focusSel, el); if (f) setTimeout(function () { f.focus(); }, 50);
  }
  function closeDrawer(el) {
    el.classList.remove("active", "is-open");
    el.setAttribute("aria-hidden", "true");
    if (!$(".cart-drawer.active, .menu-drawer.is-open, .modal.is-open")) document.documentElement.classList.remove("overflow-hidden");
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  function cartDrawer() {
    var d = $("#CartDrawer");
    $$("[data-cart-open]").forEach(function (a) {
      a.addEventListener("click", function (e) { if (location.pathname.indexOf("/cart/") === -1) { e.preventDefault(); openDrawer(d, ".drawer__close"); } });
    });
    $$("[data-cart-close]", d).forEach(function (b) { b.addEventListener("click", function () { closeDrawer(d); }); });
    var m = $("#CheckoutModal");
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-checkout]")) {
        var n = items().reduce(function (s, x) { return s + x.q; }, 0);
        $("[data-modal-summary]", m).textContent = n ? "Your cart: " + n + (n === 1 ? " item" : " items") + ". It stays saved on this device." : "";
        if (d.classList.contains("active")) closeDrawer(d);
        openDrawer(m, "[data-modal-close].button");
      }
    });
    $$("[data-modal-close]", m).forEach(function (b) { b.addEventListener("click", function () { closeDrawer(m); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      if (m.classList.contains("is-open")) closeDrawer(m);
      else if (d.classList.contains("active")) closeDrawer(d);
    });
  }
  function menuDrawer() {
    var d = $("#menu-drawer"), btn = $("[data-menu-open]");
    if (!d || !btn) return;
    btn.addEventListener("click", function () { btn.setAttribute("aria-expanded", "true"); openDrawer(d, ".drawer__close"); });
    $$("[data-menu-close]", d).forEach(function (b) { b.addEventListener("click", function () { btn.setAttribute("aria-expanded", "false"); closeDrawer(d); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && d.classList.contains("is-open")) closeDrawer(d); });
  }
  function megaMenu() {
    var hover = window.matchMedia("(hover: hover) and (min-width: 990px)");
    $$("[data-mega]").forEach(function (item) {
      var btn = $("button", item), t;
      function open() { clearTimeout(t); item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); }
      function close() { clearTimeout(t); item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
      item.addEventListener("mouseenter", function () { if (hover.matches) open(); });
      item.addEventListener("mouseleave", function () { if (hover.matches) t = setTimeout(close, 160); });
      btn.addEventListener("click", function () { item.classList.contains("is-open") ? close() : open(); });
      item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
      document.addEventListener("click", function (e) { if (!item.contains(e.target)) close(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && item.classList.contains("is-open")) { close(); btn.focus(); } });
    });
  }

  /* ---------- product forms (main-product, featured-product, hero picker) ---------- */
  function currentOpts(form) {
    var p = C[form.getAttribute("data-handle")];
    return p.o.map(function (o, i) {
      var r = form.querySelector('input[data-option-index="' + i + '"]:checked');
      return r ? r.value : o.v[0];
    });
  }
  function updateForm(form) {
    var handle = form.getAttribute("data-handle"), p = C[handle];
    if (!p) return;
    var opts = currentOpts(form);
    var price = variantPrice(handle, opts);
    var scope = form.closest("[data-product]") || form.closest("[data-hero-picker]") || form;
    var priceEl = $("[data-price]", scope);
    if (priceEl && p.v.length) priceEl.textContent = money(price);
    var from = priceEl && priceEl.parentNode.querySelector(".price__from");
    if (from && p.v.length) from.hidden = true;
    opts.forEach(function (v, i) {
      var out = form.querySelector('[data-option-value="' + i + '"]');
      if (out) out.textContent = p.o[i].l[p.o[i].v.indexOf(v)];
    });
    if (form.closest("[data-product]") && p.v.length) {
      var idx = p.v.map(function (x) { return x[0].join("|"); }).indexOf(opts.join("|"));
      try { history.replaceState(null, "", location.pathname + (idx > 0 ? "?variant=" + (idx + 1) : "")); } catch (e) { /* file:// */ }
    }
  }
  function pillsHTML(handle) {
    var p = C[handle];
    return p.o.map(function (o, i) {
      var name = "hero-" + i;
      return '<fieldset class="js product-form__input product-form__input--pill"><legend class="form__label">' + esc(o.n) +
        ': <span class="form__label-value" data-option-value="' + i + '">' + esc(o.l[0]) + '</span></legend><div class="pills">' +
        o.v.map(function (v, j) {
          return '<input type="radio" id="' + name + "-" + j + '" name="' + name + '" value="' + esc(v) + '"' + (j === 0 ? " checked" : "") + ' data-option-index="' + i + '"><label for="' + name + "-" + j + '">' + esc(o.l[j]) + "</label>";
        }).join("") + "</div></fieldset>";
    }).join("");
  }
  function heroPicker() {
    var box = $("[data-hero-picker]");
    if (!box) return;
    var form = $("form", box), img = $("[data-hero-img]", box);
    box.addEventListener("change", function (e) {
      if (e.target.name !== "hero-item") return;
      var h = e.target.value, p = C[h];
      form.setAttribute("data-handle", h);
      $("[data-hero-options]", box).innerHTML = pillsHTML(h);
      $("[data-hero-title]", box).textContent = p.t;
      $("[data-hero-link]", box).setAttribute("href", ROOT + "products/" + h + "/");
      if (img && p.img) {
        img.classList.add("is-swapping");
        setTimeout(function () { img.src = imgSrc(p); img.onload = function () { img.classList.remove("is-swapping"); }; }, reduce ? 0 : 160);
      }
      updateForm(form);
    });
  }
  function productForms() {
    $$("[data-product-form]").forEach(function (form) {
      var handle = form.getAttribute("data-handle");
      if (!C[handle]) return;
      // ?variant=N preselects options, as Shopify does with ?variant=<id>
      var m = /[?&]variant=(\d+)/.exec(location.search);
      if (m && form.closest("[data-product]")) {
        var v = C[handle].v[parseInt(m[1], 10) - 1];
        if (v) v[0].forEach(function (val, i) {
          var r = form.querySelector('input[data-option-index="' + i + '"][value="' + val.replace(/"/g, '\\"') + '"]');
          if (r) r.checked = true;
        });
      }
      form.addEventListener("change", function (e) { if (e.target.matches("[data-option-index]")) updateForm(form); });
      form.addEventListener("click", function (e) {
        var b = e.target.closest(".quantity__button");
        if (!b) return;
        var input = $(".quantity__input", b.parentNode);
        var n = (parseInt(input.value, 10) || 1) + (b.name === "plus" ? 1 : -1);
        input.value = Math.max(1, Math.min(50, n));
      });
      function add(openCheckout) {
        var h = form.getAttribute("data-handle");
        var opts = currentOpts(form);
        var props = {};
        $$("[name^='properties[']", form).forEach(function (f) { var k = f.name.slice(11, -1); if (f.value) props[k] = f.value; });
        var q = $(".quantity__input", form);
        addItem(h, opts, props, q ? Math.max(1, parseInt(q.value, 10) || 1) : 1);
        var btn = $("[data-add]", form), label = $("span", btn);
        btn.classList.add("is-added"); label.textContent = "Added";
        setTimeout(function () { btn.classList.remove("is-added"); label.textContent = "Add to cart"; }, 1600);
        var bubble = $("[data-cart-count]"); if (bubble) { bubble.classList.remove("is-bumped"); void bubble.offsetWidth; bubble.classList.add("is-bumped"); }
        if (C[h].pet && opts.some(function (o) { return o === "YES"; })) pawTrail(btn);
        if (openCheckout) $("[data-checkout]").click();
        else openDrawer($("#CartDrawer"), ".drawer__close");
      }
      form.addEventListener("submit", function (e) { e.preventDefault(); add(false); });
      var buy = $("[data-buy-now]", form);
      if (buy) buy.addEventListener("click", function () { add(true); });
      updateForm(form);
    });
  }

  /* ---------- collection sort (Dawn facets "Sort by") ---------- */
  function sorting() {
    var sel = $("[data-sort]"), grid = $("[data-grid]");
    if (!sel || !grid) return;
    var cards = $$("li", grid).filter(function (li) { return li.parentNode === grid; });
    cards.forEach(function (li, i) {
      li.dataset.i = i;
      var pr = $("[data-price]", li);
      li.dataset.p = pr ? parseFloat(pr.textContent.replace(/[^0-9.]/g, "")) : 0;
      li.dataset.t = $(".card__heading", li).textContent.trim();
    });
    sel.addEventListener("change", function () {
      var v = sel.value;
      cards.sort(function (a, b) {
        if (v === "price-asc") return a.dataset.p - b.dataset.p;
        if (v === "price-desc") return b.dataset.p - a.dataset.p;
        if (v === "title-asc") return a.dataset.t.localeCompare(b.dataset.t);
        return a.dataset.i - b.dataset.i;
      }).forEach(function (li) { grid.appendChild(li); });
    });
  }

  /* ---------- header, mobile bar, reveal ---------- */
  function stickyHeader() {
    var h = $(".section-header");
    if (!h) return;
    var on = function () { h.classList.toggle("scrolled-past-header", window.scrollY > 8); };
    on(); window.addEventListener("scroll", on, { passive: true });
  }
  function mobileActions() {
    var bar = $(".mobile-actions");
    if (!bar) return;
    var anchor = $("[data-hero-cta]");
    if (anchor && "IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { bar.classList.toggle("is-visible", !en[0].isIntersecting && en[0].boundingClientRect.top < 0); }).observe(anchor);
    } else {
      var on = function () { bar.classList.toggle("is-visible", window.scrollY > 200); };
      on(); window.addEventListener("scroll", on, { passive: true });
    }
  }
  function reveal() {
    var els = $$(".scroll-trigger");
    if (reduce || !("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("is-visible"); }); return; }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  /* Product card photo expands into the product page (cross-document view transition). */
  function expandLinks() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-vt]");
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey || reduce) return;
      var card = a.closest("[data-vt-key]");
      var m = card && $(".media", card);
      if (!m) return;
      $$("[style*='view-transition-name']").forEach(function (el) { el.style.viewTransitionName = ""; });
      m.style.viewTransitionName = "expand";
      try { sessionStorage.setItem("vt", JSON.stringify({ key: a.getAttribute("data-vt"), t: Date.now() })); } catch (x) { /* ignore */ }
    });
    window.addEventListener("pageshow", function () { $$(".card-wrapper .media").forEach(function (m) { m.style.viewTransitionName = ""; }); });
  }

  /* ---------- forms (Dawn contact form wording) ---------- */
  function fieldError(field, msg) {
    var wrap = field.closest(".field");
    wrap.classList.toggle("field--error", !!msg);
    var out = wrap.parentNode.querySelector('[data-for="' + field.id + '"]');
    if (msg && !out) {
      out = document.createElement("p"); out.className = "form__message"; out.setAttribute("data-for", field.id); out.id = field.id + "-error";
      wrap.insertAdjacentElement("afterend", out);
    }
    if (out) { out.hidden = !msg; out.innerHTML = msg ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 7v6M12 17h.01"/></svg>' + msg : ""; }
    field.setAttribute("aria-invalid", msg ? "true" : "false");
    if (msg) field.setAttribute("aria-describedby", field.id + "-error"); else field.removeAttribute("aria-describedby");
  }
  function check(field) {
    var v = field.value.trim();
    if (field.required && !v) { fieldError(field, "This field is required."); return false; }
    if (v && field.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { fieldError(field, "Enter a valid email address."); return false; }
    if (v && field.type === "tel" && v.replace(/\D/g, "").length !== 10) { fieldError(field, "Enter a 10-digit phone number."); return false; }
    fieldError(field, ""); return true;
  }
  function contactForm() {
    var form = $("[data-contact-form]");
    if (!form) return;
    var topic = /[?&]topic=([a-z]+)/.exec(location.search);
    if (topic) { var s = $("#ContactForm-topic"); if (s) s.value = topic[1]; }
    $$("input, textarea", form).forEach(function (f) { f.addEventListener("blur", function () { if (f.value.trim() || f.closest(".field--error")) check(f); }); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      $$("input, textarea", form).forEach(function (f) { if (!check(f)) ok = false; });
      var err = $("[data-form-error]", form);
      if (!ok) { err.hidden = false; err.focus && err.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" }); return; }
      // Prototype: nothing is sent. On Shopify this is the native contact form (form type "contact").
      var first = ($("#ContactForm-name").value || "").trim().split(" ")[0];
      var done = $("[data-form-success]");
      $("[data-first-name]", done).textContent = first ? ", " + first : "";
      form.hidden = true; done.hidden = false;
    });
  }
  function newsletter() {
    $$("[data-newsletter]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var input = $("input", form), msg = $("[data-newsletter-msg]", form);
        var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
        msg.hidden = false;
        msg.style.color = ok ? "#9fe0b8" : "";
        msg.textContent = ok ? "Thanks for subscribing." : "Enter a valid email address.";
        if (ok) input.value = "";
      });
    });
  }

  /* ---------- Easter eggs ---------- */
  // 1. The final band is a carpet: drag across it and fresh vacuum stripes follow, then settle back.
  function carpet() {
    $$("[data-carpet]").forEach(function (sec) {
      var cv = $("canvas", sec), ctx = cv.getContext("2d"), dpr = Math.min(window.devicePixelRatio || 1, 2);
      var marks = [], last = null, raf = null;
      function size() { cv.width = sec.clientWidth * dpr; cv.height = sec.clientHeight * dpr; draw(); }
      function base() {
        ctx.clearRect(0, 0, cv.width, cv.height);
        var w = 46 * dpr;
        for (var x = 0; x < cv.width; x += w * 2) { ctx.fillStyle = "rgba(255,255,255,0.025)"; ctx.fillRect(x, 0, w, cv.height); }
      }
      function draw() {
        base();
        var now = performance.now();
        marks = marks.filter(function (m) { return now - m.t < 4200; });
        marks.forEach(function (m) {
          var age = (now - m.t) / 4200, a = 0.16 * (1 - age);
          ctx.save(); ctx.translate(m.x, m.y); ctx.rotate(m.r);
          ctx.fillStyle = "rgba(255,255,255," + a + ")"; ctx.fillRect(-20 * dpr, -30 * dpr, 40 * dpr, 60 * dpr);
          ctx.fillStyle = "rgba(232,80,31," + a * 0.5 + ")"; ctx.fillRect(-20 * dpr, -30 * dpr, 2 * dpr, 60 * dpr); ctx.fillRect(18 * dpr, -30 * dpr, 2 * dpr, 60 * dpr);
          ctx.restore();
        });
        raf = marks.length ? requestAnimationFrame(draw) : null;
      }
      function move(x, y) {
        var r = cv.getBoundingClientRect(); x = (x - r.left) * dpr; y = (y - r.top) * dpr;
        if (last) {
          var dx = x - last.x, dy = y - last.y, d = Math.hypot(dx, dy), ang = Math.atan2(dy, dx) + Math.PI / 2;
          for (var s = 0; s < d; s += 10 * dpr) marks.push({ x: last.x + dx * s / d, y: last.y + dy * s / d, r: ang, t: performance.now() });
          if (marks.length > 900) marks.splice(0, marks.length - 900);
        }
        last = { x: x, y: y };
        if (!raf) raf = requestAnimationFrame(draw);
      }
      if (reduce) { size(); return; }
      sec.addEventListener("pointermove", function (e) { if (!e.target.closest("a, button")) move(e.clientX, e.clientY); });
      sec.addEventListener("pointerleave", function () { last = null; });
      window.addEventListener("resize", size); size();
    });
  }
  // 2. "Welcome to the family": type "family", or tap the logo five times on the home page.
  function family() {
    var toast;
    function show() {
      if (!toast) {
        toast = document.createElement("div"); toast.className = "toast"; toast.setAttribute("role", "status");
        toast.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="16" fill="#e8501f"/><path d="M11 9.5h4l1 2h-6zM17 9.5h4l1 2h-6z" fill="#10144a"/><circle cx="13" cy="15" r="2.6" fill="#10144a"/><circle cx="19.5" cy="15" r="2.6" fill="#10144a"/><path d="M9 25c.6-4 2.2-6 4-6s3.4 2 4 6M15.5 25c.6-4 2.2-6 4-6s3.4 2 4 6" fill="#10144a"/></svg><span>Welcome to the family.</span>';
        document.body.appendChild(toast);
      }
      requestAnimationFrame(function () { toast.classList.add("is-visible"); });
      setTimeout(function () { toast.classList.remove("is-visible"); }, 3200);
    }
    var buf = "";
    document.addEventListener("keydown", function (e) {
      if (e.target.closest("input, textarea, select")) return;
      buf = (buf + (e.key || "").toLowerCase()).slice(-6);
      if (buf === "family") show();
    });
    var logo = $("[data-logo]"), taps = [];
    if (logo) logo.addEventListener("click", function (e) {
      var home = location.pathname.replace(/index\.html$/, "").replace(/\/$/, "") === new URL(logo.href).pathname.replace(/\/$/, "");
      if (!home) return;
      e.preventDefault();
      var now = Date.now(); taps = taps.filter(function (t) { return now - t < 2500; }); taps.push(now);
      if (taps.length >= 5) { taps = []; show(); }
    });
  }
  // 3. Adding pet urine treatment: little paw prints trot off the button, then get cleaned up.
  function pawTrail(btn) {
    if (reduce) return;
    var r = btn.getBoundingClientRect(), box = document.createElement("div");
    box.className = "paw-trail"; box.style.left = r.left + "px"; box.style.top = (r.top - 10) + "px"; box.style.width = r.width + "px";
    var paw = '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="currentColor"><ellipse cx="12" cy="15" rx="5" ry="4.2"/><circle cx="5.5" cy="9" r="2.2"/><circle cx="9.8" cy="5.6" r="2.2"/><circle cx="14.2" cy="5.6" r="2.2"/><circle cx="18.5" cy="9" r="2.2"/></g></svg>';
    for (var i = 0; i < 6; i++) {
      var s = document.createElement("span"); s.innerHTML = paw;
      var el = s.firstChild; el.style.left = (12 + i * (r.width - 40) / 5) + "px"; el.style.top = (i % 2 ? -8 : 4) + "px";
      el.style.transform = "rotate(90deg)"; el.style.animationDelay = (i * 0.12) + "s"; box.appendChild(el);
    }
    document.body.appendChild(box);
    setTimeout(function () { box.remove(); }, 2600);
  }
  // 4. Footer stain counter: click it, a stain appears, and gets wiped straight away.
  function stain() {
    $$("[data-stain]").forEach(function (b) {
      var n = $("[data-stain-count]", b), busy = false;
      b.addEventListener("click", function () {
        if (busy) return; busy = true;
        n.textContent = "1"; b.classList.add("has-stain");
        setTimeout(function () { b.classList.add("is-wiping"); }, 700);
        setTimeout(function () { n.textContent = "0"; b.classList.remove("has-stain", "is-wiping"); busy = false; }, 1300);
      });
    });
  }
  // 5. 404 rug: tap to lift the corner.
  function rug() { var r = $("[data-rug]"); if (r) r.addEventListener("click", function () { r.classList.toggle("is-lifted"); }); }

  document.addEventListener("DOMContentLoaded", function () {
    renderCart();
    cartDrawer(); menuDrawer(); megaMenu(); stickyHeader(); mobileActions();
    heroPicker(); productForms(); sorting(); reveal(); expandLinks();
    contactForm(); newsletter();
    carpet(); family(); stain(); rug();
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
    if (window.console) console.log("%cThe Clean Don", "font-weight:700;font-size:14px;color:#1a22c4", "\nLooking under the cushions? Nothing down here but a clean codebase. Built by White Phoenix.");
  });
  window.addEventListener("storage", function (e) { if (e.key === KEY) { memory = load(); renderCart(); } });
})();
