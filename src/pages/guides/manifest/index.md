---
title: Generate A Document Manifest
description: Inspect document properties and layers, generate thumbnails, and retrieve embedded content
keywords:
  - document properties
  - generate-manifest
  - layers
  - manifest
  - thumbnails
hideBreadcrumbNav: true
---

# Generate A Document Manifest

Use `POST /v2/generate-manifest` to inspect a Photoshop document before editing
it. The manifest describes the document and its layers; you can also request
layer thumbnails, XMP metadata, and files embedded in smart objects.

## Before You Start

Get an [access token and API key](../../getting-started/index.md), and a
download URL for a PSD you have permission to process. The URL must remain
readable while the job runs. Keep credentials and temporary file links private.

## Generate And Read A Manifest

Replace `<SIGNED_GET_URL>` with your PSD's download URL and submit:

```shell
curl -X POST https://photoshop-api.adobe.io/v2/generate-manifest \
  -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "image": { "source": { "url": "<SIGNED_GET_URL>" } },
    "outputs": [
      { "destination": { "embedded": "json" }, "mediaType": "application/json" }
    ]
  }'
```

The response contains a `statusUrl`. Poll it until the job succeeds or fails;
an accepted request does not mean the manifest is ready. See the
[API reference](../../api/photoshop-v2/index.md) for the status response.

For this request, the successful result contains the manifest as an object at
`result.outputs[0].destination.content`. This excerpt omits other fields:

```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "destination": {
          "content": {
            "document": {
              "bounds": { "left": 0, "top": 0, "right": 1000, "bottom": 1000 },
              "depth": 8,
              "imageMode": "rgb"
            },
            "layers": [
              { "id": 1, "index": 0, "name": "Background", "type": "background_layer", "visible": true }
            ]
          }
        }
      }
    ]
  }
}
```

`result.outputs` is an array of output objects. See the
[API reference](../../api/photoshop-v2/index.md) for other destinations. For the embedded
JSON destination above, each output has these fields:

| Field | Type | Meaning |
|---|---|---|
| `result.outputs[].destination` | object | The returned destination, containing `content` for this embedded JSON request. |
| `result.outputs[].destination.content` | object | The manifest itself; its `document`, `layers`, and nested fields are defined in the [Manifest Response Reference](../photoshop-v2/manifest-response-reference.md). |

The [API reference](../../api/photoshop-v2/index.md) defines the surrounding job status
and request errors. The example requests one output, so its index is `0`; do
not use that index as a layer ID.

## Request Fields

