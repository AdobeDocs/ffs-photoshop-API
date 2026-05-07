---
title: Background Layer Operations Migration (V1 to V2)
description: Migrate background layer operations from V1 to V2
hideBreadcrumbNav: true
keywords:
  - background layer
  - layers
  - migration
  - v1 to v2
---

# Background Layer Operations Migration (V1 to V2)

This guide helps you migrate background layer operations from V1's `/documentOperations` endpoint to V2's `/create-composite` endpoint.

## Overview

**V1 Endpoint:**

- `/pie/psdService/documentOperations` - Add/edit/delete background layers

**V2 Endpoint:** `/v2/create-composite` with `edits.layers`

The background layer represents the default layer in a Photoshop document and has special behavior compared to regular image layers. In V1, it was referenced as `type: "backgroundLayer"`, while V2 uses `type: "background_layer"` (snake_case).

## Supported Operations

| Operation | V1 | V2 | Notes |
|-----------|----|----|-------|
| Add (create) | ✓ | ✓ | Create a new background layer with pixel content |
| Read (manifest) | ✓ | ✓ | Background appears with `id: -1` in v1. In v2, a valid layer ID is returned. For assets that contain only a background layer, the ID is `0`|
| Edit pixel content | ✓ (internal auto-convert) | ✓ (via `image.source`) | V2 is explicit about image replacement |
| Convert to layer | ✓ (internal) | ✓ (explicit `convertToLayer: true`) | Convert background to regular layer |
| Delete | ✓ | ✓ | Remove background layer |
| Move | ✗ | ✗ | Background layer position is fixed; move operations not supported |

## Key Migration Changes

### Type Name Change

**V1:** `"backgroundLayer"`

```json
{
  "type": "backgroundLayer"
}
```

**V2:** `"background_layer"` (snake_case)

```json
{
  "type": "background_layer"
}
```

### Visibility Property

**V1:** `"visible": true`

**V2:** `"isVisible": true`

### Layer Lock Property

**V1:** `"locked": true`

**V2:** `"protection": ["all"]` (array of protection types)

See [Advanced Layer Operations](layer-operations-advanced.md) for protection details.

### Operation Structure

**V1:** Separate `add` block

```json
{
  "type": "backgroundLayer",
  "name": "Background",
  "add": {},
  "input": {
    "href": "<IMAGE_URL>",
    "storage": "external"
  }
}
```

**V2:** Explicit `operation` block

```json
{
  "type": "background_layer",
  "name": "Background",
  "image": {
    "source": {
      "url": "<IMAGE_URL>"
    }
  },
  "operation": {
    "type": "add"
  }
}
```

## Adding a Background Layer

### V1 Approach

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
        "type": "backgroundLayer",
        "name": "Background",
        "add": {},
        "input": {
          "href": "<IMAGE_URL>",
          "storage": "external"
        },
        "locked": false,
        "visible": true
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

