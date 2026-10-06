"""Build the brand-kit inner pages as native Elementor containers + widgets.

Run: python3 build_pages.py  -> writes out/pages/<slug>.json and out/pages/index.json,
plus out/contact-form.json (the MetForm used on the Contact page).
Detail-page copy comes from kit_pages.json (python3 parse_kit.py <kit dir>).
"""
import json
import os

from elementor_lib import box, check_clean, container, gap, img, mark_inner, px, typo, widget, fluid
from build_home import (CREAM, GREEN, GREEN_D, GREEN_L, H1, H2, INK, LINE, NAVY, SERIF, TEXT, WHITE,
                        awards, col, display, image, kicker, para, pill_button, row, section)
import media as M

SEC = dict(padding=box(150, 72, 150, 72), padding_tablet=box(110, 40, 110, 40),
           padding_mobile=box(96, 24, 96, 24))
LINK = {"is_external": "", "nofollow": ""}


def url(u):
    return dict(LINK, url=u)


def kit(img_id):
    return M.KIT[img_id]


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------
def page_hero(m, crumbs, current, kick, h1, lead=""):
    """Photo hero with the navy panel sliding in (CSS) — breadcrumbs, kicker, H1, lead."""
    trail = "".join(f"<a href='{u}'>{label}</a><span>/</span>" for label, u in crumbs)
    trail += f"<span class='is-current'>{current}</span>"
    items = [
        widget("text-editor", editor=f"<p>{trail}</p>", text_color="#C9CBE0", css_classes="ch-crumbs",
               **typo(size=14, weight=600, lh=20, lh_unit="px")),
        kicker(kick, GREEN_L),
        display(h1, H1, WHITE, tag="h1", lh=1.1, ls=-0.01),
    ]
    if lead:
        items.append(para(lead, "#E4E5F2", cls="ch-mw-40"))
    panel = container(items, content_width="full", flex_direction="column",
                      flex_justify_content="center", flex_align_items="flex-start", flex_gap=gap(24),
                      padding=box(150, 64, 56, 64), padding_tablet=box(130, 36, 48, 36),
                      padding_mobile=box(120, 24, 48, 24), background_background="classic",
                      background_color=NAVY, css_classes="ch-ph-panel")
    return container([image(m, cls="ch-ph-img"), panel], seed="page-hero", content_width="full",
                     padding=box(0), html_tag="header", background_background="classic",
                     background_color=INK, css_classes="ch-page-hero")


def cta_buttons():
    book = widget("button", text="Book a site visit", link=url("/contact/"),
                  selected_icon={"value": "fas fa-arrow-right", "library": "fa-solid"},
                  icon_align="row-reverse", button_text_color=INK, background_color=GREEN,
                  hover_color=INK, button_background_hover_color="#7FD16F",
                  border_radius=box(999), text_padding=box(8, 8, 8, 26),
                  css_classes="ch-pill-btn ch-pill-btn--green",
                  **typo(size=14, weight=700, ls=0.08, ls_unit="em", transform="uppercase",
                         lh=14, lh_unit="px"))
    phone = widget("button", text="(905) 866-4111", link=url("tel:+19058664111"),
                   button_text_color=WHITE, background_color="rgba(0,0,0,0)", hover_color=WHITE,
                   button_background_hover_color="rgba(0,0,0,0)", border_border="solid",
                   border_width=box(2), border_color="rgba(255,255,255,0.5)",
                   button_hover_border_color=GREEN, border_radius=box(999),
                   text_padding=box(14, 26, 14, 26),
                   **typo(family=SERIF, size=22, weight=700, lh=1.1))
    return container([book, phone], content_width="full", flex_direction="row", flex_wrap="wrap",
                     flex_align_items="center", flex_gap=gap(14), padding=box(0),
                     css_classes="ch-cta-actions")


def cta(m, kick, h2, text):
    left = col([kicker(kick, GREEN_L), display(h2, color=WHITE), para(text, "#E4E5F2", cls="ch-mw-52")],
               gap_px=24, css_classes="ch-cta-copy")
    r = row([left, cta_buttons()], seed="cta-row", gap_px=40, wrap="wrap", align="flex-end")
    return section([r], INK, "cta", background_image=img(m), background_size="cover",
                   background_position="center center",
                   background_overlay_background="gradient",
                   background_overlay_color="rgba(15,17,48,0.94)",
                   background_overlay_color_stop=px(0, "%"),
                   background_overlay_color_b="rgba(15,17,48,0.5)",
                   background_overlay_color_b_stop=px(100, "%"),
                   background_overlay_gradient_type="linear", background_overlay_opacity=px(1),
                   background_overlay_gradient_angle=px(90, "deg"), overflow="hidden")


