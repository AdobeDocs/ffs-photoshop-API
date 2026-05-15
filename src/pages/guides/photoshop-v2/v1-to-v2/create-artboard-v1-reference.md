---
title: Create Artboard — Complete V1 Migration Reference
description: Field-level V1 vs V2 comparison for the artboardCreate endpoint migrating to /v2/create-artboard
hideBreadcrumbNav: true
keywords:
  - create-artboard
  - artboardCreate
  - artboards
  - migration reference
  - v1 to v2
---

# Create Artboard — Complete V1 Migration Reference

This page is the authoritative single-page field-level reference for migrating from the V1
`/pie/psdService/artboardCreate` endpoint to `/v2/create-artboard`.

For a guided walkthrough with examples and best practices, see [Artboard Migration](artboard-migration.md).

## 1. Endpoint and base URL

| | V1 | V2 |
|---|---|---|
| **Endpoint** | `POST /pie/psdService/artboardCreate` | `POST /v2/create-artboard` |
| **Base URL** | `https://image.adobe.io` | `https://photoshop-api.adobe.io` |
| **Status check** | `GET /pie/psdService/status/{jobId}` | `GET /v2/status/{jobId}` |

## 2. Request envelope

<InlineAlert variant="warning" slots="text"/>

**The top-level V1 request structure has no equivalent in V2.** V1 wrapped input images under `options.artboard[]`; V2 uses a top-level `images[]` array. The `options` container is completely removed.

**V1:**

```json
{
  "options": {
    "artboard": [
      {"href": "<IMAGE_1_URL>", "storage": "external"},
      {"href": "<IMAGE_2_URL>", "storage": "external"}
    ]
  },
  "outputs": [...]
}
```

**V2:**

```json
{
  "images": [
    {"source": {"url": "<IMAGE_1_URL>"}},
    {"source": {"url": "<IMAGE_2_URL>"}}
  ],
  "artboardSpacing": 50,
  "outputs": [...]
}
```

| V1 field | V2 field | Notes |
|---|---|---|
| `options.artboard[]` | `images[]` | Breaking: `options` wrapper removed |
| `outputs[]` | `outputs[]` | Same top-level location |
| *(not in V1)* | `artboardSpacing` | New: integer, pixels, optional (default 50) |

## 3. Input image fields

### Field mapping

| V1 (`options.artboard[n].*`) | V2 (`images[n].source.*`) | Notes |
|---|---|---|
| `href` (any URL) | `url` (presigned HTTPS URL) | Breaking: renamed, nested under `source` |
| `storage: "external"` | *(omit storageType)* | External URLs: no storage type needed |
| `storage: "adobe"` + CC path | `creativeCloudPath: "folder/file.jpg"` | Breaking: explicit CC path field, **no leading slash** |
| `storage: "adobe"` + URN | `creativeCloudFileId: "urn:aaid:sc:…"` | Breaking: explicit CC file ID field |
| `storage: "acp"` | `url` (ACP presigned URL) | Use presigned URL directly |
| `storage: "azure"` | `url` (Azure presigned URL) | Input side: no storageType needed |
| `storage: "dropbox"` | `url` (Dropbox URL) | Input side: no storageType needed |
| `storage: "cclib"` | `creativeCloudFileId: "urn:aaid:sc:…"` | CC Library → file ID |
| *(not in V1)* | `lightroomPath` | New: Lightroom catalog path |

### Array constraints

| | V1 | V2 |
|---|---|---|
| Minimum images | 1 | 1 |
| Maximum images | Not documented | **25** (error returned if exceeded) |

<InlineAlert variant="warning" slots="text"/>

**V2 enforces a maximum of 25 input images.** V1 had no documented limit. If your workflow sends more than 25 images, you must split requests. Error returned: `"images must contain between 1 and 25 items"`

### Storage to source mapping examples

**External presigned URL (S3, Frame.io, Google Drive):**

```json
// V1
{"href": "<PRESIGNED_URL>", "storage": "external"}

// V2
{"source": {"url": "<PRESIGNED_URL>"}}
```

**Creative Cloud path:**

```json
// V1
{"href": "/path/to/image.jpg", "storage": "adobe"}

// V2 — note: no leading slash in V2
{"source": {"creativeCloudPath": "path/to/image.jpg"}}
```

**Creative Cloud file ID:**

```json
// V1
{"href": "urn:aaid:sc:US:...", "storage": "adobe"}

// V2
{"source": {"creativeCloudFileId": "urn:aaid:sc:US:..."}}
```

## 4. Artboard spacing

| Field | V1 | V2 |
|---|---|---|
| `artboardSpacing` | Not present | Optional integer, pixels |
| Default | N/A | 50 pixels |
| Location | N/A | Top-level sibling to `images` and `outputs` |

