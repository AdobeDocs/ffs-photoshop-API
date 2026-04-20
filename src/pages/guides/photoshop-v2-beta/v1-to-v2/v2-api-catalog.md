---
title: V2 API Behavior Catalog (V1 vs V2)
description: Per-endpoint behavioral comparison of all V1 and V2 API changes
hideBreadcrumbNav: true
keywords:
  - api catalog
  - v1 to v2
  - behavior changes
  - breaking changes
  - migration reference
---

# V2 API behavior catalog

This page is a comprehensive per-endpoint behavioral reference for developers migrating from V1 to V2. For each endpoint group it covers: what V1 did, what V2 does, a table of behavioral changes, and links to detailed guides.

For a positive framing of net new capabilities (things you couldn't do at all in V1), see [What's New in V2](v2-whats-new.md).

## 1. Edit operations

**V1 Endpoints:** `/lrService/autoTone`, `/lrService/autoStraighten`, `/lrService/presets`, `/lrService/xmp`, `/lrService/edit`

**V2 Endpoint:** `/v2/edit`

### V1 behavior

V1 Lightroom operations were individual endpoints: one endpoint per operation type. To apply multiple adjustments you made multiple sequential API calls, each returning a job ID to poll. Inputs used `inputs[].href` + `storage` discriminant. The `options` block held adjustment parameters.

### V2 behavior

All Lightroom edit operations are unified under `/v2/edit`. You can combine any number of adjustments — `autoTone`, `autoStraighten`, `light`, `color`, `detail`, `effects`, `optics`, XMP presets — in a single request. The adjustment parameter names and value ranges are identical to V1; only the envelope changed.

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Endpoint per operation type | `/lrService/autoTone`, `/lrService/autoStraighten`, etc. | Single `/v2/edit` for all | Breaking Change |
| Input specification | `inputs[0].href` + `"storage": "external"` | `image.source.url` | Breaking Change |
| Adjustment parameters location | `options` block | Top-level fields (`autoTone`, `light`, `color`, etc.) | Breaking Change |
| Output destination | `outputs[0].href` + `"storage": "external"` | `outputs[0].destination.url` | Breaking Change |
| Output format field | `"type": "image/jpeg"` | `"mediaType": "image/jpeg"` | Breaking Change |
| Multiple operations per request | Not supported — one operation per call | Supported — combine any adjustments | Net New |
| Adjustment parameter values | Same | Same | Unchanged |
| Authentication | OAuth Server-to-Server | OAuth Server-to-Server (unchanged) | Unchanged |

### Guide

[Edit Operations Migration](edit-operations.md)

## 2. Composite and layer operations

**V1 Endpoints:** `/pie/psdService/renditionCreate`, `/pie/psdService/documentCreate`, `/pie/psdService/documentOperations`, layer operations via `documentOperations`

**V2 Endpoint:** `/v2/create-composite`

### V1 behavior

V1 used three separate endpoints for what are now unified operations:
- `renditionCreate` — convert PSD to JPEG/PNG/TIFF (format conversion only)
- `documentCreate` — create a new blank document
- `documentOperations` — modify existing documents: resize, crop, trim, add/edit/delete layers

Layer operations were specified as an `options.layers` array within `documentOperations`. Layer types used camelCase names (`layerSection`, `textLayer`, `smartObject`).

### V2 behavior

All three operations are unified under `/v2/create-composite`. The request structure uses `image.source` for input, `edits` for operations, and `outputs` for results. Layer types use snake_case names. Processing order is strictly top-down through the `edits.layers` array — layer position is not determined by array index alone.

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Endpoint consolidation | Three separate endpoints | Single `/v2/create-composite` | Breaking Change |
| Input field | `inputs[0].href` | `image.source.url` | Breaking Change |
| Operations block | `options` | `edits` | Breaking Change |
| `operation.type` required on layer edits | Not required | Required: `"add"`, `"edit"`, `"delete"`, `"move"` | Breaking Change |
| Layer type names | camelCase (`layerSection`, `textLayer`, etc.) | snake_case (`group_layer`, `text_layer`, etc.) | Breaking Change |
| Processing order | Not strictly defined | Top-down through `edits.layers` array | Breaking Change |
| `referenceLayer` for relative positioning | Not available | Supported | Net New |
| `protection` array | `locked: boolean` | `protection: ["position", "transparency", ...]` | Breaking Change |
| Group layer type name | `layerSection` | `group_layer` | Renamed |
| `isClipped` for clipping masks | Not available | Supported | Net New |
| `pixelMask.delete` to remove a pixel mask | Not available | `pixelMask: { "delete": true }` on edit operations | Net New |
| Multiple outputs per request | Single output | Up to N outputs | Net New |

