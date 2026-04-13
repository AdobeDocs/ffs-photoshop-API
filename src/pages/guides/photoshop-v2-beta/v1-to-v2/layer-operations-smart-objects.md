---
title: Smart Object Operations Migration
description: Migrate smart object layer operations from V1 to V2
hideBreadcrumbNav: true
keywords:
  - smart objects
  - smart object layers
  - linked smart objects
  - embedded smart objects
  - migration
  - v1 to v2
---

# Smart Object Operations Migration

This guide helps you migrate smart object layer operations from V1's `/documentCreate` and `/documentOperations` endpoints to V2's `/create-composite` endpoint.

<InlineAlert variant="warning" slots="text"/>

Note: V1 also had a dedicated `/psdService/smartObject` endpoint for specific smart object workflows. That endpoint is separate and not covered in this guide.

## Overview

**V1 Endpoints:**

- `/pie/psdService/documentCreate` - Create documents with smart object layers
- `/pie/psdService/documentOperations` - Add/edit smart object layers

**V2 Endpoint:** `/v2/create-composite` with `edits.layers`

### Smart Object Types

- **Embedded Smart Objects** - The source file is embedded in the PSD
- **Linked Smart Objects** - The source file is linked externally (V1 supported, V2 status TBD)

## Adding Smart Object Layers

### V1 approach: documentOperations

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
        "type": "smartObject",
        "name": "Logo Smart Object",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<SMART_OBJECT_SOURCE_URL>",
          "storage": "external"
        },
        "smartObject": {
          "linked": false
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
        "type": "smart_object_layer",
        "name": "Logo Smart Object",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<SMART_OBJECT_SOURCE_URL>"
            }
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

## Key Migration Changes

### 1. Layer Type Name

**V1:** `"type": "smartObject"`

**V2:** `"type": "smart_object_layer"`

### 2. Source Reference

**V1:** Uses `input` property

```json
{
  "type": "smartObject",
  "input": {
    "href": "<URL>",
    "storage": "external"
  }
}
```

**V2:** Uses `smartObject.smartObjectFile.source` property

```json
{
  "type": "smart_object_layer",
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<URL>"
      }
    }
  }
}
```

<InlineAlert variant="warning" slots="text"/>

The smart object file reference is nested under `smartObject.smartObjectFile.source.url`, not at the layer level.

### 3. Linked vs Embedded

**V1:** Explicit `smartObject.linked` property

```json
{
  "type": "smartObject",
  "smartObject": {
    "linked": false
  }
}
```

**V2:** (Status TBD - check V2 documentation)

<InlineAlert variant="info" slots="text"/>

Check the current V2 API documentation for linked smart object support status. This feature may be in development.

### 4. Add Operation Structure

**V1:** Separate `add` block

```json
{
  "type": "smartObject",
  "add": {
    "insertTop": true
  }
}
```

**V2:** Unified `operation` block with `smartObject` property

```json
{
  "type": "smart_object_layer",
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  },
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<SMART_OBJECT_SOURCE_URL>"
      }
    }
  }
}
```

## Supported Source File Types

Smart objects can contain various file types:

**V1 Supported:**

- PSD (image/vnd.adobe.photoshop)
- JPEG (image/jpeg)
- PNG (image/png)

**V2 Supported:**

- PSD (image/vnd.adobe.photoshop)
- JPEG (image/jpeg)
- PNG (image/png)
- SVG (image/svg+xml)

<InlineAlert variant="info" slots="text"/>

V2 supports SVG files as smart object sources, which can be useful for scalable graphics.

## Transform Mode

V2 introduces `transformMode` property that controls how the smart object is transformed:

- **`"none"`** - No transform applied (use original size)
- **`"custom"`** - Use explicit transform values (offset, dimension, angle, etc.)
- **`"fit"`** - Fit the smart object to maintain aspect ratio
- **`"fill"`** - Fill the available space

```json
{
  "type": "smart_object_layer",
  "transformMode": "fit",
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<SMART_OBJECT_URL>"
      }
    }
  }
}
```

