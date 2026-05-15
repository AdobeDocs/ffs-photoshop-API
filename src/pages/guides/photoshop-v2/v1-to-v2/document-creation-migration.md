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
- **Initial Content:** Can add layers during document creation (creating a new document with a group layer is not yet supported — upcoming feature; to add layers inside a group, use create-composite on an existing document with placement `type: "into"` and `referenceLayer`).

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

**Key points:**

- Document dimensions: `width`, `height` (pixels), `resolution` (object with `unit` and `value`)
- `fill`: Background type (e.g. `"transparent"`, `"white"`, `"background_color"`) or object for custom RGB
- `mode`: Color mode (e.g. `"rgb"`, `"cmyk"`, `"grayscale"`)
- `depth`: Bit depth as integer (e.g. `8`, `16`, `32`)

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
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "transparent",
    "mode": "rgb",
    "depth": 8
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

### Required parameters

**`width`**

- Type: Integer
- Range: 1-32000 pixels
- Description: Width of the document in pixels

**`height`**

- Type: Integer
- Range: 1-32000 pixels
- Description: Height of the document in pixels

**`resolution`**

- Type: Object with `unit` and `value` properties
- Format: `{"unit": "density_unit", "value": N}` where N must be at least 1 (value >= 1)
- Description: Document resolution in pixels per inch (PPI)
- Common values: 72 (web), 150 (draft print), 300 (high-quality print)
- Example: `{"unit": "density_unit", "value": 72}`

### Optional parameters

**`fill`**

- Type: String or Object
- Default: `"white"`
- String options:
  - `"white"` - White background
  - `"background_color"` - Uses background color (customizable)
  - `"transparent"` - Transparent background
- Object form (for custom colors): `{"solidColor": {"rgb": {"red": R, "green": G, "blue": B}}}`
- Description: Background fill for the document

<InlineAlert variant="warning" slots="header,text"/>

The `fill` field changed between V1 and V2

Two breaking differences: (1) `"backgroundColor"` was renamed to `"background_color"` — the V1 string enum `"backgroundColor"` is invalid in V2. Use `"background_color"` (with underscore). (2) Custom solid colors require the object form in V2 — V1 only supported the three string shortcuts, V2 adds `{"solidColor": {"rgb": {"red": R, "green": G, "blue": B}}}` for arbitrary custom colors.

**`mode`**

- Type: String
- Default: `"rgb"`
- Options: `"rgb"`, `"bitmap"`, `"grayscale"`, `"indexed"`, `"hsb"`, `"cmyk"`, `"lab"`, `"duotone"`, `"multichannel"`
- Description: Color mode for the document. Supported depths vary by mode (see table below).

**`depth`**

- Type: Integer
- Default: `8` (when omitted)
- Values: `1`, `8`, `16`, or `32` (bit depth per channel). Valid combinations depend on `mode`:
  - **bitmap:** `1` only
  - **grayscale, rgb, hsb:** 8, 16, or 32
  - **cmyk, lab, multichannel:** 8 or 16
  - **indexed, duotone:** 8 only

| mode         | Supported depths |
|--------------|------------------|
| bitmap       | 1                |
| grayscale    | 8, 16, 32        |
| rgb          | 8, 16, 32        |
| hsb          | 8, 16, 32        |
| cmyk         | 8, 16            |
| lab          | 8, 16            |
| multichannel | 8, 16            |
| indexed      | 8 only           |
| duotone      | 8 only           |

**`pixelScaleFactor`**

- Type: Number (Double)
- Default: `1` when omitted
- Range: Must be positive, minimum 0.1
- Description: Pixel scale factor for the image (e.g., for high-DPI/Retina scaling)

**`iccProfile`**

- Type: Object (`standard` or `custom`)
- Default: None (optional)
- Description: ICC profile for color management applied at document creation time. Both standard named profiles and custom `.icc` files are supported.

  **Standard profile:** `{"type": "standard", "name": "<profile_name>"}` where `name` is one of: Adobe RGB (1998), Apple RGB, ColorMatch RGB, sRGB IEC61966-2.1, Dot Gain 10%/15%/20%/25%/30%, Gray Gamma 1.8, Gray Gamma 2.2

  **Custom profile:** `{"type": "custom", "name": "<descriptive_name>", "source": {"url": "<icc_file_url>"}}` — provide a URL to your `.icc` or `.icm` file. Supports `imageMode: "rgb"`, `"grayscale"`, or `"cmyk"`.

**`name`**

- Type: String
- Max length: 255 characters
- Description: Optional document name/title

## Examples by use case

### Web graphics document

Create a document optimized for web graphics:

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "transparent",
    "mode": "rgb",
    "depth": 8
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
    "resolution": {"unit": "density_unit", "value": 300},
    "fill": "white",
    "mode": "cmyk",
    "depth": 8
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
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "white",
    "mode": "rgb",
    "depth": 8
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
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "transparent",
    "mode": "rgb",
    "depth": 8
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

### Document with custom ICC profile

Create a document with a custom `.icc` profile for specialized color workflows:

