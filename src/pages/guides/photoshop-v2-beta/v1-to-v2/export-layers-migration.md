---
title: Export Layers Migration
description: Migrate exporting one or more layers from a document to the V2 create-composite endpoint
hideBreadcrumbNav: true
keywords:
  - export layers
  - layer export
  - single-layer
  - multi-layer
  - migration
  - v1 to v2
---

# Export Layers Migration Guide

## Overview

This guide describes how to migrate **exporting one or more layers** from a document to the V2 `/v2/create-composite` endpoint: schema changes, enum support for single-layer export, PSD support (single-layer only; multi-layer does not support PSD as of now), default quality and compression, and sample V1/V2 requests.

## Key differences (single-layer vs multi-layer export)

- **Single-layer export** – One layer in `output.layers`; export that layer's pixels. Supports JPEG, PNG, TIFF, and PSD.
- **Multi-layer export** – Two or more layers in `output.layers`; composite those layers to one raster file. Supports JPEG, PNG, and TIFF only. **PSD is not supported for multi-layer export as of now.**

<HorizontalLine />

## Enum support (V2)

### Crop mode (`cropMode`)

Controls the output bounding box for exported content. Supported for single-layer, multi-layer, and document export, with one restriction: `layer_bounds` is only valid for single-layer export.

| Value | Description | Single-layer | Multi-layer | Document export |
|-------|-------------|:---:|:---:|:---:|
| `layer_bounds` | Use the layer's own bounds (default for single-layer export). | Yes | No | No |
| `trim_to_transparency` | Crop to tight bounds of non-transparent pixels. | Yes | Yes | Yes |
| `document_bounds` | Use full document (or artboard) bounds (default for document/multi-layer export). | Yes | Yes | Yes |

<InlineAlert variant="info" slots="text"/>

Using `layer_bounds` with multi-layer or document export returns a validation error. Use `trim_to_transparency` or `document_bounds` instead.

### Media type (`mediaType`)

For single-layer export, V2 supports: `image/jpeg`, `image/png`, `image/tiff`, `image/vnd.adobe.photoshop` (PSD). See [Output Types Migration](output-types-migration.md) for full enum details.

<HorizontalLine />

## Defaults when exporting layers

- **JPEG quality (when omitted):** `photoshop_max`. Allowed values: `very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, `photoshop_max`.
- **PNG compression (when omitted):** `default` (level 6); you can also set `medium`, `maximum`, etc. See [Output Types Migration – PNG](output-types-migration.md#png-output-migration).

<HorizontalLine />

## ICC profile support for layer export

Both single-layer and multi-layer exports support the optional `iccProfile` field on the output. This enables ICC color space conversion (e.g., sRGB, Adobe RGB, grayscale, or custom profiles) when exporting specific layers.

- Works with supported layer export formats that support ICC: JPEG, TIFF, PSD for single-layer; JPEG, TIFF for multi-layer (**PNG does not support ICC profiles**)
- Each output in a request can have its own independent `iccProfile`
- Mixed outputs are supported: some with `iccProfile`, some without, in the same request
- Supports both standard and custom ICC profiles (see [ICC Profile Migration](icc-profile-migration.md) for full schema details)

### Example: single-layer export with ICC profile

```json
{
  "outputs": [{
    "destination": {"url": "https://example.com/out.tif"},
    "mediaType": "image/tiff",
    "layers": [{"id": 1096}],
    "iccProfile": {
      "type": "standard",
      "name": "sRGB IEC61966-2.1"
    }
  }]
}
```

### Example: multi-layer export with ICC profile

```json
{
  "outputs": [{
    "destination": {"url": "https://example.com/out.jpg"},
    "mediaType": "image/jpeg",
    "layers": [{"id": 1096}, {"id": 996}],
    "quality": "high",
    "iccProfile": {
      "type": "standard",
      "name": "Adobe RGB (1998)"
    }
  }]
}
```

<HorizontalLine />

## Sample: single-layer export

### V1 (example)

```bash
curl -X POST "https://image.adobe.io/pie/psdService/renditionCreate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{"href": "https://my-bucket.s3.amazonaws.com/input.psd", "storage": "external"}],
    "outputs": [{
      "href": "https://my-bucket.s3.amazonaws.com/out.png",
      "storage": "external",
      "type": "image/png",
      "layers": [{"id": 1096}],
      "compression": "medium"
    }]
  }'
```

### V2 (example)

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/create-composite" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {"source": {"url": "https://my-bucket.s3.amazonaws.com/input.psd"}},
    "outputs": [{
      "destination": {"url": "https://my-bucket.s3.amazonaws.com/out.png"},
      "mediaType": "image/png",
      "layers": [{"id": 1096}],
      "cropMode": "trim_to_transparency",
      "compression": "medium"
    }]
  }'
```

**Schema changes (single-layer):** `inputs[].href` → `image.source.url`; `outputs[].href` → `outputs[].destination.url`; `outputs[].type` → `outputs[].mediaType`; `outputs[].layers` remains per output. Optional in V2: `cropMode`, `quality` / `compression` as string enums.

<HorizontalLine />

## Sample: multi-layer export

### V1 (example)

```bash
curl -X POST "https://image.adobe.io/pie/psdService/renditionCreate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{"href": "https://my-bucket.s3.amazonaws.com/input.psd", "storage": "external"}],
    "outputs": [{
      "href": "https://my-bucket.s3.amazonaws.com/out.jpg",
      "storage": "external",
      "type": "image/jpeg",
      "layers": [{"id": 1096}, {"id": 996}],
      "quality": 7
    }]
  }'
```

### V2 (example)

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/create-composite" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {"source": {"url": "https://my-bucket.s3.amazonaws.com/input.psd"}},
    "outputs": [{
      "destination": {"url": "https://my-bucket.s3.amazonaws.com/out.jpg"},
      "mediaType": "image/jpeg",
      "layers": [{"id": 1096}, {"id": 996}],
      "quality": "maximum",
      "cropMode": "trim_to_transparency"
    }]
  }'
```

**Schema changes (multi-layer):** Same as above. **Note:** Multi-layer export does not support PSD as of now; use `mediaType`: `image/jpeg`, `image/png`, or `image/tiff` only. `cropMode` supports `trim_to_transparency` and `document_bounds` (not `layer_bounds`). Use string enums for `quality` (e.g. `maximum`, `photoshop_max`) and `compression` for PNG.

<HorizontalLine />

## Migration checklist for export layers

- [ ] Use `outputs[].destination.url`, `outputs[].mediaType`, and `outputs[].layers` (V2 shape).
- [ ] For multi-layer export, do not request PSD; use JPEG, PNG, or TIFF.
- [ ] `cropMode` `trim_to_transparency` and `document_bounds` work for all export types; `layer_bounds` is single-layer only.
- [ ] Use string enums for `quality` (JPEG) and `compression` (PNG); omit for defaults (`photoshop_max` / `default`).
- [ ] `iccProfile` is optional on layer exports — add if you need color space conversion (see [ICC Profile Migration](icc-profile-migration.md)).

<HorizontalLine />

## Related guides

- [Output Types Migration](output-types-migration.md) – JPEG quality and PNG compression enums, media types, and structural changes for all outputs
- [ICC Profile Migration](icc-profile-migration.md) – ICC profile schema, standard/custom profiles, and format support
- [Layer Operations Overview](layer-operations-overview.md) – Introduction to layer operations in V2
- [Composite Migration](composite-migration.md) – Create-composite endpoint and layer operations
- [Migration Overview](index.md) – Full V1 to V2 migration overview

<HorizontalLine />

**Last Updated:** March 2026
