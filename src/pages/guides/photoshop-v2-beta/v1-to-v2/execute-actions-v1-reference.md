---
title: Execute Actions — Complete V1 Migration Reference
description: Field-level V1 vs V2 comparison for photoshopActions, actionJSON, and convenience API endpoints migrating to /v2/execute-actions
hideBreadcrumbNav: true
keywords:
  - execute-actions
  - photoshopActions
  - actionJSON
  - productCrop
  - splitView
  - sideBySide
  - migration reference
  - v1 to v2
---

# Execute Actions — Complete V1 Migration Reference

This page is the authoritative single-page field-level reference for migrating from the V1
Photoshop action endpoints to `/v2/execute-actions`.

For a guided walkthrough with examples, see [Actions Migration](actions-migration.md).

## 1. V1 endpoint coverage

| V1 Endpoint | V2 Endpoint | Notes |
|---|---|---|
| `POST /pie/psdService/photoshopActions` | `POST /v2/execute-actions` | `.atn` file execution |
| `POST /pie/psdService/actionJSON` | `POST /v2/execute-actions` | Inline ActionJSON (stringified in V2) |
| `POST /pie/psdService/productCrop` | `POST /v2/execute-actions` (published action) | Convenience API |
| `POST /pie/psdService/splitView` | `POST /v2/execute-actions` (published action) | Requires 2 additional contents |
| `POST /pie/psdService/sideBySide` | `POST /v2/execute-actions` (published action) | Requires 2 additional contents |
| `POST /pie/psdService/depthBlur` | **Not yet supported** | Neural Filters unavailable in V2 |
| `POST /pie/psdService/text` | `/v2/execute-actions` | Use UXP/actions instead |
| `POST /pie/psdService/smartObjectV2` | `/v2/execute-actions` | Use UXP/actions instead |

<InlineAlert variant="info" slots="text"/>

The only known API-visible gap is Neural Filters (Depth Blur), which are not yet available in V2.

## 2. Request envelope

<InlineAlert variant="warning" slots="text"/>

**`inputs[]` array → `image` single object.** V1 used an `inputs` array (max 1 item); V2 uses a top-level `image` object. There is no multi-input support in execute-actions.

**V1:**

```json
{"inputs": [{"href": "<URL>", "storage": "external"}]}
```

**V2:**

```json
{"image": {"source": {"url": "<URL>"}}}
```

| V1 | V2 | Notes |
|---|---|---|
| `inputs[0].href` | `image.source.url` | Breaking |
| `inputs[0].storage: "external"` | *(omit)* | External URLs need no type |
| `inputs[0].storage: "adobe"` (path) | `image.source.creativeCloudPath` | No leading slash |
| `inputs[0].storage: "adobe"` (URN) | `image.source.creativeCloudFileId` | |
| `inputs[0].storage: "acp"` | `image.source.url` | Use presigned URL |
| `outputs[].href` | `outputs[].destination.url` | Breaking |
| `outputs[].storage` | `outputs[].destination.storageType` (Azure/Dropbox only) | Breaking |
| `outputs[].type` | `outputs[].mediaType` | Breaking |

## 3. Actions (`.atn` files)

| V1 (`options.actions[n].*`) | V2 (`options.actions[n].source.*`) | Notes |
|---|---|---|
| `href` (URL or path) | `url` | Breaking: nested under `source` |
| `storage: "external"` | *(omit)* | |
| `storage: "adobe"` (path) | `creativeCloudPath` | |
| `storage: "adobe"` (URN) | `creativeCloudFileId` | |
| `storage: "acp"` | `url` | |

**V1 → V2 action item example:**

```json
// V1
{"href": "<ACTION_URL>", "storage": "external"}

// V2
{"source": {"url": "<ACTION_URL>"}}
```

**Multiple actions (V2 only):**

V1 supported a single action per request. V2 allows up to **10 actions** executed in sequence —
the first `.atn` and inline ActionJSON can be mixed freely within the same array.

## 4. ActionJSON (critical breaking change)

<InlineAlert variant="warning" slots="text"/>

**ActionJSON format changed completely.** In V1, `options.actionJSON` was an array of inline JSON objects. In V2, ActionJSON is provided as a **stringified JSON string** inside `options.actions[].source.content` and must include `contentType: "application/json"`.

| | V1 | V2 |
|---|---|---|
| Field | `options.actionJSON[]` | `options.actions[].source.content` |
| Format | Inline JSON array of objects | **Stringified** JSON string |
| contentType | Not required | `"application/json"` required |

**V1:**

```json
{
  "options": {
    "actionJSON": [
      {"_obj": "convertMode", "to": {"_enum": "colorSpaceMode", "_value": "grayscale"}}
    ]
  }
}
```

**V2:**

