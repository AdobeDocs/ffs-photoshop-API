---
title: Create Composite — Complete V1 Migration Reference
description: Field-level V1 vs V2 comparison for documentCreate, documentOperations, renditionCreate, and smartObject
hideBreadcrumbNav: true
keywords:
  - create-composite
  - documentCreate
  - documentOperations
  - renditionCreate
  - smartObject
  - layer operations
  - migration reference
---

# Create Composite — Complete V1 Migration Reference

This page is the authoritative single-page reference for migrating from all four V1 Photoshop API
composite-family endpoints to `/v2/create-composite`. It consolidates field-level comparisons for
document creation, document operations, all layer types, and output formats.

For general concepts and context, see [Layer Operations Overview](layer-operations-overview.md).
For individual topic deep dives, use the specific guides listed in that overview.

## 1. V1 endpoint coverage

All four V1 endpoints (and the informal `smartObjectV2` variant) map to the single V2 endpoint:

| V1 Endpoint | V2 Endpoint | Purpose |
|---|---|---|
| `POST /pie/psdService/documentCreate` | `POST /v2/create-composite` | Create new blank PSD documents |
| `POST /pie/psdService/documentOperations` | `POST /v2/create-composite` | Document-level ops + layer manipulation |
| `POST /pie/psdService/renditionCreate` | `POST /v2/create-composite` | Export PSD to JPEG/PNG/PSD/TIFF |
| `POST /pie/psdService/smartObject` | `POST /v2/create-composite` | Smart object operations

## 2. Request envelope

### Input

| V1 | V2 | Notes |
|---|---|---|
| `inputs[].href` + `"storage": "external"` | `image.source.url` | Presigned URL |
| `inputs[].href` + `"storage": "acp"` | `image.source.url` | ACP presigned URL |
| `inputs[].href` + `"storage": "adobe"` | `image.source.creativeCloudPath` or `.creativeCloudFileId` | CC storage |
| `inputs[].href` + `"storage": "dropbox"` | `image.source.url` + `destination.storageType: "dropbox"` | On output side |
| `inputs[].href` + `"storage": "azure"` | `image.source.url` + `destination.storageType: "azure"` | On output side |
| `options.document.*` | `image.*` (top-level fields) | Document creation parameters |
| `options.layers[]` | `edits.layers[]` | Layer operations |
| `options.*` (doc-level ops) | `edits.document.*` | Crop, resize, trim |

### Output

| V1 | V2 | Notes |
|---|---|---|
| `outputs[].href` | `outputs[].destination.url` | |
| `outputs[].storage` | `outputs[].destination.storageType` (Azure/Dropbox only) | |
| `outputs[].type` | `outputs[].mediaType` | |

### V1 vs V2 envelope example

**V1 (`documentOperations`):**

```json
{
  "inputs": [{"href": "<SIGNED_GET_URL>", "storage": "external"}],
  "options": {
    "layers": [
      {
        "type": "textLayer",
        "name": "Title",
        "add": {"insertTop": true},
        "text": {"content": "Hello"}
      }
    ]
  },
  "outputs": [{"href": "<SIGNED_POST_URL>", "storage": "external", "type": "image/vnd.adobe.photoshop"}]
}
```

**V2 (`/v2/create-composite`):**

```json
{
  "image": {"source": {"url": "<SIGNED_GET_URL>"}},
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Title",
        "operation": {"type": "add", "placement": {"type": "top"}},
        "text": {"content": "Hello"}
      }
    ]
  },
  "outputs": [
    {"destination": {"url": "<SIGNED_POST_URL>"}, "mediaType": "image/vnd.adobe.photoshop"}
  ]
}
```

### Layer processing order

<InlineAlert variant="warning" slots="text"/>

**Breaking change:** Layer processing order is reversed between V1 and V2. **V1:** Layers processed **bottom-up** (last item in array processed first). **V2:** Layers processed **top-down** (first item in array processed first). In V2, if Layer B uses `placement.type: "above"` with `referenceLayer: {name: "Layer A"}`, then Layer A **must appear earlier** in the array than Layer B. This is the opposite of V1 where Layer A would have appeared later in the array.

## 3. Document creation parameters

`documentCreate` `options.document.*` → V2 `image.*` (top-level):

