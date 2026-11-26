---
title: Add, Edit, And Delete Solid-Color Layers
description: Add, recolor, and delete solid-color layers with the Create Composite API.
keywords:
  - create composite
  - solid-color layers
  - fill color
  - RGB
hideBreadcrumbNav: true
---

# Add, Edit, And Delete Solid-Color Layers

Use `POST /v2/create-composite` to add a solid-color layer to a Photoshop
document, change its color, or delete it. Request a PSD to retain editable
layers and a PNG to preview the flattened result.

## Before You Start

- Get an access token and client ID; see [Authentication](../../getting-started/index.md).
- Prepare signed URLs for reading and writing files; see
  [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
  Replace each `<...>` placeholder in the requests with your own URL.
- For an existing PSD, use Generate Manifest to find the layer's `id` or
  `name`. When selecting by name, use a unique name.

## Add A Solid-Color Layer

This request adds a red layer named `Backdrop` to a new 100 × 100 pixel
document and saves the editable PSD. The document fill is omitted, so it uses
the default transparent fill. Save the request as `request.json`:

```json
{
  "image": { "width": 100, "height": 100 },
  "edits": {
    "layers": [
      {
        "type": "solid_color_layer",
        "name": "Backdrop",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "fill": { "solidColor": { "rgb": { "red": 255, "green": 0, "blue": 0 } } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<NEW_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Send the request:

```shell
curl --request POST https://photoshop-api.adobe.io/v2/create-composite \
  --header "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  --header "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  --header "Content-Type: application/json" \
  --data @request.json
```

The response contains a `statusUrl`. Poll it until the job succeeds before
reading the output files; acceptance alone does not mean processing succeeded.
See [Get Job Status](../get-job-status/index.md).

## Request Fields

The tables describe the fields used in this guide. For other document and
layer options, see the [API Reference](../../api/photoshop-v2/index.md).

| Property | Type | Required | Default / Omission | Use |
|---|---|---|---|---|
| `image` | object | Yes | — | Defines a new document with `width`, `height`, and `fill`, or an existing file with `source`. |
| `image.width`, `image.height` | integer | No | `100` each | Dimensions of the new document, from 1 to 32,000 pixels. |
| `image.unit` | string | No | `pixels_unit` | Unit for new-document dimensions. |
| `image.fill` | string | No | `transparent` | Background fill for a new document: `white`, `background_color`, or `transparent`. |
| `image.source` | object | For an existing file | — | Contains `url`. Use this instead of blank-document dimensions. |
| `image.source.url` | string | Yes for this input form | — | Signed URL for reading the input PSD. |
| `edits` | object | No | — | Contains `layers`; omit it to make no edits. |
| `edits.layers` | array of objects | No | — | Layer operations, applied in array order. Each element uses the fields below. |
| `outputs` | array of objects | Yes | — | Supply 1 to 25 output objects. |
| `outputs[].destination` | object | Yes | — | Contains `url` for the output location used in these examples. |
| `outputs[].destination.url` | string | Yes for this destination form | — | Signed URL for writing the output file. |
| `outputs[].mediaType` | string | No | `image/jpeg` | Use `image/vnd.adobe.photoshop` for a PSD or `image/png` for a PNG. |

### Layer Operation Fields

| Property | Type | Required | Default / Omission | Use |
|---|---|---|---|---|
| `type` | string | For add and edit | — | Set to `solid_color_layer`. Omit for a delete. |
| `name` | string | `id` or `name` for edit/delete | — | Names a new layer, or identifies an existing layer by name. |
| `id` | integer | `id` or `name` for edit/delete | — | Identifies an existing layer by ID. |
| `operation` | object | Yes | — | Contains `type` and, for an add, `placement`. |
| `operation.type` | string | Yes | — | Use `add`, `edit`, or `delete`. |
| `operation.placement` | object | For an add | — | Contains `type` and, when needed, `referenceLayer`. |
| `operation.placement.type` | string | No | `top` | Use `top`, `bottom`, `above`, `below`, or `into`. |
| `operation.placement.referenceLayer` | object | For `above`, `below`, or `into` | — | Identify the reference with exactly one `id` (integer) or `name` (string). For `into`, the reference must be a group. |
| `fill` | object | For add; optional for edit | No default on add; omit on edit to keep the color | Contains `solidColor`; see [Solid-Color Fields](#solid-color-fields). |
| `isVisible` | boolean | No | `true` on add; omit on edit to keep the current value | `false` hides the layer. |
| `blendOptions` | object | No | — | Contains `opacity` and may contain `blendMode`; see the API Reference for blend modes. |
| `blendOptions.opacity` | integer | No | `100` on add; omit on edit to keep the current value | Layer opacity from 0 to 100. |

In the `Default / Omission` column, `—` means no default is documented for
an optional field, or that a required value must be supplied.

An opaque solid-color layer at the top can cover layers below it. Choose a
different placement, or use `blendOptions` such as `{"opacity": 50}` to
make the layers below visible through it.

## Choose A Color

For a solid-color layer, set `fill.solidColor.rgb` to red, green, and blue
components. Each is an integer from 0 to 255: `0` is no intensity and `255`
is full intensity. Supply all three components, even when one is zero.

### Solid-Color Fields

| Property | Type | Default / Omission | Use |
|---|---|---|---|
| `fill.solidColor` | object | Required; no default | Include it when setting a color. |
| `fill.solidColor.rgb` | object | Required; no default | Contains `red`, `green`, and `blue`. |
| `fill.solidColor.rgb.red` | integer | `0` when omitted | Red component, 0 to 255. |
| `fill.solidColor.rgb.green` | integer | `0` when omitted | Green component, 0 to 255. |
| `fill.solidColor.rgb.blue` | integer | `0` when omitted | Blue component, 0 to 255. |

An omitted RGB component defaults to `0`; it does not preserve the previous
component when changing a color. To keep the current color while changing
another layer property, omit `fill` altogether. Do not send an empty `fill`
when changing a color.

For example, the hexadecimal color `#E8462B` is red `E8` = 232, green `46`
= 70, and blue `2B` = 43. Send those three numbers as in the add request;
do not send the hexadecimal string as `rgb`.

| Color | `red` | `green` | `blue` |
|---|---:|---:|---:|
| Black | 0 | 0 | 0 |
| Blue | 0 | 0 | 255 |
| White | 255 | 255 | 255 |

## Add A Full-Size Color Layer

This larger example adds the orange-red `#E8462B` color to a white 1200 × 600
document, then writes a PSD and PNG preview:

```json
{
  "image": { "width": 1200, "height": 600, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "solid_color_layer",
        "name": "Backdrop",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "fill": { "solidColor": { "rgb": { "red": 232, "green": 70, "blue": 43 } } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<BANNER_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<BANNER_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

The example uses the explicit `top` placement; omitting the placement type
uses the documented default shown above.

Solid-color fills use the `rgb` object shown here. CMYK, Lab, HSB, and
grayscale objects are not supported for `fill.solidColor`; convert those
colors to RGB before sending the request. This is separate from the document's
color mode and from color fields used by other layer types.

## Edit A Solid-Color Layer

Use the PSD from the add request as the input. This request finds `Backdrop`
by name and changes its RGB color to blue. Replace `<SOURCE_PSD_GET_URL>` with
a read URL for that PSD, and provide new output URLs:

```json
{
  "image": { "source": { "url": "<SOURCE_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "solid_color_layer",
        "name": "Backdrop",
        "operation": { "type": "edit" },
        "fill": {
          "solidColor": {
            "rgb": { "red": 32, "green": 112, "blue": 208 }
          }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<EDITED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<EDITED_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

To select by ID instead, replace `name` with the layer's integer `id`.
Submit and poll this request the same way as the add request.

## Delete A Solid-Color Layer

Use the edited PSD as the input. Send the layer identifier and a `delete`
operation; omit the layer `type` and `fill`. After the layer is removed in
this sequence, the original transparent area is visible again.

```json
{
  "image": { "source": { "url": "<EDITED_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "name": "Backdrop",
        "operation": { "type": "delete" }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<FINAL_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<FINAL_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

Submit and poll the request as above. To delete by ID, replace `name` with
the layer's integer `id`.

## Troubleshooting

- **The color is unexpected:** Check all three RGB components and use values
  from 0 to 255. An omitted component becomes `0`.
- **Other content is hidden:** Check the layer's placement and opacity; a
  visible, opaque fill at the top can cover content underneath.
- **The layer cannot be found:** Generate a manifest for the input PSD and
  use the layer's `id` or unique `name`.
- **The request was accepted but no output is available:** Check the job
  status and error details before reading the destination.
