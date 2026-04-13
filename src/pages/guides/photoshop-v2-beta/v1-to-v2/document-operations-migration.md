---
title: Document Operations Migration (V1 to V2)
description: Migrate from /pie/psdService/documentOperations to /v2/create-composite for document-level editing operations
hideBreadcrumbNav: true
keywords:
  - documentOperations
  - crop
  - resize
  - trim
  - canvas
  - document editing
  - PSD
  - migration
  - v1 to v2
---

# Document Operations Migration (V1 to V2)

This guide helps you migrate from the v1 `/pie/psdService/documentOperations` endpoint to the v2 `/create-composite` endpoint for document-level editing operations.

## Overview

In v1, the `/documentOperations` endpoint was used for document-level operations like cropping, resizing, and trimming existing PSD files. These operations affect the entire document rather than individual layers.

**V1 Endpoint:**

```text
POST /pie/psdService/documentOperations
```

**V2 Endpoint:**

```text
POST /v2/create-composite
```

In v2, document operations are specified in the `edits.document` object within the `/create-composite` request.

<InlineAlert variant="warning" slots="header,text"/>

Important:

V2 currently supports a subset of V1 document operation features. Additional capabilities are being added incrementally. Review the available operations below to ensure your use case is supported.

## Key differences

- **Request Structure:** Operations moved to the `edits.document` object.
- **Operation Names:** Some operation names and parameters have changed.
- **Enhanced Options:** More granular control over operations.
- **Feature Parity:** Not all v1 features are available yet in v2.

## Available document operations

V2 currently supports the following document operations:

- **Resize** - Change document dimensions.
- **Crop** - Crop document to specified bounds.
- **Trim** - Remove transparent pixels from edges.

## When to use document operations

Use **Document Operations** when:

- Resizing entire documents
- Cropping to specific dimensions
- Removing transparent edges
- Preparing images for specific output sizes

Use **[Format Conversion](format-conversion-migration.md)** when:

- Converting PSDs to other formats without edits
- Generating multiple output formats
- Exporting without modifications

Use **[Document Creation](document-creation-migration.md)** when:

- Creating new blank documents
- Building templates from scratch
- Starting with specific dimensions

Use **[Composite Operations](composite-migration.md)** when:

- Adding, removing, or modifying layers
- Applying layer effects
- Complex multi-layer compositions

## Resize operations

Resize changes the dimensions of the entire document, affecting all layers.

**Key Points:**

- `width` and `height` are now Objects with `unit` (e.g. `pixels_unit`, `percent_unit`) and `value`.
- `constrainProportions` maintains aspect ratio (default `true`).
- `resample` controls the algorithm — `bicubic`, `bicubic_smoother`, `bicubic_sharper`, `bilinear`, `nearest_neighbor`.
- `scaleStyles` scales layer effects proportionally (default `true`).
- `rasterize` rasterizes layers during resize (default `false`).

**V2 Example:**

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
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 1920
        },
        "height": {
          "unit": "pixels_unit",
          "value": 1080
        },
        "constrainProportions": true,
        "resample": "bicubic",
        "scaleStyles": true
      }
    }
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

### Resize parameters

**`width` and `height`**

Both width and height are objects with `unit` and `value` properties:

```json
{
  "width": {
    "unit": "pixels_unit",
    "value": 1920
  },
  "height": {
    "unit": "pixels_unit",
    "value": 1080
  }
}
```

**Unit Types:**

- `pixels_unit` - Absolute pixel measurements
- `percent_unit` - Percentage-based scaling
- `distance_unit` - Physical measurements in points

**`constrainProportions`**

- Type: Boolean
- Default: `true`
- Description: Maintain aspect ratio when resizing
- When `true`: Only need to specify one dimension

**`resample`**

- Type: String
- Default: `"bicubic"`
- Options:
  - `"nearest_neighbor"` - Fastest, lowest quality
  - `"bilinear"` - Fast, moderate quality
  - `"bicubic"` - Balanced quality and speed (recommended)
  - `"bicubic_smoother"` - Good for upscaling
  - `"bicubic_sharper"` - Good for downscaling
- Description: Resampling algorithm for resizing

**`scaleStyles`**