Images are arranged horizontally left-to-right. The spacing applies between each pair of adjacent
artboards. Total output width = sum of image widths + (spacing × (image count − 1)).

## 5. Output fields

<InlineAlert variant="warning" slots="text"/>

**Three V1 boolean output fields are replaced by a single enum in V2:** `overwrite: boolean` → `shouldOverwrite: boolean` (renamed); `trimToCanvas: boolean` → use `cropMode: "trim_to_transparency"` or `"document_bounds"`; `trimToLayer: boolean` → use `cropMode: "layer_bounds"`.

| V1 field | V2 field | Notes |
|---|---|---|
| `href` | `destination.url` | Breaking: nested in `destination` |
| `storage` | `destination.storageType` (Azure/Dropbox only) | Breaking: removed for most types |
| `type` | `mediaType` | Breaking: renamed |
| `quality` (number 1–7) | `quality` (string enum) | Breaking: type changed |
| `compression` (`small`/`medium`/`large`) | `compression` (10-level enum) | Breaking: values changed |
| `width` | `width` | Unchanged |
| `maxWidth` | `maxWidth` | Unchanged |
| `overwrite` | `shouldOverwrite` | Breaking: renamed |
| `trimToCanvas` | *(removed)* | Breaking: use `cropMode` |
| `trimToLayer` | *(removed)* | Breaking: use `cropMode` |
| *(not in V1)* | `height` | New: explicit output height |
| *(not in V1)* | `cropMode` | New: `trim_to_transparency`, `document_bounds`, `layer_bounds` |
| `layers` | `layers` (max 100 items) | Same concept; V2 enforces 100 item limit |
| `iccProfile` | `iccProfile` (not for PSDC output) | Same concept; V2 restricts PSDC |

### Output array constraints

Both V1 and V2 require 1–25 outputs per request.

## 6. JPEG quality mapping

| V1 (numeric) | V2 (string enum) |
|---|---|
| 1 | `"very_poor"` |
| 2 | `"poor"` |
| 3–4 | `"medium"` |
| 5–6 | `"high"` |
| 7 | `"maximum"` |
| *(not in V1)* | `"low"` |
| *(not in V1)* | `"photoshop_max"` |

<InlineAlert variant="info" slots="text"/>

Use `"photoshop_max"` as the default for production workflows — it produces the highest quality JPEG output. Passing a numeric value (e.g., `7`) will return a validation error in V2.

## 7. PNG compression mapping

| V1 (string) | V2 (string) | Level |
|---|---|---|
| `"small"` | `"maximum"` | Highest compression, smallest file |
| `"medium"` | `"medium"` | Balanced |
| `"large"` | `"low"` | Least compression, largest file |
| *(not in V1)* | `"none"` | No compression |
| *(not in V1)* | `"very_low"` | |
| *(not in V1)* | `"medium_low"` | |
| *(not in V1)* | `"medium_high"` | |
| *(not in V1)* | `"default"` | Level 6 (library default) |
| *(not in V1)* | `"high"` | |
| *(not in V1)* | `"very_high"` | |

## 8. Supported output formats

| Format | V1 `type` | V2 `mediaType` | Notes |
|---|---|---|---|
| JPEG | `image/jpeg` | `image/jpeg` | |
| PNG | `image/png` | `image/png` | |
| TIFF | `image/tiff` | `image/tiff` | |
| PSD | `image/vnd.adobe.photoshop` or `vnd.adobe.photoshop` | `image/vnd.adobe.photoshop` | V2 normalizes |
| PSDC | Not supported | `document/vnd.adobe.cpsd+dcxucf` | **New in V2** |
| PSDC (alternate) | Not supported | `document/vnd.adobe.cpsd+dcx` | **New in V2** |

## 9. Destination types (V2 new capability)

V1 used `href` + `storage` enum. V2 uses a typed `destination` union:

| Destination type | Fields | When to use |
|---|---|---|
| **URL** | `url` (required), `storageType` (`azure`/`dropbox`, optional) | S3, Azure, Dropbox, Frame.io presigned URLs |
| **Creative Cloud** | `creativeCloudPath` (required), `creativeCloudProjectId` (optional) | ACP / CC storage |
| **Hosted** | `validityPeriod` (required, 60–86400 seconds) | Adobe-managed temporary storage; no pre-existing bucket needed |

### Destination mapping from V1 storage

| V1 output `storage` | V2 `destination` |
|---|---|
| `"external"` | `{"url": "<presigned URL>"}` |
| `"acp"` | `{"url": "<ACP presigned URL>"}` |
| `"adobe"` + CC path | `{"creativeCloudPath": "folder/file.psd"}` |
| `"adobe"` + URN | `{"creativeCloudFileId": "urn:aaid:sc:…"}` |
| `"azure"` | `{"url": "<Azure URL>", "storageType": "azure"}` |
| `"dropbox"` | `{"url": "<Dropbox URL>", "storageType": "dropbox"}` |
| *(not in V1)* | `{"validityPeriod": 3600}` |

