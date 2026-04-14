---
title: Artboard Migration
description: Migrate from /pie/psdService/artboards to /v2/create-artboard
hideBreadcrumbNav: true
keywords:
  - artboards
  - migration
  - v1 to v2
---

# Artboard Migration

This guide helps you migrate from the v1 artboards endpoint to `/v2/create-artboard`.

## Overview

The artboard functionality allows you to create artboards from multiple input images, positioning each image with specific bounds. The v2 endpoint provides the same functionality with an updated request/response structure.

**V1 Endpoint:**

- `/pie/psdService/artboards`

**V2 Endpoint:**

- `/v2/create-artboard`

## Best practices

**Planning Artboard Layout:**

1. Calculate total artboard size needed based on all image positions
2. Ensure images don't overlap unless intentional
3. Leave appropriate spacing between images
4. Consider final output resolution requirements

**Performance Tips:**

1. Use appropriately sized source images
2. Batch multiple outputs in a single request
3. Use hosted storage for temporary outputs
4. Consider using embedded storage for small previews

**Output Optimization:**

1. Generate multiple formats in one request (PSD, JPEG, and PNG)
2. Use quality settings appropriate for your use case
3. Specify dimensions for optimized outputs
4. Enable canvas trimming if appropriate

## Migration example

**Key differences from v1 to v2:**

**Input structure:**

- The v1 API's `inputs[].href` is now `images[].source.url` in v2
- The v1 API's `inputs[].storage` is now `outputs[].destination.storageType` in v2

**Output structure:**

- The v1 API's `outputs[].href` is now `outputs[].destination.url` in v2
- The v1 API's `outputs[].type` is now `outputs[].mediaType` in v2
- The v1 API's `outputs[].storage` is now `outputs[].destination.storageType` in v2

### V1 approach

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/artboards \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<IMAGE_1_URL>",
      "storage": "external",
      "bounds": {
        "left": 0,
        "top": 0,
        "width": 500,
        "height": 500
      }
    },
    {
      "href": "<IMAGE_2_URL>",
      "storage": "external",
      "bounds": {
        "left": 550,
        "top": 0,
        "width": 500,
        "height": 500
      }
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
      },
      "bounds": {
        "left": 0,
        "top": 0,
        "width": 500,
        "height": 500
      }
    },
    {
      "source": {
        "url": "<IMAGE_2_URL>"
      },
      "bounds": {
        "left": 550,
        "top": 0,
        "width": 500,
        "height": 500
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

## Input images

Each image requires a source and bounds specification:

```json
{
  "images": [
    {
      "source": {
        "url": "<IMAGE_URL>"
      },
      "bounds": {
        "left": 0,
        "top": 0,
        "width": 500,
        "height": 500
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

## Bounds specification

Bounds define where each image is positioned on the artboard:

```json
{
  "bounds": {
    "left": 0,
    "top": 0,
    "width": 500,
    "height": 500
  }
}
```

**Bounds parameters:**

- `left`: X-coordinate of the left edge (pixels)
- `top`: Y-coordinate of the top edge (pixels)
- `width`: Width of the image placement (pixels, 4-32000)
- `height`: Height of the image placement (pixels, 4-32000)

Alternatively, you can use `right` and `bottom` instead of `width` and `height`:

```json
{
  "bounds": {
    "left": 0,
    "top": 0,
    "right": 500,
    "bottom": 500
  }
}
```

## Output options

The v2 API provides more flexible output options. A maximum of 25 outputs are allowed per request.

### Multiple output formats

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

**Embedded Storage:**

```json
{
  "destination": {
    "embedded": "base64"
  },
  "mediaType": "image/jpeg"
}
```

**Creative Cloud Storage:**

```json
{
  "destination": {
    "creativeCloudPath": "/path/to/output.psd"
  },
  "mediaType": "image/vnd.adobe.photoshop"
}
```

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
      "shouldTrimToCanvas": true
    }
  ]
}
```

**Available Parameters:**

- `width`: Output width in pixels
- `height`: Output height in pixels
- `quality`: JPEG quality (`very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, `photoshop_max`)
- `compression`: PNG compression (`none`, `very_low`, `low`, `medium_low`, `medium`, `medium_high`, `default`, `high`, `very_high`, `maximum`)
- `shouldTrimToCanvas`: Trim to canvas bounds
- `shouldOverwrite`: Overwrite existing files
- `iccProfile`: ICC color profile
- `layers`: Specific layers to include in output

## Complete example with multiple images

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
      },
      "bounds": {
        "left": 0,
        "top": 0,
        "width": 800,
        "height": 600
      }
    },
    {
      "source": {
        "url": "<IMAGE_2_URL>"
      },
      "bounds": {
        "left": 850,
        "top": 0,
        "width": 800,
        "height": 600
      }
    },
    {
      "source": {
        "url": "<IMAGE_3_URL>"
      },
      "bounds": {
        "left": 0,
        "top": 650,
        "width": 800,
        "height": 600
      }
    },
    {
      "source": {
        "url": "<IMAGE_4_URL>"
      },
      "bounds": {
        "left": 850,
        "top": 650,
        "width": 800,
        "height": 600
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
      "quality": "maximum"
    }
  ]
}'
```

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

❌ **Problem:** Using v1 input format

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

✅ **Solution:** Use v2 images structure

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

### Missing bounds

❌ **Problem:** Not providing bounds for images

✅ **Solution:** Each image must have bounds specified

```json
{
  "images": [
    {
      "source": {
        "url": "<URL>"
      },
      "bounds": {
        "left": 0,
        "top": 0,
        "width": 500,
        "height": 500
      }
    }
  ]
}
```

### Invalid bounds values

❌ **Problem:** Bounds values outside valid range

✅ **Solution:** Ensure width and height are between 4 and 32000 pixels

```json
{
  "bounds": {
    "left": 0,
    "top": 0,
    "width": 500,
    "height": 500
  }
}
```

## Next steps

- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for more storage options
- Check the [composite migration guide](composite-migration.md) for advanced layer operations
- Test your artboard creation with development endpoints

## Need help?

Contact the Adobe DI ART Service team for technical support with artboard operations.
