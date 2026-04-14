---
title: Key Improvements and Architecture with v2
description: Understand details about the architectural and service improvements that were made in the Photoshop API v2.
hideBreadcrumbNav: true
keywords:
  - v1 to v2
  - architecture
  - migration overview
  - API consolidation
---

# Key Improvements and Architecture with v2

Understand the key service improvements with the v2 API.

This page explains the main architectural and service improvements in the Photoshop API v2 so you can see what changed and why migrating is beneficial.
These sections outline the major improvements on all endpoint in these areas:

- **Combined operations** – Apply multiple edits in a single request instead of multiple API calls.
- **Flexible storage options** – Embedded, hosted, presigned, and Creative Cloud storage.
- **Published action files** – Inspect and customize the action definitions behind convenience workflows.
- **Enhanced layer operations** – Richer layer control via the create-composite endpoint.
- **Improved error handling** – Clearer error codes, multiple validation details, and a consistent error shape.

When you're ready to begin the migration process, start with the [V1 to V2 Migration Guide overview](index.md).

## Combined operations

The v1 API required multiple calls to apply different operations. For example, to apply auto tone and auto straighten, you would need to make three separate API calls.

```shell
# Step 1: Apply auto tone
curl -X POST https://image.adobe.io/lrService/autoTone ...

# Step 2: Apply auto straighten
curl -X POST https://image.adobe.io/lrService/autoStraighten ...

# Step 3: Adjust exposure
curl -X POST https://image.adobe.io/lrService/applyEdits ...
```

The v2 API allows you to combine multiple operations in a single call.

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
  "autoTone": true,
  "autoStraighten": {
    "enabled": true
  },
  "light": {
    "exposure": 1.2
  },
  "outputs": [...]
}'
```

## Flexible storage options

V2 introduces new storage options beyond presigned URLs:

- **Embedded Storage** - Get results inline (base64, string, or JSON)
- **Hosted Storage** - Adobe-managed temporary storage with configurable validity
- **Presigned URLs** - Enhanced support for Azure, Dropbox, and external storage
- **Creative Cloud Storage** - Direct integration with Creative Cloud paths

See the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for detailed information.

## Published action files

Convenience APIs for specific workflows in v1, like `productCrop`, `depthBlur`, `splitView`, and `sideBySide` used hidden server-side action files.

In v2, these action files are now published and available to you:

**Benefits:**

- Examine the exact action definitions Adobe uses
- Customize and tweak actions for your specific needs
- Learn from Adobe's implementations
- Create your own similar functionality

**Specific Workflow Migration Guides:**

- [Product Crop Migration](convenience-apis/product-crop.md) - Auto-crop products with customizable padding.
- [Split View Migration](convenience-apis/split-view.md) - Before/after comparisons with divider line.
- [Side by Side Migration](convenience-apis/side-by-side.md) - Simple before/after comparisons.

See the [Actions Migration Guide](actions-migration.md) for general information about using actions in v2.

## Enhanced layer operations

The v2 `/create-composite` endpoint provides more comprehensive layer manipulation:

- Add, delete, and move layers with precise control
- Support for adjustment layers
- Smart object transformations
- Text layer editing
- Layer masks and blending options

## Improved error handling

V2 provides more detailed error messages and validation:

- Clear error codes for each validation failure
- Multiple error details in a single response
- Better context for troubleshooting
- Consistent error structure across all endpoints

## Next steps

Review the [quick reference table in the V1 to V2 Migration Guide overview](index.md#service-migration-reference) when you're ready to begin the migration.
