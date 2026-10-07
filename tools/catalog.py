"""Catalog for The Clean Don prototype.
Prices, options and variants come from data/products.json (the store's own /products/<handle>.js).
Everything written here is our plain-language copy of what the store says; see facts.md for sources."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(HERE, "..", "data", "products.json")))

UPHOLSTERY_STEPS = [
    ("We look first", "An inspection with photos, so you can see where we started."),
    ("Vacuum", "A pre-vacuum to lift loose dirt and hair."),
    ("Pre-treat and clean", "Spots get pre-treated if needed, then a pre-clean and extraction."),
    ("Protect", "Fabric sealant goes on now, if you added it."),
    ("Walk-through", "We go over it with you and take the after photos."),
]
STAIN_NOTE = "Stains like paint, oil, grease or ink that don't come out with a normal clean are handled and billed separately."

COLLECTIONS = [
    {"handle": "upholstery-cleaning", "title": "Upholstery and mattresses", "short": "Upholstery",
     "img": "sofa", "contain": True,
     "desc": "Sofas, sectionals, chairs, ottomans, mattresses and curtains. Pick the piece and the fabric, add pet urine treatment or sealant, and the price updates as you go."},
    {"handle": "carpet-and-floors", "title": "Carpet, tile and grout", "short": "Carpet and floors",
     "img": "tile", "contain": False,
     "desc": "Carpet is priced per 150 sq ft and tile and grout per 100 sq ft. Set the quantity to match your space."},
    {"handle": "home-and-rental-cleaning", "title": "Home and rental cleaning", "short": "Home and rentals",
     "img": "airbnb", "contain": False,
     "desc": "House cleans, Airbnb turnovers and windows. These start from a set price and we confirm the rest with you once we know the size of the place."},
    {"handle": "mobile-detailing", "title": "Mobile detailing", "short": "Mobile detailing",
     "img": "detailing", "contain": False,
     "desc": "We come to you. Pick your vehicle size and the package, from a deluxe wash to a full detail."},
    {"handle": "commercial-and-property", "title": "Commercial and property", "short": "Commercial and property",
     "img": "commercial", "contain": False,
     "desc": "Offices and other commercial spaces, disinfection fogging, and trash removal for clean-outs and job sites."},
]
PRO_SHOP = {"handle": "pro-shop", "title": "Pro shop", "img": "washer", "contain": False,
            "desc": "Training and tools from The Clean Don: a make-ready cleaning course, a business planning form, and a pressure washer for local pickup."}

# handle -> our copy. img: key in assets/img. contain: white-background product shot shown whole.
P = {}
def add(handle, **kw):
    kw["handle"] = handle
    raw = RAW[handle]
    kw.setdefault("title", raw["title"])
    kw["price_min"] = raw["price_min"]
    kw["options"] = raw["options"]
    kw["variants"] = raw["variants"]
    P[handle] = kw

OPTION_LABELS = {"Material": "Material", "Urine Treatment?": "Pet urine treatment", "Add Sealant?": "Fabric sealant",
                 "Size": "Size", "Vehicle Type/ Body Style": "Vehicle", "Service": "Package"}
VALUE_LABELS = {"no": "No", "YES": "Yes", "Linen/Leather/Cotton": "Linen, leather or cotton", "YES (Clear)": "Clear",
                "YES (Colored)": "Colored", "Small/ Medium Car": "Small or medium car", "Small/Medium SUV/Truck/Van": "Small or medium SUV, truck or van",
                "Large SUV/Truck/Van": "Large SUV, truck or van", "Deluxe Wash & Wax": "Deluxe wash and wax", "Deluxe Wash": "Deluxe wash",
                "Interior Restoration": "Interior restoration", "Exterior Restoration": "Exterior restoration", "Engine Clean": "Engine clean",
                "Full Detail": "Full detail", "Deluxe Full Detail": "Deluxe full detail", "Natural Stone": "Natural stone", "Large Car": "Large car"}

def upholstery(handle, title, img, line, contain=True, extra_imgs=None):
    add(handle, title=title, collection="upholstery-cleaning", img=img, contain=contain, card=line,
        summary=line + " Pick the fabric, then add pet urine treatment or a fabric sealant if you need it.",
        steps=UPHOLSTERY_STEPS, notes=[STAIN_NOTE], extra_imgs=extra_imgs or ["chair-before", "chair-after"],
        upholstery=True)

upholstery("sofa-cleaning", "Sofa cleaning", "sofa", "A standard sofa, cleaned where it sits.")
upholstery("loveseat-cleaning", "Loveseat cleaning", "loveseat", "Two-seaters and loveseats.")
upholstery("sectional-cleaning", "Sectional cleaning", "sectional", "L-shapes and multi-piece sectionals.")
upholstery("armchair-cleaning", "Armchair cleaning", "armchair", "Armchairs, accent chairs and recliners.")
upholstery("ottoman-cleaning", "Ottoman cleaning", "ottoman", "Ottomans and footstools.", contain=False)
upholstery("chair-barstool-cleaning", "Chair and barstool cleaning", "barstool", "Dining chairs and barstools, priced per chair.", contain=False)
P["chair-barstool-cleaning"]["qty_label"] = "Chairs"

add("mattress-cleaning", title="Mattress cleaning", collection="upholstery-cleaning", img="mattress", contain=False,
    card="Twin to king, priced by size.", summary="Mattress cleaning, priced by size. Twin, full, queen or king.",
    steps=None, notes=[], extra_imgs=[])
add("curtains-drapery-in-place", title="Curtain and drape cleaning", collection="upholstery-cleaning", img="curtains", contain=False,
    card="Cleaned in place, no taking them down.", summary="Curtains and drapes cleaned where they hang, so you don't have to take them down.",
    calc=True, fields=[("panels", "Number of panels", "number"), ("notes", "Fabric, length or anything we should know", "text")],
    notes=["The price shown is the starting price. We'll confirm the total with you before the visit."], extra_imgs=[])

add("carpet-cleaning", title="Carpet cleaning", collection="carpet-and-floors", img="carpet", contain=False,
    card="Priced per 150 sq ft. Wool welcome.", qty_label="Areas (150 sq ft each)",
    summary="Priced per 150 sq ft, roughly a 12 by 12 room. Choose standard or wool, then add pet urine treatment or sealant.",
    steps=[("We look first", "An inspection with photos."), ("Vacuum", "A pre-vacuum before any water touches the carpet."),
           ("Heavy soil clean", "Pre-spotting if needed, a pre-clean, then extraction."), ("Protect", "Sealant goes on now, if you added it."),
           ("Walk-through", "We go over it with you and take the after photos.")],
    notes=[STAIN_NOTE, "One quantity covers 150 sq ft. Two rooms of about 12 by 12 feet is a quantity of 2."], extra_imgs=[])
add("tile-grout-cleaning", title="Tile and grout cleaning", collection="carpet-and-floors", img="tile", contain=False,
    card="Priced per 100 sq ft. Clear or colored sealant.", qty_label="Areas (100 sq ft each)",
    summary="Priced per 100 sq ft. Standard tile or natural stone, with no sealant, a clear sealant or a colored one.",
    steps=[("We look first", "An inspection with photos."), ("Sweep", "A pre-vacuum or sweep."),
           ("Heavy soil clean", "Pre-spotting if needed, a pre-clean, then extraction."), ("Seal", "Clear or colored sealant, if you chose one."),
           ("Walk-through", "We go over it with you and take the after photos.")],
    notes=[STAIN_NOTE, "We can't take responsibility for baseboards that were sealed badly before we got there.",
           "One quantity covers 100 sq ft."],
    extra_imgs=[], caption="Before and after, tile and grout")

add("residential-cleaning", title="House cleaning", collection="home-and-rental-cleaning", img="residential", contain=False,
    card="Regular and post-construction cleans.", calc=True,
    summary="House cleaning for homes and apartments, including post-construction cleans.",
    fields=[("bedrooms", "Bedrooms", "select:1,2,3,4,5+"), ("bathrooms", "Bathrooms", "select:1,1.5,2,2.5,3,3.5,4+"),
            ("sqft", "Approx. square feet", "number"), ("type", "Type of clean", "select:Regular clean,Deep clean,Move in or move out,Post-construction")],
    notes=["Post-construction: extra paint, QuickSet and similar removal is billed separately.",
           "The price shown is the starting price. We'll confirm the total with you before the visit."], extra_imgs=[], stock=True)
add("airbnb-cleaning", title="Airbnb cleaning", collection="home-and-rental-cleaning", img="airbnb", contain=False,
    card="Turnovers between guests.", calc=True,
    summary="Turnover cleans between guests, with beds made and linen changed if you ask.",
    fields=[("bedrooms", "Bedrooms", "select:Studio,1,2,3,4,5+"), ("bathrooms", "Bathrooms", "select:1,1.5,2,2.5,3,3.5,4+"),
            ("checkout", "Guest checkout time", "time"), ("linen", "Change the linen?", "select:Yes,No")],
    included=["Dust cobwebs, ceiling fan blades, blinds and window sills", "Wipe baseboards, and smudges off doors and light switches",
              "Vacuum carpet and hard floors, stairs included, then mop", "Empty the trash", "Make the beds, and change the linen if you ask",
              "Clean mirrors and glass shower doors", "Clean and disinfect toilets, tubs, showers and vanities, and polish the chrome",
              "Wipe cabinet fronts, the stove top and front, and the microwave inside and out", "Clean and disinfect counters and the sink",
              "Load the dishwasher if it's empty, and polish the outside"],
    notes=["The price shown is the starting price. We'll confirm the total with you before the first turnover."], extra_imgs=[])
add("window-cleaning", title="Window cleaning", collection="home-and-rental-cleaning", img="window", contain=False,
    card="From single windows to full-height glass.", calc=True,
    summary="Window cleaning for every size, from a small bathroom window to full-height glass.",
    fields=[("windows", "Number of windows", "number"), ("sizes", "Mostly small, medium, large or full height?", "select:Small,Medium,Large,Full height,A mix"),
            ("stories", "Stories", "select:1,2,3+")],
    notes=["The price shown is the starting price for one window. We'll confirm the total with you before the visit."],
    extra_imgs=["window-2", "window-3"], stock=True)

DETAIL_PACKAGES = [
    ("Deluxe wash", ["Hand wash, with bugs cleared off the front end and mirrors", "Surface spots removed, then a chamois dry",
                     "Door and trunk jambs cleaned", "Rims cleaned and tires dressed", "Windows cleaned inside and out",
                     "Interior vacuumed", "Dash, console and door panels wiped down"]),
    ("Deluxe wash and wax", ["Everything in the deluxe wash", "Spray wax and paint sealant", "Rims degreased and polished", "All plastic dressed"]),
    ("Interior restoration", ["Detailed vacuum", "Carpets and mats extracted and shampooed", "Upholstery cleaned, shampooed and steamed",
                              "Windows cleaned inside", "Leather cleaned and conditioned", "Dash, steering wheel, console and door panels cleaned and conditioned",
                              "Disinfected and sanitized"]),
    ("Exterior restoration", ["Everything in the deluxe wash and wax", "Clay bar on the whole vehicle", "High speed buff and polish", "Windows cleaned outside"]),
    ("Full detail", ["Everything in the deluxe wash and wax", "Everything in the interior restoration"]),
    ("Deluxe full detail", ["Everything in the interior restoration", "Everything in the exterior restoration"]),
]
add("mobile-detailing", title="Mobile detailing", collection="mobile-detailing", img="detailing", contain=False,
    card="We come to you. Seven packages.", summary="We come to you. Pick your vehicle size and a package, and you'll see the price straight away.",
    packages=DETAIL_PACKAGES, notes=[], extra_imgs=["engine"])

add("commercial-cleaning", title="Commercial cleaning", collection="commercial-and-property", img="commercial", contain=False,
    card="Starts with a free estimate on site.", estimate=True,
    summary="Office and commercial cleaning. It starts with a free estimate on site, so the price fits your space and schedule.",
    notes=[], extra_imgs=[], stock=True)
add("viral-fogging-covid-coronavirus-sars-etc", title="Disinfection fogging", collection="commercial-and-property", img=None, contain=False,
    card="Priced per 1,000 sq ft.", qty_label="Areas (1,000 sq ft each)",
    summary="Disinfection fogging for homes and businesses, priced per 1,000 sq ft.", notes=["One quantity covers 1,000 sq ft."], extra_imgs=[])
add("trash-removal-dumpster-to-dump", title="Trash removal", collection="commercial-and-property", img="trash", contain=False,
    card="Unprepped trash to the curb, or dumpster to the dump.", calc=True,
    summary="We haul unprepped trash to the curb or a dumpster, or take a full dumpster load to the dump.",
    fields=[("haul", "What do you need?", "select:Unprepped trash to the curb or dumpster,Dumpster to the dump"),
            ("amount", "Roughly how much?", "text")],
    notes=["The price shown is the starting price. We'll confirm the total once we know the size of the load."], extra_imgs=[])

add("professional-make-ready-cleaning-course", title="Make-ready cleaning course", collection="pro-shop", img="course", contain=False,
    card="Training for cleaning technicians.", digital=True,
    summary="A course that prepares cleaning technicians to do make-ready cleans to industry standards.", notes=[], extra_imgs=[], stock=True)
add("business-planning-form-the-clean-don", title="Business planning form", collection="pro-shop", img=None, contain=False,
    card="Plan your goals and next steps.", digital=True,
    summary="A guided form that walks you through your business: your goals, how you'll get there, and where you could grow.", notes=[], extra_imgs=[])
add("4000-psi-pressure-washer", title="4000 psi pressure washer", collection="pro-shop", img="washer", contain=False,
    card="Honda GX390, 4 gpm. New.", pickup=True,
    summary="A new 4000 psi pressure washer with a Honda GX390 engine and 4 gallons per minute. Local pickup only.", notes=[], extra_imgs=[])

JOBS = [
    ("job-postings", "Cleaning technician and housekeeper",
     "Homes, hotels, Airbnbs, restaurants and salons.",
     ["Take at least 6 before photos of each room and add-on, and 6 after photos when you finish",
      "Dust top to bottom, polish furniture and fixtures",
      "Clean and sanitize bathrooms, kitchens, counters, cabinets and baseboards",
      "Make beds, change linen, wash windows, mirrors and glass",
      "Vacuum, sweep and mop, paying attention to the corners",
      "Get Airbnbs ready for the next guest, including restocking",
      "Report anything you notice, like damage or pests"]),
    ("job-postings-general-contractor", "Residential general contractor",
     "Single-family homes, multi-unit properties, Airbnbs and investor rehabs.",
     ["Walk-throughs and site assessments", "Demolition, framing, drywall, painting and trim",
      "Flooring: tile, hardwood, laminate and vinyl", "Basic plumbing and electrical repairs"]),
    ("job-postings-epa-lead-safe-renovator", "General contractor, EPA lead-safe renovator",
     "Renovation and repair work in homes and rentals, done lead-safe.",
     ["Walk-throughs and site assessments", "Demolition, framing, drywall, painting and trim",
      "Flooring and basic plumbing and electrical", "Lead-safe work practices on older properties"]),
    ("job-postings-general-contractor-copy", "Pool cleaner and maintenance technician",
     "Weekly service for residential and commercial pools.",
     ["Take at least 4 before photos on arrival and 4 after photos when you finish", "Skim, vacuum and brush walls and floors",
      "Empty skimmer and pump baskets", "Test and balance the water", "Inspect equipment and handle minor repairs"]),
]


def label(opt):
    return OPTION_LABELS.get(opt, opt)


def vlabel(v):
    return VALUE_LABELS.get(v, v)


def money(cents):
    return "${:,.2f}".format(cents / 100)


def by_collection(handle):
    return [p for p in P.values() if p["collection"] == handle]


def col_min(handle):
    items = [p for p in by_collection(handle) if not p.get("estimate")]
    return min(p["price_min"] for p in items) if items else None
