---
title: Manifest Migration (V1 to V2)
description: Migrate from /pie/psdService/documentManifest to /v2/generate-manifest
hideBreadcrumbNav: true
keywords:
  - manifest
  - document manifest
  - PSD manifest
  - migration
  - v1 to v2
---

# Manifest Migration (V1 to V2)

This guide helps you migrate from the v1 document manifest endpoint to `/v2/generate-manifest`.

## Overview

The manifest generation endpoint extracts detailed information about a PSD document, including:

- Document dimensions and properties
- Layer hierarchy and structure
- Layer properties and bounds
- Optional layer thumbnails
- XMP metadata

**V1 Endpoint:**

- `/pie/psdService/documentManifest`

**V2 Endpoint:**

- `/v2/generate-manifest`

## Basic migration example

<InlineAlert variant="warning" slots="text"/>

Both V1 and V2 require explicit opt-in for layer thumbnail generation:

- **V1**: Include `options.thumbnails` object with a `type` property
- **V2**: Set `includeLayerThumbnails: true` and optionally specify format in `exportOptions`

**Key differences**

**Input Structure:**

- V1: `inputs[].href` → V2: `image.source.url`
- V1: `inputs[].storage` → V2: Storage specified in outputs

**Options:**

- V1: `options.thumbnails` (object with `type` property) → V2: `includeLayerThumbnails` (boolean) + `exportOptions.mediaType`
- V1: Thumbnail format in `options.thumbnails.type` → V2: Format in `exportOptions.mediaType`
- V1: Layer information always included → V2: Layer information always included
- New in V2: `includeXmp`, `maximumThumbnailDepth`, `trimToTransparency`
- Both versions require explicit opt-in for thumbnail generation

**Output Structure:**

- V1: Manifest returned in response → V2: Manifest written to destination specified in `outputs`

### V1 approach

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentManifest \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "external"
    }
  ],
  "options": {
    "thumbnails": {
      "type": "image/jpeg"
    }
  }
}'
```

### V2 approach

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/generate-manifest \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "includeLayerThumbnails": true,
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_OUTPUT_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}'
```

## Configuration options

### Thumbnail format migration

**V1 Thumbnail Formats:**

V1 supported three thumbnail formats via `options.thumbnails.type`:

- `image/jpeg`
- `image/png`
- `image/tiff`

**V2 Equivalent:**

In V2, specify the format in `exportOptions.mediaType`:

```json
{
  "includeLayerThumbnails": true,
  "exportOptions": {
    "mediaType": "image/jpeg",
    "quality": "high"
  }
}
```

or for PNG:

```json
{
  "includeLayerThumbnails": true,
  "exportOptions": {
    "mediaType": "image/png",
    "compression": "medium"
  }
}
```

### Include layer thumbnails

Generate thumbnail images for all layers:

```json
{
  "includeLayerThumbnails": true
}
```

Default: `false`

**Note:** Both V1 and V2 require explicit opt-in for thumbnail generation. In V1, you included an `options.thumbnails` object with a `type` property. In V2, you set `includeLayerThumbnails: true`.

### Maximum thumbnail depth

Control how deep to generate thumbnails in the layer hierarchy:

```json
{
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 3
}
```

- `0`: No depth limit (generate for all layers)
- `> 0`: Generate thumbnails only up to specified depth
- Default: All layers

### Include XMP metadata

Include XMP metadata in the manifest:

```json
{
  "includeXmp": true
}
```

Default: `false`

### Trim to transparency

Trim layer thumbnails to remove transparent pixels:

```json
{
  "trimToTransparency": true
}
```

Default: `false`

### Export options

Control thumbnail export quality:

```json
{
  "exportOptions": {
    "mediaType": "image/jpeg",
    "quality": "high"
  }
}
```

or

```json
{
  "exportOptions": {
    "mediaType": "image/png",
    "compression": "medium"
  }
}
```

## Output options

### External storage

