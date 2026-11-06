#!/usr/bin/env python3
"""Generate the stylized "TIA Portal Classic" themes and their CSS layer.

Outputs
  themes/tia-portal-classic-project-view-color-theme.json
  themes/tia-portal-classic-portal-view-color-theme.json
  css/tia-portal-classic.css     (gradients, bevels, glossy title strips,
                                  gear watermark - needs a custom-CSS loader)

Colors were pixel-sampled from TIA Portal V16/V19 screenshots.
"""
import json, math, os, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# ---------------------------------------------------------------------------
# Sampled TIA palette
# ---------------------------------------------------------------------------
BLACK = "#1C1C1C"          # title strips, bottom "Portal view" bar
NAVY_DEEP = "#1B2030"      # group separators, portal nav column
NAVY = "#2D354D"           # active editor title bar
NAVY_EMPTY = "#3A435E"     # empty work area (gears)
SLATE = "#3C4561"          # portal panels / buttons
SLATE_DARK = "#282F47"     # portal bottom bar, pressed buttons
PERIWINKLE = "#8495BF"     # bullets, inactive icons
LINK = "#B7C5FF"           # portal link text
ORANGE = "#FF8000"         # active marker / online
CHROME = "#CCCCCC"         # menu & toolbar
HEADER = "#B2B2B2"         # "Project tree" / "Tasks" header bars
PANE = "#F0F0F0"           # tree background
PANE_ALT = "#E1E1E1"       # tree rows
BODY = "#EAEAEA"           # task card / inspector body
TAB_TOP = "#F3F3F3"        # raised tab gradient start
TAB_BOTTOM = "#D9D9D9"     # raised tab gradient end
EDGE = "#6C6C6C"           # header bottom edge
EDGE_LIGHT = "#8A8A8A"     # button / table borders
SEL = "#D9DEE3"            # tree selection
INFO_BLUE = "#5885B1"

SYNTAX = dict(kw="#0000FF", region="#C800FF", comment="#008000", text="#000000",
              pragma="#808080", lineNo="#646464")


def tokens():
    def t(name, scope, fg, style=None):
        s = {"foreground": fg}
        if style is not None:
            s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}
    k = SYNTAX
    return [
        t("Default text", ["source", "variable", "constant", "string", "entity.name.function",
                           "support.function", "meta.function-call", "variable.other.local.scl",
                           "variable.other.global.scl", "constant.numeric", "constant.other.literal.scl",
                           "keyword.operator", "punctuation"], k["text"], ""),
        t("Comments", ["comment", "punctuation.definition.comment"], k["comment"]),
        t("Pragmas / attributes", ["meta.attribute.scl", "meta.preprocessor"], k["pragma"]),
        t("Keywords", ["keyword", "keyword.control", "keyword.other", "storage", "storage.type",
                       "storage.modifier", "support.type", "keyword.operator.word",
                       "keyword.operator.logical.scl", "constant.language"], k["kw"]),
        t("Regions (TIA magenta)", ["keyword.control.region.scl", "entity.name.section.region.scl"], k["region"]),
        t("Types / classes", ["entity.name.type", "entity.name.class", "support.class"], k["text"]),
        t("Markup headings", ["markup.heading", "entity.name.section"], NAVY, "bold"),
        t("Markup links", ["markup.underline.link"], k["kw"]),
        t("Tags", ["entity.name.tag"], k["kw"]),
        t("Attributes", ["entity.other.attribute-name"], k["region"]),
        t("Invalid", ["invalid"], "#E00000"),
    ]


