---
title: Depth Blur Migration
description: Migrate from V1 depthBlur to V2 execute-actions for Neural Filter depth-of-field effects
hideBreadcrumbNav: true
keywords:
  - depth blur
  - neural filters
  - convenience API
  - migration
  - v1 to v2
---

# Depth Blur Migration

Migrate from the v1 API's `/pie/psdService/depthBlur` endpoint to the v2 API.

## Overview

The Depth Blur convenience API uses Photoshop's Neural Filters to create professional depth-of-field effects with customizable blur parameters. This guide shows how to migrate from V1's `/pie/psdService/depthBlur` to V2's `/v2/execute-actions`.

**Key benefits of V2:**
- Access to all 11 customizable parameters
- Full control over blur intensity, focal point, and color adjustments
- Ability to chain with other actions
- Published ActionJSON for learning and customization

<InlineAlert variant="warning" slots="text"/>

**Depth Blur is not currently supported in V2.** Neural Filters, which power the depth blur functionality, are not yet available in the V2 API. The V1 `/pie/psdService/depthBlur` endpoint remains the only way to use this feature at this time. This documentation is provided for reference and will be updated once Neural Filters support is added to V2.

## V1 API (deprecated)

**Endpoint:** `/pie/psdService/depthBlur`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/depthBlur \
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

## V2 API (current)

**Endpoint:** `/v2/execute-actions`

### Using default settings

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
          "content": "[{\"NF_OUTPUT_TYPE\":1,\"NF_UI_DATA\":{\"_obj\":\"NF_UI_DATA\",\"spl::filterStack\":[{\"_obj\":\"spl::filterStack\",\"spl::cropStates\":[{\"_obj\":\"spl::cropStates\",\"spl::cropId\":\"layer1\",\"spl::values\":{\"_obj\":\"spl::values\",\"spl::focalSelector\":\"auto\",\"spl::generateDepthMap\":false,\"spl::selectSubjectUsage\":1,\"spl::slideAperture\":50,\"spl::slideFocalDist\":50,\"spl::slideFocalRange\":50,\"spl::sliderBrightness\":0,\"spl::sliderHaze\":0,\"spl::sliderNoise\":0,\"spl::sliderSaturation\":0,\"spl::sliderSelectResolutionLevel\":1,\"spl::sliderTint\":0,\"spl::sliderWarmness\":0}}],\"spl::enabled\":true,\"spl::id\":\"internal.Hazy\",\"spl::version\":\"1.0\"}],\"spl::version\":\"1.0.6\"},\"_obj\":\"neuralGalleryFilters\"}]",
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

## ActionJSON definition

The Depth Blur action uses Photoshop's Neural Gallery Filters:

```json
[
  {
    "NF_OUTPUT_TYPE": 1,
    "NF_UI_DATA": {
      "_obj": "NF_UI_DATA",
      "spl::filterStack": [
        {
          "_obj": "spl::filterStack",
          "spl::cropStates": [
            {
              "_obj": "spl::cropStates",
              "spl::cropId": "layer1",
              "spl::values": {
                "_obj": "spl::values",
                "spl::focalSelector": "auto",
                "spl::generateDepthMap": false,
                "spl::selectSubjectUsage": 1,
                "spl::slideAperture": 50,
                "spl::slideFocalDist": 50,
                "spl::slideFocalRange": 50,
                "spl::sliderBrightness": 0,
                "spl::sliderHaze": 0,
                "spl::sliderNoise": 0,
                "spl::sliderSaturation": 0,
                "spl::sliderSelectResolutionLevel": 1,
                "spl::sliderTint": 0,
                "spl::sliderWarmness": 0
              }
            }
          ],
          "spl::enabled": true,
          "spl::id": "internal.Hazy",
          "spl::version": "1.0"
        }
      ],
      "spl::version": "1.0.6"
    },
    "_obj": "neuralGalleryFilters"
  }
]
```

## Customizable parameters

All parameters with their default values and ranges:

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `spl::focalSelector` | `"auto"` | `"auto"`, `"manual"` | Focus point selection method |
| `spl::selectSubjectUsage` | `1` | `0`, `1` | Subject selection mode (0=off, 1=on) |
| `spl::slideAperture` | `50` | `0-100` | **Blur strength** - Higher values create more blur |
| `spl::slideFocalDist` | `50` | `0-100` | **Focal distance** - Where the focus point is |
| `spl::slideFocalRange` | `50` | `0-100` | **Focal range** - Size of the focused area |
| `spl::sliderBrightness` | `0` | `-100 to 100` | Brightness adjustment |
| `spl::sliderHaze` | `0` | `-100 to 100` | Haze effect intensity |
| `spl::sliderNoise` | `0` | `0-100` | Grain/noise amount |
| `spl::sliderSaturation` | `0` | `-100 to 100` | Color saturation adjustment |
| `spl::sliderTint` | `0` | `-100 to 100` | Color tint adjustment |
| `spl::sliderWarmness` | `0` | `-100 to 100` | Color temperature adjustment |

