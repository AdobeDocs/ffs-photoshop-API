---
title: Output Types Migration (v1 to v2)
description: Migrate JPEG, PNG, PSD, and TIFF output configurations from V1 to V2 structural and quality/compression changes
hideBreadcrumbNav: true
keywords:
  - output types
  - JPEG
  - PNG
  - PSD
  - TIFF
  - quality
  - compression
  - migration
  - v1 to v2
---

# Output Types Migration Guide (v1 to v2)

## Overview

Adobe Photoshop API v2 introduces significant changes to output format specifications. This guide covers the structural changes, field renaming, and quality/compression parameter transformations for all output types: JPEG, PNG, PSD, and TIFF.

## Summary of changes

All output formats in v2 share common structural changes:

| Change | v1 | v2 |
|--------|----|----|
| **Location URL** | `outputs[].href` | `outputs[].destination.url` |
| **Format Type** | `outputs[].type` | `outputs[].mediaType` |
| **Storage Type** | `outputs[].storage` (required) | `outputs[].destination.storageType` (optional) |
| **Quality (JPEG)** | Numeric 1-7 (or 1-12) | String enum |
| **Compression (PNG)** | "small", "medium", "large" | Detailed string enum |

## Structural changes (all output types)

**Key structural changes:**

1. **Destination Object**: URLs are now nested in a `destination` object.
2. **Storage Type**:
   - v1: `storage` field required for all outputs.
   - v2: `storageType` only needed for Azure Blob Storage and Dropbox.
   - AWS S3 presigned URLs don't require `storageType`.
3. **Media Type**: Renamed from `type` to `mediaType` for clarity.

### V1 output structure

```json
{
  "outputs": [
    {
      "href": "https://example.com/output.jpg",
      "storage": "external",
      "type": "image/jpeg",
      "width": 1920,
      "quality": 7
    }
  ]
}
```

### V2 output structure

```json
{
  "outputs": [
    {
      "destination": {
        "url": "https://example.com/output.jpg"
      },
      "mediaType": "image/jpeg",
      "width": 1920,
      "quality": "maximum"
    }
  ]
}
```

### Common output fields

All output types support these common fields:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `mediaType` | string | Output format (e.g., "image/jpeg") | Yes |
| `destination` | object | Output destination configuration | Yes |
| `width` | integer | Output width in pixels (≥ 0) | No |
| `height` | integer | Output height in pixels (≥ 0) | No |
| `maxWidth` | integer | Maximum width in pixels (≥ 0) | No |
| `shouldTrimToCanvas` | boolean | Trim transparent pixels | No |

<HorizontalLine />

## JPEG output migration

### Quality parameter changes

The most significant change for JPEG outputs is the quality parameter transformation from numeric to descriptive string values.

### V1 JPEG quality (numeric)

```json
{
  "type": "image/jpeg",
  "quality": 7
}
```

In the v1 API, you can use numeric values:

- Range: 1-7 (some versions supported 1-12)
- Higher number = better quality
- Default: 7 (maximum quality)

### V2 JPEG quality (string enum)

```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum"
}
```

In the v2 API, you use descriptive string values:

- `"very_poor"` - Lowest quality, smallest file size
- `"poor"` - Poor quality
- `"low"` - Low quality
- `"medium"` - Balanced quality and file size
- `"high"` - High quality
- `"maximum"` - Maximum quality
- `"photoshop_max"` - Photoshop maximum quality (recommended default)

### JPEG quality mapping table

| v2 Quality | v1 Quality | Use Case |
|------------|------------|----------|
| `"very_poor"` | N/A | Smallest files (v2 only) |
| `"poor"` | N/A | Very small files (v2 only) |
| `"low"` | 1-2 | Thumbnails, small previews |
| `"medium"` | 3-4 | Standard web images |
| `"high"` | 5-6 | High-quality web images |
| `"maximum"` | 7 | Print, production |
| `"photoshop_max"` | N/A | Professional print, highest quality (recommended) |

The quality parameter is optional. If not specified, the API uses different defaults based on the operation type:

- **Create Composite** (`/v2/create-composite`): Default quality is `photoshop_max`
- **Generate Manifest** (`/v2/generate-manifest`): Default quality for layer thumbnails is `medium`

