---
title: LLM Migration Reference Guide
description: Comprehensive reference for AI assistants helping developers migrate from Adobe Photoshop API v1 to v2
hideBreadcrumbNav: true
keywords:
  - LLM
  - AI assistant
  - migration reference
  - v1 to v2
  - comprehensive guide
---

# Adobe Photoshop API v1 to v2 migration - LLM reference guide

**Purpose:** This document serves as a comprehensive reference for AI assistants (LLMs) helping developers migrate from Adobe Photoshop API v1 to v2. It consolidates patterns, examples, and troubleshooting guidance from all migration guides.

## Table of contents

1. [Quick reference and decision trees](#quick-reference-and-decision-trees)
2. [Core architectural changes](#core-architectural-changes)
3. [Migration patterns by operation type](#migration-patterns-by-operation-type)
4. [Storage solutions reference](#storage-solutions-reference)
5. [Output types migration](#output-types-migration)
6. [ICC profile support (V2 new feature)](#icc-profile-support-v2-new-feature)
7. [Common migration issues and solutions](#common-migration-issues-and-solutions)
8. [Code transformation examples](#code-transformation-examples)
9. [Validation checklist](#validation-checklist)
10. [LLM interaction guidelines](#llm-interaction-guidelines)

## Quick reference and decision trees

### Complete V1 to V2 endpoint mapping

| V1 Endpoint | V2 Endpoint | Category | Description |
|-------------|-------------|----------|-------------|
| `/lrService/autoTone` | `/v2/edit` | Edit Operations | Auto tone adjustment |
| `/lrService/autoStraighten` | `/v2/edit` | Edit Operations | Auto straighten image |
| `/lrService/presets` | `/v2/edit` | Edit Operations | Apply Lightroom presets |
| `/lrService/xmp` | `/v2/edit` | Edit Operations | Apply XMP metadata |
| `/lrService/edit` | `/v2/edit` | Edit Operations | Manual adjustments |
| `/pie/psdService/renditionCreate` | `/v2/create-composite` | Format Conversion | Convert PSD to other formats |
| `/pie/psdService/documentCreate` | `/v2/create-composite` | Document Creation | Create new blank documents |
| `/pie/psdService/documentOperations` | `/v2/create-composite` | Document/Layer Operations | Document-level operations and layer manipulation |
| `/pie/psdService/photoshopActions` | `/v2/execute-actions` | Actions | Execute .atn action files |
| `/pie/psdService/actionJSON` | `/v2/execute-actions` | Actions | Execute inline ActionJSON |
| `/pie/psdService/productCrop` | `/v2/execute-actions` | Actions | Product crop convenience API |
| `/pie/psdService/depthBlur` | Not yet supported (Neural Filters unavailable) | Actions | Depth blur convenience API |
| `/pie/psdService/splitView` | `/v2/execute-actions` | Actions | Split view convenience API |
| `/pie/psdService/sideBySide` | `/v2/execute-actions` | Actions | Side by side convenience API |
| `/pie/psdService/artboardCreate` | `/v2/create-artboard` | Artboards | Create artboards from images |
| `/pie/psdService/documentManifest` | `/v2/generate-manifest` | Manifest | Generate PSD manifest |
| `/pie/psdService/status/{jobId}` | `/v2/status/{jobId}` | Status | Check job status (Photoshop) |
| `/lrService/status/{jobId}` | `/v2/status/{jobId}` | Status | Check job status (Lightroom) |
| Sensei PSDC Engine | `/v2/create-composite` | Format Conversion | PSD/Cloud PSD conversion engine (engine retiring, not endpoint) |

### Decision tree for migration path selection

```
START: What are you trying to do?
│
├─ Apply image adjustments (autoTone, exposure, etc.)?
│  └─> Use /v2/edit endpoint
│     └─> Guide: Edit Operations Migration
│
├─ Convert PSD to JPEG/PNG/TIFF without edits?
│  └─> Use /v2/create-composite (no edits block)
│     └─> Guide: Format Conversion Migration
│
├─ Using sensei PSDC engine for PSD/Cloud PSD conversion?
│  └─> Use /v2/create-composite
│     └─> URNs map to creativeCloudFileId, paths to creativeCloudPath
│     └─> Guide: Format Conversion Migration (PSDC Engine section)
│
├─ Create a new blank document?
│  └─> Use /v2/create-composite with document params
│     └─> Guide: Document Creation Migration
│
├─ Resize/crop/trim existing document?
│  └─> Use /v2/create-composite with edits.document
│     └─> Guide: Document Operations Migration
│
├─ Add/edit/delete layers in a PSD?
│  └─> Use /v2/create-composite with edits.layers
│     ├─> Image layers? → Layer Operations: Image
│     ├─> Text layers? → Layer Operations: Text
│     ├─> Adjustment layers? → Layer Operations: Adjustments
│     ├─> Smart objects? → Layer Operations: Smart Objects
│     └─> Move/delete/masks? → Layer Operations: Advanced
│
├─ Execute Photoshop actions or scripts?
│  └─> Use /v2/execute-actions
│     └─> Guide: Actions Migration
│
├─ Create artboards from multiple images?
│  └─> Use /v2/create-artboard
│     └─> Guide: Artboard Migration
│
├─ Get PSD structure and layer information?
│  └─> Use /v2/generate-manifest
│     └─> Guide: Manifest Migration
│
└─ Check job status?
   └─> Use /v2/status/{jobId}
      └─> Guide: Status Migration
```

### Migration path by V1 endpoint

**If using Lightroom endpoints:**
- `/lrService/*` → All migrate to `/v2/edit`
- Combine multiple operations in single request

**If using PSD layer operations:**
- `/pie/psdService/documentOperations` → `/v2/create-composite` with `edits.layers`
- Check layer type for specific guide

**If using action endpoints:**
- All action endpoints → `/v2/execute-actions`
- Action files now published and customizable

**If using format conversion:**
- `/renditionCreate` → `/v2/create-composite` (no edits)
- Can generate multiple outputs in one request

**For a complete behavioral reference:**
- `v2-whats-new.md` — net new V2 capabilities (artboard metadata, smart object extraction, UXP scripts, hosted/embedded storage, ICC profiles, granular protection, scriptOutputPattern, multiple outputs)
- `v2-api-catalog.md` — per-endpoint behavioral comparison tables and a breaking changes checklist covering all endpoints

## Core architectural changes

### Breaking changes summary

#### 1. Base URL changes

| Environment | V1 Base URL | V2 Base URL |
|-------------|-------------|-------------|
| Production | `https://image.adobe.io` | `https://photoshop-api.adobe.io` |

**Action Required:** Update all base URL references in your code.

#### 2. Request structure changes

**V1 Pattern:**
```json
{
  "inputs": [
    {
      "href": "<URL>",
      "storage": "external"
    }
  ],
  "options": { ... },
  "outputs": [
    {
      "href": "<URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}
```

**V2 Pattern:**
```json
{
  "image": {
    "source": {
      "url": "<URL>"
    }
  },
  "edits": { ... },
  "outputs": [
    {
      "destination": {
        "url": "<URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}
```

**Key Changes:**
- `inputs[0].href` → `image.source.url`
- `options` → `edits`
- `outputs[].href` → `outputs[].destination.url`
- `outputs[].type` → `outputs[].mediaType`
- `storage` → `storageType` (and it's now optional for external URLs)

<InlineAlert variant="info" slots="text"/>

**Artboard exception:** The `/v2/create-artboard` endpoint uses `images` (plural) with a `source` object per image, not `image` (singular), because it accepts multiple input images.

#### 3. Storage type specification

**V1:** Required for all storage types
```json
{
  "storage": "external"
}
```

**V2:** Optional for external presigned URLs, required only for Azure and Dropbox
```json
{
  "destination": {
    "url": "<URL>",
    "storageType": "azure"  // Only for Azure/Dropbox
  }
}
```

**When to use `storageType` in V2:**
- **REQUIRED:** Azure Blob Storage → `"storageType": "azure"`
- **REQUIRED:** Dropbox → `"storageType": "dropbox"`
- **NOT REQUIRED:** AWS S3, Frame.io, Google Drive, standard HTTPS URLs

#### 4. Authentication (unchanged)

V2 uses the same OAuth Server-to-Server authentication as V1:
```shell
curl -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d 'scope=openid,AdobeID,read_organizations'
```

### New capabilities in V2

#### 1. Batch operations

**V1 Required Multiple Sequential Calls:**
```shell
# Call 1
POST /lrService/autoTone

# Call 2
POST /lrService/autoStraighten

# Call 3
POST /lrService/edit
```

**V2 Single Call:**
```json
{
  "edits": {
    "autoTone": true,
    "autoStraighten": {"enabled": true},
    "light": {"exposure": 0.5}
  }
}
```

#### 2. Four storage options

1. **External Storage** - Your presigned URLs (AWS S3, Azure, etc.)
2. **Creative Cloud Storage** - Direct CC integration
3. **Embedded Storage** - Inline response (text outputs only)
4. **Hosted Storage** - Adobe-managed temporary storage

#### 3. Published action files

V1 convenience APIs (productCrop, depthBlur, etc.) used hidden server-side actions. V2 publishes these ActionJSON definitions so you can:
- Examine exact action steps
- Customize for your needs
- Learn from Adobe's implementations
- Create variants

#### 4. Enhanced layer operations

V2 supports comprehensive layer manipulation:
- Add, edit, delete, move layers
- Adjustment layers (brightness, hue/saturation, exposure, color balance)
- Smart objects with transformations
- Resize (`width`/`maxWidth`) with linked smart objects
- Text layers with full styling
- Layer masks and groups (add, edit, delete pixel masks)
- Blend modes and opacity

#### 5. Better error handling

```json
{
  "status": "failed",
  "errorDetails": [
    {
      "errorCode": "400401",
      "message": "The value provided is not valid."
    },
    {
      "errorCode": "400420",
      "message": "Required fields missing on the API request."
    }
  ]
}
```

## Migration patterns by operation type

### A. Edit operations (Lightroom)

**V1 Endpoints Consolidated:**
- `/lrService/autoTone`
- `/lrService/autoStraighten`
- `/lrService/presets`
- `/lrService/xmp`
- `/lrService/edit`

**V2 Endpoint:** `/v2/edit`

**Pattern:** Multiple sequential V1 calls → Single V2 call

**V1 Approach (3 separate calls):**
```shell
# Step 1
curl -X POST https://image.adobe.io/lrService/autoTone \
  -d '{"inputs": {"href": "<URL>", "storage": "external"}}'

# Step 2
curl -X POST https://image.adobe.io/lrService/autoStraighten \
  -d '{"inputs": {"href": "<URL>", "storage": "external"}}'

# Step 3
curl -X POST https://image.adobe.io/lrService/edit \
  -d '{"inputs": {"href": "<URL>"}, "options": {"Exposure": 1.2}}'
```

**V2 Approach (single call):**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "edits": {
    "autoTone": true,
    "autoStraighten": {
      "enabled": true,
      "constrainCrop": true
    },
    "light": {
      "exposure": 1.2,
      "contrast": 10
    },
    "color": {
      "saturation": 15
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

**Adjustment Categories:**
- `autoTone` (boolean)
- `autoStraighten` (object with enabled, constrainCrop, uprightMode)
- `light` (exposure, contrast, highlights, shadows, whites, blacks)
- `color` (saturation, vibrance, whiteBalance)
- `effects` (clarity, dehaze, texture, vignette)
- `sharpen` (object with detail, radius, edgeMasking)
  - `detail`: integer 0-100 (amount of detail sharpening)
  - `radius`: number (radius of sharpening effect)
  - `edgeMasking`: integer 0-100 (masking to edges)
- `noiseReduction` (luminance, color)
- `presets` (array of preset sources)
- `xmp` (XMP source object with optional orientation and masks)

**Parameter Name Changes:**
- V1: PascalCase (`Exposure`, `Contrast`, `Sharpness`)
- V2: camelCase (`exposure`, `contrast`) within category objects
- V1 `Sharpness` (integer 0-100) → V2 `sharpen.detail` (integer 0-100)

### XMP with masks migration (localized adjustments)

For advanced Camera Raw editing workflows with localized adjustments, masks can be included alongside XMP metadata. These masks are binary files that define selection areas for localized adjustments and are passed as part of the `/lrService/xmp` endpoint in V1.

**V1 Approach (`/lrService/xmp`):**

```json
{
  "inputs": {
    "source": {
      "href": "<IMAGE_URL>",
      "storage": "external"
    }
  },
  "options": {
    "xmp": "<XMP_STRING>",
    "masks": [
      {
        "href": "<MASK_FILE_URL>",
        "storage": "external",
        "digest": "37B3568A954F0C80CA946DA0187FB9E2"
      }
    ]
  },
  "outputs": [...]
}
```

Note: In V1, masks were provided in `options.masks` alongside the XMP string at the `/lrService/xmp` endpoint.

**V2 Approach:**

```json
{
  "image": {
    "source": {
      "url": "<IMAGE_URL>"
    }
  },
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        }
      ]
    }
  },
  "outputs": [...]
}
```

**Key Changes:**
1. **Endpoint Change**: `/lrService/xmp` → `/v2/edit`
2. **Structure Change**: `options.masks` (sibling to xmp) → `edits.xmp.masks` (nested inside xmp)
3. **Mask Source**: `href` + `storage` → `source.url`
4. **XMP Format**: V1 accepted inline XMP string in `options.xmp`, V2 requires file reference in `edits.xmp.source`
5. **Digest**: Remains the same - fingerprint for mask identification
6. **Storage Parameter**: No longer required for standard URLs (only for Azure/Dropbox)

**Multiple Masks Example:**

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_1_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        },
        {
          "source": {
            "url": "<MASK_FILE_2_URL>"
          },
          "digest": "D15158972C7044869B171697AEBAFB0F"
        }
      ]
    }
  }
}
```

**Important Notes:**
- Masks are **optional** and only needed for advanced Camera Raw editing with localized adjustments
- Each mask requires both `source` (file reference) and `digest` (fingerprint/identifier)
- Mask files are typically binary `.bin` files generated by Adobe Camera Raw
- The `digest` is used to associate mask data with XMP adjustments
- Multiple masks can be provided for complex workflows

**Note on `/lrService/mask` endpoint:** The V1 `/lrService/mask` endpoint is a separate, unrelated feature for AI-based mask generation (selectSubject, selectSky, etc.) and has a different deprecation path. The masks discussed in this section are for localized Camera Raw adjustments passed via the `/lrService/xmp` endpoint.

### XMP with orientation override

V2 allows you to override the image's embedded orientation metadata by specifying an `orientation` parameter within the `xmp` object. This is useful for applying rotation or flip transformations as part of your Camera Raw workflow.

**V2 Structure:**

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "orientation": "right_top"
    }
  }
}
```

**Orientation Values (EXIF/TIFF Specification):**

| Value | Description | EXIF Code | Common Use |
|-------|-------------|-----------|------------|
| `"top_left"` | Column 0 = left, Row 0 = top | 1 | Normal orientation |
| `"top_right"` | Column 0 = right, Row 0 = top | 2 | Horizontal flip |
| `"bottom_right"` | Column 0 = right, Row 0 = bottom | 3 | 180° rotation |
| `"bottom_left"` | Column 0 = left, Row 0 = bottom | 4 | Vertical flip |
| `"left_top"` | Column 0 = top, Row 0 = left | 5 | 90° CCW + H-flip |
| `"right_top"` | Column 0 = top, Row 0 = right | 6 | 90° CW rotation |
| `"right_bottom"` | Column 0 = bottom, Row 0 = right | 7 | 90° CCW rotation |
| `"left_bottom"` | Column 0 = bottom, Row 0 = left | 8 | 90° CW + H-flip |

**Combined with Masks Example:**

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "orientation": "right_top",
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        }
      ]
    }
  }
}
```

**Key Points:**
- `orientation` is **optional** and only overrides embedded orientation when specified
- If not provided, the image's embedded EXIF orientation metadata is used
- Uses descriptive string values (e.g., `"right_top"`) instead of numeric EXIF codes
- Automatically handles width/height swaps for 90°/270° rotations (codes 5-8)
- Can be combined with masks and other XMP adjustments
- V1 did not support orientation override - this is a new V2 capability

### B. Composite operations (document/layer)

**V1 Endpoints Consolidated:**
- `/pie/psdService/renditionCreate` (format conversion)
- `/pie/psdService/documentCreate` (new documents)
- `/pie/psdService/documentOperations` (document and layer ops)

**V2 Endpoint:** `/v2/create-composite`

**Use Cases:**
1. **Format Conversion** - No `edits` block, just convert PSD to JPEG/PNG
2. **Document Creation** - `image` with dimensions, no `source`
3. **Document Operations** - `edits.document` with resize/crop/trim
4. **Layer Operations** - `edits.layers` with add/move/delete/edit

**Request Structure Pattern:**
```json
{
  "image": {
    "source": {"url": "<URL>"}  // For existing documents
    // OR
    "width": 1920,                // For new documents
    "height": 1080,
    "resolution": {"unit": "density_unit", "value": 72},  // Object format required
    "fill": "white",  // Also: "transparent", "background_color" (NOT "backgroundColor" — camelCase is rejected in V2)
                      // Or object: {"solidColor": {"red": 255, "green": 255, "blue": 255}}
    "mode": "rgb",    // Use "grayscale" (not "gray") for grayscale documents
    "depth": 8        // Integer, not string. Valid values depend on mode:
                      // bitmap: 1; grayscale/rgb/hsb: 8, 16, 32; cmyk/lab/multichannel: 8, 16; indexed/duotone: 8
  },
  "edits": {
    "document": {
      "resize": {...},
      "crop": {...},
      "trim": {...}
    },
    "layers": [
      {
        "type": "layer|text_layer|adjustment_layer|smart_object_layer|solid_color_layer",
        "name": "Layer Name",
        "operation": {
          "type": "add|edit|delete",
          "placement": {...}
        },
        // Layer-specific properties
      }
    ]
  },
  "outputs": [...]
}
```

**Layer Operation Types:**
- `"type": "add"` - Add new layer
- `"type": "edit"` - Edit existing layer properties (**required** — the `operation` field is mandatory for edit operations; it cannot be inferred)
- `"type": "delete"` - Remove layer
- `"type": "move"` - Move layer to a new position

<InlineAlert variant="info" slots="text"/>

**Layer lock:** Use `"protection": ["all"]` to lock, `"protection": ["none"]` to unlock (replaces V1 `"locked": true/false`). When using `all` or `none`, the array must contain only that element. Individual flags: `transparency`, `composite`, `position`, `artboard_autonest`. Clipping masks: use top-level `"isClipped": true` on a layer (not `mask.clip`).

**Layer Types:**
- `"layer"` - Image/pixel layers
- `"text_layer"` - Text layers
- `"adjustment_layer"` - Non-destructive adjustments
- `"smart_object_layer"` - Smart objects
- `"solid_color_layer"` - Solid color fill layers
- `"group_layer"` - Layer groups (V1 `"layerSection"` → V2 `"group_layer"`). **Creating a new document with a group layer is not yet supported (upcoming feature).** **Editing an existing document** to add a layer inside a group layer **is supported**: use placement `type: "into"` with `referenceLayer` (e.g. `"referenceLayer": { "name": "Group 1" }`).

**Placement Options:**
```json
{
  "placement": {
    "type": "top"  // or "bottom", "above", "below", "into"
    // For relative placement:
    "referenceLayer": {
      "name": "Layer Name"  // or "id": 123
    }
  }
}
```

<InlineAlert variant="warning" slots="text"/>

**Layer processing order (breaking change):** V1 processed layers bottom-up (last item in array first); V2 processes layers top-down (first item in array first). If a layer uses `above`, `below`, or `into` placement with a `referenceLayer`, the referenced layer must appear **earlier** in the array (already created/existing) before the layer that references it.

**Layer Property Locations (V2):**

| Property | V1 | V2 (most layer types) | V2 (`smart_object_layer`) |
|---|---|---|---|
| Opacity | `blendOptions.opacity` | top-level `opacity` | `blendOptions.opacity` |
| Blend mode | `blendOptions.blendMode` | top-level `blendMode` | `blendOptions.blendMode` |
| Visibility | `visible` | `isVisible` | `isVisible` |
| Lock | `locked: true/false` | `protection: ["all"]` / `["none"]` | `protection: ["all"]` / `["none"]` |

<InlineAlert variant="info" slots="text"/>

For `smart_object_layer`, `opacity` and `blendMode` remain nested under `blendOptions`. For all other layer types (image, text, adjustment, solid color, group), they are **top-level** properties in V2.

**Layer Transforms (V1 → V2):**

- V1: layer-level `bounds: {left, top, width, height}`
- V2: `transformMode: "custom"` (required) + `transform: {offset: {horizontal, vertical}, dimension: {width, height}}`
- Additional V2 transform fields: `angle` (rotation in degrees), `skew: {horizontal, vertical}`, `anchor: {horizontal, vertical}`
- `transformMode` values: `"none"`, `"custom"`, `"fit"`, `"fill"` — **not applicable to adjustment layers**

**Layer Alignment (V1 → V2):**

- V1: layer-level `horizontalAlign`, `verticalAlign`
- V2: placement-level `horizontalAlignment`, `verticalAlignment` within `placement: {type: "custom", horizontalAlignment: "center", verticalAlignment: "center"}` (add/move operations only)

**Smart Object Specifics:**

- Layer type: V1 `"smartObject"` → V2 `"smart_object_layer"`
- Source: V1 `input: {href, storage}` → V2 `smartObject.smartObjectFile.source.url` (nested deeper)
- Linked flag: V1 `smartObject.linked` → V2 `smartObject.isLinked`
- V2 supports SVG as source format (V1 did not)
- **Resize with linked smart objects:** Width-only resize (no layer edits) → ALL linked SOs are rasterized to pixel layers. Edit/add a linked SO in the same request + resize → that edited SO stays linked; all other linked SOs are rasterized.
- Cannot replace a linked SO with an embedded SO (V2 limitation)

**Adjustment Layer Specifics:**

- Layer type: V1 `"adjustmentLayer"` → V2 `"adjustment_layer"`
- `adjustments.type` discriminant is **required in V2 and did not exist in V1** — omitting it causes the request to be rejected

  | V1 implicit key | V2 `adjustments.type` | Payload key |
  |---|---|---|
  | `brightnessContrast` | `"brightness_contrast"` | `brightnessContrast` |
  | `exposure` | `"exposure"` | `exposure` |
  | `hueSaturation` | `"hue_saturation"` | `hueSaturation` |
  | `colorBalance` | `"color_balance"` | `colorBalance` |
  | (not in V1) | `"curves"` | — |
  | (not in V1) | `"levels"` | — |
  | (not in V1) | `"gradient_map_custom_stops"` | — |

- **Exposure payload rename:** Inside the `exposure` payload, the amount field is `exposure` in V1 → `exposureValue` in V2 (range: -20 to 20)
- **Hue/Saturation restructure:** V1 `hueSaturation.channels[]` with `channel: "master"` → V2 `hueSaturation.hueSaturationAdjustments[]`; omit `localRange` for master (entire image); include `localRange` with `channelId` for specific color range (`REDS`, `YELLOWS`, `GREENS`, `CYANS`, `BLUES`, `MAGENTAS`) — only when `colorize: false`
- `transformMode` is **not applicable** to adjustment layers
- Parameter ranges: `brightnessContrast.brightness`/`contrast` (-150 to 150); `exposureValue` (-20 to 20), `offset` (-0.5 to 0.5), `gammaCorrection` (0.01 to 9.99); `hue` (-180 to 180, or 0–360 when `colorize: true`); `saturation`/`lightness` (-100 to 100, or 0–100 when `colorize: true`); color balance levels (-100 to 100)

**Text Layer Specifics:**

- Layer type: V1 `"textLayer"` → V2 `"text_layer"`
- **Character style range semantics (breaking off-by-one):**
  - V1: `to` = **length** — `{from: 0, to: 5}` = 5 characters (indices 0–4)
  - V2: `apply.to` = **inclusive end index** — `{apply: {from: 0, to: 4}}` = indices 0–4 (same result)
  - **Migration rule: subtract 1 from V1's `to` value**. Same applies to paragraph style ranges.
- Character style structure: V1 direct properties → V2 wrapped in `characterStyle` object
- Font name: V1 top-level `fontName` → V2 `characterStyle.font.postScriptName` (inside `characterStyle.font`)
- Text bounds: V1 layer-level `bounds: {left, top, width, height}` → V2 `text.frame: {type: "area", bounds: {top, left, right, bottom}}` where `right = left + width`, `bottom = top + height`
- V2 also supports point frames: `text.frame: {type: "point", origin: {x, y}}`
- **Default when no frame given:** V1 default = area frame at (0,0,4,4); V2 default = point frame at canvas center — always set `text.frame` explicitly for predictable placement
- `textOrientation` is a text-level property (not per character-style as V1's `orientation`)
- Multi-line text: use `\r` for line breaks (same in both)
- Font options: V1 `options.fonts` (href+storage) → V2 `fontOptions.additionalFonts` (source.url); V1 `options.globalFont` → V2 `fontOptions.defaultFontPostScriptName`; V1 `options.manageMissingFonts: "useDefault"` → V2 `fontOptions.missingFontStrategy: "use_default"` (`"fail"` unchanged)

### C. Actions migration

**V1 Endpoints Consolidated:**
- `/pie/psdService/photoshopActions`
- `/pie/psdService/actionJSON`
- `/pie/psdService/productCrop`
- `/pie/psdService/depthBlur`
- `/pie/psdService/splitView`
- `/pie/psdService/sideBySide`

**V2 Endpoint:** `/v2/execute-actions`

**Key Change:** Action files for convenience APIs are now published!

**Pattern for .atn Files:**

V1:
```json
{
  "options": {
    "actions": [
      {"href": "<ACTION_URL>", "storage": "external"}
    ]
  }
}
```

V2:
```json
{
  "options": {
    "actions": [
      {
        "source": {
          "url": "<ACTION_URL>"
        }
      }
    ]
  }
}
```

**Pattern for Inline ActionJSON:**

V1:
```json
{
  "options": {
    "actionJSON": [
      {"_obj": "convertMode", "to": {...}}
    ]
  }
}
```

V2:
```json
{
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"convertMode\",\"to\":{...}}]",
          "contentType": "application/json"
        }
      }
    ]
  }
}
```

**Important:** ActionJSON must be stringified JSON in V2.

**Multiple Actions:**
V2 supports up to 10 actions executed in sequence:
```json
{
  "options": {
    "actions": [
      {"source": {"url": "<ACTION_1_URL>"}},
      {"source": {"url": "<ACTION_2_URL>"}},
      {"source": {"url": "<ACTION_3_URL>"}}
    ]
  }
}
```

**Additional Resources:**
```json
{
  "options": {
    "actions": [...],
    "additionalContents": [  // Max 25 (images/compositing resources)
      {"source": {"url": "<IMAGE_URL>"}}
    ],
    "brushes": [           // Max 10 — must use external URLs (binary, no inline)
      {"source": {"url": "<BRUSH_URL>"}}
    ],
    "patterns": [          // Max 10 — must use external URLs (binary, no inline)
      {"source": {"url": "<PATTERN_URL>"}}
    ],
    "fontOptions": {
      "additionalFonts": [ // Max 10 — must use external URLs (binary, no inline)
        {"source": {"url": "<FONT_URL>"}}
      ],
      "missingFontStrategy": "use_default"
    }
  }
}
```

**Additional Contents Placeholder:**
Reference in ActionJSON or UXP scripts as `__ADDITIONAL_CONTENTS_PATH_0__`, `__ADDITIONAL_CONTENTS_PATH_1__`, etc. (0-based index matches position in `additionalContents` array). Binary resources (brushes, patterns, fonts) must use external URLs — inline content is not supported for these types.

#### Convenience API details

**Product Crop:**
- **Steps**: 8 action steps
- **Additional Images**: No
- **Key Parameter**: Padding (default: 50 pixels, customizable)
- **What It Does**: Auto cutout + trim + padding + flatten
- **Customization**: Modify canvasSize step (5th action) to change padding values
- **Use Case**: E-commerce product isolation with consistent padding

**Depth Blur:** **Depth Blur is not yet supported in V2.** Neural Filters are unavailable in V2; continue using the V1 `/pie/psdService/depthBlur` endpoint for this feature. The parameters below are for reference only.
- **Steps**: 1 action step (Neural Gallery Filter)
- **Additional Images**: No
- **Key Parameters**: 11 customizable parameters (all have defaults)
  - `spl::focalSelector`: "auto" - Focus point selection
  - `spl::selectSubjectUsage`: 1 - Subject selection mode
  - `spl::slideAperture`: 50 - Blur strength (0-100)
  - `spl::slideFocalDist`: 50 - Focal distance (0-100)
  - `spl::slideFocalRange`: 50 - Focal range size (0-100)
  - `spl::sliderBrightness`: 0 - Brightness (-100 to 100)
  - `spl::sliderHaze`: 0 - Haze effect (-100 to 100)
  - `spl::sliderNoise`: 0 - Grain/noise (0-100)
  - `spl::sliderSaturation`: 0 - Saturation (-100 to 100)
  - `spl::sliderTint`: 0 - Color tint (-100 to 100)
  - `spl::sliderWarmness`: 0 - Color temperature (-100 to 100)
- **What It Does**: Applies neural depth-of-field blur effect
- **Use Case**: Portrait and product photography with bokeh effects

**Text Layer Operations:**
- **V1**: `/pie/psdService/text` — declarative request with `options.layers[]` (layer name + characterStyles with `size`, `color`, `fontPostScriptName`, etc.)
- **V2**: `/v2/execute-actions` — **no equivalent declarative text endpoint exists in V2**; must use ActionJSON or UXP
- **Additional Contents**: No

**When to use ActionJSON vs UXP for text edits:**

| Use Case | Use |
|---|---|
| Fixed edits (font, size, color) for known layer names | ActionJSON (`options.actions`) |
| Conditional edits (only if layer is text type, only if name matches) | UXP (`options.uxp`) |
| Iterate all layers and apply logic | UXP |
| Toggle or state-based changes (e.g. bold → regular) | UXP |

**ActionJSON pattern** (stringified, passed as `options.actions[].source.content` with `contentType: "application/json"`):
1. `select` layer by `_name` → `makeVisible: true`
2. `set` textStyle: font size (`size` with `_unit: "pointsUnit"`, `textOverrideFeatureName: 808465458`, `typeStyleOperationType: 3`)
3. `set` textStyle: font (`fontPostScriptName`, `fontName`, `fontStyleName`)
4. `set` textStyle: color (`color` with `_obj: "RGBColor"`, `red`, `green`, `blue`)

For multiple layers: repeat the `select` + `set` sequence within the same stringified ActionJSON array.

**UXP pattern** (passed as `options.uxp.source.content` with `contentType: "application/javascript"`):
- Use `core.executeAsModal()` for document modifications
- Access `layer.kind === "text"` to identify text layers
- Use `layer.textItem.characterStyle` to modify `fauxBold`, `fauxItalic`, etc.
- Use `plugin-temp:/filename.ext` for script output files

**Split View:**
- **Steps**: 34 action steps
- **Additional Contents**: Yes (2 required)
  - `__ADDITIONAL_CONTENTS_PATH_0__`: Edited/final output image
  - `__ADDITIONAL_CONTENTS_PATH_1__`: Product logo
- **Key Parameters**: Width: 1200px (resizes final output)
- **What It Does**: Masked before/after comparison with center divider line + logo
- **Use Case**: Demonstrating image processing effects with branding

**Side by Side:**
- **Steps**: 19 action steps
- **Additional Contents**: Yes (2 required)
  - `__ADDITIONAL_CONTENTS_PATH_0__`: Edited/final output image
  - `__ADDITIONAL_CONTENTS_PATH_1__`: Product logo
- **Key Parameters**: Width: 1195.0px (exact value with decimal)
- **What It Does**: Simple side-by-side comparison without masking + logo
- **Use Case**: Clean before/after comparisons with branding
- **Key Difference from Split View**: Simpler, no complex masking or divider lines

**UXP Scripts (Limited Availability):**
```json
{
  "options": {
    "uxp": {
      "source": {
        "content": "const app = require('photoshop').app; app.activeDocument.flatten();",
        "contentType": "application/javascript"
      }
    }
  }
}
```

Use `plugin-temp:/filename.ext` path in UXP scripts to write output files to the plugin temporary directory (e.g., `plugin-temp:/result.json`). Then reference them in `scriptOutputPattern`.

**Script Output Discovery:**
```json
{
  "outputs": [
    {
      "destination": {"validityPeriod": 3600},
      "mediaType": "application/json",
      "scriptOutputPattern": "result.json"
    }
  ]
}
```

Supports glob patterns: `*.json`, `result-*.png`, etc.

### D. Other operations

**Artboards:**

- **V1:** `image.adobe.io/pie/psdService/artboardCreate` → **V2:** `photoshop-api.adobe.io/v2/create-artboard`
- **Input structure:** V1 `inputs[].href` → V2 `images[].source.url` (or `creativeCloudPath`, `creativeCloudFileId`, `lightroomPath`). V1 `inputs[].storage` → only needed for Azure/Dropbox in outputs; omit for standard URLs.
- **Output structure:** Same as other endpoints — `outputs[].href` → `outputs[].destination.url`, `outputs[].type` → `outputs[].mediaType`.
- **New V2 parameter:** `artboardSpacing` (optional integer, pixels, default 50) — horizontal spacing between artboards.
- **Validation:** 1–25 images, 1–25 outputs.
- **Source options:** External URL, Creative Cloud Path, Creative Cloud File ID, Lightroom Path.
- **Output formats:** JPEG, PNG, TIFF, PSD, PSDC, JSON manifest (6 formats).
- **Storage options:** Same as other endpoints (External, Hosted, Embedded, Creative Cloud, Azure, Dropbox).

**Manifest:**
- V1: `/pie/psdService/documentManifest`
- V2: `/v2/generate-manifest`
- Pattern: Returns manifest to specified output destination
- Options: `includeLayerThumbnails`, `includeXmp`, `maximumThumbnailDepth`, `trimToTransparency` (boolean, crops layer thumbnails to visible content; requires `includeLayerThumbnails: true`; has no effect on adjustment layers or layers with no pixel data — those always return a blank white canvas thumbnail; specific to `/v2/generate-manifest` — for trimming exported images in `/v2/create-composite` or `/v2/execute-actions`, use `cropMode: "trim_to_transparency"` in output options instead)
- V1 manifest had `locked` (boolean) on layers → V2 returns `protection` (array of flags: `none`, `all`, `transparency`, `composite`, `position`, `artboard_autonest`)
- V1 manifest had `mask` property with `offset.x`/`offset.y` → V2 uses `pixelMask` with `offset.horizontal`/`offset.vertical`, plus new `hasMask`, `extendOpaque`, `bounds` fields; density/feather moved to separate `userMask` property; to delete a pixel mask in edit operations use `pixelMask: { "delete": true }` (edit only, not valid on add; supported on all layer types)
- Clipping mask: V1 `mask.clip` → V2 `layerSettings.clippingMask` in manifest; use top-level `isClipped: true` in edit operations
- **Layer type renames** (manifest response only — V2 edit/create-composite request payloads still use `"type": "layer"` unchanged): `layer`→`pixel_layer`, `textLayer`→`text_layer`, `layerSection`→`group_layer`, `layerSection`(artboard)→`artboard`, `smartObject`→`smart_object_layer`, `fillLayer`→`solid_color_layer`, `adjustmentLayer`→`adjustment_layer`, `backgroundLayer`→`background_layer`
- **`bounds` format changed**: V1 `{height, left, top, width}` → V2 `{left, top, right, bottom}` (no height/width; compute from right-left, bottom-top)
- **`thumbnail` changed**: V1 plain string URL → V2 object `{mediaType, url}` (only present when thumbnails requested)
- **Artboard children key changed**: V1/groups use `children[]`; V2 artboards use `layers[]` for their children (recursive traversal must handle both)
- Document field renames: `bitDepth`→`depth`, `iccProfileName`→`iccProfile`, `name`→`title`, `height`+`width`→`bounds`; `photoshopBuild` removed
- See `manifest-response-migration.md` for the full field-by-field response format reference

**Status:**
- V1: Service-specific endpoints
- V2: Unified `/v2/status/{jobId}`
- Same jobId works across all operation types

### E. Export layers (single vs multi-layer)

Export layers via `outputs[].layers` on the `/v2/create-composite` endpoint. Behavior differs between single-layer and multi-layer exports.

**Single-Layer Export** — specify exactly one layer in `outputs[].layers`:
- Supports all `cropMode` values: `"layer_bounds"` (default), `"trim_to_transparency"`, `"document_bounds"`
- Supported formats: JPEG, PNG, TIFF, **PSD** (PSD is allowed for single-layer only)
- Default JPEG quality: `photoshop_max`; default PNG compression: `default` (level 6)

**Multi-Layer Export** — specify two or more layers in `outputs[].layers`:
- Composites those layers to a single raster file
- Supported formats: JPEG, PNG, TIFF — **PSD is NOT supported for multi-layer export**
- `cropMode` supports `"document_bounds"` (default) and `"trim_to_transparency"` — `"layer_bounds"` returns a validation error
- Same quality/compression defaults as single-layer

**Document Export** — no `layers` specified (exports full document):
- `cropMode` supports `"document_bounds"` (default) and `"trim_to_transparency"` — `"layer_bounds"` returns a validation error

```json
// Single-layer: V2 example with cropMode
{
  "image": {"source": {"url": "<PSD_URL>"}},
  "outputs": [{
    "destination": {"url": "<OUTPUT_URL>"},
    "mediaType": "image/png",
    "layers": [{"id": 1096}],
    "cropMode": "trim_to_transparency"
  }]
}