| V1 (`options.document.*`) | V2 (`image.*`) | Notes |
|---|---|---|
| `width` | `width` | 1–32000 px |
| `height` | `height` | 1–32000 px |
| `resolution` (number, e.g. `72`) | `resolution: {"unit": "density_unit", "value": 72}` | Breaking: number → object |
| `fill: "white"` | `fill: "white"` | Preserved string shortcut |
| `fill: "transparent"` | `fill: "transparent"` | Preserved string shortcut |
| `fill: "backgroundColor"` | `fill: "background_color"` | Breaking: spelling changed |
| `fill: "white"` (explicit color) | `fill: {"solidColor": {"rgb": {"red": 255, "green": 255, "blue": 255}}}` | V2 adds object form for custom colors |
| `mode: "greyscale"` | `mode: "grayscale"` | Breaking: spelling fixed |
| `mode: "rgb"` / `"cmyk"` / `"lab"` etc. | Same values | Unchanged |
| `depth: 8` | `depth: 8` | Unchanged (integer) |
| *(not in V1)* | `pixelScaleFactor` | New: number, min 0.1 |
| *(not in V1)* | `name` | New: string, max 255 chars |
| *(not in V1)* | `iccProfile: {"type": "standard", "name": "..."}` | New: standard ICC profiles only |

<InlineAlert variant="warning" slots="text"/>

**`fill` changed from string to object for custom colors.** V1 accepted `"white"` as a string shortcut; V2 still accepts `"white"` and `"transparent"` as string shortcuts, but solid colors must use the object form. Also note: V1 used `"backgroundColor"` — V2 uses `"background_color"`.

**V1 (string):**

```json
{ "fill": "white" }
```

**V2 (object form for custom RGB):**

```json
{ "fill": {"solidColor": {"rgb": {"red": 255, "green": 255, "blue": 255}}} }
```

## 4. Document-level operations

### Resize (`edits.document.imageSize`)

| V1 | V2 | Notes |
|---|---|---|
| `width`, `height` | `width`, `height` | Unchanged |
| `resolution` (number) | `resolution: {"unit": "density_unit", "value": N}` | Breaking: number → object |
| `constrainProportions` | `constrainProportions` | Unchanged |
| *(not in V1)* | `resample` | New: `nearest_neighbor`, `bilinear`, `bicubic`, `bicubic_smoother`, `bicubic_sharper` |
| *(not in V1)* | `scaleStyles` | New in V2 |
| *(not in V1)* | `rasterize` | New in V2 |

### Trim (`edits.document.trim`)

| V1 | V2 | Notes |
|---|---|---|
| `trimType: "transparent_pixels"` | `trimType: "transparent_pixels"` | Supported |
| Trim by color (any color mode) | **Not supported** | Missing feature in V2 |

<InlineAlert variant="warning" slots="text"/>

**Missing V2 features:** The following V1 document operations are not yet available in V2: **Canvas size adjustment** (V1 `canvasSize` is not yet supported), **Image rotation** (V1 image rotation is not yet supported), and **Trim by color** (V1 color-based trim modes are not supported in V2).

## 5. Layer operation model

### Operation specification

**V1:** Separate sibling objects on each layer entry:

```json
{
  "type": "textLayer",
  "name": "My Layer",
  "add": {"insertTop": true},
  "text": {"content": "Hello"}
}
```

**V2:** Unified `operation` object:

```json
{
  "type": "text_layer",
  "name": "My Layer",
  "operation": {"type": "add", "placement": {"type": "top"}},
  "text": {"content": "Hello"}
}
```

### Placement type mapping

| V1 (`add.*`) | V2 (`operation.placement`) |
|---|---|
| `insertTop: true` | `{type: "top"}` |
| `insertBottom: true` | `{type: "bottom"}` |
| `insertAbove: {name: "LayerName"}` | `{type: "above", referenceLayer: {name: "LayerName"}}` |
| `insertAbove: {id: 123}` | `{type: "above", referenceLayer: {id: 123}}` |
| `insertBelow: {name: "LayerName"}` | `{type: "below", referenceLayer: {name: "LayerName"}}` |
| `insertBelow: {id: 123}` | `{type: "below", referenceLayer: {id: 123}}` |
| `insertInto: {name: "GroupName"}` | `{type: "into", referenceLayer: {name: "GroupName"}}` |

<InlineAlert variant="info" slots="text"/>

V1 used a field called `relativeTo` in some contexts. V2 uses `referenceLayer` — these are not the same field name. Update all relative placement references.

## 6. Common layer properties

### Lock / protection

| V1 | V2 | Notes |
|---|---|---|
| `locked: true` | `protection: ["all"]` | Breaking: boolean → array |
| `locked: false` | `protection: ["none"]` | |
| *(not in V1)* | `protection: ["transparency"]` | Granular, V2 only |
| *(not in V1)* | `protection: ["position"]` | V2 only |
| *(not in V1)* | `protection: ["composite"]` | V2 only |
| *(not in V1)* | `protection: ["artboard_autonest"]` | V2 only |

