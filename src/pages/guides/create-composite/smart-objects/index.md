---
title: Add, Edit, And Delete Smart Objects
description: Add Smart Object layers and replace their contents in a Photoshop document.
keywords:
  - create composite
  - smart objects
  - linked smart objects
  - replace content
hideBreadcrumbNav: true
---

# Add, Edit, And Delete Smart Objects

Use `POST /v2/create-composite` to add a Smart Object layer, replace its
contents, or delete it. Request a PSD to retain the layer for later edits and
a PNG to preview the result.

## Before You Start

- Get an access token and client ID; see [Authentication](../../../getting-started/index.md).
- Prepare signed URLs for the files you read and write; see
  [Storage Solutions](https://developer.adobe.com/firefly-services/docs/photoshop/getting-started/storage-solutions/).
  Replace the placeholders below with your own URLs.
- To edit or delete an existing layer, obtain its `name` or `id` from a
  Generate Manifest response. See the
  [Generate Manifest request](../../../getting-started/index.md#3-submit-a-request).

## Add An Embedded Smart Object

This request adds a 128 × 128 pixel PNG as an embedded Smart Object named
`Product Artwork` and saves the editable PSD. The source image is already the
same size as the canvas, and the request sets `transformMode` explicitly.

```shell
curl --request POST https://photoshop-api.adobe.io/v2/create-composite \
  --header "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  --header "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  --header "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "image": { "width": 128, "height": 128, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "smart_object_layer",
        "name": "Product Artwork",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "smartObject": {
          "smartObjectFile": { "source": { "url": "<SMART_OBJECT_GET_URL>" } }
        },
        "transformMode": "none"
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
JSON
```

### Document, Layers, And Output Fields

The request above creates a blank document. To start with an existing PSD
instead, replace the `image` object with the value shown here:

```json
{ "source": { "url": "<PSD_GET_URL>" } }
```

The following fields describe the request forms used in this guide:

| Property | Type | Required | Default / Omission | Use |
|---|---|---|---|---|
| `image` | object | Yes | — | Defines a blank document or identifies an existing file. |
| `image.width` | integer | No | `100` | Blank-document width in the selected unit, from 1 to 32,000. |
| `image.height` | integer | No | `100` | Blank-document height in the selected unit, from 1 to 32,000. |
| `image.unit` | string | No | `pixels_unit` | Blank-document dimension unit; `pixels_unit` or `points_unit`. |
| `image.resolution` | object | No | 72 pixels per inch | Document resolution. |
| `image.resolution.value` | integer | Yes in `resolution` | — | Resolution in pixels per inch, at least 1. |
| `image.resolution.unit` | string | No | `density_unit` | Resolution unit. |
| `image.fill` | string | No | `transparent` | Blank-document fill: `white`, `background_color`, or `transparent`. |
| `image.source` | object | For an existing document | — | Contains the file's `url`. |
| `image.source.url` | string | Yes for this input form | — | Signed HTTPS URL for reading the PSD. |
| `edits` | object | No | — | Contains the layer changes. |
| `edits.layers` | array of objects | No | — | Each element is a layer operation, applied in array order. See [Layer Operations](#layer-operations). |
| `outputs` | array of objects | Yes | — | Supply 1 to 25 output objects. |
| `outputs[].destination` | object | Yes for each output | — | Destination for the output file. |
| `outputs[].destination.url` | string | Yes for this destination form | — | Signed HTTPS URL for writing the output file. |
| `outputs[].maxWidth` | integer | No | — | Non-negative maximum width in pixels. A value of `0` means no maximum. |
| `outputs[].mediaType` | string | No | `image/jpeg` | Use `image/vnd.adobe.photoshop` for a PSD or `image/png` for a PNG. |
| `outputs[].width` | integer | No | — | Non-negative target width in pixels. A value of `0` means no explicit target width. |

In the `Default / Omission` column, `—` means no default is documented for
an optional field, or that a required value must be supplied.

With `points_unit`, dimensions are converted to pixels using the document
resolution and rounded to the nearest pixel. For example, 100 points at
144 pixels per inch becomes 200 pixels. Each converted dimension must be at
most 32,000 pixels.

The PSD keeps the layer. The explicit-size example below also writes a PNG
preview.

The response contains a `statusUrl`. Poll it until the job succeeds before
reading the files at the output locations. See [Get Job Status](../../get-job-status/index.md).
A successful submission alone does not mean that processing succeeded.

## Set An Explicit Smart Object Size

When you need to set the added layer's dimensions explicitly, use
`transformMode: "custom"` and provide both dimensions:

```json
{
  "image": { "width": 128, "height": 128, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "smart_object_layer",
        "name": "Product Artwork",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "smartObject": {
          "isLinked": false,
          "smartObjectFile": { "source": { "url": "<SMART_OBJECT_GET_URL>" } }
        },
        "transformMode": "custom",
        "transform": { "dimension": { "width": 128, "height": 128 } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

For a 128 × 128 solid red PNG as the source, this request produces a red PNG
preview and a PSD with the named layer.

## Layer Operations

These properties describe each Smart Object operation in `edits.layers`:

| Property | Type | Required | Default / Omission | Use |
|---|---|---|---|---|
| `id` | integer | `id` or `name` for edit/delete | — | Identifies an existing layer. |
| `name` | string | `id` or `name` for edit/delete | — | Names a new layer or identifies an existing one. Use a unique name when selecting by name. |
| `operation` | object | Yes | — | Its `type` is `add`, `edit`, or `delete` in this guide. An add also contains `placement`; see [Layer Placement](#layer-placement). |
| `smartObject` | object | For add; optional for edit | — | Contains the file and link settings described in [Smart Object Fields](#smart-object-fields). Omit it for a delete. |
| `transform` | object | No | — | The pixel-sizing example uses its `dimension` object; see [Size A Smart Object](#size-a-smart-object). |
| `transformMode` | string | No | Set explicitly | Controls layer sizing; see [Size A Smart Object](#size-a-smart-object). |
| `type` | string | For add and edit | — | Set to `smart_object_layer`. Omit it for delete. |

For an edit or delete, supply a layer `id` or a unique `name`. Use one
identifier when selecting the layer.

| Operation | Required Fields | Effect |
|---|---|---|
| `add` | `type`, `operation.placement`, and `smartObject.smartObjectFile.source` | Adds a layer; `name` is optional. |
| `delete` | `id` or `name` | Removes the selected layer. Send the identifier and `operation`, not the add or edit fields. |
| `edit` | `type` and `id` or `name` | Changes an existing layer. Supply a file source to replace its contents. |

### Layer Placement

The `placement` object in the add operation determines where the new layer
appears. Its `type` is `top`, `bottom`, `above`, `below`, or `into`; it
defaults to `top`. For `above`, `below`, or `into`, include a
`referenceLayer` object with exactly one of `id` (integer) or `name`
(string). For `into`, the reference must be a group.

`"placement": { "type": "top" }` puts the layer at the top of the stack.

| Property | Type | Required | Default / Omission |
|---|---|---|---|
| `operation.placement` | object | For add | — |
| `operation.placement.type` | string | No | `top` |
| `operation.placement.referenceLayer` | object | For `above`, `below`, and `into` | — |

### Smart Object Fields

These properties belong to a layer's `smartObject` object:

| Property | Type | Required | Default / Omission | Use |
|---|---|---|---|---|
| `autoResize` | boolean | No | `true` for embedded replacements; omit for linked replacements | Edit only. Controls the size of an embedded replacement; see [Control Replacement Size](#control-replacement-size). |
| `contentPlacement` | object | No | — | Edit only. Fits or fills an eligible embedded frame; see [Place Content In A Frame](#place-content-in-a-frame). |
| `isLinked` | boolean | No | `false` | `false` embeds the file; `true` makes the replacement or added layer linked. |
| `smartObjectFile` | object | For add or content replacement | — | Contains `source`, an object identifying the file. |
| `smartObjectFile.source` | object | Required for the URL form | — | Contains the file's `url`. |
| `smartObjectFile.source.url` | string | Required for this input form | — | Signed HTTPS URL for reading the file. |

Use a PNG as in the examples. Inline file content is not supported in
`smartObjectFile.source`.

An embedded Smart Object can be replaced with another embedded file or with a
linked file. When replacing an existing linked Smart Object, set
`"isLinked": true`; replacing it with embedded content fails. Supply a
replacement file when changing the link state. If multiple layers share a Smart
Object, replacing its content can also change the other copies. Use independent
Smart Objects when their contents must differ.

## Size A Smart Object

The custom-size request above uses `transformMode: "custom"` and a
`transform.dimension` object to size the added layer. `dimension.width` and
`dimension.height` are integers; the example uses the default pixel unit. Set
both to the desired size in pixels:

```json
{
  "transformMode": "custom",
  "transform": { "dimension": { "width": 128, "height": 128 } }
}
```

This is a fragment of a layer operation. The `dimension` object also has an
optional `unit` string, which defaults to `pixels_unit`.

| Property | Type | Required | Default / Omission |
|---|---|---|---|
| `transform.dimension.width` | integer | Set both dimensions for `custom` | — |
| `transform.dimension.height` | integer | Set both dimensions for `custom` | — |
| `transform.dimension.unit` | string | No | `pixels_unit` |

The `transformMode` value controls how the layer is sized:

| Value | Effect |
|---|---|
| `custom` | Applies the supplied `transform`, such as the dimensions above. |
| `fill` | Scales toward filling the target area; the layer may extend beyond it. |
| `fit` | Scales toward fitting the layer inside the target area. |
| `none` | Applies no additional automatic transform. |

For `fill`, `fit`, and `none`, omit `transform`. When adding a layer, the
target area is the document canvas. When editing a layer, it is the layer's
original bounds. To crop replacement content inside an existing frame, use
[Place Content In A Frame](#place-content-in-a-frame) instead.

To size the added layer with `fit` in the first request, replace the layer's
`transformMode` and `transform` properties with:

```json
{ "transformMode": "fit" }
```

To size a replacement with `fill` relative to an existing layer's original
bounds, set `image.source.url` to a PSD containing `Product Artwork` and
include this edit operation in `edits.layers`:

```json
{
  "type": "smart_object_layer",
  "name": "Product Artwork",
  "operation": { "type": "edit" },
  "smartObject": {
    "isLinked": false,
    "smartObjectFile": { "source": { "url": "<REPLACEMENT_GET_URL>" } }
  },
  "transformMode": "fill"
}
```

For a 32 × 16 red PNG, the `fit` add example shows a 128 × 64 red area on the
128 × 128 white canvas. For the `fill` edit, start with a 128 × 128 white PSD
containing a 64 × 32 embedded `Product Artwork` layer at the top-left, and
replace it with a solid green 64 × 16 PNG. The PNG output shows a 128 × 32
green region extending beyond the original 64 × 32 frame. The canvas and masks
can limit what is visible; inspect the output when exact bounds matter.

## Add A Linked Smart Object

Use the same add operation as above, but set `isLinked` to `true`. This
fragment belongs in `edits.layers`:

```json
{
  "type": "smart_object_layer",
  "name": "Product Artwork",
  "operation": { "type": "add", "placement": { "type": "top" } },
  "smartObject": {
    "isLinked": true,
    "smartObjectFile": { "source": { "url": "<SMART_OBJECT_GET_URL>" } }
  },
  "transformMode": "custom",
  "transform": { "dimension": { "width": 128, "height": 128 } }
}
```

The PNG previews the artwork, and a manifest of the PSD identifies the layer
as linked. Keep a copy of the source artwork. If Photoshop reports a missing
file when you open the PSD elsewhere, right-click the affected layer in the
Layers panel, choose **Relink to File**, select that copy, and choose **Place**.
You can also respond to the missing-file dialog. To include the artwork in the
PSD instead, add an embedded Smart Object. See the
[Smart Object Workflow](../../workflows/smart_object/index.md#opening-the-output-psd-in-photoshop).

### Resize An Output PSD

`width` sets the target output width, while `maxWidth` caps it. If both are
positive, the smaller value is used. If only `maxWidth` is set, the output is
reduced only when the document is wider than that maximum. Height scales
proportionally.

For example, replace the PSD entry in the first request's `outputs` array with
this object:

```json
{
  "destination": { "url": "<PSD_PUT_URL>" },
  "mediaType": "image/vnd.adobe.photoshop",
  "width": 256,
  "maxWidth": 192
}
```

For a 128 × 128 document, the expected output is 192 × 192 pixels.

When a PSD output is resized using `outputs[].width` or `outputs[].maxWidth`,
linked Smart Objects whose source files are unavailable can become regular
pixel layers. To help retain a linked layer, provide its source file in an add
or edit operation in the same request, and verify the output manifest. Providing
one layer's file does not ensure that other linked layers' files are available.
Check each layer and keep an unresized PSD when retaining every linked layer matters.

## Replace Embedded Content

Select an existing embedded Smart Object and provide a new file. This
fragment replaces `Product Artwork` with an embedded PNG:

```json
{
  "type": "smart_object_layer",
  "name": "Product Artwork",
  "operation": { "type": "edit" },
  "smartObject": {
    "isLinked": false,
    "autoResize": false,
    "smartObjectFile": { "source": { "url": "<REPLACEMENT_GET_URL>" } }
  }
}
```

To replace embedded content with linked content instead, set `isLinked` to
`true` and omit `autoResize`. The resulting PSD contains a linked layer.

### Control Replacement Size

For an embedded PNG replacement, `autoResize: false` uses the replacement's
native dimensions and resolution. With `autoResize: true`, the replacement
is resized for the existing Smart Object. Omit `autoResize` to use its
default of `true`; omit it entirely for a linked replacement.

For example, replacing a 128 × 128 pixel embedded red square with a
32 × 16 pixel green PNG in a 128 × 128 white document produces:

| Setting | Visible Result |
|---|---|
| `false` | A 32 × 16 green area. |
| `true` | A 128 × 64 green area, preserving the replacement's proportions. |

The surrounding document is white. This example does not imply that every
file format or transformed layer has the same sizing behavior.

### Place Content In A Frame

For an eligible embedded Smart Object, `contentPlacement` places the
replacement inside the existing frame. Provide a replacement file and omit
`autoResize`, `transform`, and `transformMode`. Do not use this option with
a linked layer or linked replacement.

| `contentPlacement` Property | Type | Default / Omission | Use |
|---|---|---|---|
| `horizontalAlign` | string | `left` | `left`, `center`, or `right`. |
| `mode` | string | Required; no default | Use `fit` to fit the content inside the frame, or `fill` to size it toward filling the frame. |
| `verticalAlign` | string | `top` | `top`, `center`, or `bottom`. |

With `fit`, unused space in the frame is transparent. A frame can clip content
that extends beyond it; use alignment to choose the content's position.

This edit fits a replacement PNG in the center of the frame:

```json
{
  "type": "smart_object_layer",
  "name": "Product Artwork",
  "operation": { "type": "edit" },
  "smartObject": {
    "isLinked": false,
    "smartObjectFile": { "source": { "url": "<REPLACEMENT_GET_URL>" } },
    "contentPlacement": {
      "mode": "fit",
      "horizontalAlign": "center",
      "verticalAlign": "center"
    }
  }
}
```

Change `"mode": "fit"` to `"mode": "fill"` to try the other placement mode.
For a 128 × 64 blue replacement in the 128 × 128 white example, centered
`fit` shows a 128 × 64 blue area with white above and below. Centered `fill`
shows blue across the frame.

`contentPlacement` accepts JPEG, PNG, PSB, PSD, and TIFF replacements in RGB,
CMYK, grayscale, or Lab documents. Warped, skewed, or perspective frames and
frames with a vector mask are not eligible. A rotated or mirrored frame with a
pixel mask is also not eligible.

## Replace Linked Content

To replace a linked Smart Object with another linked file, include
`"isLinked": true` and omit `autoResize`:

```json
{
  "type": "smart_object_layer",
  "name": "Product Artwork",
  "operation": { "type": "edit" },
  "smartObject": {
    "isLinked": true,
    "smartObjectFile": { "source": { "url": "<REPLACEMENT_GET_URL>" } }
  }
}
```

The output PSD retains a linked Smart Object; the PNG previews the
replacement. A manifest layer fragment for this example looks like:

```json
{
  "name": "Product Artwork",
  "type": "smart_object_layer",
  "smartObject": { "isSmartObject": true, "isLinked": true }
}
```

This is a partial layer object, not the complete manifest. `name` and `type`
are strings; `smartObject.isSmartObject` and `smartObject.isLinked` are
booleans.

## Delete A Smart Object

This layer-operation fragment removes the named layer:

```json
{ "name": "Product Artwork", "operation": { "type": "delete" } }
```

For the initial example, deleting the only added layer leaves the white
background in the PNG. The output PSD no longer contains `Product Artwork`.

## Example: Update A Product Icon

This complete request adds a 128 × 128 red PNG as an embedded Smart Object
and replaces it with a 32 × 16 green PNG without resizing. Operations run in
order. Use distinct signed URLs for the two inputs and the two outputs.

```json
{
  "image": { "width": 128, "height": 128, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "smart_object_layer",
        "name": "Product Artwork",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "smartObject": {
          "isLinked": false,
          "smartObjectFile": { "source": { "url": "<SMART_OBJECT_GET_URL>" } }
        },
        "transformMode": "custom",
        "transform": { "dimension": { "width": 128, "height": 128 } }
      },
      {
        "type": "smart_object_layer",
        "name": "Product Artwork",
        "operation": { "type": "edit" },
        "smartObject": {
          "isLinked": false,
          "autoResize": false,
          "smartObjectFile": { "source": { "url": "<REPLACEMENT_GET_URL>" } }
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

After the job succeeds, the PNG shows the smaller green icon on white. The
PSD has one embedded `Product Artwork` Smart Object. Change `autoResize` to
`true` to resize the green replacement as in
[Control Replacement Size](#control-replacement-size).

## Troubleshooting

| Symptom | Cause And Fix |
|---|---|
| The request or job fails when adding a layer | Include `smartObject.smartObjectFile.source` and an add `placement`. Check that the signed input URL is readable. |
| An edit or delete cannot find the layer | Use its manifest `id` or a unique `name`, and use the correct input PSD. |
| A linked replacement fails | Set `isLinked` to `true` and omit `autoResize`; a linked Smart Object cannot be replaced with embedded content. |
| Frame placement fails | Use an embedded target and replacement, and omit `autoResize`, `transform`, and `transformMode`. Check whether the frame is eligible. |
| The output has the wrong size | Check `transform.dimension` on add and `autoResize` or `contentPlacement` on replacement. Inspect the resulting PNG and PSD. |

## Next Steps

- [Get Job Status](../../get-job-status/index.md): poll the job and check for errors.
- [Storage Solutions](https://developer.adobe.com/firefly-services/docs/photoshop/getting-started/storage-solutions/):
  prepare signed URLs for other storage providers.
