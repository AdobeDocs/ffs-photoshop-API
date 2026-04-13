---
title: Edit Operations Migration
description: Migrate from individual Lightroom API endpoints to the unified /v2/edit endpoint
hideBreadcrumbNav: true
keywords:
  - edit operations
  - Lightroom API
  - autoTone
  - autoStraighten
  - migration
  - v1 to v2
---

# Edit Operations Migration

This guide helps you migrate from individual Lightroom v1 endpoints to the unified `/v2/edit` endpoint.

## Overview

In v1, Lightroom editing operations were split across multiple endpoints. V2 consolidates all edit operations into a single `/v2/edit` endpoint, allowing you to combine multiple adjustments in one API call.

**V1 Endpoints Being Consolidated:**

| V1 Endpoint                 | V2 Equivalent                           |
| --------------------------- | --------------------------------------- |
| `/lrService/autoTone`       | `/v2/edit` with `autoTone: true`        |
| `/lrService/autoStraighten` | `/v2/edit` with `autoStraighten` object |
| `/lrService/presets`        | `/v2/edit` with `presets` array         |
| `/lrService/xmp`            | `/v2/edit` with `xmp` object            |
| `/lrService/edit`           | `/v2/edit` with adjustment parameters   |

## Benefits of the unified v2 endpoint

- **Single API Call:** Combine multiple adjustments instead of chaining requests
- **Better Performance:** Reduced network overhead and faster processing
- **Atomic Operations:** All adjustments succeed or fail together
- **Flexible Outputs:** Multiple output formats and destinations in one request

## Migration examples

### Auto tone

**Key Differences:**

- Input structure changed from `inputs.href` to `image.source.url`
- Output structure changed from `outputs[].href` to `outputs[].destination.url`
- Media type moved from `outputs[].type` to `outputs[].mediaType`
- `storageType` is optional for external presigned URLs; only required for Azure or Dropbox

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/lrService/autoTone \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoTone": true
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

### Auto straighten

**Key Differences:**

- V2 provides more control with `constrainCrop` and `uprightMode` options
- Options: `uprightMode` can be `auto`, `full`, `level`, or `vertical`
- Default `constrainCrop` is `true` to remove blank edges

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/lrService/autoStraighten \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoStraighten": {
      "enabled": true,
      "constrainCrop": true,
      "uprightMode": "auto"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

### Apply presets

**Key Differences:**

