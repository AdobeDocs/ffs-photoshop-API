---
title: Create Artboard
description: Combine 1 to 25 images into one Photoshop document, with one artboard per image, using POST /v2/create-artboard.
keywords:
  - create artboard
  - artboards
  - combine images
  - photoshop api
hideBreadcrumbNav: true
---

# Create Artboard

Use `POST /v2/create-artboard` to combine 1 to 25 images into one Photoshop
document. Each image becomes an artboard of the same size, placed left to
right in request order. Request a PSD to keep the artboards and layers
editable, or a JPEG, PNG, or TIFF to get a flat image of the whole document.

## Before You Start

- Get an access token and client ID; see [Authentication](../../getting-started/index.md).
- Prepare a signed URL to read each input and to write each output; see
  [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
  Replace each `<...>` placeholder in the requests with your own URL.
- Use PSD or JPEG inputs.

## Create An Artboard Document

This request combines a PSD and a JPEG into one PSD. Save it as
`request.json`:

```json
{
  "images": [
    { "source": { "url": "<POSTER_PSD_GET_URL>" } },
    { "source": { "url": "<PHOTO_JPEG_GET_URL>" } }
  ],
  "outputs": [
    {
      "destination": { "url": "<ARTBOARDS_PSD_PUT_URL>" },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

Send the request:

```shell
curl --request POST https://photoshop-api.adobe.io/v2/create-artboard \
  --header "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  --header "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  --header "Content-Type: application/json" \
  --data @request.json
```

A `202 Accepted` response contains a `statusUrl`. Poll it until `status` is
`succeeded` or `failed`. Read the PSD from your output URL only when the job
succeeds; on failure, inspect `errorDetails`. Acceptance alone does not mean
processing succeeded. See [Get Job Status](../get-job-status/index.md).

For a 1000 × 1000 pixel PSD and a 300 × 600 pixel JPEG, the result is a
1400 × 1050 pixel document with these artboards:

| Artboard name | Left | Top | Right | Bottom |
|---|---:|---:|---:|---:|
| `1000 x 1000` | 0 | 0 | 1000 | 1000 |
| `300 x 600` | 1050 | 0 | 1350 | 600 |

To read the artboards of any result, send the PSD to Generate Manifest.

## How Artboards Are Arranged

- **Canvas height:** The tallest image plus 50 pixels.
- **Canvas width:** The sum of the image widths, plus `artboardSpacing` once
  per image. The space after the last artboard is included.
- **Layer contents:** A PSD keeps its layers and groups inside its artboard. A
  flat image, such as a JPEG, becomes one pixel layer.
- **Layers panel:** Artboards stack in request order, with the last image at
  the top. An empty layer named `Layer 1` is at the bottom.
- **Names:** Each artboard uses `images[].name`. Without a name, it uses the
  image size as `<width> x <height>`, for example `1000 x 1000`.
- **Position:** The first artboard starts at the left edge. All artboards
  align to the top edge. Each later artboard starts `artboardSpacing` pixels
  after the previous one.
- **Size:** Each artboard matches its image's width and height in pixels.

## Request Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `artboardSpacing` | integer | No | `50` | Horizontal space after each artboard, in pixels. Use `0` or more; `0` places artboards edge to edge. |
| `images` | array of [Image](#image-fields) objects | Yes | None | Images to combine, from 1 to 25. Each image becomes one artboard, in array order. |
| `outputs` | array of [Output](#output-fields) objects | Yes | None | Files to create, from 1 to 25. |

### Image Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `name` | string | No | Image size, such as `1000 x 1000` | Artboard name, from 1 to 255 characters. Names need not be unique. |
| `source` | [Source](#source-fields) object | Yes | None | Location of the input image. |

### Source Fields

Supply exactly one of these three shapes.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `creativeCloudFileId` | string | Yes, for a Creative Cloud file ID | None | File ID in Creative Cloud storage. Starts with `urn:aaid:`. |
| `creativeCloudPath` | string | Yes, for a Creative Cloud path | None | Path in Creative Cloud storage. Not blank. |
| `creativeCloudProjectId` | string | No | None | With `creativeCloudPath` only. Project that contains the path. Starts with `urn:aaid:`. |
| `url` | string | Yes, for a URL | None | HTTPS URL that the API can read, such as a signed GET URL. |

For Creative Cloud locations, see
[Creative Cloud Storage](../shared-reference/input-files-and-storage.md#creative-cloud-path-source).

### Output Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `compression` | string | No | `default` | PNG only. One of `none`, `very_low`, `low`, `medium_low`, `medium`, `medium_high`, `default`, `high`, `very_high`, `maximum`. |
| `destination` | [Destination](#destination-fields) object | Yes | None | Where to write the file. Use a different destination for each output. |
| `maxWidth` | integer | No | None | Largest output width, in pixels, 0 or more. A wider document is scaled down to this width; its height scales proportionally. |
| `mediaType` | string | No | `image/jpeg` | Output format. One of `image/jpeg`, `image/png`, `image/tiff`, `image/vnd.adobe.photoshop` (PSD). |
| `quality` | string | No | `photoshop_max` | JPEG only. One of `very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, `photoshop_max`. |
| `resample` | string | No | `bicubic_sharper` when resizing | Resizing method. One of `nearest_neighbor`, `bilinear`, `bicubic`, `bicubic_smoother`, `bicubic_sharper`. |
| `scan` | [JPEG Scan](#jpeg-scan-fields) object | No | Baseline | JPEG only. Encoding options. |
| `width` | integer | No | None | Output width, in pixels, 0 or more. Its height scales proportionally. `0` keeps the document width. |

PSD outputs keep artboards and layers editable. JPEG, PNG, and TIFF outputs
contain the whole document, including the space around the artboards. For
color profiles and layer exports, see the [API Reference](../../api/photoshop-v2/index.md).

### Destination Fields

Supply exactly one of these three shapes.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `creativeCloudPath` | string | Yes, for Creative Cloud | None | Path to write in Creative Cloud storage. Not blank. |
| `creativeCloudProjectId` | string | No | None | With `creativeCloudPath` only. Project that contains the path. Starts with `urn:aaid:`. |
| `storageType` | string | No; required for Azure or Dropbox | None | With `url` only. Set `azure` for an Azure Blob Storage SAS URL or `dropbox` for a Dropbox upload URL. Omit for other signed URLs. |
| `url` | string | Yes, for a URL | None | HTTPS URL that the API can write to, such as a signed PUT URL. |
| `validityPeriod` | integer | Yes, for hosted storage | None | Requests a temporary download URL that Adobe hosts. Lifetime in seconds, from 60 to 86,400. |

For a hosted output, read the download URL from
`result.outputs[].destination.url` in the job status. See
[Hosted Storage](../shared-reference/output-formats-and-options.md#hosted-destination).

### JPEG Scan Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `optimized` | boolean | No | `false` | With `baseline` only. `true` writes optimized baseline encoding. |
| `scans` | integer | No | None | With `progressive` only. Number of scans, from 3 to 5. |
| `type` | string | No | `baseline` | One of `baseline` or `progressive`. |

## Name Artboards And Create Several Formats

This request names each artboard, sets 100 pixels of spacing, and writes a
PSD, a JPEG preview no wider than 1000 pixels, and a PNG:

```json
{
  "images": [
    { "name": "Poster", "source": { "url": "<POSTER_PSD_GET_URL>" } },
    { "name": "Photo", "source": { "url": "<PHOTO_JPEG_GET_URL>" } }
  ],
  "artboardSpacing": 100,
  "outputs": [
    {
      "destination": { "url": "<ARTBOARDS_PSD_PUT_URL>" },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": { "url": "<PREVIEW_JPEG_PUT_URL>" },
      "mediaType": "image/jpeg",
      "quality": "high",
      "maxWidth": 1000
    },
    {
      "destination": { "url": "<ARTBOARDS_PNG_PUT_URL>" },
      "mediaType": "image/png"
    }
  ]
}
```

With the same inputs as before, the PSD and PNG are 1500 × 1050 pixels, and
the JPEG is 1000 × 700 pixels. The `Photo` artboard starts at 1100 pixels from
the left edge.

## Use Creative Cloud Files

This request reads one input by Creative Cloud path and one by file ID, and
writes the PSD to Creative Cloud storage:

```json
{
  "images": [
    {
      "name": "Poster",
      "source": { "creativeCloudPath": "<POSTER_PSD_CREATIVE_CLOUD_PATH>" }
    },
    {
      "name": "Photo",
      "source": { "creativeCloudFileId": "urn:aaid:sc:US:<PHOTO_FILE_ID>" }
    }
  ],
  "outputs": [
    {
      "destination": { "creativeCloudPath": "<ARTBOARDS_PSD_CREATIVE_CLOUD_PATH>" },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

## Troubleshooting

A `422` response means the request is invalid. Its message names the field.

- **`artboard name must be between 1 and 255 characters`:** Shorten the name,
  or omit `name` to use the image size.
- **`image/webp output is only supported for create-composite`:** Choose a
  JPEG, PNG, TIFF, or PSD output.
- **`images must contain between 1 and 25 items`:** Send from 1 to 25 images.
  To combine more, split them across several requests.
- **`outputs must contain between 1 and 25 items`:** Send from 1 to 25
  outputs.
- **Two artboards have the same name:** Images of the same size get the same
  default name. Set `name` for each image.
- **The request was accepted but no output is available:** Check the job
  status and its `errorDetails` before reading the destination. Confirm each
  input URL is readable and each output URL is writable.
