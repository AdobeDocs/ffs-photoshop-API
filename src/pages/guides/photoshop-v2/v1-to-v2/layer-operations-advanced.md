---
title: Advanced Layer Operations Migration
description: Migrate advanced layer operations including move, delete, masks, groups, blend modes, and transforms from V1 to V2
hideBreadcrumbNav: true
keywords:
  - move layers
  - delete layers
  - layer masks
  - layer groups
  - blend modes
  - transforms
  - migration
  - v1 to v2
---

# Advanced Layer Operations Migration

This guide helps you migrate advanced layer operations from V1's `/documentOperations` endpoint to V2's `/create-composite` endpoint, including moving, deleting, masking, grouping, and transforming layers.

## Overview

**V1 Endpoint:** `/pie/psdService/documentOperations`

**V2 Endpoint:** `/v2/create-composite` with `edits.layers`

**Operations covered in this guide:**

- Moving layers
- Deleting layers
- Layer masks (pixel masks)
- Layer groups (layerSection)
- Blend modes and opacity
- Layer transformations

## Moving layers

### V1 approach

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentOperations \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [{
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  }],
  "options": {
    "layers": [
      {
        "name": "Layer to Move",
        "move": {
          "insertTop": true
        }
      }
    ]
  },
  "outputs": [{
    "href": "<SIGNED_POST_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

### V2 approach

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "edits": {
    "layers": [
      {
        "name": "Layer to Move",
        "operation": {
          "type": "move",
          "placement": {
            "type": "top"
          }
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
}'
```

### Move operation changes

**V1:** Separate `move` block

```json
{
  "name": "Layer to Move",
  "move": {
    "insertTop": true
  }
}
```

**V2:** Unified `operation` block

```json
{
  "name": "Layer to Move",
  "operation": {
    "type": "move",
    "placement": {
      "type": "top"
    }
  }
}
```

### Move placement options

**V1 → V2 Mapping:**

| V1                                    | V2                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| `move: {insertTop: true}`             | `operation: {type: "move", placement: {type: "top"}}`                                 |
| `move: {insertBottom: true}`          | `operation: {type: "move", placement: {type: "bottom"}}`                              |
| `move: {insertAbove: {name: "X"}}`    | `operation: {type: "move", placement: {type: "above", referenceLayer: {name: "X"}}}`      |
| `move: {insertBelow: {id: 123}}`      | `operation: {type: "move", placement: {type: "below", referenceLayer: {id: 123}}}`        |
| `move: {insertInto: {name: "Group"}}` | `operation: {type: "move", placement: {type: "into", referenceLayer: {name: "Group"}}}` |

## Deleting layers

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Layer to Delete",
        "delete": {}
      }
    ]
  }
}
```

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Layer to Delete",
        "operation": {
          "type": "delete"
        }
      }
    ]
  }
}
```

### Delete operation changes

**V1:** `delete: {}` block (potentially with `includeChildren`)

```json
{
  "name": "Group Layer",
  "delete": {
    "includeChildren": true
  }
}
```

**V2:** `operation: {type: "delete"}` (check V2 docs for child handling)

```json
{
  "name": "Group Layer",
  "operation": {
    "type": "delete"
  }
}
```

### Deleting multiple layers

Both V1 and V2 support deleting multiple layers in one request:

**V2 Example:**

```json
{
  "edits": {
    "layers": [
      {
        "name": "Unwanted Layer 1",
        "operation": {
          "type": "delete"
        }
      },
      {
        "name": "Unwanted Layer 2",
        "operation": {
          "type": "delete"
        }
      }
    ]
  }
}
```

## Layer masks (pixel masks)

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Masked Layer",
        "edit": {},
        "mask": {
          "input": {
            "href": "<MASK_IMAGE_URL>",
            "storage": "external"
          },
          "linked": true,
          "enabled": true,
          "offset": {
            "x": 0,
            "y": 0
          }
        }
      }
    ]
  }
}
```

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Masked Layer",
        "operation": { "type": "edit" },
        "pixelMask": {
          "source": {
            "url": "<MASK_IMAGE_URL>"
          },
          "isLinked": true,
          "isEnabled": true,
          "offset": {
            "horizontal": 0,
            "vertical": 0
          }
        }
      }
    ]
  }
}
```

### Mask property changes

**V1:**

```json
{
  "mask": {
    "input": {
      "href": "<URL>",
      "storage": "external"
    },
    "linked": true,
    "enabled": true,
    "clip": false
  }
}
```

**V2:**

```json
{
  "pixelMask": {
    "source": {
      "url": "<URL>"
    },
    "isLinked": true,
    "isEnabled": true,
    "offset": {
      "horizontal": 0,
      "vertical": 0
    }
  }
}
```

**Key Changes:**

| V1 Property | V2 Property | Notes |
| ----------- | ----------- | ----- |
| `mask` | `pixelMask` | Property renamed at layer level |
| `input.href` + `input.storage` | `source.url` | Simplified to single URL property |
| `linked` | `isLinked` | Boolean naming convention updated |
| `enabled` | `isEnabled` | Boolean naming convention updated |
| `offset.x` / `offset.y` | `offset.horizontal` / `offset.vertical` | Coordinate naming updated |
| `clip` | Moved to layer level | Now a top-level layer property `isClipped`. See [Clipping Masks](#clipping-masks) section below |

<InlineAlert variant="info" slots="text"/>

The `clip` property has been restructured in V2. Instead of `mask.clip`, use the top-level layer property `isClipped` to control clipping mask behavior.

### Deleting a pixel mask

V2 supports removing a pixel mask from a layer during an edit operation. Set `pixelMask.delete` to `true` on the layer — this removes the pixel mask entirely. When `delete` is `true`, all other `pixelMask` properties (`source`, `isEnabled`, `isLinked`, `offset`) are ignored.

<InlineAlert variant="warning" slots="text"/>

Deleting a pixel mask is only available on **edit** operations (`operation.type: "edit"`). It is not valid on **add** operations.

**V2 Example — Delete pixel mask from a layer:**

```json
{
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Layer with Mask to Remove",
        "operation": { "type": "edit" },
        "pixelMask": {
          "delete": true
        }
      }
    ]
  }
}
```

**V2 Example — Delete pixel mask using layer ID:**

```json
{
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "id": 42,
        "operation": { "type": "edit" },
        "pixelMask": {
          "delete": true
        }
      }
    ]
  }
}
```

**Combining with other layer edits:**

You can delete a pixel mask while also modifying other layer properties in the same layer entry:

```json
{
  "edits": {
    "layers": [
      {
        "type": "smart_object_layer",
        "name": "Update Layer",
        "operation": { "type": "edit" },
        "opacity": 80,
        "isVisible": true,
        "pixelMask": {
          "delete": true
        }
      }
    ]
  }
}
```

**Validation rules:**

- `delete` must be a boolean (`true` or `false`).
- When `delete` is `false` (or omitted on add operations), the other `pixelMask` properties (`source`, `isEnabled`, `isLinked`, `offset`) are applied normally.

### Mask requirements

Both V1 and V2:

- Mask image must be grayscale
- Supported formats: JPEG, PNG, PSD
- White = visible, Black = hidden

## Layer groups

<InlineAlert variant="warning" slots="text"/>

**Creating a new document with a group layer is not yet supported (upcoming feature).** **Editing an existing document** to add a layer inside a group layer **is supported**, as is editing existing group layers (name, visibility, protection, etc.). Use placement `type: "into"` with `referenceLayer` to add a layer into an existing group.

### Adding a layer into an existing group

When **editing an existing document** (e.g., create-composite with an existing PSD), you can add a new layer inside a group that already exists: use `operation.type: "add"` with `placement.type: "into"` and `referenceLayer` pointing to the group:

```json
{
  "type": "layer",
  "name": "Child Layer",
  "image": { "source": { "url": "<IMAGE_URL>" } },
  "operation": {
    "type": "add",
    "placement": {
      "type": "into",
      "referenceLayer": { "name": "My Group" }
    }
  }
}
```

The group must already exist in the document (e.g., from the PSD). Creating a new document with a group layer is not yet supported (upcoming feature).

### Editing group layers

When editing an existing group layer (`operation.type: "edit"`), you can modify these properties:

- `name` - Layer name
- `isVisible` - Visibility
- `protection` - Protection flags (propagates to all descendant layers)
- `blendOptions` - Opacity and blend mode
- `pixelMask` - Mask settings

<InlineAlert variant="warning" slots="text"/>

**Not supported for edit operations on group layers:** `isClipped` (clipping is a property of content layers, not group layers) and `children` (use `into` placement with `referenceLayer` to add layers into an existing group; the `children` array is not accepted in edit operations).

**Example: Editing a group layer**

```json
{
  "edits": {
    "layers": [
      {
        "name": "My Group",
        "type": "group_layer",
        "operation": { "type": "edit" },
        "isVisible": true,
        "protection": ["all"]
      }
    ]
  }
}
```

## Blend modes and opacity

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Layer with Blend",
        "edit": {},
        "blendOptions": {
          "opacity": 75,
          "blendMode": "multiply"
        }
      }
    ]
  }
}
```

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Layer with Blend",
        "opacity": 75,
        "blendMode": "multiply"
      }
    ]
  }
}
```

### Blend property changes

**V1:** Nested in `blendOptions`

```json
{
  "blendOptions": {
    "opacity": 75,
    "blendMode": "multiply"
  }
}
```

**V2:** Top-level properties

```json
{
  "opacity": 75,
  "blendMode": "multiply"
}
```

### Supported blend modes

Both V1 and V2 support the same blend modes:

- `normal`, `dissolve`
- `darken`, `multiply`, `colorBurn`, `linearBurn`, `darkerColor`
- `lighten`, `screen`, `colorDodge`, `linearDodge`, `lighterColor`
- `overlay`, `softLight`, `hardLight`, `vividLight`, `linearLight`, `pinLight`, `hardMix`
- `difference`, `exclusion`, `subtract`, `divide`
- `hue`, `saturation`, `color`, `luminosity`

## Layer visibility and lock

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Layer",
        "edit": {},
        "visible": false,
        "locked": true
      }
    ]
  }
}
```

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Layer",
        "isVisible": false,
        "protection": ["all"]
      }
    ]
  }
}
```

### Property name changes

| V1        | V2          |
| --------- | ----------- |
| `visible` | `isVisible` |
| `locked`  | `protection` (array, e.g. `["all"]` or `["none"]`) |

### Protection array (all flag types)

V2 uses a `protection` array instead of a boolean `locked`. Valid values:

- `none` - No protection (layer fully editable)
- `all` - Full protection (all aspects locked)
- `transparency` - Protects layer transparency from editing
- `composite` - Protects layer compositing/painting
- `position` - Protects layer position from moving
- `artboard_autonest` - Artboard-specific autonest protection

<InlineAlert variant="warning" slots="text"/>

When using `all` or `none`, the array must contain only that element. `["all","transparency"]` and `["none","position"]` are invalid; use either `["all"]`, `["none"]`, or a combination of the four individual flags only.

**Examples:** `["all"]`, `["none"]`, `["transparency","position"]`

**Add operations:** When adding a layer, omitting `protection` (or null/empty array) defaults to `["none"]`, same as V1 where omitted `locked` meant the layer was unlocked.

**Edit operations:** For edits, omit, null, or an empty array `[]` all mean "don't change" the layer's current protection. Only include `protection` when you want to explicitly set it.

**Group layers:** When editing a group layer, setting `protection` propagates to all descendant layers (children and nested groups).

### Artboard visibility — V1 vs V2 behavioral difference

Setting `visible: false` on an **artboard root layer** behaves differently across API versions:

| Behavior | V1 (`documentOperations`) | V2 (`create-composite`) |
|---|---|---|
| Artboard content rendered | **Always** (visibility ignored) | Only if `isVisible: true` |
| Output dimensions | Full document canvas | Shrinks to visible artboards only |
| Effect on child layers | No change | Children not composited |

**V1 quirk:** In V1, hiding an artboard container by `id` (e.g., `{"id": 328, "visible": false}`) has no effect on the rendered output. The full document canvas is returned at its original pixel dimensions regardless of artboard visibility state. This is a known V1 limitation — artboard visibility is tracked but not applied at render time.

**V2 behavior:** V2 correctly respects artboard visibility. A PSD with multiple artboards produces an output image sized to only the visible artboard content when other artboards are hidden.

**Migration impact:** If your V1 workflow hides artboard root IDs to isolate a specific artboard for export, V2 will produce a different (smaller) output size. This is the correct and intended behavior — update any downstream size assumptions accordingly.

## Layer transformations

### Positioning and sizing

**V1:** Uses `bounds` for positioning and sizing

```json
{
  "name": "Transformed Layer",
  "bounds": {
    "left": 100,
    "top": 100,
    "width": 500,
    "height": 300
  }
}
```

**V2:** Uses `transform` with `offset` and `dimension`

```json
{
  "name": "Transformed Layer",
  "transformMode": "custom",
  "transform": {
    "offset": {
      "horizontal": 100,
      "vertical": 100
    },
    "dimension": {
      "width": 500,
      "height": 300
    }
  }
}
```

**`transform.dimension.unit`** *(optional)*

- Type: String
- Default: `"pixels_unit"`
- Values: `"pixels_unit"` | `"points_unit"`
- Description: Unit for `transform.dimension.width` and `transform.dimension.height`. When `"points_unit"`, dimensions are converted to pixels: `Math.round(points × (DPI / 72))`. DPI is resolved from `image.resolution.value`, the source document's native DPI, or 72 as a fallback.

<InlineAlert variant="info" slots="text"/>

V2 requires `transformMode: "custom"` to be set when using the `transform` object. The `transform` object provides additional capabilities beyond basic positioning and sizing, including `anchor`, `angle` (rotation in degrees), `skew`, `horizontalAlign`, and `verticalAlign`.

<InlineAlert variant="warning" slots="text1"/>

**`transform` object is only valid with `transformMode: "custom"`** — sending a `transform` object with `fit`, `fill`, or `none` is rejected with a 400 error.

**`fit` and `fill` always position the layer at `(0, 0)`** after scaling. For any other position, omit the `transform` object on the fit/fill request, then send a second request targeting the same layer with `transformMode: "custom"` and the desired `offset`.

**Two-pass execution for `custom` mode (when `dimension`, `angle`, or `skew` is present):**

1. **Pass 1** — geometry (`dimension` + `angle` + `skew`) is applied using `anchor` as the pivot. If `anchor` is omitted, PIE defaults to `(0, 0)`.
2. **Pass 2** — position is set via `setOffset` using this priority: explicit `offset` → `horizontalAlign`/`verticalAlign` → fallback (restores original x, y so the layer does not drift).

**Geometry-only** (dimension/angle/skew with no offset and no alignment): the fallback applies — original position is silently preserved. This matches V1 behaviour.

### Alignment options

**V1:** `horizontalAlign` and `verticalAlign`

```json
{
  "name": "Centered Layer",
  "horizontalAlign": "center",
  "verticalAlign": "center"
}
```

**V2:** Uses placement alignment (for add/move operations)

```json
{
  "name": "Centered Layer",
  "operation": {
    "type": "add",
    "placement": {
      "type": "custom",
      "horizontalAlignment": "center",
      "verticalAlignment": "center"
    }
  }
}
```

## Clipping masks

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Clipped Layer",
        "edit": {},
        "mask": {
          "clip": true
        }
      }
    ]
  }
}
```

