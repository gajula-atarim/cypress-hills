"""UAE header + footer templates and the MetForm contact form, as Elementor trees."""
import json
import os

from elementor_lib import box, check_clean, container, gap, img, mark_inner, px, typo, widget
import media as M

NAVY, INK, GREEN, GREEN_D, GREEN_L, CREAM, WHITE = (
    "#262A78", "#0F1130", "#55B847", "#2F7A28", "#8FD67F", "#F4F2EC", "#FFFFFF")


def header():
    nav = widget("navigation-menu", menu="primary-menu", layout="horizontal", navmenu_align="right",
                 submenu_icon="arrow", submenu_animation="slide_up", pointer="none",
                 dropdown="tablet", resp_align="right", full_width_dropdown="yes",
                 padding_horizontal_menu_item=px(15), padding_vertical_menu_item=px(10),
                 menu_space_between=px(4),
                 color_menu_item=WHITE, color_menu_item_hover=WHITE, color_menu_item_active=WHITE,
                 bg_color_menu_item="rgba(0,0,0,0)", bg_color_menu_item_hover="rgba(255,255,255,0.16)",
                 bg_color_menu_item_active="rgba(255,255,255,0.18)",
                 background_color_dropdown_item=WHITE, background_color_dropdown_item_hover=CREAM,
                 background_color_dropdown_item_active=CREAM,
                 color_dropdown_item=NAVY, color_dropdown_item_hover=GREEN_D,
                 color_dropdown_item_active=GREEN_D,
                 dropdown_border_radius=box(0, 0, 40, 0), width_dropdown_item=px(260),
                 padding_horizontal_dropdown_item=px(16), padding_vertical_dropdown_item=px(13),
                 dropdown_divider_border="none", distance_from_menu=px(12),
                 toggle_color=WHITE, toggle_hover_color=GREEN_L, toggle_size=px(22),
                 **typo("menu_typography", size=14, weight=600, lh=1.2),
                 **typo("dropdown_typography", size=14, weight=700, lh=1.35))

    cta = widget("button", text="Contact Us", link={"url": "/#book", "is_external": "", "nofollow": ""},
                 button_text_color=INK, background_color=GREEN, hover_color=INK,
                 button_background_hover_color="#7FD16F", border_radius=box(999),
                 text_padding=box(12, 20, 12, 20), hide_mobile="hidden-mobile",
                 **typo(size=14, weight=800, lh=1.2))

    right = container([nav, cta], content_width="full", flex_direction="row",
                      flex_align_items="center", flex_justify_content="flex-end",
                      flex_gap=gap(6), padding=box(0), _flex_size="grow")

    logo = widget("site-logo", site_logo_fallback="yes", custom_image=img(M.LOGO),
                  site_logo_size_size="medium_large", align="left", width=px(157),
                  width_mobile=px(128), space=px(100, "%"), link_to="default")

    pill = container([logo, right], seed="hdr-pill", content_width="full", flex_direction="row",
                     flex_wrap="nowrap", flex_align_items="center",
                     flex_justify_content="space-between", flex_gap=gap(20),
                     padding=box(8, 8, 8, 24), padding_mobile=box(8, 8, 8, 18),
                     background_background="classic", background_color="rgba(15,17,48,0.5)",
                     border_border="solid", border_width=box(1),
                     border_color="rgba(255,255,255,0.16)", border_radius=box(999),
                     css_classes="ch-header-pill")

    return mark_inner([container([pill], seed="hdr", content_width="boxed", boxed_width=px(1440),
                                 padding=box(18, 48, 18, 48), padding_tablet=box(16, 28, 16, 28),
                                 padding_mobile=box(12, 16, 12, 16), css_classes="ch-header")])


def link_list(items, color="#F4F2EC", size=15):
    return widget("icon-list", view="traditional", space_between=px(12),
                  icon_list=[{"_id": f"{abs(hash(l)) % 0xfffffff:07x}", "text": l,
                              "selected_icon": {"value": "", "library": ""},
                              "link": {"url": u, "is_external": "", "nofollow": ""}}
                             for l, u in items],
                  text_color=color, text_color_hover=GREEN,
                  **typo("icon_typography", size=size, weight=400, lh=1.4))