```json
{
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"convertMode\",\"to\":{\"_enum\":\"colorSpaceMode\",\"_value\":\"grayscale\"}}]",
          "contentType": "application/json"
        }
      }
    ]
  }
}
```

## 5. Additional images / contents

<InlineAlert variant="warning" slots="text"/>

**`options.additionalImages` renamed to `options.additionalContents`.** The placeholder format used inside ActionJSON also changed. The old `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_X` placeholder is still accepted in V2 for backward compatibility, but `__ADDITIONAL_CONTENTS_PATH_X__` is the preferred format.

| | V1 | V2 |
|---|---|---|
| Field name | `options.additionalImages[]` | `options.additionalContents[]` |
| Item structure | `{href, storage}` | `{source: {url}}` |
| Placeholder (ActionJSON) | `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0` | `__ADDITIONAL_CONTENTS_PATH_0__` |
| Max items | 25 | 25 |

**V1:**

```json
{
  "options": {
    "additionalImages": [
      {"href": "<OVERLAY_URL>", "storage": "external"}
    ],
    "actionJSON": [
      {"_obj": "placeEvent", "null": {"_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"}}
    ]
  }
}
```

**V2:**

```json
{
  "options": {
    "additionalContents": [
      {"source": {"url": "<OVERLAY_URL>"}}
    ],
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"placeEvent\",\"null\":{\"_path\":\"__ADDITIONAL_CONTENTS_PATH_0__\",\"_kind\":\"local\"}}]",
          "contentType": "application/json"
        }
      }
    ]
  }
}
```

## 6. Additional resources (fonts, brushes, patterns)

| V1 | V2 | Notes |
|---|---|---|
| `options.fonts[]` with `{href, storage}` | `options.fontOptions.additionalFonts[]` with `{source: {url}}` | Breaking: renamed + wrapped in `fontOptions` |
| `options.brushes[].href` | `options.brushes[].source.url` | Breaking: nested |
| `options.brushes[].storage` | *(implicit)* | |
| `options.patterns[].href` | `options.patterns[].source.url` | Breaking: nested |
| `options.patterns[].storage` | *(implicit)* | |
| *(not in V1)* | `fontOptions.missingFontStrategy` | New: `"use_default"` or `"fail"` |
| *(not in V1)* | `fontOptions.defaultFontPostScriptName` | New: fallback font |

**Resource limits:**

| Resource | V1 | V2 |
|---|---|---|
| Fonts | Undocumented | **10** (in `fontOptions.additionalFonts`) |
| Brushes | Undocumented | **10** |
| Patterns | Undocumented | **10** |

All binary resources (fonts, brushes, patterns, additional images) must be external file
references. **Inline content is not supported for binary resources in V2.**

## 7. Removed V1 options

| V1 Field | V2 Status | Notes |
|---|---|---|
| `options.costOptimization` (boolean) | **Removed** | No equivalent; optimization is internal in V2 |
| `outputs[].includeMetadata` (boolean) | **Removed** | No equivalent; implicit behavior |
| `outputs[].embedICCProfiles` (boolean) | **Replaced** | Use `outputs[].iccProfile` object instead |

## 8. Output fields

| V1 | V2 | Notes |
|---|---|---|
| `href` | `destination.url` | Breaking |
| `storage` | `destination.storageType` (Azure/Dropbox only) | Breaking |
| `type` | `mediaType` | Breaking |
| `quality` (number, 1–12) | `quality` (string enum) | Breaking: see quality table |
| `compression` (`small`/`medium`/`large`) | `compression` (10-level enum) | Breaking |
| `overwrite` (boolean) | `shouldOverwrite` (boolean) | Breaking: renamed |
| `includeMetadata` (boolean) | **Removed** | No equivalent |
| `embedICCProfiles` (boolean) | **Removed** | Use `iccProfile` object |
| *(not in V1)* | `width`, `height`, `maxWidth` | New |
| *(not in V1)* | `iccProfile` object | New (replaces `embedICCProfiles`) |
| *(not in V1)* | `destination.embedded` (`base64`/`string`/`json`) | New |
| *(not in V1)* | `destination.validityPeriod` (60–86400 sec) | New |
| *(not in V1)* | `scriptOutputPattern` (glob string) | New; UXP only; hosted/embedded destinations only |

## 9. JPEG quality mapping

| V1 (numeric) | V2 (string enum) |
|---|---|
| 1–2 | `"very_poor"` / `"poor"` |
| 3–4 | `"low"` / `"medium"` |
| 5–6 | `"high"` |
| 7–8 | `"maximum"` |
| 9–12 | `"photoshop_max"` |

<InlineAlert variant="info" slots="text"/>

Use `"photoshop_max"` for highest quality production output. Passing a numeric value in V2 returns a validation error.

## 10. PNG compression mapping