### V2 approach

In V2, clipping mask is now a top-level layer property instead of being nested under the `mask` object:

```json
{
  "edits": {
    "layers": [
      {
        "name": "Clipped Layer",
        "isClipped": true
      }
    ]
  }
}
```

**Key Change:**

| V1 Property | V2 Property | Notes |
| ----------- | ----------- | ----- |
| `mask.clip` | `isClipped` | Moved from mask object to top-level layer property |

<InlineAlert variant="info" slots="text"/>

The clipping mask functionality has been restructured in V2. Use the `isClipped` boolean property directly on the layer (not nested under `mask`).

## Migration checklist

When migrating advanced layer operations from V1 to V2:

- [ ] Move: Replace `move: {...}` with `operation: {type: "move", placement: {...}}`
- [ ] Delete: Replace `delete: {}` with `operation: {type: "delete"}`
- [ ] Transforms: Replace `bounds` with `transform` using `offset` and `dimension`; set `transformMode: "custom"`
- [ ] `transform` object must NOT be present when `transformMode` is `fit`, `fill`, or `none` — the service returns 400
- [ ] `fit`/`fill`: layer is always placed at (0,0) after scaling; for other positions, use a second request with `transformMode: "custom"` and the desired offset
- [ ] `custom` with dimension/angle/skew: two-pass — geometry first (anchor as pivot, default (0,0)), then position via `setOffset`; priority: offset → alignment → restore original x,y
- [ ] Masks: Rename `mask` to `pixelMask`
- [ ] Masks: Change `mask.input` to `pixelMask.source`
- [ ] Masks: Change `mask.linked` to `pixelMask.isLinked`
- [ ] Masks: Change `mask.enabled` to `pixelMask.isEnabled`
- [ ] Masks: Change `offset.x`/`offset.y` to `offset.horizontal`/`offset.vertical`
- [ ] Masks: To delete a pixel mask, use `pixelMask: { "delete": true }` on an edit operation
- [ ] Clipping: Move `mask.clip` to top-level `isClipped` property
- [ ] Groups: Change `type: "layerSection"` to `type: "group_layer"`
- [ ] Groups: Replace `children` array with `into` placement and `referenceLayer`
- [ ] Blend: Move `blendOptions.opacity` to top-level `opacity`
- [ ] Blend: Move `blendOptions.blendMode` to top-level `blendMode`
- [ ] Visibility: Change `visible` to `isVisible`
- [ ] Lock: Change `locked` to `protection` (array, e.g. `["all"]` or `["none"]`)
- [ ] Remove explicit `edit: {}` blocks
- [ ] Update storage syntax (`href`/`storage` → `url`/`storageType`)