def common_editor():
    return {
        "editor.background": "#FFFFFF",
        "editor.foreground": "#000000",
        "editorLineNumber.foreground": SYNTAX["lineNo"],
        "editorLineNumber.activeForeground": "#000000",
        "editorGutter.background": "#FFFFFF",
        "editor.lineHighlightBackground": "#F2F5F8",
        "editor.lineHighlightBorder": "#E3E8EE",
        "editor.selectionBackground": "#ADD6FF",
        "editor.inactiveSelectionBackground": "#E5EBF1",
        "editor.selectionHighlightBackground": "#D9DEE3",
        "editor.wordHighlightBackground": "#D9DEE3",
        "editor.findMatchBackground": "#FFC27C",
        "editor.findMatchHighlightBackground": "#FFE6C799",
        "editorCursor.foreground": "#000000",
        "editorWhitespace.foreground": "#C3C3C3",
        "editorIndentGuide.background1": "#E6E6E6",
        "editorIndentGuide.activeBackground1": "#B2B2B2",
        "editorBracketMatch.background": "#D9DEE3",
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
        "editorSuggestWidget.highlightForeground": "#0000FF",
        "editorSuggestWidget.focusHighlightForeground": "#B7C5FF",
        "editorHoverWidget.background": "#FFFFE1",
        "editorHoverWidget.foreground": "#000000",
        "editorHoverWidget.border": "#767676",
        "editorStickyScroll.background": PANE,
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
        "editorStickyScroll.border": HEADER,
    }


def common_widgets():
    return {
        "focusBorder": "#00000000",
        "contrastBorder": "#00000000",
        "selection.background": "#ADD6FF",
        "errorForeground": "#E00000",
        "widget.shadow": "#00000040",
        "widget.border": EDGE_LIGHT,
        "textLink.foreground": "#0000FF",
        "textLink.activeForeground": "#0000CC",
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
        "menu.background": PANE,
        "menu.foreground": "#000000",
        "menu.selectionBackground": SEL,
        "menu.selectionForeground": "#000000",
        "menu.selectionBorder": EDGE_LIGHT,
        "menu.separatorBackground": HEADER,
        "menu.border": "#767676",
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
        "notificationLink.foreground": "#0000FF",
        "debugToolBar.background": CHROME,
        "debugToolBar.border": ORANGE,
        "statusBar.debuggingBackground": ORANGE,
        "statusBar.debuggingForeground": "#000000",
        "statusBar.debuggingBorder": ORANGE,
        "gitDecoration.modifiedResourceForeground": "#1F4FA0",
        "gitDecoration.untrackedResourceForeground": "#2E8B2E",
        "gitDecoration.deletedResourceForeground": "#C00000",
        "gitDecoration.ignoredResourceForeground": "#808080",
        "gitDecoration.conflictingResourceForeground": "#C05800",
        "terminal.background": "#FFFFFF",
        "terminal.foreground": "#000000",
        "terminalCursor.foreground": "#000000",
        "settings.headerForeground": "#000000",
        "settings.modifiedItemIndicator": ORANGE,
        "welcomePage.tileBackground": PANE,
        "walkThrough.embeddedEditorBackground": PANE,
    }


def project_view():
    c = {}
    c.update(common_widgets())
    c.update(common_editor())
    c.update({
        "foreground": "#000000",
        "descriptionForeground": "#4D4D4D",
        "disabledForeground": "#808080",
        "icon.foreground": "#2D354D",
        "sash.hoverBorder": NAVY_DEEP,

        "titleBar.activeBackground": BLACK,
        "titleBar.activeForeground": "#FFFFFF",
        "titleBar.inactiveBackground": "#585858",
        "titleBar.inactiveForeground": "#CCCCCC",
        "titleBar.border": BLACK,
        "menubar.selectionBackground": "#FFFFFF33",
        "menubar.selectionForeground": "#FFFFFF",
        "commandCenter.background": "#FFFFFF",
        "commandCenter.foreground": "#4D4D4D",
        "commandCenter.border": EDGE_LIGHT,
        "commandCenter.activeBackground": "#FFFFFF",

        # left vertical strip ("Start" / "PLC programming")
        "activityBar.background": HEADER,
        "activityBar.foreground": "#FFFFFF",
        "activityBar.inactiveForeground": "#FFFFFFB3",
        "activityBar.activeBorder": ORANGE,
        "activityBar.activeBackground": NAVY,
        "activityBar.border": "#737373",
        "activityBarBadge.background": ORANGE,
        "activityBarBadge.foreground": "#000000",

        # project tree
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
        "list.inactiveFocusOutline": "#B2B2B2",
        "list.highlightForeground": "#0000FF",
        "list.errorForeground": "#C00000",
        "list.warningForeground": "#A06000",
        "tree.indentGuidesStroke": "#B2B2B2",
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

        # inspector window
        "panel.background": BODY,
        "panel.border": NAVY_DEEP,
        "panelTitle.activeForeground": "#000000",
        "panelTitle.activeBorder": "#00000000",
        "panelTitle.inactiveForeground": "#333333",
        "panelSectionHeader.background": TAB_BOTTOM,
        "panelSectionHeader.foreground": "#000000",
        "panelInput.border": EDGE_LIGHT,

        # bottom "Portal view" bar
        "statusBar.background": BLACK,
        "statusBar.foreground": "#FFFFFF",
        "statusBar.border": BLACK,
        "statusBar.noFolderBackground": BLACK,
        "statusBar.noFolderForeground": "#FFFFFF",
        "statusBarItem.hoverBackground": "#FFFFFF26",
        "statusBarItem.activeBackground": "#FFFFFF40",
        "statusBarItem.remoteBackground": "#FFFFFF",
        "statusBarItem.remoteForeground": "#000000",
        "statusBarItem.remoteHoverBackground": "#E6E6E6",
        "statusBarItem.prominentBackground": ORANGE,
        "statusBarItem.prominentForeground": "#000000",
        "statusBarItem.errorBackground": "#C00000",
        "statusBarItem.warningBackground": "#C07000",
    })
    return c


