---
title: Layer Operations Migration Overview (v1 to v2)
description: Understanding the migration from v1 layer operations to the unified v2 approach
hideBreadcrumbNav: true
keywords:
  - layer operations
  - layers
  - composite
  - PSD
  - migration
  - v1 to v2
---

# Layer Operations Migration Overview (v1 to v2)

This guide explains how layer operations have changed from v1 to v2 and helps you navigate the migration process.

The v2 API consolidates all layer operations into the `/v2/create-composite` endpoint:

- **Single endpoint** for all layer manipulation
- **Batch operations** - combine multiple layer edits in one request
- **Atomic transactions** - all edits succeed or fail together
- **Expanded capabilities** - support for layer types not available in v1

<InlineAlert variant="warning" slots="text"/>

The v2 API currently supports only a subset of v1 functionality. Some advanced v1 features are still being migrated. Check specific guides for feature availability.

## Basic request structure

All layer operations now follow this basic request structure:

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "edits": {
    "layers": [
      {
        "type": "layer_type",
        "name": "Layer Name",
        // Layer-specific properties
        "operation": {
          "type": "add|edit|delete"
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

## Key migration changes

### Request structure changes

In the v1 API, each operation had its own endpoint structure.

In the v2 API, all layer operations are unified into a single `edits.layers` array.

```json
{
  "image": {"source": {"url": "<DOCUMENT_URL>"}},
  "edits": {
    "layers": [
      // All layer operations here
    ]
  },
  "outputs": [...]
}
```

### Operation types

The v2 API introduces explicit operation types:

- `add` - Add new layers
- `edit` - Modify existing layer properties
- `delete` - Remove layers

Move operations are now handled as edit operations with transform/bounds properties.

### Batch operations

In the v1 API, multiple sequential API calls were required to perform batch operations.

```shell
POST /endpoint1 (add layer)
POST /endpoint2 (modify layer)
POST /endpoint3 (add another layer)
```

In the v2 API, a single API call with multiple operations is now supported.

```json
{
  "edits": {
    "layers": [
      {"type": "layer", "operation": {"type": "add"}, ...},
      {"name": "Existing", "isVisible": false},
      {"type": "text_layer", "operation": {"type": "add"}, ...}
    ]
  }
}
```

## Layer processing order

In the v1 API, layers were processed from last to first (bottom-up) in the payload array.

In the v2 API, layers are processed in the order they are provided in the payload (top-down). This means that the first layer in your request array will be processed first, followed by the second, and so on. The order of layers in your API request directly affects the final composition of your document.

If a layer needs to reference another layer being created in the same payload (for example, using placement types `above`, `below`, or `into` with a `referenceLayer`), you must create the referenced layer first in the payload array before any layers that depend on it. This is a change from v1, where layers were processed in reverse order.

### Example

Consider adding two layers, where Layer B should be positioned above Layer A:

**V1 Approach:** (processed last to first)

```json
{
  "layers": [
    {
      "name": "Layer B",
      "add": { "insertAbove": { "name": "Layer A" } }
    },
    {
      "name": "Layer A",
      "add": { "insertTop": true }
    }
  ]
}
```

Layer A is created first, then Layer B references it.

**V2 Approach:** (processed first to last)

```json
{
  "edits": {
    "layers": [
      {
        "name": "Layer A",
        "type": "layer",
        "operation": {
          "type": "add",
          "placement": { "type": "top" }
        }
      },
      {
        "name": "Layer B",
        "type": "layer",
        "operation": {
          "type": "add",
          "placement": {
            "type": "above",
            "referenceLayer": { "name": "Layer A" }
          }
        }
      }
    ]
  }
}
```

Layer A must come first in the array since it's processed first and Layer B references it.

## Migration strategy

1. **Audit your V1 usage** - Identify which V1 endpoints you're currently using.
2. **Choose specific migration guides** - Navigate to the guide for each layer type.
3. **Start simple** - Migrate one operation type at a time.
4. **Test incrementally** - Validate each migration step before proceeding.
5. **Combine operations** - Once comfortable, batch multiple operations for efficiency.

## Specific layer type guides

For detailed information on working with specific layer types, see these guides:

- **[Image Layers](layer-operations-image.md)** - Image and solid color layers
- **[Text Layers](layer-operations-text.md)** - Text layers with character and paragraph styles
- **[Adjustment Layers](layer-operations-adjustments.md)** - Non-destructive adjustment layers
- **[Smart Objects](layer-operations-smart-objects.md)** - Smart object layers
- **[Advanced Operations](layer-operations-advanced.md)** - Masks, groups, blend modes, and transformations

## Related migration guides

Layer operations are just one part of the V2 migration:

- **[Format Conversion](format-conversion-migration.md)** - Migrate `/renditionCreate` for PSD exports
- **[Document Creation](document-creation-migration.md)** - Migrate `/documentCreate` for new documents
- **[Document Operations](document-operations-migration.md)** - Migrate `/documentOperations` for crop/resize/trim

## Next steps

1. Choose the [specific layer type guide](#specific-layer-type-guides) that matches your V1 usage.
2. Start with simple migrations before combining operations.
3. Test with development endpoints before production.

## Need help?

Contact the Adobe DI ART Service team for technical support with your migration.
