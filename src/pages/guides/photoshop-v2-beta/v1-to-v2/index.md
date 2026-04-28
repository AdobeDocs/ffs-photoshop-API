---
title: Migration to v2 Overview
description: Learn what's changing and how to migrate from v1 Photoshop and Lightroom APIs to the unified v2 API architecture.
hideBreadcrumbNav: true
keywords:
  - v1 to v2
  - migration
  - API upgrade
  - Photoshop API
  - Lightroom API
---

# Migration to v2 Overview

This overview helps you understand the general changes and how to prepare for the migration from the legacy v1 Photoshop and Lightroom APIs to the new unified v2 API.

## What's different?

The Photoshop and Lightroom API v2 represents a significant improvement over v1.

For all the details about the new architecture and powerful new service improvements, see the [Key Improvements and Architecture with v2](./key-improvements.md) page.

**Unified architecture**

- All Photoshop and Lightroom operations are now served from a single, unified API
- Consistent request/response patterns across all endpoints
- Simplified authentication and error handling

**Improved capabilities**

- Combine multiple operations in a single API call
- More flexible output options with embedded, hosted, and external storage
- Enhanced layer manipulation and document editing
- Support for custom actions and scripts

**Better performance**

- Optimized processing pipeline
- Reduced latency for common operations
- More efficient resource utilization

## What are the breaking changes?

The v2 API introduces some breaking changes:

**Base URL change**

- Photoshop API v2 uses `photoshop-api*.adobe.io` domains instead of `image*.adobe.io`.

**Request payload structure changes**

- Field renaming and restructuring across all endpoints.

**Output format changes**

- JPEG quality now uses string enums instead of numbers (7 is now "maximum").
- PNG compression is expanded from 3 to 10 levels.

**Response format modifications**

- Updated status and result structures.

**Different output configuration options** - New destination object structure, with an optional `storageType`.

- **New required fields in some cases**

- Required fields now include `mediaType` (was `type`) and `destination` (was `href`).

**Deprecated fields**

- The `storage` field for AWS S3 is deprecated.
- Numeric quality values for JPEG are no longer supported.

Review the detailed migration guides for each endpoint type to understand the specific impacts to your integration and how to migrate.

## What about authentication?

Authentication remains unchanged. Continue using your existing OAuth Server-to-Server credentials with the new v2 endpoints. See the [Authentication Guide](../../../getting-started/index.md) for more information.

## How should I begin migrating?

1. **[Read the Key Improvements and Architecture with v2](./key-improvements.md)** to understand the architectural changes
2. **Review storage options** in the [enhanced storage solutions guide](../../../getting-started/storage-solutions/index.md)
3. **Choose your migration path** based on the endpoints you currently use (see the reference table below):
   - **Lightroom Operations:**
     - [Edit Operations](edit-operations.md) - Lightroom editing operations (autoTone, presets, XMP, etc.)
   - **Document Operations:**
     - [Format Conversion](format-conversion-migration.md) - Converting PSDs to other formats (renditionCreate) and PSDC Engine migration
     - [Document Creation](document-creation-migration.md) - Creating new blank documents (documentCreate)
     - [Document Operations](document-operations-migration.md) - Document-level operations like crop, resize, trim (documentOperations)
   - **Layer Operations:**
     - [Layer Operations Overview](layer-operations-overview.md) - Introduction to layer operations in V2
     - [Image Layer Operations](layer-operations-image.md) - Image and solid color layers
     - [Text Layer Operations](layer-operations-text.md) - Text layers with styling
     - [Adjustment Layer Operations](layer-operations-adjustments.md) - Non-destructive adjustments
     - [Smart Object Operations](layer-operations-smart-objects.md) - Smart object layers
     - [Advanced Layer Operations](layer-operations-advanced.md) - Masks, groups, transforms, blend modes
   - **Other Operations:**
     - [Actions Migration](actions-migration.md) - Photoshop actions and convenience APIs
     - [Output Types Migration](output-types-migration.md) - JPEG, PNG, PSD, TIFF output format changes
     - [Artboard Migration](artboard-migration.md) - Artboard operations
     - [Manifest Migration](manifest-migration.md) - Manifest generation
     - [Status Migration](status-migration.md) - Job status checking
4. **Test your migration** with non-production workloads
5. **Update your production systems** once testing is complete

### Service migration reference

Use this table to quickly find the v2 equivalent for your v1 endpoints:

| V1 Endpoint                          | V2 Endpoint             | Guide                                                     |
| ------------------------------------ | ----------------------- | --------------------------------------------------------- |
| `/lrService/autoTone`                | `/v2/edit`              | [Edit Operations](edit-operations.md)                     |
| `/lrService/autoStraighten`          | `/v2/edit`              | [Edit Operations](edit-operations.md)                     |
| `/lrService/presets`                 | `/v2/edit`              | [Edit Operations](edit-operations.md)                     |
| `/lrService/xmp`                     | `/v2/edit`              | [Edit Operations](edit-operations.md)                     |
| `/lrService/edit`                    | `/v2/edit`              | [Edit Operations](edit-operations.md)                     |
| `/pie/psdService/smartObject`        | `/v2/create-composite`  | [Smart Object](guides-v2/smart-object-workflow.md)        |
| `/pie/psdService/renditionCreate`    | `/v2/create-composite`  | [Format Conversion](format-conversion-migration.md)       |
| `/pie/psdService/documentCreate`     | `/v2/create-composite`  | [Document Creation](document-creation-migration.md)       |
| `/pie/psdService/documentOperations` | `/v2/create-composite`  | [Document Operations](document-operations-migration.md)   |
| `/pie/psdService/photoshopActions`   | `/v2/execute-actions`   | [Actions Migration](actions-migration.md)                 |
| `/pie/psdService/actionJSON`         | `/v2/execute-actions`   | [Actions Migration](actions-migration.md)                 |
| `/pie/psdService/productCrop`        | `/v2/execute-actions`   | [Product Crop](convenience-apis/product-crop.md)          |
| `/pie/psdService/artboardCreate`     | `/v2/create-artboard`   | [Artboard Migration](artboard-migration.md)               |
| `/pie/psdService/documentManifest`   | `/v2/generate-manifest` | [Manifest Migration](manifest-migration.md)               |
| `/pie/psdService/status/{jobId}`     | `/v2/status/{jobId}`    | [Status Migration](status-migration.md)                   |
| `/lrService/status/{jobId}`          | `/v2/status/{jobId}`    | [Status Migration](status-migration.md)                   |
| Layer operations                     | `/v2/create-composite`  | [Layer Operations](composite-migration.md) (see sub-guides) |

## Need help?

If you encounter issues during migration:

- Review the detailed guides for your specific endpoints
- Check the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for storage-related questions
- Contact the Adobe DI ART Service team for technical support
