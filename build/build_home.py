"""Build the Cypress Hills home page as native Elementor containers + widgets.

Run: python3 build_home.py  -> writes out/home.json (the _elementor_data element tree).
No Shortcode or HTML widgets are used; decorative behaviour hooks onto css_classes
handled by the child theme (assets/css/cypress-hills.css, assets/js/cypress-hills.js).
"""
import json
import os

from elementor_lib import box, check_clean, container, fluid, gap, img, mark_inner, px, typo, widget
import media as M

NAVY, INK, GREEN, GREEN_D, GREEN_L = "#262A78", "#0F1130", "#55B847", "#2F7A28", "#8FD67F"
CREAM, WHITE, TEXT, LINE = "#F4F2EC", "#FFFFFF", "#45475A", "#C8C4B8"

SEC_PAD = dict(padding=box(150, 72, 150, 72), padding_tablet=box(110, 40, 110, 40),
               padding_mobile=box(96, 24, 96, 24))


def section(children, bg, seed, pad=None, **extra):
    s = dict(content_width="boxed", boxed_width=px(1296), flex_direction="column",
             flex_gap=gap(48), background_background="classic", background_color=bg,
             html_tag="section")
    s.update(pad if pad is not None else SEC_PAD)
    s.update(extra)
    return container(children, seed=seed, **s)


def row(children, seed=None, gap_px=32, wrap="nowrap", justify="space-between", align="flex-end",
        stack_on="mobile", **extra):
    s = dict(content_width="full", flex_direction="row", flex_wrap=wrap, flex_gap=gap(gap_px),
             flex_justify_content=justify, flex_align_items=align, padding=box(0))
    if stack_on:
        s[f"flex_direction_{stack_on}"] = "column"
        s[f"flex_align_items_{stack_on}"] = "flex-start"
    s.update(extra)
    return container(children, seed=seed, **s)


def col(children, seed=None, gap_px=20, width=None, width_t=None, width_m=None, align=None, **extra):
    s = dict(content_width="full", flex_direction="column", flex_gap=gap(gap_px), padding=box(0))
    if width is not None:
        s["width"] = px(width, "%")
    if width_t is not None:
        s["width_tablet"] = px(width_t, "%")
    if width_m is not None:
        s["width_mobile"] = px(width_m, "%")
    if align:
        s["flex_align_items"] = align
    s.update(extra)
    return container(children, seed=seed, **s)


def kicker(text, color=GREEN_D, bar=True, seed=None):
    return widget("heading", seed=seed, title=text, header_size="div", title_color=color,
                  css_classes="ch-kicker" if bar else "",
                  **typo(size=13, weight=800, ls=2.1, transform="uppercase", lh=1.3))


def display(text, size, color=NAVY, tag="h2", lh=0.98, ls=-0.02, weight=800,
            cls="ch-wide", seed=None, **extra):
    """Display heading; size is a fluid() clamp copied from the design, ls is in em."""
    return widget("heading", seed=seed, title=text, header_size=tag, title_color=color,
                  css_classes=cls,
                  **typo(size=size, weight=weight, style="italic", lh=lh, ls=ls, ls_unit="em"), **extra)


def para(html, color=TEXT, size=17, lh=1.7, cls="ch-mw-52", seed=None, **extra):
    return widget("text-editor", seed=seed, editor=f"<p>{html}</p>", text_color=color,
                  css_classes=cls, **typo(size=size, lh=lh), **extra)


def pill_button(text, url, seed=None):
    """Navy pill with a round green arrow (icon styled by .ch-pill-btn)."""
    return widget("button", seed=seed, text=text, link={"url": url, "is_external": "", "nofollow": ""},
                  selected_icon={"value": "fas fa-arrow-right", "library": "fa-solid"},
                  icon_align="row-reverse", button_text_color=WHITE, background_color=NAVY,
                  hover_color=WHITE, button_background_hover_color="#1C1F5C",
                  border_radius=box(999), text_padding=box(8, 8, 8, 26),
                  css_classes="ch-pill-btn",
                  **typo(size=13, weight=800, ls=1, transform="uppercase", lh=1.2))


