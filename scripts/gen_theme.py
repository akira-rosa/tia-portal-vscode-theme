#!/usr/bin/env python3
"""Generate the TIA Portal theme for VS Code and its CSS layer.

Outputs
  themes/tia-portal-color-theme.json   the color theme (flat colors)
  css/tia-portal.css                   gradients, bevels, glossy title strips,
                                       dialog frames, gear watermark
                                       (needs a custom-CSS loader, see README)

One theme that mirrors TIA Portal's Project View, with the Portal View's navy
navigation column and orange accents. Colors were pixel-sampled from TIA Portal
V16/V19 screenshots. Edit the palette here and re-run; don't edit the outputs.
"""
import json, math, os, random, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
THEME_FILE = "tia-portal-color-theme.json"

# ---------------------------------------------------------------------------
# Palette (sampled from TIA Portal)
# ---------------------------------------------------------------------------
BLACK = "#1C1C1C"          # title strips, bottom bar
NAVY_DEEP = "#1B2030"      # separators, navigation column
NAVY = "#2D354D"           # active editor title bar
NAVY_EMPTY = "#3A435E"     # empty work area (gears)
SLATE = "#3C4561"          # portal buttons
SLATE_DARK = "#282F47"
PERIWINKLE = "#8495BF"     # inactive nav icons
ORANGE = "#FF8000"         # active marker / online
CHROME = "#CCCCCC"         # menus, toolbars, dialog body
HEADER = "#B2B2B2"         # "Project tree" / "Tasks" header bars
PANE = "#F0F0F0"           # project tree
BODY = "#EAEAEA"           # task cards / inspector body
TAB_TOP = "#F3F3F3"        # raised tab gradient
TAB_BOTTOM = "#D9D9D9"
EDGE = "#6C6C6C"           # raised tab bottom edge
EDGE_LIGHT = "#8A8A8A"     # buttons, inputs
SEL = "#D9DEE3"            # tree selection
INFO_BLUE = "#5885B1"

# SCL editor colors - TIA keeps it minimal
KW = "#0000FF"
REGION = "#C800FF"
COMMENT = "#008000"
TEXT = "#000000"
PRAGMA = "#808080"
LINE_NO = "#646464"


def tokens():
    def t(name, scope, fg, style=None):
        s = {"foreground": fg}
        if style is not None:
            s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}
    return [
        t("Operands, numbers, literals, calls: plain black like TIA",
          ["source", "variable", "constant", "string", "entity.name.function", "support.function",
           "meta.function-call", "variable.other.local.scl", "variable.other.global.scl",
           "constant.numeric", "constant.other.literal.scl", "keyword.operator", "punctuation"], TEXT, ""),
        t("Comments", ["comment", "punctuation.definition.comment"], COMMENT),
        t("Pragmas / attribute lists", ["meta.attribute.scl", "meta.preprocessor"], PRAGMA),
        t("Keywords and data types", ["keyword", "keyword.control", "keyword.other", "storage", "storage.type",
                                      "storage.modifier", "support.type", "keyword.operator.word",
                                      "keyword.operator.logical.scl", "constant.language"], KW),
        t("REGION lines (magenta)", ["keyword.control.region.scl", "entity.name.section.region.scl"], REGION),
        t("Types / classes", ["entity.name.type", "entity.name.class", "support.class"], TEXT),
        t("Markup headings", ["markup.heading", "entity.name.section"], NAVY, "bold"),
        t("Markup links", ["markup.underline.link"], KW),
        t("Tags", ["entity.name.tag"], KW),
        t("Attributes", ["entity.other.attribute-name"], REGION),
        t("Invalid", ["invalid"], "#E00000"),
    ]