### Guide

[Layer Operations Overview](layer-operations-overview.md) — then choose a sub-guide:
- [Image Layers](layer-operations-image.md)
- [Text Layers](layer-operations-text.md)
- [Adjustment Layers](layer-operations-adjustments.md)
- [Smart Objects](layer-operations-smart-objects.md)
- [Advanced Operations](layer-operations-advanced.md)
- [Document Creation](document-creation-migration.md)
- [Document Operations](document-operations-migration.md)
- [Format Conversion](format-conversion-migration.md)

## 3. Actions and scripts

**V1 Endpoints:** `/pie/psdService/photoshopActions`, `/pie/psdService/actionJSON`, `/pie/psdService/productCrop`, `/pie/psdService/splitView`, `/pie/psdService/sideBySide`, `/pie/psdService/depthBlur`

**V2 Endpoint:** `/v2/execute-actions`

### V1 behavior

V1 had separate endpoints for each action type: `photoshopActions` for `.atn` files, `actionJSON` for inline action commands, and dedicated convenience endpoints for specific operations (product crop, split view, etc.). Convenience endpoints used hidden server-side action files that developers could not inspect or modify.

### V2 behavior

All action types are unified under `/v2/execute-actions`. The `options` block contains an array of action objects with a `type` discriminant (`"photoshopActions"`, `"actionJSON"`, `"uxp"`). UXP scripts (ES6+ JavaScript) are a new option alongside the existing action types. The action files used by V1 convenience APIs are now published and accessible via `additionalContents`.

<InlineAlert variant="warning" slots="text"/>

Depth Blur (`/pie/psdService/depthBlur`) is **not yet supported in V2** — Neural Filters are not available. See [Depth Blur Migration](convenience-apis/depth-blur.md) for status.

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Endpoint per action type | Separate endpoints | Single `/v2/execute-actions` | Breaking Change |
| Input field | `inputs[0].href` | `image.source.url` | Breaking Change |
| Action type discriminant | Implied by endpoint | `options[].type` required | Breaking Change |
| Action file reference | `inputs[].href` with `"storage"` | `options[].photoshopAction.source.url` | Breaking Change |
| ActionJSON inline commands | `options.actions` array | `options[].actionJSON.commands` array | Breaking Change |
| UXP script support | Not available | `options[].type: "uxp"` with `source.content` | Net New |
| `additionalContents` (supply action file deps) | Not available | Supported | Net New |
| `scriptOutputPattern` for dynamic outputs | Not available | Supported for UXP scripts | Net New |
| `plugin-temp:/` virtual path in scripts | Not available | Supported for inter-script file exchange | Net New |
| Convenience action files inspectable | Hidden server-side | Published, downloadable | Net New |
| Depth Blur | Available | Not yet supported | Removed (temporarily) |

### Guide

[Actions Migration](actions-migration.md)

## 4. Manifest generation

**V1 Endpoint:** `/pie/psdService/documentManifest`

**V2 Endpoint:** `/v2/generate-manifest`

### V1 behavior

V1 `documentManifest` returned a layer tree with basic per-layer information: name, type (camelCase), bounds (height/width/left/top format), a presigned S3 thumbnail URL string, and simple `locked` boolean. Artboards were indistinguishable from group layers. Smart objects had a flat structure with `instanceId`, `name`, `path`, and MIME-type `type`. The document block had `bitDepth`, `iccProfileName`, `name`.

### V2 behavior