// Multi-layer: V2 example with cropMode (no PSD)
{
  "image": {"source": {"url": "<PSD_URL>"}},
  "outputs": [{
    "destination": {"url": "<OUTPUT_URL>"},
    "mediaType": "image/jpeg",
    "layers": [{"id": 1096}, {"id": 996}],
    "quality": "maximum",
    "cropMode": "trim_to_transparency"
  }]
}
```

## Storage solutions reference

### Storage decision matrix

| Use Case | Recommended Storage | Why |
|----------|-------------------|-----|
| Production workflows | External presigned URLs | Full control, scalability, integration |
| Creative Cloud/ACP integration | Creative Cloud paths | Seamless CC workflow via ACP, direct access |
| Large files or batches | External storage | Better performance, cost-effective |
| XMP metadata / JSON manifests | Embedded (string/json) | Immediate response, no storage setup |
| Temporary edits | Hosted (presigned URLs) | No storage management required |

### 1. External storage (presigned URLs)

**Supports:** AWS S3, Azure Blob, Dropbox, Frame.io, Google Drive

**For Input:**
```json
{
  "image": {
    "source": {
      "url": "<PRESIGNED_GET_URL>"
    }
  }
}
```

**For Output:**
```json
{
  "outputs": [
    {
      "destination": {
        "url": "<PRESIGNED_PUT_URL>",
        "storageType": "azure"  // Only for Azure or Dropbox
      },
      "mediaType": "image/jpeg"
    }
  ]
}
```

**When to use `storageType`:**
- Azure: `"storageType": "azure"`
- Dropbox: `"storageType": "dropbox"`
- AWS S3, Frame.io, Google Drive: NOT required

### 2. Creative Cloud storage

**Note:** Creative Cloud Storage refers specifically to ACP (Adobe Content Platform) for file storage and access.

```json
{
  "image": {
    "source": {
      "creativeCloudPath": "my-folder/input.psd"
      // OR
      "creativeCloudFileId": "urn:aaid:...",
      "creativeCloudProjectId": "urn:aaid:sc:..."  // Optional
    }
  },
  "outputs": [
    {
      "destination": {
        "creativeCloudPath": "my-folder/output.jpg"
      },
      "mediaType": "image/jpeg"
    }
  ]
}
```

<InlineAlert variant="warning" slots="text"/>

**No leading slash:** `creativeCloudPath` values must NOT have a leading `/`. Use `"my-folder/file.psd"`, not `"/my-folder/file.psd"`.

**When to use:**
- Integration with CC ecosystem and ACP
- Direct access to user's CC files stored in ACP
- Collaboration workflows

### 3. Embedded storage

**For text-based outputs only (XMP, JSON):**
```json
{
  "outputs": [
    {
      "destination": {
        "embedded": "string"  // For XMP (XML text)
        // OR
        "embedded": "json"    // For JSON manifests
        // OR
        "embedded": "base64"  // For small binary data
      },
      "mediaType": "application/rdf+xml"  // or application/json
    }
  ]
}
```

**When to use:**
- XMP metadata extraction
- JSON manifest data
- Immediate access needed
- No storage setup required

**IMPORTANT:** Do NOT use for images. Only for text/metadata outputs.

**Response format:**
```json
{
  "result": {
    "outputs": [
      {
        "destination": {
          "embedded": "string",
          "content": "<?xml version=\"1.0\"...>"  // For string
          // OR for JSON:
          // "embedded": "json",
          // "content": {"document": {...}}
        },
        "mediaType": "application/rdf+xml"
      }
    ]
  }
}
```

### 4. Hosted storage

**Adobe-managed temporary storage:**
```json
{
  "outputs": [
    {
      "destination": {
        "validityPeriod": 3600  // Seconds: 60-86400 (max 1 day)
      },
      "mediaType": "image/jpeg"
    }
  ]
}
```

**When to use:**
- Temporary processing workflows
- No long-term storage needed (files expire within 24 hours)
- Quick prototyping

**Response:**
```json
{
  "result": {
    "outputs": [
      {
        "destination": {
          "url": "https://adobe-hosted-storage.../file.jpg?expires=..."
        },
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

**IMPORTANT:** Download before URL expires (maximum 24 hours from job completion)!

## Output types migration

### Overview

V2 introduces significant changes to output format specifications affecting all endpoints that generate outputs. This section covers the structural changes and format-specific parameter transformations for JPEG, PNG, PSD, and TIFF outputs.

### Structural changes (all output formats)

All output types share these common structural changes:

| V1 Field | V2 Field | Required | Notes |
|----------|----------|----------|-------|
| `outputs[].href` | `outputs[].destination.url` | Yes | Nested in destination object |
| `outputs[].type` | `outputs[].mediaType` | Yes | Renamed for clarity |
| `outputs[].storage` | `outputs[].destination.storageType` | No* | Only for Azure/Dropbox |

*`storageType` is optional and only required for Azure Blob Storage and Dropbox.

**V1 Pattern:**
```json
{
  "outputs": [{
    "href": "https://...",
    "storage": "external",
    "type": "image/jpeg"
  }]
}
```

**V2 Pattern:**
```json
{
  "outputs": [{
    "destination": {
      "url": "https://..."
    },
    "mediaType": "image/jpeg"
  }]
}
```

### JPEG quality migration

**V1:** Numeric values (1-7 or 1-12)
**V2:** Descriptive string enums

#### JPEG quality mapping

| V1 Numeric | V2 String | Use Case |
|------------|-----------|----------|
| 1-2 | `"low"` | Thumbnails, small previews |
| 3-4 | `"medium"` | Standard web images |
| 5-6 | `"high"` | High-quality web images |
| 7 | `"maximum"` | Print, production |
| N/A | `"photoshop_max"` | Professional print, highest quality (recommended default) |
| N/A | `"very_poor"` | Smallest file size (V2 only) |
| N/A | `"poor"` | Very small files (V2 only) |

**Default:** Use `"photoshop_max"` for production workflows.

**V1 Example:**
```json
{
  "type": "image/jpeg",
  "quality": 7,
  "width": 2000
}
```

**V2 Example:**
```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum",
  "width": 2000
}
```

### PNG compression migration

**V1:** Three compression levels: "small", "medium", "large"
**V2:** Ten granular compression levels (zlib/libpng standard)

#### PNG compression mapping

| V1 | V2 Recommended | V2 Alternatives | Notes |
|----|---------------|-----------------|-------|
| `"small"` | `"maximum"` | `"very_high"`, `"high"` | Smallest files, slower |
| `"medium"` | `"medium"` | `"default"`, `"medium_high"`, `"medium_low"` | Balanced (default) |
| `"large"` | `"low"` | `"very_low"`, `"none"` | Fastest, larger files |

#### V2 PNG compression values (complete)

- `"none"` (level 0) - No compression
- `"very_low"` (level 1) - Minimal compression
- `"low"` (level 2) - Low compression
- `"medium_low"` (level 3) - Medium-low compression
- `"medium"` (level 4) - Medium compression
- `"medium_high"` (level 5) - Medium-high compression
- `"default"` (level 6) - **Library standard (default when omitted)**
- `"high"` (level 7) - High compression
- `"very_high"` (level 8) - Very high compression
- `"maximum"` (level 9) - Maximum compression

**V1 Example:**
```json
{
  "type": "image/png",
  "compression": "medium"
}
```

**V2 Example:**
```json
{
  "mediaType": "image/png",
  "compression": "medium"
}
```

**Important:** PNG uses `compression`, NOT `quality`.

### PSD and TIFF outputs

**PSD** and **TIFF** outputs have no format-specific parameters (no quality or compression options in V2). Only the structural field changes apply:

**V1 PSD:**
```json
{
  "href": "https://...",
  "storage": "external",
  "type": "image/vnd.adobe.photoshop"
}
```

**V2 PSD:**
```json
{
  "destination": {
    "url": "https://..."
  },
  "mediaType": "image/vnd.adobe.photoshop"
}
```

**Cloud PSD (PSDC):**
Use `"mediaType": "document/vnd.adobe.cpsd+dcxucf"` (primary form). Both `document/vnd.adobe.cpsd+dcxucf` and `document/vnd.adobe.cpsd+dcx` are supported for ACP (Adobe Cloud Platform) storage and external storage. The older V1 form `image/vnd.adobe.photoshop+dcx` is not used in V2.

### Common output fields

All output types support these optional fields:

- `width` (integer, ≥ 0) - Output width in pixels
- `height` (integer, ≥ 0) - Output height in pixels
- `maxWidth` (integer, ≥ 0) - Maximum width in pixels
- `resample` (string, optional) - Resampling algorithm when resizing to `width`/`maxWidth`. Values: `nearest_neighbor`, `bilinear`, `bicubic`, `bicubic_smoother`, `bicubic_sharper`. Defaults to `bicubic`. Applies to JPEG, PNG, and TIFF exports.
- `shouldTrimToCanvas` (boolean) - Trim transparent pixels

### Multiple outputs

V2 supports up to 25 outputs per request:

```json
{
  "outputs": [
    {
      "destination": {"url": "..."},
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2400
    },
    {
      "destination": {"url": "..."},
      "mediaType": "image/jpeg",
      "quality": "medium",
      "width": 800
    },
    {
      "destination": {"url": "..."},
      "mediaType": "image/png",
      "compression": "high"
    }
  ]
}
```

### Color mode and bit depth validation

The API automatically converts source images when the color mode or bit depth is not supported by the target format. The behavior differs by export path.

<InlineAlert variant="info" slots="text"/>

**Export paths:** *Full document* = whole document export. *Single layer* = exporting one layer. *Layers composite* = exporting a composite of multiple selected layers. Layers composite does **not** apply any format-specific conversion.

#### Bit depth validation table

| Export Path      | Target Format | Supported Depths | Fallback                   | ICC Profile Specified |
| ---------------- | ------------- | ---------------- | -------------------------- | --------------------- |
| Full document    | JPEG          | 8-bit only       | Convert to 8-bit if needed | No                    |
| Full document    | JPEG          | 8-bit only       | No conversion              | Yes                   |
| Full document    | PNG           | 8-bit, 16-bit    | Convert to 8-bit if needed | No                    |
| Full document    | PNG           | 8-bit, 16-bit    | No conversion              | Yes                   |
| Full document    | TIFF          | 8, 16, 32-bit    | No conversion              | N/A                   |
| Full document    | PSD           | 8, 16, 32-bit    | No conversion              | N/A                   |
| Full document    | PSDC          | 8, 16, 32-bit    | No conversion              | N/A                   |
| Single layer     | JPEG          | 8-bit only       | Convert to 8-bit if needed | N/A                   |
| Single layer     | PNG           | 8-bit, 16-bit    | Convert to 8-bit if needed | N/A                   |
| Single layer     | TIFF          | 8, 16, 32-bit    | No conversion              | N/A                   |
| Single layer     | PSD           | 8, 16-bit only   | Convert to 8-bit if needed | N/A                   |
| Layers composite | JPEG          | —                | No conversion              | N/A                   |
| Layers composite | PNG           | —                | No conversion              | N/A                   |
| Layers composite | TIFF          | —                | No conversion              | N/A                   |

<InlineAlert variant="info" slots="text"/>

Single-layer PSD export supports only 8 or 16-bit (not 32-bit).

#### Color mode validation table

| Export Path      | Target Format | Supported Modes      | Fallback                 | ICC Profile Specified |
| ---------------- | ------------- | -------------------- | ------------------------ | --------------------- |
| Full document    | JPEG          | RGB, Grayscale, CMYK | Convert to RGB if needed | No                    |
| Full document    | JPEG          | RGB, Grayscale, CMYK | No conversion            | Yes                   |
| Full document    | PNG           | RGB, Grayscale       | Convert to RGB if needed | No                    |
| Full document    | PNG           | RGB, Grayscale       | No conversion            | Yes                   |
| Full document    | TIFF          | All                  | No conversion            | N/A                   |
| Full document    | PSD           | All                  | No conversion            | N/A                   |
| Full document    | PSDC          | All                  | No conversion            | N/A                   |
| Single layer     | JPEG          | RGB, Grayscale, CMYK | Convert to RGB if needed | N/A                   |
| Single layer     | PNG           | RGB, Grayscale       | Convert to RGB if needed | N/A                   |
| Single layer     | TIFF          | All                  | No conversion            | N/A                   |
| Single layer     | PSD           | RGB, Grayscale, CMYK | Convert to RGB if needed | N/A                   |
| Layers composite | JPEG          | —                    | No conversion            | N/A                   |
| Layers composite | PNG           | —                    | No conversion            | N/A                   |
| Layers composite | TIFF          | —                    | No conversion            | N/A                   |

### Output type-specific issues

#### Issue: Numeric JPEG quality

**Problem:**
```json
{
  "mediaType": "image/jpeg",
  "quality": 7
}
```

**Error:**
```
Invalid value '7' at path 'outputs[0].quality'.
Accepted values are: very_poor, poor, low, medium, high, maximum, photoshop_max
```

**Solution:**
```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum"
}
```

#### Issue: Old PNG compression values

**Problem:**
```json
{
  "mediaType": "image/png",
  "compression": "small"
}
```

**Error:**
```
Invalid value 'small' at path 'outputs[0].compression'.
```

**Solution:**
```json
{
  "mediaType": "image/png",
  "compression": "maximum"
}
```

#### Issue: Using quality for PNG

**Problem:**
```json
{
  "mediaType": "image/png",
  "quality": "high"
}
```

**Error:**
```
'quality' parameter is not supported for PNG format
```

**Solution:**
```json
{
  "mediaType": "image/png",
  "compression": "high"
}
```

## ICC profile support (V2 new feature)

ICC profile support is a **new V2 capability** — V1 had no output color profile configuration.

### Overview

ICC profiles can be applied in two places:

1. **On `outputs`** — controls the exported file's color space. Add `iccProfile` to any output in `/v2/create-composite`, `/v2/create-artboard`, or `/v2/execute-actions`. Supported for JPEG, PNG, TIFF, and PSD — **not for PSDC** (Cloud PSD).
2. **On `image` (document creation)** — sets the document's embedded color profile at creation time. Add `iccProfile` to the `image` block when creating a new document (no `image.source`). Supports both standard and custom profiles.

### Standard profiles

Use a predefined profile name (no external file needed):

```json
"iccProfile": {
  "type": "standard",
  "name": "sRGB IEC61966-2.1",
  "imageMode": "rgb"
}
```

**RGB profiles:** `"Adobe RGB (1998)"`, `"Apple RGB"`, `"ColorMatch RGB"`, `"sRGB IEC61966-2.1"`

**Grayscale profiles (Dot Gain):** `"Dot Gain 10%"`, `"Dot Gain 15%"`, `"Dot Gain 20%"`, `"Dot Gain 25%"`, `"Dot Gain 30%"`

**Grayscale profiles (Gray Gamma):** `"Gray Gamma 1.8"`, `"Gray Gamma 2.2"`

<InlineAlert variant="warning" slots="text"/>

Profile names must match exactly (including spaces and punctuation). `imageMode` for standard profiles: `"rgb"` or `"grayscale"` only — CMYK is not supported.

### Custom profiles (enables CMYK)

Use your own `.icc` file — required for CMYK output:

```json
"iccProfile": {
  "type": "custom",
  "name": "U.S. Web Coated (SWOP) v2",
  "imageMode": "cmyk",
  "source": {
    "url": "https://example.com/profiles/custom.icc"
  }
}
```

`imageMode` options for custom: `"rgb"`, `"grayscale"`, or `"cmyk"`.

### Format support table

| Format | mediaType | ICC Profile Supported |
|--------|-----------|----------------------|
| JPEG | `image/jpeg` | Yes |
| PNG | `image/png` | Yes |
| TIFF | `image/tiff` | Yes |
| PSD | `image/vnd.adobe.photoshop` | Yes |
| PSDC | `document/vnd.adobe.cpsd+dcxucf` | **No** |

### Conversion behavior with ICC profile

When an ICC profile is specified on a full-document export, format-specific bit-depth/color-mode conversion is **skipped** — the ICC transformation handles color management instead. See Color Mode and Bit Depth Validation tables above.

### Output migration quick reference

**For LLMs helping with migration:**

1. **Always check output format** before suggesting parameters:
   - JPEG → use `quality` (string enum)
   - PNG → use `compression` (string enum)
   - PSD/TIFF → no format-specific parameters

2. **Default recommendations:**
   - JPEG: `"photoshop_max"` (highest quality, recommended default)
   - PNG: `"default"` (level 6 library standard; default when omitted)

3. **Common transformation pattern:**
   ```javascript
   // V1 to V2 transformation
   v1.outputs[0].href → v2.outputs[0].destination.url
   v1.outputs[0].type → v2.outputs[0].mediaType
   v1.outputs[0].quality (7) → v2.outputs[0].quality ("maximum")
   v1.outputs[0].storage → omit (for S3) or move to destination.storageType
   ```

## Common migration issues and solutions

### Category: Missing/incorrect fields

#### Issue: Missing outputs array

**Problem:**
```json
{
  "image": {"source": {"url": "<URL>"}},
  "edits": {...}
  // Missing outputs!
}
```

**Solution:**
```json
{
  "image": {"source": {"url": "<URL>"}},
  "edits": {...},
  "outputs": [
    {
      "destination": {"url": "<OUTPUT_URL>"},
      "mediaType": "image/jpeg"
    }
  ]
}
```

#### Issue: Wrong media type property

**Problem:** Using `type` instead of `mediaType`
```json
{
  "outputs": [{
    "destination": {...},
    "type": "image/jpeg"  // Wrong!
  }]
}
```

**Solution:**
```json
{
  "outputs": [{
    "destination": {...},
    "mediaType": "image/jpeg"  // Correct!
  }]
}
```

#### Issue: Invalid quality values

**Problem:** Using V1 numeric quality (1-7)
```json
{
  "quality": 7  // V1 format
}
```

**Solution:** Use V2 string values
```json
{
  "quality": "maximum"  // V2 format
}
```

Valid V2 values: `"very_poor"`, `"poor"`, `"low"`, `"medium"`, `"high"`, `"maximum"`, `"photoshop_max"`

**Note:** V2 only accepts string enums. Numeric values from V1 are not supported.

### Category: Storage issues

#### Issue: Using V1 storage parameter

**Problem:**
```json
{
  "storage": "external"  // V1 format
}
```

**Solution:** Use destination structure
```json
{
  "destination": {
    "url": "<URL>"
    // storageType only for Azure/Dropbox
  }
}
```

#### Issue: storageType confusion

**Problem:** Adding storageType for AWS S3
```json
{
  "destination": {
    "url": "<S3_URL>",
    "storageType": "external"  // NOT needed!
  }
}
```

**Solution:** Omit storageType for standard URLs
```json
{
  "destination": {
    "url": "<S3_URL>"
    // No storageType needed
  }
}
```

Only use storageType for:
- Azure: `"storageType": "azure"`
- Dropbox: `"storageType": "dropbox"`

#### Issue: Embedded storage for images

**Problem:** Using embedded for image output
```json
{
  "destination": {
    "embedded": "base64"
  },
  "mediaType": "image/jpeg"  // Too large!
}
```

**Solution:** Use external or hosted storage for images
```json
{
  "destination": {
    "url": "<OUTPUT_URL>"
  },
  "mediaType": "image/jpeg"
}
```

Embedded is only for XMP metadata and JSON manifests.

### Category: Request structure issues

#### Issue: Using V1 input structure

**Problem:**
```json
{
  "inputs": [
    {
      "href": "<URL>",
      "storage": "external"
    }
  ]
}
```

**Solution:** Use V2 image structure
```json
{
  "image": {
    "source": {
      "url": "<URL>"
    }
  }
}
```

#### Issue: Wrong parameter names

**Problem:** Using V1 PascalCase
```json
{
  "options": {
    "Exposure": 1.2,
    "Contrast": 10
  }
}
```

**Solution:** Use V2 camelCase with categories
```json
{
  "edits": {
    "light": {
      "exposure": 1.2,
      "contrast": 10
    }
  }
}
```

### Category: Layer operations

#### Issue: Missing operation type

**Problem:** Not specifying operation type when adding layer
```json
{
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "New Layer",
        "image": {
          "source": {"url": "<URL>"}
        }
        // Missing operation!
      }
    ]
  }
}
```

**Solution:** Specify operation type
```json
{
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "New Layer",
        "image": {
          "source": {"url": "<URL>"}
        },
        "operation": {
          "type": "add",
          "placement": {"type": "top"}
        }
      }
    ]
  }
}
```

#### Issue: Wrong layer type name

**Problem:** Using V1 layer type names
```json
{
  "type": "textLayer"     // V1
  "type": "adjustmentLayer"  // V1
  "type": "smartObject"   // V1
}
```

**Solution:** Use V2 underscore format
```json
{
  "type": "text_layer"           // V2
  "type": "adjustment_layer"     // V2
  "type": "smart_object_layer"   // V2
  "type": "solid_color_layer"    // V2
}
```

#### Issue: Incorrect placement syntax

**Problem:** Using V1 placement syntax
```json
{
  "add": {
    "insertTop": true
  }
}
```

**Solution:** Use V2 operation structure
```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

### Category: XMP and masks issues

#### Issue: V1 mask structure not working

**Problem:** Using V1 mask structure with href and storage

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"}
    },
    "masks": [
      {
        "href": "<MASK_URL>",
        "storage": "external",
        "digest": "37B3568A954F0C80CA946DA0187FB9E2"
      }
    ]
  }
}
```

**Solution:** Masks must be nested inside `xmp` object, not sibling to it, and use `source` structure

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"},
      "masks": [
        {
          "source": {
            "url": "<MASK_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        }
      ]
    }
  }
}
```

#### Issue: Inline XMP string not supported in V2

**Problem:** Using inline XMP string from V1

```json
{
  "edits": {
    "xmp": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>..."
  }
}
```

**Solution:** V2 requires XMP to be provided as a file reference

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_FILE_URL>"
      }
    }
  }
}
```

Or use Creative Cloud storage:

```json
{
  "edits": {
    "xmp": {
      "source": {
        "creativeCloudPath": "/path/to/metadata.xmp"
      }
    }
  }
}
```

#### Issue: Missing mask digest

**Problem:** Providing mask without digest

```json
{
  "masks": [
    {
      "source": {"url": "<MASK_URL>"}
    }
  ]
}
```

**Solution:** Each mask must include a digest for identification

```json
{
  "masks": [
    {
      "source": {"url": "<MASK_URL>"},
      "digest": "37B3568A954F0C80CA946DA0187FB9E2"
    }
  ]
}
```

#### Issue: Using numeric orientation values

**Problem:** Using numeric EXIF codes for orientation

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"},
      "orientation": 6
    }
  }
}
```

**Solution:** Use descriptive string values from the enum

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"},
      "orientation": "right_top"
    }
  }
}
```