def colors():
    return {
        # base
        "foreground": "#000000",
        "descriptionForeground": "#4D4D4D",
        "disabledForeground": "#808080",
        "errorForeground": "#E00000",
        "icon.foreground": NAVY,
        "focusBorder": "#00000000",
        "contrastBorder": "#00000000",
        "selection.background": "#ADD6FF",
        "widget.shadow": "#00000040",
        "widget.border": EDGE_LIGHT,
        "sash.hoverBorder": ORANGE,
        "textLink.foreground": KW,
        "textLink.activeForeground": "#0000CC",

        # title bar: glossy black strip
        "titleBar.activeBackground": BLACK,
        "titleBar.activeForeground": "#FFFFFF",
        "titleBar.inactiveBackground": "#585858",
        "titleBar.inactiveForeground": CHROME,
        "titleBar.border": BLACK,
        "menubar.selectionBackground": "#FFFFFF33",
        "menubar.selectionForeground": "#FFFFFF",
        "menu.background": PANE,
        "menu.foreground": "#000000",
        "menu.selectionBackground": SEL,
        "menu.selectionForeground": "#000000",
        "menu.selectionBorder": EDGE_LIGHT,
        "menu.separatorBackground": HEADER,
        "menu.border": "#767676",
        "commandCenter.background": "#FFFFFF",
        "commandCenter.foreground": "#4D4D4D",
        "commandCenter.border": EDGE_LIGHT,
        "commandCenter.activeBackground": "#FFFFFF",

        # activity bar: Portal View navigation column
        "activityBar.background": NAVY_DEEP,
        "activityBar.foreground": "#FFFFFF",
        "activityBar.inactiveForeground": PERIWINKLE,
        "activityBar.activeBorder": ORANGE,
        "activityBar.activeBackground": SLATE,
        "activityBar.border": NAVY_DEEP,
        "activityBarBadge.background": ORANGE,
        "activityBarBadge.foreground": "#000000",

        # side bar: Project tree
        "sideBar.background": PANE,
        "sideBar.foreground": "#000000",
        "sideBar.border": NAVY_DEEP,
        "sideBarTitle.background": HEADER,
        "sideBarTitle.foreground": "#FFFFFF",
        "sideBarSectionHeader.background": TAB_BOTTOM,
        "sideBarSectionHeader.foreground": "#000000",
        "sideBarSectionHeader.border": EDGE,
        "list.activeSelectionBackground": SEL,
        "list.activeSelectionForeground": "#000000",
        "list.activeSelectionIconForeground": "#000000",
        "list.inactiveSelectionBackground": SEL,
        "list.inactiveSelectionForeground": "#000000",
        "list.hoverBackground": "#E6EAEE",
        "list.focusOutline": EDGE_LIGHT,
        "list.focusAndSelectionOutline": EDGE_LIGHT,
        "list.inactiveFocusOutline": HEADER,
        "list.highlightForeground": KW,
        "list.errorForeground": "#C00000",
        "list.warningForeground": "#A06000",
        "tree.indentGuidesStroke": HEADER,
        "tree.inactiveIndentGuidesStroke": "#D0D0D0",

        # editor windows
        "editorGroup.border": NAVY_DEEP,
        "editorGroup.emptyBackground": NAVY_EMPTY,
        "editorGroup.dropBackground": "#8495BF55",
        "editorGroupHeader.tabsBackground": HEADER,
        "editorGroupHeader.tabsBorder": "#737373",
        "editorGroupHeader.noTabsBackground": NAVY,
        "tab.activeBackground": NAVY,
        "tab.activeForeground": "#FFFFFF",
        "tab.activeBorderTop": "#00000000",
        "tab.activeBorder": "#00000000",
        "tab.inactiveBackground": HEADER,
        "tab.inactiveForeground": "#FFFFFF",
        "tab.unfocusedActiveBackground": "#8C93A6",
        "tab.unfocusedActiveForeground": "#FFFFFF",
        "tab.unfocusedInactiveForeground": "#FFFFFFCC",
        "tab.hoverBackground": "#9DA3B4",
        "tab.hoverForeground": "#FFFFFF",
        "tab.border": "#737373",
        "tab.modifiedBorder": ORANGE,
        "tab.activeModifiedBorder": ORANGE,
        "breadcrumb.background": CHROME,
        "breadcrumb.foreground": "#333333",
        "breadcrumb.focusForeground": "#000000",
        "breadcrumb.activeSelectionForeground": "#000000",
        "breadcrumbPicker.background": PANE,

        # editor
        "editor.background": "#FFFFFF",
        "editor.foreground": "#000000",
        "editorLineNumber.foreground": LINE_NO,
        "editorLineNumber.activeForeground": "#000000",
        "editorGutter.background": "#FFFFFF",
        "editor.lineHighlightBackground": "#F2F5F8",
        "editor.lineHighlightBorder": "#E3E8EE",
        "editor.selectionBackground": "#ADD6FF",
        "editor.inactiveSelectionBackground": "#E5EBF1",
        "editor.selectionHighlightBackground": SEL,
        "editor.wordHighlightBackground": SEL,
        "editor.findMatchBackground": "#FFC27C",
        "editor.findMatchHighlightBackground": "#FFE6C799",
        "editorCursor.foreground": "#000000",
        "editorWhitespace.foreground": "#C3C3C3",
        "editorIndentGuide.background1": "#E6E6E6",
        "editorIndentGuide.activeBackground1": HEADER,
        "editorBracketMatch.background": SEL,
        "editorBracketMatch.border": EDGE_LIGHT,
        "editorRuler.foreground": "#E1E1E1",
        "editorError.foreground": "#E00000",
        "editorWarning.foreground": "#E5A000",
        "editorInfo.foreground": INFO_BLUE,
        "editorGutter.addedBackground": "#3BA33B",
        "editorGutter.modifiedBackground": INFO_BLUE,
        "editorGutter.deletedBackground": "#E00000",
        "editorGutter.foldingControlForeground": "#808080",
        "editorOverviewRuler.border": HEADER,
        "editorWidget.background": BODY,
        "editorWidget.foreground": "#000000",
        "editorWidget.border": EDGE_LIGHT,
        "editorSuggestWidget.background": "#FFFFFF",
        "editorSuggestWidget.border": EDGE_LIGHT,
        "editorSuggestWidget.foreground": "#000000",
        "editorSuggestWidget.selectedBackground": NAVY,
        "editorSuggestWidget.selectedForeground": "#FFFFFF",
        "editorSuggestWidget.highlightForeground": KW,
        "editorSuggestWidget.focusHighlightForeground": "#B7C5FF",
        "editorHoverWidget.background": "#FFFFE1",
        "editorHoverWidget.foreground": "#000000",
        "editorHoverWidget.border": "#767676",
        "editorStickyScroll.background": PANE,
        "editorStickyScroll.border": HEADER,
        "editorStickyScrollHover.background": SEL,
        "peekView.border": NAVY,
        "peekViewTitle.background": HEADER,
        "peekViewTitleLabel.foreground": "#FFFFFF",
        "peekViewEditor.background": "#FAFAFA",
        "peekViewResult.background": PANE,
        "peekViewResult.selectionBackground": SEL,
        "editor.stackFrameHighlightBackground": "#FFE0B2",
        "editor.focusedStackFrameHighlightBackground": "#FFC27C",
        "minimap.background": "#FFFFFF",

        # panel: inspector window
        "panel.background": BODY,
        "panel.border": NAVY_DEEP,
        "panelTitle.activeForeground": "#000000",
        "panelTitle.activeBorder": "#00000000",
        "panelTitle.inactiveForeground": "#333333",
        "panelSectionHeader.background": TAB_BOTTOM,
        "panelSectionHeader.foreground": "#000000",
        "panelInput.border": EDGE_LIGHT,
        "terminal.background": "#FFFFFF",
        "terminal.foreground": "#000000",
        "terminalCursor.foreground": "#000000",

        # status bar: bottom "Portal view" bar
        "statusBar.background": BLACK,
        "statusBar.foreground": "#FFFFFF",
        "statusBar.border": BLACK,
        "statusBar.noFolderBackground": BLACK,
        "statusBar.noFolderForeground": "#FFFFFF",
        "statusBar.debuggingBackground": ORANGE,
        "statusBar.debuggingForeground": "#000000",
        "statusBar.debuggingBorder": ORANGE,
        "statusBarItem.hoverBackground": "#FFFFFF26",
        "statusBarItem.activeBackground": "#FFFFFF40",
        "statusBarItem.remoteBackground": "#FFFFFF",
        "statusBarItem.remoteForeground": "#000000",
        "statusBarItem.remoteHoverBackground": "#E6E6E6",
        "statusBarItem.prominentBackground": ORANGE,
        "statusBarItem.prominentForeground": "#000000",
        "statusBarItem.errorBackground": "#C00000",
        "statusBarItem.warningBackground": "#C07000",
        "debugToolBar.background": CHROME,
        "debugToolBar.border": ORANGE,

        # controls
        "button.background": "#E2E2E2",
        "button.foreground": "#000000",
        "button.hoverBackground": "#F4F4F4",
        "button.border": EDGE_LIGHT,
        "button.secondaryBackground": "#E2E2E2",
        "button.secondaryForeground": "#000000",
        "button.secondaryHoverBackground": "#F4F4F4",
        "button.separator": EDGE_LIGHT,
        "input.background": "#FFFFFF",
        "input.foreground": "#000000",
        "input.border": EDGE_LIGHT,
        "input.placeholderForeground": "#808080",
        "inputOption.activeBorder": NAVY,
        "inputOption.activeBackground": SEL,
        "inputValidation.errorBackground": "#FFE5E5",
        "inputValidation.errorBorder": "#E00000",
        "inputValidation.warningBorder": "#E5A000",
        "dropdown.background": "#FFFFFF",
        "dropdown.foreground": "#000000",
        "dropdown.border": EDGE_LIGHT,
        "dropdown.listBackground": "#FFFFFF",
        "checkbox.background": "#FFFFFF",
        "checkbox.border": EDGE_LIGHT,
        "checkbox.foreground": "#000000",
        "badge.background": ORANGE,
        "badge.foreground": "#000000",
        "progressBar.background": ORANGE,
        "scrollbar.shadow": "#00000000",
        "scrollbarSlider.background": "#C8C8C8",
        "scrollbarSlider.hoverBackground": "#B4B4B4",
        "scrollbarSlider.activeBackground": "#A0A0A0",

        # quick input, notifications (TIA dialog style)
        "quickInput.background": CHROME,
        "quickInput.foreground": "#000000",
        "quickInputTitle.background": BLACK,
        "quickInputList.focusBackground": NAVY,
        "quickInputList.focusForeground": "#FFFFFF",
        "quickInputList.focusIconForeground": "#FFFFFF",
        "pickerGroup.foreground": NAVY,
        "pickerGroup.border": HEADER,
        "keybindingLabel.background": "#FFFFFF",
        "keybindingLabel.foreground": "#000000",
        "keybindingLabel.border": EDGE_LIGHT,
        "keybindingLabel.bottomBorder": EDGE_LIGHT,
        "notifications.background": CHROME,
        "notifications.foreground": "#000000",
        "notifications.border": HEADER,
        "notificationCenterHeader.background": BLACK,
        "notificationCenterHeader.foreground": "#FFFFFF",
        "notificationToast.border": "#FFFFFF",
        "notificationsInfoIcon.foreground": INFO_BLUE,
        "notificationsWarningIcon.foreground": "#E5A000",
        "notificationsErrorIcon.foreground": "#E00000",
        "notificationLink.foreground": KW,

        # misc
        "gitDecoration.modifiedResourceForeground": "#1F4FA0",
        "gitDecoration.untrackedResourceForeground": "#2E8B2E",
        "gitDecoration.deletedResourceForeground": "#C00000",
        "gitDecoration.ignoredResourceForeground": "#808080",
        "gitDecoration.conflictingResourceForeground": "#C05800",
        "settings.headerForeground": "#000000",
        "settings.modifiedItemIndicator": ORANGE,
        "welcomePage.tileBackground": PANE,
        "walkThrough.embeddedEditorBackground": PANE,
    }


