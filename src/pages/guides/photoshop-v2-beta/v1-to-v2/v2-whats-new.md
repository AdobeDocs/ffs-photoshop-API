---
title: What's New in V2
description: Net new capabilities in the V2 API that weren't available in V1
hideBreadcrumbNav: true
keywords:
  - new features
  - v2 capabilities
  - artboard
  - smart object extraction
  - smart objects
  - SVG
  - group layers
  - pixel mask
  - delete pixel mask
  - text rendering
  - UXP scripts
  - GenAI
  - hosted storage
  - cropMode
---

# What's new in V2

This page covers capabilities that are **net new in V2** — things you couldn't do at all in V1. If you're looking for a complete behavioral comparison (what changed, what was renamed, what broke), see the [V2 API Behavior Catalog](v2-api-catalog.md).

## `/v2/execute-actions` — new capabilities

### UXP script execution

<InlineAlert variant="info" slots="text"/>

V2 supports modern ES6+ JavaScript automation via Adobe's UXP platform alongside traditional `.atn` Photoshop actions and ActionJSON. UXP scripts run inside Photoshop with full API access to document structure and layers.

V1 supported `.atn` action files and ActionJSON. V2 adds UXP scripts — JavaScript that runs inside Photoshop using Adobe's modern extension platform:

```json
{
  "image": {
    "source": { "url": "https://example.com/input.psd" }
  },
  "options": {
    "uxp": [
      {
        "source": {
          "content": "const doc = require('photoshop').app.activeDocument;\nconst layers = doc.layers;\nconst info = layers.map(l => ({ name: l.name, kind: l.kind }));\nrequire('uxp').storage.localFileSystem.getTemporaryFolder()\n  .then(tmp => tmp.createFile('info.json'))\n  .then(f => f.write(JSON.stringify(info)));"
        }
      }
    ]
  },
  "outputs": [
    {
      "mediaType": "application/json",
      "destination": { "embedded": "json" },
      "scriptOutputPattern": "info.json"
    }
  ]
}
```

UXP scripts can:
- Use ES6+ JavaScript — modern syntax, arrow functions, async/await, modules
- Read and modify document structure, layers, and effects via the full Photoshop API
- Run sandboxed inside Photoshop; file I/O is restricted to `plugin-temp:/`
- Combine with `.atn` / ActionJSON in a single request (actions execute first, then UXP scripts)

### New actions

A whole lot of never actions are getting supported via the Actions execution. These include following besides may more:

 1. Generative Fill
 2. Generative Expand
 3. People/Wire Distractor
 4. Dynamic Text
 5. And many more...

See [Actions Migration](actions-migration.md) for the full UXP syntax reference.

### UXP adhoc file output

<InlineAlert variant="info" slots="text"/>

UXP scripts can write any file to `plugin-temp:/` during execution. The `scriptOutputPattern` field (glob syntax) captures those runtime-generated files and delivers them to the caller — enabling adhoc, variable outputs that aren't known before the job starts. This helper is **UXP-only** and does not apply to `.atn` or ActionJSON.

In V1, every output required a pre-defined file name and destination URL before the job started. If your script generated a variable number of files, you couldn't capture them.

V2 `scriptOutputPattern` is a glob pattern matched against files written by a UXP script at execution time:

```json
{
  "outputs": [
    {
      "mediaType": "image/png",
      "destination": { "hosted": true },
      "scriptOutputPattern": "preview-*.png"
    }
  ]
}
```

If the script writes `preview-small.png`, `preview-medium.png`, and `preview-large.png`, the response expands into three separate output entries, each with its own hosted URL.

Key constraints:
- Only `embedded` and `hosted` destinations are supported — presigned URLs require pre-known filenames
- Patterns are matched case-insensitively against filenames in the UXP output directory
- `quality`, `compression`, `width`, `height` output parameters are ignored when `scriptOutputPattern` is set

See [Actions Migration](actions-migration.md) for full syntax and examples.

### Published and customizable action files

<InlineAlert variant="info" slots="text"/>

V1 convenience APIs (`productCrop`, `splitView`, `sideBySide`) ran hidden server-side action files you couldn't inspect or modify. V2 publishes those same action files so you can examine, fork, and customize them.

V1 had several convenience endpoints that wrapped undisclosed Photoshop action files:

- `/pie/psdService/productCrop` — auto-crop products with padding
- `/pie/psdService/splitView` — before/after comparison with divider
- `/pie/psdService/sideBySide` — before/after side-by-side layout