Valid orientation values: `"top_left"`, `"top_right"`, `"bottom_right"`, `"bottom_left"`, `"left_top"`, `"right_top"`, `"right_bottom"`, `"left_bottom"`

#### Issue: Orientation at wrong nesting level

**Problem:** Placing orientation at `edits` level instead of within `xmp`

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"}
    },
    "orientation": "right_top"
  }
}
```

**Solution:** Nest orientation inside the `xmp` object

```json
{
  "edits": {
    "xmp": {
      "source": {"url": "<XMP_URL>"},
      "orientation": "right_top"
    }
  }
}
```

### Category: Actions issues

#### Issue: Wrong ActionJSON format

**Problem:** Providing ActionJSON as object/array
```json
{
  "source": {
    "content": [{"_obj": "..."}],  // Wrong: array
    "contentType": "application/json"
  }
}
```

**Solution:** Stringify the ActionJSON
```json
{
  "source": {
    "content": "[{\"_obj\":\"...\"}]",  // Correct: string
    "contentType": "application/json"
  }
}
```

#### Issue: Missing contentType

**Problem:**
```json
{
  "source": {
    "content": "[...]"
    // Missing contentType!
  }
}
```

**Solution:** Always specify contentType for inline content
```json
{
  "source": {
    "content": "[...]",
    "contentType": "application/json"
  }
}
```

#### Issue: Wrong action structure

**Problem:** Using V1 action structure
```json
{
  "options": {
    "actions": [
      {
        "href": "<URL>",
        "storage": "external"
      }
    ]
  }
}
```

**Solution:** Use V2 source structure
```json
{
  "options": {
    "actions": [
      {
        "source": {
          "url": "<URL>"
        }
      }
    ]
  }
}
```

### Category: Artboard issues

#### Issue: Incorrect input structure

**Problem:** Using v1 input format
```json
{
  "inputs": [
    {"href": "<URL>", "storage": "external"}
  ]
}
```

**Solution:** Use v2 images structure
```json
{
  "images": [
    {"source": {"url": "<URL>"}}
  ]
}
```

#### Issue: Too many images

**Problem:** Exceeding the maximum number of images (25).

**Error:** `Array size must be between 1 and 25 at path 'images'`

**Solution:** Ensure between 1 and 25 images in the request.

#### Issue: Too many outputs

**Problem:** Exceeding the maximum number of outputs (25).

**Error:** `Array size must be between 1 and 25 at path 'outputs'`

**Solution:** Ensure between 1 and 25 outputs in the request.

#### Issue: Missing required source

**Problem:** Missing source in image.

**Error:** `Required field 'source' is missing at path 'images[0]'`

**Solution:** Every image must have a source field.
```json
{
  "images": [
    {"source": {"url": "<URL>"}}
  ]
}
```

#### Issue: Invalid hosted storage period

**Problem:** Hosted storage validityPeriod outside allowed range (60–86400 seconds).

**Error:** `validityPeriod must be between 60 and 86400 seconds`

**Solution:** Use a value between 60 (1 minute) and 86400 (24 hours).
```json
{
  "destination": {"validityPeriod": 3600}
}
```

#### Issue: Missing storage type for Azure/Dropbox

**Problem:** Using Azure or Dropbox without specifying storageType.

**Error:** `Azure Blob Storage URL requires 'storageType': 'azure'`

**Solution:** Add storageType for Azure and Dropbox.
```json
{
  "destination": {
    "url": "<AZURE_URL>",
    "storageType": "azure"
  }
}
```

#### Issue: Invalid JPEG quality value (artboard outputs)

**Problem:** Using numeric quality instead of string enum.

**Error:** `Invalid value '7' at path 'outputs[0].quality'. Accepted values are: very_poor, poor, low, medium, high, maximum, photoshop_max`

**Solution:** Use string enum values for quality.
```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum"
}
```

### Category: Response handling

#### Issue: Looking for manifest in initial response

**Problem:** Expecting manifest data immediately

**Solution:** Poll status endpoint
```shell
# Step 1: Submit job
curl -X POST https://photoshop-api.adobe.io/v2/generate-manifest ...