def badge(text_path, ball=False, center="35", sub="Years"):
    """Green spinning badge: '35 Years' (About) or the kit's ball with a white core (detail pages)."""
    kids = [widget("text-path", text=text_path, path="circle", text_color_normal=INK,
                   **typo("text_typography", size=15, weight=800, ls=3))]
    if ball:
        kids.append(container([], content_width="full", padding=box(0), css_classes="ch-ball-core"))
    else:
        kids += [
            widget("heading", title=center, header_size="div", title_color=INK, align="center",
                   **typo(family=SERIF, size=fluid(30, 3.4, 46), weight=700, lh=0.9)),
            widget("heading", title=sub, header_size="div", title_color=INK, align="center",
                   **typo(size=11, weight=800, ls=1.5, transform="uppercase", lh=1.4)),
        ]
    return container(kids, content_width="full", flex_direction="column",
                     flex_justify_content="center", flex_align_items="center", flex_gap=gap(4),
                     padding=box(0), background_background="classic", background_color=GREEN,
                     css_classes="ch-badge" + (" ch-ball" if ball else ""))


def collage(m1, m2, b, variant=""):
    return container([image(m1, cls="ch-collage-a ch-fill"), image(m2, cls="ch-collage-b ch-fill"), b],
                     content_width="full", padding=box(0), width=px(50, "%"),
                     width_tablet=px(100, "%"), css_classes=("ch-collage " + variant).strip())


def media_box(m, ratio="5-4", corner="br", extra=""):
    """Image filling a fixed aspect-ratio box with one big rounded corner (CSS classes)."""
    return image(m, cls=f"ch-media ch-ar-{ratio} ch-r-{corner} {extra}".strip())


def text_link(text, u):
    return widget("button", text=text, link=url(u), button_text_color=NAVY,
                  background_color="rgba(0,0,0,0)", hover_color=GREEN_D,
                  button_background_hover_color="rgba(0,0,0,0)", border_border="solid",
                  border_width=box(0, 0, 2, 0), border_color=GREEN, border_radius=box(0),
                  text_padding=box(0, 0, 6, 0), css_classes="ch-text-link",
                  **typo(size=14, weight=700, ls=0.08, ls_unit="em", transform="uppercase",
                         lh=14, lh_unit="px"))


def chips(names, interval, cls="ch-chips"):
    """Pill tags; the script highlights one at a time (ch-cycle-<ms>)."""
    return container([widget("heading", title=n, header_size="span", title_color=NAVY,
                             css_classes="ch-pill-tag", **typo(size=15, weight=700, lh=1.2))
                      for n in names],
                     content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=gap(10),
                     padding=box(0), css_classes=f"{cls} ch-cycle ch-cycle-{interval}")


def statement(html):
    return widget("text-editor", editor=f"<p>{html}</p>", text_color=NAVY, css_classes="ch-mw-54",
                  **typo(family=SERIF, size=fluid(20, 1.8, 26), weight=700, lh=1.3))


def lead(html, color=INK, weight=400):
    return widget("text-editor", editor=f"<p>{html}</p>", text_color=color, css_classes="ch-mw-54",
                  **typo(size=17, weight=weight, lh=27, lh_unit="px"))