## Common migration issues

### Issue: multiple operations on same layer

**Problem:** V1 allowed edit + move in one layer block

**Solution:** V2 requires choosing one operation type per layer reference

```json
// If you need to move AND modify properties, specify move as the operation
{
  "name": "Layer",
  "opacity": 80,
  "operation": {
    "type": "move",
    "placement": {
      "type": "top"
    }
  }
}
```

### Issue: group children structure

**Problem:** V1 used nested `children` array

**Solution:** V2 uses sequential layer definitions with `into` placement and `referenceLayer` to add layers into an existing group (example below).

```json
// First create the group
{
  "type": "group_layer",
  "name": "Group",
  "operation": {"type": "add", "placement": {"type": "top"}}
},
// Then add layers into it
{
  "type": "layer",
  "name": "Child",
  "image": {
    "source": {...}
  },
  "operation": {
    "type": "add",
    "placement": {
      "type": "into",
      "referenceLayer": {"name": "Group"}
    }
  }
}
```

### Issue: blend mode naming

**Problem:** Some blend modes have different names

**Solution:** Use exact names from the supported list (same in V1 and V2)

## Complete migration example

**V1 documentOperations:**

```json
{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "external"
    }
  ],
  "options": {
    "layers": [
      {
        "name": "Background",
        "move": {
          "insertBottom": true
        }
      },
      {
        "name": "Old Layer",
        "delete": {}
      },
      {
        "type": "layerSection",
        "name": "Effects Group",
        "add": {
          "insertTop": true
        }
      },
      {
        "type": "layer",
        "name": "Overlay",
        "add": {
          "insertInto": {
            "name": "Effects Group"
          }
        },
        "input": {
          "href": "<OVERLAY_URL>",
          "storage": "external"
        },
        "blendOptions": {
          "opacity": 60,
          "blendMode": "overlay"
        }
      },
      {
        "name": "Existing Layer",
        "edit": {},
        "mask": {
          "input": {
            "href": "<MASK_URL>",
            "storage": "external"
          },
          "linked": true,
          "enabled": true
        }
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}
```