### V2 Approach

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
        "type": "background_layer",
        "name": "Background",
        "image": {
          "source": {
            "url": "<IMAGE_URL>"
          }
        },
        "operation": {
          "type": "add"
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

<InlineAlert variant="info" slots="text1"/>

Background layers do not accept a `placement` in the operation — they are always positioned at the bottom of the layer stack. This is different from other layer types which require explicit placement.

## Editing a Background Layer

### V1 Approach

```json
{
  "options": {
    "layers": [
      {
        "type": "backgroundLayer",
        "id": -1,
        "edit": {},
        "visible": false,
        "locked": true
      }
    ]
  }
}
```

### V2 Approach

In v2, editing requires an explicit `operation` block, and layers must be referenced using the `id` or `name` returned by the manifest.
The following properties can be edited **directly** on a background layer without conversion:

- `isVisible` — toggle layer visibility
- `image.source` — replace background pixel content


```json
{
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "id": 1,
        "operation": {
          "type": "edit"
        },
        "isVisible": false
      }
    ]
  }
}
```

All other properties (`transform`, `transformMode`, `pixelMask`, `protection`, `blendOptions`) are **not supported** directly on a background layer. To apply them, first convert the background to a regular layer using `convertToLayer: true`.

<InlineAlert variant="info" slots="text1"/>

In V2, editing layers **requires** an explicit `operation` block with `type: "edit"`. Background layer must be referenced using the `id` or `name` returned by the manifest:

## Editing Pixel Content

### V1 Approach (Internal Auto-Convert)

In V1, replacing background layer pixel content was handled internally:

```json
{
  "options": {
    "layers": [
      {
        "type": "backgroundLayer",
        "id": -1,
        "edit": {},
        "input": {
          "href": "<NEW_IMAGE_URL>",
          "storage": "external"
        }
      }
    ]
  }
}
```

### V2 Approach (Explicit)

In V2, image replacement is explicit via `image.source`:

```json
{
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "id": 1,
        "operation": {
          "type": "edit"
        },
        "image": {
          "source": {
            "url": "<NEW_IMAGE_URL>"
          }
        }
      }
    ]
  }
}
```

## Converting Background to Regular Layer

The background layer has a special property: it can be explicitly converted to a regular layer. This is now a first-class operation in V2.

### V1 Approach (Internal)

In V1, this conversion happened implicitly during operations.

### V2 Approach (Explicit)

```json
{
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "id": 1,
        "operation": {
          "type": "edit"
        },
        "convertToLayer": true,
        "convertedLayerName": "Layer_From_Background"
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text1"/>

Use the optional `convertedLayerName` property to assign a name immediately — this name can then be used to target the converted layer in subsequent entries within the same `layers` array. After this operation, the layer is no longer the background layer and can be moved, deleted, or further manipulated like a regular layer.

Here is a complete example of first converting the background layer to a regular layer, and then applying edits:

```json
{
    "edits": {
        "layers": [
            {
                "type": "background_layer",
                "name": "Background",
                "operation": {
                    "type": "edit"
                },
                "convertToLayer": true,
                "convertedLayerName": "Layer_From_Background"
            },
            {
                "type": "layer",
                "name": "Layer_From_Background",
                "operation": {
                    "type": "edit"
                },
                "transformMode": "custom",
                "transform": {
                    "offset": {
                        "horizontal": 100,
                        "vertical": 100
                    }
                }
            }
        ]
    }
}
```

## Reading Background Layer in Manifest

In v2, the manifest response for background layer returns the actual layer ID and this ID should be used for all further operations on background layer. For documents that contain only a background layer (no other layers), the ID returned is `0`.
The manifest response for background layer also contains special metadata:

### V2 Manifest Response

```json
{
  "id": 0,
  "index": 0,
  "type": "background_layer",
  "name": "Background",
  "visible": true,
  "protection": ["none"],
  "background": {
    "canConvertToLayer": true
  },
  "blendOptions": {
    "opacity": 100,
    "blendMode": "normal"
  }
}
```

Key properties:

- **`id: 0`** - Background layer returns `id` as `0` when it is the only layer in the document.
- **`background.canConvertToLayer`** - Indicates whether this background can be converted to a regular layer
- **`index: 0`** - Background is always at index 0 (bottom of the layer stack)

## Deleting a Background Layer

### V1 Approach

```json
{
  "options": {
    "layers": [
      {
        "type": "backgroundLayer",
        "id": -1,
        "delete": {}
      }
    ]
  }
}
```

### V2 Approach

```json
{
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "id": 1,
        "operation": {
          "type": "delete"
        }
      }
    ]
  }
}
```

## Unsupported Operations

### Move

Background layer position is fixed at the bottom of the layer stack. Move operations are not supported.


## Migration Checklist

When migrating background layer operations from V1 to V2:

- [ ] Change `type: "backgroundLayer"` to `type: "background_layer"`
- [ ] Change `visible` to `isVisible`
- [ ] Change `locked` to `protection` array (e.g., `["all"]` for fully locked, `["none"]` for unlocked)
- [ ] Replace `add: {}` with `operation: { "type": "add" }`
- [ ] Replace `edit: {}` with `operation: { "type": "edit" }`
- [ ] Replace `delete: {}` with `operation: { "type": "delete" }`
- [ ] Change `input.href` to `image.source.url` for pixel content
- [ ] Remove `input.storage` (defaults to external)
- [ ] Reference background layer by `id` (returned from the manifest response) when editing or deleting
- [ ] Update manifest parsing to use `background_layer` type name
- [ ] Use explicit `convertToLayer: true` instead of relying on implicit conversion
- [ ] Note: Move operations not supported; background position is fixed
- [ ] Verify error handling for unsupported move operations

## Common Migration Issues

### Issue: Layer ID mismatch

**Problem:** Trying to edit background layer with ID `-1`

**Solution:** Always use `id` returned from manifest response for background layer operations

```json
{
  "type": "background_layer",
  "id": 0,
  "operation": {
    "type": "edit"
  }
}
```

### Issue: Missing operation block

**Problem:** Editing without explicit `operation` type

**Solution:** Always include `operation` block with explicit type

```json
{
  "operation": {
    "type": "edit"
  }
}
```

### Issue: Move operation not supported

**Problem:** Attempting to move background layer

**Solution:** Move is not supported for background layers. Convert to layer first if needed:

```json
{
  "type": "background_layer",
  "id": 1,
  "operation": {
    "type": "edit"
  },
  "convertToLayer": true,
  "convertedLayerName": "Layer_From_Background"
}
```

### Issue: Type name case sensitivity

**Problem:** Using `"backgroundLayer"` (camelCase) in V2

**Solution:** Use snake_case in V2

```json
{
  "type": "background_layer"
}
```

## Complete Migration Example

### V1 documentOperations

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
        "type": "backgroundLayer",
        "name": "Background",
        "add": {},
        "input": {
          "href": "<BACKGROUND_IMAGE_URL>",
          "storage": "external"
        },
        "locked": false,
        "visible": true
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

### V2 create-composite

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
        "type": "background_layer",
        "name": "Background",
        "image": {
          "source": {
            "url": "<BACKGROUND_IMAGE_URL>"
          }
        },
        "operation": {
          "type": "add"
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

## Feature Availability

### Currently Available in V2

- ✅ Add background layer with pixel content
- ✅ Edit background layer properties (visibility)
- ✅ Replace background layer pixel content
- ✅ Convert background to regular layer
- ✅ Delete background layer
- ✅ Read background in manifest

### V1 Features Not Yet in V2

- ⏳ (None currently known — all V1 background layer features are supported in V2)

## Related Guides

- [Layer Operations Overview](layer-operations-overview.md) — General layer concepts and processing order
- [Image Layer Operations](layer-operations-image.md) — Standard image/pixel layers
- [Advanced Layer Operations](layer-operations-advanced.md) — Protection, masks, blend modes