### Complete JPEG migration example

**Key Transformations:**

1. `inputs[].href` → `image.source.url`
2. `outputs[].href` → `outputs[].destination.url`
3. `outputs[].type` → `outputs[].mediaType`
4. `quality: 7` → `quality: "maximum"`
5. `storage: "external"` removed (implicit for S3 URLs)

**V1 Request:**

```json
{
  "inputs": [
    {
      "href": "https://my-bucket.s3.amazonaws.com/input.psd",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "https://my-bucket.s3.amazonaws.com/output.jpg",
      "storage": "external",
      "type": "image/jpeg",
      "quality": 7,
      "width": 2000
    }
  ]
}
```

**V2 Request:**

```json
{
  "image": {
    "source": {
      "url": "https://my-bucket.s3.amazonaws.com/input.psd"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "https://my-bucket.s3.amazonaws.com/output.jpg"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2000
    }
  ]
}
```

<HorizontalLine />

## PNG output migration

### Compression parameter changes

PNG outputs have expanded compression options in V2, offering more granular control over file size and compression speed.

### V1 PNG compression

```json
{
  "type": "image/png",
  "compression": "medium"
}
```

In the v1 API, you can use three compression levels:

- `"small"` - High compression (smaller files)
- `"medium"` - Balanced compression
- `"large"` - Low compression (larger files)

### V2 PNG compression

```json
{
  "mediaType": "image/png",
  "compression": "medium"
}
```

In the v2 API, you can use ten compression levels (following zlib/libpng standards):

- `"none"` - No compression (level 0)
- `"very_low"` - Minimal compression (level 1)
- `"low"` - Low compression (level 2)
- `"medium_low"` - Medium-low compression (level 3)
- `"medium"` - Medium compression (level 4)
- `"medium_high"` - Medium-high compression (level 5)
- `"default"` - Default compression (level 6, library standard)
- `"high"` - High compression (level 7)
- `"very_high"` - Very high compression (level 8)
- `"maximum"` - Maximum compression (level 9)

### PNG compression mapping table

| v1 Compression | v2 Recommended | v2 Alternatives | Notes |
|---------------|----------------|-----------------|-------|
| `"small"` | `"maximum"` | `"very_high"`, `"high"` | Smallest file size, slower |
| `"medium"` | `"medium"` | `"default"`, `"medium_high"`, `"medium_low"` | Balanced performance |
| `"large"` | `"low"` | `"very_low"`, `"none"` | Fastest, larger files |

The compression parameter is optional. If not specified, the API uses `default` (level 6) for both Create Composite and Generate Manifest operations, which provides a good balance between file size and processing speed.

### Complete PNG migration example

**Key Transformations:**

1. `inputs[].href` → `image.source.url`
2. `outputs[].href` → `outputs[].destination.url`
3. `outputs[].type` → `outputs[].mediaType`
4. `compression: "medium"` stays the same (but more options available)
5. `storage` field removed

**V1 Request:**

```json
{
  "inputs": [
    {
      "href": "https://my-storage.com/input.psd",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "https://my-storage.com/output.png",
      "storage": "external",
      "type": "image/png",
      "compression": "medium",
      "width": 1920
    }
  ]
}
```

**V2 Request:**

```json
{
  "image": {
    "source": {
      "url": "https://my-storage.com/input.psd"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "https://my-storage.com/output.png"
      },
      "mediaType": "image/png",
      "compression": "medium",
      "width": 1920
    }
  ]
}
```

## PSD output migration

### PSD format changes

Photoshop document (PSD) outputs have no format-specific parameters, like quality or compression. The only changes are the structural field renaming.

### V1 PSD output

```json
{
  "type": "image/vnd.adobe.photoshop",
  "href": "https://example.com/output.psd",
  "storage": "external"
}
```

### V2 PSD output

```json
{
  "mediaType": "image/vnd.adobe.photoshop",
  "destination": {
    "url": "https://example.com/output.psd"
  }
}
```

### Supported media types for PSD

V2 accepts both media type formats:

- `"image/vnd.adobe.photoshop"` (recommended)
- `"vnd.adobe.photoshop"` (legacy support)

### Complete PSD migration example

**Key Transformations:**