- Type: Boolean
- Default: `true`
- Description: Scale layer styles (effects) proportionally

**`rasterize`**

- Type: Boolean
- Default: `false`
- Description: Rasterize layers during resize

### Resize examples

**Resize with Constrained Proportions:**

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 1920
        },
        "constrainProportions": true,
        "resample": "bicubic"
      }
    }
  }
}
```

When `constrainProportions` is `true`, you only need to specify width OR height. The other dimension will be calculated automatically.

**Resize by Percentage:**

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "percent_unit",
          "value": 50
        },
        "height": {
          "unit": "percent_unit",
          "value": 50
        },
        "resample": "bicubic_sharper"
      }
    }
  }
}
```

**Resize to Exact Dimensions:**

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 800
        },
        "height": {
          "unit": "pixels_unit",
          "value": 600
        },
        "constrainProportions": false,
        "resample": "bicubic"
      }
    }
  }
}
```

**Upscaling with Smooth Interpolation:**

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 4000
        },
        "constrainProportions": true,
        "resample": "bicubic_smoother",
        "scaleStyles": true
      }
    }
  }
}
```

**Downscaling with Sharp Interpolation:**

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 800
        },
        "constrainProportions": true,
        "resample": "bicubic_sharper",
        "scaleStyles": true
      }
    }
  }
}
```

## Crop operations

Crop removes portions of the document based on specified boundaries.

**Key Points:**

- `bounds`: Rectangle, in pixels, (`left`, `top`, `right`, `bottom`) relative to document origin.
- `hide`: `false` for destructive crop (delete pixels), `true` for non-destructive (hide pixels, but preserve data).

**V2 Approach:**

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
    "document": {
      "crop": {
        "bounds": {
          "left": 100,
          "top": 100,
          "right": 1820,
          "bottom": 980
        },
        "hide": false
      }
    }
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

### Crop parameters

**`bounds`**

Defines the crop rectangle in pixels:

```json
{
  "bounds": {
    "left": 100, // Left edge X coordinate
    "top": 100, // Top edge Y coordinate
    "right": 1820, // Right edge X coordinate
    "bottom": 980 // Bottom edge Y coordinate
  }
}
```

- All values are in pixels
- Coordinates are relative to the document origin (0,0 at top-left)

**`hide`**

- Type: Boolean
- Default: `false`
- Description:
  - `false` - Destructive crop (deletes pixels outside bounds)
  - `true` - Non-destructive crop (hides pixels, preserves data)

### Crop examples

**Destructive Crop (Delete Pixels):**

```json
{
  "edits": {
    "document": {
      "crop": {
        "bounds": {
          "left": 0,
          "top": 0,
          "right": 1920,
          "bottom": 1080
        },
        "hide": false
      }
    }
  }
}
```

**Non-Destructive Crop (Hide Pixels):**

```json
{
  "edits": {
    "document": {
      "crop": {
        "bounds": {
          "left": 100,
          "top": 100,
          "right": 1820,
          "bottom": 980
        },
        "hide": true
      }
    }
  }
}
```

**Center Crop:**

For a 1920x1080 image, crop to 1200x800 centered:

```json
{
  "edits": {
    "document": {
      "crop": {
        "bounds": {
          "left": 360, // (1920 - 1200) / 2
          "top": 140, // (1080 - 800) / 2
          "right": 1560, // 360 + 1200
          "bottom": 940 // 140 + 800
        },
        "hide": false
      }
    }
  }
}
```

**Square Crop:**

```json
{
  "edits": {
    "document": {
      "crop": {
        "bounds": {
          "left": 420, // Center 1080x1080 in 1920 width
          "top": 0,
          "right": 1500, // 420 + 1080
          "bottom": 1080
        },
        "hide": false
      }
    }
  }
}
```

## Trim operations

Trim automatically removes transparent pixels from the edges of the document.

**Key Points:**

- `trimUpon` is the basis for trim in v2, instead of `"transparent_pixels"` in v1.

**V2 Approach:**

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
    "document": {
      "trim": {
        "trimUpon": "transparent_pixels"
      }
    }
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

### Trim parameters

**`trimUpon`**

- Type: String
- Current options: `"transparent_pixels"`
- Description: Basis for trim operation

<InlineAlert variant="info" slots="text"/>

Additional trim options (like trim based on pixel color) are planned for future releases.

## Combining multiple document operations

You can combine multiple document operations in a single request. Operations are applied in order: resize, then crop, then trim.

**Key Points:**

- Include `resize`, `crop`, and `trim` in a single `edits.document` object.
- Operations execute in order: resize → crop → trim.

**V2 Approach:**

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
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 2000
        },
        "constrainProportions": true,
        "resample": "bicubic"
      },
      "crop": {
        "bounds": {
          "left": 100,
          "top": 100,
          "right": 1900,
          "bottom": 1000
        },
        "hide": false
      },
      "trim": {
        "trimUpon": "transparent_pixels"
      }
    }
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

## Combining with output conversion

Apply document operations and convert to different formats in one request:

**Key Points:**

- Use `edits.document` for operations and multiple `outputs[]` entries for different formats (e.g. PSD and JPEG in one call).

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
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 1920
        },
        "constrainProportions": true,
        "resample": "bicubic"
      }
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<PSD_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": {
        "url": "<JPEG_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high"
    }
  ]
}'
```