def image(m, cls="", size="full", seed=None, **extra):
    return widget("image", seed=seed, image=img(m), image_size=size, css_classes=cls,
                  width=px(100, "%"), **extra)


# ---------------------------------------------------------------------------
# 1. Hero — background slideshow + navy text panel
# ---------------------------------------------------------------------------
HERO_SLIDES = [
    (M.AERIAL, "In Business Since 1994 | 35 Years of Industry Experience",
     "Transforming Landscapes, One Project at a Time", "Creative Outdoor Services", "#services"),
    (M.POOL, "Pools", "The pool and the yard, built as one.", "Explore pools", "#services"),
    (M.STONE, "Armour stone walls", "Stone walls set by our own crew and machines.", "See stonework", "#services"),
    (M.GREEN, "Backyard putting greens", "Your own short game, steps from the house.", "See putting greens", "#services"),
    (M.COURSE, "Golf course shaping", "Greens and bunkers shaped for real courses.", "Golf & turf", "#services"),
    (M.KITCHEN, "Outdoor living", "Kitchens, cabanas and fire for long evenings.", "See outdoor living", "#services"),
    (M.NIGHT, "Landscape lighting", "A yard that works after dark.", "See lighting", "#services"),
]


def hero():
    """Hero slider: one editable container per slide (photo + navy text panel).

    The child theme script turns the .ch-slide containers into the design's slider
    (image wipe + slow zoom, panel slide-in, staggered text reveal) and drives the
    counter and the prev/next buttons below it.
    """
    slides = []
    for i, (m, kick, title, cta, url) in enumerate(HERO_SLIDES):
        panel = col([
            widget("heading", title=kick, header_size="div", title_color=GREEN_L,
                   css_classes="ch-slide-kicker",
                   **typo(size=13, weight=800, ls=0.16, ls_unit="em", transform="uppercase", lh=1.4)),
            display(title, fluid(32, 3.3, 52), WHITE, tag="h1" if i == 0 else "h2", lh=1.04,
                    ls=-0.01, cls="ch-wide ch-slide-title"),
            widget("button", text=cta, link={"url": url, "is_external": "", "nofollow": ""},
                   button_text_color=WHITE, background_color="rgba(0,0,0,0)",
                   hover_color=INK, button_background_hover_color=GREEN,
                   border_border="solid", border_width=box(2), border_color=WHITE,
                   button_hover_border_color=GREEN, border_radius=box(999),
                   text_padding=box(15, 26, 15, 26), css_classes="ch-slide-cta",
                   **typo(size=14, weight=700, ls=0.08, ls_unit="em", transform="uppercase", lh=1.2)),
        ], seed=f"hero-panel-{i}", gap_px=26, flex_justify_content="center",
            flex_align_items="flex-start",
            padding=box(110, 56, 48, 56), padding_tablet=box(110, 36, 48, 36),
            padding_mobile=box(100, 24, 40, 24),
            background_background="classic", background_color=NAVY, css_classes="ch-slide-panel")
        slides.append(container([image(m, cls="ch-slide-img"), panel], seed=f"hero-slide-{i}",
                                content_width="full", padding=box(0), css_classes="ch-slide"))

    stage = container(slides, seed="hero", content_width="full", padding=box(0),
                      background_background="classic", background_color=INK, css_classes="ch-hero")

    def arrow(label, cls, aria):
        return widget("button", text=label, link={"url": "#", "is_external": "", "nofollow": ""},
                      button_text_color=GREEN_D, background_color=WHITE, hover_color=GREEN_D,
                      button_background_hover_color=WHITE, border_border="solid",
                      border_width=box(1), border_color="#DAD6CC", button_hover_border_color=NAVY,
                      border_radius=box(999), text_padding=box(0), css_classes=f"ch-hero-arrow {cls}",
                      button_css_id="", **typo(size=24, weight=700, lh=1))

    counter = container([
        widget("heading", title="01", header_size="div", title_color=INK, css_classes="ch-hero-cur",
               **typo(size=15, weight=800, lh=1)),
        container([], content_width="full", padding=box(0), css_classes="ch-hero-bar"),
        widget("heading", title=f"0{len(HERO_SLIDES)}", header_size="div", title_color="#A8A498",
               css_classes="ch-hero-total", **typo(size=15, weight=800, lh=1)),
    ], content_width="full", flex_direction="row", flex_wrap="nowrap", flex_align_items="center",
        flex_gap=gap(14), padding=box(0), css_classes="ch-hero-count")

    arrows = container([arrow("‹", "ch-hero-prev", "Previous"), arrow("›", "ch-hero-next", "Next")],
                       content_width="full", flex_direction="row", flex_wrap="nowrap",
                       flex_gap=gap(12), padding=box(0), css_classes="ch-hero-arrows")

    controls = container([counter, arrows], seed="hero-controls", content_width="full",
                         flex_direction="row", flex_wrap="nowrap",
                         flex_justify_content="space-between", flex_align_items="center",
                         flex_gap=gap(24), padding=box(22, 72, 28, 72),
                         padding_tablet=box(20, 40, 24, 40), padding_mobile=box(18, 24, 22, 24),
                         css_classes="ch-hero-controls")

    return container([stage, controls], seed="hero-wrap", content_width="full",
                     flex_direction="column", flex_gap=gap(0), padding=box(0),
                     background_background="classic", background_color=CREAM,
                     css_classes="ch-hero-wrap")


