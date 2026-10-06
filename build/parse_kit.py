"""Extract the content of the brand-kit detail pages (shared layout) into build/kit_pages.json.

Usage: python3 parse_kit.py <path-to-Cypress-Hills-Site>
"""
import json
import re
import sys

from bs4 import BeautifulSoup

DETAIL = {
    "Pools": "pools",
    "Fiberglass Pool Installation": "fiberglass-pool-installation",
    "Swimming Pool Installation Caledon": "swimming-pool-installation-caledon",
    "Backyard Putting Greens": "backyard-putting-greens",
    "Golf Course Shaping": "golf-course-shaping",
    "Armor Stone Walls": "armor-stone-walls",
    "Artificial Grass Installation": "artificial-grass-installation",
    "Synthetic Turf Installation": "synthetic-turf-installation",
}
KIT_LINKS = {
    "Cypress%20Hills%20Home%20v2.dc.html": "/",
    "Services.dc.html": "/services/",
    "Pools.dc.html": "/pools/",
    "Projects.dc.html": "/projects/",
    "Contact.dc.html": "/contact/",
    "About.dc.html": "/about/",
}
for name, slug in DETAIL.items():
    KIT_LINKS[name.replace(" ", "%20") + ".dc.html"] = f"/{slug}/"

S3_ID = re.compile(r"generations/([0-9a-f-]{36})\.jpg")


def link(href):
    return KIT_LINKS.get(href, href)


def inner(el):
    """Inner HTML with the kit's green accent spans mapped to the theme class and
    inline links pointed at the WordPress pages (styled by .ch-inline-link)."""
    el = BeautifulSoup(str(el), "html.parser").find()
    for a in el.find_all("a"):
        a.attrs = {"href": link(a.get("href")), "class": "ch-inline-link"}
    html = el.decode_contents()
    html = re.sub(r'<a class="ch-inline-link" href="([^"]*)">', r"<a class='ch-inline-link' href='\1'>", html)
    html = re.sub(r'<a href="([^"]*)" class="ch-inline-link">', r"<a class='ch-inline-link' href='\1'>", html)
    html = re.sub(r'<span style="color:#55B847">', "<span class='ch-green'>", html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def img_id(el):
    m = S3_ID.search(el.get("src", "")) if el else None
    return m.group(1) if m else None


def section(soup, label):
    return soup.find(attrs={"data-screen-label": label})


def kicker_and_h(block):
    k = block.find("div", style=re.compile("letter-spacing:.16em"))
    return (k.get_text(" ", strip=True) if k else ""), block.find(["h1", "h2"])


def opts(script):
    """The rotating 'opts' list from the page script: titles and optional descriptions."""
    m = re.search(r"opts: (\[.*?\])\.map\(", script, re.S)
    raw = m.group(1).replace("'", '"')
    raw = re.sub(r'(?<=[A-Za-z])"(?=[a-z])', "'", raw)  # apostrophes inside words
    data = json.loads(raw)
    out = []
    for o in data:
        t, d = (o, "") if isinstance(o, str) else (o[0], o[1])
        out.append({"t": t, "d": d})
    ms = int(re.search(r"setInterval\(\(\) => this\.setState\(s => \(\{ tick: s\.tick \+ 1 \}\)\), (\d+)\)", script).group(1))
    return out, ms


def right_column(block):
    items = []
    for el in block.find_all(recursive=False):
        style = el.get("style", "")
        if el.name == "div" and "letter-spacing:.16em" in style:
            items.append({"type": "label", "text": el.get_text(" ", strip=True)})
        elif el.name == "h3":
            items.append({"type": "h3", "html": inner(el)})
        elif el.name == "p" and "Source Serif" in style:
            items.append({"type": "statement", "html": inner(el)})
        elif el.name == "p" and ("font-weight:600" in style or "font-weight:500" in style):
            items.append({"type": "lead", "html": inner(el)})
        elif el.name == "p":
            items.append({"type": "p", "html": inner(el)})
        elif el.name == "a":
            items.append({"type": "link", "text": el.get_text(" ", strip=True), "href": link(el.get("href"))})
    return items


def detail(path, slug):
    html = open(path).read()
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", attrs={"data-dc-script": True}).string

    hero = section(soup, "Hero")
    crumbs = [(a.get_text(strip=True), link(a.get("href"))) for a in hero.select("div > a")]
    current = hero.find("span", style=re.compile("color:#FFFFFF")).get_text(strip=True)
    hk, h1 = kicker_and_h(hero)
    lead = hero.find("p")

    intro = section(soup, "Intro")
    ik, ih = kicker_and_h(intro)
    imgs = [img_id(s) for s in intro.find_all("image-slot")]
    ball = re.search(r"textPath', \{ href: '#\w+' \}, '([^']*)'", script).group(1)

    elev = section(soup, "Elevate")
    ek, eh = kicker_and_h(elev)

    tour = section(soup, "Tour quality")
    wrap = tour.find("div").find_all("div", recursive=False)
    tk, th = kicker_and_h(wrap[0])
    tour_p = wrap[0].find("p", recursive=False)
    o, ms = opts(script)
    bottom = wrap[-1]
    tour_img = img_id(bottom.find("image-slot"))
    right = bottom.find_all("div", recursive=False)[-1]

    cta = section(soup, "CTA")
    ck, ch = kicker_and_h(cta)

    return {
        "slug": slug,
        "title": current,
        "nav": "pools" if "pool" in slug else "services",
        "hero": {"img": img_id(hero.find("image-slot")), "crumbs": crumbs, "current": current,
                 "kicker": hk, "h1": inner(h1), "lead": inner(lead) if lead else ""},
        "intro": {"kicker": ik, "h2": inner(ih), "img1": imgs[0], "img2": imgs[1], "ball": ball,
                  "ps": [{"html": inner(p), "lead": "font-size:17px" in p.get("style", "")}
                         for p in intro.find_all("p")]},
        "elevate": {"img": img_id(elev.find("image-slot")), "kicker": ek, "h2": inner(eh),
                    "ps": [inner(p) for p in elev.find_all("p")]},
        "tour": {"kicker": tk, "h2": inner(th), "p": inner(tour_p) if tour_p else "",
                 "opts": o, "interval": ms, "img": tour_img, "right": right_column(right)},
        "cta": {"img": img_id(cta.find("image-slot")), "kicker": ck, "h2": inner(ch),
                "p": inner(cta.find("p"))},
    }


if __name__ == "__main__":
    base = sys.argv[1].rstrip("/")
    pages = [detail(f"{base}/{name}.dc.html", slug) for name, slug in DETAIL.items()]
    with open("kit_pages.json", "w") as f:
        json.dump(pages, f, ensure_ascii=False, indent=1)
    for p in pages:
        print(p["slug"], len(p["intro"]["ps"]), len(p["elevate"]["ps"]), len(p["tour"]["opts"]),
              [r["type"] for r in p["tour"]["right"]])
