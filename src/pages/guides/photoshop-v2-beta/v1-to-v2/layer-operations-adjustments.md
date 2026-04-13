---
title: Adjustment Layer Operations Migration (V1 to V2)
description: Migrate adjustment layer operations from V1 to V2
hideBreadcrumbNav: true
keywords:
  - adjustment layers
  - brightness
  - contrast
  - exposure
  - hue saturation
  - color balance
  - migration
  - v1 to v2
---

# Adjustment Layer Operations Migration (V1 to V2)

This guide helps you migrate adjustment layer operations from V1's `/documentCreate` and `/documentOperations` endpoints to V2's `/create-composite` endpoint.

## Overview

**V1 Endpoints:**

- `/pie/psdService/documentCreate` - Create documents with adjustment layers
- `/pie/psdService/documentOperations` - Add/edit adjustment layers

**V2 Endpoint:** `/v2/create-composite` with `edits.layers`

### Supported Adjustment Types

Both V1 and V2 support these adjustment layer types. In **V2**, the `adjustments` object **requires** a `type` parameter (snake_case) alongside the adjustment payload:

| Adjustment          | V2 `type` value       | Payload key          |
| ------------------- | --------------------- | -------------------- |
| Brightness/Contrast | `brightness_contrast` | `brightnessContrast` |
| Exposure            | `exposure`            | `exposure`           |
| Hue/Saturation      | `hue_saturation`      | `hueSaturation`      |
| Color Balance       | `color_balance`       | `colorBalance`       |

