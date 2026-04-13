---
title: Advanced Layer Operations Migration (V1 to V2)
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

# Advanced Layer Operations Migration (V1 to V2)

This guide helps you migrate advanced layer operations from V1's `/documentOperations` endpoint to V2's `/create-composite` endpoint, including moving, deleting, masking, grouping, and transforming layers.

## Overview

**V1 Endpoint:** `/pie/psdService/documentOperations`

**V2 Endpoint:** `/v2/create-composite` with `edits.layers`

### Operations Covered

- Moving layers
- Deleting layers
- Layer masks
- Layer groups (layerSection)
- Blend modes and opacity
- Layer transformations

## Moving Layers

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

### Move Operation Changes

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

### Move Placement Options

**V1 → V2 Mapping:**

| V1                                    | V2                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| `move: {insertTop: true}`             | `operation: {type: "move", placement: {type: "top"}}`                                 |
| `move: {insertBottom: true}`          | `operation: {type: "move", placement: {type: "bottom"}}`                              |
| `move: {insertAbove: {name: "X"}}`    | `operation: {type: "move", placement: {type: "above", relativeTo: {name: "X"}}}`      |
| `move: {insertBelow: {id: 123}}`      | `operation: {type: "move", placement: {type: "below", relativeTo: {id: 123}}}`        |
| `move: {insertInto: {name: "Group"}}` | `operation: {type: "move", placement: {type: "inside", relativeTo: {name: "Group"}}}` |

## Deleting Layers

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

### Delete Operation Changes

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

### Deleting Multiple Layers

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

## Layer Masks

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
        "mask": {
          "source": {
            "url": "<MASK_IMAGE_URL>"
          },
          "isLinked": true,
          "isEnabled": true,
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

### Mask Property Changes

**Key Changes:**

| V1 Property | V2 Property | Notes |
| ----------- | ----------- | ----- |
| `input.href` + `input.storage` | `source.url` | Simplified to single URL property |
| `linked` | `isLinked` | Boolean naming convention updated |
| `enabled` | `isEnabled` | Boolean naming convention updated |
| `offset` | `offset` | No change - same property name |
| `clip` | Moved to layer level | Now a top-level layer property `isClipped`. See [Clipping Masks](#clipping-masks) section below |

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
  "mask": {
    "source": {
      "url": "<URL>"
    },
    "isLinked": true,
    "isEnabled": true
  }
}
```

<InlineAlert variant="info" slots="text"/>

The `clip` property has been restructured in V2. Instead of `mask.clip`, use the top-level layer property `isClipped` to control clipping mask behavior.

### Mask Requirements

Both V1 and V2:

- Mask image must be grayscale
- Supported formats: JPEG, PNG, PSD
- White = visible, Black = hidden

## Layer Groups

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "type": "layerSection",
        "name": "My Group",
        "add": {
          "insertTop": true
        },
        "children": []
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
        "type": "layer_group",
        "name": "My Group",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      }
    ]
  }
}
```

### Group Type Changes

**V1:** `type: "layerSection"`

**V2:** `type: "layer_group"`

### Creating Groups with Children

**V1:** Used `children` array

```json
{
  "type": "layerSection",
  "name": "My Group",
  "children": [
    {
      "type": "layer",
      "name": "Child Layer 1"
    }
  ]
}
```

**V2:** Use `insertInto`/`inside` placement

```json
{
  "edits": {
    "layers": [
      {
        "type": "layer_group",
        "name": "My Group",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      },
      {
        "type": "layer",
        "name": "Child Layer 1",
        "image": {
          "source": {...}
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "inside",
            "relativeTo": {
              "name": "My Group"
            }
          }
        }
      }
    ]
  }
}
```

## Blend Modes and Opacity

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

### Blend Property Changes

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

### Supported Blend Modes

Both V1 and V2 support the same blend modes:

- `normal`, `dissolve`
- `darken`, `multiply`, `colorBurn`, `linearBurn`, `darkerColor`
- `lighten`, `screen`, `colorDodge`, `linearDodge`, `lighterColor`
- `overlay`, `softLight`, `hardLight`, `vividLight`, `linearLight`, `pinLight`, `hardMix`
- `difference`, `exclusion`, `subtract`, `divide`
- `hue`, `saturation`, `color`, `luminosity`

## Layer Visibility and Lock

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
        "isLocked": true
      }
    ]
  }
}
```

### Property Name Changes

| V1        | V2          |
| --------- | ----------- |
| `visible` | `isVisible` |
| `locked`  | `isLocked`  |

## Layer Transformations

### Positioning and Sizing

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
      "x": 100,
      "y": 100
    },
    "dimension": {
      "width": 500,
      "height": 300
    }
  }
}
```