# ---------------------------------------------------------------------------
# 2. About — intro copy + photo collage with spinning badge
# ---------------------------------------------------------------------------
def about():
    left = col([
        kicker("In Business Since 1994"),
        display("Landscaping in Toronto and <span class='ch-green'>Surrounding Areas</span>",
                fluid(40, 5, 80), ls=-0.025),
        widget("heading", title="Transform Your Outdoor Space with Landscape Design",
               header_size="h3", title_color=INK, **typo(size=fluid(20, 1.6, 24), weight=700, lh=1.3)),
        para("Cypress Hills Landscaping Inc. has been your trusted source for residential and "
             "commercial landscape design in Toronto and the surrounding area since 1994. We’ve "
             "been serving our customers with custom landscaping solutions that ensure your "
             "property stays beautiful for years to come."),
        pill_button("Make your landscaping dreams a reality", "#book"),
    ], seed="about-left", gap_px=26, width=50, width_t=100)

    badge = container([
        widget("text-path", text="SINCE 1994 • 35 YEARS OF INDUSTRY EXPERIENCE • ",
               path="circle", text_color_normal=INK,
               **typo("text_typography", size=15, weight=800, ls=3)),
        widget("heading", title="35", header_size="div", title_color=INK, align="center",
               css_classes="ch-wider", **typo(size=fluid(30, 3.4, 46), weight=900,
                                              style="italic", lh=0.9)),
        widget("heading", title="Years", header_size="div", title_color=INK, align="center",
               **typo(size=11, weight=800, ls=1.5, transform="uppercase", lh=1.4)),
    ], seed="about-badge", content_width="full", flex_direction="column",
        flex_justify_content="center", flex_align_items="center", flex_gap=gap(4),
        padding=box(0), background_background="classic", background_color=GREEN,
        css_classes="ch-badge")

    collage = container([
        image(M.POOL, cls="ch-collage-a ch-fill"),
        image(M.STONE, cls="ch-collage-b ch-fill"),
        badge,
    ], seed="about-collage", content_width="full", padding=box(0), width=px(50, "%"), width_tablet=px(100, "%"),
        css_classes="ch-collage")

    return section([row([left, collage], seed="about-row", gap_px=110, align="center",
                        stack_on="tablet")],
                   WHITE, "about", _element_id="about", overflow="hidden")


