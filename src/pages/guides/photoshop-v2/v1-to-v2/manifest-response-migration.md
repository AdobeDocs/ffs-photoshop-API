---
title: Manifest Response Format (V1 to V2)
description: Field-by-field changes in the /v2/generate-manifest response format
hideBreadcrumbNav: true
keywords:
  - manifest
  - response format
  - layer types
  - v1 to v2
  - migration
---

# Manifest Response Format (V1 to V2)

This guide covers every field-level change in the `/v2/generate-manifest` response. For request format migration (how to call the API), see the [Manifest Migration guide](manifest-migration.md).

## Overview

The V2 manifest response is significantly richer than V1. The changes fall into these categories:

| Section | What changed |
| ------- | ------------ |
| [Document-level fields](#document-level-fields) | Field renames + many new document properties |
| [Layer type taxonomy](#layer-type-taxonomy) | All type strings renamed to snake_case; artboards promoted to distinct type |
| [Per-layer common fields](#per-layer-common-fields) | `bounds` format, `blendOptions` extensions, `pixelMask` restructure, `thumbnail` object |
| [Adjustment layers](#adjustment-layers) | `adjustments.type` discriminant + per-type restructuring |
| [Background layer](#background-layer) | Type `background_layer`; new sub-fields; no `typeAttributes` |
| [Fill / solid color layer](#fill--solid-color-layer) | Type rename + vector mask exposure |
| [Artboard structure](#artboard-structure) | Promoted from `layerSection`, new `typeAttributes`, `layers[]` vs `children[]` |
| [Smart object detail](#smart-object-detail) | Heavily restructured nested fields |
| [Text layer detail](#text-layer-detail) | `characterStyles`, `paragraphAttributes` rename, enriched `frame` object |

<InlineAlert variant="warning" slots="text"/>

All layer `type` strings changed (e.g. `"adjustmentLayer"` → `"adjustment_layer"`). Any code that switches on `type` must be updated. See [Layer type taxonomy](#layer-type-taxonomy) for the full rename table.

## Document-level fields

**CHANGED** — The old manifest had a `document` sub-object with different field names. The new format has a richer top-level `document` object.

### Field renames

| Old field name     | New field name  | Notes                                           |
| ------------------ | --------------- | ----------------------------------------------- |
| `bitDepth`         | `depth`         | Renamed                                         |
| `iccProfileName`   | `iccProfile`    | Renamed                                         |
| `name`             | `title`         | Renamed                                         |
| `height` + `width` | `bounds`        | Replaced by `{left, top, right, bottom}` object |
| `photoshopBuild`   | —               | REMOVED                                         |

### New document fields

| Field                    | Type    | Example                      | Notes                                   |
| ------------------------ | ------- | ---------------------------- | --------------------------------------- |
| `bounds`                 | object  | `{left, top, right, bottom}` | Document canvas bounds                  |
| `imageMode`              | string  | `"rgb"`                      | Color mode                              |
| `depth`                  | number  | `8`                          | Bit depth per channel                   |
| `iccProfile`             | string  | `"sRGB IEC61966-2.1"`        | Embedded ICC profile name               |
| `xmp`                    | string  | (full XMP XML)               | Complete XMP metadata block             |
| `title`                  | string  | `"filename.psd"`             | Document filename                       |
| `globalLightingAngle`    | number  | —                            | Global light angle for layer effects    |
| `globalLightingAltitude` | number  | —                            | Global light altitude for layer effects |
| `layerFXVisible`         | boolean | —                            | Whether layer effects are visible       |
| `pixelScaleFactor`       | number  | —                            | HiDPI/retina scale factor               |
| `resolution`             | object  | `{value, unit}`              | Document resolution (e.g. 72 PPI)       |

## Layer type taxonomy

<InlineAlert variant="warning" slots="text"/>

All layer type strings changed in V2. Switch statements and `if/else` chains that compare `layer.type` must be updated.

**CHANGED** — Type names renamed to snake_case; artboards promoted to a distinct type.

| Old type string           | New type string      | Notes                                                      |
| ------------------------- | -------------------- | ---------------------------------------------------------- |
| `adjustmentLayer`         | `adjustment_layer`   | All adjustment layers (brightness, curves, levels, etc.)   |
| `backgroundLayer`         | `background_layer`   | Background layer (locked-by-default canvas base)           |
| `fillLayer`               | `solid_color_layer`  | Solid color fill layers                                    |
| `layer`                   | `layer`              | Generic rasterized pixel layers                            |
| `layerSection`            | `group_layer`        | Groups / folders                                           |
| `layerSection` (artboard) | `artboard`           | Artboards are now a distinct type (see [Artboard structure](#artboard-structure)) |
| `smartObject`             | `smart_object_layer` | Smart objects                                              |
| `textLayer`               | `text_layer`         | Text layers                                                |

In the old format, artboards were `layerSection` nodes indistinguishable from regular groups. The new format promotes artboards to `type: "artboard"` with dedicated `typeAttributes.artboard` data.

## Per-layer common fields

### `bounds` — CHANGED format

<InlineAlert variant="warning" slots="text"/>

The `bounds` object no longer uses `height`/`width`. Computed dimensions must now be derived from `right - left` and `bottom - top`.

Old format uses `{height, left, top, width}`:

```json
{ "height": 200, "left": 10, "top": 20, "width": 300 }
```

New format uses `{left, top, right, bottom}` (no `height`/`width`):

```json
{ "left": 10, "top": 20, "right": 310, "bottom": 220 }
```

### `thumbnail` — CHANGED (restructured)

<InlineAlert variant="warning" slots="text"/>

`thumbnail` is no longer a plain string URL. Code that treats it as a string will break.

Old format: plain string (pre-signed S3 URL):

```json
"thumbnail": "https://s3.amazonaws.com/..."
```

New format: object with media type and short-URL:

```json
"thumbnail": {
  "mediaType": "image/jpeg",
  "url": "https://photoshop-api.adobe.io/v2/short-url/urn:aaid:ps:..."
}
```

The thumbnail is optional — only present when the caller requests thumbnails. The URL is now a `/v2/short-url/` redirect rather than a direct S3 URL.

### Children nesting key — CHANGED

- **Old**: all nested layers use `children[]` at every level
- **New**: groups use `children[]`; artboards use `layers[]` for their children (see [Artboard structure](#artboard-structure))

### `blendOptions` — CHANGED (extended)

Old `blendOptions` only carried `{blendMode, opacity}`.

New `blendOptions` adds:

| New field                 | Type    | Notes                                             |
| ------------------------- | ------- | ------------------------------------------------- |
| `clipped`                 | boolean | Clipping mask state                               |
| `interior`                | boolean | Interior effects state                            |
| `fillOpacity`             | number  | Fill opacity (0–100), separate from layer opacity |
| `pixelMaskAsGlobalMask`   | boolean |                                                   |
| `vectorMaskAsGlobalMask`  | boolean |                                                   |
| `transparencyShapesLayer` | boolean |                                                   |
| `knockout`                | string  | e.g. `"none"`                                     |
| `channelRestrictions`     | array   | Per-channel blend restrictions                    |
| `blendRanges`             | array   | Blend-if ranges                                   |

### `pixelMask` — CHANGED (was `mask`)

Old format uses a `mask` field at the layer level:

```json
"mask": {
  "enabled": true,
  "linked": true,
  "offset": { "x": 0, "y": 0 },
  "type": "layer"
}
```

New format renames and restructures this as `pixelMask` (can be `null` or populated):

```json
"pixelMask": {
  "hasMask": true,
  "extendOpaque": true,
  "bounds": { "left": 0, "top": 0, "right": 2100, "bottom": 1500 },
  "enabled": true,
  "linked": true,
  "offset": { "horizontal": 0, "vertical": 0 }
}
```

| Change                                                              | Notes                                        |
| ------------------------------------------------------------------- | -------------------------------------------- |
| `mask` → `pixelMask`                                                | Field renamed                                |
| `type: "layer"` removed                                             | Discriminant removed                         |
| `extendOpaque` (NEW)                                                | boolean — extend mask opacity                |
| `bounds` (NEW)                                                      | Mask bounds added `{left,top,right,bottom}`  |
| `offset.x` → `offset.horizontal`, `offset.y` → `offset.vertical`  | Key names changed                            |

### Fields removed in V2

| Field       | Type    | Replacement in V2                                     |
| ----------- | ------- | ----------------------------------------------------- |
| `locked`    | boolean | Replaced by `protection` array                        |
| `rotate`    | number  | Replaced by `rotation` (renamed)                      |
| `mask`      | object  | Replaced by `pixelMask` (see above)                   |
| `thumbnail` | string  | Replaced by `thumbnail` object `{mediaType, url}`     |

### New fields in V2 only

| Field                 | Type           | Notes                                                                                            |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `protection`          | array          | Replaces boolean `locked`; e.g. `["none"]`, `["position"]`, `["all"]`                            |
| `rotation`            | number         | Replaces `rotate` (renamed)                                                                      |
| `linked`              | array          | Linked layer references                                                                          |
| `userMask`            | object         | `{density, feather}` — user mask state                                                           |
| `vectorMask`          | object or null | `{hasMask, bounds}` — vector mask                                                                |
| `pixelMask`           | object or null | Restructured from old `mask` field                                                               |
| `proportionalScaling` | boolean        | Lock aspect ratio during transform                                                               |
| `effects`             | object         | Layer effects container                                                                          |
| `compositeFrame`      | object         | `{absolute: {l,t,r,b}, relative: {l,t,r,b}}` — canvas-space and parent-relative composite bounds |
| `referenceFrame`      | object         | `{left, top, right, bottom}` — untransformed layer content bounds                                |
| `compositeDimensions` | object         | `{left, top, right, bottom}` — enclosing artboard/document bounds                                |
| `layerSettings`       | object         | Rich settings block (enabled, FXRefPoint, layerSpecific, warp data for text layers)              |

## Adjustment layers

**Type rename**: `adjustmentLayer` → `adjustment_layer`

### `adjustments` block — CHANGED (restructured with type discriminant)

Old format uses a camelCase sub-object key per adjustment type:

```json
{ "adjustments": { "vibrance": { "saturation": -24, "vibrance": 15 } } }
{ "adjustments": { "brightnessContrast": { "brightness": 18, "contrast": 36 } } }
```

New format adds a `type` discriminant (snake_case) and restructures some sub-fields:

```json
{ "adjustments": { "type": "vibrance", "vibrance": 15, "saturation": -24 } }
{ "adjustments": { "type": "brightness_contrast", "brightnessContrast": { "brightness": 18, "contrast": 36 } } }
```

### Per-type change summary

| Type (old key / new `type`)         | Key change  | Field changes                                                                                                     |
| ----------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------- |
| `vibrance` / `vibrance`             | none        | Fields hoisted: `adjustments.vibrance.{saturation,vibrance}` → `adjustments.{vibrance,saturation}` (flat)        |
| `exposure` / `exposure`             | none        | `exposure` value renamed to `exposureValue`; all values now nested under `exposure` sub-object                    |
| `hueSaturation` / `hue_saturation`  | snake_case  | `channels[].channel` ("master") → `hueSaturationAdjustments[]`; per-channel ranges use new `localRange` fields   |
| `brightnessContrast` / `brightness_contrast` | snake_case  | Structure same; key renamed; V2 may add `center` and `useLegacy`                                       |
| `colorBalance` / `color_balance`    | snake_case  | Structure same; key renamed                                                                                       |
| `levels` / `levels`                 | none        | Fully new structure: `levels.adjustment[]` array with typed `levelsAdjustment` objects                            |
| — / `curves`                        | NEW in V2   | Only in new format; `adjustments[]` with `channel` and `curves[{horizontal,vertical}]`                           |
| — / `gradient_map_custom_stops`     | NEW in V2   | Rich gradient with `colorStops`, `transparencyStops`, `interpolation`                                            |

## Background layer

**Type rename**: `backgroundLayer` → `background_layer`

The background layer in the new format carries additional sub-fields not present in the old format. Background layer entries do not include `typeAttributes` (they match other layer types such as text, group, and adjustment).

| Field                          | Type    | Notes                                                                  |
| ------------------------------ | ------- | ---------------------------------------------------------------------- |
| `backgroundLayer`              | boolean | Top-level flag `true` — explicitly marks this as the background layer  |
| `background.canConvertToLayer` | boolean | `true` — indicates the background can be promoted to a regular layer   |

Example V2 background layer:

```json
{
  "type": "background_layer",
  "id": 1,
  "name": "Background",
  "backgroundLayer": true,
  "background": {
    "canConvertToLayer": true
  }
}
```

## Fill / solid color layer

**Type rename**: `fillLayer` → `solid_color_layer`

### `fill.solidColor.rgb` — unchanged

Both old and new use identical structure and value range (8-bit, 0–255):

```json
{ "red": 255, "green": 0, "blue": 0 }
```

### Vector mask — NEW in V2

Old `fillLayer` had no vector mask information. New `solid_color_layer` exposes:

```json
{
  "vectorMask": {
    "hasMask": true,
    "bounds": { "left": 0, "top": 0, "right": 500, "bottom": 500 }
  }
}
```

`layerSettings.vectorMask` may also carry offset sub-data for the mask.

## Artboard structure

<InlineAlert variant="warning" slots="text"/>

Artboard children are under `layers[]` in V2, not `children[]`. Recursive traversal code must handle both keys.

### Old format — no distinct artboard type

Artboards were plain `layerSection` nodes, indistinguishable from regular groups:

```json
{
  "type": "layerSection",
  "id": 1,
  "name": "iPhone 16 Pro – 1",
  "children": [ ... ]
}
```

### New format — distinct `artboard` type with rich metadata

```json
{
  "type": "artboard",
  "id": 1,
  "name": "iPhone 16 Pro – 1",
  "typeAttributes": {
    "artboard": {
      "type": "artboard",
      "artboardBackgroundType": 1,
      "artboardPresetName": "iPhone 16 Pro",
      "artboardRect": {
        "type": "classFloatRect",
        "left": 0,
        "top": 0,
        "right": 393,
        "bottom": 852
      },
      "color": {
        "type": "RGBColor",
        "red": 255,
        "grain": 255,
        "blue": 255
      },
      "guideIDs": []
    },
    "layerSection": "layerSectionStart",
    "type": "layerSection"
  },
  "layers": [ ... ]
}
```

### New artboard-specific fields

| Field                                            | Notes                                                          |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `typeAttributes.artboard.artboardBackgroundType` | number — background type (0 = transparent, 1 = white, etc.)   |
| `typeAttributes.artboard.artboardPresetName`     | string — device preset name (e.g. `"iPhone 16 Pro"`)          |
| `typeAttributes.artboard.artboardRect`           | `{type, left, top, right, bottom}` — artboard geometry        |
| `typeAttributes.artboard.color`                  | `{type, red, grain, blue}` — background color                 |
| `typeAttributes.artboard.guideIDs`               | array — guide IDs associated with the artboard                |
| `typeAttributes.layerSection`                    | `"layerSectionStart"` — dual typing retained for compatibility |
| `typeAttributes.type`                            | `"layerSection"` — inner discriminant                         |

### Children key difference

| Format           | Children key |
| ---------------- | ------------ |
| Old (all layers) | `children[]` |
| New (groups)     | `children[]` |
| New (artboards)  | `layers[]`   |

## Smart object detail

### Old `smartObject` block

```json
{
  "instanceId": "16da7404-...",
  "linked": false,
  "name": "foo.psd",
  "path": "foo.psd",
  "type": "image/vnd.adobe.photoshop"
}
```

### New smart object block (heavily restructured)

```json
{
  "isSmartObject": true,
  "isLinked": false,
  "isValid": true,
  "smartObjectData": {
    "type": "smartObject",
    "transform": [x0, y0, x1, y1, x2, y2, x3, y3],
    "fileInfo": {
      "name": "foo.psd",
      "path": "foo.psd",
      "fileType": "ps3",
      "linked": false
    }
  },
  "extracted": {
    "mediaType": "application/octet-stream",
    "url": "https://photoshop-api.adobe.io/v2/short-url/urn:..."
  }
}
```

`extracted` is only present for non-linked (embedded) smart objects. `ccLibrariesElement` inside `fileInfo` is only present for CC Library-linked assets.

### Field-by-field comparison

| Old field     | New field                           | Status  | Notes                                                          |
| ------------- | ----------------------------------- | ------- | -------------------------------------------------------------- |
| `instanceId`  | —                                   | REMOVED | Identity now inferred from `fileInfo`                          |
| `linked`      | `isLinked`                          | CHANGED | Renamed; promoted to top level                                 |
| `name`        | `smartObjectData.fileInfo.name`     | CHANGED | Moved into nested `fileInfo`                                   |
| `path`        | `smartObjectData.fileInfo.path`     | CHANGED | Moved into nested `fileInfo`                                   |
| `type` (MIME) | `smartObjectData.fileInfo.fileType` | CHANGED | MIME string replaced by short code (e.g. `"ps3"`, `"unknown"`) |
| —             | `isSmartObject`                     | NEW     | Explicit boolean flag                                          |
| —             | `isValid`                           | NEW     | Validity state                                                 |
| —             | `smartObjectData.transform`         | NEW     | 8-element quad `[x0,y0, x1,y1, x2,y2, x3,y3]`                |
| —             | `extracted.mediaType` + `.url`      | NEW     | Download URL for embedded smart object content                 |

## Text layer detail

### Character styles — CHANGED and NEW

Old `characterStyles` fields:

```json
{
  "fontAvailable": true,
  "fontColor": { "rgb": { "red": 0, "green": 0, "blue": 0 } },
  "fontName": "PostScriptName",
  "fontSize": 12,
  "orientation": "horizontal"
}
```

New `characterStyles` fields:

| Field                            | Status  | Notes                                                   |
| -------------------------------- | ------- | ------------------------------------------------------- |
| `font.postScriptName`            | CHANGED | Restructured: font info moved into nested `font` object |
| `font.isAvailable`               | CHANGED | Renamed from `fontAvailable`, now nested under `font`   |
| `fontSize`                       | same    | Now a float (more precision)                            |
| `fontColor.rgb.{red,green,blue}` | same    | value range [0–32768] — compatible                    |
| `fontAlpha`                      | NEW     | Float 0–1 — character alpha                             |
| `syntheticBold`                  | NEW     | boolean                                                 |
| `syntheticItalic`                | NEW     | boolean                                                 |
| `underline`                      | NEW     | boolean                                                 |
| `capsOption`                     | NEW     | string, e.g. `"normal_caps"`                            |
| `lineHeight`                     | NEW     | float                                                   |
| `letterSpacing`                  | NEW     | number                                                  |
| `position`                       | NEW     | `{from, to}` — character range this style applies to   |

`orientation` (old) is no longer a per-character-style field; it is now `textOrientation` at the text object level.

### Paragraph styles — CHANGED and NEW

Old array was `paragraphStyles`:

```json
[{ "alignment": "left" }]
```

New array is `paragraphAttributes` (renamed):

| Field              | Status | Notes                          |
| ------------------ | ------ | ------------------------------ |
| `alignment`        | same   | string                         |
| `writingDirection` | NEW    | e.g. `"left_to_right"`         |
| `firstLineIndent`  | NEW    | number                         |
| `startIndent`      | NEW    | number                         |
| `endIndent`        | NEW    | number                         |
| `spaceBefore`      | NEW    | number                         |
| `spaceAfter`       | NEW    | number                         |
| `position`         | NEW    | `{from, to}` — paragraph range |

### Text object top-level — CHANGED and NEW

| Field             | Status  | Notes                                                                   |
| ----------------- | ------- | ----------------------------------------------------------------------- |
| `content`         | same    | Text string                                                             |
| `textOrientation` | NEW     | e.g. `"horizontal"` — moved from per-character-style                    |
| `missingFonts`    | NEW     | Array of font names not available on the server                         |
| `antiAliasing`    | NEW     | e.g. `"crisp"`                                                          |
| `frame`           | CHANGED | Restructured from old `text.type` + `text.frameType` fields (see below) |

### Text frame — CHANGED

Old text frame fields:

```json
{
  "type": "area",
  "frameType": "inPath"
}
```

New `frame` object:

```json
{
  "type": "area",
  "bounds": { "top": 0, "left": 0, "bottom": 100, "right": 300 },
  "boundsRaw": { "left": 0, "top": 0, "right": 300, "bottom": 100 },
  "matrix": { "f_xx": 1, "f_xy": 0, "f_yx": 0, "f_yy": 1, "f_tx": 0, "f_ty": 0 },
  "baselineAlignment": { "flag": 0, "minimum": 0 }
}
```

| Sub-field           | Status  | Notes                                           |
| ------------------- | ------- | ----------------------------------------------- |
| `type`              | same    | e.g. `"area"`                                   |
| `frameType`         | REMOVED | Subsumed by richer `frame` object               |
| `bounds`            | NEW     | Absolute canvas bounds of the text box          |
| `boundsRaw`         | NEW     | Unscaled text box dimensions                    |
| `matrix`            | NEW     | 2D affine transform matrix                      |
| `baselineAlignment` | NEW     | `{flag, minimum}` baseline alignment parameters |

## Summary: new vs. changed

### Fully new fields (absent in V1)

- Document-level metadata: `bounds`, `imageMode`, `depth`, `iccProfile`, `xmp`, `title`, `resolution`, `globalLightingAngle`, `globalLightingAltitude`, `layerFXVisible`, `pixelScaleFactor`
- `protection` array (replaces `locked`)
- `userMask`, `vectorMask` per-layer; `pixelMask` (restructured from `mask`)
- `compositeFrame`, `referenceFrame`, `compositeDimensions` per-layer bounds
- `proportionalScaling`, `effects`, `layerSettings` block
- Extended `blendOptions` fields: `clipped`, `interior`, `fillOpacity`, `knockout`, `channelRestrictions`, `blendRanges`
- Text: `missingFonts`, `antiAliasing`, `textOrientation`, `frame.bounds`, `frame.boundsRaw`, `frame.matrix`, `frame.baselineAlignment`
- Text warp: `layerSettings.layerSpecific.textLayerSettings` block
- Character style: `fontAlpha`, `syntheticBold`, `syntheticItalic`, `underline`, `capsOption`, `lineHeight`, `letterSpacing`, `position`
- Paragraph: `writingDirection`, `firstLineIndent`, `startIndent`, `endIndent`, `spaceBefore`, `spaceAfter`, `position`
- Smart object: `isSmartObject`, `isValid`, `smartObjectData.transform`, `ccLibrariesElement`, `extracted`
- Artboard: `typeAttributes.artboard` block, `artboardPresetName`, `artboardRect`, background color, `guideIDs`
- Background layer: `backgroundLayer` flag, `background.canConvertToLayer` (no `typeAttributes`)
- Adjustment `adjustments.type` discriminant; new adjustment types: `curves`, `gradient_map_custom_stops`
- `version` top-level field

### Changed fields (present in both, different shape)

- Document field renames: `bitDepth`→`depth`, `iccProfileName`→`iccProfile`, `name`→`title`, `height`+`width`→`bounds`; `photoshopBuild` removed
- **Layer type names** (see [Layer type taxonomy](#layer-type-taxonomy))
- **`bounds` format**: `{height,left,top,width}` → `{left,top,right,bottom}`
- `locked` (boolean) → `protection` (array of strings)
- `rotate` → `rotation` (renamed)
- `mask` → `pixelMask` (restructured; `offset.{x,y}` → `offset.{horizontal,vertical}`; `extendOpaque` and `bounds` added)
- **`thumbnail`**: plain string URL → `{mediaType, url}` object
- **Artboard children key**: `children[]` → `layers[]`
- Text `font` restructured: `fontName`/`fontAvailable` → `font.postScriptName`/`font.isAvailable`
- Text paragraph array: `paragraphStyles` → `paragraphAttributes`
- Text frame: `{type, frameType}` → `frame` object with bounds + matrix
- Smart object: flat `{instanceId, linked, name, path, type}` → nested `{isLinked, isValid, smartObjectData: {fileInfo, transform}, extracted}`
- Smart object MIME string `type` → `fileType` short code (e.g. `"ps3"`)
- Adjustment `adjustments` block: per-type keys renamed to snake_case; `type` discriminant added; `vibrance` fields hoisted; `exposure` value renamed to `exposureValue`; `hueSaturation.channels[]` → `hueSaturationAdjustments[]`