### Visibility

| V1 | V2 |
|---|---|
| `visible` | `isVisible` |

### Blend options

| V1 | V2 | Notes |
|---|---|---|
| `blendOptions.opacity` | `opacity` (top-level) | Breaking: de-nested |
| `blendOptions.blendMode` | `blendMode` (top-level) | Breaking: de-nested |

**Blend mode enum values** (all 29 — unchanged between V1 and V2):
`normal`, `dissolve`, `darken`, `multiply`, `color_burn`, `linear_burn`, `darker_color`,
`lighten`, `screen`, `color_dodge`, `linear_dodge`, `lighter_color`, `overlay`, `soft_light`,
`hard_light`, `vivid_light`, `linear_light`, `pin_light`, `hard_mix`, `difference`, `exclusion`,
`subtract`, `divide`, `hue`, `saturation`, `color`, `luminosity`, `pass_through`

### Pixel layer bounds / transform

| V1 | V2 | Notes |
|---|---|---|
| `bounds: {left, top, width, height}` | `transform: {offset: {horizontal, vertical}, dimension: {width, height}}` | Breaking |
| `bounds.left` | `transform.offset.horizontal` | |
| `bounds.top` | `transform.offset.vertical` | |
| `bounds.width` | `transform.dimension.width` | |
| `bounds.height` | `transform.dimension.height` | |

### Mask fields

| V1 | V2 | Notes |
|---|---|---|
| `mask.clip: true` | `isClipped: true` (top-level on layer) | Breaking: moved out of mask |
| `mask.linked` | `mask.isLinked` | Renamed |
| `mask.enabled` | `mask.isEnabled` | Renamed |
| `mask.input: {href, storage}` | `mask.source.url` | Breaking: restructured |

### fillToCanvas (missing feature)

<InlineAlert variant="warning" slots="text"/>

**`fillToCanvas` is not supported in V2.** This property, available on pixel and smart object layers in V1, has no equivalent in V2. If your V1 workflows rely on `fillToCanvas: true`, you must implement equivalent scaling/positioning logic using `transform` properties instead.

## 7. Per-layer-type reference

### 7a. Adjustment layers (`adjustmentLayer` → `adjustment_layer`)

**Type rename:** `"adjustmentLayer"` → `"adjustment_layer"`

<InlineAlert variant="warning" slots="text"/>

**`adjustments.type` is required in V2 but did not exist in V1.** In V1, the adjustment type was inferred from the key name (e.g., the presence of `brightnessContrast` identified the type). In V2, you must explicitly declare `adjustments.type` using the snake_case type name.

**V1:**
```json
{"adjustments": {"brightnessContrast": {"brightness": 25}}}
```

**V2:**
```json
{"adjustments": {"type": "brightness_contrast", "brightnessContrast": {"brightness": 25}}}
```

**Adjustment type name mapping:**

| V1 key name | V2 `adjustments.type` | Status |
|---|---|---|
| `brightnessContrast` | `brightness_contrast` | Breaking: renamed |
| `exposure` | `exposure` | Unchanged |
| `hueSaturation` | `hue_saturation` | Breaking: renamed |
| `colorBalance` | `color_balance` | Breaking: renamed |
| *(not in V1)* | `curves` | New in V2 |
| *(not in V1)* | `gradient_map_custom_stops` | New in V2 |
| *(not in V1)* | `levels` | New in V2 |

**Field changes within adjustment payloads:**

| Adjustment | V1 field | V2 field | Notes |
|---|---|---|---|
| Exposure | `exposure.exposure` | `exposure.exposureValue` | Breaking: renamed |
| Hue/Saturation | Master channel only | `localRange.channelId` for per-channel | New in V2 |

### 7b. Background layers

<InlineAlert variant="warning" slots="text"/>