# ---------------------------------------------------------------------------
# 3. What We Do — services chips marquee
# ---------------------------------------------------------------------------
def what_we_do():
    pics = {"Landscape design": M.AERIAL, "Pools & water features": M.FALLS, "Spas": M.POOL,
            "Custom cabanas": M.KITCHEN, "Stonework": M.STONE, "Woodwork": M.CREW,
            "Outdoor kitchens": M.KITCHEN, "Pergolas": M.GREEN, "Fireplaces": M.NIGHT,
            "Outdoor lighting": M.NIGHT}
    names = list(pics)

    def chip(name, solid):
        return container([
            image(pics[name], cls="ch-chip-img", size="thumbnail"),
            widget("heading", title=name, header_size="div", title_color=NAVY if solid else WHITE,
                   css_classes="ch-wide", **typo(size=fluid(20, 2, 28), weight=800,
                                                 style="italic", lh=1.1)),
        ], content_width="full", flex_direction="row", flex_align_items="center",
            flex_gap=gap(16), padding=box(10, 28, 10, 10), border_radius=box(999),
            background_background="classic",
            background_color=WHITE if solid else "rgba(255,255,255,0.08)",
            border_border="none" if solid else "solid", border_width=box(1),
            border_color="rgba(255,255,255,0.18)", css_classes="ch-chip")

    def track(items, solid, rev):
        return container([chip(n, solid) for n in items], content_width="full",
                         flex_direction="row", flex_wrap="nowrap", flex_gap=gap(16),
                         padding=box(0), css_classes="ch-marq-track" + (" ch-marq-track--rev" if rev else ""))

    head = container([
        row([
            col([kicker("Creative Outdoor Services", GREEN_L),
                 display("What We Do", fluid(44, 6, 96), WHITE, lh=0.92, ls=-0.025)], gap_px=20),
            para("Our services include landscape design, pools &amp; water features, spas, custom "
                 "cabanas, outdoor kitchens, pergolas, stonework, woodwork, fireplaces, and outdoor "
                 "lighting. We specialize in outdoor spaces that are perfect for relaxing or "
                 "entertaining with family and friends.", color="#D9DBF0", lh=1.65),
        ], seed="wwd-row"),
    ], seed="wwd-head", content_width="boxed", boxed_width=px(1296), padding=box(140, 72, 56, 72),
        padding_tablet=box(110, 40, 48, 40), padding_mobile=box(96, 24, 40, 24))

    marquee = container([
        track(names[:7], True, False),
        track(names[5:] + names[:2], False, True),
    ], seed="wwd-marquee", content_width="full", flex_direction="column", flex_gap=gap(16),
        padding=box(0, 0, 140, 0), padding_tablet=box(0, 0, 110, 0),
        padding_mobile=box(0, 0, 96, 0), css_classes="ch-marquee", overflow="hidden")

    return container([head, marquee], seed="wwd", content_width="full", flex_direction="column",
                     flex_gap=gap(0), padding=box(0), html_tag="section",
                     background_background="classic", background_color=NAVY,
                     overflow="hidden", _element_id="services")