## Adding Adjustment Layers

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
        "type": "adjustmentLayer",
        "name": "Brightness",
        "add": {
          "insertTop": true
        },
        "adjustments": {
          "brightnessContrast": {
            "brightness": 25,
            "contrast": 10
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
        "type": "adjustment_layer",
        "name": "Brightness",
        "adjustments": {
          "type": "brightness_contrast",
          "brightnessContrast": {
            "brightness": 25,
            "contrast": 10
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

## Key Migration Changes

### 1. Layer Type Name

**V1:** `"type": "adjustmentLayer"`

**V2:** `"type": "adjustment_layer"`

### 2. Add Operation Structure

**V1:** Separate `add` block

```json
{
  "type": "adjustmentLayer",
  "add": {
    "insertTop": true
  },
  "adjustments": {...}
}
```

**V2:** Unified `operation` block

```json
{
  "type": "adjustment_layer",
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  },
  "adjustments": {...}
}
```

### 3. Adjustments Structure — Required `type` in V2

**V1:** No `type` inside `adjustments`; only the adjustment payload (e.g. `brightnessContrast`).

**V2:** The `adjustments` object **must** include a `type` parameter (snake_case) that identifies the adjustment, plus the corresponding payload.

**V1 (no type):**

```json
{
  "adjustments": {
    "brightnessContrast": {
      "brightness": 25,
      "contrast": 10
    }
  }
}
```

**V2 (type required):**

```json
{
  "adjustments": {
    "type": "brightness_contrast",
    "brightnessContrast": {
      "brightness": 25,
      "contrast": 10
    }
  }
}
```

Valid V2 `type` values: `brightness_contrast`, `exposure`, `hue_saturation`, `color_balance`.

## Brightness/Contrast

**V2** requires `type` inside `adjustments`:

```json
{
  "type": "adjustment_layer",
  "name": "Brightness/Contrast",
  "adjustments": {
    "type": "brightness_contrast",
    "brightnessContrast": {
      "brightness": 25,
      "contrast": -10
    }
  }
}
```

**Parameters:**

- `brightness`: -150 to 150 (default: 0)
- `contrast`: -150 to 150 (default: 0)

## Exposure

**V2** requires `type` inside `adjustments`. The exposure amount parameter is named **`exposureValue`** in V2 (V1 used `exposure`).

```json
{
  "type": "adjustment_layer",
  "name": "Exposure",
  "adjustments": {
    "type": "exposure",
    "exposure": {
      "exposureValue": 0.5,
      "offset": 0.01,
      "gammaCorrection": 1.2
    }
  }
}
```

**Parameters:**

- **V2:** `exposureValue`: -20 to 20 (default: 0) — **V1** used the property name `exposure`.
- `offset`: -0.5 to 0.5 (default: 0)
- `gammaCorrection`: 0.01 to 9.99 (default: 1)

## Hue/Saturation

Both V1 and V2 use the same top-level structure. V2 adds support for **local range** (individual color channels) in addition to the master channel. **V2** requires `type` inside `adjustments`.

```json
{
  "type": "adjustment_layer",
  "name": "Hue/Saturation",
  "adjustments": {
    "type": "hue_saturation",
    "hueSaturation": {
      "colorize": false,
      "hueSaturationAdjustments": [
        {
          "hue": 15,
          "saturation": 20,
          "lightness": -5
        },
        {
          "hue": 5,
          "saturation": 15,
          "lightness": 0,
          "localRange": {
            "channelId": "REDS",
            "beginRamp": 20,
            "beginSustain": 10,
            "endSustain": 100,
            "endRamp": 60
          }
        }
      ]
    }
  }
}
```

**Parameters:**

- **`colorize`** (boolean, required):
  - **`false`**: Normal Hue/Saturation mode. Adjusts hue, saturation, and lightness per adjustment. Use an entry without `localRange` for overall (master) adjustments, or include **`localRange`** for color-specific edits (REDS, YELLOWS, GREENS, CYANS, BLUES, MAGENTAS). When colorize is false, `localRange` can only be used for non-master channels.
  - **`true`**: Colorize mode. Converts the image to a single hue tint (e.g. sepia, duotone, or colored overlay). When colorize is true, `localRange` cannot be used. Useful for toning or stylized color effects.
- **`hueSaturationAdjustments`**: Array of adjustments. Each entry has `hue`, `saturation`, and `lightness`; omit `localRange` for master (entire image), or include **`localRange`** for a specific color range.
  - **`hue`**: -180 to 180 (or 0 to 360 when colorize is true)
  - **`saturation`**: -100 to 100 (or 0 to 100 when colorize is true)
  - **`lightness`**: -100 to 100 (or 0 to 100 when colorize is true)
  - **`localRange`** (optional): Not applicable for the master channel or when `colorize` is true. For non-master channels only when `colorize` is false. Defines the color range and ramp/sustain (0–360 degrees).
    - **`channelId`** (required): `"REDS"`, `"YELLOWS"`, `"GREENS"`, `"CYANS"`, `"BLUES"`, `"MAGENTAS"`.
    - **`beginRamp`**: Start of feather (0–360).
    - **`beginSustain`**: Start of full effect (0–360).
    - **`endSustain`**: End of full effect (0–360).
    - **`endRamp`**: End of feather (0–360).

### Local range (V2)

**Local range** in Hue/Saturation means adjusting only a specific color range in the image, not the whole image. **`localRange` is not applicable with the master channel or when `colorize` is true.** In V2 you can specify multiple entries in `hueSaturationAdjustments`. Omit `localRange` for master (entire image); include **`localRange`** with **`channelId`** for a specific color range when `colorize` is false. Use **`beginRamp`**, **`beginSustain`**, **`endSustain`**, and **`endRamp`** (0–360 degrees) to define the hue range boundaries.

| `channelId` value | Color range affected |
| ----------------- | -------------------- |
| (omit `localRange`) | Entire image (master) |
| `REDS`            | Red color range      |
| `YELLOWS`         | Yellow color range   |
| `GREENS`          | Green color range    |
| `CYANS`           | Cyan color range     |
| `BLUES`           | Blue color range     |
| `MAGENTAS`        | Magenta color range  |

Use local range to change only skin tones (REDS/YELLOWS), skies (BLUES/CYANS), foliage (GREENS), etc. **V1** only supported master; **V2** supports all of the above with optional ramp/sustain tuning.

## Color Balance

**V2** requires `type` inside `adjustments`:

```json
{
  "type": "adjustment_layer",
  "name": "Color Balance",
  "adjustments": {
    "type": "color_balance",
    "colorBalance": {
      "preserveLuminosity": true,
      "shadowLevels": [-10, 5, 15],
      "midtoneLevels": [0, 0, 10],
      "hightoneLevels": [5, -5, 0]
    }
  }
}
```

**Parameters:**

- `preserveLuminosity`: true/false
- `shadowLevels`: Array of 3 integers [-100 to 100]
- `midtoneLevels`: Array of 3 integers [-100 to 100]
- `hightoneLevels`: Array of 3 integers [-100 to 100]

Each array represents: [Cyan-Red, Magenta-Green, Yellow-Blue]

## Editing Existing Adjustment Layers

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Adjustment",
        "edit": {},
        "adjustments": {
          "brightnessContrast": {
            "brightness": 50
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
        "name": "Existing Adjustment",
        "adjustments": {
          "type": "brightness_contrast",
          "brightnessContrast": {
            "brightness": 50
          }
        }
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text"/>

In V2, editing existing layers doesn't require an explicit operation type or edit block. Simply reference the layer and specify new adjustment values.

## Placement Options

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
      // or with relativeTo:
      "type": "above",
      "relativeTo": {"name": "..."}
    }
  }
}
```

See [Image Layer Operations](layer-operations-image.md) for detailed placement migration patterns.

## Creating Documents with Adjustment Layers

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
        "type": "adjustmentLayer",
        "name": "Exposure",
        "adjustments": {
          "exposure": {
            "exposure": 0.5
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
        "type": "adjustment_layer",
        "name": "Exposure",
        "adjustments": {
          "type": "exposure",
          "exposure": {
            "exposureValue": 0.5
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

## Multiple Adjustment Layers

Both V1 and V2 support multiple adjustment layers in one request:

**V2 Example:**

```json
{
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Brightness/Contrast",
        "adjustments": {
          "type": "brightness_contrast",
          "brightnessContrast": {
            "brightness": 20,
            "contrast": 15
          }
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      },
      {
        "type": "adjustment_layer",
        "name": "Hue/Saturation",
        "adjustments": {
          "type": "hue_saturation",
          "hueSaturation": {
            "colorize": false,
            "channels": [
              {
                "channel": "master",
                "saturation": 25
              }
            ]
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
  }
}
```

## Layer Properties

Adjustment layers support standard layer properties:

```json
{
  "type": "adjustment_layer",
  "name": "My Adjustment",
  "isVisible": true,
  "opacity": 80,
  "blendMode": "normal",
  "adjustments": {...}
}
```

<InlineAlert variant="info" slots="text"/>

**transformMode** is not applicable for adjustment layers. Use it only with layer types that support transforms (e.g. image layers).

See [Advanced Layer Operations](layer-operations-advanced.md) for blend modes and other properties.

## Migration Checklist

When migrating adjustment layer operations from V1 to V2:

- [ ] Change `type: "adjustmentLayer"` to `type: "adjustment_layer"`
- [ ] Replace `add` block with `operation.type: "add"`
- [ ] Convert placement directives (insertTop → placement.type: "top", etc.)
- [ ] Remove explicit `edit: {}` block for modifications
- [ ] Convert `visible` to `isVisible` if using visibility
- [ ] Update storage syntax (`href`/`storage` → `url`/`storageType`)
- [ ] Add required `type` inside `adjustments` (e.g. `"type": "brightness_contrast"`) — see [Adjustments Structure](#3-adjustments-structure--required-type-in-v2)
- [ ] For Exposure: rename `exposure` to `exposureValue` inside the exposure payload (V2 only)

## Common Migration Issues

### Issue: Forgetting operation block

**Problem:** V2 requires explicit operation for new layers

**Solution:** Always include operation block when adding

```json
{
  "type": "adjustment_layer",
  "adjustments": {
    "type": "brightness_contrast",
    "brightnessContrast": { "brightness": 30, "contrast": 20 }
  },
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

### Issue: Adjustment values out of range

**Problem:** Same validation rules apply in V1 and V2

**Solution:** Ensure values are within documented ranges

- Brightness/Contrast: -150 to 150
- Exposure (V2: `exposureValue`): -20 to 20
- Hue: -180 to 180
- Saturation/Lightness: -100 to 100

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
        "type": "adjustmentLayer",
        "name": "Brightness/Contrast",
        "add": {
          "insertTop": true
        },
        "adjustments": {
          "brightnessContrast": {
            "brightness": 25,
            "contrast": 10
          }
        }
      },
      {
        "type": "adjustmentLayer",
        "name": "Color Balance",
        "add": {
          "insertTop": true
        },
        "adjustments": {
          "colorBalance": {
            "preserveLuminosity": true,
            "shadowLevels": [10, 0, -10],
            "midtoneLevels": [0, 5, 0],
            "hightoneLevels": [-5, 0, 5]
          }
        },
        "blendOptions": {
          "opacity": 80
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
        "type": "adjustment_layer",
        "name": "Brightness/Contrast",
        "adjustments": {
          "type": "brightness_contrast",
          "brightnessContrast": {
            "brightness": 25,
            "contrast": 10
          }
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      },
      {
        "type": "adjustment_layer",
        "name": "Color Balance",
        "adjustments": {
          "type": "color_balance",
          "colorBalance": {
            "preserveLuminosity": true,
            "shadowLevels": [10, 0, -10],
            "midtoneLevels": [0, 5, 0],
            "hightoneLevels": [-5, 0, 5]
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
}
```

## Feature Availability

### Currently Available in V2

- ✅ Brightness/Contrast adjustments
- ✅ Exposure adjustments
- ✅ Hue/Saturation adjustments, including **local range** (individual color channels: reds, yellows, greens, cyans, blues, magentas)
- ✅ Color Balance adjustments
- ✅ Add adjustment layers
- ✅ Edit existing adjustment layers
- ✅ Layer visibility and opacity

### Not Applicable to Adjustment Layers

- **transformMode** — Use only with layer types that support transforms (e.g. image layers). Adjustment layers do not support transformMode.

### Coming Soon

- ⏳ Additional adjustment layer types

<InlineAlert variant="info" slots="text"/>

If you need adjustment types not currently supported, contact the Adobe DI ART Service team to discuss alternatives or timeline.

## Next steps

- Review [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Check [Image Layers](layer-operations-image.md) for combining with image layers
- See [Advanced Operations](layer-operations-advanced.md) for masks and blend modes

## Need Help?

Contact the Adobe DI ART Service team for technical support with adjustment layer migration.
