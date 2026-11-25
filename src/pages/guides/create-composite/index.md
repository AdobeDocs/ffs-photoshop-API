---
title: Create Composite Overview
description: Create or edit a Photoshop document with the Create Composite API, then export it.
keywords:
  - create composite
  - layers
  - layer operations
  - placement
  - outputs
hideBreadcrumbNav: true
---

# Create Composite Overview

Use `POST /v2/create-composite` to start from an existing file or a new blank
document, add, edit, move, or delete layers, apply document-level edits, and
write one or more output files.

The request is asynchronous. A `202` response means the job was accepted;
poll the job status to learn whether it succeeded.

## Before You Start

- Get an access token and client ID; see
  [Authentication](../../getting-started/index.md).
- Prepare signed URLs for reading inputs and writing outputs; see
  [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
  Replace each `<...>` placeholder with your own URL.
- To edit an existing file, use Generate Manifest to find layer `id` and
  `name` values.

## Create A Blank Document

This request creates a 100 × 100 pixel transparent document and saves it as
a PSD:

```json
{
  "image": { "width": 100, "height": 100 },
  "outputs": [
    { "destination": { "url": "<NEW_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

## Add A Color And Text Layer

This request creates a white 1200 × 600 pixel document, adds an orange-red
solid-color layer named `Backdrop`, adds a text layer named `Offer` above it,
and writes a PSD and a PNG. Save the request as `request.json`:

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
      },
      {
        "type": "text_layer",
        "name": "Offer",
        "operation": { "type": "add", "placement": { "type": "top" } },
        "text": {
          "content": "Save 20% on everything",
          "frame": { "type": "point", "origin": { "x": 60, "y": 300 } },
          "characterStyles": [{ "characterStyle": { "fontSize": 40 } }]
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<NEW_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
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

Layers are applied in array order, so `Offer` is placed on top of `Backdrop`.
A new document created with `fill` set to `white` already contains a locked
layer named `Background`; both new layers sit above it.

## Read The Result

The `202` response contains `jobId` and `statusUrl`. Poll `statusUrl` until
`status` is `succeeded` or `failed`; see
[Get Job Status](../get-job-status/index.md). Outputs are written only when
the job succeeds.

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `jobId` | string | Always | Job identifier. |
| `status` | string | Always | `not_started`, `running`, `succeeded`, or `failed`. |
| `result.outputs` | array of objects | When `succeeded` | One entry per written output. |
| `result.outputs[].mediaType` | string | When `succeeded` | Format of the written file. |
| `result.outputs[].destination` | object | When `succeeded` | Where the file was written. For a signed-URL destination, contains `url`. |
| `errorDetails` | array of objects | When `failed` | Reasons for the failure. |
| `errorDetails[].errorCode` | string | When `failed` | Machine-readable failure code. |
| `errorDetails[].message` | string | When `failed` | Human-readable description. |

## Request Structure

A request has four top-level fields. Only `image` and `outputs` are required.

```text
image                 existing file (source) or new document (width, height, ...)
fontOptions           font handling for text layers
edits
  layers[]            layer operations, applied in array order
  document            crop, resize, and trim, applied after all layer operations
outputs[]             1 to 25 files to write
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `image` | object | Yes | — | The document to start from. Use either an [existing file](#existing-file) or a [new document](#new-document), not both. |
| `fontOptions` | object | No | — | Font handling for text layers; see [Font Options](text-layers.md#font-options). |
| `edits` | object | No | — | Changes to make. Omit to export `image` unchanged. See [Edits Fields](#edits-fields). |
| `outputs` | array of objects | Yes | — | 1 to 25 output files. See [Outputs](#outputs). |

In the `Default` column, `—` means no default is documented for an optional
field, or that a required field must be supplied. A value marked “on add”
applies only when creating a layer. On edits, omitted fields keep their
current values where the table says so; this is different from a default
used when adding a layer.

## Input Image

### Existing File

Set `image.source` to the PSD to edit.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `image.source` | object | Yes | — | Location of the input file. Supply exactly one of `url`, `creativeCloudPath`, `creativeCloudFileId`, or `lightroomPath`. |
| `image.source.url` | string | One of | — | Signed URL for reading the file. |
| `image.source.creativeCloudPath` | string | One of | — | Path of a file in Creative Cloud storage; see [Creative Cloud Storage](../shared-reference/input-files-and-storage.md#creative-cloud-path-source). |
| `image.source.creativeCloudProjectId` | string | No | — | Project that contains `creativeCloudPath`. Starts with `urn:aaid:`. |
| `image.source.creativeCloudFileId` | string | One of | — | Creative Cloud file ID. Starts with `urn:aaid`. |
| `image.source.lightroomPath` | string | One of | — | Partial Lightroom asset path beginning with `/v2/`; see [Lightroom Storage](../shared-reference/input-files-and-storage.md#lightroom-path-source). |

### New Document

Omit `source` and describe a blank document instead.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `image.width` | integer | No | `100` | Width, 1 to 32,000, in `image.unit`. `null` is rejected. |
| `image.height` | integer | No | `100` | Height, 1 to 32,000, in `image.unit`. `null` is rejected. |
| `image.unit` | string | No | `pixels_unit` | `pixels_unit` or `points_unit`. See [Points Example](#points-example). |
| `image.fill` | string | No | `transparent` | `white`, `background_color`, or `transparent`. |
| `image.resolution` | object | No | 72 ppi | Contains `value` and `unit`. |
| `image.resolution.value` | integer | Yes, in `resolution` | — | Pixels per inch, at least 1. |
| `image.resolution.unit` | string | No | `density_unit` | Only `density_unit`. |
| `image.mode` | string | No | `rgb` | `rgb`, `grayscale`, `cmyk`, `lab`, `hsb`, `indexed`, `bitmap`, `duotone`, or `multichannel`. |
| `image.depth` | integer | No | Mode default | Bits per channel. Must suit `mode`; see the table below. |
| `image.pixelScaleFactor` | number | No | `1.0` | At least 0.1. |
| `image.iccProfile` | object | No | — | Color profile to assign; see [ICC Profile Fields](export-documents-and-layers.md#icc-profile-fields). |
| `image.name` | string | No | — | Document title, up to 255 characters. |

| `mode` | Allowed `depth` |
|---|---|
| `rgb`, `hsb`, `grayscale` | 8, 16, 32 |
| `cmyk`, `lab`, `multichannel` | 8, 16 |
| `indexed`, `duotone` | 8 |
| `bitmap` | 1, or omit |

#### Points Example

With `points_unit`, width and height are converted to pixels as
`round(points × resolution ÷ 72)`. The result must not exceed 32,000 pixels.

```json
{
  "image": {
    "width": 288,
    "height": 144,
    "unit": "points_unit",
    "resolution": { "value": 300, "unit": "density_unit" },
    "fill": "white"
  },
  "outputs": [
    { "destination": { "url": "<NEW_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

| Field | Calculation | Pixels |
|---|---|---:|
| `width` | round(288 × 300 ÷ 72) | 1200 |
| `height` | round(144 × 300 ÷ 72) | 600 |

At the default 72 ppi, one point equals one pixel.

## Edits Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `edits.layers` | array of objects | No | — | Layer operations, applied one at a time in array order. Each element uses the [Layer Operation Fields](#layer-operation-fields). |
| `edits.document` | object | No | — | Document crop, resize, and trim; see [Document Edits](document-edits.md). Applied after all layer operations. |

## Layer Operation Fields

Each `edits.layers` element selects or names one layer and performs one
operation on it.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `operation` | object | Yes | — | What to do. See [Operation Fields](#operation-fields). |
| `type` | string | For `add` and `edit` | — | Layer type; see [Layer Types](#layer-types). Omit for `delete` and `move`. |
| `id` | integer | `edit`, `delete`, `move`: `id` or `name` | — | Existing layer ID. Takes precedence over `name`. |
| `name` | string | `edit`, `delete`, `move`: `id` or `name` | — | For `add`, the new layer's name. Otherwise selects an existing layer by name; use a unique name. |
| `isVisible` | boolean | No | `true` on add | `false` hides the layer. Omit on edit to keep the current visibility. |
| `blendOptions` | object | No | — | Contains `opacity` (integer 0 to 100; `100` on add) and `blendMode`; see the [API Reference](../../api/photoshop-v2/index.md) for blend modes. |
| `isClipped` | boolean | No | `false` on add | `true` clips the layer to the layer below. Not for group layers. |

Other fields depend on `type`; see the guide in [Layer Types](#layer-types).
For `transform`, `transformMode`, `protection`, `pixelMask`, and
`layerEffects`, see the [API Reference](../../api/photoshop-v2/index.md).

### Layer Types

| `type` | Add | Edit | Type-specific fields | Guide |
|---|---|---|---|---|
| `adjustment_layer` | Yes | Yes | `adjustments` | [API Reference](../../api/photoshop-v2/index.md) |
| `background_layer` | Yes | Yes | `image`, `convertToLayer`, `convertedLayerName` | [API Reference](../../api/photoshop-v2/index.md) |
| `group_layer` | No | Yes | None | [API Reference](../../api/photoshop-v2/index.md) |
| `layer` | Yes | Yes | `image` (required on add) | [API Reference](../../api/photoshop-v2/index.md) |
| `smart_object_layer` | Yes | Yes | `smartObject` | [Smart Objects](smart-objects/index.md) |
| `solid_color_layer` | Yes | Yes | `fill` | [Solid-Color Layers](solid-color-layers.md) |
| `text_layer` | Yes | Yes | `text` | [Text Layers](text-layers.md) |

On edit, set `type` to the existing layer's type.

### Operation Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `operation.type` | string | Yes | — | `add`, `edit`, `delete`, or `move`. Lowercase only. |
| `operation.placement` | object | For `add` and `move` | — | Where the layer goes. See [Placement Fields](#placement-fields). Not used when adding a `background_layer`. |
| `operation.shouldIncludeChildren` | boolean | No | `true` | `delete` and `move` only. For a group, `true` includes its contents; `false` leaves them in the document. |

How the operations differ:

| `operation.type` | Layer selection | `type` | `placement` | Other layer fields |
|---|---|---|---|---|
| `add` | New layer; `name` sets its name | Required | Required | Allowed |
| `edit` | `id` or `name` | Required | Not used | Allowed; omitted fields keep their current values |
| `delete` | `id` or `name` | Omit | Not used | Not allowed |
| `move` | `id` or `name` | Omit | Required | Not allowed |

A `delete` or `move` element accepts only `id`, `name`, and `operation`.
Any other field rejects the request with `400`.

### Placement Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `placement.type` | string | No | `top` | `top` or `bottom` of the layer stack; `above` or `below` the reference layer; `into` the reference group. |
| `placement.referenceLayer` | object | For `above`, `below`, `into` | — | The layer to place relative to. |
| `placement.referenceLayer.id` | integer | One of | — | Reference layer ID. |
| `placement.referenceLayer.name` | string | One of | — | Reference layer name. Must not be blank. |

Supply exactly one of `referenceLayer.id` and `referenceLayer.name`. Without a
reference, `above`, `below`, and `into` are accepted but the job fails.

## Edit An Existing Document

This request opens a PSD, changes the text of `Offer`, hides `Badge`, and
deletes `Draft Note`:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Offer",
        "operation": { "type": "edit" },
        "text": { "content": "Save 30% on everything" }
      },
      {
        "type": "text_layer",
        "name": "Badge",
        "operation": { "type": "edit" },
        "isVisible": false
      },
      {
        "name": "Draft Note",
        "operation": { "type": "delete" }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<EDITED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" },
    { "destination": { "url": "<PREVIEW_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

## Reorder And Remove Layers

This request moves layer `7` above the layer named `Backdrop` and deletes the
group `Old Promo` while keeping its contents:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "id": 7,
        "operation": {
          "type": "move",
          "placement": { "type": "above", "referenceLayer": { "name": "Backdrop" } }
        }
      },
      {
        "name": "Old Promo",
        "operation": { "type": "delete", "shouldIncludeChildren": false }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<EDITED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

A group cannot be moved into itself. A document's only layer cannot be deleted.

## Outputs

Each `outputs` element writes one file. Only `destination` is required; the
format defaults to JPEG.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `outputs[].destination` | object | Yes | — | Where to write. For a signed URL, `{"url": "<...>"}`. Other destinations: [Destinations](export-documents-and-layers.md#destinations). |
| `outputs[].mediaType` | string | No | `image/jpeg` | Output format; see [Formats](export-documents-and-layers.md#formats). |

To resize an output, export specific layers, or set format options, see
[Export Documents And Layers](export-documents-and-layers.md).

## Errors

Requests that fail validation are rejected before a job starts. The body
contains `error_code` and `message`.

| Status | `message` example | Fix |
|---|---|---|
| `400` | `Request payload contains invalid fields: type, text` | Remove fields the operation does not accept, such as `type` on a delete. |
| `422` | `edits.layers[0].operation.placement: must not be null` | Add `placement` to every `add`. |
| `422` | `Missing required field 'type' for edit operation at path 'edits.layers[0]'` | Add the layer `type` to every `add` and `edit`. |
| `422` | `edits.layers[0]: Either id or name is required when operation type is edit` | Identify the existing layer with `id` or `name`. |
| `422` | `Invalid value 'Add' at path 'edits.layers[0].operation.type'. Accepted values are: add, edit, delete, move` | Use lowercase operation names. |

Accepted jobs can still fail. The job status then contains `errorDetails`,
for example:

```json
{
  "status": "failed",
  "errorDetails": [
    {
      "errorCode": "invalid_parameters",
      "message": "create text layer: Reference layer ID or name is required for ABOVE, BELOW, INTO Placement types"
    }
  ]
}
```

| Symptom | Fix |
|---|---|
| Reference layer is required | Add `referenceLayer` for `above`, `below`, or `into`. |
| Layer is not found | Check `id` or `name` against the document's manifest. |
| Delete by name fails | More than one layer has that name; use `id`. |

## Next Steps

- [Document Edits](document-edits.md)
- [Export Documents And Layers](export-documents-and-layers.md)
- [Text Layers](text-layers.md)
- [Solid-Color Layers](solid-color-layers.md)
- [Smart Objects](smart-objects/index.md)
- [Get Job Status](../get-job-status/index.md)