# ---------------------------------------------------------------------------
# 4. Custom design — sketch vs finished compare
# ---------------------------------------------------------------------------
def custom_design():
    head = row([
        col([kicker("From vision to reality"),
             display("Custom Landscape Design Tailored to Your Unique Vision", fluid(36, 4.4, 70),
                     lh=1, ls=-0.02)], gap_px=20, width=50, width_t=100),
        col([para("At Cypress Hills Landscaping Inc., we understand that your outdoor space is an "
                  "extension of your home and personal style. That’s why we offer custom landscape "
                  "design to bring your vision to life. Our experienced designers will work closely "
                  "with you to create a stunning outdoor oasis that perfectly reflects your "
                  "preferences and complements your property’s features. We’ll transform your "
                  "backyard into a tranquil retreat that you’ll love spending time in.", cls="")],
            width=50, width_t=100),
    ], seed="cd-row", gap_px=96, stack_on="tablet")

    def label(text, bg, fg, side):
        return widget("heading", title=text, header_size="div", title_color=fg,
                      css_classes=f"ch-cmp-label ch-cmp-label--{side}",
                      _background_background="classic", _background_color=bg,
                      _padding=box(10, 16, 10, 16), _border_radius=box(999),
                      **typo(size=12, weight=800, ls=1.7, transform="uppercase", lh=1.2))

    compare = container([
        image(M.SKETCH, cls="ch-cmp-img ch-fill"),
        image(M.FINISHED, cls="ch-cmp-img ch-cmp-after ch-fill"),
        label("The sketch", WHITE, NAVY, "l"),
        label("The finished yard", GREEN, INK, "r"),
    ], seed="cd-compare", content_width="full", padding=box(0), background_background="classic",
        background_color="#E2DFD6", border_radius=box(0, 0, 220, 0),
        border_radius_tablet=box(0, 0, 150, 0), border_radius_mobile=box(0, 0, 110, 0),
        css_classes="ch-compare")

    caption = widget("text-editor", editor="<p>Drag to compare the design sketch with the finished yard</p>",
                     text_color="#6B6E85", align="center", **typo(size=14, lh=1.5))

    return section([head, compare, caption], CREAM, "custom-design")


# ---------------------------------------------------------------------------
# 5. Services — rotating image + numbered list
# ---------------------------------------------------------------------------
SERVICES = [
    ("Pools", "Fiberglass pools, spas and water features, landscaped by the same crew.", M.POOL),
    ("Armour stone walls", "Retaining walls, steps and terraces set with our own machines.", M.STONE),
    ("Outdoor living", "Kitchens, cabanas, pergolas and fireplaces built around how you entertain.", M.KITCHEN),
    ("Landscape lighting", "Path, step, tree and pool lighting planned with the layout.", M.NIGHT),
    ("Putting greens", "Contoured backyard greens with fringe, cups and bunkers.", M.GREEN),
    ("Golf course shaping", "Greens, tees and bunker complexes for golf courses.", M.COURSE),
]


def services():
    head = row([
        col([kicker("What we build"), display("Six crafts.<br>One crew.", fluid(40, 5, 80))]),
        para("Every one is designed and built in-house by our own crew.", lh=1.6, cls="ch-mw-38"),
    ], seed="svc-head")

    media_box = container(
        [image(m, cls="ch-svc-img ch-fill") for _, _, m in SERVICES] + [
            widget("heading", title=SERVICES[0][0], header_size="div", title_color=INK,
                   css_classes="ch-svc-label", _background_background="classic",
                   _background_color=GREEN, _padding=box(10, 16, 10, 16), _border_radius=box(999),
                   **typo(size=13, weight=800, ls=1.6, transform="uppercase", lh=1.2))],
        seed="svc-media", content_width="full", padding=box(0), width=px(50, "%"), width_tablet=px(100, "%"),
        min_height=px(560), min_height_tablet=px(480), min_height_mobile=px(420),
        background_background="classic", background_color=INK,
        border_radius=box(0, 0, 180, 0), border_radius_mobile=box(0, 0, 100, 0),
        css_classes="ch-svc-media")

    items = []
    for i, (name, desc, _) in enumerate(SERVICES):
        items.append(container([
            widget("heading", title=f"0{i + 1}", header_size="div", title_color="#A8A498",
                   css_classes="ch-svc-num", _element_width="initial",
                   _element_custom_width=px(52), **typo(size=14, weight=800)),
            container([
                widget("heading", title=name, header_size="h3", title_color=INK,
                       css_classes="ch-svc-name ch-wide",
                       **typo(size=fluid(28, 3, 48), weight=800, style="italic", lh=1,
                              ls=-0.015, ls_unit="em")),
                widget("text-editor", editor=f"<p>{desc}</p>", text_color=TEXT,
                       css_classes="ch-svc-desc", **typo(size=15, lh=1.5)),
            ], content_width="full", flex_direction="column", flex_gap=gap(8), padding=box(0),
                css_classes="ch-svc-body", _flex_size="grow"),
            widget("icon", selected_icon={"value": "fas fa-arrow-right", "library": "fa-solid"},
                   primary_color=NAVY, size=px(18), css_classes="ch-svc-arrow"),
        ], content_width="full", flex_direction="row", flex_wrap="nowrap", flex_gap=gap(16),
            flex_align_items="center", padding=box(28, 0, 28, 0),
            border_border="solid", border_width=box(0, 0, 1, 0), border_color=LINE,
            css_classes="ch-svc-item"))

    lst = container(items, seed="svc-list", content_width="full", flex_direction="column",
                    flex_gap=gap(0), padding=box(0), width=px(50, "%"), width_tablet=px(100, "%"),
                    border_border="solid", border_width=box(1, 0, 0, 0), border_color=LINE)

    grid = row([media_box, lst], seed="svc-grid", gap_px=64, align="stretch", wrap="nowrap",
               stack_on="tablet")
    return section([head, grid], CREAM, "services", css_classes="ch-services",
                   flex_gap=gap(56), padding=box(0, 72, 150, 72),
                   padding_tablet=box(0, 40, 110, 40), padding_mobile=box(0, 24, 96, 24))