<InlineAlert variant="info" slots="text"/>

V2 requires `transformMode: "custom"` to be set when using the `transform` object. The `transform` object provides additional capabilities beyond basic positioning and sizing, including `anchor`, `angle` (rotation in degrees), `skew`, `horizontalAlign`, and `verticalAlign`.

### Alignment Options

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

## Clipping Masks

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

## Migration Checklist

When migrating advanced layer operations from V1 to V2:

- [ ] Move: Replace `move: {...}` with `operation: {type: "move", placement: {...}}`
- [ ] Delete: Replace `delete: {}` with `operation: {type: "delete"}`
- [ ] Transforms: Replace `bounds` with `transform` using `offset` and `dimension`
- [ ] Masks: Change `mask.input` to `mask.source`
- [ ] Masks: Change `mask.linked` to `mask.isLinked`
- [ ] Masks: Change `mask.enabled` to `mask.isEnabled`
- [ ] Clipping: Move `mask.clip` to top-level `isClipped` property
- [ ] Groups: Change `type: "layerSection"` to `type: "layer_group"`
- [ ] Groups: Replace `children` array with `inside` placement
- [ ] Blend: Move `blendOptions.opacity` to top-level `opacity`
- [ ] Blend: Move `blendOptions.blendMode` to top-level `blendMode`
- [ ] Visibility: Change `visible` to `isVisible`
- [ ] Lock: Change `locked` to `isLocked`
- [ ] Remove explicit `edit: {}` blocks
- [ ] Update storage syntax (`href`/`storage` → `url`/`storageType`)

## Common Migration Issues

### Issue: Multiple operations on same layer

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

### Issue: Group children structure

**Problem:** V1 used nested `children` array

**Solution:** V2 uses sequential layer definitions with `inside` placement

```json
// First create the group
{
  "type": "layer_group",
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
      "type": "inside",
      "relativeTo": {"name": "Group"}
    }
  }
}
```

### Issue: Blend mode naming

**Problem:** Some blend modes have different names

**Solution:** Use exact names from the supported list (same in V1 and V2)

## Complete Migration Example

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

**V2 create-composite:**

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
        "type": "layer_group",
        "name": "Effects Group",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
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
            "type": "inside",
            "relativeTo": {
              "name": "Effects Group"
            }
          }
        }
      },
      {
        "name": "Existing Layer",
        "mask": {
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

## Feature Availability

### Currently Available in V2

- ✅ Move layers
- ✅ Delete layers
- ✅ Layer masks (pixel masks)
- ✅ Clipping masks (via `isClipped` property)
- ✅ Layer groups
- ✅ Blend modes and opacity
- ✅ Layer visibility and lock
- ✅ Layer positioning (bounds)

### V1 Features - Status TBD

- ⏳ Group children deletion options
- ⏳ Some alignment options

<InlineAlert variant="info" slots="text"/>

If you rely on V1 features not yet in V2, contact the Adobe DI ART Service team to discuss alternatives or timeline.

## Next steps

- Review [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Check [Image Layers](layer-operations-image.md) for placement patterns
- See [Text Layers](layer-operations-text.md) for text operations
- See [Adjustment Layers](layer-operations-adjustments.md) for adjustments

## Need Help?

Contact the Adobe DI ART Service team for technical support with advanced layer operation migration.