## Customization examples

### Strong blur effect

Increase the `slideAperture` value for more intense blur:

```json
{
  "spl::values": {
    "_obj": "spl::values",
    "spl::focalSelector": "auto",
    "spl::selectSubjectUsage": 1,
    "spl::slideAperture": 90,
    "spl::slideFocalDist": 50,
    "spl::slideFocalRange": 50,
    ...
  }
}
```

### Cinematic look with warm tint

```json
{
  "spl::values": {
    "_obj": "spl::values",
    "spl::slideAperture": 70,
    "spl::sliderBrightness": 10,
    "spl::sliderHaze": 15,
    "spl::sliderWarmness": 20,
    "spl::sliderSaturation": 10,
    ...
  }
}
```

### Portrait mode effect

```json
{
  "spl::values": {
    "_obj": "spl::values",
    "spl::slideAperture": 85,
    "spl::slideFocalDist": 30,
    "spl::slideFocalRange": 40,
    "spl::sliderBrightness": 5,
    ...
  }
}
```

## Parameter guide

### Focus control

- **`spl::focalSelector`**: Set to `"auto"` for AI-detected focus, or `"manual"` for custom control
- **`spl::selectSubjectUsage`**: When set to `1`, automatically detects the main subject
- **`spl::slideFocalDist`**: Controls where the focus plane is positioned (0=foreground, 100=background)
- **`spl::slideFocalRange`**: Controls the size of the in-focus area (smaller=tighter focus, larger=more in focus)

### Blur intensity

- **`spl::slideAperture`**: The primary blur control
  - `0-30`: Subtle blur
  - `30-60`: Medium blur (default: 50)
  - `60-100`: Strong blur for dramatic effects

### Color and atmosphere

- **`spl::sliderBrightness`**: Brighten (`+`) or darken (`-`) the image
- **`spl::sliderHaze`**: Add atmospheric haze (`+`) or increase clarity (`-`)
- **`spl::sliderSaturation`**: Boost (`+`) or reduce (`-`) color intensity
- **`spl::sliderTint`**: Shift towards magenta (`+`) or green (`-`)
- **`spl::sliderWarmness`**: Warm/orange (`+`) or cool/blue (`-`) color temperature
- **`spl::sliderNoise`**: Add film grain or texture

## Migration checklist

- [ ] Replace `/pie/psdService/depthBlur` endpoint with `/v2/execute-actions`
- [ ] Update request structure from `inputs`/`outputs` to `image`/`outputs`
- [ ] Convert `href` fields to `url` fields
- [ ] Remove `storage` fields
- [ ] Update `type` field to `mediaType`
- [ ] Include the ActionJSON in `options.actions[].source.content`
- [ ] Set `contentType` to `"application/json"`
- [ ] Test with default parameter values
- [ ] Customize parameters for your specific use case

## Migration examples

### Basic migration

**V1:**
```json
{
  "inputs": [{"href": "s3://portrait.jpg", "storage": "external"}],
  "outputs": [{"href": "s3://blurred.jpg", "type": "image/jpeg"}]
}
```

**V2:**
```json
{
  "image": {"source": {"url": "s3://portrait.jpg"}},
  "options": {
    "actions": [{
      "source": {
        "content": "[{...ActionJSON with default values...}]",
        "contentType": "application/json"
      }
    }]
  },
  "outputs": [{"destination": {"url": "s3://blurred.jpg"}, "mediaType": "image/jpeg"}]
}
```

### With custom blur strength

```json
{
  "image": {"source": {"url": "https://..."}},
  "options": {
    "actions": [{
      "source": {
        "content": "[{...modify slideAperture to 80...}]",
        "contentType": "application/json"
      }
    }]
  },
  "outputs": [{"destination": {"url": "https://..."}, "mediaType": "image/jpeg"}]
}
```

## Use cases

### Portrait photography
- **Blur**: 70-85
- **Focal Distance**: 30-40 (focus on face)
- **Focal Range**: 35-45 (keep face sharp)
- **Brightness**: +5 to +10
- **Warmness**: +10 to +20 (flattering skin tones)

### Product photography
- **Blur**: 60-75
- **Focal Distance**: 50 (center product)
- **Focal Range**: 30-40 (isolate product)
- **Brightness**: 0 to +5
- **Saturation**: +10 to +15 (vivid colors)

### Landscape/tilt-shift
- **Blur**: 50-70
- **Focal Distance**: 40-60 (focus on specific area)
- **Focal Range**: 20-30 (miniature effect)
- **Haze**: -10 to -20 (increase clarity)

## Additional resources

- [Actions Migration Overview](../actions-migration.md)
- [V2 Execute Actions API Reference](https://developer.adobe.com/firefly-services/docs/photoshop/api/photoshop-v2-beta/#operation/executeActions)
