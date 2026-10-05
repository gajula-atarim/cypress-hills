"""Small helpers for hand-building Elementor (v3 widgets + flexbox containers) JSON."""
import hashlib
import itertools

_counter = itertools.count(1)


def eid(seed=None):
    """Elementor element ids are 7-char hex strings; derive them deterministically."""
    n = next(_counter)
    return hashlib.md5(f"ch-{seed or ''}-{n}".encode()).hexdigest()[:7]


def px(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}


def box(t, r=None, b=None, l=None, unit="px"):
    """Dimensions control (padding, margin, border radius)."""
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l),
            "isLinked": t == r == b == l}


def gap(col, row=None, unit="px"):
    row = col if row is None else row
    return {"column": str(col), "row": str(row), "isLinked": col == row, "unit": unit, "size": col}


def img(media):
    return {"id": media["id"], "url": media["url"], "alt": media.get("alt", ""), "source": "library"}


def typo(prefix="typography", family="Archivo", size=None, size_t=None, size_m=None, weight=None,
         style=None, lh=None, lh_unit="em", ls=None, transform=None):
    s = {f"{prefix}_typography": "custom", f"{prefix}_font_family": family}
    if size is not None:
        s[f"{prefix}_font_size"] = px(size)
    if size_t is not None:
        s[f"{prefix}_font_size_tablet"] = px(size_t)
    if size_m is not None:
        s[f"{prefix}_font_size_mobile"] = px(size_m)
    if weight is not None:
        s[f"{prefix}_font_weight"] = str(weight)
    if style:
        s[f"{prefix}_font_style"] = style
    if lh is not None:
        s[f"{prefix}_line_height"] = px(lh, lh_unit)
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls)
    if transform:
        s[f"{prefix}_text_transform"] = transform
    return s


def container(children=None, seed=None, **settings):
    return {"id": eid(seed), "elType": "container", "isInner": False,
            "settings": settings, "elements": children or []}


def widget(wtype, seed=None, **settings):
    return {"id": eid(seed), "elType": "widget", "widgetType": wtype, "isInner": False,
            "settings": settings, "elements": []}


def mark_inner(elements, top=True):
    """Containers nested in containers must carry isInner=True."""
    for el in elements:
        if el["elType"] == "container":
            el["isInner"] = not top
        mark_inner(el.get("elements", []), top=False)
    return elements


def walk(elements):
    for el in elements:
        yield el
        yield from walk(el.get("elements", []))


def check_clean(elements):
    """Fail fast on content that would need JSON backslash escapes (quotes, newlines)."""
    import json
    raw = json.dumps(elements, ensure_ascii=False)
    bad = [c for c in ('\\"', "\\n", "\\t", "\\\\") if c in raw]
    return bad