# Response: {"jobId": "..."}

# Step 2: Poll status
curl -X GET https://photoshop-api.adobe.io/v2/status/{jobId} ...

# Response when complete:
# {
#   "status": "succeeded",
#   "result": {
#     "outputs": [
#       {"url": "..."}  // for hosted/url destinations
#       // OR
#       {"destination": {"embedded": "...", "content": {...}}}  // for embedded
#     ]
#   }
# }
```

#### Issue: Not handling all status values

**Problem:** Only checking succeeded/failed
```javascript
if (status === 'succeeded') { ... }
else { /* assume failed */ }
```

**Solution:** Handle all status values
```javascript
switch (status) {
  case 'succeeded':
    // Process result
    break;
  case 'failed':
    // Handle error
    break;
  case 'pending':
  case 'running':
    // Continue polling
    break;
  default:
    // Unknown status
}
```

#### Issue: Not handling error details array

**Problem:** Expecting single error message
```javascript
console.error(status.error);  // Wrong
```

**Solution:** Iterate error details array
```javascript
status.errorDetails.forEach(error => {
  console.error(`${error.errorCode}: ${error.message}`);
});
```

## Code transformation examples

### Example 1: Simple edit (auto tone)

**V1 Code:**
```shell
curl -X POST https://image.adobe.io/lrService/autoTone \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "https://my-storage.com/input.jpg",
    "storage": "external"
  },
  "outputs": [
    {
      "href": "https://my-storage.com/output.jpg",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Code:**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "https://my-storage.com/input.jpg"
    }
  },
  "edits": {
    "autoTone": true
  },
  "outputs": [
    {
      "destination": {
        "url": "https://my-storage.com/output.jpg"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

**Key Transformations:**
1. Base URL: `image.adobe.io` → `photoshop-api.adobe.io`
2. Endpoint: `/lrService/autoTone` → `/v2/edit`
3. Input: `inputs.href` → `image.source.url`
4. Operation: Implicit → `edits.autoTone: true`
5. Output: `outputs[].href` → `outputs[].destination.url`
6. Type: `type` → `mediaType`
7. Storage: Removed (not needed for standard URLs)

### Example 2: Complex edit (multiple adjustments)

**V1 Code (3 separate calls):**
```shell
# Call 1
curl -X POST https://image.adobe.io/lrService/autoTone ...

# Call 2
curl -X POST https://image.adobe.io/lrService/autoStraighten ...

# Call 3
curl -X POST https://image.adobe.io/lrService/edit \
  -d '{
    "inputs": {...},
    "options": {
      "Exposure": 1.2,
      "Contrast": 10,
      "Saturation": 15
    },
    "outputs": [...]
  }'
```

**V2 Code (single call):**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<INPUT_URL>"
    }
  },
  "edits": {
    "autoTone": true,
    "autoStraighten": {
      "enabled": true,
      "constrainCrop": true
    },
    "light": {
      "exposure": 1.2,
      "contrast": 10
    },
    "color": {
      "saturation": 15
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

**Key Transformations:**
1. Three calls → One call
2. Operations combined in `edits` object
3. PascalCase params → camelCase within categories
4. `Exposure` → `light.exposure`
5. `Saturation` → `color.saturation`

### Example 3: Format conversion (PSD to JPEG)

**V1 Code:**
```shell
curl -X POST https://image.adobe.io/pie/psdService/renditionCreate \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "https://my-storage.com/document.psd",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "https://my-storage.com/output.jpg",
      "storage": "external",
      "type": "image/jpeg",
      "quality": 7,
      "width": 1920
    }
  ]
}'
```

**V2 Code:**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "https://my-storage.com/document.psd"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "https://my-storage.com/output.jpg"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 1920
    }
  ]
}'
```

**Key Transformations:**
1. Endpoint: `/pie/psdService/renditionCreate` → `/v2/create-composite`
2. Input: `inputs[0].href` → `image.source.url`
3. Output: `outputs[0].href` → `outputs[0].destination.url`
4. Quality: Numeric `7` → String `"maximum"`
5. Storage: Removed (not needed)
6. No `edits` block (just format conversion)

### Example 4: Layer addition

**V1 Code:**
```shell
curl -X POST https://image.adobe.io/pie/psdService/documentOperations \
  -d '{
  "inputs": [{
    "href": "<DOCUMENT_URL>",
    "storage": "external"
  }],
  "options": {
    "layers": [
      {
        "type": "layer",
        "name": "New Image",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<IMAGE_URL>",
          "storage": "external"
        }
      }
    ]
  },
  "outputs": [{
    "href": "<OUTPUT_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

**V2 Code:**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<DOCUMENT_URL>"
    }
  },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "New Image",
        "image": {
          "source": {
            "url": "<IMAGE_URL>"
          }
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

**Key Transformations:**
1. Endpoint: `/documentOperations` → `/create-composite`
2. Structure: `options.layers` → `edits.layers`
3. Add operation: `add: {insertTop: true}` → `operation: {type: "add", placement: {type: "top"}}`
4. Layer source: `input.href` → `image.source.url`

### Example 4b: Layer edit operation

**V1 Code (with edit: \{\}):**
```shell
curl -X POST https://image.adobe.io/pie/psdService/documentOperations \
  -d '{
  "inputs": [{
    "href": "<DOCUMENT_URL>",
    "storage": "external"
  }],
  "options": {
    "layers": [
      {
        "id": 123,
        "type": "layer",
        "edit": {},
        "text": {
          "content": "Updated text"
        }
      }
    ]
  },
  "outputs": [{
    "href": "<OUTPUT_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

**V2 Code (explicit edit operation):**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<DOCUMENT_URL>"
    }
  },
  "edits": {
    "layers": [
      {
        "id": 123,
        "type": "text_layer",
        "text": {
          "content": "Updated text"
        },
        "operation": {
          "type": "edit"
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

**Key Transformations:**
1. Layer type: `type: "layer"` → `type: "text_layer"` (specify actual layer type)
2. Operation: V1 `"edit": {}` → V2 `"operation": {"type": "edit"}`
3. Edit operation is now explicit and required (not implicit)
4. When V1 layer has `"edit": {}` with no add/delete, use edit operation in V2

### Example 5: Action execution

**V1 Code:**
```shell
curl -X POST https://image.adobe.io/pie/psdService/photoshopActions \
  -d '{
  "inputs": [{
    "href": "<IMAGE_URL>",
    "storage": "external"
  }],
  "options": {
    "actions": [
      {
        "href": "<ACTION_FILE_URL>",
        "storage": "external"
      }
    ]
  },
  "outputs": [{
    "href": "<OUTPUT_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

**V2 Code:**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/execute-actions \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<IMAGE_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "url": "<ACTION_FILE_URL>"
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

**Key Transformations:**
1. Endpoint: `/photoshopActions` → `/execute-actions`
2. Input: `inputs[0].href` → `image.source.url`
3. Action: `actions[0].href` → `actions[0].source.url`
4. Storage: Removed from action and input

### Example 6: Status checking

**V1 Code:**
```shell
# Lightroom job
curl -X GET https://image.adobe.io/lrService/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"

# Photoshop job
curl -X GET https://image.adobe.io/pie/psdService/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

**V2 Code:**
```shell
# All jobs use same endpoint
curl -X GET https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

**Key Transformations:**
1. Service-specific endpoints → Unified endpoint
2. Same jobId works for all operation types

### Example 7: Artboard create

**V1 Code:**
```shell
curl -X POST https://image.adobe.io/pie/psdService/artboardCreate \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {"href": "<IMAGE_1_URL>", "storage": "external"},
    {"href": "<IMAGE_2_URL>", "storage": "external"}
  ],
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

**V2 Code:**
```shell
curl -X POST https://photoshop-api.adobe.io/v2/create-artboard \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "images": [
    {"source": {"url": "<IMAGE_1_URL>"}},
    {"source": {"url": "<IMAGE_2_URL>"}}
  ],
  "outputs": [
    {
      "destination": {"url": "<SIGNED_POST_URL>"},
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

**Key Transformations:**
1. Endpoint: `/pie/psdService/artboardCreate` → `/v2/create-artboard`
2. Input: `inputs[]` → `images[]`; `href` + `storage` → `source.url`
3. Output: `outputs[].href` → `outputs[].destination.url`; `type` → `mediaType`
4. Optional: Add `artboardSpacing` (integer, pixels) for horizontal spacing between artboards (default 50)
5. Storage: Omit for standard URLs; use `destination.storageType` only for Azure/Dropbox

## V2 status response output patterns

### Overview

The V2 status response structure varies significantly from V1, particularly in how outputs are represented. Understanding these patterns is crucial for correct migration, as the `result.outputs[]` field structure depends on the destination type specified in the original request.

### Base response structure

All V2 status responses share this base structure regardless of destination type:

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "createdTime": "2025-11-11T10:00:00.000Z",
  "modifiedTime": "2025-11-11T10:05:30.000Z",
  "status": "succeeded",
  "result": {
    "outputs": [...]  // Structure varies by destination type
  }
}
```

### Key structural changes from V1

| V1 Field | V2 Field | Notes |
|----------|----------|-------|
| `created` | `createdTime` | ISO-8601 datetime format |
| `modified` | `modifiedTime` | ISO-8601 datetime format |
| `_links.self.href` | *removed* | No hypermedia links in V2 |
| `outputs` (top-level) | `result.outputs` | Nested inside result object |
| `outputs[].status` | `status` (job-level) | Single status for entire job, not per-output |
| `outputs[]._links` | *removed* | No per-output hypermedia links |
| `outputs[].input` | *removed* | No input echo in outputs |

**Status Values:** `"pending"`, `"running"`, `"succeeded"`, `"failed"`

### Destination type patterns

The `result.outputs[]` structure varies based on the destination type specified in the request. Here are all 5 destination types and their status response patterns:

#### 1. External URL destination (presigned URLs)

**Use Case:** AWS S3, Azure Blob, Dropbox, Frame.io, Google Drive presigned URLs

**Request:**
```json
{
  "outputs": [{
    "destination": {
      "url": "https://s3.amazonaws.com/bucket/output.jpg?X-Amz-Signature=..."
    },
    "mediaType": "image/jpeg",
    "quality": "maximum"
  }]
}
```

**Status Response (succeeded):**
```json
{
  "jobId": "...",
  "createdTime": "2025-11-11T10:00:00.000Z",
  "modifiedTime": "2025-11-11T10:05:30.000Z",
  "status": "succeeded",
  "result": {
    "outputs": [{
      "destination": {
        "url": "https://s3.amazonaws.com/bucket/output.jpg?X-Amz-Signature=..."
      },
      "mediaType": "image/jpeg",
      "quality": "maximum"
    }]
  }
}
```

**Pattern:** The output echoes back the destination URL exactly as provided. The file has been written to the presigned URL.

**V1 vs V2 Comparison:**
```javascript
// V1 Status Response
{
  outputs: [{
    _links: {
      self: { href: "https://s3.amazonaws.com/bucket/output.jpg?..." }
    },
    input: "https://input-url...",
    status: "succeeded"
  }]
}

// V2 Status Response
{
  result: {
    outputs: [{
      destination: { url: "https://s3.amazonaws.com/bucket/output.jpg?..." },
      mediaType: "image/jpeg",
      quality: "maximum"
    }]
  },
  status: "succeeded"  // Job-level, not per-output
}
```

**Key Migration Points:**
- V1: `outputs[]._links.self.href` → V2: `result.outputs[].destination.url`
- V1: Per-output status → V2: Single job-level status
- V1: Includes `input` field → V2: No input echo
- V2: Preserves all output parameters (quality, width, height, etc.)

#### 2. Embedded destination (inline content)

**Use Case:** XMP metadata, JSON manifests, small text outputs returned inline

**Request (embedded: "string"):**
```json
{
  "outputs": [{
    "destination": {
      "embedded": "string"
    },
    "mediaType": "application/rdf+xml"
  }]
}
```

**Status Response:**
```json
{
  "status": "succeeded",
  "result": {
    "outputs": [{
      "destination": {
        "embedded": "string",
        "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<x:xmpmeta xmlns:x=\"adobe:ns:meta/\">...</x:xmpmeta>"
      },
      "mediaType": "application/rdf+xml"
    }]
  }
}
```

**Request (embedded: "json"):**
```json
{
  "outputs": [{
    "destination": {
      "embedded": "json"
    },
    "mediaType": "application/json"
  }]
}
```

**Status Response:**
```json
{
  "result": {
    "outputs": [{
      "destination": {
        "embedded": "json",
        "content": {
          "document": {
            "width": 1920,
            "height": 1080,
            "layers": [...]
          }
        }
      },
      "mediaType": "application/json"
    }]
  }
}
```

**Request (embedded: "base64"):**
```json
{
  "outputs": [{
    "destination": {
      "embedded": "base64"
    },
    "mediaType": "image/png"
  }]
}
```

**Status Response:**
```json
{
  "result": {
    "outputs": [{
      "destination": {
        "embedded": "base64",
        "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
      },
      "mediaType": "image/png"
    }]
  }
}
```

**Pattern:** Destination includes `content` field with actual data inline.

**Embedded Types:**
- `"string"`: Plain text (XMP, XML, text files) - returned as string
- `"json"`: JSON data (manifests, structured data) - returned as parsed JSON object
- `"base64"`: Binary data (small images/files) - returned as base64-encoded string

**V1 vs V2:**
```javascript
// V1: Limited embedded support, varied formats
{
  outputs: [{
    _links: { self: { href: "data:..." } },
    status: "succeeded"
  }]
}

// V2: Standardized embedded format with content field
{
  result: {
    outputs: [{
      destination: {
        embedded: "string",
        content: "<?xml version=..."
      },
      mediaType: "application/rdf+xml"
    }]
  }
}
```

**Important Restrictions:**
- Only use embedded for text/metadata/small file outputs
- Not suitable for large images (use URL or Hosted instead)
- Recommended for XMP extraction and JSON manifests

#### 3. Hosted destination (Adobe temporary storage)

**Use Case:** Temporary storage without managing your own presigned URLs (V2 new feature)

**Request:**
```json
{
  "outputs": [{
    "destination": {
      "validityPeriod": 3600  // seconds: 60-86400 (1 min - 24 hours)
    },
    "mediaType": "image/jpeg",
    "quality": "high"
  }]
}
```

**Status Response:**
```json
{
  "status": "succeeded",
  "result": {
    "outputs": [{
      "destination": {
        "url": "https://adobe-hosted-storage.example.com/path/to/output.jpg?expires=1699700000&signature=abc123..."
      },
      "mediaType": "image/jpeg",
      "quality": "high"
    }]
  }
}
```

**Pattern:** Adobe generates a temporary presigned URL valid for the specified period (max 24 hours). The URL is returned in `destination.url`.

**Key Characteristics:**
- Adobe manages the storage temporarily
- URL includes expiration timestamp and signature
- Files automatically deleted after expiration
- Maximum validity period: 86400 seconds (24 hours)
- Minimum validity period: 60 seconds (1 minute)

**CRITICAL:** Download the file before the URL expires! No recovery after expiration.

**V1 Equivalent:** None - this is a new V2 feature.

**Use Cases:**
- Temporary processing workflows
- Quick prototyping
- No long-term storage needed
- Simplifies workflows by eliminating presigned URL generation

#### 4. Creative Cloud destination

**Use Case:** Direct integration with Creative Cloud storage (ACP - Adobe Content Platform)

**Request:**
```json
{
  "outputs": [{
    "destination": {
      "creativeCloudPath": "my-folder/output.jpg"
    },
    "mediaType": "image/jpeg",
    "quality": "maximum"
  }]
}
```

**Status Response:**
```json
{
  "status": "succeeded",
  "result": {
    "outputs": [{
      "destination": {
        "creativeCloudPath": "my-folder/output.jpg"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum"
    }]
  }
}
```

**Pattern:** The output echoes back the Creative Cloud path. File has been written to CC storage (ACP).

**Alternative: Creative Cloud File ID**
```json
// Request
{
  "destination": {
    "creativeCloudFileId": "urn:aaid:sc:VA6C2:...",
    "creativeCloudProjectId": "urn:aaid:sc:VA6C2:..."  // Optional
  }
}

// Status Response
{
  "destination": {
    "creativeCloudFileId": "urn:aaid:sc:VA6C2:...",
    "creativeCloudProjectId": "urn:aaid:sc:VA6C2:..."
  }
}
```

**V1 vs V2:**
```javascript
// V1 Status Response (CC storage)
{
  outputs: [{
    _links: {
      self: {
        href: "my-folder/output.jpg",
        storage: "external"
      }
    },
    status: "succeeded"
  }]
}

// V2 Status Response (CC storage)
{
  result: {
    "outputs": [{
      destination: {
        creativeCloudPath: "my-folder/output.jpg"
      },
      mediaType: "image/jpeg"
    }]
  },
  status: "succeeded"
}
```

**When to Use:**
- Integration with Creative Cloud ecosystem and ACP
- Direct access to user's CC files
- Collaboration workflows
- Seamless CC workflow integration

#### 5. Script output pattern (dynamic file discovery)

**Use Case:** UXP scripts that generate files dynamically (V2 new feature, `/v2/execute-actions` only)

**Request with glob pattern:**
```json
{
  "outputs": [{
    "destination": {
      "validityPeriod": 3600
    },
    "mediaType": "application/json",
    "scriptOutputPattern": "*.json"  // Matches any JSON files
  }]
}
```

**Status Response when script generates 3 JSON files:**
```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "destination": {
          "url": "https://adobe-hosted.../fonts.json?expires=..."
        },
        "mediaType": "application/json"
      },
      {
        "destination": {
          "url": "https://adobe-hosted.../layers.json?expires=..."
        },
        "mediaType": "application/json"
      },
      {
        "destination": {
          "url": "https://adobe-hosted.../metadata.json?expires=..."
        },
        "mediaType": "application/json"
      }
    ]
  }
}
```

**Pattern:** One request output with pattern expands to multiple status response outputs (one per matched file).

**Exact filename match:**
```json
{
  "scriptOutputPattern": "document-info.json"  // Exact match
}
// Status: Single output with that specific file
```

**Glob patterns supported:**
- `*.json` - All JSON files generated by script
- `result-*.png` - Files matching pattern (result-1.png, result-2.png, etc.)
- `data-*.txt` - Pattern with wildcard
- `document-info.json` - Exact filename (no glob)

**Pattern Expansion Examples:**

1 request output → 1 status output (exact match):
```json
// Request
{"scriptOutputPattern": "metadata.json"}