# ---------------------------------------------------------------------------
# Detail pages (Pools + the seven service pages share one layout)
# ---------------------------------------------------------------------------
def detail_page(d):
    h, i, e, t, c = d["hero"], d["intro"], d["elevate"], d["tour"], d["cta"]
    crumbs = [(label, u) for label, u in h["crumbs"]]

    intro_text = [kicker(i["kicker"]), display(i["h2"])]
    for p in i["ps"]:
        intro_text.append(lead(p["html"]) if p["lead"] else para(p["html"], cls="ch-mw-54"))
    intro = section([row([col(intro_text, gap_px=24, width=50, width_t=100),
                          collage(kit(i["img1"]), kit(i["img2"]), badge(i["ball"], ball=True),
                                  "ch-collage--svc")],
                         seed="intro-row", gap_px=110, align="center", stack_on="tablet")],
                    WHITE, "intro")

    elev_text = [kicker(e["kicker"], GREEN_L), display(e["h2"], color=WHITE)]
    for n, p in enumerate(e["ps"]):
        elev_text.append(para(p, "#E4E5F2" if n == 0 else "#C9CBE0", cls="ch-mw-54"))
    elevate = section([row([media_box(kit(e["img"]), "5-4", "br", "ch-half"),
                            col(elev_text, gap_px=24, width=50, width_t=100)],
                           seed="elev-row", gap_px=110, align="center", stack_on="tablet",
                           flex_direction_tablet="column-reverse")],
                      NAVY, "elevate")

    head = row([col([kicker(t["kicker"]), display(t["h2"])], gap_px=20, width=50, width_t=100),
                col([para(t["p"], cls="ch-mw-54")] if t["p"] else [], width=50, width_t=100)],
               seed="tour-head", gap_px=110, align="flex-end", stack_on="tablet")
    cells = []
    for n, o in enumerate(t["opts"]):
        txt = [widget("heading", title=o["t"], header_size="h3", title_color=NAVY,
                      css_classes="ch-opt-title",
                      **typo(family=SERIF, size=fluid(22, 2, 30), weight=700, lh=1.1))]
        if o["d"]:
            txt.append(widget("text-editor", editor=f"<p>{o['d']}</p>", text_color=TEXT,
                              css_classes="ch-opt-desc", **typo(size=15, lh=23, lh_unit="px")))
        cells.append(container([
            container(txt, content_width="full", flex_direction="column", flex_gap=gap(10),
                      padding=box(0), css_classes="ch-opt-text"),
            widget("heading", title=f"0{n + 1}", header_size="div", title_color=LINE,
                   css_classes="ch-opt-num", **typo(family=SERIF, size=fluid(36, 3.4, 52), weight=700, lh=0.8)),
        ], content_width="full", flex_direction="row", flex_wrap="nowrap",
            flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(18),
            padding=box(36, 40, 36, 40), padding_mobile=box(24, 24, 24, 24), css_classes="ch-opt"))
    opts = container(cells, content_width="full", padding=box(0),
                     css_classes=f"ch-opts ch-opts-{len(cells)} ch-cycle ch-cycle-{t['interval']}")

    right = []
    for it in t["right"]:
        if it["type"] == "label":
            right.append(kicker(it["text"], bar=False))
        elif it["type"] == "h3":
            right.append(display(it["html"], fluid(22, 2, 30), tag="h3", lh=1.18, ls=0))
        elif it["type"] == "statement":
            right.append(statement(it["html"]))
        elif it["type"] == "lead":
            right.append(lead(it["html"], weight=600 if not any(x["type"] == "h3" for x in t["right"]) else 500))
        elif it["type"] == "p":
            right.append(para(it["html"], cls="ch-mw-54"))
        elif it["type"] == "link":
            right.append(text_link(it["text"], it["href"]))
    bottom = row([media_box(kit(t["img"]), "16-10", "bl", "ch-half"),
                  col(right, gap_px=22, width=46, width_t=100)],
                 seed="tour-bottom", gap_px=96, align="center", stack_on="tablet",
                 padding=box(24, 0, 0, 0))
    tour = section([head, opts, bottom], CREAM, "tour", flex_gap=gap(56))

    return mark_inner([
        page_hero(kit(h["img"]), crumbs, h["current"], h["kicker"], h["h1"], h["lead"]),
        intro, elevate, tour,
        cta(kit(c["img"]), c["kicker"], c["h2"], c["p"]),
    ])


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    ("Landscape Drawing", "Landscape Design", "d29796c7-7bdc-420d-98be-42877f39f314",
     "The key to making your house stand out is its landscaping. We will work together to review your ideas and develop a well-organized plan that aligns with your vision. Our team provides the necessary analysis, planning, creativity, problem-solving skills, quality materials, and artistic craftsmanship to create a stunning outdoor space."),
    ("Pool", "Pools and Water Features", "6b71663b-b520-44a7-94bb-a5c470c68ce1",
     "Turn your vision of the perfect pool into a reality with our swimming pool installation service. Our personalized approach to building water features sets us apart from the rest, ensuring we create a unique outdoor space tailored to your needs and budget. We specialize in steel vinyl liners and fiberglass pools of various shapes and sizes. Let us help you bring your dreams to life."),
    ("Hot Tub", "Spas", "e60daa01-e579-4885-b3b2-9a3ea46940b9",
     "We prioritize customer experience and satisfaction by building each hot tub to our customers’ specifications. Our commitment to quality is uncompromising, ensuring that every detail is carefully crafted to perfection. Trust us to provide nothing but the best for your relaxing needs."),
    ("Custom Cabanas", "Custom Cabanas", "b77c3889-6717-4556-8bb0-b9d812545c75",
     "Cozy up or entertain in style with our customized cabanas. Our team of skilled carpenters can bring your vision to life, whether you’re looking for change rooms, washrooms, outdoor showers, dining areas, wet bars, or spaces to entertain family and friends. Alternatively, you can relax on the couch and enjoy a movie. Whatever your needs, we can create the perfect cabana for you."),
    ("Outdoor Kitchen", "Outdoor Kitchens", "b77c3889-6717-4556-8bb0-b9d812545c75",
     "Add an outdoor kitchen to transform your backyard into a vibrant gathering area. It’s the perfect spot to prepare delicious gourmet meals, grill vegetables, or whip up a homemade pizza. Imagine savoring your creations while sipping on your favorite wine or enjoying a refreshing cocktail. Enhance your outdoor oasis with an outdoor kitchen that brings joy to both you and your loved ones."),
    ("Pergolas", "Pergolas", "a7606c2d-5fc9-4d4e-9486-757d5101e8ac",
     "Maximize your outdoor living space with our customizable aluminum louvered pergola. Regardless of your budget, we can work with you to create the perfect solution. Our pergolas feature retractable motorized screens, a back wall for your TV, lights, and weather-resistant, low-maintenance design elements. Enjoy the great outdoors in comfort and style."),
    ("Man Doing Stonework", "Stonework", "3ba47ee2-7f56-4aaf-9d34-bd3844bda08e",
     "With over 35 years of experience in masonry and paving stones, our team has extensive knowledge in creating driveways and walkways, designing patios, and installing custom pool decks. We also specialize in customizing staircases and retaining walls. Trust us to bring your dreams to life with our expertise and craftsmanship."),
    ("Deck", "Woodwork", "e39ef06c-0b14-4e6f-88cc-7956c6082637",
     "We have perfected the art of designing and building with our over 35 years of experience in custom woodwork. Whether you’re looking for an exquisite cabana, elegant pergola, durable shed, stylish fence, or functional deck, we have the expertise to create something tailored to your unique needs and budget. Trust us to bring your vision to life with our exceptional woodworking skills."),
    ("Fireplace", "Fireplaces", "e2ed4fb5-6ace-4fbf-beed-eeaee18f7f69",
     "Enhance your backyard space and enjoy year-round warmth with our selection of wood-burning and gas fireplaces. Whether you prefer the cozy crackle of a wood fire or the convenience of a gas fireplace, we have options to suit your needs. Consider adding fire tables, fire pits, or fire bowls to elevate your fall and winter outdoor experiences."),
    ("Beautiful House With Outdoor Lighting", "Outdoor Lighting", "e2ed4fb5-6ace-4fbf-beed-eeaee18f7f69",
     "Transform your backyard into an illuminating outdoor space with a well-designed outdoor lighting plan. Our expert team can showcase the highlights of your property, such as a pool, cabana, pergola, outdoor kitchen, stonework, woodwork, retaining walls, plants, driveway, and pathways. With carefully placed lighting, you can create a soft and warm ambiance that enhances your outdoor living space. Enjoy years of outdoor enjoyment with our professional lighting solutions."),
]
SERVICE_TAGS = ["Stone work", "Synthetic turf", "Artificial grass", "Putting greens", "Interlock",
                "Golf course shaping", "Retaining walls", "Armour stone walls", "Pool landscaping"]