V2 `generate-manifest` returns a much richer layer tree. Layer type names are renamed to snake_case. Bounds use `{left, top, right, bottom}` format. Thumbnails return as `{mediaType, url}` objects pointing to `/v2/short-url/` redirects. Artboards are a distinct `type: "artboard"` with full geometry and preset data. Smart objects expose `extracted.url` for embedded content download. The document block gains `xmp`, `resolution`, `globalLightingAngle`, and other fields.

### Layer type renames

| V1 Type | V2 Type |
|---------|---------|
| `adjustmentLayer` | `adjustment_layer` |
| `backgroundLayer` | `background_layer` |
| `fillLayer` | `solid_color_layer` |
| `layer` | `layer` |
| `layerSection` (group) | `group_layer` |
| `layerSection` (artboard) | `artboard` |
| `smartObject` | `smart_object_layer` |
| `textLayer` | `text_layer` |

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Layer type names | camelCase | snake_case | Breaking Change |
| Bounds format | `{height, left, top, width}` | `{left, top, right, bottom}` | Breaking Change |
| Thumbnail field | String URL (direct S3) | `{mediaType, url}` object (`/v2/short-url/` redirect) | Breaking Change |
| `locked` field | `boolean` | Replaced by `protection` array | Breaking Change |
| `rotate` field | number | Renamed to `rotation` | Renamed |
| `mask` field | `{enabled, linked, offset.x/y, type}` | Renamed to `pixelMask`; `offset.x/y` → `offset.horizontal/vertical` | Breaking Change |
| Artboard type | `layerSection` (same as groups) | `type: "artboard"` with `typeAttributes.artboard` | Net New |
| Artboard children key | `children[]` | `layers[]` | Breaking Change |
| Smart object structure | Flat `{instanceId, linked, name, path, type}` | Nested `{isLinked, isValid, smartObjectData, extracted}` | Breaking Change |
| Smart object MIME type field | `type` string | `smartObjectData.fileInfo.fileType` short code | Breaking Change |
| `extracted.url` on embedded smart objects | Not available | Available | Net New |
| Document `bitDepth` | `bitDepth` | `depth` | Renamed |
| Document `iccProfileName` | `iccProfileName` | `iccProfile` | Renamed |
| Document `name` | `name` | `title` | Renamed |
| Document `photoshopBuild` | Present | Removed | Removed |
| Document XMP | Not available | `document.xmp` | Net New |
| Document resolution | Not available | `document.resolution` | Net New |
| `compositeFrame` / `referenceFrame` per layer | Not available | Available | Net New |
| `layerSettings` block (warp, FXRefPoint) | Not available | Available | Net New |
| `blendRanges` in `blendOptions` | Not available | Available | Net New |
| `ccLibrariesElement` on smart objects | Not available | Available | Net New |
| `options.includeXmp` | Not available | Supported | Net New |
| `options.maximumThumbnailDepth` | Not available | Supported | Net New |
| `options.trimToTransparency` | Not available | Supported | Net New |

For a complete field-by-field reference, see [Manifest Response Migration](manifest-response-migration.md).

### Guide

[Manifest Migration](manifest-migration.md) · [Manifest Response Migration](manifest-response-migration.md)

## 5. Artboard creation

**V1 Endpoint:** `/pie/psdService/artboardCreate`

**V2 Endpoint:** `/v2/create-artboard`

### V1 behavior

V1 `artboardCreate` accepted a flat list of input images and created a new PSD with one artboard per image. Images were specified in the top-level `inputs[]` array alongside output configuration.

### V2 behavior

V2 `/v2/create-artboard` uses a dedicated `images[]` array where each entry has a `source` object for the input and `id` for ordering. Artboard spacing is configurable via `artboardSpacing`. The request follows the standard V2 envelope with `outputs[]`.

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Input specification | `inputs[].href` + `storage` | `images[].source.url` | Breaking Change |
| Image identifier | Order-based (array index) | `images[].id` field | Breaking Change |
| Artboard spacing control | Not available | `artboardSpacing` field | Net New |
| At least one image required | Not enforced | Validated — error if `images[]` is empty | Breaking Change |

### Guide

[Artboard Migration](artboard-migration.md)