// Status
{"outputs": [{"destination": {"url": ".../metadata.json?..."}}]}
```

1 request output → 3 status outputs (glob match):
```json
// Request
{"scriptOutputPattern": "*.json"}

// Status (if 3 JSON files generated)
{"outputs": [
  {"destination": {"url": ".../file1.json?..."}},
  {"destination": {"url": ".../file2.json?..."}},
  {"destination": {"url": ".../file3.json?..."}}
]}
```

**Restrictions:**
- Only works with **Hosted** or **Embedded** destinations
- Cannot use with **URL** or **Creative Cloud** destinations (require pre-known filenames)
- Only applicable to `/v2/execute-actions` endpoint
- Files are filtered by `mediaType` - only matching extensions included
- Not applicable to `/v2/edit`, `/v2/create-composite`, or other endpoints

**MediaType Filtering:**
If `mediaType: "application/json"`, only files with `.json` extension are included, even if pattern matches others.

**V1 Equivalent:** None - this is a new V2 feature for UXP script workflows.

**Use Cases:**
- UXP scripts that generate unknown number of files
- Scripts that output dynamic filenames
- Batch processing where file count varies
- Discovery of script-generated assets

### Multiple outputs example

When multiple outputs with different destinations are requested:

**Request:**
```json
{
  "outputs": [
    {
      "destination": {"url": "https://s3.../output.jpg?..."},
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2400
    },
    {
      "destination": {"embedded": "json"},
      "mediaType": "application/json"
    },
    {
      "destination": {"creativeCloudPath": "folder/output.png"},
      "mediaType": "image/png",
      "compression": "high"
    },
    {
      "destination": {"validityPeriod": 7200},
      "mediaType": "image/tiff"
    }
  ]
}
```

**Status Response:**
```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "destination": {"url": "https://s3.../output.jpg?..."},
        "mediaType": "image/jpeg",
        "quality": "maximum",
        "width": 2400
      },
      {
        "destination": {
          "embedded": "json",
          "content": {"document": {"width": 1920, "height": 1080}}
        },
        "mediaType": "application/json"
      },
      {
        "destination": {"creativeCloudPath": "folder/output.png"},
        "mediaType": "image/png",
        "compression": "high"
      },
      {
        "destination": {"url": "https://adobe-hosted.../output.tiff?expires=..."},
        "mediaType": "image/tiff"
      }
    ]
  }
}
```

**Pattern:** Each output maintains its destination type and parameters. Outputs array order is preserved.

### Failed job response

When job fails, no `result` field is present:

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "createdTime": "2025-11-11T10:00:00.000Z",
  "modifiedTime": "2025-11-11T10:05:35.000Z",
  "status": "failed",
  "errorDetails": [
    {
      "errorCode": "400401",
      "message": "The value provided is not valid."
    },
    {
      "errorCode": "400420",
      "message": "Required fields missing on the API request."
    }
  ]
}
```

