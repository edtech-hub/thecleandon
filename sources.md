# Sources: every element and where it comes from

The client sells on Shopify, so store elements follow Shopify's reference theme **Dawn** (github.com/Shopify/dawn): section list, markup class names, settings and storefront wording (`locales/en.default.json`). Dawn's license only covers Shopify themes, so this repo holds none of Dawn's files: the structure, names and tokens are followed, and the CSS is our own. Content sections Dawn doesn't cover use WordPress core patterns, as in the playbook. Facts and prices come from the client's store (`/products/<handle>.js`); see the private fact sheet.

| Element | Source | What we changed |
|---|---|---|
| Announcement bar | Dawn `sections/announcement-bar.liquid` | Message about prices being online |
| Header: logo left, inline menu, icons, cart bubble | Dawn `sections/header.liquid`, `snippets/cart-icon-bubble` | Phone number shown at 1180px and up |
| Services mega menu | Dawn header "mega" menu type (`component-mega-menu.css`) | Collection cards with "From" prices |
| Mobile menu | Dawn `snippets/header-drawer.liquid` (menu-drawer) | Call and Shop buttons in the utility area |
| Hero: copy + price card | Dawn `image-banner` layout + `featured-product` section | Product switcher pills feed the featured product's variant picker |
| Variant pills | Dawn `snippets/product-variant-picker` (`product-form__input--pill`) | Pill radius 40px (Dawn default), brand ink for checked |
| Quantity input | Dawn `quantity-input` (`quantity__button`, `quantity__input`) | None |
| Trust row | Dawn `sections/multicolumn.liquid` | Our own SVG icons in brand colors |
| Shop by service | Dawn `sections/collection-list.liquid` | "From" price under each card |
| Product card | Dawn `snippets/card-product.liquid` (`card__heading`, `price`, `media--hover-effect` scale 1.03) | Short caption line per service |
| Before and after | Dawn `sections/collage.liquid` + `image-with-text` | Before / After badges (Dawn `badge`) |
| Visit steps | WordPress TT25 numbered steps, inside Dawn `image-with-text` | Steps from the store's own "Cleaning Includes" list |
| Hosts section | Dawn `image-with-text` (reversed) | Checklist from the Airbnb product description |
| Review slots | Dawn `multicolumn` used as testimonials | Empty placeholder slots, no invented reviews |
| FAQ | Dawn `sections/collapsible-content.liquid` | Two-column layout |
| Closing band | Dawn `sections/rich-text.liquid` (color scheme 3) | Carpet canvas Easter egg |
| Footer | Dawn `sections/footer.liquid` (menus, newsletter "Subscribe to our emails", social icons, policies) | Stain counter Easter egg |
| Collection page | Dawn `main-collection-banner` + `main-collection-product-grid` + `facets` (Filter, Sort by, product count) | Category filter as chips |
| Product page | Dawn `sections/main-product.liquid` (vendor caption, title, price, tax note, description, variant picker, quantity, Add to cart, Buy it now, collapsible tabs, pickup availability) | Line item properties for calculator-priced jobs; assurance list |
| Related products | Dawn `sections/related-products.liquid` ("You may also like") | None |
| Cart drawer | Dawn `snippets/cart-drawer.liquid` (`cart-item__*`, Estimated total, Check out) | Opens on Add to cart (Dawn "drawer" cart type) |
| Cart page | Dawn `main-cart-items` + `main-cart-footer` (cart note "Order special instructions") | Shopify cart attributes: service ZIP, preferred date, time window |
| Checkout notice | Dawn `product-popup-modal` | Explains Shopify checkout opens here on the live store |
| Contact page | Dawn `sections/contact-form.liquid` (Name, Email, Phone number, Comment; "Thanks for contacting us...") | Topic select, prefilled by `?topic=` |
| 404 | Dawn `sections/main-404.liquid` ("Page not found", "Continue shopping") | Rug Easter egg |
| Scroll reveal | Dawn "Reveal sections on scroll" (`scroll-trigger animate--slide-in`, slideIn 600ms `cubic-bezier(0, 0, .3, 1)`, 75ms stagger) | None |
| Page transitions, card photo expanding into product page | WordPress Performance team View Transitions + playbook section 8 | Card media and product gallery paired with `data-vt` |
| Speculative loading | WordPress 6.8 core speculation rules | None |
| Storefront wording | Dawn `locales/en.default.json`: Add to cart, Choose options, From, Sold out, Your cart, Estimated total, Check out, Your cart is empty, Continue shopping, Filter, Sort by, You may also like, View full details | Owner's plain voice everywhere else |
| URLs | Shopify routes: `/collections/<handle>`, `/products/<handle>`, `/cart`, `/pages/<handle>` | Same handles as the live store, so old links keep working |
| Font | Archivo (Shopify font library and Google Fonts), headings at width 88 | Nod to the condensed logo lettering |
| Colors | Logo: blue lettering, orange mop figures | Blue toned to pass AA with white labels |
