---
title: Image Layer Operations Migration
description: Migrate image layer and solid color layer operations from V1 to V2
hideBreadcrumbNav: true
keywords:
  - image layers
  - solid color
  - pixel layers
  - fill layers
  - migration
  - v1 to v2
---

# Image Layer Operations Migration

This guide helps you migrate image layer and solid color layer operations from v1's `/documentCreate` and `/documentOperations` endpoints to v2's `/create-composite` endpoint.

## Overview

The v1 endpoints `/pie/psdService/documentCreate` and `/pie/psdService/documentOperations` were used to create documents with image/fill layers and add/edit image/fill layers respectively.

Now in the v2 API, all layer operations are unified into the `/v2/create-composite` endpoint with the `edits.layers` array.

Layer types covered in this guide are:

- **Image/Pixel Layers** - V1 `type: "layer"` → V2 `type: "layer"`
- **Solid Color Layers** - V1 `type: "fillLayer"` → V2 `type: "solid_color_layer"`

## Key migration changes

### 1. Add operation structure

In the v1 API, the `add` block was used with insert instructions to specify the placement of the new layer.

```json
{
  "type": "layer",
  "name": "New Layer",
  "add": {
    "insertTop": true
  },
  "input": {
    "href": "<URL>",
    "storage": "external"
  }
}
```

In the v2 API, one `operation` block is used with the `placement` property to specify the placement of the new layer.

```json
{
  "type": "layer",
  "name": "New Layer",
  "image": {
    "source": {
      "url": "<URL>"
    }
  },
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

### 2. Image source property

The v1 API used the `input` object.

```json
{
  "input": {
    "href": "<URL>",
    "storage": "external"
  }
}
```

The v2 API uses the `image.source` object.

```json
{
  "image": {
    "source": {
      "url": "<URL>"
    }
  }
}
```

### 3. Layer placement

Layer placement is now specified in the `operation.placement` property. See the [Layer placement migration patterns](#layer-placement-migration-patterns) section for more details.

## Adding image layers

### V1 approach

The v1 API used the `/documentOperations` endpoint with the `add` block to add a new image layer.

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
        "type": "layer",
        "name": "New Image",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<IMAGE_URL>",
          "storage": "external"
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
        "type": "layer",
        "name": "New Image",
        "image": {
          "source": {
            "url": "<IMAGE_URL>"
          }
        },
        "operation": {
          "type": "add",
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

## Layer placement migration patterns

In the v1 API, the placement options were controlled by these parameters:

- `insertTop: true` - Add at the top of the layer stack
- `insertBottom: true` - Add at the bottom of the layer stack
- `insertAbove: {id: 123}` - Add above a specific layer by ID
- `insertBelow: {name: "Layer"}` - Add below a specific layer by name
- `insertInto: {name: "Group"}` - Add inside a group by name

In the v2 API, the corresponding placement options are controlled by the `operation.placement` property:

- `type: "top"` - Add at top
- `type: "bottom"` - Add at bottom
- `type: "above"` with `relativeTo` - Above specific layer
- `type: "below"` with `relativeTo` - Below specific layer
- `type: "inside"` with `relativeTo` - Inside a group

### Insert at Top

**V1:**

```json
{
  "add": {
    "insertTop": true
  }
}
```

**V2:**

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

### Insert at Bottom

**V1:**

```json
{
  "add": {
    "insertBottom": true
  }
}
```

**V2:**

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "bottom"
    }
  }
}
```

### Insert Above Layer

**V1:**

```json
{
  "add": {
    "insertAbove": {
      "name": "Background"
    }
  }
}
```

**V2:**

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "above",
      "relativeTo": {
        "name": "Background"
      }
    }
  }
}
```

### Insert Below Layer

**V1:**

```json
{
  "add": {
    "insertBelow": {
      "id": 123
    }
  }
}
```

**V2:**

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "below",
      "relativeTo": {
        "id": 123
      }
    }
  }
}
```

### Insert Into Group

**V1:**

```json
{
  "add": {
    "insertInto": {
      "name": "My Group"
    }
  }
}
```

**V2:**

```json
{
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
```

## Solid Color Layers