## 6. Job status

**V1 Endpoints:** `/pie/psdService/status/{jobId}`, `/lrService/status/{jobId}`

**V2 Endpoint:** `/v2/status/{jobId}`

### V1 behavior

Each V1 service had its own status endpoint. Photoshop jobs used `/pie/psdService/status/{jobId}`; Lightroom jobs used `/lrService/status/{jobId}`. Status responses were service-specific in structure.

### V2 behavior

All V2 jobs use a single `/v2/status/{jobId}` endpoint regardless of which operation created the job. The response includes a `status` field (`pending`, `running`, `succeeded`, `failed`), an `outputs` array with per-output status and destination URLs, and a structured `errors` array.

### Behavioral changes

| Behavior | V1 | V2 | Type |
|----------|----|----|------|
| Endpoint per service | Separate endpoints for PS and LR | Single `/v2/status/{jobId}` | Breaking Change |
| Status field name | Varies by service | `status` (consistent) | Breaking Change |
| Output URLs in status response | Varies | `outputs[].destination.url` | Breaking Change |
| Error structure | Varies | Structured `errors[]` array | Breaking Change |

### Guide

[Status Migration](status-migration.md)

## 7. Cross-cutting changes

These changes apply to **all V2 endpoints**.

### Base URLs

| Environment | V1 Base URL | V2 Base URL |
|-------------|-------------|-------------|
| Production | `https://image.adobe.io` | `https://photoshop-api.adobe.io` |

### Request structure

| Element | V1 | V2 |
|---------|----|----|
| Input | `inputs[0].href` + `"storage": "external"` | `image.source.url` |
| Storage type discriminant | `"storage": "external"` / `"s3"` / `"azure"` / etc. | Implicit from destination object shape |
| Operations block | `options` | `edits` (for composite/document ops) or top-level fields (for edit ops) |
| Output destination | `outputs[0].href` + `storage` | `outputs[0].destination.url` |
| Output format | `"type": "image/jpeg"` | `"mediaType": "image/jpeg"` |

### Storage options

| Storage Type | V1 | V2 |
|---|---|---|
| Presigned URL (S3) | `"storage": "external"` | `{"url": "..."}` in destination |
| Azure Blob | `"storage": "azure"` | `{"url": "..."}` in destination |
| Dropbox | `"storage": "dropbox"` | `{"url": "..."}` in destination |
| Creative Cloud | `"storage": "adobe"` | `{"creativeCloudPath": "..."}` or `{"creativeCloudFileId": "..."}` |
| Embedded | Not available | `{"embedded": "base64"}` / `{"embedded": "string"}` / `{"embedded": "json"}` |
| Hosted (Adobe-managed) | Not available | `{"hosted": true, "hostedExpiresInSeconds": N}` |
| AWS S3 `storage` field | `"storage": "s3"` (deprecated) | Use presigned URL pattern instead |

<InlineAlert variant="info" slots="text"/>

Authentication is **unchanged** between V1 and V2. Continue using your existing OAuth Server-to-Server credentials.

### Output format changes

| Format | V1 | V2 | Type |
|--------|----|-----|------|
| JPEG quality | Numeric `1–100` | String enum: `"low"`, `"medium"`, `"high"`, `"maximum"` | Breaking Change |
| PNG compression | Scale `0–2` (3 levels) | Scale `"default"`, or `0–9` (10 levels) | Breaking Change |
| TIFF compression | Named string | Named string (unchanged) | Unchanged |
| PSD output | Supported | Supported (unchanged) | Unchanged |
| Cloud PSD (`.psdc`) | Supported via Sensei engine | `mediaType: "document/vnd.adobe.cpsd+dcxucf"` | Renamed |
| ICC profile per output | Not available | `iccProfile: {standard: "..."}` or `{custom: {...}}` | Net New |

### Error response structure

V2 errors use a consistent structure across all endpoints:

```json
{
  "errors": [
    {
      "code": "INPUT_EXCEEDS_MAX_SIZE",
      "message": "Input file exceeds maximum allowed size of 100MB"
    }
  ]
}
```

V1 error structures varied by service.

### Guide

