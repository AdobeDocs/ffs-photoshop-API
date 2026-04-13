---
title: Product Crop Migration (v1 to v2)
description: Migrate from v1 productCrop to v2 execute-actions for auto-crop and padding.
hideBreadcrumbNav: true
keywords:
  - product crop
  - convenience API
  - migration
  - v1 to v2
---
# Product Crop Migration (v1 to v2)

This guide shows how to migrate from the v1 API's `/pie/psdService/productCrop` endpoint to the v2 API's `/v2/execute-actions` endpoint.

The Product Crop convenience API automatically removes backgrounds and adds customizable padding - perfect for e-commerce product photography.

**Key benefits of the v2 API:**

- Access to the exact ActionJSON used server-side
- Full customization of all parameters
- Ability to modify and extend the workflow
- Consistent with other action-based APIs

## V1 API (Deprecated)

**Endpoint:** `/pie/psdService/productCrop`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/productCrop \
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
      "type": "image/jpeg"
    }
  ]
}'
```

## V2 API (Current)

**Endpoint:** `/v2/execute-actions`

### Using inline ActionJSON

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/execute-actions \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"autoCutout\",\"sampleAllLayers\":false},{\"_obj\":\"make\",\"at\":{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"mask\"},\"new\":{\"_class\":\"channel\"},\"using\":{\"_enum\":\"userMaskEnabled\",\"_value\":\"revealSelection\"}},{\"_obj\":\"newPlacedLayer\"},{\"_obj\":\"trim\",\"bottom\":true,\"left\":true,\"right\":true,\"top\":true,\"trimBasedOn\":{\"_enum\":\"trimBasedOn\",\"_value\":\"transparency\"}},{\"_obj\":\"canvasSize\",\"height\":{\"_unit\":\"pixelsUnit\",\"_value\":10},\"horizontal\":{\"_enum\":\"horizontalLocation\",\"_value\":\"center\"},\"relative\":true,\"vertical\":{\"_enum\":\"verticalLocation\",\"_value\":\"center\"},\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":10}},{\"_obj\":\"placedLayerConvertToLayers\"},{\"_obj\":\"delete\",\"_target\":[{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"mask\"}]},{\"_obj\":\"trim\",\"bottom\":true,\"left\":true,\"right\":true,\"top\":true,\"trimBasedOn\":{\"_enum\":\"trimBasedOn\",\"_value\":\"transparency\"}}]",
          "contentType": "application/json"
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

## ActionJSON Definition

The Product Crop action performs 8 distinct operations:

```json
[
  {
    "_obj": "autoCutout",
    "sampleAllLayers": false
  },
  {
    "_obj": "make",
    "at": {
      "_enum": "channel",
      "_ref": "channel",
      "_value": "mask"
    },
    "new": {
      "_class": "channel"
    },
    "using": {
      "_enum": "userMaskEnabled",
      "_value": "revealSelection"
    }
  },
  {
    "_obj": "newPlacedLayer"
  },
  {
    "_obj": "trim",
    "bottom": true,
    "left": true,
    "right": true,
    "top": true,
    "trimBasedOn": {
      "_enum": "trimBasedOn",
      "_value": "transparency"
    }
  },
  {
    "_obj": "canvasSize",
    "height": {
      "_unit": "pixelsUnit",
      "_value": 10
    },
    "horizontal": {
      "_enum": "horizontalLocation",
      "_value": "center"
    },
    "relative": true,
    "vertical": {
      "_enum": "verticalLocation",
      "_value": "center"
    },
    "width": {
      "_unit": "pixelsUnit",
      "_value": 10
    }
  },
  {
    "_obj": "placedLayerConvertToLayers"
  },
  {
    "_obj": "delete",
    "_target": [
      {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
      }
    ]
  },
  {
    "_obj": "trim",
    "bottom": true,
    "left": true,
    "right": true,
    "top": true,
    "trimBasedOn": {
      "_enum": "trimBasedOn",
      "_value": "transparency"
    }
  }
]
```

## What this action does

1. **Auto Cutout** - Automatically detects and isolates the main subject using AI
2. **Create Mask** - Creates a layer mask from the auto-generated selection
3. **Convert to Smart Object** - Converts layer to smart object for non-destructive editing
4. **First Trim** - Removes transparent pixels around the subject to minimize canvas size
5. **Add Canvas Padding** - Adds 10 pixels of padding on all sides (default, customizable)
6. **Convert to Layers** - Converts smart object back to regular layer
7. **Delete Mask** - Removes the layer mask (no longer needed)
8. **Final Trim** - Final trim to clean up edges and ensure consistent output

## Customizing the padding

The default action uses 10-pixel padding on all sides. To customize:

### Modify padding values

Locate the `canvasSize` step (5th action in the sequence) and modify the `_value` fields:

**Example with 100-pixel padding:**

```json
{
  "_obj": "canvasSize",
  "height": {
    "_unit": "pixelsUnit",
    "_value": 100
  },
  "horizontal": {
    "_enum": "horizontalLocation",
    "_value": "center"
  },
  "relative": true,
  "vertical": {
    "_enum": "verticalLocation",
    "_value": "center"
  },
  "width": {
    "_unit": "pixelsUnit",
    "_value": 100
  }
}
```

### Change to percentage-based padding

You can also use percentage-based padding by changing the `_unit`:

```json
{
  "_obj": "canvasSize",
  "height": {
    "_unit": "percentUnit",
    "_value": 10
  },
  ...
  "width": {
    "_unit": "percentUnit",
    "_value": 10
  }
}
```

This adds 10% padding to each side.

## Common customizations

### 1. No padding (tight crop)

Remove the `canvasSize` step entirely or set values to 0:

```json
{
  "_obj": "canvasSize",
  "height": {
    "_unit": "pixelsUnit",
    "_value": 0
  },
  ...
}
```

### 2. Asymmetric padding

For different padding on different sides, you'll need to use multiple `canvasSize` operations or switch to absolute positioning.

### 3. Add post-processing

You can add additional actions after the product crop sequence:

```json
{
  "options": {
    "actions": [
      {
        "source": {
          "content": "[...product crop actions...{\"_obj\":\"brightnessEvent\",\"brightness\":20}]",
          "contentType": "application/json"
        }
      }
    ]
  }
}
```

## Migration checklist

- [ ] Replace `/pie/psdService/productCrop` endpoint with `/v2/execute-actions`
- [ ] Update request structure from `inputs`/`outputs` to `image`/`outputs`
- [ ] Convert `href` fields to `url` fields
- [ ] Remove `storage` fields (V2 auto-detects storage type)
- [ ] Update `type` field to `mediaType`
- [ ] Include the ActionJSON in `options.actions[].source.content`
- [ ] Set `contentType` to `"application/json"`
- [ ] Test with default padding values
- [ ] Customize padding if needed for your use case

## Migration examples

### Basic migration

**V1:**

```json
{
  "inputs": [{"href": "s3://input.jpg", "storage": "external"}],
  "outputs": [{"href": "s3://output.jpg", "type": "image/jpeg"}]
}
```

**V2:**

```json
{
  "image": {"source": {"url": "s3://input.jpg"}},
  "options": {
    "actions": [{
      "source": {
        "content": "[{...ActionJSON...}]",
        "contentType": "application/json"
      }
    }]
  },
  "outputs": [{"destination": {"url": "s3://output.jpg"}, "mediaType": "image/jpeg"}]
}
```

### With custom padding

```json
{
  "image": {"source": {"url": "https://..."}},
  "options": {
    "actions": [{
      "source": {
        "content": "[{...modify canvasSize _value to 100...}]",
        "contentType": "application/json"
      }
    }]
  },
  "outputs": [{"destination": {"url": "https://..."}, "mediaType": "image/png"}]
}
```

## Additional resources

- [Actions Migration Overview](../actions-migration.md)
- [V2 Execute Actions API Reference](https://developer.adobe.com/photoshop/photoshop-api-docs/api/#tag/Photoshop/operation/actionJsonCreate)
- [Image I/O Guide](https://developer.adobe.com/photoshop/photoshop-api-docs/features/#input-and-output)

## Support

For questions or issues:

- [Adobe Developer Forum](https://community.adobe.com/t5/photoshop-api/ct-p/ct-photoshop-api)
- [GitHub Issues](https://github.com/AdobeDocs/photoshop-api-docs/issues)
