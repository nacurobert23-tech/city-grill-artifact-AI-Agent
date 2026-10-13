"""Build data/reviews.js for the dashboard from the coded reviews CSV.

Usage: python3 tools/build_data.py <city_grill_reviews_coded.csv> <legacy index.html with coded sample>

Google review text is NOT written to the output (Google Maps terms restrict
redistribution); only ratings, codes and features derived from the text are kept.
Tripadvisor rows are already paraphrased, so their text is kept.
"""
import csv, json, re, sys, unicodedata

CSV, LEGACY = sys.argv[1], sys.argv[2]
OUT = "data/reviews.js"
TA_FROM = "2025-01"   # v2 interface covers Tripadvisor visits from Jan 2025

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# Dish and drink dictionary, multilingual, matched on diacritic-free lower-case text
ITEMS = {
    "knuckle":  ["ciolan", "pork knuckle", "knuckle", "stinco", "golonka", "golonk", "codillo", "codillo", "haxe", "eisbein", "jarret", "pork shank", "joelho"],
    "papanasi": ["papanas", "papanasi"],
    "sarmale":  ["sarmal", "cabbage roll", "involtini di cavolo", "golabk", "golabki"],
    "mici":     ["mici", "mititei"],
    "soup":     ["ciorba", "soup", "zuppa", "sopa", "zupa", "suppe", "soupe", "bors"],
    "polenta":  ["mamaliga", "polenta"],
    "lamb":     ["miel", "lamb", "agnello", "cordero", "jagniec", "jagnie", "lamm", "agneau", "kuzu"],
    "ribs":     ["coaste", "costite", "ribs", "costine", "costillas", "zeberk", "rippchen", "ribbetjes"],
    "platter":  ["platou", "platter", "tagliere", "plato combinado", "deska", "platte"],
    "duck":     ["rata", "duck", "anatra", "pato", "kaczk", "ente", "canard"],
    "schnitzel":["snitel", "schnitzel", "cotoletta", "escalope"],
    "fries":    ["cartofi prajiti", "fries", "patatine", "patatas fritas", "frytki", "pommes"],
    "bread":    ["paine", "bread", "pane", "chleb", "brot", "brotchen"],
    "beer":     ["bere", "beer", "birra", "cerveza", "piwo", "bier", "biere"],
    "wine":     ["wine", "vinul", "vinuri", "vinului", "vin rosu", "vin alb", "vin fiert", "vino", "wino", "wein", "vinho"],
}
ITEM_RE = {k: re.compile(r"\b(" + "|".join(re.escape(w) for w in ws) + r")", re.I) for k, ws in ITEMS.items()}
# words that must match whole-word only (short, ambiguous)
WHOLE = {"rata", "pane", "bere", "mici", "bors", "pato", "ente", "vino", "wino", "brot", "vin rosu", "vin alb"}
for k, ws in ITEMS.items():
    parts = [(re.escape(w) + (r"\b" if w in WHOLE else "")) for w in ws]
    ITEM_RE[k] = re.compile(r"\b(" + "|".join(parts) + r")", re.I)

FILLER = set(norm(w) for w in """multumim multumesc multumiri multumita thanks thank you thx merci grazie gracias danke dziekuje
super bravo top excelent excelenta perfect perfecta great amazing excellent best the a si and e o ospatar ospatarul ospatarita
waiter waitress cameriere cameriera camarero camarera kelner kelnerka chelner chelnerul mr mrs domnul doamna dl dna a fost was is
very foarte molto muy bardzo""".split())

legacy = open(LEGACY, encoding="utf-8").read()
m = re.search(r"const R = (\[\n.*?\n\]);", legacy, re.S)
R = json.loads(re.sub(r"\{f:(\d),s:(\d),v:(\d),a:(\d)\}", r'{"f":\1,"s":\2,"v":\3,"a":\4}', m.group(1)))
VCODE = {"Caru' cu Bere": "ccb", "Hanu' lui Manuc": "hlm"}

rows = []
for r in csv.DictReader(open(CSV, encoding="utf-8-sig")):
    g = r["source"] == "Google"
    v = VCODE[r["restaurant"]]
    if not g and r["date"] < TA_FROM:
        continue
    text = r["text"].strip()
    n = norm(text)
    names = [w for w in r["waiters_named"].split(";") if w]
    words = re.findall(r"[a-z]+", n)
    name_tok = set(re.findall(r"[a-z]+", norm(" ".join(names))))
    rest = [w for w in words if w not in name_tok and w not in FILLER]
    name_only = int(bool(text) and bool(names) and len(rest) <= 2)
    items = [k for k, rx in ITEM_RE.items() if rx.search(n)]
    # Romanian "mici" also means "small" (portii mici, preturi mai mici): drop those uses
    if "mici" in items and not re.search(r"mititei|micii\b", n):
        food_use = [m for m in re.finditer(r"\bmici\b", n)
                    if not re.search(r"(portii\w*|cantitat\w*|pretur\w*|foarte|mai|sunt|destul de)\s+$", n[max(0, m.start() - 25):m.start()])]
        if not food_use:
            items.remove("mici")
    themes = [t for t in r["themes"].split(";") if t]
    if g:
        pol = None  # polarity follows the star band for Google
    else:
        pol = json.loads(r["theme_polarity"])
    sub = None
    if not g:
        hit = [x for x in R if x[0] == v and x[1] == r["date"] and x[2] == int(r["rating"]) and x[5] == text]
        assert len(hit) == 1, text
        sub = hit[0][3]
    rows.append([
        0 if g else 1, v, r["date"], int(r["rating"]), r["language"] or "",
        themes if g else [("+" if pol[t] > 0 else "-") + t for t in pol],
        len(names) > 0 and 1 or 0,
        (1 if r["owner_replied"] == "1" else 0) if g else None,
        int(r["quotes_price"] or 0),
        1 if text else 0,
        name_only,
        len(words),
        items,
        "" if g else text,
        sub,
    ])

meta = {
    "built": "2026-10-14",
    "fields": ["src(0=Google,1=Tripadvisor)", "venue", "date", "stars", "lang", "themes", "waiterNamed", "ownerReplied", "quotesPrice", "hasText", "nameOnly", "words", "items", "text", "sub"],
    "googleTextIncluded": False,
    "tripadvisorFrom": TA_FROM,
    "itemsDictionary": ITEMS,
}
with open(OUT, "w", encoding="utf-8") as f:
    f.write("// Generated by tools/build_data.py from data/city_grill_reviews_coded.csv. Do not edit by hand.\n")
    f.write("window.CG_META=" + json.dumps(meta, ensure_ascii=False) + ";\n")
    f.write("window.CG_ROWS=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(rows), "rows written to", OUT)