def services_page():
    lead_txt = ("We provide expert stone work landscaping in Toronto, ON, helping homeowners transform "
                "their outdoor spaces into functional and visually striking landscapes.")
    hero = page_hero(M.AERIAL, [("Home", "/")], "Services",
                     "Residential &amp; Commercial Landscaping Services",
                     "Landscaping in Toronto, ON and <span class='ch-green'>Surrounding Areas</span>", lead_txt)

    left = col([kicker("What we do"),
                display("Residential &amp; Commercial <span class='ch-green'>Landscaping Services</span>"),
                chips(SERVICE_TAGS, 1800)], gap_px=24, width=50, width_t=100, css_classes="ch-sticky")
    right = col([
        lead(lead_txt + " Our customized solutions are designed to enhance curb appeal while reflecting your unique vision."),
        para("Our full range of services includes synthetic turf installation and artificial grass installation, "
             "ideal for low-maintenance, year-round greenery. We also design and install backyard putting greens, "
             "perfect for golf enthusiasts looking to elevate their outdoor living space.", cls=""),
        para("In addition, we specialize in interlock installation for patios, walkways, and driveways, as well as "
             "golf course shaping to create smooth, professional-grade landscapes. Our expertise extends to landscape "
             "stone work, including durable retaining walls and custom armour stone walls built for both strength "
             "and style.", cls=""),
        para("To complete your outdoor retreat, we offer pool landscaping that seamlessly blends stone, turf, and "
             "hardscape elements to create cohesive and inviting backyard environments.", cls=""),
        widget("text-editor", editor="<p>Ready to transform your outdoor space? Contact Cypress Hills Landscaping "
                                     "Inc. today for a free consultation, and let’s bring your vision to life!</p>",
               text_color=NAVY, css_classes="ch-quote",
               **typo(family=SERIF, size=20, weight=700, lh=1.5)),
    ], gap_px=22, width=50, width_t=100)
    intro = section([row([left, right], seed="svcs-intro", gap_px=110, align="flex-start",
                         stack_on="tablet")], WHITE, "intro")

    tiles = []
    for n, (_, name, img_id, _) in enumerate(SERVICES, 1):
        tiles.append(container([
            image(kit(img_id), cls="ch-tile-img", size="medium_large"),
            container([], content_width="full", padding=box(0), css_classes="ch-tile-shade"),
            widget("heading", title=f"{n:02d}", header_size="div", title_color=WHITE,
                   css_classes="ch-tile-num", **typo(family=SERIF, size=14, weight=700, lh=1)),
            container([
                widget("heading", title=name, header_size="div", title_color=WHITE,
                       **typo(family=SERIF, size=fluid(18, 1.4, 22), weight=700, lh=1.1)),
                widget("icon", selected_icon={"value": "fas fa-arrow-down", "library": "fa-solid"},
                       primary_color=INK, size=px(14), css_classes="ch-tile-arrow"),
            ], content_width="full", flex_direction="row", flex_wrap="nowrap",
                flex_justify_content="space-between", flex_align_items="flex-end", flex_gap=gap(10),
                padding=box(0), css_classes="ch-tile-foot"),
        ], content_width="full", padding=box(0), html_tag="a", link=url(f"#svc-{n}"),
            background_background="classic", background_color=INK, css_classes="ch-tile"))
    tile_head = row([col([kicker("Everything outdoors", GREEN_L),
                          display("Ten services.<br>One <span class='ch-green'>crew.</span>", color=WHITE)]),
                     para("From the first drawing to the last light fixture, every part of your yard is designed "
                          "and built by our own team. Pick a service to jump to it.", "#D9DBF0", cls="ch-mw-40")],
                    seed="tiles-head", wrap="wrap")
    tile_grid = container(tiles, content_width="full", padding=box(0),
                          css_classes="ch-tiles ch-cycle ch-cycle-1800")
    tile_sec = section([tile_head, tile_grid], NAVY, "tiles", flex_gap=gap(56),
                       padding=box(140, 72, 140, 72), padding_tablet=box(100, 40, 100, 40),
                       padding_mobile=box(88, 24, 88, 24), overflow="hidden")

    rows = []
    for n, (k, name, img_id, desc) in enumerate(SERVICES, 1):
        flip = n % 2 == 0
        media = container([
            image(kit(img_id), cls="ch-fill ch-abs"),
            widget("heading", title=f"{n:02d}", header_size="div", title_color=INK,
                   css_classes="ch-row-num", **typo(family=SERIF, size=20, weight=700, lh=1)),
        ], content_width="full", padding=box(0), width=px(50, "%"), width_tablet=px(100, "%"),
            css_classes="ch-row-media " + ("ch-r-bl" if flip else "ch-r-br"))
        text = col([kicker(k), display(name, fluid(22, 2, 30), tag="h3", lh=1.18, ls=-0.02),
                    para(desc, cls="ch-mw-54"), text_link("Get a free consultation →", "/contact/")],
                   gap_px=22, width=46, width_t=100)
        rows.append(container([media, text], seed=f"svc-row-{n}", content_width="full",
                              flex_direction="row-reverse" if flip else "row", flex_wrap="nowrap",
                              flex_direction_tablet="column", flex_align_items="center",
                              flex_gap=gap(96, 48), padding=box(0), _element_id=f"svc-{n}",
                              css_classes="ch-svc-row"))
    list_sec = section(rows, CREAM, "svc-rows", flex_gap=gap(130), flex_gap_tablet=gap(96),
                       flex_gap_mobile=gap(72), padding=box(128, 72, 150, 72),
                       padding_tablet=box(96, 40, 110, 40), padding_mobile=box(80, 24, 96, 24))

    return mark_inner([hero, intro, tile_sec, list_sec,
                       cta(M.NIGHT, "Work with Us", "Let’s walk<br>your <span class='ch-green'>yard.</span>",
                           "Schedule a consultation with our residential landscaping experts to discuss your "
                           "exterior renovation and turn your dream landscape project into a reality.")])


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
STEPS = [
    ("01", "Site walk", "We walk the property with you and listen to how you want to use it.", M.STEP_WALK),
    ("02", "Design", "A drawn plan with materials and pricing, revised until it’s right.", M.STEP_DESIGN),
    ("03", "Build", "Our own crews and machines build it piece by piece.", M.STEP_BUILD),
    ("04", "Handover", "A final walkthrough, a handshake, and the keys are yours.", M.STEP_HANDOVER),
]
AREAS = ["Caledon", "Nobleton", "King City", "Vaughan", "Kleinburg", "Woodbridge", "Muskoka",
         "Collingwood", "Toronto"]


