---
title: Release Notes
description: Release notes for the Photoshop API.
keywords:
  - release notes
  - changelog
  - photoshop api
---

# Release Notes

This page lists the latest updates, improvements, and fixes for the Photoshop API.

## November 18, 2026

### Bug Fixes

- Prevented crashes from off-canvas trimmed thumbnails while preserving layer metadata in the response.

## November 4, 2026

### Features

- **`smartObject.contentPlacement`** is now an optional field on `/v2/create-composite` smart object edits, placing the replacement inside the existing frame using `fill` (crop overflow) or `fit` (transparent padding). See [Place Content In A Frame](../create-composite/smart-objects/index.md#place-content-in-a-frame).
- **WebP output** is now supported for `/v2/create-composite` document and layer exports and `/v2/generate-manifest` thumbnails, with lossy/lossless compression and quality options.

### Bug Fixes

- Corrected `trim_to_transparency` single-layer exports for artboards positioned above or left of the canvas origin.

## October 21, 2026

### Features

- The optional `x-user-token` header is now cached per-job and preferred for Typekit font downloads to resolve Adobe Fonts entitlements independently of the request's authorization identity, with fallback to the Authorization token when unavailable.

### Bug Fixes

- Prevented `/v2/generate-manifest` from crashing when an embedded smart object's metadata cannot be read.
- Corrected file downloads that failed when the server returned a blank HTTP Content-Type header.

## October 7, 2026

### Features

- **`/v2/execute-actions`** now accepts `application/json` and `text/plain` files in `additionalContents`, enabling UXP scripts to read non-image data files.
- **`/v2/execute-actions`** now accepts Creative Cloud PSD files as `image.source` inputs.

## September 23, 2026

### Bug Fixes

- Corrected the `JpegScanOptions.type` field to be optional, defaulting to baseline.
- Layer type mismatches now return a `layer_type_invalid` error instead of an opaque unknown error in `/v2/status/` responses.

## September 9, 2026

### Features

- **JPEG exports** now support baseline optimized and progressive scan encoding in addition to the previous baseline standard mode.
- **JPEG outputs** on `/v2/create-composite`, `/v2/create-artboard`, and `/v2/generate-manifest` now accept an optional `scan` field to select baseline or progressive encoding.

### Bug Fixes

- Custom and TypeKit font loading now continues with a warning on individual failures rather than aborting the entire operation.

## August 26, 2026

### Features

- **Layer effects** (drop shadow) can now be applied when adding or editing layers via `/v2/create-composite`.

### Bug Fixes

- Corrected layer isolation in `/v2/create-composite` so `outputs[].layers[]` now excludes sibling layers when exporting a layer nested inside a group.
- Prevented a `/v2/generate-manifest` crash when a document contains an embedded smart object that cannot be opened.

## August 12, 2026

### Features

- `/v2/edit` now accepts an optional `preset` boolean on `XmpOutput` to generate a portable Lightroom preset instead of a plain XMP sidecar.

## July 29, 2026

### Features

- `/v2/edit` now accepts a `lightroomPath` field for Lightroom storage input.

### Bug Fixes

- Resolved a crash in `/v2/generate-manifest` when processing PSDs containing Color Lookup adjustment layers.
- Corrected `/v2/edit` to apply XMP crop correctly, returning the cropped image.
- Resolved `/v2/execute-actions` request failures caused by file paths exceeding the maximum allowed length.

## July 7, 2026

### Features

- **Gradient fill layers** are now included in the `/v2/generate-manifest` response with full gradient properties such as angle, type, scale, and color stops.
- **XMP metadata** from embedded smart object layers is now included in the `/v2/generate-manifest` response when `includeXmp` is set.
- **Group and artboard layers** can now be exported as PSD files with the full layer hierarchy preserved.
- `/v2/create-artboard` now accepts an optional `name` field on each `images` array entry to set explicit artboard names.

### Bug Fixes

- Improved error reporting for layer transform operations that exceed output size limits — now returns a descriptive `layer_operation_failed` error instead of an opaque `unknown` error.
- Corrupt or truncated PSDC inputs now return a structured `FILE_CORRUPTED` or `FILE_FORMAT_UNSUPPORTED` error instead of propagating an unhandled exception.
- Corrected smart object placement via `/v2/create-composite` — source images are no longer stretched to fill the canvas when added.