# ---------------------------------------------------------------------------
# 6. Recent work — sticky stacked project cards
# ---------------------------------------------------------------------------
PROJECTS = [
    ("Pools", "King City", "Pool, cabana & terrace",
     "A fiberglass pool set into a sloped lot with armour stone terracing and lighting.",
     ["Fiberglass pool", "Armour stone", "Cabana"], M.POOL),
    ("Stonework", "Caledon", "Hillside retaining walls",
     "Three tiers of armour stone turning a steep grade into usable lawn.",
     ["Armour stone", "Grading", "Planting"], M.STONE),
    ("Golf & turf", "Kleinburg", "Backyard short game",
     "A contoured putting green with fringe and bunker.",
     ["Putting green", "Shaping", "Turf"], M.GREEN),
    ("Full backyard", "Vaughan", "The whole estate",
     "Pool, terraces, lawn and green planned and built as one property.",
     ["Pool", "Stone", "Green", "Lighting"], M.AERIAL),
]


def work():
    head = row([
        col([kicker("Recent work"), display("Built across<br>Ontario.", fluid(40, 5, 80))]),
        pill_button("All projects", "/projects/"),
    ], seed="work-head")

    cards = []
    n = len(PROJECTS)
    for i, (cat, town, title, desc, tags, m) in enumerate(PROJECTS):
        body = container([
            widget("heading", header_size="div", title_color=GREEN, css_classes="ch-count",
                   title=f"0{i + 1}<span class='ch-count-line'></span><span class='ch-count-total'>0{n}</span>",
                   **typo(size=14, weight=800)),
            container([
                widget("heading", title=f"{cat} · {town}", header_size="div", title_color=GREEN_L,
                       **typo(size=13, weight=800, ls=2.1, transform="uppercase", lh=1.3)),
                widget("heading", title=title, header_size="h3", title_color=WHITE,
                       css_classes="ch-wide", **typo(size=fluid(36, 4.4, 72), weight=800,
                                                     style="italic", lh=0.98, ls=-0.02, ls_unit="em")),
                widget("text-editor", editor=f"<p>{desc}</p>", text_color="#E4E5F2",
                       css_classes="ch-mw-40", **typo(size=17, lh=1.55)),
                container([widget("heading", title=t, header_size="span", title_color=WHITE,
                                  css_classes="ch-tag", **typo(size=13, weight=700, lh=1.2))
                           for t in tags],
                          content_width="full", flex_direction="row", flex_wrap="wrap",
                          flex_gap=gap(8), padding=box(0)),
            ], content_width="full", flex_direction="column", flex_gap=gap(18), padding=box(0)),
        ], content_width="full", flex_direction="column", flex_justify_content="space-between",
            flex_gap=gap(24), padding=box(64), padding_tablet=box(44), padding_mobile=box(28),
            width=px(560, "px"), width_mobile=px(100, "%"), css_classes="ch-stack-body")

        cards.append(container([body], seed=f"work-card-{i}", content_width="full",
                               flex_direction="row", padding=box(0), html_tag="a",
                               link={"url": "/projects/", "is_external": "", "nofollow": ""},
                               min_height=px(460),
                               background_background="classic", background_image=img(m),
                               background_size="cover", background_position="center center",
                               background_overlay_background="gradient",
                               background_overlay_color="rgba(15,17,48,0.82)",
                               background_overlay_color_stop=px(0, "%"),
                               background_overlay_color_b="rgba(15,17,48,0)",
                               background_overlay_color_b_stop=px(100, "%"),
                               background_overlay_gradient_type="linear", background_overlay_opacity=px(1),
                               background_overlay_gradient_angle=px(90, "deg"),
                               border_radius=box(0, 0, 200, 0),
                               border_radius_tablet=box(0, 0, 140, 0),
                               border_radius_mobile=box(0, 0, 100, 0),
                               overflow="hidden", css_classes="ch-stack-card"))

    stack = container(cards, seed="work-stack", content_width="full", flex_direction="column",
                      flex_gap=gap(28), padding=box(0))
    return section([head, stack], WHITE, "work", _element_id="work", flex_gap=gap(40))