def portal_view():
    c = {}
    c.update(common_widgets())
    c.update(common_editor())
    c.update({
        "foreground": "#000000",
        "descriptionForeground": "#3C4561",
        "disabledForeground": "#808080",
        "icon.foreground": SLATE,
        "sash.hoverBorder": ORANGE,
        "editor.background": "#F7F7F7",
        "editorGutter.background": "#F0F0F0",
        "editor.lineHighlightBackground": "#FFFFFF",
        "editor.lineHighlightBorder": "#E1E1E1",
        "minimap.background": "#F7F7F7",

        "titleBar.activeBackground": BLACK,
        "titleBar.activeForeground": "#FFFFFF",
        "titleBar.inactiveBackground": "#3A3A3A",
        "titleBar.inactiveForeground": "#B2B2B2",
        "titleBar.border": NAVY_DEEP,
        "menubar.selectionBackground": "#FFFFFF26",
        "menubar.selectionForeground": "#FFFFFF",
        "commandCenter.background": SLATE,
        "commandCenter.foreground": LINK,
        "commandCenter.border": SLATE_DARK,
        "commandCenter.activeBackground": "#4A5476",

        # navigation column (Start / Devices & networks / PLC programming...)
        "activityBar.background": NAVY_DEEP,
        "activityBar.foreground": "#FFFFFF",
        "activityBar.inactiveForeground": PERIWINKLE,
        "activityBar.activeBorder": ORANGE,
        "activityBar.activeBackground": SLATE,
        "activityBar.border": NAVY_DEEP,
        "activityBarBadge.background": ORANGE,
        "activityBarBadge.foreground": "#000000",

        # slate action panel
        "sideBar.background": SLATE,
        "sideBar.foreground": LINK,
        "sideBar.border": NAVY_DEEP,
        "sideBarTitle.background": NAVY_DEEP,
        "sideBarTitle.foreground": "#FFFFFF",
        "sideBarSectionHeader.background": SLATE_DARK,
        "sideBarSectionHeader.foreground": "#FFFFFF",
        "sideBarSectionHeader.border": NAVY_DEEP,
        "list.activeSelectionBackground": "#4E5A80",
        "list.activeSelectionForeground": "#FFFFFF",
        "list.activeSelectionIconForeground": "#FFFFFF",
        "list.inactiveSelectionBackground": "#47516F",
        "list.inactiveSelectionForeground": "#FFFFFF",
        "list.hoverBackground": "#8495BF33",
        "list.hoverForeground": "#FFFFFF",
        "list.focusOutline": "#00000000",
        "list.focusAndSelectionOutline": "#00000000",
        "list.highlightForeground": ORANGE,
        "list.errorForeground": "#FF8C8C",
        "list.warningForeground": "#FFC27C",
        "list.deemphasizedForeground": PERIWINKLE,
        "tree.indentGuidesStroke": "#5A6488",
        "tree.inactiveIndentGuidesStroke": "#4A5476",

        "editorGroup.border": NAVY_DEEP,
        "editorGroup.emptyBackground": SLATE,
        "editorGroup.dropBackground": "#FF800033",
        "editorGroupHeader.tabsBackground": SLATE_DARK,
        "editorGroupHeader.tabsBorder": NAVY_DEEP,
        "editorGroupHeader.noTabsBackground": SLATE,
        "tab.activeBackground": SLATE,
        "tab.activeForeground": "#FFFFFF",
        "tab.activeBorderTop": ORANGE,
        "tab.activeBorder": "#00000000",
        "tab.inactiveBackground": SLATE_DARK,
        "tab.inactiveForeground": PERIWINKLE,
        "tab.unfocusedActiveBackground": "#343C56",
        "tab.unfocusedActiveForeground": LINK,
        "tab.unfocusedActiveBorderTop": "#FF800080",
        "tab.unfocusedInactiveForeground": "#6E7DA3",
        "tab.hoverBackground": "#343C56",
        "tab.hoverForeground": "#FFFFFF",
        "tab.border": NAVY_DEEP,
        "tab.modifiedBorder": ORANGE,
        "breadcrumb.background": CHROME,
        "breadcrumb.foreground": "#333333",
        "breadcrumb.focusForeground": "#000000",
        "breadcrumb.activeSelectionForeground": "#000000",
        "breadcrumbPicker.background": PANE,

        "panel.background": CHROME,
        "panel.border": NAVY_DEEP,
        "panelTitle.activeForeground": "#000000",
        "panelTitle.activeBorder": ORANGE,
        "panelTitle.inactiveForeground": "#333333",
        "panelSectionHeader.background": TAB_BOTTOM,
        "panelSectionHeader.foreground": "#000000",
        "terminal.background": "#F7F7F7",

        "statusBar.background": SLATE_DARK,
        "statusBar.foreground": LINK,
        "statusBar.border": NAVY_DEEP,
        "statusBar.noFolderBackground": SLATE_DARK,
        "statusBar.noFolderForeground": LINK,
        "statusBarItem.hoverBackground": "#FFFFFF1A",
        "statusBarItem.activeBackground": "#FFFFFF33",
        "statusBarItem.remoteBackground": ORANGE,
        "statusBarItem.remoteForeground": "#000000",
        "statusBarItem.remoteHoverBackground": "#FF9933",
        "statusBarItem.prominentBackground": ORANGE,
        "statusBarItem.prominentForeground": "#000000",
        "statusBarItem.errorBackground": "#C00000",
        "statusBarItem.warningBackground": "#C07000",
    })
    return c


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
    # hole (drawn counter-clockwise for even-odd)
    d += f" M{cx + hole:.1f},{cy:.1f} A{hole},{hole} 0 1,0 {cx - hole:.1f},{cy:.1f} A{hole},{hole} 0 1,0 {cx + hole:.1f},{cy:.1f} Z"
    return d