1. Field renaming (same as other formats)
2. `options` → `edits`
3. No quality or compression parameters needed

**V1 Request:**

```json
{
  "inputs": [
    {
      "href": "https://storage.example.com/document.psd",
      "storage": "external"
    }
  ],
  "options": {
    "layers": [
      {
        "name": "Background",
        "locked": false
      }
    ]
  },
  "outputs": [
    {
      "href": "https://storage.example.com/modified.psd",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}
```

**V2 Request:**

```json
{
  "image": {
    "source": {
      "url": "https://storage.example.com/document.psd"
    }
  },
  "edits": {
    "layers": [
      {
        "name": "Background",
        "locked": false
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "https://storage.example.com/modified.psd"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

## TIFF output migration

### TIFF format changes

TIFF outputs in the v2 API do not have compression options. Like PSD, the changes are purely structural.

### V1 TIFF output

```json
{
  "type": "image/tiff",
  "href": "https://example.com/output.tiff",
  "storage": "external"
}
```

### V2 TIFF output

```json
{
  "mediaType": "image/tiff",
  "destination": {
    "url": "https://example.com/output.tiff"
  }
}
```

### Complete TIFF migration example

**Key Transformations:**

1. Standard field renaming
2. No compression parameters in v2
3. Common output fields still supported (width, height, etc.)

**V1 Request:**

```json
{
  "inputs": [
    {
      "href": "https://storage.example.com/input.psd",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "https://storage.example.com/output.tiff",
      "storage": "external",
      "type": "image/tiff",
      "width": 3000
    }
  ]
}
```

**V2 Request:**

```json
{
  "image": {
    "source": {
      "url": "https://storage.example.com/input.psd"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "https://storage.example.com/output.tiff"
      },
      "mediaType": "image/tiff",
      "width": 3000
    }
  ]
}
```

## Multiple outputs

V2 supports generating multiple outputs in different formats from a single request (up to 25 outputs).

### Multiple output example

**V2 Request:**

```json
{
  "image": {
    "source": {
      "url": "https://storage.example.com/input.psd"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "https://storage.example.com/output-hq.jpg"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 2400
    },
    {
      "destination": {
        "url": "https://storage.example.com/output-preview.jpg"
      },
      "mediaType": "image/jpeg",
      "quality": "medium",
      "width": 800
    },
    {
      "destination": {
        "url": "https://storage.example.com/output.png"
      },
      "mediaType": "image/png",
      "compression": "maximum",
      "width": 1920
    },
    {
      "destination": {
        "url": "https://storage.example.com/output.psd"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

This generates four outputs in a single API call:

1. High-quality JPEG at 2400px width
2. Medium-quality preview JPEG at 800px width
3. PNG with maximum compression at 1920px width
4. Original PSD with any edits applied

## Storage type considerations

### When to use `storageType`

In v2, the `storageType` field is optional and only required for specific storage providers:

| Storage Provider | storageType Required | Value |
|-----------------|---------------------|-------|
| AWS S3 (presigned URLs) | ❌ No | Not needed |
| Azure Blob Storage | ✅ Yes | `"azure"` |
| Dropbox | ✅ Yes | `"dropbox"` |
| Frame.io | ❌ No | Not needed |
| Google Drive | ❌ No | Not needed |

### Azure Blob Storage example

```json
{
  "destination": {
    "url": "https://myaccount.blob.core.windows.net/container/output.jpg",
    "storageType": "azure"
  },
  "mediaType": "image/jpeg",
  "quality": "high"
}
```

### Dropbox example

```json
{
  "destination": {
    "url": "https://dropbox.com/path/to/output.jpg",
    "storageType": "dropbox"
  },
  "mediaType": "image/jpeg",
  "quality": "high"
}
```

## Common migration errors

### Using V1 field names

❌ **Problem:**

```json
{
  "outputs": [{
    "href": "https://...",
    "type": "image/jpeg"
  }]
}
```

❌ **Error:**

```text
Required field 'destination' is missing
Required field 'mediaType' is missing
```

✅ **Solution:**

```json
{
  "outputs": [{
    "destination": {
      "url": "https://..."
    },
    "mediaType": "image/jpeg"
  }]
}
```

### Numeric JPEG quality

❌ **Problem:**

```json
{
  "mediaType": "image/jpeg",
  "quality": 7
}
```

❌ **Error:**

```text
Invalid value '7' at path 'outputs[0].quality'.
Accepted values are: very_poor, poor, low, medium, high, maximum, photoshop_max
```

✅ **Solution:**

```json
{
  "mediaType": "image/jpeg",
  "quality": "maximum"
}
```

### Invalid PNG compression

❌ **Problem:**

```json
{
  "mediaType": "image/png",
  "compression": "small"
}
```

❌ **Error:**

```txt
Invalid value 'small' at path 'outputs[0].compression'.
```

✅ **Solution:**

Use V2 compression values:

```json
{
  "mediaType": "image/png",
  "compression": "maximum"
}
```

### Using JPEG quality for PNG

❌ **Problem:**

```json
{
  "mediaType": "image/png",
  "quality": "high"
}
```

❌ **Error:**

```txt
'quality' parameter is not supported for PNG format
```

✅ **Solution:**

Use `compression` for PNG:

```json
{
  "mediaType": "image/png",
  "compression": "high"
}
```

### Missing storage type for Azure

❌ **Problem:**

```json
{
  "destination": {
    "url": "https://myaccount.blob.core.windows.net/..."
  }
}
```

❌ **Error:**

```txt
Azure Blob Storage URL requires 'storageType': 'azure'
```

✅ **Solution:**

```json
{
  "destination": {
    "url": "https://myaccount.blob.core.windows.net/...",
    "storageType": "azure"
  }
}
```

## Migration checklist

Use this checklist when migrating output configurations:

### All Output Types

- [ ] Replace `outputs[].href` with `outputs[].destination.url`
- [ ] Replace `outputs[].type` with `outputs[].mediaType`
- [ ] Remove `storage: "external"` for AWS S3 presigned URLs
- [ ] Add `storageType` for Azure Blob Storage or Dropbox if applicable
- [ ] Verify common fields (`width`, `height`, `maxWidth`) if used

### JPEG specific

- [ ] Convert numeric `quality` values to string enums
- [ ] Map V1 quality values using the mapping table
- [ ] Quality is optional; defaults to `photoshop_max` for create-composite, `medium` for manifest thumbnails

### PNG specific

- [ ] Update `compression` values to V2 enum
- [ ] Map V1 compression values using the mapping table
- [ ] Compression is optional; defaults to `default` (level 6)
- [ ] Ensure using `compression` not `quality`

### PSD specific

- [ ] Use `"image/vnd.adobe.photoshop"` for `mediaType`
- [ ] No quality or compression parameters needed

### TIFF specific

- [ ] Use `"image/tiff"` for `mediaType`
- [ ] No compression parameters in V2

## Quick reference

### Field name changes (all formats)

| v1 Field | v2 Field | Notes |
|----------|----------|-------|
| `outputs[].href` | `outputs[].destination.url` | Nested in destination object |
| `outputs[].type` | `outputs[].mediaType` | Renamed for clarity |
| `outputs[].storage` | `outputs[].destination.storageType` | Optional in V2 |

### JPEG quality quick reference

| v1 | v2 | When to Use |
|----|----|----|
| 7 | `"maximum"` | Default for production |
| 5-6 | `"high"` | High-quality web |
| 3-4 | `"medium"` | Standard web |
| 1-2 | `"low"` | Thumbnails |

### PNG compression quick reference

| v1 | v2 | When to Use |
|----|----|----|
| `"small"` | `"maximum"` | Smallest files |
| `"medium"` | `"medium"` | Balanced |
| `"large"` | `"low"` | Fastest processing |

## Additional resources

- [V2 API Documentation](https://developer.adobe.com/photoshop/api/v2/)
- [Execute Actions Endpoint](actions-migration.md)
- [Status Endpoint](status-migration.md)

**Related migration guides:**

- [Migration Overview](index.md) - Complete V1 to V2 migration overview
- [Format Conversion Migration](format-conversion-migration.md) - Converting between formats
- [Actions Migration](actions-migration.md) - Executing Photoshop actions
- [Storage Solutions](../../../getting-started/storage-solutions/index.md) - Detailed storage configuration