# ---------------------------------------------------------------------------
# 7. Process — four steps
# ---------------------------------------------------------------------------
STEPS = [
    ("01", "Site walk", "We walk the property with you and listen to how you want to use it.", M.STEP_WALK),
    ("02", "Design", "A drawn plan with materials and pricing, revised until it’s right.", M.STEP_DESIGN),
    ("03", "Build", "Our own crews and machines build it piece by piece.", M.STEP_BUILD),
    ("04", "Handover", "A final walkthrough, a handshake, and the keys are yours.", M.STEP_HANDOVER),
]


def process():
    head = row([
        col([kicker("How a project runs", GREEN_L),
             display("From an idea<br>to your <span class='ch-green'>keys.</span>", fluid(40, 5, 80),
                     WHITE)]),
        para("One project lead walks with you from the first site visit to the day we hand it over.",
             color="#C9CBE0", lh=1.6, cls="ch-mw-40"),
    ], seed="proc-head")

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
            widget("heading", title=title, header_size="h3", title_color=WHITE, align="center",
                   css_classes="ch-step-title ch-wide",
                   **typo(size=fluid(22, 2, 28), weight=800, style="italic", lh=1.2)),
            widget("text-editor", editor=f"<p>{desc}</p>", text_color="#E4E5F2", align="center",
                   css_classes="ch-step-desc ch-mw-28", **typo(size=15, lh=1.55)),
        ], content_width="full", flex_direction="column", flex_align_items="center",
            flex_gap=gap(18), padding=box(0), width=px(22, "%"), width_tablet=px(46, "%"),
            width_mobile=px(100, "%"), css_classes="ch-step"))

    grid = container(steps, seed="proc-grid", content_width="full", flex_direction="row",
                     flex_wrap="wrap", flex_justify_content="space-between",
                     flex_gap=gap(48, 56), padding=box(0, 0, 24, 0))
    return section([head, grid], NAVY, "process", flex_gap=gap(64), css_classes="ch-process",
                   overflow="hidden")


# ---------------------------------------------------------------------------
# 8. Awards
# ---------------------------------------------------------------------------
def awards():
    r = row([
        col([kicker("Recognition"), display("Awards Of Excellence", fluid(36, 4.2, 66), lh=1)],
            gap_px=18),
        image(M.AWARDS, cls="ch-award", _element_width="initial",
              _element_custom_width=px(620), _element_custom_width_mobile=px(100, "%")),
    ], seed="awards-row", gap_px=80, align="center", stack_on="tablet")
    return section([r], WHITE, "awards", pad=dict(padding=box(110, 72, 110, 72),
                                                  padding_tablet=box(88, 40, 88, 40),
                                                  padding_mobile=box(72, 24, 72, 24)))