- Presets are now nested inside the `edits` object
- Maximum 10 presets allowed
- Preset structure changed from `href` to `source.url`

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/lrService/presets \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  },
  "options": {
    "presets": [
      {
        "href": "<PRESET_URL>",
        "storage": "external"
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "presets": [
      {
        "source": {
          "url": "<PRESET_URL>"
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

### Apply XMP

**Key Differences:**

- XMP is now nested inside the `edits` object
- Structure changed from `options.xmp.href` to `edits.xmp.source.url`

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/lrService/xmp \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  },
  "options": {
    "xmp": {
      "href": "<XMP_URL>",
      "storage": "external"
    }
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      }
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

### Apply XMP with masks (advanced)

For advanced Camera Raw editing workflows, you can include mask data alongside your XMP metadata. Masks are binary files that define selection areas for localized adjustments in Camera Raw.

**Key Points:**

- Masks are **optional** and only needed for advanced Camera Raw editing
- Each mask requires both a `source` (URL to the mask file) and a `digest` (fingerprint for identification)
- The `digest` is a unique identifier used to associate the mask data with the XMP adjustments
- Mask files are typically binary `.bin` files generated by Adobe Camera Raw
- Multiple masks can be provided for workflows with multiple localized adjustments

**V2 Approach with Masks:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        }
      ]
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

**Multiple Masks:**

You can include multiple mask files for complex editing workflows:

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_1_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        },
        {
          "source": {
            "url": "<MASK_FILE_2_URL>"
          },
          "digest": "D15158972C7044869B171697AEBAFB0F"
        }
      ]
    }
  }
}
```

### Apply XMP with orientation override

You can override the image's embedded orientation metadata by specifying an `orientation` parameter within the `xmp` object. This is useful for applying rotation or flip transformations as part of your Camera Raw workflow.

**Key Points:**

- `orientation` is **optional** and only overrides the image's embedded orientation when specified
- If not provided, the image's embedded EXIF orientation metadata is used
- The orientation value uses descriptive string names (e.g., `"right_top"`) rather than numeric codes
- Orientation transformations are applied during image processing, with automatic width/height adjustments for 90°/270° rotations

**V2 Approach with Orientation:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "orientation": "right_top"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

**Orientation Values:**

The `orientation` parameter follows the EXIF/TIFF specification for image orientation:

| Value | Description |
|-------|-------------|
| `"top_left"` | Column 0 = left, Row 0 = top (normal orientation) |
| `"top_right"` | Column 0 = right, Row 0 = top (horizontal flip) |
| `"bottom_right"` | Column 0 = right, Row 0 = bottom (180° rotation) |
| `"bottom_left"` | Column 0 = left, Row 0 = bottom (vertical flip) |
| `"left_top"` | Column 0 = top, Row 0 = left (90° CCW rotation + horizontal flip) |
| `"right_top"` | Column 0 = top, Row 0 = right (90° CW rotation) |
| `"right_bottom"` | Column 0 = bottom, Row 0 = right (90° CCW rotation) |
| `"left_bottom"` | Column 0 = bottom, Row 0 = left (90° CW rotation + horizontal flip) |

**Combined with Masks:**

You can use orientation together with masks for complete control over your Camera Raw editing workflow:

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<XMP_URL>"
      },
      "orientation": "right_top",
      "masks": [
        {
          "source": {
            "url": "<MASK_FILE_URL>"
          },
          "digest": "37B3568A954F0C80CA946DA0187FB9E2"
        }
      ]
    }
  }
}
```

### Manual adjustments

**Key Differences:**

