---
title: Layers
description: Add and edit pixel, adjustment, background, and group layers, and apply masks, clipping, blend options, drop shadows, protection, and transforms with Create Composite.
keywords:
  - create composite
  - pixel layers
  - adjustment layers
  - background layer
  - group layers
  - pixel masks
  - drop shadow
  - blend options
hideBreadcrumbNav: true
---

# Layers

Use `POST /v2/create-composite` to add and edit pixel, adjustment,
background, and group layers, and to set the options they share: blend
options, clipping, drop shadows, pixel masks, protection, and transforms.

This page covers what is specific to each layer type and option. For the
fields every layer element uses (`id`, `name`, `operation`, `placement`), see
[Layer Operation Fields](index.md#layer-operation-fields). For other layer
types, see [Text Layers](text-layers.md),
[Solid-Color Layers](solid-color-layers.md), and
[Smart Objects](smart-objects/index.md).

## Before You Start

- Get an access token and client ID; see
  [Authentication](../../getting-started/index.md).
- Prepare signed URLs for inputs and outputs; see
  [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
  Replace each `<...>` placeholder with your own URL.
- To edit an existing layer, find its `id`, `name`, and type with Generate
  Manifest.
- Send each example as `request.json`:

```shell
curl --request POST https://photoshop-api.adobe.io/v2/create-composite \
  --header "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  --header "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  --header "Content-Type: application/json" \
  --data @request.json
```

A `202` response returns a job; poll [Get Job Status](../get-job-status/index.md)
until it is `succeeded`, then open the outputs.

## Operations By Layer Type

| `type` | Add | Edit | Delete | Move |
|---|---|---|---|---|
| `adjustment_layer` | Yes; `adjustments` required | Yes; send only the values to change | Yes | Yes |
| `background_layer` | Yes; sets the document background | Yes; replace pixels, hide, or convert to a layer | Convert to a layer first, then delete it | No; rejected before a job starts |
| `group_layer` | No; not supported | Yes; no `isClipped` | Yes; `shouldIncludeChildren` removes or keeps contents | Yes; `shouldIncludeChildren` moves or leaves contents |
| `layer` | Yes; `image` required | Yes; `image` replaces the pixels | Yes | Yes |

Delete and move use the same fields for every type; see
[Operation Fields](index.md#operation-fields).

Fields each type accepts on add and edit:

| Field | `adjustment_layer` | `background_layer` | `group_layer` | `layer` |
|---|---|---|---|---|
| `blendOptions` | Yes | No | Yes | Yes |
| `isClipped` | Yes | No | No | Yes |
| `isVisible` | Yes | Yes | Yes | Yes |
| `layerEffects` | Yes | No | Yes; see [Layer Effects](#layer-effects) | Yes |
| `pixelMask` | Yes | No | Yes | Yes |
| `protection` | Yes | No | Yes; applies to contents | Yes |
| `transform` | No | No | Accepted, not applied | Yes, with `transformMode: custom` |
| `transformMode` | `none` only | No | Accepted, not applied | Yes |

In the `Default` column, `—` means no default is documented for an optional
field, or that a required field must be supplied. A value marked “on add”
applies only to a new layer. On edit, omitted fields keep their current
values where the table says so.

## Add A Pixel Layer

This request adds one image as a pixel layer at the top of an existing
document and explicitly fits it to the canvas:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Logo",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "transformMode": "fit",
        "image": { "source": { "url": "<LOGO_PNG_GET_URL>" } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

## Adjustment Layers

An adjustment layer changes the colors of the layers below it without
changing their pixels. Each adjustment layer has one adjustment type.

### Add A Brightness/Contrast Layer

This request adds `Brighten` above `Hero Photo`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Brighten",
        "operation": {
          "type": "add",
          "placement": { "type": "above", "referenceLayer": { "name": "Hero Photo" } }
        },
        "adjustments": {
          "type": "brightness_contrast",
          "brightnessContrast": { "brightness": 40, "contrast": 15 }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: the PSD has a Brightness/Contrast layer named `Brighten` with
brightness `40` and contrast `15`, and every visible layer below it is
brighter in the PNG. A new adjustment layer gets an empty (white) mask.

### Adjustments Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `adjustments` | object | On add | — | One adjustment. |
| `adjustments.brightnessContrast` | object | When `type` is `brightness_contrast` | — | See [Brightness/Contrast](#brightnesscontrast). |
| `adjustments.colorBalance` | object | When `type` is `color_balance` | — | See [Color Balance](#color-balance). |
| `adjustments.exposure` | object | When `type` is `exposure` | — | See [Exposure](#exposure). |
| `adjustments.hueSaturation` | object | When `type` is `hue_saturation` | — | See [Hue/Saturation](#huesaturation). |
| `adjustments.type` | string | Yes | — | `brightness_contrast`, `color_balance`, `exposure`, or `hue_saturation`. On edit, use the existing layer's adjustment. |

An adjustment layer cannot be transformed: omit `transform`, and omit
`transformMode` or set it to `none`.

### Brightness/Contrast

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `brightness` | integer | No | `0` | −150 to 150. Positive values brighten. |
| `contrast` | integer | No | `0` | −150 to 150. Positive values increase contrast. |

### Color Balance

Each level array has exactly three integers from −100 to 100, in this order:

| Index | Negative Value Shifts Toward | Positive Value Shifts Toward |
|---|---|---|
| 0 | Cyan | Red |
| 1 | Magenta | Green |
| 2 | Yellow | Blue |

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `highlightLevels` | array of 3 integers | No | `[0, 0, 0]` | Shift for highlights. |
| `midtoneLevels` | array of 3 integers | No | `[0, 0, 0]` | Shift for midtones. |
| `preserveLuminosity` | boolean | No | `true` | `true` keeps each pixel's brightness while shifting color. |
| `shadowLevels` | array of 3 integers | No | `[0, 0, 0]` | Shift for shadows. |

This request warms the image by moving midtones toward red and yellow and
highlights slightly toward red:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Warm Tone",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "adjustments": {
          "type": "color_balance",
          "colorBalance": {
            "highlightLevels": [10, 0, 0],
            "midtoneLevels": [25, 0, -20],
            "preserveLuminosity": true,
            "shadowLevels": [0, 0, 0]
          }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: a Color Balance layer named `Warm Tone` at the top of the stack,
with midtones `+25, 0, −20` and highlights `+10, 0, 0`.

### Exposure

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `exposureValue` | number | No | `0` | −20 to 20 stops. Positive values brighten highlights. |
| `gammaCorrection` | number | No | `1.0` | 0.01 to 9.99. Below `1` brightens midtones; above `1` darkens them. |
| `offset` | number | No | `0` | −0.5 to 0.5. Positive values lift shadows and midtones. |

This request edits the existing exposure layer `Exposure 1` and changes only
`exposureValue`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Exposure 1",
        "operation": { "type": "edit" },
        "adjustments": {
          "type": "exposure",
          "exposure": { "exposureValue": 1.5 }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: `Exposure 1` has exposure `+1.5`. On edit, omitted adjustment values
keep their current values.

### Hue/Saturation

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `colorize` | boolean | No | `false` | `true` tints the image with one hue. |
| `hueSaturationAdjustments` | array of [Hue/Saturation Adjustment](#huesaturation-adjustment) | Yes | — | At least one entry. Use one entry without `localRange` for all colors, and one entry per color range. |

#### Hue/Saturation Adjustment

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `hue` | integer | No | `0` | −180 to 180 degrees; with `colorize`, 0 to 360. |
| `lightness` | integer | No | `0` | −100 to 100; with `colorize`, 0 to 100. |
| `localRange` | [Local Range](#local-range) | No | — | Limits the entry to one color range. Not allowed with `colorize: true`. Omit for the all-colors entry. |
| `saturation` | integer | No | `0` | −100 to 100; with `colorize`, 0 to 100. |

#### Local Range

Positions are degrees on the color wheel (0 to 360). The entry applies fully
between `beginSustain` and `endSustain` and fades out toward `beginRamp` and
`endRamp`.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `beginRamp` | integer | No | — | 0 to 360. Where the fade-in starts. |
| `beginSustain` | integer | No | — | 0 to 360. Where the full effect starts. |
| `channelId` | string | Yes | `REDS` | `REDS`, `YELLOWS`, `GREENS`, `CYANS`, `BLUES`, or `MAGENTAS`. Uppercase. |
| `endRamp` | integer | No | — | 0 to 360. Where the fade-out ends. |
| `endSustain` | integer | No | — | 0 to 360. Where the full effect ends. |

This request lowers saturation for all colors by `10` and makes blues more
saturated and darker:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Deep Sky",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "adjustments": {
          "type": "hue_saturation",
          "hueSaturation": {
            "colorize": false,
            "hueSaturationAdjustments": [
              { "hue": 0, "saturation": -10, "lightness": 0 },
              {
                "hue": 0,
                "saturation": 35,
                "lightness": -15,
                "localRange": { "channelId": "BLUES", "beginRamp": 195, "beginSustain": 225, "endSustain": 255, "endRamp": 285 }
              }
            ]
          }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: blue areas such as sky are deeper and richer; other colors are
slightly muted.

This request adds a hue/saturation adjustment layer configured as a sepia tint:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "adjustment_layer",
        "name": "Sepia",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "adjustments": {
          "type": "hue_saturation",
          "hueSaturation": {
            "colorize": true,
            "hueSaturationAdjustments": [{ "hue": 35, "saturation": 25, "lightness": 0 }]
          }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

The request uses hue `35`, saturation `25`, and lightness `0` for the sepia tint.

## Background Layers

A document has at most one background layer, always at the bottom. It
cannot be moved, transformed, masked, blended, styled, or protected; convert
it to a layer first.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `convertedLayerName` | string | No | — | Edit only. Name for the converted layer; use it to select the layer in later elements. |
| `convertToLayer` | boolean | No | `false` | Edit only. `true` turns the background into a pixel layer. Cannot be combined with `image`. |
| `image` | object | No | — | New background pixels. Contains `source`, a file reference; see [Input Files And Storage](../shared-reference/input-files-and-storage.md). |
| `isVisible` | boolean | No | `true` | `false` hides the background. In a document that has only a background, also send `convertToLayer: true`. |

### Replace The Background

This request replaces the background pixels with a new image:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "name": "Background",
        "operation": { "type": "edit" },
        "image": { "source": { "url": "<NEW_BACKGROUND_JPG_GET_URL>" } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: the background shows the new image; other layers are unchanged.
With `"operation": { "type": "add" }` and no `name`, the same element sets
the document background. An `add` without `image` leaves the background
unchanged.

### Convert The Background To A Layer

This request converts the background, names it `Base Photo`, and sets that
layer to 80% opacity:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "background_layer",
        "name": "Background",
        "operation": { "type": "edit" },
        "convertToLayer": true,
        "convertedLayerName": "Base Photo"
      },
      {
        "type": "layer",
        "name": "Base Photo",
        "operation": { "type": "edit" },
        "blendOptions": { "opacity": 80 }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: the document has no background; the bottom layer is the pixel layer
`Base Photo` at 80% opacity. It can now be moved, masked, or deleted.

## Blend Options

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `blendOptions.blendMode` | string | No | `normal` on add | How the layer mixes with the layers below; see the table below. |
| `blendOptions.opacity` | integer | No | `100` on add | 0 (transparent) to 100 (opaque). |

On edit, omitted values keep their current values.

| Group | `blendMode` values |
|---|---|
| Normal | `normal`, `dissolve` |
| Darken | `darken`, `multiply`, `color_burn`, `linear_burn`, `darker_color` |
| Lighten | `lighten`, `screen`, `color_dodge`, `linear_dodge`, `lighter_color` |
| Contrast | `overlay`, `soft_light`, `hard_light`, `vivid_light`, `pin_light`, `hard_mix` |
| Comparative | `difference`, `exclusion`, `divide` |
| Color | `hue`, `saturation`, `color`, `luminosity` |

This request sets `Shadow Overlay` to Multiply at 60% opacity:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Shadow Overlay",
        "operation": { "type": "edit" },
        "blendOptions": { "blendMode": "multiply", "opacity": 60 }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: `Shadow Overlay` darkens the layers below it and is 40% see-through.

## Clipping Masks

Set `isClipped: true` to show a layer only where the layer directly below it
has content. `false`, the default on add, removes clipping. Groups ignore
`isClipped`. To clip a background, convert it first with `convertToLayer`.

This request adds a texture above `Headline Shape` and clips it to that
shape:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Gold Texture",
        "operation": {
          "type": "add",
          "placement": { "type": "above", "referenceLayer": { "name": "Headline Shape" } }
        },
        "image": { "source": { "url": "<TEXTURE_PNG_GET_URL>" } },
        "transformMode": "fill",
        "isClipped": true
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: the texture covers the canvas but is visible only inside
`Headline Shape`.

## Group Layers

You can edit, delete, and move existing groups, and add layers into them.
Adding a group isn't supported.

- `protection` on a group also applies to every layer inside it.
- `isVisible`, `blendOptions`, and `pixelMask` apply to the group as a whole.
- `transform` is accepted but not applied; transform the layers inside it.
- To add a layer inside a group, use placement `into` with the group as
  `referenceLayer`.
- With `id`, `name` renames the group.

This request renames group `12` to `Spring Promo`, sets it to 75% opacity,
and adds a logo inside it:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "group_layer",
        "id": 12,
        "name": "Spring Promo",
        "operation": { "type": "edit" },
        "blendOptions": { "opacity": 75 }
      },
      {
        "type": "layer",
        "name": "Logo",
        "operation": {
          "type": "add",
          "placement": { "type": "into", "referenceLayer": { "id": 12 } }
        },
        "image": { "source": { "url": "<LOGO_PNG_GET_URL>" } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: group `12` is named `Spring Promo`, is 75% opaque, and contains
`Logo`. To move or delete a group with or without its contents, see
[Reorder And Remove Layers](index.md#reorder-and-remove-layers).

## Layer Effects

`layerEffects` adds layer styles. Drop shadow is the only supported effect.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `layerEffects.dropShadow` | array of [Drop Shadow](#drop-shadow) | Yes, if `layerEffects` is sent | — | 1 to 10 drop shadows. |

A drop shadow on a group is accepted but may not render; apply it to the
layers inside the group.

### Drop Shadow

Omitted fields use the default drop-shadow setting; set every value you
want to control.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `angle` | integer | No | — | −180 to 180 degrees. Direction of the light; `90` lights from the top, so the shadow falls below. |
| `antiAliased` | boolean | No | — | `true` smooths the contour. |
| `blendMode` | string | No | — | Any [blend mode](#blend-options), usually `multiply`. |
| `color` | [Effect Color](#effect-color) | No | — | Shadow color. |
| `contour` | [Contour](#contour) | No | Linear | Shape of the shadow fade. |
| `distance` | integer | No | — | 0 to 30000 pixels. How far the shadow is offset. |
| `enabled` | boolean | No | — | `false` keeps the shadow but hides it. |
| `layerKnocksOut` | boolean | No | — | `true` hides the shadow under semi-transparent parts of the layer. |
| `noise` | integer | No | — | 0 to 100 percent. Adds grain. |
| `opacity` | integer | No | — | 0 to 100 percent. |
| `size` | integer | No | — | 0 to 250 pixels. Blur radius. |
| `spread` | integer | No | — | 0 to 100 percent. Hardens the edge before blurring. |
| `useGlobalLight` | boolean | No | — | `true` uses the document's global light angle instead of `angle`. |

#### Effect Color

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `rgb` | object | Yes | — | Red, green, and blue channels. |
| `rgb.blue` | integer | Yes | — | 0 to 255. |
| `rgb.green` | integer | Yes | — | 0 to 255. |
| `rgb.red` | integer | Yes | — | 0 to 255. |

To use a hex color, convert each pair of digits to decimal: `#1A2B3C` is
`red` 26, `green` 43, `blue` 60.

#### Contour

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `curve` | array of [Curve Point](#curve-point) | Yes | — | 2 to 16 points, ordered by `horizontal`. Other counts render a linear contour. |
| `name` | string | Yes | — | `Custom`. |

#### Curve Point

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `continuity` | boolean | Yes | — | `true` for a smooth point; `false` for a corner. |
| `horizontal` | number | Yes | — | 0 to 255. Input position across the shadow. |
| `vertical` | number | Yes | — | 0 to 255. Output opacity at that position. |

This request adds a soft navy shadow below and to the right of `Product`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Product",
        "operation": { "type": "edit" },
        "layerEffects": {
          "dropShadow": [
            {
              "angle": 135,
              "antiAliased": true,
              "blendMode": "multiply",
              "color": { "rgb": { "red": 26, "green": 43, "blue": 60 } },
              "contour": {
                "name": "Custom",
                "curve": [
                  { "horizontal": 0, "vertical": 0, "continuity": false },
                  { "horizontal": 128, "vertical": 96, "continuity": true },
                  { "horizontal": 255, "vertical": 255, "continuity": false }
                ]
              },
              "distance": 12,
              "enabled": true,
              "layerKnocksOut": true,
              "noise": 0,
              "opacity": 55,
              "size": 18,
              "spread": 5,
              "useGlobalLight": false
            }
          ]
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

The request specifies a navy (`#1A2B3C`) drop shadow with 55% opacity, a
12-pixel offset, and an 18-pixel size.

## Pixel Layers

A pixel layer (`type: layer`) holds image pixels from a file.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `image` | object | On add | — | Contains `source`, a file reference; see [Input Files And Storage](../shared-reference/input-files-and-storage.md). On edit, replaces the layer's pixels. |
| `transform` | [Transform](#transform) | No | — | Requires `transformMode: custom`. |
| `transformMode` | string | No | `none` | How the image is sized; see [Transforms](#transforms). |

### Size And Position A Pixel Layer

This request places a 400 × 400 pixel logo with its top-left corner at
(40, 40):

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Logo",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "image": { "source": { "url": "<LOGO_PNG_GET_URL>" } },
        "transformMode": "custom",
        "transform": {
          "dimension": { "width": 400, "height": 400 },
          "offset": { "horizontal": 40, "vertical": 40 }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: a pixel layer `Logo` at the top of the stack, 400 × 400 pixels,
40 pixels from the left and top edges.

### Replace Layer Pixels

This request replaces the pixels of `Hero Photo` and requests a fill transform:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Hero Photo",
        "operation": { "type": "edit" },
        "image": { "source": { "url": "<NEW_PHOTO_JPG_GET_URL>" } },
        "transformMode": "fill"
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

The request retains `Hero Photo`'s name and stack position and asks to fill the
canvas. The target must be a pixel layer; otherwise the job fails.

## Pixel Masks

A pixel mask hides parts of a layer. The mask is a grayscale image: white
shows the layer, black hides it, and gray partly hides it.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `pixelMask.delete` | boolean | No | `false` | Edit only. `true` removes the mask; other mask fields are ignored. Fails if the layer has no mask. Do not send `null`. |
| `pixelMask.isEnabled` | boolean | No | `true` on add | `false` keeps the mask but turns it off. |
| `pixelMask.isLinked` | boolean | No | `true` on add | `true` moves the mask with the layer. |
| `pixelMask.offset` | object | No | `{ "horizontal": 0, "vertical": 0 }` on add | Moves the mask relative to the layer. |
| `pixelMask.offset.horizontal` | integer | No | `0` | Pixels; positive moves right. |
| `pixelMask.offset.vertical` | integer | No | `0` | Pixels; positive moves down. |
| `pixelMask.source` | object | No | — | The mask image, a file reference; see [Input Files And Storage](../shared-reference/input-files-and-storage.md). On edit, replaces the mask. |

This request adds a photo with a vignette mask:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Portrait",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "image": { "source": { "url": "<PORTRAIT_JPG_GET_URL>" } },
        "pixelMask": {
          "source": { "url": "<VIGNETTE_MASK_PSD_GET_URL>" },
          "isEnabled": true,
          "isLinked": true
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: `Portrait` is visible where the mask is white and fades out where it
is black.

This request moves the mask of `Portrait` 30 pixels right and removes the
mask from `Banner`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Portrait",
        "operation": { "type": "edit" },
        "pixelMask": { "offset": { "horizontal": 30, "vertical": 0 } }
      },
      {
        "type": "layer",
        "name": "Banner",
        "operation": { "type": "edit" },
        "pixelMask": { "delete": true }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: the visible area of `Portrait` shifts 30 pixels right; `Banner` has
no mask and is fully visible.

## Protection

`protection` locks parts of a layer. It is applied after every other change
in the same element.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `protection` | array of strings | No | — | Values from the table below. On edit, omit it or send `[]` to keep the current locks. |

| Value | Locks |
|---|---|
| `all` | Everything. Must be the only value. |
| `artboard_autonest` | Moving the layer into or out of artboards. |
| `composite` | Painting on the layer's pixels. |
| `none` | Nothing; removes all locks. Must be the only value. |
| `position` | The layer's position. |
| `transparency` | Transparent pixels. |

This request locks the position and transparency of `Logo` and unlocks
`Hero Photo`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Logo",
        "operation": { "type": "edit" },
        "protection": ["position", "transparency"]
      },
      {
        "type": "layer",
        "name": "Hero Photo",
        "operation": { "type": "edit" },
        "protection": ["none"]
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Result: in the PSD, `Logo` shows the position and transparency locks;
`Hero Photo` has none.

## Transforms

`transformMode` sets how a pixel layer is sized and placed:

| `transformMode` | Result |
|---|---|
| `custom` | Applies `transform`. Without `transform`, nothing changes. |
| `fill` | Requests scale-to-cover placement from the top left while preserving aspect ratio. |
| `fit` | Scales the image to fit inside the canvas, keeping its aspect ratio, from the top-left corner. |
| `none` | Keeps the image's size. Default on edit. |

### Transform

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `anchor` | object | No | Document origin | Pivot for `angle`, `dimension`, and `skew`. |
| `anchor.horizontal` | number | Yes | — | Pivot x position in pixels. |
| `anchor.vertical` | number | Yes | — | Pivot y position in pixels. |
| `angle` | number | No | — | Rotation in degrees. |
| `dimension` | object | No | — | New layer size. |
| `dimension.height` | integer | No | — | 0 to 32000. |
| `dimension.unit` | string | No | `pixels_unit` | `pixels_unit` or `points_unit`. |
| `dimension.width` | integer | No | — | 0 to 32000. |
| `horizontalAlign` | string | No | — | `left`, `center`, or `right` of the canvas. Ignored when `offset` is set. |
| `offset` | object | No | — | Position of the layer's top-left corner. Overrides alignment. |
| `offset.horizontal` | integer | No | — | Pixels from the left edge of the canvas. |
| `offset.vertical` | integer | No | — | Pixels from the top edge of the canvas. |
| `skew` | object | No | — | Slant. |
| `skew.horizontal` | integer | Yes | — | Horizontal slant in degrees. |
| `skew.vertical` | integer | Yes | — | Vertical slant in degrees. |
| `verticalAlign` | string | No | — | `top`, `center`, or `bottom` of the canvas. Ignored when `offset` is set. |

Without `offset` or alignment, a resized, rotated, or skewed layer keeps its
top-left corner where it was.

This request rotates `Badge` by 15 degrees and centers it on the canvas:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "layer",
        "name": "Badge",
        "operation": { "type": "edit" },
        "transformMode": "custom",
        "transform": {
          "angle": 15,
          "horizontalAlign": "center",
          "verticalAlign": "center"
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Result: `Badge` is rotated 15 degrees and its bounding box is centered on the
canvas.

## Errors

Requests that fail validation are rejected before a job starts:

| `message` example | Fix |
|---|---|
| `adjustments is required when adding an adjustment layer` | Add `adjustments`. |
| `background_layer does not support operation type: move` | Convert the background to a layer, then move it. |
| `blendOptions is not applicable for background_layer` | Convert the background to a layer first. The same applies to `transform`, `transformMode`, `protection`, `pixelMask`, and `layerEffects`. |
| `image and convertToLayer are mutually exclusive for background_layer` | Replace pixels and convert in separate elements. |
| `image is required for image layers` | Add `image` when adding a `layer`. |
| `layerEffects must contain at least one effect` | Add `dropShadow` or remove `layerEffects`. |
| `transform is not applicable for adjustment_layer` | Remove `transform` and any `transformMode` other than `none`. |
| `transform is only applicable when transformMode is custom` | Add `"transformMode": "custom"`. |

Values outside a field's range are also rejected. Accepted jobs can still
fail; the job status then contains `errorDetails`. See
[Errors And Limits](../errors-and-limits/index.md).

| Symptom | Fix |
|---|---|
| A background edit asks to convert to a layer | Add `"convertToLayer": true`. |
| A job fails and the request adds a `group_layer` | Adding a group isn't supported; add layers into an existing group instead. |
| Deleting a mask fails | The layer has no mask; remove `"delete": true`. |
| Replacing pixels fails because the layer is not an image layer | Use the edit for that layer's type, such as `fill` for a solid-color layer. |

## Related Pages

- [Create Composite Overview](index.md)
- [Text Layers](text-layers.md)
- [Solid-Color Layers](solid-color-layers.md)
- [Smart Objects](smart-objects/index.md)
- [Input Files And Storage](../shared-reference/input-files-and-storage.md)
- [Output Formats And Options](../shared-reference/output-formats-and-options.md)
- [Get Job Status](../get-job-status/index.md)
- [API Reference](../../api/photoshop-v2/index.md)
