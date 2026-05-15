---
title: Smart Object Replace Migration
description: Migrate from V1 /pie/psdService/smartObject to V2 /v2/create-composite
hideBreadcrumbNav: true
keywords:
  - smart objects
  - smart object replace
  - smart object place
  - migration
  - v1 to v2
  - create-composite
---

# Smart Object Replace Migration (V1 to V2)

<InlineAlert variant="info" slots="text"/>

This guide covers migration from V1's dedicated `/pie/psdService/smartObject` endpoint to V2's `/v2/create-composite` endpoint.

<InlineAlert variant="info" slots="text"/>

V1 also used `/pie/psdService/documentOperations` for smart object layer operations embedded in larger document workflows. That migration path is covered in [Smart Object Layer Operations](../layer-operations-smart-objects.md). This guide covers only the dedicated `/psdService/smartObject` endpoint.

## Overview

V1's `/psdService/smartObject` endpoint was a dedicated convenience endpoint for two operations:

- **Place** — add a new smart object layer to an existing PSD
- **Replace** — swap the content of an existing smart object layer

In V2, both operations are handled by `/v2/create-composite` using `edits.layers` with `type: "smart_object_layer"`.

**V1 Endpoint:** `/pie/psdService/smartObject`

**V2 Endpoint:** `/v2/create-composite`

## Place a Smart Object (Add)

### V1 Request

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/smartObject \
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
    "layers": [
      {
        "name": "My Smart Object",
        "add": {
          "insertTop": true
        },
        "input": {
          "href": "<SMART_OBJECT_SOURCE_URL>",
          "storage": "external"
        }
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "vnd.adobe.photoshop"
    }
  ]
}'
```

### V2 Request

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
        "type": "smart_object_layer",
        "name": "My Smart Object",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<SMART_OBJECT_SOURCE_URL>"
            }
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

## Replace Smart Object Content

### V1 Request

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/smartObject \
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
    "layers": [
      {
        "name": "Existing Smart Object Layer",
        "input": {
          "href": "<NEW_CONTENT_URL>",
          "storage": "external"
        }
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "vnd.adobe.photoshop"
    }
  ]
}'
```

### V2 Request

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
        "type": "smart_object_layer",
        "name": "Existing Smart Object Layer",
        "operation": {
          "type": "edit"
        },
        "smartObject": {
          "smartObjectFile": {
            "source": {
              "url": "<NEW_CONTENT_URL>"
            }
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

## Key Field Mapping

| V1 Field | V2 Field | Notes |
|----------|----------|-------|
| `inputs[0].href` | `image.source.url` | PSD input |
| `inputs[0].storage` | *(removed)* | Not needed for presigned URLs |
| `options.layers[].name` | `edits.layers[].name` | Layer name unchanged |
| `options.layers[].add.insertTop` | `edits.layers[].operation.type: "add"` + `placement.type: "top"` | See [Placement Options](#placement-options) |
| `options.layers[].add.insertBottom` | `placement.type: "bottom"` | |
| `options.layers[].add.insertAbove` | `placement.type: "above"` + `referenceLayer` | |
| `options.layers[].add.insertBelow` | `placement.type: "below"` + `referenceLayer` | |
| `options.layers[].input.href` | `edits.layers[].smartObject.smartObjectFile.source.url` | Smart object source file |
| `options.layers[].input.storage` | *(removed)* | Not needed for presigned URLs |
| *(no field — replace implied by omitting `add`)* | `operation.type: "edit"` | V2 requires explicit operation |
| `outputs[0].href` | `outputs[0].destination.url` | Output destination |
| `outputs[0].type: "vnd.adobe.photoshop"` | `outputs[0].mediaType: "image/vnd.adobe.photoshop"` | Format field renamed |

## Placement Options

### V1 Placement

```json
{
  "add": {
    "insertTop": true
  }
}
```

```json
{
  "add": {
    "insertAbove": { "name": "Background" }
  }
}
```

### V2 Placement

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  }
}
```

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "above",
      "referenceLayer": {
        "name": "Background"
      }
    }
  }
}
```

Supported placement types: `"top"`, `"bottom"`, `"above"`, `"below"`, `"into"`.

<InlineAlert variant="info" slots="text"/>

V2 uses `referenceLayer` with `name` or `id` instead of inline object references.

## V1 Limitations Lifted in V2

| V1 Limitation | V2 Behavior |
|---------------|-------------|
| Linked smart objects not supported | `smartObject.isLinked: true` supported |
| Objects over 2000×2000 px are rasterized | No equivalent rasterization limit |
| Smart object name must be alphanumeric | Any valid layer name accepted |
| Replaced smart object auto-fits original bounding box | Use `transformMode` to control fit behavior |

For transform control, see [Smart Object Layer Operations](../layer-operations-smart-objects.md#transform-mode).

## Migration Checklist

- [ ] Change endpoint from `https://image.adobe.io/pie/psdService/smartObject` to `https://photoshop-api.adobe.io/v2/create-composite`
- [ ] Move `inputs[0].href` to `image.source.url`
- [ ] Remove `storage` fields (not needed for presigned URLs)
- [ ] Add `"type": "smart_object_layer"` to each layer entry
- [ ] For add operations: convert `add.insertTop/Bottom/Above/Below` to `operation.type: "add"` + `placement`
- [ ] For replace operations: add `operation.type: "edit"` (required in V2 — there is no implicit replace)
- [ ] Move `input.href` to `smartObject.smartObjectFile.source.url`
- [ ] Change `outputs[0].href` to `outputs[0].destination.url`
- [ ] Change `outputs[0].type` to `outputs[0].mediaType: "image/vnd.adobe.photoshop"`

## Additional Resources

- [Smart Object Layer Operations](../layer-operations-smart-objects.md) — Full V2 smart object layer reference including transformations, linked objects, and V1 `documentOperations` migration
- [Layer Operations Overview](../layer-operations-overview.md) — V2 processing order and `referenceLayer`
- [Text Layer Operations Migration](text-layer-operations.md) — Companion convenience API migration guide