def process_light():
    head = row([col([kicker("How a project runs"),
                     display("From an idea<br>to your <span class='ch-green'>keys.</span>")]),
                para("One project lead walks with you from the first site visit to the day we hand it over.",
                     cls="ch-mw-40")], seed="proc-head")
    steps = []
    for n, title, desc, m in STEPS:
        circle = container([
            image(m, cls="ch-step-img"),
            widget("heading", title=n, header_size="div", title_color=INK, align="center",
                   css_classes="ch-step-num", _background_background="classic",
                   _background_color=GREEN, **typo(size=15, weight=800, lh=1)),
        ], content_width="full", flex_direction="column", flex_justify_content="center",
            flex_align_items="center", padding=box(0), background_background="classic",
            background_color=WHITE, css_classes="ch-step-circle")
        steps.append(container([
            circle,
            widget("heading", title=title, header_size="h3", title_color=NAVY, align="center",
                   css_classes="ch-step-title",
                   **typo(family=SERIF, size=fluid(22, 2, 28), weight=700, lh=1.2)),
            widget("text-editor", editor=f"<p>{desc}</p>", text_color=TEXT, align="center",
                   css_classes="ch-step-desc ch-mw-28", **typo(size=15, lh=1.55)),
        ], content_width="full", flex_direction="column", flex_align_items="center",
            flex_gap=gap(18), padding=box(0), width=px(22, "%"), width_tablet=px(46, "%"),
            width_mobile=px(100, "%"), css_classes="ch-step"))
    grid = container(steps, seed="proc-grid", content_width="full", flex_direction="row",
                     flex_wrap="wrap", flex_justify_content="space-between",
                     flex_gap=gap(48, 56), padding=box(0, 0, 24, 0))
    return section([head, grid], CREAM, "process", flex_gap=gap(64),
                   css_classes="ch-process ch-process--light", overflow="hidden")