Fields not shown in a fragment retain their values from the complete request
above. The request supports these options:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `exportOptions` | object | No | JPEG thumbnails | Thumbnail encoding settings. See [Thumbnail Encoding](#thumbnail-encoding). |
| `extractSmartObjectData` | boolean | No | `false` | Request files embedded in smart objects. See [XMP And Smart Object Content](#xmp-and-smart-object-content). |
| `image` | object | Yes | None | The input document; contains `source`, defined below. |
| `includeLayerThumbnails` | boolean | No | `false` | Request layer previews. |
| `includeXmp` | boolean | No | `false` | Request XMP metadata. |
| `maximumThumbnailDepth` | integer | No | `0` (no limit) | Maximum nesting depth for thumbnails, `0` or greater. |
| `outputs` | array of objects | Yes | None | One to 25 output definitions. Each element contains a `destination` and a manifest `mediaType`, defined below. |
| `trimToTransparency` | boolean | No | `false` | Request removal of transparent padding from layer thumbnails; this does not edit the input document. |

### Input And Output Fields

The complete example uses a URL input and an embedded JSON output:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `image.source` | object | Yes | None | Identifies the input; the URL form contains `url`. |
| `image.source.url` | string | For a URL input | None | URL of the PSD. See the [API reference](../../api/photoshop-v2/index.md) for input requirements. |
| `outputs[].destination` | object | Yes | None | Where an output is returned. The embedded form contains `embedded`. |
| `outputs[].destination.embedded` | string | For an embedded destination | None | Set to `json` to return the parsed manifest object in the status result. |
| `outputs[].mediaType` | string | No | `application/json` | Manifest format used in this guide. |

Other source and destination forms, storage requirements, and output
encodings are defined in the [API reference](../../api/photoshop-v2/index.md).

## Generate Layer Thumbnails

Add these fields to the complete request to get JPEG previews:

```json
{
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 0,
  "exportOptions": { "mediaType": "image/jpeg", "quality": "high" }
}
```

`maximumThumbnailDepth` counts from top-level layers at depth `0`; a positive
value limits previews to that depth or closer to the top level. For example,
`1` includes top-level layers and their immediate children. The special value
`0` removes the depth limit. The setting controls thumbnails, not the layer
hierarchy in the manifest.

Where a thumbnail is returned, its layer has a `thumbnail` object with
`mediaType` and `url`. Download the URL while it is valid. Not every layer
necessarily has a thumbnail. The [thumbnail fields](../photoshop-v2/manifest-response-reference.md#layer-thumbnails)
describe the returned object.

### Thumbnail Encoding

`exportOptions` applies to thumbnails, not to the JSON manifest. If supplied,
its `mediaType` selects the fields that apply:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `exportOptions.compression` | string | No; PNG only | `default` | `none`, `very_low`, `low`, `medium_low`, `medium`, `medium_high`, `default`, `high`, `very_high`, or `maximum`. Compression changes encoding, not the intended image content. |
| `exportOptions.mediaType` | string | Yes, when `exportOptions` is supplied | None | `image/jpeg`, `image/png`, or `image/webp`. JPEG and PNG examples follow; see [WebP Thumbnails](#webp-thumbnails) for WebP. |
| `exportOptions.quality` | string | No; JPEG only | `medium` | Requested quality preset: `very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, or `photoshop_max`. |
| `exportOptions.scan` | object | No; JPEG only | Baseline standard | Requested JPEG scan encoding; its fields are defined below. |

For a PNG preview with transparency, request PNG and optional trimming:

```json
{
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 0,
  "trimToTransparency": true,
  "exportOptions": { "mediaType": "image/png", "compression": "high" }
}
```

Trimming requests a crop of transparent padding where applicable; it does not
change the PSD or replace the layer bounds in the manifest. PNG preserves
transparency, whereas JPEG does not.

### WebP Thumbnails

Set `exportOptions.mediaType` to `image/webp`. The WebP-specific
settings below belong inside `exportOptions`, not at the request root.

WebP exports use `compression: "lossy"` (the default) or `"lossless"`.
For lossy compression, `quality` is an integer from 0 to 100 and defaults
to 100; omit `quality` for lossless compression. Optional `includeEXIFData`,
`includePsExtras`, and `includeXMPData` booleans default to `false`.
Resizing, ICC profiles, animation, and content credential signing are not
supported for WebP.

### JPEG Scan Fields

The `scan` object can request baseline or progressive JPEG encoding:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `exportOptions.scan.optimized` | boolean | No; baseline only | `false` | Requests optimized baseline encoding. Omit for progressive encoding. |
| `exportOptions.scan.scans` | integer | No; progressive only | `3` | Progressive encoding setting: `3`, `4`, or `5`. Omit for baseline encoding. |
| `exportOptions.scan.type` | string | No | `baseline` | `baseline` or `progressive`. Set `progressive` explicitly when using `scans`. |

For example, this fragment requests the progressive `3` setting:

```json
{
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 0,
  "exportOptions": {
    "mediaType": "image/jpeg",
    "quality": "high",
    "scan": { "type": "progressive", "scans": 3 }
  }
}
```

To use the default progressive setting, omit `scans`:

```json
{
  "includeLayerThumbnails": true,
  "maximumThumbnailDepth": 0,
  "exportOptions": {
    "mediaType": "image/jpeg",
    "quality": "high",
    "scan": { "type": "progressive" }
  }
}
```

The `scans` setting is not necessarily the number of JPEG Start of Scan
markers: a color image can use separate component scans. If your workflow
depends on the scan structure, inspect the downloaded thumbnail.

## XMP And Smart Object Content

Add this fragment to request metadata and embedded smart-object files:

```json
{
  "includeLayerThumbnails": false,
  "includeXmp": true,
  "extractSmartObjectData": true
}
```

When available, document XMP is returned as `document.xmp`, and XMP for an
embedded smart object is returned as `smartObject.xmp` on its layer. XMP is an
XML string and may contain private metadata. When extraction succeeds, the
layer's `smartObject.extracted` object contains a file `mediaType` and a
temporary download `url`. Linked smart objects refer to external files and are
not extracted by this option.

Both settings default to `false`; request either one independently if you do
not need both. The [smart-object fields](../photoshop-v2/manifest-response-reference.md#smart-object-layers)
explain the returned flags and conditional fields. Download links can expire;
keep them private.

## Use The Manifest To Inspect A Template

1. Generate the manifest for your PSD and wait for `succeeded`.
2. Read `document.bounds` to determine the canvas size. Walk `layers`, including
   any nested group or artboard layers, to find the layer you want.
3. Use the layer's `id` or `name` when targeting it in an edit. IDs identify
   layers within this document; they are not array positions, and names need
   not be unique.
4. If you requested previews or embedded files, retrieve their respective
   `thumbnail.url` or `smartObject.extracted.url` while valid.

See the [response reference](../photoshop-v2/manifest-response-reference.md)
for rectangles, layer types, text, gradients, and nested objects.

## Troubleshooting

| Symptom | Cause And Fix |
|---|---|
| The request is rejected | Check the JSON, input URL, output destination, supported field names, and option values. In particular, thumbnail depth cannot be negative. |
| The job was accepted but no manifest is available | Poll until the job reaches `succeeded`; inspect `errorDetails` if it reaches `failed`. |
| A layer has no thumbnail | Check that `includeLayerThumbnails` is `true` and that the layer is within the requested depth; a thumbnail is not guaranteed for every layer. |
| No extracted file appears | The option extracts eligible embedded smart objects, not linked objects. Check the layer's `smartObject.isLinked` and whether extraction was requested. |
| A download link no longer works | Generate a new manifest and retrieve its temporary links promptly. |