<InlineAlert variant="info" slots="text"/>

Creative Cloud paths must **not** have a leading slash. Use `"folder/file.psd"`, not `"/folder/file.psd"`.

## 10. Crop mode (replaces V1 trim booleans)

V1 had two separate boolean flags on outputs. V2 consolidates into a single enum:

| V1 | V2 `cropMode` |
|---|---|
| `trimToCanvas: true` | `"document_bounds"` |
| `trimToLayer: true` | `"layer_bounds"` |
| `trimToCanvas: true` + transparent pixels | `"trim_to_transparency"` |
| Both false (default) | Omit `cropMode` |

## 11. Status response changes

The V2 status response structure is substantially different from V1:

| | V1 | V2 | Notes |
|---|---|---|---|
| **Status location** | `outputs[n].status` | `status` (top-level) | Breaking |
| **Status values** | `succeeded`, `failed`, `pending` | `pending`, `running`, `succeeded`, `failed` | `running` added |
| **Timestamps** | `outputs[n].created`, `outputs[n].modified` | `createdTime`, `modifiedTime` (top-level) | Breaking |
| **Output URL** | `outputs[n]._links.renditions[m].href` | `result.outputs[n].destination.url` | Breaking |
| **Outputs location** | `outputs[]` (top-level) | `result.outputs[]` | Breaking |
| **Input echo** | `outputs[n].input[m].href` | Not returned | Removed |
| **Error structure** | `outputs[n].errors.code` (number) | `errorDetails[n].errorCode` (string) | Breaking |
| **Hypermedia links** | `_links.self.href` | Not present | Removed |

See [Status Migration](status-migration.md) for the full status response reference.

## 12. Complete V1 → V2 request example

**V1:**

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/artboardCreate \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "options": {
    "artboard": [
      {"href": "<IMAGE_1_URL>", "storage": "external"},
      {"href": "<IMAGE_2_URL>", "storage": "external"}
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    },
    {
      "href": "<JPEG_URL>",
      "storage": "external",
      "type": "image/jpeg",
      "quality": 7,
      "width": 2000
    }
  ]
}'
```

**V2:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-artboard \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "images": [
    {"source": {"url": "<IMAGE_1_URL>"}},
    {"source": {"url": "<IMAGE_2_URL>"}}
  ],
  "artboardSpacing": 50,
  "outputs": [
    {
      "destination": {"url": "<SIGNED_POST_URL>"},
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": {"url": "<JPEG_URL>"},
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2000
    }
  ]
}'
```

**Key transformation summary:**
1. `options.artboard[]` → `images[]` (remove `options` wrapper)
2. `href` + `storage` → `source.url` (on inputs)
3. `href` + `storage` → `destination.url` (on outputs; `storageType` only for Azure/Dropbox)
4. `type` → `mediaType`
5. `quality: 7` → `quality: "maximum"`
6. Add `artboardSpacing` if custom spacing needed (default is 50)

## 13. Migration checklist

- [ ] Change `options.artboard[]` to top-level `images[]`
- [ ] Change `href` + `storage` → `source.url` on each image (or `source.creativeCloudPath` / `source.creativeCloudFileId` for CC)
- [ ] Change `outputs[].href` → `outputs[].destination.url`
- [ ] Remove `outputs[].storage` (only add `destination.storageType` for Azure or Dropbox)
- [ ] Change `outputs[].type` → `outputs[].mediaType`
- [ ] Change JPEG `quality` from numeric (1–7) to string enum (`"maximum"`, `"high"`, etc.)
- [ ] Change PNG `compression` from `small`/`medium`/`large` to V2 enum (`"maximum"`, `"medium"`, `"low"`, etc.)
- [ ] Replace `overwrite` with `shouldOverwrite`
- [ ] Replace `trimToCanvas`/`trimToLayer` booleans with `cropMode` enum
- [ ] Add `artboardSpacing` if your V1 workflow needed specific spacing
- [ ] Update status polling: `outputs[n].status` → top-level `status`; `outputs[n]._links.renditions[m].href` → `result.outputs[n].destination.url`
- [ ] Verify image count ≤ 25 (V2 enforces this limit)
- [ ] No leading slash on Creative Cloud paths

## See also

- [Artboard Migration](artboard-migration.md) — Guided walkthrough with examples and best practices
- [Output Types Migration](output-types-migration.md) — JPEG, PNG, TIFF, PSD output format details
- [ICC Profile Migration](icc-profile-migration.md) — Color management options
- [Status Migration](status-migration.md) — Job status response format