| V1 | V2 |
|---|---|
| `"small"` | `"maximum"` |
| `"medium"` | `"medium"` |
| `"large"` | `"low"` |
| *(not in V1)* | `"none"`, `"very_low"`, `"medium_low"`, `"medium_high"`, `"default"`, `"high"`, `"very_high"` |

## 11. Supported output formats

| Format | V1 `type` | V2 `mediaType` | Notes |
|---|---|---|---|
| JPEG | `image/jpeg` | `image/jpeg` | |
| PNG | `image/png` | `image/png` | |
| TIFF | `image/tiff` | `image/tiff` | |
| PSD | `image/vnd.adobe.photoshop` or `vnd.adobe.photoshop` | `image/vnd.adobe.photoshop` | V2 normalizes |
| GIF | `image/gif` | Not confirmed in V2 | Present in V1 only |
| PSDC | Not supported | `document/vnd.adobe.cpsd+dcxucf` | New in V2 |
| JSON | Not supported | `application/json` | New in V2 |

## 12. Convenience API migration

V1 convenience APIs called predefined server-side action files. In V2, those action files are
published; you use them via `/v2/execute-actions`. See the per-API migration guides for the
complete ActionJSON definitions.

| V1 Endpoint | V2 Approach | Guide |
|---|---|---|
| `productCrop` | Published ActionJSON | [Product Crop](convenience-apis/product-crop.md) |
| `splitView` | Published ActionJSON + 2 `additionalContents` | [Split View](convenience-apis/split-view.md) |
| `sideBySide` | Published ActionJSON + 2 `additionalContents` | [Side by Side](convenience-apis/side-by-side.md) |
| `depthBlur` | **Not yet supported** | Neural Filters unavailable in V2 |

## 13. Resource limits summary

| Resource | V1 | V2 |
|---|---|---|
| Input images | 1 | 1 |
| Actions | 1 | **10** (can mix `.atn` and inline) |
| Additional images/contents | 25 | 25 |
| Brushes | Undocumented | **10** |
| Patterns | Undocumented | **10** |
| Fonts | Undocumented | **10** |
| UXP scripts | 0 | 1 (limited availability) |
| Outputs | Undocumented | **25** |

## 14. Complete migration checklist

- [ ] Replace `inputs[0].href` + `storage` with `image.source.url` (or `creativeCloudPath` / `creativeCloudFileId`)
- [ ] Replace `outputs[].href` + `storage` with `outputs[].destination.url` (or CC / hosted / embedded)
- [ ] Replace `outputs[].type` with `outputs[].mediaType`
- [ ] Replace `options.actions[].href` + `storage` with `options.actions[].source.url`
- [ ] Stringify ActionJSON: `options.actionJSON[...]` → `options.actions[].source.content` as JSON string + `contentType: "application/json"`
- [ ] Rename `options.additionalImages[]` to `options.additionalContents[]`; update item structure to `source.url`
- [ ] Update placeholder format: `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0` → `__ADDITIONAL_CONTENTS_PATH_0__`
- [ ] Rename `options.fonts[]` to `options.fontOptions.additionalFonts[]`; update item structure to `source.url`
- [ ] Update `options.brushes[].href` + `storage` to `options.brushes[].source.url`
- [ ] Update `options.patterns[].href` + `storage` to `options.patterns[].source.url`
- [ ] Remove `options.costOptimization` (no equivalent)
- [ ] Change JPEG `quality` from numeric (1–12) to string enum
- [ ] Change PNG `compression` from `small`/`medium`/`large` to V2 enum
- [ ] Rename `overwrite` to `shouldOverwrite` on outputs
- [ ] Remove `includeMetadata` and `embedICCProfiles` from outputs; add `iccProfile` object if needed
- [ ] Check resource counts are within V2 limits (10 for brushes/patterns/fonts, 25 for outputs)

## 15. New and noteworthy additional features

1. **Scripting support**: UXP scripts can now be executed on the server. These run in a sandbox with network and disk access restricted.
2. **Generative AI**: Most of the generative functionality offered via Photoshop Desktop is available via Actions, including Generative Fill, Generative Expand, Wire Distractor, and People Distractor.
3. **Dynamic text**: Dynamic text functionality is now available via Actions and UXP scripting.
4. **Better background removal**: Improved background removal capabilities.

## See also

- [Actions Migration](actions-migration.md) — Guided walkthrough with examples and best practices
- [Output Types Migration](output-types-migration.md) — JPEG, PNG, TIFF output format details
- [ICC Profile Migration](icc-profile-migration.md) — Color management options
- [Product Crop](convenience-apis/product-crop.md) — Full ActionJSON definition
- [Split View](convenience-apis/split-view.md) — Full ActionJSON definition
- [Side by Side](convenience-apis/side-by-side.md) — Full ActionJSON definition