def gears_svg(dark, light):
    gears = [(330, 250, 150, 122, 22, 62), (610, 175, 105, 86, 18, 44),
             (560, 455, 128, 104, 20, 52), (820, 330, 118, 96, 20, 48),
             (360, 560, 92, 75, 16, 38)]
    binary = []
    import random
    rnd = random.Random(7)
    for row in range(26):
        line = "".join(rnd.choice("01") for _ in range(70))
        binary.append(f'<text x="120" y="{150 + row * 17}">{line}</text>')
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">',
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>',
        f'<g font-family="Consolas,monospace" font-size="13" fill="{light}" opacity="0.10" letter-spacing="1">'
        + "".join(binary) + "</g>",
    ]
    for g in gears:
        d = gear_path(*g)
        parts.append(f'<path d="{d}" fill="url(#g)" fill-rule="evenodd" opacity="0.30" '
                     f'stroke="{light}" stroke-opacity="0.18" stroke-width="2"/>')
    parts.append("</svg>")
    return "".join(parts)


def data_uri(svg):
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg, safe=" =:/,;'().-")


def css():
    gears_project = data_uri(gears_svg("#2B334B", "#7C8BB5"))
    gears_portal = data_uri(gears_svg("#2E3650", "#8495BF"))
    PV = '[class*="tia-portal-classic-project-view"]'
    PO = '[class*="tia-portal-classic-portal-view"]'
    ANY = '[class*="tia-portal-classic-"]'
    return f"""/*
 * TIA Portal Classic - stylized layer for VS Code
 * https://github.com/akira-rosa/tia-portal-vscode-theme
 *
 * Adds what color themes cannot: gradients, bevels, glossy title strips,
 * raised tabs, dialog frames and the gear watermark. Every rule is scoped to
 * the two "TIA Portal Classic" themes, so switching theme turns it all off.
 * Load it with a custom-CSS extension (see README).
 * Generated by scripts/gen_classic.py - edit the script, not this file.
 */

/* ---------- shared tokens ---------------------------------------------- */
{ANY} {{
  --tia-black: {BLACK};
  --tia-gloss: linear-gradient(180deg, #8E8E8E 0px, #555555 7px, {BLACK} 8px, {BLACK} 100%);
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
{ANY}.monaco-workbench,
{ANY} .monaco-workbench .part {{
  font-family: var(--tia-font);
}}

/* ---------- title bar: glossy black strip ------------------------------- */
{ANY} .part.titlebar {{
  background: var(--tia-gloss) !important;
  border-bottom: 1px solid #000 !important;
}}
{ANY} .part.titlebar .window-title,
{ANY} .part.titlebar .menubar .menubar-menu-button {{
  color: #FFFFFF !important;
  font-weight: 600;
}}
{ANY} .part.titlebar .command-center .agent-status-badge,
{ANY} .part.titlebar .command-center-center {{
  border-radius: 0 !important;
}}
{ANY} .part.titlebar .command-center .action-item.command-center-center {{
  box-shadow: inset 1px 1px 0 #C3C3C3 !important;
}}

/* ---------- activity bar: TIA vertical strip ---------------------------- */
{PV} .part.activitybar {{
  background: linear-gradient(90deg, #BDBDBD 0%, {HEADER} 40%, #A8A8A8 100%) !important;
  box-shadow: inset -1px 0 0 #737373;
}}
{PO} .part.activitybar {{
  background: {NAVY_DEEP} !important;
}}
{ANY} .part.activitybar .action-item.checked {{
  box-shadow: inset 4px 0 0 {ORANGE};
}}
{ANY} .part.activitybar .action-item.checked .active-item-indicator::before {{
  border-left-width: 4px !important;
}}
{PO} .part.activitybar .action-item {{
  margin: 3px 4px;
  background: linear-gradient(180deg, #46506D 0%, {SLATE} 50%, #343C56 100%);
  border: 1px solid #282F47;
}}
{PO} .part.activitybar .action-item.checked {{
  background: linear-gradient(180deg, #4A5476 0%, {SLATE} 100%);
}}

/* ---------- side bar: "Project tree" ------------------------------------ */
{ANY} .part.sidebar > .composite.title,
{ANY} .part.auxiliarybar > .composite.title {{
  background: var(--tia-gray-bar) !important;
  border-bottom: 1px solid #8A8A8A;
}}
{PO} .part.sidebar > .composite.title,
{PO} .part.auxiliarybar > .composite.title {{
  background: linear-gradient(180deg, #252B3F 0%, {NAVY_DEEP} 100%) !important;
  border-bottom: 1px solid #000;
}}
{ANY} .part.sidebar > .composite.title h2,
{ANY} .part.auxiliarybar > .composite.title h2,
{ANY} .part.sidebar > .composite.title .title-label,
{ANY} .part.auxiliarybar > .composite.title .title-label {{
  color: #FFFFFF !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  text-shadow: 0 1px 0 rgba(0,0,0,.25);
}}

/* pane headers become TIA raised tabs ("Devices", "Details view") */
{ANY} .pane > .pane-header {{
  background: var(--tia-raised) !important;
  border-top: 1px solid #FFFFFF !important;
  border-bottom: 1px solid {EDGE} !important;
  color: #000000 !important;
  font-weight: 600;
}}
{ANY} .pane > .pane-header:hover {{
  background: var(--tia-raised-hover) !important;
}}
{ANY} .pane > .pane-header h3.title {{
  text-transform: none !important;
  font-size: 12.5px !important;
}}
{PO} .pane > .pane-header {{
  background: linear-gradient(180deg, #46506D 0%, {SLATE} 52%, #343C56 53%, {SLATE_DARK} 100%) !important;
  border-top: 1px solid #5A6488 !important;
  border-bottom: 1px solid {NAVY_DEEP} !important;
  color: #FFFFFF !important;
}}
{PO} .pane > .pane-header:hover {{
  background: linear-gradient(180deg, #505B7C 0%, #46506D 100%) !important;
}}

/* tree rows: TIA grid lines and dotted focus box */
{PV} .part.sidebar .monaco-list-row,
{PV} .part.auxiliarybar .monaco-list-row {{
  box-shadow: inset 0 -1px 0 #FFFFFF;
}}
{PV} .part.sidebar .monaco-list:not(.drop-target) .monaco-list-row.selected,
{PV} .part.auxiliarybar .monaco-list-row.selected {{
  outline: 1px dotted #000000 !important;
  outline-offset: -1px !important;
}}
{PO} .part.sidebar .monaco-list-row.selected {{
  box-shadow: inset 4px 0 0 {ORANGE};
}}
{PO} .part.sidebar .monaco-list-row:not(.selected):hover .label-name {{
  color: #FFFFFF;
}}
/* slate panel watermark */
{PO} .part.sidebar > .content {{
  background-image: url("{gears_portal}");
  background-repeat: no-repeat;
  background-position: -120px 102%;
  background-size: 640px auto;
}}

/* ---------- editor windows ---------------------------------------------- */
/* tab strip = TIA editor title bars */
{ANY} .editor-group-container > .title .tabs-container {{
  background: var(--tia-gray-bar) !important;
}}
{PO} .editor-group-container > .title .tabs-container {{
  background: linear-gradient(180deg, #343C56 0%, {SLATE_DARK} 100%) !important;
}}
{ANY} .editor-group-container > .title .tabs-container > .tab {{
  border-radius: 0 !important;
  font-weight: 600;
  box-shadow: inset 1px 0 0 rgba(255,255,255,.25);
}}
{PV} .editor-group-container > .title .tabs-container > .tab:not(.active) {{
  background: var(--tia-gray-bar) !important;
}}
{PV} .editor-group-container.active > .title .tabs-container > .tab.active {{
  background: var(--tia-navy-bar) !important;
  color: #FFFFFF !important;
}}
{PV} .editor-group-container:not(.active) > .title .tabs-container > .tab.active {{
  background: linear-gradient(180deg, #A5ACBE 0%, #8C93A6 100%) !important;
}}
{PO} .editor-group-container > .title .tabs-container > .tab.active {{
  background: linear-gradient(180deg, #4A5476 0%, {SLATE} 100%) !important;
}}
{ANY} .editor-group-container > .title .tabs-container > .tab .label-name {{
  text-shadow: 0 1px 0 rgba(0,0,0,.3);
}}
/* breadcrumbs = TIA editor toolbar */
{ANY} .editor-group-container > .title .breadcrumbs-control {{
  background: linear-gradient(180deg, {BODY} 0%, {CHROME} 100%) !important;
  border-bottom: 1px solid {HEADER};
}}
/* code margin: TIA region rail */
{ANY} .monaco-editor .margin {{
  box-shadow: inset 6px 0 0 #E1E1E1, inset 7px 0 0 #C3C3C3, inset -1px 0 0 #E1E1E1;
}}

/* empty work area: navy with gears */
{PV} .editor-group-container.empty,
{PV} .part.editor > .content .editor-group-container.empty {{
  background-color: {NAVY_EMPTY} !important;
  background-image: url("{gears_project}") !important;
  background-repeat: no-repeat !important;
  background-position: center 35% !important;
  background-size: min(1100px, 95%) auto !important;
}}
{PO} .editor-group-container.empty {{
  background-color: {SLATE} !important;
  background-image: url("{gears_portal}") !important;
  background-repeat: no-repeat !important;
  background-position: center 35% !important;
  background-size: min(1100px, 95%) auto !important;
}}
{ANY} .editor-group-container.empty .letterpress {{
  opacity: 0 !important;
}}
{ANY} .editor-group-watermark dl,
{ANY} .editor-group-watermark dt,
{ANY} .editor-group-watermark dd {{
  color: #C9D2EC !important;
}}

/* ---------- panel: inspector window ------------------------------------- */
{ANY} .part.panel > .composite.title,
{ANY} .part.panel > .title {{
  background: {HEADER} !important;
  border-bottom: 1px solid #737373;
}}
{PO} .part.panel > .composite.title,
{PO} .part.panel > .title {{
  background: {SLATE_DARK} !important;
  border-bottom: 1px solid {NAVY_DEEP};
}}
{ANY} .part.panel > .composite.title .composite-bar .action-item {{
  background: var(--tia-raised);
  border: 1px solid #8A8A8A;
  border-bottom: none;
  margin: 4px 1px 0 1px;
  padding: 0 10px !important;
}}
{ANY} .part.panel > .composite.title .composite-bar .action-item .action-label {{
  color: #000000 !important;
  text-transform: none !important;
  font-size: 13px !important;
  font-weight: 600;
}}
{ANY} .part.panel > .composite.title .composite-bar .action-item.checked {{
  background: linear-gradient(180deg, #FFFFFF 0%, {TAB_TOP} 50%, {BODY} 100%);
  margin-top: 2px;
  padding-bottom: 2px !important;
}}
{ANY} .part.panel > .composite.title .composite-bar .action-item.checked .active-item-indicator {{
  display: none;
}}

/* ---------- status bar: bottom "Portal view" bar ------------------------ */
{PV} .part.statusbar {{
  background: linear-gradient(180deg, #2A2A2A 0%, {BLACK} 40%, #0E0E0E 100%) !important;
}}
{PO} .part.statusbar {{
  background: linear-gradient(180deg, #313955 0%, {SLATE_DARK} 100%) !important;
}}
{PV} .part.statusbar .statusbar-item.remote-kind,
{PV} .part.statusbar #status\\.host {{
  background: linear-gradient(180deg, #FFFFFF 0%, #EDEDED 60%, #DCDCDC 100%) !important;
  color: #000000 !important;
  font-weight: 600;
  margin: 2px 6px 2px 4px;
  border: 1px solid #000;
}}
{ANY} .part.statusbar.debugging,
{ANY}.monaco-workbench.debugging .part.statusbar,
{ANY} .monaco-workbench.debugging .part.statusbar {{
  background: linear-gradient(180deg, #FFA040 0%, {ORANGE} 100%) !important;
}}

/* ---------- buttons, inputs, checkboxes --------------------------------- */
{ANY} .monaco-button,
{ANY} .monaco-text-button,
{ANY} .monaco-button-dropdown > .monaco-button {{
  background: var(--tia-button) !important;
  color: #000000 !important;
  border: 1px solid {EDGE_LIGHT} !important;
  border-radius: 0 !important;
  box-shadow: inset 1px 1px 0 #FFFFFF;
}}
{ANY} .monaco-button:hover,
{ANY} .monaco-text-button:hover {{
  background: var(--tia-button-hover) !important;
}}
{ANY} .monaco-button:active {{
  background: linear-gradient(180deg, #CECECE 0%, #E2E2E2 100%) !important;
}}
{ANY} .monaco-inputbox,
{ANY} .monaco-select-box,
{ANY} .monaco-custom-toggle.monaco-checkbox {{
  border-radius: 0 !important;
  box-shadow: inset 1px 1px 0 #D0D0D0;
}}

/* ---------- scrollbars: always-visible classic style -------------------- */
{ANY} .monaco-scrollable-element > .scrollbar.vertical {{
  background: linear-gradient(90deg, #E3E3E3 0%, #F2F2F2 100%);
  box-shadow: inset 1px 0 0 #D0D0D0;
}}
{ANY} .monaco-scrollable-element > .scrollbar.horizontal {{
  background: linear-gradient(180deg, #E3E3E3 0%, #F2F2F2 100%);
  box-shadow: inset 0 1px 0 #D0D0D0;
}}
{ANY} .monaco-scrollable-element > .scrollbar.vertical > .slider {{
  background: linear-gradient(90deg, #FFFFFF 0%, #E7E7E7 50%, #D8D8D8 100%) !important;
  border: 1px solid {EDGE_LIGHT};
  box-sizing: border-box;
}}
{ANY} .monaco-scrollable-element > .scrollbar.horizontal > .slider {{
  background: linear-gradient(180deg, #FFFFFF 0%, #E7E7E7 50%, #D8D8D8 100%) !important;
  border: 1px solid {EDGE_LIGHT};
  box-sizing: border-box;
}}
{ANY} .monaco-scrollable-element > .scrollbar.invisible.fade {{
  opacity: 1 !important;
  transition: none !important;
}}
{ANY} .monaco-scrollable-element > .scrollbar.invisible {{
  opacity: .85 !important;
}}
{PO} .part.sidebar .monaco-scrollable-element > .scrollbar {{
  background: transparent;
  box-shadow: none;
}}
{PO} .part.sidebar .monaco-scrollable-element > .scrollbar > .slider {{
  background: #5A6488 !important;
  border-color: #282F47;
}}

/* ---------- dialogs: TIA "Creating project..." frame -------------------- */
{ANY} .monaco-dialog-box {{
  background: {CHROME} !important;
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
  padding-top: 34px !important;
  position: relative;
  box-shadow: 0 6px 24px rgba(0,0,0,.45) !important;
}}
{ANY} .monaco-dialog-box::before {{
  content: "Visual Studio Code";
  position: absolute; left: 0; right: 0; top: 0; height: 28px;
  background: linear-gradient(180deg, #898989 0px, #5A5A5A 11px, {BLACK} 12px, {BLACK} 100%);
  border-bottom: 1px solid #FFFFFF;
  color: #FFFFFF; font: 600 15px var(--tia-font);
  padding: 4px 10px; box-sizing: border-box;
}}
{ANY} .monaco-dialog-box .dialog-buttons-row {{
  background: {HEADER};
  margin: 16px -20px -20px -20px !important;
  padding: 14px 20px !important;
  border-bottom: 8px solid {BLACK};
  box-shadow: 0 -1px 0 #A0A0A0;
}}

/* ---------- quick input & notifications --------------------------------- */
{ANY} .quick-input-widget {{
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
  box-shadow: 0 6px 24px rgba(0,0,0,.45) !important;
}}
{ANY} .quick-input-widget .quick-input-titlebar {{
  background: linear-gradient(180deg, #898989 0px, #5A5A5A 11px, {BLACK} 12px, {BLACK} 100%) !important;
  color: #FFFFFF !important;
  border-radius: 0 !important;
}}
{ANY} .quick-input-widget .quick-input-header {{
  border-bottom: 1px solid {HEADER};
}}
{ANY} .quick-input-list .monaco-list-row.focused {{
  background: var(--tia-navy-bar) !important;
}}
{ANY} .notifications-toasts .notification-toast,
{ANY} .notifications-center {{
  border: 2px solid #FFFFFF !important;
  outline: 1px solid {BLACK};
  border-radius: 0 !important;
}}
{ANY} .notifications-center .notifications-center-header {{
  background: linear-gradient(180deg, #898989 0px, #5A5A5A 11px, {BLACK} 12px, {BLACK} 100%) !important;
  color: #FFFFFF !important;
}}

/* ---------- hovers: classic tooltip ------------------------------------- */
{ANY} .monaco-hover {{
  border-radius: 0 !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,.35) !important;
}}

/* ---------- suggest widget & editor widgets ----------------------------- */
{ANY} .monaco-editor .suggest-widget,
{ANY} .monaco-editor .find-widget {{
  border-radius: 0 !important;
}}
{ANY} .monaco-editor .find-widget {{
  background: var(--tia-raised) !important;
  border: 1px solid {EDGE_LIGHT};
}}

/* ---------- settings / welcome tables ----------------------------------- */
{ANY} .monaco-table-th,
{ANY} .monaco-workbench .settings-editor .settings-tabs-widget {{
  background: var(--tia-table-head) !important;
}}
"""


def write(theme_name, colors, fname):
    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": theme_name,
        "type": "light",
        "semanticHighlighting": False,
        "colors": colors,
        "tokenColors": tokens(),
    }
    with open(os.path.join(ROOT, "themes", fname), "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)
    print("wrote", fname, len(colors), "colors")


if __name__ == "__main__":
    write("TIA Portal Classic – Project View", project_view(),
          "tia-portal-classic-project-view-color-theme.json")
    write("TIA Portal Classic – Portal View", portal_view(),
          "tia-portal-classic-portal-view-color-theme.json")
    os.makedirs(os.path.join(ROOT, "css"), exist_ok=True)
    with open(os.path.join(ROOT, "css", "tia-portal-classic.css"), "w", encoding="utf-8") as f:
        f.write(css())
    print("wrote css/tia-portal-classic.css")
