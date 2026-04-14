---
title: Layer Operations Migration
description: Learn how to migrate your v1 composite operations to v2 layer operations.
hideBreadcrumbNav: true
keywords:
  - layer operations
  - layers
  - composite
  - PSD
  - migration
  - v1 to v2
---

# Layer Operations Migration

This page helps you navigate the layer operation migration guides. Layer operations have been split into focused guides for easier navigation and future expansion.

## Overview

The v2 `/create-composite` endpoint now provides comprehensive layer manipulation capabilities. To understand the changes in the greatest detail, layer operations are organized into specialized guides by layer type and operation complexity to show how the v2 service can achieve those results.

## Quick reference

### By operation type

| What You Want to Do           | Guide to Use                                                 |
| ----------------------------- | ------------------------------------------------------------ |
| Add an image to a document    | [Image Layer Operations](layer-operations-image.md)          |
| Add text to a document        | [Text Layer Operations](layer-operations-text.md)            |
| Apply color/tonal adjustments | [Adjustment Layer Operations](layer-operations-adjustments.md) |
| Add scalable graphics         | [Smart Object Operations](layer-operations-smart-objects.md) |
| Move layers in the stack      | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Delete layers                 | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Apply layer masks             | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Organize into groups          | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Change blend modes            | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Transform layers              | [Advanced Layer Operations](layer-operations-advanced.md)    |
| Export specific layers (JPEG/PNG/TIFF/PSD) | [Export Layers Migration](export-layers-migration.md) |

### By layer type

| Layer Type                  | Guide                                                        |
| --------------------------- | ------------------------------------------------------------ |
| Standard image/pixel layers | [Image Layer Operations](layer-operations-image.md)          |
| Solid color layers          | [Image Layer Operations](layer-operations-image.md)          |
| Text layers                 | [Text Layer Operations](layer-operations-text.md)            |
| Adjustment layers           | [Adjustment Layer Operations](layer-operations-adjustments.md) |
| Smart object layers         | [Smart Object Operations](layer-operations-smart-objects.md) |
| Group layers                | [Advanced Layer Operations](layer-operations-advanced.md)    |

## Choose your guide

### [Layer Operations Overview](layer-operations-overview.md)

**Start here if you're new to layer operations in v2.**

- Introduction to layer operations concepts
- Basic request structure
- Operation types (add, edit, delete)
- Common patterns and best practices
- When to use layer operations vs other endpoints

### [Image Layer Operations](layer-operations-image.md)

**For working with image and solid color layers.**

- Adding image layers
- Solid color fill layers
- Layer placement strategies
- Positioning with bounds
- Layer properties (visibility, opacity, blend modes)

### [Text Layer Operations](layer-operations-text.md)

**For working with text layers.**

- Adding and editing text layers
- Character styles (font, size, color, styling)
- Paragraph styles (alignment, spacing, indentation)
- Multi-style text
- Font handling and custom fonts

### [Adjustment Layer Operations](layer-operations-adjustments.md)

**For non-destructive image adjustments.**

- Brightness/Contrast adjustments
- Hue/Saturation adjustments
- Exposure adjustments
- Color Balance adjustments
- Adjustment layer placement and targeting

### [Smart Object Operations](layer-operations-smart-objects.md)

**For working with smart object layers.**

- Adding smart objects
- Non-destructive transformations
- Rotation, scaling, and positioning
- Transform modes
- Smart object sources (external, Creative Cloud, Adobe Assets)

### [Advanced Layer Operations](layer-operations-advanced.md)

**For advanced layer manipulation.**

- Moving and deleting layers
- Layer masks (pixel masks)
- Clipping masks
- Layer groups and organization
- Blend modes
- Layer transformations
- Complex layer compositions

## Common workflows to migrate

### Building a composition

1. Start with [Image Layers](layer-operations-image.md) for background
2. Add [Text Layers](layer-operations-text.md) for titles
3. Apply [Adjustment Layers](layer-operations-adjustments.md) for color correction
4. Use [Smart Objects](layer-operations-smart-objects.md) for logos/graphics
5. Organize with [Groups](layer-operations-advanced.md) and apply [Blend Modes](layer-operations-advanced.md)

### Editing existing documents

1. Review [Layer Operations Overview](layer-operations-overview.md) for editing patterns
2. Use specific guides to modify existing layers
3. Apply [Advanced Operations](layer-operations-advanced.md) to reorganize layer stack
4. Test with visible/opacity changes before finalizing

## Related guides

Layer operations work in conjunction with other v2 endpoints:

- **[Export Layers Migration](export-layers-migration.md)** - Export one or more layers (single vs multi-layer, PSD support, quality defaults)
- **[Format Conversion](format-conversion-migration.md)** - Convert PSDs to other formats without edits
- **[Document Creation](document-creation-migration.md)** - Create new blank documents
- **[Document Operations](document-operations-migration.md)** - Document-level operations (resize, crop, trim)

## Need help?

- Check the [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for output options
- Contact the Adobe DI ART Service team for technical support

## What's next?

1. **Start with basics**: Begin with the [Layer Operations Overview](layer-operations-overview.md)
2. **Choose your layer type**: Navigate to the specific guide for the layer type you're working with
3. **Test simple operations**: Start with adding a single layer
4. **Combine operations**: Build more complex compositions once comfortable
5. **Add advanced features**: Explore masks, groups, and advanced operations