## Smart Object with Transformations

### V1 approach

```json
{
  "type": "smartObject",
  "name": "Scaled Logo",
  "add": {
    "insertTop": true
  },
  "input": {
    "href": "<URL>",
    "storage": "external"
  },
  "bounds": {
    "left": 100,
    "top": 100,
    "width": 500,
    "height": 300
  }
}
```

### V2 approach

```json
{
  "type": "smart_object_layer",
  "name": "Scaled Logo",
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  },
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<URL>"
      }
    }
  },
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

<InlineAlert variant="info" slots="text"/>

V2 uses `transform` with `offset` and `dimension` instead of `bounds`. The `transformMode` property specifies how the transform is applied ("custom", "fit", "fill", or "none").

## Editing Existing Smart Objects

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Smart Object",
        "edit": {},
        "visible": false
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
        "type": "smart_object_layer",
        "name": "Existing Smart Object",
        "operation": {
          "type": "edit"
        },
        "isVisible": false
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text"/>

V2 requires explicit `operation.type: "edit"` for editing existing layers, even if no other changes are made.

## Replacing Smart Object Content

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Smart Object",
        "edit": {},
        "input": {
          "href": "<NEW_SOURCE_URL>",
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
        "type": "smart_object_layer",
        "name": "Existing Smart Object",
        "operation": {
          "type": "edit"
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<NEW_SOURCE_URL>"
            }
          }
        }
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text"/>

To replace smart object content, include `smartObject.smartObjectFile.source.url` with the new file URL. The `operation.type: "edit"` is required.

## Placement Options

Smart objects support the same placement options as other layers:

### V1 Placement

```json
{
  "add": {
    "insertTop": true              // or
    "insertBottom": true            // or
    "insertAbove": {"name": "..."}  // or
    "insertBelow": {"id": 123}      // or
    "insertInto": {"name": "Group"}
  }
}
```

### V2 Placement

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"                // or "bottom"
      // or with referenceLayer:
      "type": "above",
      "referenceLayer": {
        "name": "..."              // or "id": 123
      }
    }
  }
}
```

<InlineAlert variant="info" slots="text"/>

V2 uses `referenceLayer` with `name` or `id` instead of `relativeTo`. Placement types include: "top", "bottom", "above", "below", "into".

See [Image Layer Operations](layer-operations-image.md) for detailed placement patterns.