In V2, these operations all use `/v2/execute-actions` with the action files now published. You can:

- Inspect exactly what Adobe's implementation does
- Run the action as-is using `additionalContents`
- Download and customize the action for your specific needs
- Build similar functionality using the published files as a reference

See the individual guides for download links and usage:
- [Product Crop](convenience-apis/product-crop.md)
- [Split View](convenience-apis/split-view.md)
- [Side by Side](convenience-apis/side-by-side.md)

## `/v2/generate-manifest` — richer document intelligence

### Distinct artboard layer type

<InlineAlert variant="info" slots="text"/>

V1 artboards were stored as `layerSection` nodes — indistinguishable from regular group folders. V2 gives them a dedicated `type: "artboard"` with full geometry, preset name, and background color.

In V1, when you called `documentManifest` on a PSD containing artboards, each artboard came back as a plain `layerSection` group with no indication that it was an artboard or what device preset it was based on. You had to infer artboard identity from naming conventions.

In V2, `generate-manifest` promotes artboards to a first-class layer type. You get:

- The artboard's device preset name (e.g. `"iPhone 16 Pro"`)
- The exact artboard rectangle (`artboardRect`)
- The background color and background type
- Child layers under `layers[]` (not `children[]`) for unambiguous traversal

```json
{
  "type": "artboard",
  "id": 1,
  "name": "iPhone 16 Pro – 1",
  "typeAttributes": {
    "artboard": {
      "artboardPresetName": "iPhone 16 Pro",
      "artboardRect": {
        "left": 0,
        "top": 0,
        "right": 393,
        "bottom": 852
      },
      "artboardBackgroundType": 1,
      "color": {
        "type": "RGBColor",
        "red": 255,
        "grain": 255,
        "blue": 255
      }
    }
  },
  "layers": [ ... ]
}
```

See [Manifest Response Migration](manifest-response-migration.md) for the full artboard field reference.

### Smart object extraction

<InlineAlert variant="info" slots="text"/>

Embedded smart objects now expose a download URL (`extracted.url`) in the manifest response. You can retrieve the raw smart object content — a PSD, PNG, or other file — without opening Photoshop.

In V1, the manifest told you a smart object existed and gave you its filename and MIME type, but you had no way to download its embedded content.

In V2, `generate-manifest` includes an `extracted` field on non-linked (embedded) smart objects:

```json
{
  "type": "smart_object_layer",
  "name": "button-component",
  "isSmartObject": true,
  "isLinked": false,
  "isValid": true,
  "smartObjectData": {
    "fileInfo": {
      "name": "button-component.psd",
      "fileType": "ps3"
    }
  },
  "extracted": {
    "mediaType": "image/vnd.adobe.photoshop",
    "url": "https://photoshop-api.adobe.io/v2/short-url/urn:aaid:ps:..."
  }
}
```

The `extracted.url` is a short-URL redirect that delivers the raw embedded content. This is available for embedded (non-CC-linked) smart objects only.

See [Manifest Response Migration](manifest-response-migration.md) for full smart object field details.

### Rich manifest layer metadata

<InlineAlert variant="info" slots="text"/>

V2 manifest responses include many new per-layer fields that V1 never exposed: composite frame bounds, warp settings, blend-if ranges, CC Libraries linkage, missing fonts, and more.

V1 manifest responses were relatively sparse — basic layer info like name, type, bounds, and blend mode.

V2 adds substantial new fields on every layer:

| Field | Description |
|-------|-------------|
| `compositeFrame` | Canvas-space bounds (absolute and parent-relative) |
| `referenceFrame` | Untransformed content bounds |
| `layerSettings.FXRefPoint` | Reference point for layer effects |
| `layerSettings` → `textLayerSettings` | Text warp state (style, value, perspective, rotation) |
| `blendOptions.blendRanges` | Blend-if color range data |
| `blendOptions.fillOpacity` | Fill opacity separate from layer opacity |
| `blendOptions.channelRestrictions` | Per-channel blend restrictions |
| `smartObjectData.ccLibrariesElement` | CC Libraries name, library, stock ID, license state |
| `text.missingFonts` | List of fonts not available on the server |
| `text.antiAliasing` | Anti-aliasing method (e.g. `"crisp"`) |
| `text.paragraphAttributes` | Indents, spacing, writing direction per paragraph |

These fields are available without any request changes — they appear automatically in `generate-manifest` responses.