# ---------------------------------------------------------------------------
# Original gear watermark (drawn here, not traced from any artwork)
# ---------------------------------------------------------------------------
def gear_path(cx, cy, r_out, r_in, teeth, hole):
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step
        for frac, r in ((0.00, r_in), (0.12, r_out), (0.42, r_out), (0.54, r_in)):
            ang = a + frac * step
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    d += (f" M{cx + hole:.1f},{cy:.1f} A{hole},{hole} 0 1,0 {cx - hole:.1f},{cy:.1f}"
          f" A{hole},{hole} 0 1,0 {cx + hole:.1f},{cy:.1f} Z")
    return d


def gears_svg(dark="#2B334B", light="#7C8BB5"):
    gears = [(330, 250, 150, 122, 22, 62), (610, 175, 105, 86, 18, 44),
             (560, 455, 128, 104, 20, 52), (820, 330, 118, 96, 20, 48),
             (360, 560, 92, 75, 16, 38)]
    rnd = random.Random(7)
    binary = [f'<text x="120" y="{150 + row * 17}">' + "".join(rnd.choice("01") for _ in range(70)) + "</text>"
              for row in range(26)]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">',
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>',
        f'<g font-family="Consolas,monospace" font-size="13" fill="{light}" opacity="0.08" letter-spacing="1">'
        + "".join(binary) + "</g>",
    ]
    for g in gears:
        parts.append(f'<path d="{gear_path(*g)}" fill="url(#g)" fill-rule="evenodd" opacity="0.30" '
                     f'stroke="{light}" stroke-opacity="0.18" stroke-width="2"/>')
    parts.append("</svg>")
    return "".join(parts)