def about_page():
    hero = page_hero(M.CREW, [("Home", "/")], "About", "In Business Since 1994",
                     "Transforming landscapes since <span class='ch-green'>1994.</span>",
                     "Residential and commercial landscape design in Toronto and the surrounding area, "
                     "with 35 years of industry experience.")
    story_text = col([
        kicker("Our story"),
        display("We build the whole yard, <span class='ch-green'>ourselves.</span>"),
        para("Cypress Hills started in 1994 with landscape construction and grew into a full design-build "
             "company. Today our crews handle pools, armour stone, outdoor living, lighting, putting greens "
             "and golf course shaping."),
        para("We keep the work in-house. The people who design your yard talk to the people who build it "
             "every day, and one project lead stays with you from the first site walk to the final walkthrough."),
    ], gap_px=24, width=50, width_t=100)
    story = section([row([collage(M.STONE, M.KITCHEN, badge("SINCE 1994 • 35 YEARS OF INDUSTRY EXPERIENCE • ")),
                          story_text], seed="story-row", gap_px=110, align="center", stack_on="tablet",
                         flex_direction_tablet="column-reverse")], WHITE, "story", overflow="hidden")

    values = []
    for n, (t, dsc) in enumerate([
            ("Experienced", "Over thirty years of building in Ontario soil and Ontario winters."),
            ("Direct", "Clear plans, clear pricing, and straight answers about schedule."),
            ("Accountable", "One project lead and one number to call for the whole job.")], 1):
        values.append(container([
            widget("heading", title=f"0{n}", header_size="div", title_color="rgba(255,255,255,0.22)",
                   css_classes="ch-value-num", **typo(family=SERIF, size=fluid(44, 4.1, 65), weight=700, lh=0.8)),
            widget("heading", title=t, header_size="h3", title_color=WHITE,
                   **typo(family=SERIF, size=fluid(26, 2.4, 34), weight=700, lh=1.15)),
            para(dsc, "#C9CBE0", cls="ch-mw-34"),
        ], content_width="full", flex_direction="column", flex_gap=gap(18), padding=box(28, 0, 0, 0),
            border_border="solid", border_width=box(2, 0, 0, 0), border_color="rgba(255,255,255,0.18)",
            css_classes="ch-value"))
    vals = section([col([kicker("How we work", GREEN_L),
                         display("Three things we<br>never <span class='ch-green'>skip.</span>", color=WHITE)]),
                    container(values, content_width="full", padding=box(0),
                              css_classes="ch-values ch-cycle ch-cycle-2200")],
                   NAVY, "values", flex_gap=gap(64))

    areas = section([row([
        col([kicker("Service Area"), display("Where we <span class='ch-green'>build.</span>"),
             para("Caledon, Nobleton, King City, Vaughan, Kleinburg, Woodbridge, Muskoka, Collingwood, "
                  "Toronto, and Surrounding Areas", cls="ch-mw-46"),
             chips(AREAS, 2200)], gap_px=24, width=46, width_t=100),
        media_box(M.AERIAL, "5-4", "br", "ch-half"),
    ], seed="areas-row", gap_px=110, align="center", stack_on="tablet")], WHITE, "areas")

    return mark_inner([hero, story, vals, process_light(), areas, awards(),
                       cta(M.NIGHT, "Work with Us", "Let’s walk<br>your <span class='ch-green'>yard.</span>",
                           "Create a serene and beautiful oasis right in your backyard. Get in touch with our "
                           "experienced professionals today so we can begin creating your perfect outdoor retreat.")])


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
def projects_page():
    hero = page_hero(M.AERIAL, [("Home", "/")], "Projects", "Our work",
                     "Built across <span class='ch-green'>Ontario.</span>",
                     "Pools, stonework, greens and outdoor living built across the GTA and cottage country.")
    head = row([col([kicker("Project gallery"), display("Every yard, one <span class='ch-green'>crew.</span>")]),
                widget("heading", header_size="div", title_color=TEXT, css_classes="ch-gallery-count",
                       title=f"<span class='ch-count-n'>{len(M.GALLERY)}</span> photos · click any to view",
                       **typo(size=14, weight=700, lh=1.3))], seed="gal-head", wrap="wrap")
    gallery = widget("image-gallery", wp_gallery=[{"id": m["id"], "url": m["url"]} for m in M.GALLERY],
                     thumbnail_size="medium_large", gallery_columns="3", gallery_link="file",
                     open_lightbox="yes", gallery_display_caption="none", image_spacing="custom",
                     image_spacing_custom=px(20), image_border_radius=box(8), css_classes="ch-gallery")
    gal = section([head, gallery], CREAM, "gallery", flex_gap=gap(56), flex_gap_mobile=gap(36),
                  padding=box(128, 72, 150, 72), padding_tablet=box(96, 40, 110, 40),
                  padding_mobile=box(80, 16, 96, 16))
    return mark_inner([hero, gal, awards(),
                       cta(M.NIGHT, "Work with Us", "Your yard<br>could be <span class='ch-green'>next.</span>",
                           "Create a serene and beautiful oasis right in your backyard. Get in touch with our "
                           "experienced professionals today so we can begin creating your perfect outdoor retreat.")])


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def contact_page(form_placeholder="CONTACT_FORM_ID"):
    hero = page_hero(M.NIGHT, [("Home", "/")], "Contact", "Work with Us",
                     "Let’s walk your <span class='ch-green'>yard.</span>",
                     "Create a serene and beautiful oasis right in your backyard. Get in touch with our "
                     "experienced professionals today so we can begin creating your perfect outdoor retreat.")
    head = row([col([kicker("Contact Us"), display("Book a site <span class='ch-green'>visit.</span>")]),
                para("We’ll measure, listen, and send you a drawn plan with pricing.", cls="ch-mw-44")],
               seed="c-head", wrap="wrap")

    def label(t, color=GREEN_D):
        return kicker(t, color, bar=False)

    phone = container([
        label("Phone", GREEN_L),
        widget("heading", title="(905) 866-4111", header_size="div", title_color=WHITE,
               **typo(family=SERIF, size=fluid(28, 2.6, 38), weight=700, lh=1.1)),
        widget("heading", title="Call now", header_size="div", title_color=WHITE, css_classes="ch-call-now",
               **typo(size=14, weight=700, ls=0.08, ls_unit="em", transform="uppercase", lh=14, lh_unit="px")),
    ], content_width="full", flex_direction="column", flex_gap=gap(18), padding=box(40),
        padding_mobile=box(28), html_tag="a", link=url("tel:+19058664111"),
        background_background="classic", background_color=NAVY, border_radius=box(8, 8, 64, 8),
        css_classes="ch-phone-card")
    hours = container([
        label("Hours of Operation"),
        widget("text-editor", editor="<p>Monday-Friday, 7 a.m.-5 p.m.</p>", text_color=INK,
               **typo(size=17, weight=600, lh=26, lh_unit="px")),
    ], content_width="full", flex_direction="column", flex_gap=gap(12), padding=box(32),
        padding_mobile=box(24), background_background="classic", background_color=WHITE,
        border_radius=box(8))
    area = container([
        label("Service Area"),
        container([widget("heading", title=a, header_size="span", title_color=NAVY, css_classes="ch-town",
                           **typo(size=14, weight=600, lh=1.2)) for a in AREAS],
                  content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=gap(8),
                  padding=box(0)),
        widget("text-editor", editor="<p>and Surrounding Areas</p>", text_color=TEXT,
               **typo(size=14, lh=22, lh_unit="px")),
    ], content_width="full", flex_direction="column", flex_gap=gap(14), padding=box(32),
        padding_mobile=box(24), background_background="classic", background_color=WHITE,
        border_radius=box(8), _flex_grow=1, css_classes="ch-area-card")
    left = col([phone, hours, area], gap_px=16, width=33, width_t=100)

    card = col([
        display("Send us a message", fluid(22, 2, 30), tag="h3", lh=1.18, ls=0),
        widget("metform", mf_form_id=form_placeholder),
    ], seed="c-card", gap_px=22, width=67, width_t=100, padding=box(48), padding_tablet=box(36),
        padding_mobile=box(28), background_background="classic", background_color=WHITE,
        border_radius=box(8, 8, 72, 8), css_classes="ch-form-card ch-form-card--page")
    grid = row([left, card], seed="c-grid", gap_px=24, align="stretch", stack_on="tablet")
    sec = section([head, grid], CREAM, "contact", flex_gap=gap(56), padding=box(128, 72, 128, 72),
                  padding_tablet=box(96, 40, 96, 40), padding_mobile=box(80, 20, 80, 20))
    return mark_inner([hero, sec, awards()])