# ---------------------------------------------------------------------------
# 9. Contact — background photo, details, MetForm card
# ---------------------------------------------------------------------------
def contact(form_id):
    def info(label, value_widget, full=False):
        return col([
            widget("heading", title=label, header_size="div", title_color=GREEN_L,
                   **typo(size=12, weight=800, ls=1.9, transform="uppercase", lh=1.3)),
            value_widget,
        ], gap_px=6, width=100 if full else 45, width_m=100)

    left = col([
        kicker("Work with Us", GREEN_L),
        display("Let’s walk<br>your <span class='ch-green'>yard.</span>", fluid(48, 6.4, 110), WHITE,
                lh=0.9, ls=-0.03, weight=900, cls="ch-wider"),
        para("Create a serene and beautiful oasis right in your backyard. Get in touch with our "
             "experienced professionals today so we can begin creating your perfect outdoor retreat.",
             color="#E4E5F2", size=18, lh=1.6, cls="ch-mw-44"),
        container([
            info("Phone", widget("heading", title="(905) 866-4111", header_size="div",
                                 link={"url": "tel:+19058664111", "is_external": "", "nofollow": ""},
                                 title_color=WHITE, title_hover_color=GREEN, css_classes="ch-wide",
                                 **typo(size=28, weight=800, style="italic", lh=1.2))),
            info("Hours of Operation", widget("text-editor", editor="<p>Monday-Friday, 7 a.m.-5 p.m.</p>",
                                              text_color=WHITE, **typo(size=17, lh=1.5))),
            info("Service Area", widget("text-editor",
                                        editor="<p>Caledon, Nobleton, King City, Vaughan, Kleinburg, "
                                               "Woodbridge, Muskoka, Collingwood, Toronto, and "
                                               "Surrounding Areas</p>",
                                        text_color="#E4E5F2", **typo(size=16, lh=1.6)), full=True),
        ], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=gap(24),
            padding=box(28, 0, 0, 0), border_border="solid", border_width=box(1, 0, 0, 0),
            border_color="rgba(255,255,255,0.2)"),
    ], seed="contact-left", gap_px=28, width=50, width_t=100)

    card = col([
        widget("heading", title="Contact Us", header_size="h3", title_color=NAVY,
               css_classes="ch-wide", **typo(size=30, weight=800, style="italic", lh=1.2)),
        widget("metform", mf_form_id=str(form_id)),
    ], seed="contact-card", gap_px=20, width=50, width_t=100, padding=box(44),
        padding_tablet=box(36), padding_mobile=box(28), background_background="classic",
        background_color=WHITE, border_radius=box(0, 0, 72, 0), css_classes="ch-form-card")

    r = row([left, card], seed="contact-row", gap_px=96, align="flex-start", stack_on="tablet",
            wrap="nowrap")
    return section([r], INK, "contact", _element_id="book",
                   background_background="classic", background_image=img(M.NIGHT),
                   background_size="cover", background_position="center center",
                   background_overlay_background="gradient",
                   background_overlay_color="rgba(15,17,48,0.94)",
                   background_overlay_color_stop=px(0, "%"),
                   background_overlay_color_b="rgba(15,17,48,0.6)",
                   background_overlay_color_b_stop=px(100, "%"),
                   background_overlay_gradient_type="linear", background_overlay_opacity=px(1),
                   background_overlay_gradient_angle=px(90, "deg"), overflow="hidden")


def build(form_id):
    return mark_inner([hero(), about(), what_we_do(), custom_design(), services(), work(),
                       process(), awards(), contact(form_id)])


if __name__ == "__main__":
    import sys
    form_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    tree = build(form_id)
    os.makedirs("out", exist_ok=True)
    with open("out/home.json", "w") as f:
        json.dump(tree, f, ensure_ascii=False)
    print("bad escapes:", check_clean(tree))
    print("bytes:", os.path.getsize("out/home.json"))