**Pattern:** Failed jobs have `errorDetails` array instead of `result` object.

### Pending/running job response

While job is processing, `result` field may be absent or incomplete:

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "createdTime": "2025-11-11T10:00:00.000Z",
  "modifiedTime": "2025-11-11T10:00:15.000Z",
  "status": "running"
}
```

**Pattern:** No `result` field until job completes. Poll endpoint until status is `"succeeded"` or `"failed"`.

**Recommended polling interval:** 5 seconds

### V1 to V2 status response quick reference table

| Request Destination Type | V1 Status Response | V2 Status Response | Status Field Location |
|--------------------------|-------------------|--------------------|----------------------|
| External URL (S3, Azure, etc.) | `outputs[]._links.self.href: "<URL>"` | `result.outputs[].destination.url: "<URL>"` | `result.outputs[].destination.url` |
| Embedded (string/json/base64) | Limited/Not standard | `result.outputs[].destination.{embedded, content}` | `result.outputs[].destination.content` |
| Hosted (Adobe temp storage) | N/A (V2 new feature) | `result.outputs[].destination.url: "<TEMP_URL>"` | `result.outputs[].destination.url` |
| Creative Cloud Path | `outputs[]._links.self.href: "path/to/file"` | `result.outputs[].destination.creativeCloudPath: "path/to/file"` | `result.outputs[].destination.creativeCloudPath` |
| Creative Cloud File ID | `outputs[]._links.self.href: "urn:aaid:..."` | `result.outputs[].destination.creativeCloudFileId: "urn:aaid:..."` | `result.outputs[].destination.creativeCloudFileId` |
| Script Pattern (glob) | N/A (V2 new feature) | Expands to multiple outputs, one per matched file | Multiple `result.outputs[]` entries |

### Key migration insights

**1. Response Structure Mirror:**
In V2, the status response `result.outputs[]` structure directly mirrors the request `outputs[]` structure:
- Request fields are echoed back (mediaType, quality, width, etc.)
- Destination details are preserved or enhanced (URL for hosted, content for embedded)
- No additional `_links` or `input` fields added

**2. Status Location:**
- V1: Per-output status (`outputs[].status`)
- V2: Single job-level status (`status` at root)

**3. Hypermedia Links:**
- V1: Extensive `_links` objects throughout
- V2: No hypermedia links - direct data structures only

**4. Destination Determination:**
The destination type in status response is determined by request:
- Request has `url` → Response has `url` (external or hosted-generated)
- Request has `embedded` → Response has `embedded` + `content`
- Request has `creativeCloudPath` → Response has `creativeCloudPath`
- Request has `scriptOutputPattern` + hosted → Response has multiple `url` entries

**5. Output Array Expansion:**
Only `scriptOutputPattern` causes output expansion (1 request → N response outputs). All other destination types maintain 1:1 mapping.

### Migration validation points

When migrating status polling code:

**Update field references:**
- `data.created` → `data.createdTime`
- `data.modified` → `data.modifiedTime`
- `data.outputs` → `data.result.outputs`
- `data.outputs[0]._links.self.href` → `data.result.outputs[0].destination.url` (or appropriate field)

**Update status checking:**
- V1: Loop through `outputs[]` checking each `output.status`
- V2: Check single `status` field at root level

**Remove hypermedia logic:**
- V1: Navigate via `_links.self.href`
- V2: Access `result.outputs[]` directly

**Handle destination types:**
- Check `destination.url` for external/hosted
- Check `destination.content` for embedded
- Check `destination.creativeCloudPath` for CC
- Handle multiple outputs for scriptOutputPattern

**Error handling:**
- V1: Check `outputs[].status` for errors
- V2: Check `status === "failed"` and parse `errorDetails[]` array

## Validation checklist

Use this checklist when migrating or validating V1 → V2 code:

### Request structure
- [ ] Base URL updated to `photoshop-api.adobe.io`
- [ ] Endpoint path updated (see mapping table)
- [ ] `inputs[].href` changed to `image.source.url`
- [ ] `options` changed to `edits` (if applicable)
- [ ] `outputs` array present and properly configured
- [ ] `outputs[].href` changed to `outputs[].destination.url`
- [ ] `outputs[].type` changed to `outputs[].mediaType`
- [ ] `storage` parameter removed or changed to `storageType` (only for Azure/Dropbox)

### Edit operations specific
- [ ] Multiple V1 calls consolidated into single V2 call
- [ ] Parameters moved to category objects (`light`, `color`, `effects`)
- [ ] Parameter names changed from PascalCase to camelCase
- [ ] `autoTone` specified as boolean `true`
- [ ] `autoStraighten` specified as object with `enabled: true`
- [ ] XMP inline string converted to file reference (`edits.xmp.source`)
- [ ] Masks moved from `options.masks` to `edits.xmp.masks`
- [ ] Mask structure changed from `href` + `storage` to `source.url`
- [ ] Each mask includes both `source` and `digest`
- [ ] XMP orientation (if used) nested inside `xmp` object, not at `edits` level
- [ ] Orientation uses string values (e.g., `"right_top"`) not numeric codes

### Layer operations specific
- [ ] Layer type names use underscores (`text_layer`, `adjustment_layer`, `smart_object_layer`, `solid_color_layer`)
- [ ] Group layer type is `"group_layer"` (not `"layer_group"` or `"layerSection"`). Creating a new document with a group layer is not yet supported (upcoming feature); editing an existing document to add a layer inside a group layer is supported (`into` + `referenceLayer`).
- [ ] Operation type specified (`add`, `edit`, `delete`) — `operation` field is **required** for edits, not inferred
- [ ] Move operations use `operation.type: "move"` with `placement` (not `move: {...}`)
- [ ] V1 layers with `edit: {}` and no add/delete → V2 with `operation.type: "edit"`
- [ ] Placement structure uses `operation.placement` format
- [ ] Relative placement uses `referenceLayer` (not `relativeTo`)
- [ ] Layer processing order is top-down in V2 (not bottom-up); layers used as `referenceLayer` must appear earlier in the array
- [ ] Layer source uses `source` not `input`
- [ ] Layer lock uses `"protection": ["all"]` / `["none"]` (not `"locked": true/false`)
- [ ] Clipping mask: use `"isClipped": true` at layer level (not `mask.clip`)
- [ ] Pixel mask: rename `mask` → `pixelMask`; offset uses `offset.horizontal`/`offset.vertical` (not `offset.x`/`offset.y`)
- [ ] Pixel mask delete: use `pixelMask: { "delete": true }` on edit operations to remove a mask from a layer
- [ ] Text layers: characterStyles wrapped in `characterStyle` object
- [ ] Text layers: paragraphStyles wrapped in `paragraphStyle` object
- [ ] Pixel mask offset uses `offset.horizontal`/`offset.vertical` (not `offset.x`/`offset.y`)
- [ ] Pixel mask: V1 `mask.linked`/`mask.enabled` → V2 `mask.isLinked`/`mask.isEnabled`; source is `mask.source.url` (not `mask.input.href`)
- [ ] Visibility: `visible` → `isVisible`
- [ ] Opacity/blend mode: for most layer types, top-level `opacity` and `blendMode` (not `blendOptions`); for `smart_object_layer`, use `blendOptions.opacity` and `blendOptions.blendMode`
- [ ] Layer transforms: V1 `bounds {left,top,width,height}` → V2 `transform {offset:{horizontal,vertical}, dimension:{width,height}}`; `transformMode: "custom"` is required
- [ ] Alignment: V1 layer-level `horizontalAlign`/`verticalAlign` → V2 placement-level `horizontalAlignment`/`verticalAlignment` within `placement: {type: "custom", ...}` (add/move only)

### Adjustment layer operations specific
- [ ] Layer type: `"adjustmentLayer"` → `"adjustment_layer"`
- [ ] `adjustments.type` discriminant **required** in V2 (did not exist in V1): `"brightness_contrast"`, `"exposure"`, `"hue_saturation"`, `"color_balance"` (also new: `"curves"`, `"levels"`, `"gradient_map_custom_stops"`)
- [ ] Inside the `exposure` payload: field `exposure` (amount) renamed to `exposureValue`
- [ ] Hue/Sat: V1 `channels[]` with `channel: "master"` → V2 `hueSaturationAdjustments[]`; omit `localRange` for master; include `localRange` with `channelId` for specific color range — only when `colorize: false`
- [ ] `transformMode` is not applicable to adjustment layers — omit it

### Text layer operations specific
- [ ] Layer type: `"textLayer"` → `"text_layer"`
- [ ] Character/paragraph style range: V1 `to` = length → V2 `apply.to` = inclusive end index; **subtract 1 from V1's `to`** when migrating
- [ ] Style properties wrapped in `characterStyle` object (V2); `apply: {from, to}` is the range wrapper
- [ ] Font name: V1 top-level `fontName` → V2 `characterStyle.font.postScriptName` (inside `characterStyle.font`)
- [ ] Paragraph styles wrapped in `paragraphStyle` object (V2)
- [ ] Text bounds: V1 layer-level `bounds {left,top,width,height}` → V2 `text.frame {type:"area", bounds:{top,left,right,bottom}}`; `right=left+width`, `bottom=top+height`
- [ ] Point frames: use `text.frame: {type:"point", origin:{x,y}}` for single-point text
- [ ] V2 default (no frame): point at canvas center — always set `text.frame` explicitly
- [ ] `textOrientation` is text-level property (not per character-style)
- [ ] Font options: `options.fonts` (href+storage) → `fontOptions.additionalFonts` (source.url); `options.globalFont` → `fontOptions.defaultFontPostScriptName`; `manageMissingFonts:"useDefault"` → `missingFontStrategy:"use_default"`

### Smart object layer operations specific
- [ ] Layer type: `"smartObject"` → `"smart_object_layer"`
- [ ] Source: V1 `input: {href, storage}` → V2 `smartObject.smartObjectFile.source.url`
- [ ] Linked flag: `smartObject.linked` → `smartObject.isLinked`
- [ ] `transformMode` required when using `transform` object: `"none"`, `"custom"`, `"fit"`, or `"fill"`
- [ ] V2 supports SVG source files (V1 did not)
- [ ] Width-only resize: linked SOs are rasterized to pixel layers unless their content is provided in the same request

### Text endpoint migration specific (`/pie/psdService/text`)
- [ ] No declarative text endpoint exists in V2 — use `/v2/execute-actions`
- [ ] Choose ActionJSON for fixed edits on known layers; choose UXP for conditional/iterative logic
- [ ] ActionJSON must be stringified; include `contentType: "application/json"`
- [ ] UXP: use `core.executeAsModal()` for document modifications; include `contentType: "application/javascript"`

### Action operations specific
- [ ] Actions use `source` object not `href`
- [ ] ActionJSON is stringified (not array/object)
- [ ] `contentType` specified for inline content
- [ ] Additional contents use correct field name (`additionalContents`, not `additionalImages`)
- [ ] Additional contents placeholder format is `__ADDITIONAL_CONTENTS_PATH_0__` (not `__ADDITIONAL_IMAGES_0__`)
- [ ] `additionalContents` max count is 25 (not 10)
- [ ] UXP script uses object syntax for `options.uxp` (not array)
- [ ] UXP script output paths use `plugin-temp:/filename.ext` (not `__UXP_OUTPUT_PATH__`)
- [ ] Script output destination uses `{"validityPeriod": 3600}` (not `{"hosted": true}` for scriptOutputPattern)

### Artboard operations specific
- [ ] `inputs[]` changed to `images[]` with `source` object
- [ ] Each image has `source` with valid reference (url, creativeCloudPath, creativeCloudFileId, or lightroomPath)
- [ ] Image count between 1 and 25
- [ ] Output count between 1 and 25
- [ ] `artboardSpacing` (if used) is integer in pixels
- [ ] Output structure uses `destination.url` and `mediaType` (not href/type)

### Storage configuration
- [ ] Correct storage type for use case selected
- [ ] `storageType` only used for Azure and Dropbox
- [ ] Embedded storage only used for XMP/JSON outputs
- [ ] Hosted storage has `validityPeriod` (60-86400 seconds)
- [ ] Creative Cloud paths have no leading slash (use `"my-folder/file.psd"` not `"/my-folder/file.psd"`)

### Output configuration
- [ ] `outputs[].href` changed to `outputs[].destination.url`
- [ ] `outputs[].type` changed to `outputs[].mediaType`
- [ ] `outputs[].storage` removed or changed to `storageType` (only for Azure/Dropbox)
- [ ] Media type is correct for output format
- [ ] Multiple outputs don't exceed limit (25)
- [ ] Embedded storage not used for images

### Output configuration: JPEG specific
- [ ] Quality uses string enum not numeric (e.g., `"maximum"` not `7`)
- [ ] Quality value mapped correctly: 7 → `"maximum"`, 5-6 → `"high"`, 3-4 → `"medium"`, 1-2 → `"low"`
- [ ] Using `quality` parameter (not `compression`)

### Output configuration: PNG specific
- [ ] Compression uses V2 enum not V1 values (e.g., `"maximum"` not `"small"`)
- [ ] Compression value mapped: "small" → `"maximum"`, "medium" → `"medium"`, "large" → `"low"`
- [ ] Using `compression` parameter (not `quality`)

### Output configuration: PSD/TIFF specific
- [ ] No quality or compression parameters included
- [ ] Correct mediaType: `"image/vnd.adobe.photoshop"` or `"image/tiff"`
- [ ] Only structural field changes applied

### Document creation specific
- [ ] `resolution` is an object `{"unit": "density_unit", "value": 72}` (not an integer)
- [ ] `depth` is an integer (e.g., `8`) not a string (e.g., `"8"`)
- [ ] Color mode `"grayscale"` used (not `"gray"`)
- [ ] `fill: "backgroundColor"` (V1 camelCase) → `fill: "background_color"` (V2 snake_case); camelCase is rejected in V2
- [ ] `fill` object form (V2): `{"solidColor": {"red": N, "green": N, "blue": N}}` for custom color
- [ ] `depth` value is mode-dependent: `bitmap`→1 only; `grayscale`/`rgb`/`hsb`→8,16,32; `cmyk`/`lab`/`multichannel`→8,16; `indexed`/`duotone`→8 only

### Export layers specific
- [ ] `cropMode` `layer_bounds` only used for single-layer export; `trim_to_transparency` and `document_bounds` work for all export types
- [ ] Multi-layer export does not request PSD format (use JPEG, PNG, or TIFF)
- [ ] Default JPEG quality is `photoshop_max` if omitted; default PNG compression is `default` (level 6)

### ICC profile specific
- [ ] `iccProfile` not used with PSDC outputs (remove or switch to another format)
- [ ] Standard profile names match exactly (including spaces and punctuation)
- [ ] CMYK output requires custom ICC profile (not standard)
- [ ] `imageMode` set correctly (`"rgb"`, `"grayscale"`, or `"cmyk"` for custom)

### Status checking
- [ ] Status endpoint uses v2 path
- [ ] Handling all status values (pending, running, succeeded, failed)
- [ ] Error details handled as array
- [ ] Polling with appropriate interval (5 seconds recommended)
- [ ] Timeout handling implemented

### Authentication
- [ ] Same OAuth token used (no change needed)
- [ ] Authorization header present
- [ ] x-api-key header present

## LLM interaction guidelines

### When users ask "How do I migrate X endpoint?"

1. **Identify the V1 endpoint category:**
   - Is it Lightroom (`/lrService/*`)? → Edit Operations
   - Is it PSD operations (`/pie/psdService/*`)? → Determine specific type
   - Is it actions? → Actions Migration
   - Is it status? → Status Migration

2. **Provide the V2 equivalent:**
   - Show endpoint mapping from Quick Reference
   - Explain the new endpoint purpose

3. **Show code transformation:**
   - Complete V1 example
   - Complete V2 equivalent
   - Highlight key differences

4. **Link to detailed guide:**
   - Reference specific migration guide section

### When users ask "My V1 code does Y, how do I do that in V2?"

1. **Analyze the V1 pattern:**
   - What operation is being performed?
   - What parameters are being used?
   - What output format is expected?

2. **Map to V2 operation type:**
   - Use Decision Tree to determine correct endpoint
   - Identify required vs optional parameters

3. **Provide equivalent V2 code:**
   - Complete working example
   - Preserve user's specific values
   - Show parameter name mappings

4. **Suggest improvements:**
   - Can operations be batched?
   - Better storage option available?
   - New capabilities that might help?

### When users ask "What storage should I use for Z?"

1. **Analyze the use case:**
   - What type of output? (image, metadata, temporary)
   - What's the workflow? (production, prototype, CC integration)
   - How long do files need to persist?

2. **Apply decision matrix:**
   - Use Storage Decision Matrix
   - Consider file size and type
   - Consider infrastructure

3. **Recommend storage type:**
   - Provide specific example
   - Explain benefits for this use case
   - Warn about limitations

### When users report "I'm getting error X in v2"

1. **Match to common issues:**
   - Check Common Migration Issues section
   - Identify error category

2. **Explain root cause:**
   - Why is this happening?
   - What changed from V1?

3. **Provide solution:**
   - Show incorrect code
   - Show correct code
   - Explain the difference

4. **Show correct pattern:**
   - Complete working example
   - Related validation checklist items

### Question type examples

**"How do I migrate /lrService/autoTone?"**

Response should include:
1. V2 endpoint: `/v2/edit`
2. Side-by-side code comparison
3. Key changes highlighted
4. Link to Edit Operations guide

**"I want to add text to a PSD"**

Response should include:
1. Use `/v2/create-composite`
2. Show `edits.layers` with `text_layer` type
3. Complete example with character/paragraph styles
4. Link to Text Layer Operations guide

**"What's the V2 equivalent of productCrop?"**

Response should include:
1. Use `/v2/execute-actions`
2. Explain published action files
3. Show ActionJSON content
4. Option to customize
5. Link to Actions guide

**"How do I get the manifest data immediately?"**

Response should include:
1. Use embedded storage
2. Show `embedded: "json"` configuration
3. Explain response format
4. Warn: Only for metadata/JSON outputs

## Appendix: Common error codes

| Error Code | Description | Common Cause | Solution |
|------------|-------------|--------------|----------|
| 400400 | Invalid JSON in request payload | Malformed JSON | Validate JSON syntax |
| 400401 | Invalid value provided | Wrong parameter value/type | Check parameter documentation |
| 400410 | Required fields missing | Missing required field | Add required fields (e.g., outputs array) |
| 400411 | Request blocked by content filters | Inappropriate content | Review content policies |
| 400420 | Required fields missing on API request | Missing critical parameter | Check all required fields present |
| 403401 | User not authorized | Invalid/expired token | Refresh access token |
| 403421 | Quota exhausted | API limits exceeded | Check quota, upgrade plan |
| 404 | Job not found | Invalid jobId | Verify jobId is correct |
| 422404 | Unable to process outputs | Output destination issue | Check output URLs, storage permissions |
| 500600 | Internal server error | Server-side issue | Retry request, contact support if persists |

## Quick command reference

### Complete migration example

**V1 (Multiple Calls):**
```shell
# Call 1: Auto tone
curl -X POST https://image.adobe.io/lrService/autoTone \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -d '{"inputs": {"href": "<URL>"}, "outputs": [...]}'

# Call 2: Status check
curl -X GET https://image.adobe.io/lrService/status/{jobId1} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"

# Call 3: Apply edits
curl -X POST https://image.adobe.io/lrService/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -d '{"inputs": {"href": "<URL>"}, "options": {...}, "outputs": [...]}'

# Call 4: Status check
curl -X GET https://image.adobe.io/lrService/status/{jobId2} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

**V2 (Single Call):**
```shell
# Single combined request
curl -X POST https://photoshop-api.adobe.io/v2/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<INPUT_URL>"
    }
  },
  "edits": {
    "autoTone": true,
    "light": {
      "exposure": 1.2,
      "contrast": 10
    },
    "color": {
      "saturation": 15
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high"
    }
  ]
}'

# Single status check
curl -X GET https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

## Document version

**Version:** 1.14
**Created:** October 29, 2025

**Coverage:**
- All migration guides consolidated
- Artboard migration: images/source structure, artboardSpacing, validation rules, common issues
- Execute-actions migration: ActionJSON stringification, additionalContents rename, resource limits
- Complete endpoint mappings (depth blur marked not yet supported)
- Storage options reference (with ACP clarification, no leading slash in CC paths)
- Common issues and solutions
- Code transformation examples
- Validation checklists
- LLM interaction patterns
- v2-whats-new.md: reorganized API-first — execute-actions (UXP script execution, UXP adhoc file output via scriptOutputPattern, published action files), generate-manifest (artboard type, smart object extraction, rich layer metadata), create-composite (smart object reworked API + SVG support, linked smart objects including resize, text rendering engine + new character styles, group layers, ICC profiles); architectural improvements (TODOs); storage options callout; dropped granular protection, multiple outputs, atomic multi-op sections
- v2-api-catalog.md: complete per-endpoint behavioral comparison with breaking changes checklist
- XMP with Masks migration patterns (V1 → V2)
- XMP with Orientation override (V2 new capability)
- Creative Cloud Storage (ACP) clarifications
- Layer processing order (V2 top-down, V1 bottom-up)
- `additionalContents` / `__ADDITIONAL_CONTENTS_PATH_0__` (replaces `additionalImages`)
- UXP object syntax and `plugin-temp:/` output path
- `scriptOutputPattern` hosted destination (`{"validityPeriod": 3600}`)
- `resolution` object format, integer `depth`, `"grayscale"` mode name
- `protection` array replaces `locked`/`isLocked`; `group_layer` type
- `operation.type: "edit"` required (not inferred)
- `referenceLayer` (not `relativeTo`) for relative placement
- Pixel mask: `pixelMask`, `offset.horizontal`/`offset.vertical`, `userMask`, `isClipped`, `pixelMask.delete` for removal (all edit layer types)
- Font color value ranges: rgb/cmyk/gray 0–32768, lab `l` 0–32768 / `a`,`b` -16384–16384
- Export layers: `cropMode` (all export types; `layer_bounds` single-layer only), PSD restriction, defaults
- ICC profile support: standard/custom profiles, CMYK via custom, PSDC restriction
- Color mode and bit depth validation tables by export path
- Cloud PSD mediaType `document/vnd.adobe.cpsd+dcxucf`
- Manifest response format changes: layer type renames (including `background_layer`, no `typeAttributes` on background entries), bounds format, thumbnail object, artboard `layers[]` key, document field renames
- Composite API V1→V2 complete field-level diff (all 4 V1 endpoints, all 7 layer types, output formats)
- Artboard API V1→V2 complete field-level diff (input restructure, storage mapping, quality/compression enums, crop mode, status response)
- Adjustment layer operations: `adjustments.type` discriminant required, type mapping table, `exposureValue` rename, hue/sat `hueSaturationAdjustments[]` restructure, `localRange`, parameter ranges, `transformMode` not applicable
- Text layer operations: character style range off-by-one (V1 `to`=length → V2 `apply.to`=inclusive end index), `font.postScriptName`, `text.frame` area/point types, bounds conversion, font options rename, `textOrientation`
- Smart object operations: `smartObject.smartObjectFile.source.url` path, `isLinked`, resize-with-linked-SO rasterization behavior, SVG support
- `/pie/psdService/text` migration: no declarative V2 equivalent; use `execute-actions` with ActionJSON (fixed edits) or UXP (conditional/iterative); decision table
- Blend mode location: top-level `opacity`/`blendMode` for most layers; `blendOptions` for `smart_object_layer`
- Layer transforms: V1 `bounds` → V2 `transform {offset, dimension}` with required `transformMode: "custom"`
- Alignment: V1 layer-level → V2 placement-level `horizontalAlignment`/`verticalAlignment` with `placement.type: "custom"`
- Document creation `fill` rename: `"backgroundColor"` → `"background_color"`; object form `{solidColor:{...}}`; depth-by-mode table

**For Updates:**
For questions, contact Firefly Services Support or refer to the official migration guides in this documentation.

## Composite API (`/v2/create-composite`) — key breaking changes reference

This section consolidates the highest-impact breaking changes across all four V1 composite-family
endpoints (`documentCreate`, `documentOperations`, `renditionCreate`, `smartObject`).

For the complete authoritative field-level diff, see
[Create Composite V1 Reference](create-composite-v1-reference.md).

### V1 endpoint to V2 mapping

All four V1 endpoints map to `POST /v2/create-composite`.

| V1 Endpoint | Purpose |
|---|---|
| `documentCreate` | Create new blank PSD |
| `documentOperations` | Document ops + layer manipulation |
| `renditionCreate` | Export to JPEG/PNG/PSD/TIFF |
| `smartObject` | Smart object operations |

### Top-level request envelope

| V1 | V2 |
|---|---|
| `inputs[].href` + `storage` | `image.source.url` |
| `options.document.*` | `image.*` (top-level) |
| `options.layers[]` | `edits.layers[]` |
| `options.*` (doc ops) | `edits.document.*` |
| `outputs[].href` | `outputs[].destination.url` |
| `outputs[].type` | `outputs[].mediaType` |

**Layer processing order:** V1 = bottom-up (last first); V2 = top-down (first first). Referenced
layers must appear earlier in the array in V2.

### Layer type renames

| V1 `type` | V2 `type` |
|---|---|
| `"adjustmentLayer"` | `"adjustment_layer"` |
| `"backgroundLayer"` | `"background_layer"` (manifest response only; cannot create in edits) |
| `"fillLayer"` | `"solid_color_layer"` |
| `"layer"` | `"layer"` (unchanged) |
| `"layerSection"` | `"group_layer"` |
| `"smartObject"` | `"smart_object_layer"` |
| `"textLayer"` | `"text_layer"` |

### Common layer property changes

| V1 | V2 | Impact |
|---|---|---|
| `locked: true/false` | `protection: ["all"]/["none"]` | Breaking |
| `visible` | `isVisible` | Breaking |
| `blendOptions.opacity` | `opacity` (top-level) | Breaking: de-nested |
| `blendOptions.blendMode` | `blendMode` (top-level) | Breaking: de-nested |
| `bounds: {left, top, width, height}` | `transform: {offset: {horizontal, vertical}, dimension: {width, height}}` | Breaking |
| `mask.clip: true` | `isClipped: true` (top-level) | Breaking |
| `mask.linked`/`enabled`/`input` | `mask.isLinked`/`isEnabled`/`source.url` | Breaking |
| `fillToCanvas: true` | **Not supported** | Feature gap |

### Text layer critical changes

| Change | V1 | V2 |
|---|---|---|
| Character style range field | `from`, `to` direct on item | `apply.from`, `apply.to` |
| `to` semantics | **Length** | **Inclusive end index** (off-by-one!) |
| Font name | `fontName: "PSName"` | `characterStyle.font.postScriptName` |
| Style wrapping | Direct properties | Inside `characterStyle: {...}` |
| Paragraph style wrapping | Direct properties | Inside `paragraphStyle: {...}` |
| Text frame bounds | Layer-level `bounds` | `text.frame.type: "area"` with `{top, left, right, bottom}` |
| Default frame | Area at (0,0,4,4) | Point frame at canvas center |
| Font options | `options.fonts`, `options.globalFont`, `options.manageMissingFonts` | `fontOptions.additionalFonts`, `.defaultFontPostScriptName`, `.missingFontStrategy` |
| Missing font strategy | `"useDefault"` | `"use_default"` (Breaking: underscore) |

#### Font color value ranges

All `fontColor` components use 16-bit integer values:

| Color Model | Components | Range | Notes |
|---|---|---|---|
| `rgb` | `red`, `green`, `blue` | 0–32768 | 16-bit unsigned |
| `cmyk` | `cyan`, `magenta`, `yellow`, `black` | 0–32768 | 16-bit unsigned |
| `lab` | `l` | 0–32768 | Lightness, 16-bit unsigned |
| `lab` | `a`, `b` | -16384–16384 | 16-bit signed |
| `gray` | `gray` | 0–32768 | 16-bit unsigned|

All components are required and default to `0` when omitted. Usage: `fontColor.rgb`, `fontColor.cmyk`, `fontColor.lab`, `fontColor.gray`.

### Adjustment layer critical changes

| Change | V1 | V2 |
|---|---|---|
| `adjustments.type` | **Not present** (type inferred from key) | **Required** — snake_case enum |
| `brightnessContrast` type | *(implicit)* | `type: "brightness_contrast"` |
| `hueSaturation` type | *(implicit)* | `type: "hue_saturation"` |
| `colorBalance` type | *(implicit)* | `type: "color_balance"` |
| Exposure amount field | `exposure.exposure` | `exposure.exposureValue` |

### Output format changes

| Feature | V1 | V2 |
|---|---|---|
| JPEG quality | Numeric 1–7 | String enum: `"low"`, `"medium"`, `"high"`, `"maximum"`, `"photoshop_max"` |
| PNG compression | `"small"`, `"medium"`, `"large"` | `"maximum"`, `"medium"`, `"low"` (and more) |
| Storage: external | `"storage": "external"` | `destination: {url: "..."}` |
| Storage: CC | `"storage": "adobe"` | `destination: {creativeCloudPath: "..."}` |
| ICC profile | Not supported | `iccProfile` on output (new) |
| Hosted storage | Not supported | `destination: {validityPeriod: N}` (new) |

### Features missing in V2

| Feature | Notes |
|---|---|
| `fillToCanvas` | Not supported |
| `background_layer` create/edit | Not supported (manifest returns `background_layer` for document background) |
| Canvas size adjustment | Coming soon |
| Image rotation | Coming soon |
| Trim by color | Not supported |
| TIFF output | Status unclear |

## Artboard API (`/v2/create-artboard`) — key breaking changes reference

For the complete authoritative field-level diff, see
[Create Artboard V1 Reference](create-artboard-v1-reference.md).

### Endpoint

| V1 | V2 |
|---|---|
| `POST /pie/psdService/artboardCreate` | `POST /v2/create-artboard` |
| `https://image.adobe.io` | `https://photoshop-api.adobe.io` |

### Request envelope (breaking change)

<InlineAlert variant="warning" slots="text"/>

**V1 input was `options.artboard[]`, not `inputs[]`.** The existing artboard-migration.md guide shows an incorrect V1 example using `inputs[]`. The actual V1 schema used `options.artboard[]`. The complete `options` wrapper is removed in V2.

| V1 | V2 |
|---|---|
| `options.artboard[n].href` + `storage` | `images[n].source.url` |
| `options` container | Removed entirely |
| Max images: undocumented | Max images: **25** (enforced) |
| *(not in V1)* | `artboardSpacing` (integer pixels, default 50) |

### Input storage mapping

| V1 `storage` | V2 `source` field |
|---|---|
| `"external"` | `source.url` |
| `"adobe"` (CC path) | `source.creativeCloudPath` (no leading slash) |
| `"adobe"` (URN) | `source.creativeCloudFileId` |
| `"acp"` | `source.url` |
| `"azure"` | `source.url` |
| `"dropbox"` | `source.url` |
| `"cclib"` | `source.creativeCloudFileId` |

### Output field changes

| V1 | V2 | Breaking? |
|---|---|---|
| `href` + `storage` | `destination.url` (or CC / hosted / embedded) | Yes |
| `type` | `mediaType` | Yes |
| `quality` 1–7 (number) | `quality` string enum | Yes |
| `compression` `small`/`medium`/`large` | `compression` 10-level enum | Yes |
| `overwrite` | `shouldOverwrite` | Yes (renamed) |
| `trimToCanvas: true` | `cropMode: "document_bounds"` or `"trim_to_transparency"` | Yes |
| `trimToLayer: true` | `cropMode: "layer_bounds"` | Yes |
| *(not in V1)* | `height` | New |

### JPEG quality mapping

| V1 (number) | V2 (string) |
|---|---|
| 7 | `"maximum"` |
| 5–6 | `"high"` |
| 3–4 | `"medium"` |
| 1–2 | `"poor"` / `"very_poor"` |
| *(new)* | `"photoshop_max"` (recommended default) |

### PNG compression mapping

| V1 | V2 |
|---|---|
| `"small"` | `"maximum"` |
| `"medium"` | `"medium"` |
| `"large"` | `"low"` |

### New output formats in V2

`document/vnd.adobe.cpsd+dcxucf` (PSDC), `application/json` (JSON manifest) — not in V1.

### Status response changes

| V1 | V2 |
|---|---|
| `outputs[n].status` | `status` (top-level) |
| `outputs[n].created`/`modified` | `createdTime`/`modifiedTime` (top-level) |
| `outputs[n]._links.renditions[m].href` | `result.outputs[n].destination.url` |
| `outputs[n].errors.code` (number) | `errorDetails[n].errorCode` (string) |

## Execute Actions API (`/v2/execute-actions`) — key breaking changes reference

For the complete authoritative field-level diff, see
[Execute Actions V1 Reference](execute-actions-v1-reference.md).

### Endpoints covered

| V1 | V2 |
|---|---|
| `POST /pie/psdService/photoshopActions` | `POST /v2/execute-actions` |
| `POST /pie/psdService/actionJSON` | `POST /v2/execute-actions` |
| `POST /pie/psdService/productCrop` | `POST /v2/execute-actions` (published action) |
| `POST /pie/psdService/splitView` | `POST /v2/execute-actions` (published action) |
| `POST /pie/psdService/sideBySide` | `POST /v2/execute-actions` (published action) |
| `POST /pie/psdService/depthBlur` | Not yet supported (Neural Filters) |
| `POST /pie/psdService/text` | Not execute-actions — use document edit operations |
| `POST /pie/psdService/smartObjectV2` | Not execute-actions — use document edit operations |

The only known API-visible gap is Neural Filters (Depth Blur), which are not yet available in V2.

### Request envelope (breaking)

| V1 | V2 |
|---|---|
| `inputs[0].href` | `image.source.url` |
| `inputs[0].storage: "external"` | *(omit — inferred)* |
| `inputs[0].storage: "adobe"` (path) | `image.source.creativeCloudPath` |
| `inputs[0].storage: "adobe"` (URN) | `image.source.creativeCloudFileId` |
| `outputs[].href` | `outputs[].destination.url` |
| `outputs[].storage` | `outputs[].destination.storageType` (Azure/Dropbox only) |
| `outputs[].type` | `outputs[].mediaType` |

### ActionJSON format (critical breaking change)

V1 `options.actionJSON` was an **array of inline JSON objects**. V2 requires ActionJSON as a **stringified JSON string** inside `options.actions[].source.content` with `contentType: "application/json"`.

```json
// V1
{"options": {"actionJSON": [{"_obj": "convertMode", "to": {"_enum": "colorSpaceMode", "_value": "grayscale"}}]}}

// V2
{"options": {"actions": [{"source": {"content": "[{\"_obj\":\"convertMode\",\"to\":{\"_enum\":\"colorSpaceMode\",\"_value\":\"grayscale\"}}]", "contentType": "application/json"}}]}}
```

### Additional images/contents rename

| | V1 | V2 |
|---|---|---|
| Field name | `options.additionalImages[]` | `options.additionalContents[]` |
| Item structure | `{href, storage}` | `{source: {url}}` |
| Placeholder | `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0` | `__ADDITIONAL_CONTENTS_PATH_0__` |

The old placeholder format is still accepted in V2 for backward compatibility but `__ADDITIONAL_CONTENTS_PATH_X__` is preferred.

### .atn action source nesting

| V1 | V2 |
|---|---|
| `options.actions[].href` | `options.actions[].source.url` |
| `options.actions[].storage` | *(implicit from source field)* |

V1 supported a single action per request. V2 allows up to **10 actions** executed in sequence (`.atn` files and inline ActionJSON can be mixed).

### Font options rename

| V1 | V2 |
|---|---|
| `options.fonts[]` | `options.fontOptions.additionalFonts[]` (capped at 10) |
| `options.brushes[].href` | `options.brushes[].source.url` |
| `options.patterns[].href` | `options.patterns[].source.url` |

### Removed V1 options

| V1 Field | V2 Status |
|---|---|
| `options.costOptimization` | **Removed** — no equivalent |
| `outputs[].includeMetadata` | **Removed** — implicit |
| `outputs[].embedICCProfiles` | **Replaced** by `outputs[].iccProfile` object |

### Output field renames

| V1 | V2 |
|---|---|
| `quality` (numeric 1–12) | `quality` (string enum: `"very_poor"`, `"poor"`, `"low"`, `"medium"`, `"high"`, `"maximum"`, `"photoshop_max"`) |
| `compression` (`"small"`/`"medium"`/`"large"`) | `compression` (10-level enum: `"none"` through `"maximum"`) |
| `overwrite` | `shouldOverwrite` |

### Resource limits

| Resource | V1 | V2 |
|---|---|---|
| Actions | 1 | **10** (can mix `.atn` + inline) |
| Additional images/contents | 25 | 25 |
| Brushes | Undocumented | **10** |
| Patterns | Undocumented | **10** |
| Fonts | Undocumented | **10** |
| Outputs | Undocumented | **25** |

**End of LLM Migration Reference Guide**
