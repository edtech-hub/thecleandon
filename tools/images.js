// Image pipeline. Usage: NODE_PATH=<dir with sharp> node tools/images.js
// Every source is the client's own Shopify image (src/, not committed). Outputs WebP in assets/img.
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const SRC = "src", OUT = "assets/img";
// name: [file, widths, crop?]  crop = [w, h] ratio box for photos; white-background product shots stay uncropped
const PHOTOS = {
  "sofa": ["sofa-cleaning-0.jpg", [400, 800]],
  "loveseat": ["loveseat-cleaning-0.jpg", [400, 800]],
  "sectional": ["sectional-cleaning-0.jpg", [450]],
  "armchair": ["armchair-cleaning-0.jpg", [225]],
  "ottoman": ["ottoman-cleaning-0.jpg", [400, 800]],
  "barstool": ["chair-barstool-cleaning-0.jpg", [488]],
  "mattress": ["mattress-cleaning-0.jpg", [400, 800]],
  "curtains": ["curtains-drapery-in-place-0.png", [353]],
  "carpet": ["carpet-cleaning-0.jpg", [450]],
  "tile": ["tile-grout-cleaning-0.jpg", [500, 991]],
  "residential": ["residential-cleaning-0.jpg", [500, 1000, 1600]],
  "airbnb": ["airbnb-cleaning-0.jpg", [500, 900, 1200]],
  "window": ["window-cleaning-1.jpg", [500, 1000]],
  "window-2": ["window-cleaning-0.jpg", [500]],
  "window-3": ["window-cleaning-2.jpg", [500]],
  "commercial": ["commercial-cleaning-0.jpg", [318]],
  "detailing": ["mobile-detailing-0.png", [479]],
  "engine": ["mobile-detailing-7.jpg", [512]],
  "trash": ["trash-removal-dumpster-to-dump-0.webp", [400, 700]],
  "course": ["professional-make-ready-cleaning-course-0.jpg", [400, 800]],
  "washer": ["4000-psi-pressure-washer-0.jpg", [400, 800, 1200]],
  "chair-before": ["armchair-cleaning-4.jpg", [400, 768]],
  "chair-after": ["armchair-cleaning-5.jpg", [400, 600]],
  "pet-sealant": ["armchair-cleaning-1.png", [338]],
};
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const meta = {};
  for (const [name, [file, widths]] of Object.entries(PHOTOS)) {
    meta[name] = { widths: [] };
    for (const w of widths) {
      const info = await sharp(path.join(SRC, file)).rotate().flatten({ background: "#ffffff" })
        .resize({ width: w, withoutEnlargement: true }).webp({ quality: 72 }).toFile(path.join(OUT, `${name}-${w}.webp`));
      meta[name].widths.push(w); meta[name].w = info.width; meta[name].h = info.height;
    }
    console.log(name, meta[name]);
  }
  // Logo: white JPG to real transparency (color-to-alpha against white), as in the starter kit.
  const { data, info } = await sharp(path.join(SRC, "logo.jpg")).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const out = Buffer.alloc(info.width * info.height * 4);
  for (let i = 0, j = 0; i < data.length; i += 3, j += 4) {
    const [r, g, b] = [data[i], data[i + 1], data[i + 2]];
    const a = Math.max(255 - r, 255 - g, 255 - b); const alpha = a < 12 ? 0 : a;
    const un = (c) => (alpha === 0 ? 0 : Math.max(0, Math.min(255, Math.round((c - 255 * (1 - alpha / 255)) / (alpha / 255)))));
    out[j] = un(r); out[j + 1] = un(g); out[j + 2] = un(b); out[j + 3] = alpha;
  }
  const logo = await sharp(out, { raw: { width: info.width, height: info.height, channels: 4 } }).trim().png().toBuffer();
  await sharp(logo).resize({ height: 180 }).webp({ quality: 90, alphaQuality: 100 }).toFile(path.join(OUT, "logo.webp"));
  await sharp(logo).resize({ height: 180 }).png().toFile(path.join(OUT, "logo.png"));
  const lm = await sharp(path.join(OUT, "logo.png")).metadata(); meta.logo = { w: lm.width, h: lm.height };
  // Favicon from the mop figures (top part of the logo).
  const fig = await sharp(logo).metadata();
  const top = await sharp(logo).extract({ left: 0, top: 0, width: fig.width, height: Math.round(fig.height * 0.5) }).trim().toBuffer();
  const sq = await sharp({ create: { width: 256, height: 256, channels: 4, background: "#ffffff" } })
    .composite([{ input: await sharp(top).resize(210, 210, { fit: "contain", background: { r: 255, g: 255, b: 255, alpha: 0 } }).toBuffer(), gravity: "center" }]).png().toBuffer();
  await sharp(sq).resize(32, 32).png().toFile(path.join(OUT, "favicon-32.png"));
  await sharp(sq).resize(180, 180).png().toFile(path.join(OUT, "apple-touch-icon.png"));
  // OG image: logo on paper with the line that sums up the site.
  const svg = Buffer.from(`<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg"><rect width="1200" height="630" fill="#f4f1ea"/>
    <text x="600" y="470" text-anchor="middle" font-family="Arial" font-weight="700" font-size="46" fill="#10144a">Carpet, upholstery and home cleaning</text>
    <text x="600" y="530" text-anchor="middle" font-family="Arial" font-size="32" fill="#3d4060">Dallas-Fort Worth  |  Prices online  |  (469) 283-8431</text></svg>`);
  const lg = await sharp(path.join(OUT, "logo.png")).resize({ height: 300 }).toBuffer();
  await sharp(svg).composite([{ input: lg, top: 70, left: Math.round(600 - (lm.width * 300 / lm.height) / 2) }]).jpeg({ quality: 84 }).toFile(path.join(OUT, "og-image.jpg"));
  fs.writeFileSync("tools/img-meta.json", JSON.stringify(meta, null, 1));
  console.log("done");
})();