- Adjustments are now nested inside the `edits` object and organized into logical groups: `light`, `color`, `effects`, `sharpen`
- Parameter names are camelCase instead of PascalCase
- More comprehensive adjustment options available

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/lrService/edit \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": {
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  },
  "options": {
    "Exposure": 1.2,
    "Contrast": 10,
    "Saturation": 20
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "light": {
      "exposure": 1.2,
      "contrast": 10
    },
    "color": {
      "saturation": 20
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

### Adjustment categories in v2

The v2 `/edit` endpoint organizes adjustments into categories:

**Light Adjustments (`light`):**

- `exposure` (-5.0 to 5.0)
- `contrast` (-100 to 100)
- `highlights` (-100 to 100)
- `shadows` (-100 to 100)
- `whites` (-100 to 100)
- `blacks` (-100 to 100)

**Color Adjustments (`color`):**

- `saturation` (-100 to 100)
- `vibrance` (-100 to 100)
- `whiteBalance` (2000 to 50000 Kelvin)

**Effects Adjustments (`effects`):**

- `clarity` (-100 to 100)
- `dehaze` (-100 to 100)
- `texture` (-100 to 100)
- `vignette` (-100 to 100)

**Sharpen Adjustments (`sharpen`):**

- `detail` (0 to 100)
- `radius` (0.5 to 3.0)
- `edgeMasking` (0 to 100)

**Noise Reduction (`noiseReduction`):**

- `luminance` (0 to 100)
- `color` (0 to 100)

## Combining multiple operations

One of the biggest advantages of v2 is the ability to combine multiple operations in a single request.

**V1 Approach (Multiple Calls):**

```shell
# Step 1: Auto tone
curl -X POST https://image.adobe.io/lrService/autoTone ...

# Step 2: Auto straighten
curl -X POST https://image.adobe.io/lrService/autoStraighten ...

# Step 3: Apply adjustments
curl -X POST https://image.adobe.io/lrService/applyEdits ...
```

**V2 Approach (Single Call):**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoTone": true,
    "autoStraighten": {
      "enabled": true
    },
    "light": {
      "exposure": 0.5,
      "contrast": 15
    },
    "color": {
      "saturation": 10
    },
    "sharpen": {
      "detail": 50
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

## Output options

V2 provides more flexible output options. You can now:

**Multiple Outputs:**

```json
"outputs": [
  {
    "destination": {
      "url": "<JPEG_URL>"
    },
    "mediaType": "image/jpeg"
  },
  {
    "destination": {
      "url": "<PNG_URL>"
    },
    "mediaType": "image/png"
  },
  {
    "destination": {
      "url": "<TIFF_URL>"
    },
    "mediaType": "image/tiff"
  },
  {
    "destination": {
      "url": "<XMP_URL>"
    },
    "mediaType": "application/rdf+xml"
  }
]
```

**Maximum 25 outputs allowed per request.**

## Returning XMP metadata

You can export XMP metadata that contains all the edit adjustments applied to the image. This is useful for:

- Saving edit presets
- Understanding what adjustments were applied
- Reapplying the same edits to other images
- Integration with other XMP-compatible tools

### XMP with Auto Tone

**Example: Auto Tone with XMP Output**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoTone": true
  },
  "outputs": [
    {
      "destination": {
        "url": "<JPEG_OUTPUT_URL>"
      },
      "mediaType": "image/jpeg"
    },
    {
      "destination": {
        "url": "<XMP_OUTPUT_URL>"
      },
      "mediaType": "application/rdf+xml"
    }
  ]
}'
```

This will generate two outputs:

1. The edited JPEG image with auto tone applied
2. An XMP file containing the adjustment values that were applied

### Inline XMP (Embedded)

For immediate access to XMP metadata without external storage, use embedded output:

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoTone": true,
    "light": {
      "exposure": 0.5,
      "contrast": 10
    },
    "color": {
      "saturation": 15
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<JPEG_OUTPUT_URL>"
      },
      "mediaType": "image/jpeg"
    },
    {
      "destination": {
        "embedded": "string"
      },
      "mediaType": "application/rdf+xml"
    }
  ]
}'
```

**Job Status Response with Embedded XMP:**

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "succeeded",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "modifiedTime": "2025-01-15T10:30:45.000Z",
  "result": {
    "outputs": [
      {
        "destination": {
          "url": "https://storage.example.com/output.jpg"
        },
        "mediaType": "image/jpeg"
      },
      {
        "destination": {
          "embedded": "string",
          "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<x:xmpmeta xmlns:x=\"adobe:ns:meta/\" x:xmptk=\"Adobe XMP Core 7.0-c000\">\n  <rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n    <rdf:Description rdf:about=\"\"\n        xmlns:crs=\"http://ns.adobe.com/camera-raw-settings/1.0/\">\n      <crs:Exposure2012>+0.50</crs:Exposure2012>\n      <crs:Contrast2012>+10</crs:Contrast2012>\n      <crs:Saturation>+15</crs:Saturation>\n      <crs:AutoTone>True</crs:AutoTone>\n    </rdf:Description>\n  </rdf:RDF>\n</x:xmpmeta>"
        },
        "mediaType": "application/rdf+xml"
      }
    ]
  }
}
```

### XMP Output Options

**External Storage:**

```json
{
  "destination": {
    "url": "<XMP_URL>"
  },
  "mediaType": "application/rdf+xml"
}
```

**Hosted Storage:**

```json
{
  "destination": {
    "validityPeriod": 3600
  },
  "mediaType": "application/rdf+xml"
}
```

**Embedded (Inline):**

```json
{
  "destination": {
    "embedded": "string"
  },
  "mediaType": "application/rdf+xml"
}
```

**Creative Cloud Storage:**

```json
{
  "destination": {
    "creativeCloudPath": "/path/to/adjustments.xmp"
  },
  "mediaType": "application/rdf+xml"
}
```

### Using XMP Output

The generated XMP file can be:

1. **Reapplied to other images** using the `xmp` parameter inside `edits`:

   ```json
   {
     "edits": {
       "xmp": {
         "source": {
           "url": "<XMP_FILE_URL>"
         }
       }
     }
   }
   ```

2. **Saved as a preset** for consistent editing across multiple images.

3. **Imported into Lightroom** or other XMP-compatible applications.

4. **Inspected to understand** what adjustments were automatically applied by `autoTone`.

### Complete Example: Auto Tone with Inline XMP

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/edit \
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
    "autoTone": true,
    "autoStraighten": {
      "enabled": true
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<JPEG_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum"
    },
    {
      "destination": {
        "embedded": "string"
      },
      "mediaType": "application/rdf+xml"
    }
  ]
}'
```