See [Manifest Response Migration](manifest-response-migration.md) for the complete field catalog.

## `/v2/create-composite` — major new capabilities

### Smart object support — enhanced in V2

<InlineAlert variant="info" slots="text"/>

V2 redesigns the smart object API for predictable behavior across place, replace, and transform operations. It adds support for SVG source files, linked smart objects, and new replacement capabilities not available in V1.

V1 smart object behavior was inconsistent across add, edit, and replace operations. V2 unifies these under a single `operation` model with explicit `type` and `placement`:

```json
{
  "type": "smart_object_layer",
  "name": "Logo",
  "operation": {
    "type": "add",
    "placement": { "type": "top" }
  },
  "smartObject": {
    "smartObjectFile": {
      "source": { "url": "<SMART_OBJECT_URL>" }
    }
  }
}
```

**New features in V2:**

1. **SVG Support** — V2 adds SVG as a supported smart object source type (`image/svg+xml`). V1 only supported PSD, JPEG, and PNG.

2. **Linked Smart Objects** — V2 provides full support for linked smart objects (external files referenced by the PSD rather than embedded). Add new linked smart objects using `isLinked: true`:

    ```json
    {
      "type": "smart_object_layer",
      "name": "External Logo",
      "operation": {
        "type": "add",
        "placement": { "type": "top" }
      },
      "smartObject": {
        "isLinked": true,
        "smartObjectFile": {
          "source": { "url": "<EXTERNAL_FILE_URL>" }
        }
      }
    }
    ```

3. **Replacement Operations** — V2 introduces smart object replacement capabilities not possible in V1:
    - Replace linked smart object with another linked smart object
    - Replace embedded smart object with linked smart object

    Example of converting an embedded smart object to linked:

    ```json
    {
      "name": "Existing Embedded Smart Object",
      "type": "smart_object_layer",
      "operation": {
        "type": "edit"
      },
      "smartObject": {
        "isLinked": true,
        "smartObjectFile": {
          "source": { "url": "<LINKED_FILE_URL>" }
        }
      }
    }
    ```