def contact_form():
    def field(wtype, name, cap, placeholder, required):
        s = dict(mf_input_label_status="yes", mf_input_label=cap, mf_input_name=name,
                 mf_input_placeholder=placeholder, css_classes="ch-field")
        if required:
            s.update(mf_input_required="yes", mf_input_validation_warning_message="This field is required.")
        return widget(wtype, **s)

    interests = widget("mf-checkbox", mf_input_label_status="yes", mf_input_label="I'm thinking about",
                       mf_input_name="interests", mf_input_display_option="inline-block",
                       css_classes="ch-interests",
                       mf_input_list=[{"_id": f"c0ffee{i}", "mf_input_option_text": o,
                                       "mf_input_option_value": o.lower().replace(" ", "-"),
                                       "mf_input_option_status": ""}
                                      for i, o in enumerate(["Pool", "Stonework", "Outdoor living",
                                                             "Putting green", "Full backyard"])])
    fields = container([
        field("mf-text", "name", "Name", "Enter Name", True),
        field("mf-telephone", "phone", "Phone", "Enter your phone number", True),
        field("mf-email", "email", "Email", "Enter Email", False),
        field("mf-text", "subject", "Subject", "Enter your subject", False),
    ], content_width="full", padding=box(0), css_classes="ch-field-grid")
    message = widget("mf-textarea", mf_input_label_status="yes", mf_input_label="Message",
                     mf_input_name="message", mf_input_placeholder="Tell us about the property",
                     css_classes="ch-field")
    button = widget("mf-button", mf_btn_text="Send message", mf_btn_align="left",
                    mf_btn_icon={"value": "fas fa-arrow-right", "library": "fa-solid"},
                    mf_btn_icon_align="right", mf_btn_text_color=INK, mf_btn_hover_color=INK,
                    mf_btn_bg_color_background="classic", mf_btn_bg_color_color=GREEN,
                    mf_btn_bg_hover_color_background="classic", mf_btn_bg_hover_color_color="#7FD16F",
                    mf_btn_border_radius=box(999), mf_btn_text_padding=box(8, 8, 8, 28),
                    css_classes="ch-send",
                    **typo("mf_btn_typography", size=14, weight=700, ls=0.08, ls_unit="em",
                           transform="uppercase", lh=14, lh_unit="px"))
    return mark_inner([container([interests, fields, message, button], seed="cform", content_width="full",
                                 flex_direction="column", flex_gap=gap(22), padding=box(0))])


# ---------------------------------------------------------------------------
PAGES = [
    # (slug, title, nav parent key)
    ("about", "About", None),
    ("services", "Services", None),
    ("projects", "Projects", None),
    ("contact", "Contact", None),
]

if __name__ == "__main__":
    os.makedirs("out/pages", exist_ok=True)
    details = json.load(open("kit_pages.json"))
    built = {"about": about_page(), "services": services_page(), "projects": projects_page(),
             "contact": contact_page()}
    index = [{"slug": s, "title": t} for s, t, _ in PAGES]
    for d in details:
        built[d["slug"]] = detail_page(d)
        index.append({"slug": d["slug"], "title": d["title"]})
    for slug, tree in built.items():
        with open(f"out/pages/{slug}.json", "w") as f:
            json.dump(tree, f, ensure_ascii=False)
        print(slug, os.path.getsize(f"out/pages/{slug}.json"), check_clean(tree))
    with open("out/pages/index.json", "w") as f:
        json.dump(index, f, ensure_ascii=False)
    with open("out/contact-form.json", "w") as f:
        json.dump(contact_form(), f, ensure_ascii=False)
    print("contact-form", check_clean(contact_form()))