```json
{
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Hosted storage

```json
{
  "outputs": [
    {
      "destination": {
        "validityPeriod": 3600
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Embedded storage

```json
{
  "outputs": [
    {
      "destination": {
        "embedded": "json"
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Creative Cloud storage

```json
{
  "outputs": [
    {
      "destination": {
        "creativeCloudPath": "/path/to/manifest.json"
      },
      "mediaType": "application/json"
    }
  ]
}
```

## Complete example with all options

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/generate-manifest \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 5,
  "includeXmp": true,
  "trimToTransparency": true,
  "exportOptions": {
    "mediaType": "image/jpeg",
    "quality": "high"
  },
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_OUTPUT_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}'
```

## Manifest structure

The generated manifest contains comprehensive document information:

```json
{
  "document": {
    "name": "example.psd",
    "width": 1920,
    "height": 1080,
    "depth": 8,
    "mode": "rgb",
    "photoshopBuild": "...",
    "imageInfo": {
      "format": "image/vnd.adobe.photoshop"
    }
  },
  "layers": [
    {
      "id": 1,
      "name": "Background",
      "type": "layer",
      "visible": true,
      "locked": false,
      "bounds": {
        "top": 0,
        "left": 0,
        "width": 1920,
        "height": 1080
      },
      "thumbnail": {
        "href": "<THUMBNAIL_URL>"
      }
    },
    {
      "id": 2,
      "name": "Text Layer",
      "type": "textLayer",
      "visible": true,
      "text": {
        "content": "Hello World",
        "characterStyles": [...]
      }
    },
    {
      "id": 3,
      "name": "Group",
      "type": "groupLayer",
      "visible": true,
      "children": [...]
    }
  ],
  "xmp": "...",
  "artboards": [...]
}
```

## Pixel mask details in manifest response

When a layer has a pixel mask, the manifest includes mask information in multiple locations with distinct purposes. Understanding these differences is crucial for migration and proper handling of mask data.

### V1 vs V2 Pixel Mask Structure Changes

**Important:** V2 introduces a new, unified structure for pixel mask information that differs significantly from V1.

**V1 Behavior:**

- Manifest responses included a `mask` property at the layer level
- Mask properties: `enabled`, `linked`, `offset` (with `x`, `y` coordinates)
- No separate metadata about mask existence or bounds
- Internal storage used `layerSettings.imageMask` for setting mask properties in edit operations

**V2 Behavior:**

- Pixel mask properties are now in a dedicated `pixelMask` property at the layer level
- Additional metadata properties: `hasMask`, `extendOpaque`, `bounds`
- Editable properties: `enabled`, `linked`, `offset` (can be modified in edit operations)
- Offset uses `horizontal`/`vertical` instead of `x`/`y`
- Common mask properties (density, feather) separated into `userMask` property
- Provides unified structure across both manifest responses and edit operations

**Migration Note:** Clients migrating from V1 should update their code to:

1. Look for `pixelMask` instead of `mask` for pixel mask properties
2. Access offset using `offset.horizontal` and `offset.vertical` instead of `offset.x` and `offset.y`
3. Check `pixelMask.hasMask` to determine if mask pixel data exists
4. Check `layerSettings.clippingMask` to determine if a layer is clipped
5. Read density and feather from the separate `userMask` property

### Mask-related fields overview

The manifest response includes two mask-related structures:

1. **`userMask`** - Common mask properties applicable for both pixel and vector masks (density, feather)
2. **`pixelMask`** - Unified pixel mask structure containing both metadata and editable properties

### Complete layer with pixel mask example

```json
{
  "id": 5,
  "name": "Layer with Mask",
  "type": "layer",
  "visible": true,
  "locked": false,
  "bounds": {
    "top": 100,
    "left": 100,
    "width": 500,
    "height": 400
  },
  "layerSettings": {
    "clippingMask": true
  },
  "userMask": {
    "density": 100,
    "feather": 0
  },
  "pixelMask": {
    "hasMask": true,
    "extendOpaque": false,
    "bounds": {
      "top": 100,
      "left": 100,
      "width": 500,
      "height": 400
    },
    "enabled": true,
    "linked": true,
    "offset": {
      "horizontal": 0,
      "vertical": 0
    }
  }
}
```

### Field descriptions and client migration guide

#### Common Layer Properties

| Property | Type | Location | Description |
| -------- | ---- | -------- | ----------- |
| `clippingMask` | Boolean | `layerSettings.clippingMask` | Indicates whether the layer is clipped to the layer below it.

**Note:** To set this property in edit operations, use the `isClipped` field at the layer config level (e.g., `layers[].isClipped: true`).

#### 1. userMask - Common Mask Properties

Contains properties that apply to both vector and pixel masks:

| Property | Type | Description |
| -------- | ---- | ----------- |
| `density` | Integer | Mask opacity (0-100). Controls overall mask strength |
| `feather` | Number | Edge softness in pixels (0-250). Blurs the mask edges |

#### 2. pixelMask - Unified Pixel Mask Structure

Contains all pixel mask information in a single, unified structure combining both metadata and editable properties:

**Metadata Properties (read-only):**

| Property | Type | Description |
| -------- | ---- | ----------- |
| `hasMask` | Boolean | Whether mask pixel data exists |
| `extendOpaque` | Boolean | How out-of-bounds areas are treated (`true` = opaque outside bounds, `false` = transparent) |
| `bounds` | Object | Spatial extent of the mask data (top, left, right, bottom) |

**Editable Properties:**

| Property | Type | Description | Default |
| -------- | ---- | ----------- | ------- |
| `enabled` | Boolean | Toggle mask visibility without deleting data | `true` |
| `linked` | Boolean | Whether mask transforms with the layer | `true` |
| `offset` | Object | Independent position relative to layer origin | `{horizontal: 0, vertical: 0}` |

**Note:** The editable properties (`enabled`, `linked`, `offset`) can be used in both `create-composite` edit operations and are returned in manifest responses. This provides a consistent structure across all API operations.

## Accessing the manifest

### With embedded storage

When using embedded storage, the manifest is returned directly in the job status response:

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

Response:

```json
{
  "jobId": "...",
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "destination": {
          "embedded": "json",
          "content": {
            "document": {...},
            "layers": [...]
          }
        },
        "mediaType": "application/json"
      }
    ]
  }
}
```

### With external/hosted storage

When using external or hosted storage, download the manifest from the provided URL:

```shell
# Get job status
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"

# Response includes output URL
{
  "jobId": "...",
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "url": "<MANIFEST_URL>"
      }
    ]
  }
}

# Download manifest
curl -X GET "<MANIFEST_URL>" -o manifest.json
```

## Use cases

### Document analysis

Extract document structure for analysis:

```json
{
  "image": {
    "source": {
      "url": "<PSD_URL>"
    }
  },
  "includeLayerThumbnails": false,
  "includeXmp": false,
  "outputs": [
    {
      "destination": {
        "embedded": "json"
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Layer preview generation

Generate thumbnails for all layers:

```json
{
  "image": {
    "source": {
      "url": "<PSD_URL>"
    }
  },
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 0,
  "trimToTransparency": true,
  "exportOptions": {
    "mediaType": "image/png",
    "compression": "medium"
  },
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Metadata extraction

Extract XMP metadata:

```json
{
  "image": {
    "source": {
      "url": "<PSD_URL>"
    }
  },
  "includeLayerThumbnails": false,
  "includeXmp": true,
  "outputs": [
    {
      "destination": {
        "embedded": "json"
      },
      "mediaType": "application/json"
    }
  ]
}
```

## Status checking

Check the status of your manifest generation job:

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/{jobId} \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

See the [status migration guide](status-migration.md) for details on the response format.

## Common migration issues

### Issue: Thumbnail syntax change

**Problem:** Need to update thumbnail generation syntax from V1 to V2

**Solution:** Both versions require explicit opt-in, but use different syntax:

```json
{
  "includeLayerThumbnails": true
}
```

**V1 Behavior:**

```json
{
  "options": {
    "thumbnails": {
      "type": "image/jpeg"
    }
  }
}
```

**V2 Equivalent:**

```json
{
  "includeLayerThumbnails": true,
  "exportOptions": {
    "mediaType": "image/jpeg"
  }
}
```

### Issue: Missing outputs array

**Problem:** Not specifying outputs in v2

**Solution:** Always include outputs array

```json
{
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}
```

### Issue: Incorrect media type

**Problem:** Using wrong media type

**Solution:** Use `application/json` for manifest output

```json
{
  "mediaType": "application/json"
}
```

### Issue: Expecting manifest in response

**Problem:** Looking for manifest in initial response

**Solution:** Check job status for manifest URL or embedded data

```shell
# Step 1: Submit job
curl -X POST https://photoshop-api.adobe.io/v2/generate-manifest ...

# Step 2: Poll status
curl -X GET https://photoshop-api.adobe.io/v2/status/{jobId} ...
```

## Performance considerations

**Thumbnail Generation:**

- Generating thumbnails for all layers can be time-consuming for complex documents
- Use `maximumThumbnailDepth` to limit generation depth
- Consider disabling thumbnails if only document structure is needed

**XMP Metadata:**

- XMP extraction adds minimal overhead
- Include only when metadata is needed

**Output Storage:**

- Use embedded storage for immediate access to small manifests
- Use hosted storage to avoid managing your own storage
- Use external storage for integration with existing workflows

## Next steps

- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for output storage options
- Check the [status migration guide](status-migration.md) for polling patterns
- Test manifest generation with development endpoints

## Need help?

Contact the Adobe DI ART Service team for technical support with manifest generation.
