#!/usr/bin/env python3
"""Turn the store's public product JSON (raw/<handle>.js, fetched from thecleandon.com/products/<handle>.js)
into data/products.json: options, variants and prices exactly as published. Run once after fetching."""
import json, os, glob
out = {}
for f in sorted(glob.glob("raw/*.json")):
    x = json.load(open(f))
    opts = [o["name"] for o in x["options"]]
    readable = not (len(opts) == 1 and opts[0] == "Title")
    out[x["handle"]] = {
        "title": x["title"],
        "type": x["type"],
        "price_min": x["price_min"],
        "options": [{"name": o["name"], "values": o["values"]} for o in x["options"]] if readable else [],
        "variants": [{"options": v["options"], "price": v["price"]} for v in x["variants"]] if readable else [],
    }
json.dump(out, open("data/products.json", "w"), indent=1)
print(len(out), "products")