def footer():
    def col_(title, items):
        return container([
            widget("heading", title=title, header_size="div", title_color=GREEN,
                   **typo(size=12, weight=800, ls=1.9, transform="uppercase", lh=1.3)),
            link_list(items),
        ], content_width="full", flex_direction="column", flex_gap=gap(14), padding=box(0),
            width=px(17, "%"), width_tablet=px(30, "%"), width_mobile=px(100, "%"))

    svc = "/#services"
    brand = container([
        widget("image", image=img(M.LOGO), image_size="medium_large", width=px(180, "px"),
               align="start", link_to="custom", link={"url": "/", "is_external": "", "nofollow": ""}),
        widget("text-editor", editor="<p>Caledon, Nobleton, King City, Vaughan, Kleinburg, "
                                     "Woodbridge, Muskoka, Collingwood, Toronto and surrounding areas</p>",
               text_color="#9A9CB8", **typo(size=14, lh=1.6)),
    ], content_width="full", flex_direction="column", flex_gap=gap(16), padding=box(0),
        width=px(24, "%"), width_tablet=px(100, "%"), width_mobile=px(100, "%"))

    cols = container([
        brand,
        col_("Services", [("Backyard Putting Greens", svc), ("Golf Course Shaping", svc),
                          ("Armor Stone Walls", svc), ("Artificial Grass Installation", svc),
                          ("Synthetic Turf Installation", svc)]),
        col_("Pools", [("Fiberglass Pool Installation", svc),
                       ("Swimming Pool Installation Caledon ON", svc)]),
        col_("Menu", [("Home", "/"), ("Projects", "/#work"), ("Contact Us", "/#book")]),
        col_("Contact", [("(905) 866-4111", "tel:+19058664111"),
                         ("Monday-Friday, 7 a.m.-5 p.m.", "/#book")]),
    ], seed="ftr-cols", content_width="full", flex_direction="row", flex_wrap="wrap",
        flex_justify_content="space-between", flex_gap=gap(32, 40), padding=box(0))

    bottom = container([
        widget("copyright", shortcode="© [hfe_current_year] Cypress Hills Landscaping & Snow Removal Inc.",
               title_color="#9A9CB8", **typo("caption_typography", size=13, lh=1.5)),
        widget("icon-list", view="inline", space_between=px(20),
               icon_list=[{"_id": "a1b2c31", "text": "Instagram", "selected_icon": {"value": "", "library": ""},
                           "link": {"url": "https://www.instagram.com/cypresshills.landscaping/",
                                    "is_external": "on", "nofollow": ""}},
                          {"_id": "a1b2c32", "text": "Facebook", "selected_icon": {"value": "", "library": ""},
                           "link": {"url": "https://www.facebook.com/cypresshillslandscaping",
                                    "is_external": "on", "nofollow": ""}}],
               text_color="#9A9CB8", text_color_hover=WHITE, **typo("icon_typography", size=13, lh=1.5)),
    ], seed="ftr-bottom", content_width="full", flex_direction="row", flex_wrap="wrap",
        flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(16),
        padding=box(24, 0, 0, 0), border_border="solid", border_width=box(1, 0, 0, 0),
        border_color="#262A60")

    return mark_inner([container([cols, bottom], seed="ftr", content_width="boxed",
                                 boxed_width=px(1328), flex_direction="column", flex_gap=gap(56),
                                 padding=box(80, 56, 40, 56), padding_tablet=box(64, 32, 36, 32),
                                 padding_mobile=box(56, 20, 32, 20),
                                 background_background="classic", background_color=INK,
                                 css_classes="ch-footer", overflow="hidden")])


def form():
    def field(wtype, name, placeholder, required):
        s = dict(mf_input_label_status="", mf_input_label=placeholder.replace("Enter ", "").capitalize(),
                 mf_input_name=name, mf_input_placeholder=placeholder)
        if required:
            s.update(mf_input_required="yes", mf_input_validation_warning_message="This field is required.")
        return widget(wtype, **s)

    return mark_inner([container([
        field("mf-text", "name", "Enter Name", True),
        field("mf-telephone", "phone", "Enter your phone number", True),
        field("mf-email", "email", "Enter Email", False),
        field("mf-text", "subject", "Enter your subject", False),
        widget("mf-button", mf_btn_text="Send message", mf_btn_align="justify",
               _margin=box(6, 0, 0, 0)),
    ], seed="form", content_width="full", flex_direction="column", flex_gap=gap(14), padding=box(0))])


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    for name, tree in (("header", header()), ("footer", footer()), ("form", form())):
        with open(f"out/{name}.json", "w") as f:
            json.dump(tree, f, ensure_ascii=False)
        print(name, os.path.getsize(f"out/{name}.json"), check_clean(tree))