[Output Types Migration](output-types-migration.md) · [ICC Profile Migration](icc-profile-migration.md) · [Storage Solutions](/getting-started/storage-solutions/index.md)

## 8. Breaking changes checklist

Use this list to audit your codebase for required V2 changes.

### Authentication and connectivity

- [ ] Update base URL from `image*.adobe.io` to `photoshop-api*.adobe.io`
- [ ] Authentication credentials are unchanged — no action needed

### Request structure

- [ ] Replace `inputs[0].href` + `"storage"` with `image.source.url`
- [ ] Replace `options` block with `edits` (for composite/document) or top-level fields (for edit)
- [ ] Replace `outputs[0].href` + `"storage"` with `outputs[0].destination.url` (or `embedded`/`hosted`)
- [ ] Replace `"type": "image/jpeg"` with `"mediaType": "image/jpeg"` in outputs

### Endpoint changes

- [ ] All `/lrService/*` calls → `/v2/edit`
- [ ] `/pie/psdService/renditionCreate` → `/v2/create-composite`
- [ ] `/pie/psdService/documentCreate` → `/v2/create-composite`
- [ ] `/pie/psdService/documentOperations` → `/v2/create-composite`
- [ ] `/pie/psdService/photoshopActions` → `/v2/execute-actions`
- [ ] `/pie/psdService/actionJSON` → `/v2/execute-actions`
- [ ] `/pie/psdService/productCrop` → `/v2/execute-actions` (with published action file)
- [ ] `/pie/psdService/splitView` → `/v2/execute-actions` (with published action file)
- [ ] `/pie/psdService/sideBySide` → `/v2/execute-actions` (with published action file)
- [ ] `/pie/psdService/artboardCreate` → `/v2/create-artboard`
- [ ] `/pie/psdService/documentManifest` → `/v2/generate-manifest`
- [ ] `/pie/psdService/status/{jobId}` → `/v2/status/{jobId}`
- [ ] `/lrService/status/{jobId}` → `/v2/status/{jobId}`

### Action requests

- [ ] Add `options[].type` discriminant (`"photoshopActions"`, `"actionJSON"`, `"uxp"`)
- [ ] Move action file reference to `options[].photoshopAction.source.url`
- [ ] Move inline ActionJSON to `options[].actionJSON.commands`

### Layer operation requests

- [ ] Add `operation.type` field to each layer operation (`"add"`, `"edit"`, `"delete"`, `"move"`)
- [ ] Rename layer types in requests: `layerSection` → `group_layer`, `textLayer` → `text_layer`, `smartObject` → `smart_object_layer`, `fillLayer` → `solid_color_layer` (creating a new document with a group layer is not yet supported — upcoming feature; editing an existing document to add a layer inside a group is supported — use `into` + `referenceLayer`)
- [ ] Replace `locked: true` with `protection: ["all"]`

### Manifest response parsing

- [ ] Update layer type string comparisons (camelCase → snake_case); expect background as `background_layer` (no `typeAttributes` on background entries)
- [ ] Update bounds parsing: drop `height`/`width`, compute from `{left, top, right, bottom}`
- [ ] Update thumbnail parsing: plain string → `{mediaType, url}` object
- [ ] Update `mask` field access → `pixelMask`; `offset.x/y` → `offset.horizontal/vertical`
- [ ] Update `locked` boolean → `protection` array
- [ ] Update artboard traversal: children under `layers[]` not `children[]`
- [ ] Update smart object parsing: flat → nested `smartObjectData.fileInfo.*`
- [ ] Update document field names: `bitDepth` → `depth`, `iccProfileName` → `iccProfile`, `name` → `title`

### Output format

- [ ] Replace numeric JPEG quality values with string enums (`7` → `"maximum"`, etc.)
- [ ] Update PNG compression range if using values above `2`

## See also

- [What's New in V2](v2-whats-new.md) — Net new capabilities framed positively
- [Migration Overview](index.md) — Architectural rationale
- [Quick Reference](index.md) — Endpoint mapping table
- [LLM Migration Reference](llm-migration-reference.md) — Consolidated reference for AI-assisted migration