## Creating Documents with Smart Objects

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
        "type": "smartObject",
        "name": "Logo",
        "input": {
          "href": "<LOGO_URL>",
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
        "type": "smart_object_layer",
        "name": "Logo",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<LOGO_URL>"
            }
          }
        }
      }
    ]
  }
}
```

## Layer Properties

Smart objects support standard layer properties:

```json
{
  "type": "smart_object_layer",
  "name": "My Smart Object",
  "isVisible": true,
  "isLocked": false,
  "blendOptions": {
    "opacity": 90,
    "blendMode": "normal"
  },
  "transformMode": "custom",
  "transform": {
    "offset": {
      "horizontal": 100,
      "vertical": 100
    },
    "dimension": {
      "width": 500,
      "height": 300
    },
    "angle": 0,
    "skew": {
      "horizontal": 0,
      "vertical": 0
    },
    "anchor": {
      "horizontal": 0.5,
      "vertical": 0.5
    }
  },
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<SMART_OBJECT_URL>"
      }
    }
  }
}
```

<InlineAlert variant="warning" slots="text"/>

- `opacity` and `blendMode` are nested under `blendOptions`, not at the layer level
- `bounds` is replaced with `transform` containing `offset` and `dimension`

> - `transformMode` can be "custom", "fit", "fill", or "none"
> - `isLocked` property is available for layer locking

See [Advanced Layer Operations](layer-operations-advanced.md) for blend modes and transforms.

## Migration Checklist

When migrating smart object operations from V1 to V2:

- [ ] Change `type: "smartObject"` to `type: "smart_object_layer"`
- [ ] Change `input` to `smartObject.smartObjectFile.source` for smart object file reference
- [ ] Change `href`/`storage` to `url` (storageType is not needed)
- [ ] Replace `add` block with `operation.type: "add"` and include `placement`
- [ ] Convert placement directives (insertTop → placement.type: "top", etc.)
- [ ] Use `referenceLayer` with `name` or `id` instead of `relativeTo`
- [ ] Add `operation.type: "edit"` for editing existing layers
- [ ] Convert `visible` to `isVisible`
- [ ] Move `opacity` and `blendMode` under `blendOptions` object
- [ ] Replace `bounds` with `transform` containing `offset` and `dimension`
- [ ] Add `transformMode` property ("custom", "fit", "fill", or "none")
- [ ] Check V2 documentation for linked smart object support
- [ ] Verify supported source file types in V2

## Common Migration Issues

### Issue: Linked smart objects

**Problem:** V1 had `smartObject.linked` property

**Solution:** Check V2 documentation for current linked smart object support

### Issue: Source file type support

**Problem:** Not all file types may be supported

**Solution:** Verify supported types in V2 documentation before migration

### Issue: Missing operation block

**Problem:** V2 requires explicit operation for new layers

**Solution:** Always include operation block when adding

```json
{
  "type": "smart_object_layer",
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  },
  "smartObject": {
    "smartObjectFile": {
      "source": {
        "url": "<SMART_OBJECT_URL>"
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
        "type": "smartObject",
        "name": "Logo",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<LOGO_PSD_URL>",
          "storage": "external"
        },
        "bounds": {
          "left": 50,
          "top": 50,
          "width": 400,
          "height": 400
        },
        "smartObject": {
          "linked": false
        }
      },
      {
        "type": "smartObject",
        "name": "Product Image",
        "add": {
          "insertAbove": {
            "name": "Logo"
          }
        },
        "input": {
          "href": "<PRODUCT_IMAGE_URL>",
          "storage": "external"
        },
        "blendOptions": {
          "opacity": 85
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
        "type": "smart_object_layer",
        "name": "Logo",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<LOGO_PSD_URL>"
            }
          }
        },
        "transformMode": "custom",
        "transform": {
          "offset": {
            "horizontal": 50,
            "vertical": 50
          },
          "dimension": {
            "width": 400,
            "height": 400
          }
        }
      },
      {
        "type": "smart_object_layer",
        "name": "Product Image",
        "operation": {
          "type": "add",
          "placement": {
            "type": "above",
            "referenceLayer": {
              "name": "Logo"
            }
          }
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<PRODUCT_IMAGE_URL>"
            }
          }
        },
        "blendOptions": {
          "opacity": 85
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

- ✅ Add embedded smart object layers
- ✅ Edit existing smart objects
- ✅ Replace smart object content
- ✅ Smart object transformations (transform with offset, dimension, angle, skew, anchor)
- ✅ Transform modes (custom, fit, fill)
- ✅ Layer visibility (`isVisible`)
- ✅ Layer locking (`isLocked`)
- ✅ Blend options (opacity, blendMode)
- ✅ Placement options (top, bottom, above, below, into)
- ✅ Reference layer by name or ID
- ✅ Multiple source file types (PSD, JPEG, PNG, SVG)

### V1 Features - Status TBD

- ⏳ Linked smart objects (`linked: true`)
- ⏳ Check V2 documentation for current status

### Coming Soon

Check V2 API documentation and release notes for upcoming features.

<InlineAlert variant="info" slots="text"/>

If you rely on V1 smart object features not yet in V2, contact the Adobe DI ART Service team to discuss alternatives or timeline.

## Next steps

- Review [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Check [Image Layers](layer-operations-image.md) for placement patterns
- See [Advanced Operations](layer-operations-advanced.md) for transforms and effects

## Need Help?

Contact the Adobe DI ART Service team for technical support with smart object migration.