```json
{
  "image": {
    "width": 2550,
    "height": 3300,
    "resolution": {"unit": "density_unit", "value": 300},
    "fill": "white",
    "mode": "rgb",
    "depth": 8,
    "iccProfile": {
      "type": "custom",
      "name": "DCI P3 D65",
      "source": {
        "url": "<PRESIGNED_URL_TO_ICC_FILE>"
      },
      "imageMode": "rgb"
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
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "white",
    "mode": "rgb",
    "depth": 8
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
    "resolution": {"unit": "density_unit", "value": 72},
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
    "resolution": {"unit": "density_unit", "value": 72},
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
    "resolution": {"unit": "density_unit", "value": 72},
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
- **Supported depths:** 8, 16, or 32

```json
{
  "mode": "rgb"
}
```

### CMYK (Cyan, Magenta, Yellow, Black)

- **Best for:** Print production, commercial printing
- **Channels:** 4 color channels (Cyan, Magenta, Yellow, Black)
- **Use case:** Documents intended for physical printing
- **Supported depths:** 8 or 16

```json
{
  "mode": "cmyk"
}
```

### Grayscale

- **Best for:** Black and white images, print optimization
- **Channels:** 1 channel
- **Use case:** Monochrome artwork, black and white photography
- **Supported depths:** 8, 16, or 32

```json
{
  "mode": "grayscale"
}
```

### Lab color

- **Best for:** Color correction, advanced color manipulation
- **Channels:** 3 channels (Lightness, a, b)
- **Use case:** Professional color grading
- **Supported depths:** 8 or 16

```json
{
  "mode": "lab"
}
```

## Bit depth explained

`depth` is an integer. Valid values depend on `mode` (see the mode/depth table above).

### 1-bit

- **File size:** Smallest possible
- **Color precision:** Binary (black or white only)
- **Best for:** Bitmap mode documents (line art, black and white scans)
- **Supported modes:** bitmap only

```json
{
  "mode": "bitmap",
  "depth": 1
}
```

### 8-bit

- **File size:** Smallest (for non-bitmap)
- **Color precision:** 256 levels per channel
- **Best for:** Web graphics, general use, final outputs
- **Supported modes:** All except bitmap

```json
{
  "depth": 8
}
```

### 16-bit

- **File size:** Medium
- **Color precision:** 65,536 levels per channel
- **Best for:** Photography, extensive editing workflows
- **Supported modes:** grayscale, rgb, hsb, cmyk, lab, multichannel

```json
{
  "depth": 16
}
```

### 32-bit

- **File size:** Largest
- **Color precision:** High Dynamic Range (HDR)
- **Best for:** HDR imaging, 3D rendering, scientific imaging
- **Supported modes:** grayscale, rgb, hsb only (not cmyk, lab, indexed, duotone, multichannel)

```json
{
  "depth": 32
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
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": "white",
    "mode": "rgb",
    "depth": 8
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
{ "width": 1200, "height": 1800, "resolution": {"unit": "density_unit", "value": 300} }
```

**5x7 inches**

```json
{ "width": 1500, "height": 2100, "resolution": {"unit": "density_unit", "value": 300} }
```

**8x10 inches**

```json
{ "width": 2400, "height": 3000, "resolution": {"unit": "density_unit", "value": 300} }
```

**8.5x11 inches (Letter)**

```json
{ "width": 2550, "height": 3300, "resolution": {"unit": "density_unit", "value": 300} }
```

### Web sizes

**Full HD**

```json
{ "width": 1920, "height": 1080, "resolution": {"unit": "density_unit", "value": 72} }
```

**4K/UHD**

```json
{ "width": 3840, "height": 2160, "resolution": {"unit": "density_unit", "value": 72} }
```

**Desktop Wallpaper (Wide)**

```json
{ "width": 2560, "height": 1440, "resolution": {"unit": "density_unit", "value": 72} }
```

## Common migration issues

### Resolution format

**Problem:** Using plain integer for resolution (invalid format in V2).

```json
{
  "resolution": 72
}
```

**Solution:** Use object format with `unit` and `value`.

```json
{
  "resolution": {"unit": "density_unit", "value": 72}
}
```

### Resolution value too low

**Problem:** Using resolution value less than 1.

```json
{
  "resolution": {"unit": "density_unit", "value": 0}
}
```

**Solution:** Use value >= 1.

```json
{
  "resolution": {"unit": "density_unit", "value": 1}
}
```

### Invalid pixelScaleFactor

**Problem:** Using zero or negative pixelScaleFactor.

```json
{
  "pixelScaleFactor": 0
}
```

**Solution:** Use positive value, minimum 0.1.

```json
{
  "pixelScaleFactor": 1.0
}
```

### Invalid color mode (gray vs grayscale)

**Problem:** Using deprecated or invalid `mode` value.

```json
{
  "mode": "gray"
}
```

**Solution:** Use `"grayscale"` (not `"gray"`). Supported values: `rgb`, `bitmap`, `grayscale`, `indexed`, `hsb`, `cmyk`, `lab`, `duotone`, `multichannel`.

```json
{
  "mode": "grayscale"
}
```

### Invalid depth for color mode

**Problem:** Depth not supported for the selected mode (e.g., 32-bit for CMYK).

```json
{
  "mode": "cmyk",
  "depth": 32
}
```

**Solution:** Use a valid depth for the mode. For bitmap, use `1`. For cmyk/lab use 8 or 16. For indexed/duotone use 8 only. For rgb/grayscale/hsb use 8, 16, or 32.

```json
{
  "mode": "cmyk",
  "depth": 16
}
```

### Invalid fill option

**Problem:** Using invalid fill value.

```json
{
  "fill": "black"
}
```

**Solution:** Use valid fill options: `"white"`, `"transparent"`, `"background_color"`, or the object form `{"solidColor": {"rgb": {"red": R, "green": G, "blue": B}}}`.

```json
{
  "fill": "white"
}
```

### Dimensions too large

**Problem:** Dimensions exceed the maximum.

```json
{
  "width": 35000,
  "height": 35000
}
```

**Solution:** Stay within 1-32000 pixel range.

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