**Why Use Embedded XMP:**

- **Immediate Access** - Get XMP in the status response without additional downloads
- **No Storage Needed** - No need to manage XMP file storage
- **Simplified Workflow** - Single status check gets both image URL and XMP data
- **Perfect for Automation** - Easy to parse and store in your database

<InlineAlert variant="info" slots="text"/>

Embedded storage is only recommended for text-based outputs like XMP metadata. For image outputs, use external, hosted, or Creative Cloud storage instead.

**Use Cases:**

- **Preset Creation** - Auto-generate presets from successful edits
- **Batch Processing** - Apply same adjustments to multiple images
- **Audit Trail** - Record what adjustments were applied
- **Learning Tool** - See what values `autoTone` automatically selected

## Status checking

The status checking process uses a unified endpoint:

See the [status migration guide](status-migration.md) for details on response format changes.

## Common migration issues

<InlineAlert variant="warning" slots="header, text"/>

**Payload Size Limits:**

Keep inline content (embedded XMP or other text-based content) limited to 50 KB and overall request payload size below 1 MB. For larger resources, use external storage with presigned URLs.

### Storage parameter not recognized

**Problem:** Using `storage` parameter from v1

```json
"outputs": [
  {
    "url": "<SIGNED_POST_URL>",
    "storage": "external"
  }
]
```

**Solution:** Use proper destination structure. Note that `storageType` is optional for external presigned URLs.

```json
"outputs": [
  {
    "destination": {
      "url": "<SIGNED_POST_URL>"
    }
  }
]
```

For Azure or Dropbox, include `storageType`:

```json
"outputs": [
  {
    "destination": {
      "url": "<SIGNED_POST_URL>",
      "storageType": "azure"
    }
  }
]
```

### Invalid parameter names

**Problem:** Using PascalCase parameter names from v1

```json
{
  "Exposure": 1.2,
  "Contrast": 10
}
```

**Solution:** Use camelCase and group into categories inside the `edits` object

```json
{
  "edits": {
    "light": {
      "exposure": 1.2,
      "contrast": 10
    }
  }
}
```

### Missing media type

**Problem:** Using `type` instead of `mediaType`

```json
"outputs": [
  {
    "destination": {...},
    "type": "image/jpeg"
  }
]
```

**Solution:** Use `mediaType`

```json
"outputs": [
  {
    "destination": {...},
    "mediaType": "image/jpeg"
  }
]
```

## Next steps

- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for new storage options
- Check the [status migration guide](status-migration.md) for status checking changes
- Test your migration with development endpoints before production deployment

## Deprecated and removed endpoints

The following Lightroom v1 endpoints have been deprecated or removed and have no direct v2 migration path:

### Deprecated endpoints

**`/lrService/mask`**

- Status: Deprecated and removed as a standalone endpoint
- V2 Migration: Mask functionality is now available through the XMP feature in `/v2/edit`
- See the [Apply XMP with Masks](#apply-xmp-with-masks-advanced) section above for usage details
- Masks are now provided as part of the `edits.xmp.masks` array alongside XMP metadata

**`/lrService/predict`**

- Status: Deprecated and removed
- Reason: Refer to the deprecation notice for details

**`/lrService/depthRefinement`**

- Status: Deprecated
- Reason: Feature no longer supported

### Removed endpoints

**`/lrService/index`**

- Status: Removed
- No v2 equivalent available

### Coming soon

**`/lrService/xmpToPreset`**

- Status: To be implemented
- Expected: V2 equivalent is planned for a future release

<InlineAlert variant="info" slots="text"/>

If your application depends on any of these deprecated or removed endpoints, please contact the Adobe DI ART Service team to discuss alternative solutions.

## Need help?

Contact the Adobe DI ART Service team if you encounter issues during migration.
