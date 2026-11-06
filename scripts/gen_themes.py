#!/usr/bin/env python3
"""Generate the two TIA Portal-inspired VS Code themes from palettes."""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes")

# ---------------------------------------------------------------------------
# Palettes
# ---------------------------------------------------------------------------
LIGHT = dict(
    name="TIA Portal – Project View", type="light",
    # chrome
    frame="#E6E6E6",        # window frame / title bar
    chrome="#F0F0F0",       # menus, toolbars, inactive tabs
    header="#D7DBDD",       # "Project tree" / task-card header bars
    pane="#FFFFFF",         # tree & editor background
    border="#B9BEC1",
    text="#000000",
    textDim="#5A6266",
    petrol="#009999",       # Siemens petrol accent
    petrolDark="#00646E",
    petrolTint="#CCEBEB",   # selection
    petrolHover="#E5F4F4",
    online="#FF9900",       # TIA online-mode orange
    error="#E00000",
    warning="#E5A000",
    ok="#2E9E2E",
    lineHL="#F2F8F8",
    editorSel="#B4DCDC",
    # syntax
    kw="#0000FF", dtype="#0000FF", comment="#008000", string="#A31515",
    number="#B35A00", local="#00646E", glob="#000000", func="#7A3E9D",
    pragma="#808080", region="#0000FF", op="#000000",
)

DARK = dict(
    name="TIA Portal – Portal View", type="dark",
    frame="#14232A",
    chrome="#1A2B33",
    header="#22363F",
    pane="#1E3038",
    border="#30474F",
    text="#E4ECEE",
    textDim="#93A7AD",
    petrol="#00B3B3",
    petrolDark="#008C8C",
    petrolTint="#0B5A5E",
    petrolHover="#243F47",
    online="#FF9900",
    error="#FF5A5A",
    warning="#FFB84D",
    ok="#5CC85C",
    lineHL="#24383F",
    editorSel="#1F5E63",
    kw="#6CB2FF", dtype="#6CB2FF", comment="#7CC47F", string="#F0A27A",
    number="#F2C072", local="#4FD8CF", glob="#E4ECEE", func="#D29BF0",
    pragma="#8A9EA4", region="#6CB2FF", op="#C9D6D9",
)