4. **Resize with Linked Smart Objects** — V1 rejected any resize (`width`/`maxWidth`) on documents containing linked smart objects. V2 removes this restriction. See [resize behavior details](layer-operations-smart-objects.md#resize-with-linked-smart-objects) in the Smart Object Operations Migration guide.

**Supported source types:** PSD, JPEG, PNG, SVG


**Use cases for linked smart objects:**
- Shared assets across multiple PSDs
- Large files that shouldn't be embedded
- Assets that need to be updated independently

See [Smart Object Operations Migration](layer-operations-smart-objects.md) for complete documentation and examples.

### Text layer support — new rendering engine

The changes include substantial changes for text rendering for complex and multilingual fonts and text.

V2 introduces new character and paragraph style attributes not available in V1:

| Property | Description |
|----------|-------------|
| `syntheticBold` | Synthesize bold when the font has no bold variant |
| `syntheticItalic` | Synthesize italic when the font has no italic variant |
| `letterSpacing` | Character tracking / letter spacing |
| `lineHeight` | Leading / line height |
| `fontAlpha` | Per-character font opacity |
| `capsOption` | Capitalization option (e.g. `"all_caps"`) |

See [Text Layer Operations Migration](layer-operations-text.md) for the complete character and paragraph style reference.

### Group layer create and edit

<InlineAlert variant="info" slots="text"/>

V2 introduces `type: "group_layer"` (V1 used `"layerSection"`) and a unified `operation` model for reordering layers within groups and for adding layers into existing groups.

**Creating a new document with a group layer is not yet supported (upcoming feature).** 
**Editing an existing document** to add a layer inside a group layer **is supported** — use `placement.type: "into"` with `referenceLayer` (e.g. `"referenceLayer": { "name": "Group 1" }`).

```json
{
  "type": "smart_object_layer",
  "name": "Logo",
  "operation": {
    "type": "add",
    "placement": {
      "type": "into",
      "referenceLayer": { "name": "Group 1" }
    }
  },
  "smartObject": {
    "smartObjectFile": { "source": { "url": "<LOGO_URL>" } }
  }
}
```

Placement options for ordering within groups: `into`, `above`, `below`, `top`, `bottom`.

See [Advanced Layer Operations Migration](layer-operations-advanced.md) for the full group layer reference.

### Delete pixel mask

<InlineAlert variant="info" slots="text"/>

V2 adds the ability to remove a pixel mask from a layer during an edit operation. V1 had no mechanism to delete an existing pixel mask without replacing the entire layer.

When editing an existing layer, you can now remove its pixel mask by setting `pixelMask.delete` to `true`. This deletes the mask data entirely.

```json
{
  "edits": {
    "layers": [
      {
        "name": "Layer with Mask",
        "operation": { "type": "edit" },
        "pixelMask": {
          "delete": true
        }
      }
    ]
  }
}
```

Key constraints:
- Only available on **edit** operations (`operation.type: "edit"`) — not valid on add
- `delete` must be a boolean (`true` or `false`);
- Can be combined with other layer edits (opacity, visibility, etc.) in the same layer entry

See [Advanced Layer Operations Migration](layer-operations-advanced.md#deleting-a-pixel-mask) for full examples and validation rules.

### ICC profile control

<InlineAlert variant="info" slots="text"/>

V2 lets you specify the output ICC profile per export — including standard Photoshop profiles or a custom profile you supply. V1 had no ICC profile control at all.

Every output destination in V2 can specify an `iccProfile`:

```json
{
  "outputs": [
    {
      "mediaType": "image/jpeg",
      "destination": { "url": "https://storage.example.com/output.jpg" },
      "iccProfile": {
        "standard": "sRGB IEC61966-2.1"
      }
    }
  ]
}
```

Standard profiles include `sRGB IEC61966-2.1`, `Adobe RGB (1998)`, `ProPhoto RGB`, and others. You can also supply a custom `.icc` file via `iccProfile.custom.source.url`.

See [ICC Profile Migration](icc-profile-migration.md) for the full list and constraints.

### Crop mode — unified enum for all export types

<InlineAlert variant="info" slots="text"/>

V1 had two separate booleans — `trimToCanvas` and `trimToLayer` — for controlling output bounds. V2 replaces them with a single `cropMode` enum that works across single-layer, multi-layer, and document export.

V1 used `trimToCanvas` (trim transparent pixels) and `trimToLayer` (use layer bounds) as separate boolean flags on rendition outputs. These worked for document and single-layer export, but multi-layer composites had no trim control.

V2 consolidates these into a single `cropMode` enum on any output:

| Value | Description | Single-layer | Multi-layer | Document export |
|-------|-------------|:---:|:---:|:---:|
| `layer_bounds` | Layer's own bounding box (default for single-layer) | Yes | No | No |
| `trim_to_transparency` | Crop to non-transparent pixels (replaces V1 `trimToCanvas: true`) | Yes | Yes | Yes |
| `document_bounds` | Full canvas size (default for document/multi-layer) | Yes | Yes | Yes |

```json
{
  "outputs": [
    {
      "mediaType": "image/png",
      "destination": { "url": "https://storage.example.com/output.png" },
      "layers": [{"id": 1096}, {"id": 996}],
      "cropMode": "trim_to_transparency"
    }
  ]
}
```

`layer_bounds` is restricted to single-layer export and returns a validation error for multi-layer or document export.

See [Export Layers Migration](export-layers-migration.md) for the full cropMode reference.

## Architectural improvements

### Long running process support

We have bumped up the processing time allowance to 15 minutes to allow processing of larger and complex edit.

### Large file support

Earlier we capped the file size to 2 GB, now that restriction is being bumped up to 4 GB. We are working on the further details and will share the new number shortly.

### Better error handling and job timeouts

Most of workflows should now return with an actionable error code to help diagnose the error better. We also added features to automatically mark job failed after an hour of inactivity.

## Storage options

V2 introduces two convenience storage modes that require no external infrastructure — useful for quick prototyping and returning intermediate results for further pipeline processing:

- **Embedded** — result returned inline as base64 in the response body, but restricted to only textual content only.
- **Hosted** — Adobe manages temporary storage and returns a download URL (configurable expiration)

For production use, external storage (S3, Azure, Dropbox, Creative Cloud) remains the recommended approach and depends on the access control the caller indends to enforce.

See the [Storage Solutions](/getting-started/storage-solutions/index.md) guide for the full reference.

## Next steps

- [V2 API Behavior Catalog](v2-api-catalog.md) — Complete per-endpoint behavioral comparison (V1 vs V2)
- [Migration Overview](index.md) — Architectural changes and high-level migration guidance
- [Quick Reference](index.md) — Endpoint mapping table and migration step list