def data_uri(svg):
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg, safe=" =:/,;'().-")


def css():
    gears = data_uri(gears_svg())
    T = '[class*="themes-tia-portal-color-theme-json"]'   # active only with this theme
    return f"""/*
 * TIA Portal theme for VS Code - CSS layer
 * https://github.com/akira-rosa/tia-portal-vscode-theme
 *
 * Adds what color themes cannot: gradients, bevels, glossy title strips,
 * raised tabs, TIA dialog frames and the gear watermark in the empty work
 * area. Every rule is scoped to the "TIA Portal" theme, so switching to
 * another theme turns it all off. Load it with a custom-CSS extension.
 * Generated by scripts/gen_theme.py - edit the script, not this file.
 */

{T} {{
  --tia-gloss: linear-gradient(180deg, #8E8E8E 0px, #555555 7px, {BLACK} 8px, {BLACK} 100%);
  --tia-dialog-strip: linear-gradient(180deg, #898989 0px, #5A5A5A 11px, {BLACK} 12px, {BLACK} 100%);
  --tia-raised: linear-gradient(180deg, {TAB_TOP} 0%, #E6E6E6 52%, {TAB_BOTTOM} 53%, {TAB_BOTTOM} 100%);
  --tia-raised-hover: linear-gradient(180deg, #FFFFFF 0%, #F0F0F0 52%, #E4E4E4 53%, #E4E4E4 100%);
  --tia-table-head: linear-gradient(180deg, #F0F0F0 0%, #E3E3E3 35%, #D3D3D3 60%, #E6E6E6 85%, #F0F0F0 100%);
  --tia-button: linear-gradient(180deg, #FFFFFF 0%, #EDEDED 30%, #E2E2E2 50%, #CECECE 55%, #DEDEDE 80%, #E8E8E8 100%);
  --tia-button-hover: linear-gradient(180deg, #FFFFFF 0%, #F6F6F6 50%, #E8E8E8 55%, #F2F2F2 100%);
  --tia-navy-bar: linear-gradient(180deg, #46506D 0%, {NAVY} 45%, #252C40 100%);
  --tia-gray-bar: linear-gradient(180deg, #C4C4C4 0%, {HEADER} 50%, #A6A6A6 100%);
  --tia-font: "Siemens Sans", "Segoe UI", "Segoe UI Variable", system-ui, sans-serif;
}}

/* ---------- typography -------------------------------------------------- */
{T}.monaco-workbench,
{T} .monaco-workbench .part {{
  font-family: var(--tia-font);
}}

/* ---------- title bar: glossy black strip ------------------------------- */
{T} .part.titlebar {{
  background: var(--tia-gloss) !important;
  border-bottom: 1px solid #000 !important;
}}
{T} .part.titlebar .window-title,
{T} .part.titlebar .menubar .menubar-menu-button {{
  color: #FFFFFF !important;
  font-weight: 600;
}}
{T} .part.titlebar .command-center .action-item.command-center-center {{
  border-radius: 0 !important;
  box-shadow: inset 1px 1px 0 #C3C3C3 !important;
}}

/* ---------- activity bar: Portal View navigation column ----------------- */
{T} .part.activitybar {{
  background: {NAVY_DEEP} !important;
}}
{T} .part.activitybar .action-item {{
  margin: 3px 4px;
  background: linear-gradient(180deg, #46506D 0%, {SLATE} 50%, #343C56 100%);
  border: 1px solid {SLATE_DARK};
}}
{T} .part.activitybar .action-item.checked {{
  background: linear-gradient(180deg, #4A5476 0%, {SLATE} 100%);
  box-shadow: inset 4px 0 0 {ORANGE};
}}
{T} .part.activitybar .action-item.checked .active-item-indicator::before {{
  border-left-width: 4px !important;
}}

/* ---------- side bar & tasks: header bars ------------------------------- */
{T} .part.sidebar > .composite.title,
{T} .part.auxiliarybar > .composite.title {{
  background: var(--tia-gray-bar) !important;
  border-bottom: 1px solid {EDGE_LIGHT};
}}
{T} .part.sidebar > .composite.title h2,
{T} .part.auxiliarybar > .composite.title h2,
{T} .part.sidebar > .composite.title .title-label,
{T} .part.auxiliarybar > .composite.title .title-label {{
  color: #FFFFFF !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  text-shadow: 0 1px 0 rgba(0,0,0,.25);
}}
{T} .part.auxiliarybar {{
  background: {BODY} !important;
}}

/* pane headers = TIA raised tabs ("Devices", "Details view") */
{T} .pane > .pane-header {{
  background: var(--tia-raised) !important;
  border-top: 1px solid #FFFFFF !important;
  border-bottom: 1px solid {EDGE} !important;
  color: #000000 !important;
  font-weight: 600;
}}
{T} .pane > .pane-header:hover {{
  background: var(--tia-raised-hover) !important;
}}
{T} .pane > .pane-header h3.title {{
  text-transform: none !important;
  font-size: 12.5px !important;
}}

/* tree rows: TIA grid lines and dotted focus box */
{T} .part.sidebar .monaco-list-row,
{T} .part.auxiliarybar .monaco-list-row {{
  box-shadow: inset 0 -1px 0 #FFFFFF;
}}
{T} .monaco-list-row.selected {{
  outline: 1px dotted #000000 !important;
  outline-offset: -1px !important;
}}
{T} .quick-input-list .monaco-list-row.selected,
{T} .quick-input-list .monaco-list-row.focused {{
  outline: none !important;
}}

/* ---------- editor windows ---------------------------------------------- */
{T} .editor-group-container > .title .tabs-container {{
  background: var(--tia-gray-bar) !important;
}}
{T} .editor-group-container > .title .tabs-container > .tab {{
  border-radius: 0 !important;
  font-weight: 600;
  box-shadow: inset 1px 0 0 rgba(255,255,255,.25);
}}
{T} .editor-group-container > .title .tabs-container > .tab:not(.active) {{
  background: var(--tia-gray-bar) !important;
}}
{T} .editor-group-container.active > .title .tabs-container > .tab.active {{
  background: var(--tia-navy-bar) !important;
  color: #FFFFFF !important;
}}
{T} .editor-group-container:not(.active) > .title .tabs-container > .tab.active {{
  background: linear-gradient(180deg, #A5ACBE 0%, #8C93A6 100%) !important;
}}
{T} .editor-group-container > .title .tabs-container > .tab .label-name {{
  text-shadow: 0 1px 0 rgba(0,0,0,.3);
}}
{T} .editor-group-container > .title .breadcrumbs-control {{
  background: linear-gradient(180deg, {BODY} 0%, {CHROME} 100%) !important;
  border-bottom: 1px solid {HEADER};
}}
/* code margin: TIA region rail */
{T} .monaco-editor .margin {{
  box-shadow: inset 6px 0 0 #E1E1E1, inset 7px 0 0 #C3C3C3, inset -1px 0 0 #E1E1E1;
}}

/* ---------- empty work area: gears, nothing else (as in TIA) ------------ */
{T} .editor-group-container.empty {{
  background-color: {NAVY_EMPTY} !important;
  background-image: url("{gears}") !important;
  background-repeat: no-repeat !important;
  background-position: center 40% !important;
  background-size: min(1100px, 95%) auto !important;
}}
{T} .editor-group-container.empty .letterpress,
{T} .editor-group-container.empty .editor-group-watermark {{
  display: none !important;
}}

/* ---------- panel: inspector window ------------------------------------- */
{T} .part.panel > .composite.title,
{T} .part.panel > .title {{
  background: {HEADER} !important;
  border-bottom: 1px solid #737373;
}}
{T} .part.panel > .composite.title .composite-bar .action-item {{
  background: var(--tia-raised);
  border: 1px solid {EDGE_LIGHT};
  border-bottom: none;
  margin: 4px 1px 0 1px;
  padding: 0 10px !important;
}}
{T} .part.panel > .composite.title .composite-bar .action-item .action-label {{
  color: #000000 !important;
  text-transform: none !important;
  font-size: 13px !important;
  font-weight: 600;
}}
{T} .part.panel > .composite.title .composite-bar .action-item.checked {{
  background: linear-gradient(180deg, #FFFFFF 0%, {TAB_TOP} 50%, {BODY} 100%);
  margin-top: 2px;
  padding-bottom: 2px !important;
}}
{T} .part.panel > .composite.title .composite-bar .action-item.checked .active-item-indicator {{
  display: none;
}}

/* ---------- status bar: bottom "Portal view" bar ------------------------ */
{T} .part.statusbar {{
  background: linear-gradient(180deg, #2A2A2A 0%, {BLACK} 40%, #0E0E0E 100%) !important;
}}
{T} .part.statusbar .statusbar-item.remote-kind,
{T} .part.statusbar #status\\.host {{
  background: linear-gradient(180deg, #FFFFFF 0%, #EDEDED 60%, #DCDCDC 100%) !important;
  color: #000000 !important;
  font-weight: 600;
  margin: 2px 6px 2px 4px;
  border: 1px solid #000;
}}
{T} .part.statusbar.debugging,
{T}.monaco-workbench.debugging .part.statusbar,
{T} .monaco-workbench.debugging .part.statusbar {{
  background: linear-gradient(180deg, #FFA040 0%, {ORANGE} 100%) !important;
}}

/* ---------- buttons, inputs --------------------------------------------- */
{T} .monaco-button,
{T} .monaco-text-button,
{T} .monaco-button-dropdown > .monaco-button {{
  background: var(--tia-button) !important;
  color: #000000 !important;
  border: 1px solid {EDGE_LIGHT} !important;
  border-radius: 0 !important;
  box-shadow: inset 1px 1px 0 #FFFFFF;
}}
{T} .monaco-button:hover,
{T} .monaco-text-button:hover {{
  background: var(--tia-button-hover) !important;
}}
{T} .monaco-button:active {{
  background: linear-gradient(180deg, #CECECE 0%, #E2E2E2 100%) !important;
}}
{T} .monaco-inputbox,
{T} .monaco-select-box,
{T} .monaco-custom-toggle.monaco-checkbox {{
  border-radius: 0 !important;
  box-shadow: inset 1px 1px 0 #D0D0D0;
}}

/* ---------- scrollbars: always-visible classic style -------------------- */
{T} .monaco-scrollable-element > .scrollbar.vertical {{
  background: linear-gradient(90deg, #E3E3E3 0%, #F2F2F2 100%);
  box-shadow: inset 1px 0 0 #D0D0D0;
}}
{T} .monaco-scrollable-element > .scrollbar.horizontal {{
  background: linear-gradient(180deg, #E3E3E3 0%, #F2F2F2 100%);
  box-shadow: inset 0 1px 0 #D0D0D0;
}}
{T} .monaco-scrollable-element > .scrollbar.vertical > .slider {{
  background: linear-gradient(90deg, #FFFFFF 0%, #E7E7E7 50%, #D8D8D8 100%) !important;
  border: 1px solid {EDGE_LIGHT};
  box-sizing: border-box;
}}
{T} .monaco-scrollable-element > .scrollbar.horizontal > .slider {{
  background: linear-gradient(180deg, #FFFFFF 0%, #E7E7E7 50%, #D8D8D8 100%) !important;
  border: 1px solid {EDGE_LIGHT};
  box-sizing: border-box;
}}
{T} .monaco-scrollable-element > .scrollbar.invisible.fade {{
  opacity: 1 !important;
  transition: none !important;
}}
{T} .monaco-scrollable-element > .scrollbar.invisible {{
  opacity: .85 !important;
}}

/* ---------- dialogs: TIA dialog frame ----------------------------------- */
{T} .monaco-dialog-box {{
  background: {CHROME} !important;
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
  padding-top: 34px !important;
  position: relative;
  box-shadow: 0 6px 24px rgba(0,0,0,.45) !important;
}}
{T} .monaco-dialog-box::before {{
  content: "Visual Studio Code";
  position: absolute; left: 0; right: 0; top: 0; height: 28px;
  background: var(--tia-dialog-strip);
  border-bottom: 1px solid #FFFFFF;
  color: #FFFFFF; font: 600 15px var(--tia-font);
  padding: 4px 10px; box-sizing: border-box;
}}
{T} .monaco-dialog-box .dialog-buttons-row {{
  background: {HEADER};
  margin: 16px -20px -20px -20px !important;
  padding: 14px 20px !important;
  border-bottom: 8px solid {BLACK};
  box-shadow: 0 -1px 0 #A0A0A0;
}}

/* ---------- quick input & notifications --------------------------------- */
{T} .quick-input-widget {{
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
  box-shadow: 0 6px 24px rgba(0,0,0,.45) !important;
}}
{T} .quick-input-widget .quick-input-titlebar {{
  background: var(--tia-dialog-strip) !important;
  color: #FFFFFF !important;
  border-radius: 0 !important;
}}
{T} .quick-input-widget .quick-input-header {{
  border-bottom: 1px solid {HEADER};
}}
{T} .quick-input-list .monaco-list-row.focused {{
  background: var(--tia-navy-bar) !important;
}}
{T} .notifications-toasts .notification-toast,
{T} .notifications-center {{
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
}}
{T} .notifications-center .notifications-center-header {{
  background: var(--tia-dialog-strip) !important;
  color: #FFFFFF !important;
}}

/* ---------- hovers, editor widgets, tables ------------------------------ */
{T} .monaco-hover {{
  border-radius: 0 !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,.35) !important;
}}
{T} .monaco-editor .suggest-widget,
{T} .monaco-editor .find-widget {{
  border-radius: 0 !important;
}}
{T} .monaco-editor .find-widget {{
  background: var(--tia-raised) !important;
  border: 1px solid {EDGE_LIGHT};
}}
{T} .monaco-table-th {{
  background: var(--tia-table-head) !important;
}}
"""


if __name__ == "__main__":
    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": "TIA Portal",
        "type": "light",
        "semanticHighlighting": False,
        "colors": colors(),
        "tokenColors": tokens(),
    }
    with open(os.path.join(ROOT, "themes", THEME_FILE), "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)
    os.makedirs(os.path.join(ROOT, "css"), exist_ok=True)
    with open(os.path.join(ROOT, "css", "tia-portal.css"), "w", encoding="utf-8") as f:
        f.write(css())
    print("wrote themes/%s (%d colors) and css/tia-portal.css" % (THEME_FILE, len(theme["colors"])))