def workbench(p):
    light = p["type"] == "light"
    fg_on_petrol = "#FFFFFF"
    return {
        # base
        "focusBorder": p["petrol"],
        "foreground": p["text"],
        "descriptionForeground": p["textDim"],
        "disabledForeground": p["textDim"] + "99",
        "errorForeground": p["error"],
        "icon.foreground": p["petrolDark"] if light else p["petrol"],
        "selection.background": p["editorSel"],
        "widget.border": p["border"],
        "widget.shadow": "#00000033" if light else "#00000080",
        "sash.hoverBorder": p["petrol"],
        "textLink.foreground": p["petrolDark"] if light else p["petrol"],
        "textLink.activeForeground": p["petrol"],

        # title bar (TIA window frame)
        "titleBar.activeBackground": p["frame"],
        "titleBar.activeForeground": p["text"],
        "titleBar.inactiveBackground": p["chrome"],
        "titleBar.inactiveForeground": p["textDim"],
        "titleBar.border": p["border"],
        "menubar.selectionBackground": p["petrolHover"],
        "menu.background": p["chrome"] if light else p["header"],
        "menu.foreground": p["text"],
        "menu.selectionBackground": p["petrolTint"],
        "menu.selectionForeground": p["text"],
        "menu.separatorBackground": p["border"],
        "menu.border": p["border"],
        "commandCenter.background": p["pane"] if light else p["chrome"],
        "commandCenter.border": p["border"],

        # activity bar (the vertical "Task cards" strip)
        "activityBar.background": p["header"],
        "activityBar.foreground": p["petrolDark"] if light else p["petrol"],
        "activityBar.inactiveForeground": p["textDim"],
        "activityBar.activeBorder": p["petrol"],
        "activityBar.activeBackground": p["pane"] if light else p["petrolHover"],
        "activityBar.border": p["border"],
        "activityBarBadge.background": p["petrol"],
        "activityBarBadge.foreground": fg_on_petrol,

        # side bar (Project tree)
        "sideBar.background": p["pane"] if light else p["chrome"],
        "sideBar.foreground": p["text"],
        "sideBar.border": p["border"],
        "sideBarTitle.foreground": p["text"],
        "sideBarSectionHeader.background": p["header"],
        "sideBarSectionHeader.foreground": p["text"],
        "sideBarSectionHeader.border": p["border"],

        # lists / trees
        "list.activeSelectionBackground": p["petrolTint"],
        "list.activeSelectionForeground": p["text"],
        "list.activeSelectionIconForeground": p["petrolDark"] if light else p["petrol"],
        "list.inactiveSelectionBackground": p["header"] if light else p["petrolHover"],
        "list.inactiveSelectionForeground": p["text"],
        "list.hoverBackground": p["petrolHover"],
        "list.focusOutline": p["petrol"],
        "list.focusAndSelectionOutline": p["petrol"],
        "list.highlightForeground": p["petrol"],
        "list.errorForeground": p["error"],
        "list.warningForeground": p["warning"],
        "tree.indentGuidesStroke": p["border"],

        # editor groups & tabs (TIA editor tabs)
        "editorGroupHeader.tabsBackground": p["chrome"],
        "editorGroupHeader.tabsBorder": p["border"],
        "editorGroup.border": p["border"],
        "tab.activeBackground": p["pane"],
        "tab.activeForeground": p["text"],
        "tab.activeBorderTop": p["petrol"],
        "tab.inactiveBackground": p["chrome"],
        "tab.inactiveForeground": p["textDim"],
        "tab.border": p["border"],
        "tab.hoverBackground": p["petrolHover"],
        "tab.unfocusedActiveBorderTop": p["border"],
        "tab.unfocusedActiveForeground": p["textDim"],
        "breadcrumb.background": p["pane"],
        "breadcrumb.foreground": p["textDim"],
        "breadcrumb.focusForeground": p["text"],

        # editor
        "editor.background": p["pane"],
        "editor.foreground": p["text"],
        "editorLineNumber.foreground": "#8C9599" if light else "#5E747B",
        "editorLineNumber.activeForeground": p["petrolDark"] if light else p["petrol"],
        "editor.lineHighlightBackground": p["lineHL"],
        "editor.lineHighlightBorder": p["lineHL"],
        "editor.selectionBackground": p["editorSel"],
        "editor.inactiveSelectionBackground": p["editorSel"] + "99",
        "editor.selectionHighlightBackground": p["petrolTint"] + "AA",
        "editor.wordHighlightBackground": p["petrolTint"] + "88",
        "editor.findMatchBackground": "#FFD24D" if light else "#8A6A00",
        "editor.findMatchHighlightBackground": "#FFE9A0AA" if light else "#5C4A1088",
        "editorCursor.foreground": p["text"],
        "editorWhitespace.foreground": p["border"],
        "editorIndentGuide.background1": "#E3E6E7" if light else "#2A3F46",
        "editorIndentGuide.activeBackground1": p["petrol"] + "80",
        "editorBracketMatch.background": p["petrolTint"],
        "editorBracketMatch.border": p["petrol"],
        "editorGutter.background": p["chrome"] if light else p["pane"],
        "editorRuler.foreground": p["border"],
        "editorError.foreground": p["error"],
        "editorWarning.foreground": p["warning"],
        "editorInfo.foreground": p["petrol"],
        "editorGutter.addedBackground": p["ok"],
        "editorGutter.modifiedBackground": p["petrol"],
        "editorGutter.deletedBackground": p["error"],
        "editorOverviewRuler.border": p["border"],
        "editorWidget.background": p["chrome"] if light else p["header"],
        "editorWidget.border": p["border"],
        "editorSuggestWidget.background": p["pane"] if light else p["header"],
        "editorSuggestWidget.border": p["border"],
        "editorSuggestWidget.selectedBackground": p["petrolTint"],
        "editorSuggestWidget.highlightForeground": p["petrol"],
        "editorHoverWidget.background": "#FFFFE1" if light else p["header"],  # classic Windows tooltip yellow
        "editorHoverWidget.border": p["border"],
        "peekView.border": p["petrol"],
        "peekViewTitle.background": p["header"],
        "peekViewEditor.background": p["lineHL"],
        "peekViewResult.background": p["chrome"],

        # panel (Inspector window: Properties | Info | Diagnostics)
        "panel.background": p["pane"] if light else p["chrome"],
        "panel.border": p["border"],
        "panelTitle.activeForeground": p["text"],
        "panelTitle.activeBorder": p["petrol"],
        "panelTitle.inactiveForeground": p["textDim"],
        "panelSectionHeader.background": p["header"],
        "terminal.background": p["pane"] if light else p["chrome"],
        "terminal.foreground": p["text"],
        "terminalCursor.foreground": p["text"],

        # status bar (TIA bottom strip; orange when "online" = debugging)
        "statusBar.background": p["header"],
        "statusBar.foreground": p["text"],
        "statusBar.border": p["border"],
        "statusBar.noFolderBackground": p["header"],
        "statusBar.debuggingBackground": p["online"],
        "statusBar.debuggingForeground": "#000000",
        "statusBar.debuggingBorder": p["online"],
        "statusBarItem.hoverBackground": p["petrolTint"],
        "statusBarItem.remoteBackground": p["petrol"],
        "statusBarItem.remoteForeground": fg_on_petrol,
        "statusBarItem.prominentBackground": p["petrol"],
        "statusBarItem.prominentForeground": fg_on_petrol,
        "statusBarItem.errorBackground": p["error"],
        "statusBarItem.warningBackground": p["warning"],
        "debugToolBar.background": p["chrome"],
        "debugToolBar.border": p["online"],
        "debugIcon.startForeground": p["ok"],
        "editor.stackFrameHighlightBackground": "#FFE0B2" if light else "#5A3D0A",
        "editor.focusedStackFrameHighlightBackground": "#FFD08A" if light else "#7A520C",

        # inputs & buttons
        "input.background": p["pane"] if light else p["frame"],
        "input.foreground": p["text"],
        "input.border": p["border"],
        "input.placeholderForeground": p["textDim"],
        "inputOption.activeBorder": p["petrol"],
        "inputOption.activeBackground": p["petrolTint"],
        "inputValidation.errorBorder": p["error"],
        "inputValidation.warningBorder": p["warning"],
        "dropdown.background": p["pane"] if light else p["frame"],
        "dropdown.border": p["border"],
        "checkbox.border": p["border"],
        "button.background": p["petrol"],
        "button.foreground": fg_on_petrol,
        "button.hoverBackground": p["petrolDark"],
        "button.secondaryBackground": p["header"],
        "button.secondaryForeground": p["text"],
        "button.secondaryHoverBackground": p["petrolTint"],
        "badge.background": p["petrol"],
        "badge.foreground": fg_on_petrol,
        "progressBar.background": p["petrol"],
        "scrollbarSlider.background": "#C1C7CA88" if light else "#4A626A88",
        "scrollbarSlider.hoverBackground": "#A8B0B4AA" if light else "#5C7880AA",
        "scrollbarSlider.activeBackground": p["petrol"] + "AA",

        # quick input / notifications
        "quickInput.background": p["chrome"] if light else p["header"],
        "quickInputList.focusBackground": p["petrolTint"],
        "quickInputList.focusForeground": p["text"],
        "pickerGroup.foreground": p["petrol"],
        "pickerGroup.border": p["border"],
        "notifications.background": p["chrome"] if light else p["header"],
        "notifications.border": p["border"],
        "notificationCenterHeader.background": p["header"],
        "notificationsInfoIcon.foreground": p["petrol"],
        "notificationsErrorIcon.foreground": p["error"],
        "notificationsWarningIcon.foreground": p["warning"],

        # git / misc
        "gitDecoration.modifiedResourceForeground": p["petrolDark"] if light else p["petrol"],
        "gitDecoration.untrackedResourceForeground": p["ok"],
        "gitDecoration.deletedResourceForeground": p["error"],
        "gitDecoration.ignoredResourceForeground": p["textDim"],
        "gitDecoration.conflictingResourceForeground": p["online"],
        "minimap.background": p["pane"],
        "welcomePage.tileBackground": p["chrome"],
        "walkThrough.embeddedEditorBackground": p["lineHL"],
        "keybindingLabel.background": p["header"],
        "keybindingLabel.border": p["border"],
    }


