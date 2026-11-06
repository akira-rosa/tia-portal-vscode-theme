# Changelog

## 2.0.0

- One theme: **TIA Portal**. It follows TIA's Project View with the Portal View's navy navigation column, slate buttons and orange active marker mixed in.
- Gear watermark appears only when no editor is open, with no extra text, as in TIA Portal. Removed the gears from the side bar.
- CSS layer renamed to `css/tia-portal.css`; generator is now `scripts/gen_theme.py`.
- Previous themes moved to `archive/` and no longer ship in the extension.
- Release workflow now runs when a GitHub release is published.
- Archived v1.0 themes renamed: the light one is now **Portal View** and the dark one **Project View**.

## 1.1.0

- New **TIA Portal Classic – Project View** and **TIA Portal Classic – Portal View** themes, pixel-matched to TIA Portal V16/V19.
- Optional CSS layer (`css/tia-portal-classic.css`) for gradients, glossy title strips, raised tabs, TIA dialog frames, classic scrollbars and an original gear watermark.
- SCL grammar: `REGION` names are now scoped (`entity.name.section.region.scl`) so the whole region line can be colored like TIA.

## 1.0.0

- First release.
- **TIA Portal – Project View** (light) and **TIA Portal – Portal View** (dark petrol) color themes.
- SCL language support for `.scl` and `.udt` files: TIA-style highlighting of `#local` tags, `"global"` tags, typed literals (`T#2s`, `16#FF`), pragmas and regions.
- Status bar turns TIA "online" orange while debugging.
