---
title: Artboard Migration
description: Migrate from /pie/psdService/artboardCreate to /v2/create-artboard
hideBreadcrumbNav: true
keywords:
  - artboards
  - migration
  - v1 to v2
---

# Artboard Migration

This guide helps you migrate from the v1 artboardCreate endpoint to `/v2/create-artboard`.

## Overview

The artboard functionality allows you to create artboards from multiple input images. The v2 endpoint provides enhanced functionality with an updated request/response structure, support for more output formats, and an optional artboard spacing parameter.

**V1 Endpoint:**

- `/pie/psdService/artboardCreate`

**V2 Endpoint:**

- `/v2/create-artboard`

## Migration example

### V1 approach

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/artboardCreate \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<IMAGE_1_URL>",
      "storage": "external"
    },
    {
      "href": "<IMAGE_2_URL>",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

### V2 approach

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-artboard \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "images": [
    {
      "source": {
        "url": "<IMAGE_1_URL>"
      }
    },
    {
      "source": {
        "url": "<IMAGE_2_URL>"
      }
    }
  ],
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

## Key differences

**Input structure:**

- V1: `inputs[].href` → V2: `images[].source.url`
- V1: `inputs[].storage` → V2: `outputs[].destination.storageType` (only for Azure/Dropbox)
- V2 adds optional `artboardSpacing` parameter for controlling horizontal spacing

**Output structure:**

- V1: `outputs[].href` → V2: `outputs[].destination.url`
- V1: `outputs[].type` → V2: `outputs[].mediaType`
- V1: `outputs[].storage` → V2: `outputs[].destination.storageType` (optional in V2)
- V2 supports 6 output formats: JPEG, PNG, TIFF, PSD, PSDC

## Input images

Each image requires a source specification. The API arranges images horizontally with configurable spacing between them.

```json
{
  "images": [
    {
      "source": {
        "url": "<IMAGE_URL>"
      }
    }
  ]
}
```

**Source options:**

The source can be specified using various storage types:

**External URL:**

```json
{
  "source": {
    "url": "<PRESIGNED_URL>"
  }
}
```

**Creative Cloud Path:**

```json
{
  "source": {
    "creativeCloudPath": "/path/to/image.jpg"
  }
}
```

**Creative Cloud File ID:**

```json
{
  "source": {
    "creativeCloudFileId": "urn:aaid:..."
  }
}
```

**Lightroom Path:**

```json
{
  "source": {
    "lightroomPath": "/path/to/image.jpg"
  }
}
```

## Artboard spacing

Control the horizontal spacing between artboards using the optional `artboardSpacing` parameter.

```json
{
  "artboardSpacing": 100,
  "images": [
    {
      "source": {
        "url": "<IMAGE_1_URL>"
      }
    },
    {
      "source": {
        "url": "<IMAGE_2_URL>"
      }
    }
  ]
}
```

**Spacing parameter:**

- **Type:** Integer
- **Unit:** Pixels
- **Default:** 50 pixels
- **Optional:** Yes
- **Description:** Horizontal spacing in pixels between each artboard

### Examples with different spacing

**Default spacing (50px):**

```json
{
  "images": [
    {
      "source": { "url": "<IMAGE_1_URL>" }
    },
    {
      "source": { "url": "<IMAGE_2_URL>" }
    }
  ]
}
```

**Custom spacing (200px):**

```json
{
  "artboardSpacing": 200,
  "images": [
    {
      "source": { "url": "<IMAGE_1_URL>" }
    },
    {
      "source": { "url": "<IMAGE_2_URL>" }
    }
  ]
}
```

**Tight spacing (10px):**

```json
{
  "artboardSpacing": 10,
  "images": [
    {
      "source": { "url": "<IMAGE_1_URL>" }
    },
    {
      "source": { "url": "<IMAGE_2_URL>" }
    }
  ]
}
```

## Validation rules

### Input images

- **Minimum:** 1 image required
- **Maximum:** 25 images allowed
- **Required field:** `source` with valid file reference

### Outputs

- **Minimum:** 1 output required
- **Maximum:** 25 outputs allowed
- **Required fields:** `destination` and `mediaType`

## Output options

V2 provides flexible output options with support for multiple formats:

### Supported output formats

**JPEG Output:**

```json
{
  "destination": {
    "url": "<JPEG_URL>"
  },
  "mediaType": "image/jpeg",
  "quality": "maximum",
  "width": 2000
}
```

**PNG Output:**

```json
{
  "destination": {
    "url": "<PNG_URL>"
  },
  "mediaType": "image/png",
  "compression": "medium",
  "width": 1920
}
```

**TIFF Output:**

```json
{
  "destination": {
    "url": "<TIFF_URL>"
  },
  "mediaType": "image/tiff",
  "width": 3000
}
```

**PSD Output:**

```json
{
  "destination": {
    "url": "<PSD_URL>"
  },
  "mediaType": "image/vnd.adobe.photoshop"
}
```

**PSDC (Cloud Document) Output:**

```json
{
  "destination": {
    "url": "<PSDC_URL>"
  },
  "mediaType": "document/vnd.adobe.cpsd+dcxucf"
}
```

**JSON Manifest Output:**

```json
{
  "destination": {
    "url": "<JSON_URL>"
  },
  "mediaType": "application/json"
}
```

### Multiple output formats

Generate multiple formats in a single request:

```json
{
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
      "quality": "maximum",
      "width": 2000
    },
    {
      "destination": {
        "url": "<PNG_URL>"
      },
      "mediaType": "image/png",
      "compression": "medium"
    }
  ]
}
```

### Output storage options

**External Storage:**

```json
{
  "destination": {
    "url": "<PRESIGNED_URL>"
  },
  "mediaType": "image/jpeg"
}
```

**Hosted Storage:**

```json
{
  "destination": {
    "validityPeriod": 3600
  },
  "mediaType": "image/jpeg"
}
```

The `validityPeriod` specifies how long the hosted URL remains valid:

- **Minimum:** 60 seconds (1 minute)
- **Maximum:** 86400 seconds (1 day / 24 hours)
- **Unit:** Seconds
- **Required** when using hosted storage

**Embedded Storage:**

```json
{
  "destination": {
    "embedded": "base64"
  },
  "mediaType": "image/jpeg"
}
```

Supported embedded formats:
- `"base64"` - Base64-encoded image data
- `"string"` - String representation
- `"json"` - JSON format

**Creative Cloud Storage:**

```json
{
  "destination": {
    "creativeCloudPath": "/path/to/output.psd"
  },
  "mediaType": "image/vnd.adobe.photoshop"
}
```

Optional Creative Cloud project ID:

```json
{
  "destination": {
    "creativeCloudPath": "/path/to/output.psd",
    "creativeCloudProjectId": "urn:aaid:sc:US:..."
  },
  "mediaType": "image/vnd.adobe.photoshop"
}
```

**Azure Blob Storage:**

```json
{
  "destination": {
    "url": "<AZURE_PRESIGNED_URL>",
    "storageType": "azure"
  },
  "mediaType": "image/jpeg"
}
```

**Dropbox Storage:**

```json
{
  "destination": {
    "url": "<DROPBOX_URL>",
    "storageType": "dropbox"
  },
  "mediaType": "image/jpeg"
}
```

<InlineAlert variant="info" slots="text"/>

The `storageType` field is only required for Azure Blob Storage and Dropbox. AWS S3 presigned URLs do not require this field.

## Output parameters

Control output rendering with additional parameters:

```json
{
  "outputs": [
    {
      "destination": {
        "url": "<JPEG_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 1920,
      "height": 1080,
      "maxWidth": 2400
    }
  ]
}
```

**Available parameters:**

- `width`: Output width in pixels (>= 0)
- `height`: Output height in pixels (>= 0)
- `maxWidth`: Maximum width constraint in pixels (>= 0)
- `quality`: JPEG quality (`very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, `photoshop_max`)
- `compression`: PNG compression (`none`, `very_low`, `low`, `medium_low`, `medium`, `medium_high`, `default`, `high`, `very_high`, `maximum`)
- `shouldOverwrite`: Overwrite existing files (boolean)
- `iccProfile`: ICC color profile for color management (standard or custom)
- `layers`: Specific layers to include in output (array of layer references)
- `cropMode`: Crop mode for layer export (`trim_to_transparency`, `document_bounds`, `layer_bounds`)

### Advanced output features

**Layer-specific export:**

```json
{
  "destination": {
    "url": "<OUTPUT_URL>"
  },
  "mediaType": "image/png",
  "layers": [
    {
      "id": 123
    },
    {
      "name": "Background"
    }
  ]
}
```

**ICC color profile:**

```json
{
  "destination": {
    "url": "<OUTPUT_URL>"
  },
  "mediaType": "image/jpeg",
  "iccProfile": {
    "type": "standard",
    "name": "sRGB IEC61966-2.1",
    "imageMode": "rgb"
  }
}
```

See the [ICC Profile Migration guide](icc-profile-migration.md) for detailed color management options.

**Crop mode:**

```json
{
  "destination": {
    "url": "<OUTPUT_URL>"
  },
  "mediaType": "image/png",
  "cropMode": "trim_to_transparency"
}
```

## Complete example with multiple images

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-artboard \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "artboardSpacing": 100,
  "images": [
    {
      "source": {
        "url": "<IMAGE_1_URL>"
      }
    },
    {
      "source": {
        "url": "<IMAGE_2_URL>"
      }
    },
    {
      "source": {
        "url": "<IMAGE_3_URL>"
      }
    },
    {
      "source": {
        "url": "<IMAGE_4_URL>"
      }
    }
  ],
  "outputs": [
    {
      "destination": {
        "url": "<PSD_OUTPUT_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": {
        "url": "<JPEG_OUTPUT_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2400
    },
    {
      "destination": {
        "validityPeriod": 7200
      },
      "mediaType": "image/png",
      "compression": "high"
    }
  ]
}'
```

This example:
1. Creates artboards from 4 images with 100px spacing between them
2. Generates a PSD output at original resolution
3. Generates a high-quality JPEG at 2400px width
4. Generates a PNG with hosted storage (2-hour validity)

## Status checking

Check the status of your artboard job:

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

See the [status migration guide](status-migration.md) for details on the response format.

## Common migration issues

### Incorrect input structure

**Problem:** Using v1 input format

```json
{
  "inputs": [
    {
      "href": "<URL>",
      "storage": "external"
    }
  ]
}
```

**Solution:** Use v2 images structure

```json
{
  "images": [
    {
      "source": {
        "url": "<URL>"
      }
    }
  ]
}
```

### Too many images

**Problem:** Exceeding the maximum number of images

**Error:**
```
Array size must be between 1 and 25 at path 'images'
```

**Solution:** Ensure you have between 1 and 25 images in your request

### Too many outputs

**Problem:** Exceeding the maximum number of outputs

**Error:**
```
Array size must be between 1 and 25 at path 'outputs'
```

**Solution:** Ensure you have between 1 and 25 outputs in your request

### Missing required fields

**Problem:** Missing source in image

**Error:**
```
Required field 'source' is missing at path 'images[0]'
```

**Solution:** Every image must have a source field

```json
{
  "images": [
    {
      "source": {
        "url": "<URL>"
      }
    }
  ]
}
```

### Invalid hosted storage period

**Problem:** Hosted storage validityPeriod outside allowed range

**Error:**
```
validityPeriod must be between 60 and 86400 seconds
```

**Solution:** Use a value between 60 seconds (1 minute) and 86400 seconds (24 hours)

```json
{
  "destination": {
    "validityPeriod": 3600
  }
}
```

### Missing storage type for Azure/Dropbox

**Problem:** Using Azure or Dropbox without specifying storageType

**Error:**
```
Azure Blob Storage URL requires 'storageType': 'azure'
```

**Solution:** Add storageType for Azure and Dropbox

```json
{
  "destination": {
    "url": "<AZURE_URL>",
    "storageType": "azure"
  }
}
```

### Invalid JPEG quality value

**Problem:** Using numeric quality instead of string enum

**Error:**
```
Invalid value '7' at path 'outputs[0].quality'. Accepted values are: very_poor, poor, low, medium, high, maximum, photoshop_max
```

**Solution:** Use string enum values for quality

```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum"
}
```

## Best practices

**Planning artboard layout:**

1. Use appropriate artboardSpacing for your design needs (default is 50px)
2. Consider the order of images in the array - they'll be arranged left to right
3. Calculate total output width: (image widths) + (spacing x (number of images - 1))
4. Consider final output resolution requirements

**Performance tips:**

1. Use appropriately sized source images
2. Batch multiple outputs in a single request (up to 25)
3. Use hosted storage for temporary outputs
4. Consider using embedded storage for small previews

**Output optimization:**

1. Generate multiple formats in one request (PSD + JPEG + PNG)
2. Use quality settings appropriate for your use case
3. Specify dimensions for optimized outputs
4. Use ICC profiles for color-critical work

**Storage strategy:**

1. Use AWS S3 presigned URLs when possible (no storageType needed)
2. Specify validityPeriod for hosted URLs based on your download timeline
3. Use Creative Cloud storage for persistent assets
4. Add storageType only for Azure Blob Storage and Dropbox

## Complete V1 parity reference

For a single-page authoritative field-level comparison of every V1 field and how it maps to V2
— including the V1 input structure, all storage-to-destination mappings,
crop mode migration, quality/compression enum mappings, and status response changes — see the
**[Create Artboard — Complete V1 Migration Reference](create-artboard-v1-reference.md)**.

## Next steps

- Review the [output types migration guide](output-types-migration.md) for detailed format options
- Check the [ICC profile migration guide](icc-profile-migration.md) for color management
- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for more storage options
- Check the [composite migration guide](composite-migration.md) for advanced layer operations
- Test your artboard creation with development endpoints

## Related migration guides

- [Output Types Migration](output-types-migration.md) - JPEG, PNG, PSD, TIFF output format changes
- [ICC Profile Migration](icc-profile-migration.md) - Color management for output exports
- [Status Migration](status-migration.md) - Job status checking in V2
- [Migration Overview](index.md) - Complete V1 to V2 migration overview