def tokens(p):
    def t(name, scope, fg, style=None):
        s = {"foreground": fg}
        if style:
            s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}

    return [
        t("Comments", ["comment", "punctuation.definition.comment"], p["comment"]),
        t("SCL pragmas / attributes", ["meta.attribute.scl", "meta.preprocessor", "comment.block.documentation"], p["pragma"]),
        t("Keywords", ["keyword", "keyword.control", "storage.modifier", "keyword.other"], p["kw"]),
        t("Declarations & block keywords", ["storage.type", "keyword.other.declaration.scl", "keyword.other.block.scl"], p["kw"]),
        t("Word operators", ["keyword.operator.word", "keyword.operator.logical.scl"], p["kw"]),
        t("Data types", ["storage.type.primitive", "support.type", "entity.name.type", "support.type.primitive.scl"], p["dtype"]),
        t("Regions", ["keyword.control.region.scl"], p["region"]),
        t("Symbol operators", ["keyword.operator", "punctuation"], p["op"]),
        t("Strings", ["string", "string.quoted"], p["string"]),
        t("Numbers & typed literals", ["constant.numeric", "constant.other.literal.scl"], p["number"]),
        t("Language constants", ["constant.language"], p["kw"]),
        t("Local tags (#Name)", ["variable.other.local.scl", "variable.parameter", "variable.other.readwrite"], p["local"]),
        t("Global tags (\"Name\")", ["variable.other.global.scl"], p["glob"]),
        t("Variables", ["variable", "meta.definition.variable"], p["text"]),
        t("Instructions / functions", ["entity.name.function", "support.function", "meta.function-call"], p["func"]),
        t("Classes / FB types", ["entity.name.class", "support.class", "entity.name.type.class"], p["func"]),
        t("Tags / markup", ["entity.name.tag"], p["kw"]),
        t("Attributes", ["entity.other.attribute-name"], p["local"]),
        t("Markup headings", ["markup.heading", "entity.name.section"], p["petrol"], "bold"),
        t("Markup bold", ["markup.bold"], p["text"], "bold"),
        t("Markup italic", ["markup.italic"], p["text"], "italic"),
        t("Markup links", ["markup.underline.link"], p["petrolDark"] if p["type"] == "light" else p["petrol"]),
        t("Invalid", ["invalid", "invalid.illegal"], p["error"]),
    ]


def semantic(p):
    return {
        "variable.local": p["local"],
        "parameter": p["local"],
        "function": p["func"],
        "method": p["func"],
        "type": p["dtype"],
        "class": p["func"],
        "keyword": p["kw"],
        "comment": p["comment"],
        "string": p["string"],
        "number": p["number"],
    }


for pal, fname in [(LIGHT, "tia-portal-project-view-color-theme.json"),
                   (DARK, "tia-portal-portal-view-color-theme.json")]:
    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": pal["name"],
        "type": pal["type"],
        "semanticHighlighting": True,
        "colors": workbench(pal),
        "tokenColors": tokens(pal),
        "semanticTokenColors": semantic(pal),
    }
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)
    print("wrote", fname, len(theme["colors"]), "colors")
