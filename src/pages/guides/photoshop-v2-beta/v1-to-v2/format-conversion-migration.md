---
title: Format Conversion Migration (V1 to V2)
description: Migrate from /pie/psdService/renditionCreate to /v2/create-composite for format conversion and export operations
hideBreadcrumbNav: true
keywords:
  - renditionCreate
  - format conversion
  - export
  - PSD
  - JPEG
  - PNG
  - Cloud PSD
  - PSDC
  - CPSD
  - sensei
  - sensei engine
  - migration
  - v1 to v2
---

# Format Conversion Migration (V1 to V2)

This guide helps you migrate from the v1 `/pie/psdService/renditionCreate` endpoint to the v2 `/create-composite` endpoint for format conversion and export operations.

## Overview

In v1, the `/renditionCreate` endpoint was primarily used for **converting and exporting PSD files to other formats** such as JPEG, PNG, or Cloud PSD. This was a rendering/export operation, not for layer manipulation or document editing.

**V1 Endpoint:**

```text
POST /pie/psdService/renditionCreate
```

**V2 Endpoint:**

```text
POST /v2/create-composite
```

## Key differences

- **Request Structure:** Input and output configuration has changed
- **Media Types:** More explicit media type declarations
- **Storage Options:** Enhanced storage options (external, hosted, embedded, Creative Cloud)
- **Multiple Outputs:** Generate multiple formats in a single request (up to 25 outputs)

## Basic format conversion

### PSD to JPEG

Convert a PSD file to JPEG format.

**Key Changes:**

- `inputs[0].href` → `image.source.url`
- `outputs[].href` → `outputs[].destination.url`
- `storage` → `storageType`
- `type` → `mediaType`
- `quality` (1-7 numeric scale) → `quality` (string: "very_poor", "poor", "low", "medium", "high", "maximum", "photoshop_max")

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/renditionCreate \
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
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/jpeg",
      "quality": 7,
      "width": 1920
    }
  ]
}'
```

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
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "width": 1920
    }
  ]
}' 
```

### PSD to PNG

Convert a PSD file to PNG format with transparency support.

**PNG-Specific Options:**

- `compression`: Control PNG compression level ("none", "very_low", "low", "medium_low", "medium", "medium_high", "default", "high", "very_high", "maximum")
- `shouldTrimToCanvas`: Trim transparent pixels around image

**V1 Approach:**

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/renditionCreate \
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
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/png",
      "width": 2048
    }
  ]
}'
```

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
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/png",
      "compression": "medium",
      "width": 2048
    }
  ]
}' 
```

### PSD to Cloud PSD

Convert a PSD file to Cloud PSD format for cloud-optimized storage.

**Cloud PSD Benefits:**

- Optimized for cloud storage and streaming
- Faster access to layer information
- Efficient for web-based editing workflows
- Compatible with Creative Cloud applications
- Best used with Creative Cloud storage for seamless integration

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
  "outputs": [
    {
      "destination": {
        "creativeCloudPath": "my-folder/output.psdc"
      },
      "mediaType": "document/vnd.adobe.cpsd+dcxucf"
    }
  ]
}' 
```

<InlineAlert variant="info" slots="text1"/>

For Cloud PSD format, both `document/vnd.adobe.cpsd+dcx` and `document/vnd.adobe.cpsd+dcxucf` are supported for ACP (Adobe Cloud Platform) storage and external storages

## Resizing during conversion

You can resize images during format conversion to generate thumbnails or scaled outputs.

**Sizing Options:**

- Specify `width` only - Height calculated automatically to maintain aspect ratio
- Specify `height` only - Width calculated automatically to maintain aspect ratio
- Specify both `width` and `height` - Image fits within bounds maintaining aspect ratio
- Size range: 1 to 32000 pixels

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
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high",
      "width": 800,
      "height": 600
    }
  ]
}' 
```

## Multiple format outputs

