---
title: Convenience APIs Migration
description: Migration guides for V1 convenience API endpoints to V2 execute-actions
hideBreadcrumbNav: true
keywords:
  - convenience APIs
  - product crop
  - split view
  - side by side
  - depth blur
  - text layer
  - migration
  - v1 to v2
---

# Convenience APIs migration

V1 provided several convenience API endpoints that wrapped predefined Photoshop action files for common operations. In V2, these operations use the `/v2/execute-actions` endpoint with published ActionJSON definitions that you can inspect and customize.

## Migration guides

- [Product Crop](product-crop.md) — Migrate from `/pie/psdService/productCrop` to `/v2/execute-actions` with published ActionJSON for auto-crop and padding
- [Split View](split-view.md) — Migrate from `/pie/psdService/splitView` to `/v2/execute-actions` for masked before/after comparisons with branding
- [Side by Side](side-by-side.md) — Migrate from `/pie/psdService/sideBySide` to `/v2/execute-actions` for side-by-side layout comparisons
- [Depth Blur](depth-blur.md) — Reference for `/pie/psdService/depthBlur` migration (Neural Filters not yet supported in V2)
- [Text Layer Operations](text-layer-operations.md) — Migrate from `/pie/psdService/text` to `/v2/execute-actions` using ActionJSON or UXP scripts

## Key changes

- V1 convenience endpoints used server-side action files. V2 publishes these ActionJSON definitions so you can examine, fork, and customize them.
- All convenience operations now use a single endpoint: `/v2/execute-actions`
- Some operations (Split View, Side by Side) require `additionalContents` for supplementary images
- Depth Blur is the only convenience API not yet available in V2 (Neural Filters dependency)