**V2 create-composite:** (Creating a new document with a group layer is not yet supported (upcoming feature). When editing an existing document, the overlay's `into` placement with `referenceLayer` is supported when the group already exists in the PSD.)

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
        "name": "Background",
        "operation": {
          "type": "move",
          "placement": {
            "type": "bottom"
          }
        }
      },
      {
        "name": "Old Layer",
        "operation": {
          "type": "delete"
        }
      },
      {
        "type": "layer",
        "name": "Overlay",
        "image": {
          "source": {
            "url": "<OVERLAY_URL>"
          }
        },
        "opacity": 60,
        "blendMode": "overlay",
        "operation": {
          "type": "add",
          "placement": {
            "type": "into",
            "referenceLayer": {
              "name": "Effects Group"
            }
          }
        }
      },
      {
        "name": "Existing Layer",
        "operation": { "type": "edit" },
        "pixelMask": {
          "source": {
            "url": "<MASK_URL>"
          },
          "isLinked": true,
          "isEnabled": true
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

## Feature availability

### Currently available in V2

- ✅ Move layers
- ✅ Delete layers
- ✅ Layer masks (pixel masks) — add, edit, and delete
- ✅ Clipping masks (via `isClipped` property)
- ✅ Layer groups
- ✅ Blend modes and opacity
- ✅ Layer visibility and lock
- ✅ Layer positioning (bounds)

### V1 features - status TBD

- ⏳ Group children deletion options
- ⏳ Some alignment options

## Next steps

- Review [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Check [Image Layers](layer-operations-image.md) for placement patterns
- See [Text Layers](layer-operations-text.md) for text operations
- See [Adjustment Layers](layer-operations-adjustments.md) for adjustments