Generate multiple formats from a single PSD in one API call.

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
  "outputs": [
    {
      "destination": {
        "url": "<PSD_OUTPUT_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": {
        "url": "<JPEG_FULL_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum"
    },
    {
      "destination": {
        "url": "<JPEG_THUMB_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high",
      "width": 400
    },
    {
      "destination": {
        "url": "<PNG_URL>"
      },
      "mediaType": "image/png",
      "compression": "small",
      "shouldTrimToCanvas": true
    }
  ]
}'
```

<InlineAlert variant="info" slots="text"/>

Maximum of 25 outputs allowed per request.

## Quality and compression options

### JPEG quality settings

V2 uses descriptive quality levels instead of numeric scales:

| V2 Quality | V1 Quality (1-7) | Description                       |
| ---------- | ---------------- | --------------------------------- |
| `very_poor` | N/A             | Smallest files (V2 only) |
| `poor`      | N/A             | Very small files (V2 only) |
| `low`       | 1-2             | Thumbnails, small previews |
| `medium`    | 3-4             | Standard web images         |
| `high`      | 5-6             | High-quality web images        |
| `maximum`   | 7               | Print, production       |
| `photoshop_max` | N/A         | Professional print, highest quality |

The quality parameter is optional. If not specified, the API uses different defaults based on the operation type:

- **Create Composite** (`/v2/create-composite`): Default quality is `photoshop_max`
- **Generate Manifest** (`/v2/generate-manifest`): Default quality for layer thumbnails is `medium`

**Example:**

```json
{
  "mediaType": "image/jpeg",
  "quality": "high"
}
```

### PNG compression settings

V2 offers ten compression levels (following zlib/libpng standards):

```json
{
  "mediaType": "image/png",
  "compression": "medium"
}
```

**Compression Options:**

- `none` - No compression (level 0)
- `very_low` - Minimal compression (level 1)
- `low` - Low compression (level 2)
- `medium_low` - Medium-low compression (level 3)
- `medium` - Medium compression (level 4)
- `medium_high` - Medium-high compression (level 5)
- `default` - Default compression (level 6, library standard)
- `high` - High compression (level 7)
- `very_high` - Very high compression (level 8)
- `maximum` - Maximum compression (level 9)

<InlineAlert variant="info" slots="text"/>

The compression parameter is optional. If not specified, the API uses `default` (level 6) for both Create Composite and Generate Manifest operations.

**V1 to V2 Mapping:**

| V1 Compression | V2 Recommended | V2 Alternatives | Notes |
|---------------|----------------|-----------------|-------|
| `small` | `maximum` | `very_high`, `high` | Smallest file size, slower |
| `medium` | `medium` | `default`, `medium_high`, `medium_low` | Balanced performance |
| `large` | `low` | `very_low`, `none` | Fastest, larger files |

## Storage options

V2 provides multiple storage options for outputs:

### External storage (pre-signed URLs)

```json
{
  "destination": {
    "url": "<SIGNED_POST_URL>"
  }
}
```

<InlineAlert variant="info" slots="text"/>

`storageType` is NOT required for AWS S3 presigned URLs or standard HTTPS URLs. Only use `storageType` for Azure Blob Storage (`"storageType": "azure"`) or Dropbox (`"storageType": "dropbox"`).

### Hosted storage (temporary Adobe hosting)

```json
{
  "destination": {
    "validityPeriod": 3600
  }
}
```

- Files hosted by Adobe for the specified duration (in seconds)
- Useful for temporary processing workflows
- No need to manage your own storage

### Creative Cloud storage with path

```json
{
  "destination": {
    "creativeCloudPath": "my-folder/output.jpg"
  }
}
```

- Store directly in user's Creative Cloud Files
- Requires user authentication
- Seamless integration with CC workflows

### Creative Cloud storage with project ID

```json
{
  "destination": {
    "creativeCloudPath": "project-assets/output.jpg",
    "creativeCloudProjectId": "urn:aaid:sc:US:a21c8629-413f-55d9-b5b0-....."
  }
}
```

To identify an asset in a project:

- `creativeCloudProjectId` (a URN starting with `urn:aaid:`) must be the ID of the project root.
- `creativeCloudPath` is the asset's path relative to that project root.
- Useful when working with Creative Cloud project-specific assets.

### Embedded (inline response)

<InlineAlert variant="warning" slots="text"/>

Embedded storage is only recommended for small outputs like JSON metadata, not for image files.

```json
{
  "destination": {
    "embedded": "base64"
  }
}
```

### Cloud PSD storage support

Cloud PSD supports the following media types for both ACP Storage and External Storage (e.g., S3, Azure):

- `document/vnd.adobe.cpsd+dcxucf`
- `document/vnd.adobe.cpsd+dcx`

## Converting with source from different storage

### From Creative Cloud

**Creative Cloud Path:**

```json
{
  "image": {
    "source": {
      "creativeCloudPath": "my-folder/design.psd"
    }
  }
}
```

- The `creativeCloudPath` property is sufficient when specifying the location of a file in the user's personal storage area

**Creative Cloud Project ID:**

```json
{
  "image": {
    "source": {
      "creativeCloudPath": "my-folder/design.psd",
      "creativeCloudProjectId": "urn:aaid:sc:US:a21c8629-413f-55d9-b5b0-....."
    }
  }
}
```

To identify an asset in a project:

- `creativeCloudProjectId` (a URN starting with `urn:aaid:`) must be the ID of the project root.
- `creativeCloudPath` is the asset's path relative to that project root.

### From Adobe Assets

```json
{
  "image": {
    "source": {
      "url": "https://assets.adobe.com/...",
      "storageType": "adobe"
    }
  }
}
```

## Complete conversion example

Here's a comprehensive example converting a PSD to multiple formats with various options:

<Accordion>
<AccordionItem header="Full Example">

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
  "outputs": [
    {
      "destination": {
        "url": "<CLOUD_PSD_URL>"
      },
      "mediaType": "document/vnd.adobe.cpsd+dcxucf"
    },
    {
      "destination": {
        "url": "<JPEG_FULL_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "maximum"
    },
    {
      "destination": {
        "url": "<JPEG_LARGE_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high",
      "width": 2048
    },
    {
      "destination": {
        "url": "<JPEG_MEDIUM_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "medium",
      "width": 1024
    },
    {
      "destination": {
        "url": "<JPEG_THUMB_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "medium",
      "width": 400
    },
    {
      "destination": {
        "url": "<PNG_URL>"
      },
      "mediaType": "image/png",
      "compression": "medium",
      "shouldTrimToCanvas": true
    }
  ]
}'
```

</AccordionItem>
</Accordion>

## Common migration issues

### Quality parameter not accepted

❌ **Problem:** Using numeric quality values from v1

```json
{
  "quality": 7
}
```

✅ **Solution:** Use descriptive quality strings

```json
{
  "quality": "maximum"
}
```

### Storage parameter not recognized

❌ **Problem:** Using v1 storage parameter

```json
{
  "storage": "external"
}
```

✅ **Solution:** Remove storage parameter for standard URLs

```json
{
  "destination": {
    "url": "<URL>"
    // storageType NOT required for S3/HTTPS URLs
    // Only use storageType for Azure ("azure") or Dropbox ("dropbox")
  }
}
```

### Type vs MediaType

❌ **Problem:** Using v1 `type` parameter

```json
{
  "type": "image/jpeg"
}
```

✅ **Solution:** Use `mediaType`

```json
{
  "mediaType": "image/jpeg"
}
```

## Migrating from PSDC conversion engine (Sensei service)

<InlineAlert variant="warning" slots="text"/>

The following service is not available to Enterprise.

<InlineAlert variant="warning" slots="text"/>

**⚠️ Important:** The sensei `/v2/predict` endpoint continues to operate. Only the PSDC Conversion Engine (ID: `Feature:sensei-demo:Service-66484d87ede04702af063315a7de4094`) is being retired. Other engines on `/v2/predict` are unaffected.

**📝 Format Naming:** PSDC, Cloud PSD, and CPSD all refer to the same format. v2 documentation uses "Cloud PSD" consistently.

**📦 Format Support:** The v2 API supports the Cloud PSD format using two media types: `document/vnd.adobe.cpsd+dcx` and `document/vnd.adobe.cpsd+dcxucf`. Both media types are fully supported for use with ACP Storage (Adobe Cloud Platform) as well as External Storage. Either format may be used with either storage option.

### Overview

The PSDC Conversion Engine was used for converting between PSD and Cloud PSD (PSDC/CPSD) formats. This engine is being retired and its functionality is now available through the V2 `/v2/create-composite` endpoint.

**PSDC Engine:**

```shell
POST /services/v2/predict
Engine ID: Feature:sensei-demo:Service-66484d87ede04702af063315a7de4094
```

**V2 API:**

```shell
POST /v2/create-composite
```

### Cloud PSD to PSD conversion (using URN)

Convert a Cloud PSD file to PSD format using file URN.

**Key Changes:**

- `repo:id` → `creativeCloudFileId` (input via URN)
- `repo:path` → `creativeCloudPath` (output to file path)
- `sensei:repoType: "RAPI"` → Not needed (inferred from field used)
- `dc:format` → `mediaType` (always `image/vnd.adobe.photoshop`)
- Simple JSON structure (no multipart/form-data)

**PSDC Engine:**

```shell
curl -X POST \
  https://sensei-ue1.adobe.io/services/v2/predict \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: multipart/form-data" \
  -F 'contentAnalyzerRequests={
  "sensei:invocation_mode": "asynchronous",
  "sensei:invocation_batch": false,
  "sensei:in_response": false,
  "sensei:engines": [{
    "sensei:execution_info": {
      "sensei:engine": "Feature:sensei-demo:Service-66484d87ede04702af063315a7de4094"
    },
    "sensei:inputs": {
      "image_in": {
        "repo:id": "urn:aaid:sc:US:edc9dc37-fb7a-4bcd-9e22-717f1ef7fa44",
        "dc:format": "document/vnd.adobe.cpsd+dcx",
        "sensei:repoType": "RAPI"
      }
    },
    "sensei:params": {
      "format": "image/vnd.adobe.photoshop"
    },
    "sensei:outputs": {
      "image_out": {
        "repo:path": "/temp/output.psd",
        "dc:format": "image/vnd.adobe.photoshop",
        "sensei:repoType": "RAPI"
      }
    }
  }]
}'
```

**V2 API:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "creativeCloudFileId": "urn:aaid:sc:US:edc9dc37-fb7a-4bcd-9e22-717f1ef7fa44"
    }
  },
  "outputs": [{
    "destination": {
      "creativeCloudPath": "temp/output.psd"
    },
    "mediaType": "image/vnd.adobe.photoshop"
  }] 
}' 
```

### PSD to Cloud PSD conversion (using file path)

Convert a PSD file to Cloud PSD format using path.

**PSDC Engine:**

```shell
curl -X POST \
  https://sensei-ue1.adobe.io/services/v2/predict \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: multipart/form-data" \
  -F 'contentAnalyzerRequests={
  "sensei:engines": [{
    "sensei:execution_info": {
      "sensei:engine": "Feature:sensei-demo:Service-66484d87ede04702af063315a7de4094"
    },
    "sensei:inputs": {
      "image_in": {
        "repo:path": "/files/input.psd",
        "dc:format": "image/vnd.adobe.photoshop",
        "sensei:repoType": "CCRepo"
      }
    },
    "sensei:params": {
      "format": "document/vnd.adobe.cpsd+dcx"
    },
    "sensei:outputs": {
      "image_out": {
        "repo:path": "/files/output.psdc",
        "dc:format": "document/vnd.adobe.cpsd+dcxucf",
        "sensei:repoType": "CCRepo"
      }
    }
  }]
}'
```

**V2 API:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "creativeCloudPath": "files/input.psd"
    }
  },
  "outputs": [{
    "destination": {
      "creativeCloudPath": "files/output.psdc"
    },
    "mediaType": "document/vnd.adobe.cpsd+dcxucf"
  }]
}'
```

