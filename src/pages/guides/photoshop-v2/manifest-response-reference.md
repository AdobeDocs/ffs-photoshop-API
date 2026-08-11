---
title: Manifest Response Reference (V2)
description: Current-state field reference for the /v2/generate-manifest response format, by layer type
hideBreadcrumbNav: true
keywords:
  - manifest
  - generate-manifest
  - gradient layer
  - fill
  - v2
---

# Manifest Response Reference (V2)

This guide documents the current `/v2/generate-manifest` response schema, layer type by layer type. Unlike the [Manifest Response Migration guide](v1-to-v2/manifest-response-migration.md), this is **not** a V1-to-V2 comparison — it describes the V2 schema as it stands today, independent of what came before. Sections are added as layer types are verified against live manifest output.

## Gradient Layer

A gradient fill layer is returned with `"type": "gradient_layer"`. It carries all the common per-layer fields (`id`, `bounds`/frame data, `blendOptions`, masks, etc. — see [Per-Layer Common Fields](v1-to-v2/manifest-response-migration.md#per-layer-common-fields)) plus a gradient-specific `fill` object.

### Full layer example

```json
{
  "id": 24,
  "name": "Gradient Fill 1",
  "type": "gradient_layer",
  "index": 12,
  "visible": true,
  "protection": ["none"],
  "linked": [],
  "userMask": {
    "density": 100,
    "feather": 0
  },
  "vectorMask": null,
  "proportionalScaling": false,
  "layerSettings": {
    "enabled": true
  },
  "effects": {},
  "pixelMask": null,
  "blendOptions": {
    "opacity": 100,
    "blendMode": "normal",
    "clipped": true,
    "interior": false,
    "fillOpacity": 100,
    "pixelMaskAsGlobalMask": false,
    "vectorMaskAsGlobalMask": false,
    "transparencyShapesLayer": true,
    "knockout": "none",
    "channelRestrictions": [],
    "blendRanges": []
  },
  "compositeFrame": {
    "absolute": { "left": 0, "top": 0, "right": 2100, "bottom": 1500 },
    "relative": { "left": 0, "top": 0, "right": 2100, "bottom": 1500 }
  },
  "referenceFrame": { "left": 0, "top": 0, "right": 0, "bottom": 0 },
  "compositeDimensions": { "left": 0, "top": 0, "right": 2100, "bottom": 1500 },
  "rotation": 0,
  "fill": {
    "type": "linear",
    "align": true,
    "angle": 90,
    "dither": false,
    "reverse": false,
    "scale": 100,
    "gradientAspectRatio": 1,
    "interpolationMethod": "smooth",
    "noisePreSeed": 10012,
    "offset": { "horizontal": 0, "vertical": 0 },
    "gradient": {
      "type": "customStops",
      "value": {
        "gradientName": "Color to Transparent",
        "colorStops": [
          {
            "type": "user_stop",
            "location": 0,
            "midpoint": 50,
            "color": { "mode": "rgb", "depth": 16, "components": [26985, 2858, 2858] }
          },
          {
            "type": "user_stop",
            "location": 4096,
            "midpoint": 50,
            "color": { "mode": "rgb", "depth": 16, "components": [26985, 2858, 2858] }
          }
        ],
        "transparencyStops": [
          { "location": 0, "midpoint": 50, "opacity": 100 },
          { "location": 4096, "midpoint": 50, "opacity": 0 }
        ],
        "interpolation": 4096
      }
    }
  }
}
```

### Common per-layer fields (as seen on this layer)

| Field                   | Type           | Notes                                                                                     |
| ------------------------ | -------------- | ------------------------------------------------------------------------------------------ |
| `id`                    | number         | Unique layer ID                                                                            |
| `name`                  | string         | Layer name as set in Photoshop                                                             |
| `type`                  | string         | Always `"gradient_layer"` for this type                                                   |
| `index`                 | number         | Stacking position                                                                          |
| `visible`               | boolean        | Layer visibility                                                                            |
| `protection`            | array          | e.g. `["none"]`, `["all"]`, `["position"]`                                                |
| `linked`                | array          | Linked layer references                                                                     |
| `userMask`              | object         | `{density, feather}` — user mask state                                                     |
| `vectorMask`            | object or null | `{hasMask, bounds}` when present                                                            |
| `proportionalScaling`   | boolean        | Lock aspect ratio during transform                                                          |
| `layerSettings`         | object         | Rich settings block; `{enabled}` at minimum                                                 |
| `effects`               | object         | Layer effects container (empty object when none applied)                                   |
| `pixelMask`             | object or null | `null` when the layer has no pixel mask                                                    |
| `blendOptions`          | object         | `{opacity, blendMode, clipped, interior, fillOpacity, pixelMaskAsGlobalMask, vectorMaskAsGlobalMask, transparencyShapesLayer, knockout, channelRestrictions, blendRanges}` |
| `compositeFrame`        | object         | `{absolute: {left,top,right,bottom}, relative: {left,top,right,bottom}}`                    |
| `referenceFrame`        | object         | `{left,top,right,bottom}` — untransformed layer content bounds                             |
| `compositeDimensions`   | object         | `{left,top,right,bottom}` — enclosing artboard/document bounds                             |
| `rotation`              | number         | Layer rotation in degrees                                                                   |

### `fill` — gradient-specific fields

| Field                                                      | Type    | Notes                                                                                          |
| ------------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------ |
| `fill.type`                                                | string  | Gradient style, e.g. `"linear"`                                                                |
| `fill.align`                                               | boolean | Aligns gradient with layer bounds                                                               |
| `fill.angle`                                               | number  | Gradient angle in degrees                                                                        |
| `fill.dither`                                              | boolean | Dithering enabled                                                                                |
| `fill.reverse`                                             | boolean | Reverses gradient direction                                                                      |
| `fill.scale`                                               | number  | Gradient scale percentage                                                                        |
| `fill.gradientAspectRatio`                                 | number  | Aspect ratio for angle gradients                                                                 |
| `fill.interpolationMethod`                                 | string  | e.g. `"smooth"`                                                                                 |
| `fill.noisePreSeed`                                        | number  | Seed used for noise gradients                                                                    |
| `fill.offset.horizontal` / `fill.offset.vertical`          | number  | Gradient offset from the layer origin                                                           |
| `fill.gradient.type`                                       | string  | Gradient definition type, e.g. `"customStops"`                                                 |
| `fill.gradient.value.gradientName`                         | string  | Named gradient preset, if any                                                                    |
| `fill.gradient.value.colorStops[]`                         | array   | Color stop list                                                                                  |
| `colorStops[].type`                                        | string  | e.g. `"user_stop"`                                                                              |
| `colorStops[].location`                                    | number  | Stop position (0–4096)                                                                          |
| `colorStops[].midpoint`                                    | number  | Midpoint between adjacent stops (0–100)                                                        |
| `colorStops[].color`                                       | object  | `{mode, depth, components[]}`                                                                   |
| `fill.gradient.value.transparencyStops[]`                  | array   | Opacity stop list                                                                                |
| `transparencyStops[].location` / `.midpoint` / `.opacity`  | number  | Same stop shape as color stops, plus `opacity` (0–100)                                          |
| `fill.gradient.value.interpolation`                        | number  | Gradient interpolation/smoothing value                                                          |

<InlineAlert variant="warning" slots="text"/>

`colorStops[].color` uses a depth-scaled component range rather than named RGB channels: `{"mode": "rgb", "depth": 16, "components": [red, green, blue]}`, where each component is scaled to the given bit depth (e.g. depth `16` → range 0–32768). This matches the color range convention used elsewhere in the V2 API (see font color fields).
