---
title: Document Creation Migration
description: Migrate from /pie/psdService/documentCreate to /v2/create-composite for creating new blank documents
hideBreadcrumbNav: true
keywords:
  - documentCreate
  - create document
  - new document
  - blank document
  - PSD
  - migration
  - v1 to v2
---

# Document Creation Migration

This guide helps you migrate from the v1 `/pie/psdService/documentCreate` endpoint to the v2 `/create-composite` endpoint for creating new blank documents from parameters.

## Overview

In v1, the `/documentCreate` endpoint was used to create new blank Photoshop documents with specified dimensions, resolution, color mode, and other properties.

**V1 Endpoint:**

```shell
POST /pie/psdService/documentCreate
```

**V2 Endpoint:**

```shell
POST /v2/create-composite
```

<InlineAlert variant="info" slots="header,text"/>

Note:

For artboard-based documents, use the separate `/v2/create-artboard` endpoint. See the [Artboard Migration guide](artboard-migration.md).

## Key differences

- **Request Structure:** Document parameters moved to the `image` object.
- **Parameter Names:** Some parameter names have changed (e.g., `fill` options).
- **Enhanced Options:** More granular control over document properties.
- **Initial Content:** Layers can now be added during document creation.

## When to use document creation

Use **Document Creation** when:

- Creating new blank documents from scratch.
- Building templates programmatically.
- Generating documents with specific dimensions.
- Starting fresh without an existing file.

Use **[Format Conversion](format-conversion-migration.md)** when:

- Converting existing PSDs to other formats.
- Exporting images without modifications.
- Generating thumbnails from existing files.

Use **[Document Operations](document-operations-migration.md)** when:

- Modifying existing documents (crop, resize, trim).
- Adjusting canvas size.
- Performing document-level transformations.

Use **[Composite Operations](composite-migration.md)** when:

- Working with existing documents and layers.
- Adding, removing, or modifying layers.
- Complex multi-layer compositions.

## Creating a basic blank document

**Key Points:**

- Document dimensions: `width`, `height` (pixels), `resolution`
- `fill`: Background type (e.g. `"transparent"`, `"white"`, `"black"`)
- `mode`: Color mode (e.g. `"rgb"`, `"cmyk"`, `"grayscale"`)
- `depth`: Bit depth (e.g. `"8"`, `"16"`, `"32"`)

**V2 Approach:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "transparent",
    "mode": "rgb",
    "depth": "8"
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

## Document parameters

| Required | Parameter | Details |
|----------|-----------|---------|
| Yes | `width` | Type: Integer. Range: 1–32000 pixels. Width of the document in pixels. |
| Yes | `height` | Type: Integer. Range: 1–32000 pixels. Height of the document in pixels. |
| Yes | `resolution` | Type: Integer. Range: 72–300 PPI. Document resolution in pixels per inch. Common values: 72 (web), 150 (draft print), 300 (high-quality print). |
| No | `fill` | Type: String. Default: `"white"`. Options: `"white"` (white background), `"background_color"` (uses background color, customizable), `"transparent"` (transparent background). Background fill for the document. |
| No | `mode` | Type: String. Default: `"rgb"`. Options: `"rgb"`, `"cmyk"`, `"gray"`, `"lab"`, `"hsb"`, `"duotone"`, `"opacity"`, `"book"`. Color mode for the document. |
| No | `depth` | Type: String. Default: `"8"`. Options: `"8"`, `"16"`, `"32"` (bits per channel). Bit depth per color channel. |

## Examples by use case

### Web graphics document

Create a document optimized for web graphics:

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "transparent",
    "mode": "rgb",
    "depth": "8"
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

### Print document

Create a high-resolution document for print:

```json
{
  "image": {
    "width": 2550,
    "height": 3300,
    "resolution": 300,
    "fill": "white",
    "mode": "cmyk",
    "depth": "8"
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

### Social media template

Create a square canvas for social media:

```json
{
  "image": {
    "width": 1080,
    "height": 1080,
    "resolution": 72,
    "fill": "white",
    "mode": "rgb",
    "depth": "8"
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

### Banner document

Create a wide banner document:

```json
{
  "image": {
    "width": 3000,
    "height": 600,
    "resolution": 72,
    "fill": "transparent",
    "mode": "rgb",
    "depth": "8"
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

## Creating with initial layers

You can create a document and add initial content layers in the same request:

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "white",
    "mode": "rgb",
    "depth": "8"
  },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Background Image",
        "image": {
          "source": {
            "url": "<IMAGE_URL>"
          }
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "bottom"
          }
        }
      },
      {
        "type": "text_layer",
        "name": "Title",
        "text": {
          "content": "Hello World",
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 72,
                "fontColor": {
                  "type": "rgb",
                  "red": 0,
                  "green": 0,
                  "blue": 0
                }
              }
            }
          ]
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

## Background fill options

### White background

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "white"
  }
}
```

### Transparent background

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "transparent"
  }
}
```

### Custom background color

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "background_color"
  }
}
```