### PSD to Cloud PSD conversion (using project ID)

Convert a PSD file to Cloud PSD format using project id and path

**Key Changes:**

- `repo:id` / `repo:path` (input) → `creativeCloudPath` + `creativeCloudProjectId` (project-scoped input)
- `repo:id` / `repo:path` (output) → `creativeCloudPath` + `creativeCloudProjectId` (project-scoped output)
- `sensei:repoType: "RAPI"` → Not needed (inferred from fields used)
- `dc:format` → `mediaType` (always `document/vnd.adobe.cpsd+dcxucf` or `document/vnd.adobe.cpsd+dcx`)
- Simple JSON structure (no multipart/form-data)

**V2 API:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "creativeCloudPath": "project-files/input.psd",
      "creativeCloudProjectId": "urn:aaid:sc:US:a21c8629-413f-55d9-b5b0-....."
    }
  },
  "outputs": [{
    "destination": {
      "creativeCloudPath": "project-files/output.psdc",
      "creativeCloudProjectId": "urn:aaid:sc:US:a21c8629-413f-55d9-b5b0-....."
    },
    "mediaType": "document/vnd.adobe.cpsd+dcx"
  }] 
}' 
```

<InlineAlert variant="info" slots="text"/>

Use `creativeCloudProjectId` together with `creativeCloudPath` when working with project-specific assets to ensure proper project context and permissions.

- `creativeCloudProjectId` must be a valid URN (starting with `urn:aaid:sc:`) of the project root.
- `creativeCloudPath` is the asset's path relative to that project root.

### Parameter mapping

| PSDC Engine | V2 API | Notes |
|-------------|--------|-------|
| `sensei:engine` | `/v2/create-composite` | Different endpoint |
| `repo:id` (URN) | `creativeCloudFileId` | Asset's identifier (URN ID) on ACP Storage provided as an input |
| `repo:path` (input) | `creativeCloudPath` | Asset's path in personal storage; or path relative to project root when used with creativeCloudProjectId provided as an input |
| `repo:path` (output) | `creativeCloudPath` | Asset's path in personal storage; or path relative to project root when used with creativeCloudProjectId provided as an output |
| N/A | `creativeCloudProjectId` (input) | Optional project root ID (URN) for project-scoped input assets |
| N/A | `creativeCloudProjectId` (output) | Optional project root ID (URN) for project-scoped output assets |
| `sensei:repoType` | Not needed | Inferred from field type |
| `dc:format` (input) | Auto-detected | Not required in V2 |
| `dcxucf:format` (output) | `mediaType` | Use `document/vnd.adobe.cpsd+dcxucf` or `document/vnd.adobe.cpsd+dcx` |
| `sensei:params.format` | `mediaType` in output | Simplified |
| `document/vnd.adobe.cpsd+dcx` | `document/vnd.adobe.cpsd+dcxucf` or `document/vnd.adobe.cpsd+dcx`| Cloud PSD format |
| Status: separate endpoint | `/v2/status/{jobId}` | Unified status |

**Benefits:**

- Simpler JSON structure
- No multipart/form-data complexity
- Unified status endpoint
- Same authentication as other V2 endpoints

<HorizontalLine />

## When to use format conversion vs other endpoints

Use **Format Conversion** (`/create-composite` without edits) when:

- Converting PSD to other formats (JPEG, PNG)
- Generating multiple output sizes
- Creating thumbnails
- Converting to Cloud PSD format
- Simple rendering without modifications

Use **[Document Operations](document-operations-migration.md)** when:

- Cropping, resizing, or trimming documents
- Modifying canvas size
- Applying document-level transformations

Use **[Composite Operations](composite-migration.md)** when:

- Adding, removing, or modifying layers
- Applying layer effects
- Complex multi-layer compositions

## Next steps

- Review the [storage solutions guide](../../../getting-started/storage-solutions/index.md) for more storage options
- Check the [status migration guide](status-migration.md) for checking job status
- Test your conversion operations with development endpoints

## Need help?

Contact the Adobe DI ART Service team for technical support with format conversion operations.