**Background layers (`backgroundLayer`) cannot be created or edited in V2.** There is no `background_layer` type in the V2 create/edit layer type enum (used in `edits.layers`). If your V1 workflow creates or modifies the document background layer, you must use a regular pixel layer (`layer`) as a substitute. Manifest responses still return background layers with `type: "background_layer"`; see [Manifest Response Format](manifest-response-migration.md#background-layer).

### 7c. Solid color layers (`fillLayer` → `solid_color_layer`)

**Type rename:** `"fillLayer"` → `"solid_color_layer"`

| V1 | V2 |
|---|---|
| `fill.solidColor.rgb.red` | `fill.solidColor.rgb.red` |
| `fill.solidColor.rgb.green` | `fill.solidColor.rgb.green` |
| `fill.solidColor.rgb.blue` | `fill.solidColor.rgb.blue` |

The RGB field structure inside `solidColor` is unchanged between V1 and V2.

### 7d. Pixel layers (`layer` → `layer`)

**Type name:** Unchanged (`"layer"`)

Key changes for pixel layers:

- **Bounds:** V1 `bounds: {left, top, width, height}` → V2 `transform: {offset: {horizontal, vertical}, dimension: {width, height}}`
- **Mask:** `mask.input` → `mask.source.url`; `mask.linked` → `mask.isLinked`; `mask.enabled` → `mask.isEnabled`
- **Clipping:** `mask.clip: true` → `isClipped: true` (top-level)
- **fillToCanvas:** Not supported in V2

### 7e. Group layers (`layerSection` → `group_layer`)

**Type rename:** `"layerSection"` → `"group_layer"`

**Creating a new document with a group layer is not yet supported (upcoming feature).**
**Editing an existing document** to add a layer inside a group layer **is supported**: use `operation.placement.type: "into"` with `referenceLayer` pointing to the group (e.g. `"referenceLayer": { "name": "Group 1" }`). Editing existing group layers (name, visibility, protection, etc.) is also supported. V1 nested children under the layer's `children` array.

### 7f. Smart object layers (`smartObject` → `smart_object_layer`)

**Type rename:** `"smartObject"` → `"smart_object_layer"`

| V1 | V2 | Notes |
|---|---|---|
| `input: {href, storage}` | `smartObject.smartObjectFile.source: {url}` | Breaking: deeply nested |
| `smartObject.linked: true` | `smartObject.isLinked: true` | Renamed; resize with linked SOs now supported |
| *(not in V1)* | `transformMode: "none"/"custom"/"fit"/"fill"` | New in V2 |
| *(not in V1)* | `transform.angle`, `transform.skew` | New in V2 |
| *(not in V1)* | `transform.anchor` | New in V2 |
| *(not in V1)* | SVG file type | New in V2 |
| `fillToCanvas: true` | **Not supported** | Missing feature |

<InlineAlert variant="info" slots="text"/>

**Linked smart objects are supported in V2 with some restrictions.** See the [Smart Object Operations Migration](layer-operations-smart-objects.md) guide for usage details.

### 7g. Text layers (`textLayer` → `text_layer`)

**Type rename:** `"textLayer"` → `"text_layer"`

<InlineAlert variant="warning" slots="text"/>

**Character and paragraph style range semantics changed. This is an off-by-one breaking change.** In V1, `to` in a character or paragraph style range was interpreted as a **length** (not an end index). In V2, `apply.to` is an **inclusive end index** (0-based). The range field location also changed: V1 uses `from` and `to` directly on the array item, while V2 wraps them as `apply.from` and `apply.to`.

**Example:** To style the first 5 characters ("Hello" in "Hello World"):

V1: `{"from": 0, "to": 5, "fontName": "Arial-BoldMT"}` — `to: 5` means length 5

V2: `{"apply": {"from": 0, "to": 4}, "characterStyle": {"font": {"postScriptName": "Arial-BoldMT"}}}` — `to: 4` is the index of the last character

**Character style field mapping:**

| V1 | V2 | Notes |
|---|---|---|
| `from`, `to` (direct on item) | `apply.from`, `apply.to` | Breaking: wrapped + semantics changed |
| `fontName: "PostScriptName"` | `characterStyle.font.postScriptName` | Breaking: nested |
| `fontAvailable` | `characterStyle.font.isAvailable` | Breaking: renamed + nested |
| Direct properties at item level | All properties in `characterStyle: {...}` | Breaking: nested |
| `fontColor.rgb`, `.cmyk`, `.lab`, `.gray` | Same nested shape | Unchanged |
| *(not in V1)* | `characterStyle.capsOption` | New |
| *(not in V1)* | `characterStyle.fontAlpha` | New |
| *(not in V1)* | `characterStyle.letterSpacing` | New |
| *(not in V1)* | `characterStyle.lineHeight` | New |
| *(not in V1)* | `characterStyle.syntheticBold` | New |
| *(not in V1)* | `characterStyle.syntheticItalic` | New |

**Paragraph style field mapping:**

| V1 | V2 | Notes |
|---|---|---|
| `from`, `to` (direct on item) | `apply.from`, `apply.to` | Same off-by-one change as character styles |
| Direct properties at item level | All properties in `paragraphStyle: {...}` | Breaking: nested |
| `alignment` | `paragraphStyle.alignment` | Same values |
| *(not in V1)* | `paragraphStyle.endIndent` | New |
| *(not in V1)* | `paragraphStyle.firstLineIndent` | New |
| *(not in V1)* | `paragraphStyle.spaceAfter` | New |
| *(not in V1)* | `paragraphStyle.spaceBefore` | New |
| *(not in V1)* | `paragraphStyle.startIndent` | New |
| *(not in V1)* | `paragraphStyle.writingDirection` | New |

**Text frame:**

| V1 | V2 | Notes |
|---|---|---|
| Layer-level `bounds: {left, top, width, height}` | `text.frame: {type: "area", bounds: {top, left, right, bottom}}` | Breaking; convert: `right = left + width`, `bottom = top + height` |
| Only area frame supported | `text.frame.type: "point" or "area"` | V2 adds point frame |
| Default area at `(0, 0, 4, 4)` | Default point frame at canvas center | Breaking: behavior changes when frame is omitted |
| *(not in V1)* | `text.frame.type: "point"` with `origin: {x, y}` | New |

**Font options:**

| V1 | V2 | Notes |
|---|---|---|
| `options.fonts[]` — `href` + `storage` | `fontOptions.additionalFonts[]` — `source.url` | Breaking: renamed + restructured |
| `options.globalFont` | `fontOptions.defaultFontPostScriptName` | Breaking: renamed |
| `options.manageMissingFonts` | `fontOptions.missingFontStrategy` | Breaking: renamed |
| `"useDefault"` | `"use_default"` | Breaking: enum value changed |
| `"fail"` | `"fail"` | Unchanged |

## 8. Output format reference

### JPEG quality

| V1 value (numeric) | V2 value (string) |
|---|---|
| 1–2 | `"very_poor"` / `"poor"` / `"low"` |
| 3–4 | `"medium"` |
| 5–6 | `"high"` |
| 7 | `"maximum"` |
| *(not in V1)* | `"photoshop_max"` (recommended default for production) |

### PNG compression

| V1 value | V2 value |
|---|---|
| `"small"` | `"maximum"` |
| `"medium"` | `"medium"` |
| `"large"` | `"low"` |
| *(not in V1)* | `"none"`, `"very_low"`, `"medium_low"`, `"medium_high"`, `"default"`, `"high"`, `"very_high"` |

### TIFF

V1 accepted TIFF output via `renditionCreate`. TIFF is supported in V2 as an output format.

### Storage / destination mapping

| V1 (`outputs[].storage`) | V2 (`outputs[].destination`) |
|---|---|
| `"external"` + `href` | `{"url": "<presigned URL>"}` |
| `"acp"` + `href` | `{"url": "<ACP presigned URL>"}` |
| `"adobe"` + CC path | `{"creativeCloudPath": "folder/file.ext"}` (no leading slash) |
| `"adobe"` + URN | `{"creativeCloudFileId": "urn:aaid:..."}` |
| `"dropbox"` + `href` | `{"url": "...", "storageType": "dropbox"}` |
| `"azure"` + `href` | `{"url": "...", "storageType": "azure"}` |
| *(not in V1)* | `{"validityPeriod": N}` — hosted, Adobe-managed temporary storage |
| *(not in V1)* | `{"embedded": "string"/"json"/"base64"}` — inline in response |

### New output features in V2

| Feature | Notes |
|---|---|
| `iccProfile` on output | `{type: "standard", name: "..."}` or `{type: "custom", ...}` (CMYK supported via custom) |
| `cropMode: "bounds_of_layer"` | Single-layer export only — exports the bounding box of that layer |
| `layers` filter | Supported in both V1 and V2; controls which layers are rendered |
| Up to 25 outputs per request | vs. lower/unspecified V1 limit |

### Missing V2 features summary

| Feature | V1 | V2 |
|---|---|---|
| `fillToCanvas` (pixel/smart object layers) | Supported | Not supported |
| Linked smart objects | Supported | Supported |
| Canvas size adjustment | Supported | Coming soon |
| Image rotation | Supported | Coming soon |
| Trim by color | Supported | Not supported |
| Background layer create/edit | Supported | Not supported |
| TIFF output | Supported | Supported |

## See also

- [Layer Operations Overview](layer-operations-overview.md) — General V2 layer concepts and processing order
- [Text Layers](layer-operations-text.md) — Detailed text layer migration with examples
- [Adjustment Layers](layer-operations-adjustments.md) — All supported adjustment types
- [Smart Objects](layer-operations-smart-objects.md) — Smart object layer migration
- [Advanced Operations](layer-operations-advanced.md) — Masks, groups, blend modes, transforms
- [Document Creation](document-creation-migration.md) — Creating new blank documents
- [Document Operations](document-operations-migration.md) — Crop, resize, trim
- [Output Types](output-types-migration.md) — JPEG, PNG, TIFF output format details