## Common use cases

### Thumbnail generation

Resize and crop to create thumbnails:

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 400
        },
        "constrainProportions": true,
        "resample": "bicubic_sharper"
      }
    }
  }
}
```

### Image optimization

Resize for web delivery:

```json
{
  "edits": {
    "document": {
      "resize": {
        "width": {
          "unit": "pixels_unit",
          "value": 1920
        },
        "constrainProportions": true,
        "resample": "bicubic"
      }
    }
  }
}
```

### Aspect ratio correction

Crop to specific aspect ratio (e.g., 16:9):

```json
{
  "edits": {
    "document": {
      "crop": {
        "bounds": {
          "left": 0,
          "top": 120,
          "right": 1920,
          "bottom": 1200
        },
        "hide": false
      }
    }
  }
}
```

### Clean up transparent edges

Trim unnecessary transparent space:

```json
{
  "edits": {
    "document": {
      "trim": {
        "trimUpon": "transparent_pixels"
      }
    }
  }
}
```

## Common migration issues

### Invalid unit type

❌ **Problem:** Using incorrect unit type

```json
{
  "width": {
    "unit": "px",
    "value": 1920
  }
}
```

✅ **Solution:** Use valid unit types

```json
{
  "width": {
    "unit": "pixels_unit",
    "value": 1920
  }
}
```

### Missing unit object

❌ **Problem:** Specifying width/height as numbers

```json
{
  "resize": {
    "width": 1920,
    "height": 1080
  }
}
```

✅ **Solution:** Use proper unit object structure

```json
{
  "resize": {
    "width": {
      "unit": "pixels_unit",
      "value": 1920
    },
    "height": {
      "unit": "pixels_unit",
      "value": 1080
    }
  }
}
```

### Invalid crop bounds

❌ **Problem:** Crop bounds outside document dimensions

```json
{
  "bounds": {
    "left": 0,
    "top": 0,
    "right": 5000, // Exceeds document width
    "bottom": 3000 // Exceeds document height
  }
}
```

✅ **Solution:** Ensure bounds are within document dimensions

```json
{
  "bounds": {
    "left": 0,
    "top": 0,
    "right": 1920, // Within document width
    "bottom": 1080 // Within document height
  }
}
```

## Feature availability

### Currently available

- ✅ Resize with multiple resampling methods
- ✅ Resize by pixels or percentage
- ✅ Constrain proportions option
- ✅ Scale layer styles option
- ✅ Crop with specified bounds
- ✅ Destructive and non-destructive crop
- ✅ Trim transparent pixels

### Coming soon

- ⏳ Canvas size adjustments
- ⏳ Trim based on pixel color
- ⏳ Additional trim options
- ⏳ Image rotation operations
- ⏳ Advanced resampling algorithms

## Next steps

- Review the [composite operations guide](composite-migration.md) for layer manipulation
- Check the [format conversion guide](format-conversion-migration.md) for output options
- Test your document operations with development endpoints

## Need help?

Contact the Adobe DI ART Service team for technical support with document operations.