### V1 approach: fillLayer

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
        "type": "fillLayer",
        "name": "Red Fill",
        "add": {
          "insertTop": true
        },
        "fill": {
          "solidColor": {
            "rgb": {
              "red": 255,
              "green": 0,
              "blue": 0
            }
          }
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
        "type": "solid_color_layer",
        "name": "Red Fill",
        "fill": {
          "solidColor": {
            "rgb": {
              "red": 255,
              "green": 0,
              "blue": 0
            }
          }
        },
        "operation": {
          "type": "add",
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

### Solid Color Layer Changes

**V1:** `type: "fillLayer"` with nested `rgb` object

```json
{
  "type": "fillLayer",
  "fill": {
    "solidColor": {
      "rgb": {
        "red": 255,
        "green": 0,
        "blue": 0
      }
    }
  }
}
```

**V2:** `type: "solid_color_layer"` with direct color properties

```json
{
  "type": "solid_color_layer",
  "fill": {
    "solidColor": {
      "rgb": {
        "red": 255,
        "green": 0,
        "blue": 0
      }
    }
  }
}
```

## Editing Existing Layers

### V1 approach: edit block

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Layer",
        "edit": {},
        "visible": false,
        "blendOptions": {
          "opacity": 75
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
        "name": "Existing Layer",
        "isVisible": false,
        "opacity": 75
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text"/>

In V2, editing existing layers doesn't require an explicit operation type. Simply reference the layer by name or ID and specify the properties to change.

## Replacing Layer Content

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Layer",
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

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Existing Layer",
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

## Layer Positioning

### Using Bounds

Both V1 and V2 support explicit positioning:

**V1:**

```json
{
  "type": "layer",
  "name": "Positioned Image",
  "bounds": {
    "left": 100,
    "top": 100,
    "width": 500,
    "height": 300
  }
}
```

**V2:** (Same pattern)

```json
{
  "type": "layer",
  "name": "Positioned Image",
  "bounds": {
    "left": 100,
    "top": 100,
    "width": 500,
    "height": 300
  }
}
```

### Alignment Options

**V1:** `horizontalAlign` and `verticalAlign`

```json
{
  "type": "layer",
  "horizontalAlign": "center",
  "verticalAlign": "center"
}
```

**V2:** Uses placement alignment

```json
{
  "type": "layer",
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

### Fill to Canvas

**V1:** `fillToCanvas` property

```json
{
  "type": "layer",
  "fillToCanvas": true
}
```

**V2:** Not yet available

<InlineAlert variant="warning" slots="text"/>

The `fillToCanvas` property from V1 is not yet available in V2. Contact Adobe DI ART Service team if you need this feature.

## Creating Documents with Image Layers

### V1 approach: documentCreate

```json
{
  "options": {
    "document": {
      "width": 1000,
      "height": 1000,
      "resolution": 72,
      "fill": "white",
      "mode": "rgb"
    },
    "layers": [
      {
        "type": "layer",
        "name": "Logo",
        "input": {
          "href": "<IMAGE_URL>",
          "storage": "external"
        }
      }
    ]
  }
}
```

### V2 approach

```json
{
  "document": {
    "width": 1000,
    "height": 1000,
    "resolution": 72,
    "fill": {
      "solidColor": {
        "red": 255,
        "green": 255,
        "blue": 255
      }
    },
    "mode": "rgb"
  },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Logo",
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
  }
}
```

## Migration checklist

When migrating image layer operations from v1 to v2:

- [ ] Change `input` to `source` for image references
- [ ] Change `href`/`storage` to `url`/`storageType` (or omit storageType for external)
- [ ] Replace `add` block with `operation.type: "add"`
- [ ] Convert placement: `insertTop` → `placement.type: "top"`
- [ ] Convert placement: `insertBottom` → `placement.type: "bottom"`
- [ ] Convert placement: `insertAbove` → `placement.type: "above"` with `relativeTo`
- [ ] Convert placement: `insertBelow` → `placement.type: "below"` with `relativeTo`
- [ ] Convert placement: `insertInto` → `placement.type: "inside"` with `relativeTo`
- [ ] Change `type: "fillLayer"` to `type: "solid_color_layer"`
- [ ] Remove explicit `edit: {}` block for modifications
- [ ] Convert `blendOptions.opacity` to `opacity` (top-level property)
- [ ] Convert `visible` to `isVisible`
- [ ] Note: `fillToCanvas` not yet available in V2

## Common migration issues

### Missing placement for an add operation

The v2 API requires explicit placement for an add operation. Always specify placement type.

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

### Storage type changes

**V1:** Required explicit storage type

```json
{
  "href": "<URL>",
  "storage": "external"
}
```

**V2:** Storage type optional, defaults to external

```json
{
  "url": "<URL>"
}
```

### Solid color structure

**V1:** Nested `rgb` object

```json
{
  "fill": {
    "solidColor": {
      "rgb": {
        "red": 255,
        "green": 0,
        "blue": 0
      }
    }
  }
}
```

**V2:** Same nested structure

```json
{
  "fill": {
    "solidColor": {
      "rgb": {
        "red": 255,
        "green": 0,
        "blue": 0
      }
    }
  }
}
```

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
        "type": "layer",
        "name": "Hero Image",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<IMAGE_URL>",
          "storage": "external"
        },
        "bounds": {
          "left": 0,
          "top": 0,
          "width": 1920,
          "height": 600
        }
      },
      {
        "type": "fillLayer",
        "name": "Background",
        "add": {
          "insertBottom": true
        },
        "fill": {
          "solidColor": {
            "rgb": {
              "red": 240,
              "green": 240,
              "blue": 240
            }
          }
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
        "type": "layer",
        "name": "Hero Image",
        "image": {
          "source": {
            "url": "<IMAGE_URL>"
          }
        },
        "bounds": {
          "left": 0,
          "top": 0,
          "width": 1920,
          "height": 600
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      },
      {
        "type": "solid_color_layer",
        "name": "Background",
        "fill": {
          "solidColor": {
            "rgb": {
              "red": 240,
              "green": 240,
              "blue": 240
            }
          }
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "bottom"
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
}
```

## Feature Availability

### Currently Available in V2

- ✅ Add image layers
- ✅ Add solid color layers
- ✅ Edit existing layers
- ✅ Replace layer content
- ✅ Layer positioning (bounds)
- ✅ Layer placement (top, bottom, above, below, inside)
- ✅ Layer visibility and opacity

### V1 Features Not Yet in V2

- ⏳ `fillToCanvas` property
- ⏳ Some advanced alignment options

<InlineAlert variant="info" slots="text"/>

If you rely on v1 features not yet in v2, contact the Adobe DI ART Service team to discuss alternatives or timeline.

## Need Help?

Contact the Adobe DI ART Service team for technical support with image layer migration.
