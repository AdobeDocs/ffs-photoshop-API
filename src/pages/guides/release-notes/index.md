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

## August 12, 2026

### Features

- **DNG exports** via `/v2/edit` now support CAI/C2PA signing, consistent with existing JPEG and PNG export paths.
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
- CAI-compatible PNG exports are now supported alongside JPEG for C2PA-signed outputs.
- `/v2/create-artboard` now accepts an optional `name` field on each `images` array entry to set explicit artboard names.

### Bug Fixes

- Improved error reporting for layer transform operations that exceed output size limits — now returns a descriptive `layer_operation_failed` error instead of an opaque `unknown` error.
- Corrupt or truncated PSDC inputs now return a structured `FILE_CORRUPTED` or `FILE_FORMAT_UNSUPPORTED` error instead of propagating an unhandled exception.
- Corrected smart object placement via `/v2/create-composite` — source images are no longer stretched to fill the canvas when added.