<InlineAlert variant="info" slots="text"/>

When using `"background_color"`, the default Photoshop background color will be used. To use a specific color, add a solid color layer during document creation.

## Color modes explained

### RGB (Red, Green, Blue)

- **Best for:** Web graphics, digital displays, photography
- **Channels:** 3 color channels (Red, Green, Blue)
- **Use case:** Most common for digital work

```json
{
  "mode": "rgb"
}
```

### CMYK (Cyan, Magenta, Yellow, Black)

- **Best for:** Print production, commercial printing
- **Channels:** 4 color channels (Cyan, Magenta, Yellow, Black)
- **Use case:** Documents intended for physical printing

```json
{
  "mode": "cmyk"
}
```

### Grayscale

- **Best for:** Black and white images, print optimization
- **Channels:** 1 channel
- **Use case:** Monochrome artwork, black and white photography

```json
{
  "mode": "gray"
}
```

### Lab color

- **Best for:** Color correction, advanced color manipulation
- **Channels:** 3 channels (Lightness, a, b)
- **Use case:** Professional color grading

```json
{
  "mode": "lab"
}
```

## Bit depth explained

### 8-bit

- **File size:** Smallest
- **Color precision:** 256 levels per channel
- **Best for:** Web graphics, general use, final outputs
- **Use when:** File size matters, standard quality sufficient

```json
{
  "depth": "8"
}
```

### 16-bit

- **File size:** Medium
- **Color precision:** 65,536 levels per channel
- **Best for:** Photography, extensive editing workflows
- **Use when:** Need to preserve quality through multiple edits

```json
{
  "depth": "16"
}
```

### 32-bit

- **File size:** Largest
- **Color precision:** High Dynamic Range (HDR)
- **Best for:** HDR imaging, 3D rendering, scientific imaging
- **Use when:** Working with HDR content or extreme tonal ranges

```json
{
  "depth": "32"
}
```

## Multiple outputs

Create a document and immediately export it in multiple formats:

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": 72,
    "fill": "white",
    "mode": "rgb",
    "depth": "8"
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

## Common dimension templates

### Social media sizes

**Instagram Post (Square)**

```json
{ "width": 1080, "height": 1080 }
```

**Instagram Story**

```json
{ "width": 1080, "height": 1920 }
```

**Facebook Cover**

```json
{ "width": 820, "height": 312 }
```

**Twitter Header**

```json
{ "width": 1500, "height": 500 }
```

**LinkedIn Banner**

```json
{ "width": 1584, "height": 396 }
```

### Standard print sizes (at 300 DPI)

**4x6 inches**

```json
{ "width": 1200, "height": 1800, "resolution": 300 }
```

**5x7 inches**

```json
{ "width": 1500, "height": 2100, "resolution": 300 }
```

**8x10 inches**

```json
{ "width": 2400, "height": 3000, "resolution": 300 }
```

**8.5x11 inches (Letter)**

```json
{ "width": 2550, "height": 3300, "resolution": 300 }
```

### Web sizes

**Full HD**

```json
{ "width": 1920, "height": 1080, "resolution": 72 }
```

**4K/UHD**

```json
{ "width": 3840, "height": 2160, "resolution": 72 }
```

**Desktop Wallpaper (Wide)**

```json
{ "width": 2560, "height": 1440, "resolution": 72 }
```

## Common migration issues

### Resolution out of range

❌ **Problem:** Trying to set resolution outside the 72-300 range.

```json
{
  "resolution": 600
}
```

✅ **Solution:** Use value within 72-300 range.

```json
{
  "resolution": 300
}
```

### Invalid fill option

❌ **Problem:** Using invalid fill value.

```json
{
  "fill": "black"
}
```

✅ **Solution:** Use valid fill options.

```json
{
  "fill": "white" // or "transparent" or "background_color"
}
```

### Dimensions too large

❌ **Problem:** Dimensions exceed the maximum.

```json
{
  "width": 35000,
  "height": 35000
}
```

✅ **Solution:** Stay within 1-32000 pixel range.

```json
{
  "width": 32000,
  "height": 32000
}
```

## Next steps

- Review the [composite operations guide](composite-migration.md) for adding layers to your new document
- Check the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for output options
- Test your document creation with development endpoints

## Need help?

Contact the Adobe DI ART Service team for technical support with document creation operations.
