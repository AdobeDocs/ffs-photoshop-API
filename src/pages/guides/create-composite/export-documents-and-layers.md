---
title: Export Documents And Layers
description: Choose formats, sizes, color profiles, layers, and destinations for Create Composite outputs.
keywords:
  - create composite
  - outputs
  - export layers
  - JPEG
  - PNG
  - ICC profile
hideBreadcrumbNav: true
---

# Export Documents And Layers

Each item in `outputs` of `POST /v2/create-composite` produces one file.
Use several items to export the same edited document in several formats,
sizes, or layer selections. For the rest of the request, see the
[Create Composite Overview](index.md).

## Export One PSD

This request saves the input document as a PSD:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

## Export Several Formats

This request saves the edited PSD, a full-size PNG, and a JPEG preview no
wider than 800 pixels:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    {
      "destination": { "url": "<EDITED_PSD_PUT_URL>" },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": { "url": "<FULL_PNG_PUT_URL>" },
      "mediaType": "image/png",
      "compression": "medium"
    },
    {
      "destination": { "url": "<PREVIEW_JPEG_PUT_URL>" },
      "mediaType": "image/jpeg",
      "quality": "high",
      "maxWidth": 800
    }
  ]
}
```

## Output Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `outputs` | array of objects | Yes | — | 1 to 25 items. Each item is one output file. |
| `outputs[].destination` | object | Yes | — | Where the file is stored. See [Destinations](#destinations). |
| `outputs[].mediaType` | string | No | `image/jpeg` | File format. See [Formats](#formats). |
| `outputs[].width` | integer | No | — | Output width in pixels, at least 0. Height scales proportionally. See [Output Size](#output-size). |
| `outputs[].maxWidth` | integer | No | — | Largest allowed output width in pixels, at least 0. See [Output Size](#output-size). |
| `outputs[].resample` | string | No | `bicubic_sharper` when `width` or `maxWidth` is set | `nearest_neighbor`, `bilinear`, `bicubic`, `bicubic_smoother`, or `bicubic_sharper`. |
| `outputs[].layers` | array of objects | No | — | Up to 100 layers to export instead of the whole document. See [Export Layers](#export-layers). |
| `outputs[].cropMode` | string | No | Depends on `layers` | Area to export. See [Crop Modes](#crop-modes). |
| `outputs[].iccProfile` | object | No | — | Color profile to embed. See [ICC Profile Fields](#icc-profile-fields). |

In the `Default` column, `—` means no default is documented for an optional
field, or that a required field must be supplied. Omitted output-sizing
fields leave the document's size unchanged; other defaults are stated in the
table.

Format-specific fields, such as `quality` and `compression`, are listed
under [Formats](#formats).

## Formats

| `mediaType` | Format | Format Fields | `width`, `maxWidth`, `iccProfile` | `layers`, `cropMode` |
|---|---|---|---|---|
| `document/vnd.adobe.cpsd+dcx` | Cloud PSD | — | No | No |
| `document/vnd.adobe.cpsd+dcxucf` | Cloud PSD package | — | No | No |
| `image/jpeg` | JPEG | [JPEG Fields](#jpeg-fields) | Yes | Yes |
| `image/png` | PNG | [PNG Fields](#png-fields) | Yes | Yes |
| `image/webp` | WebP | [WebP Fields](#webp-fields) | No | Yes |
| `image/tiff` | TIFF | — | Yes | Yes |
| `image/vnd.adobe.photoshop` | PSD | — | Yes | Yes |

### JPEG Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `quality` | string | No | — | `very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, or `photoshop_max`. |
| `scan` | object | No | Baseline | Encoding order. |
| `scan.type` | string | No | `baseline` | `baseline` or `progressive`. |
| `scan.optimized` | boolean | No | `false` | Optimized baseline encoding. Only with `baseline`. |
| `scan.scans` | integer | No | — | Number of progressive passes: 3, 4, or 5. Only with `progressive`. |

A progressive JPEG for web previews:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    {
      "destination": { "url": "<PREVIEW_JPEG_PUT_URL>" },
      "mediaType": "image/jpeg",
      "quality": "maximum",
      "scan": { "type": "progressive", "scans": 3 }
    }
  ]
}
```

### PNG Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `compression` | string | No | `default` | Compression level. See the table below. |

Higher levels produce smaller files and take longer. All levels are
lossless.

| `compression` | Level |
|---|---:|
| `none` | 0 |
| `very_low` | 1 |
| `low` | 2 |
| `medium_low` | 3 |
| `medium` | 4 |
| `medium_high` | 5 |
| `default` | 6 |
| `high` | 7 |
| `very_high` | 8 |
| `maximum` | 9 |

### WebP Fields

WebP exports use `compression: "lossy"` (the default) or `"lossless"`.
For lossy compression, `quality` is an integer from 0 to 100 and defaults
to 100; omit `quality` for lossless compression. Optional `includeEXIFData`,
`includePsExtras`, and `includeXMPData` booleans default to `false`.
Resizing, ICC profiles, animation, and content credential signing are not
supported for WebP.

## Output Size

`width` scales the output to exactly that width, larger or smaller.
`maxWidth` reduces the output only when it would be wider. When both are
set, the smaller value wins. Height always keeps the document's ratio. A
value of `0` is the same as omitting the field.

For a 300 × 600 pixel document:

| `width` | `maxWidth` | Output |
|---:|---:|---|
| — | — | 300 × 600 |
| 500 | — | 500 × 1000 |
| — | 200 | 200 × 400 |
| — | 800 | 300 × 600, unchanged |
| 900 | 800 | 800 × 1600 |

Output size does not change the document itself. To change the saved
canvas, use [document resize](document-edits.md#resize-a-document).

## Export Layers

`outputs[].layers` exports selected layers instead of the whole document.

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    {
      "destination": { "url": "<LOGO_PNG_PUT_URL>" },
      "mediaType": "image/png",
      "layers": [ { "name": "Logo" } ]
    },
    {
      "destination": { "url": "<PRODUCT_SHOT_PNG_PUT_URL>" },
      "mediaType": "image/png",
      "layers": [ { "name": "Product" }, { "id": 12 } ],
      "cropMode": "trim_to_transparency"
    }
  ]
}
```

The first output is the `Logo` layer cropped to its own bounds. The second
is one image of `Product` and layer `12` together, with every other layer
hidden, trimmed to the visible pixels.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `layers[].id` | integer | One of `id` or `name` | — | Layer ID. |
| `layers[].name` | string | One of `id` or `name` | — | Layer name. |
| `layers[].shouldIncludeChildren` | boolean | No | `true` | For a group, `true` also shows the layers inside it. `false` shows only the group's own content. |

An empty `layers` array exports the whole document. Listing a layer twice
exports it once.

### Crop Modes

| `cropMode` | Exported Area | Default When |
|---|---|---|
| `document_bounds` | The whole canvas. | Several layers are listed. |
| `layer_bounds` | The bounds of the single listed layer. Requires exactly one layer. | One layer is listed. |
| `trim_to_transparency` | The visible pixels, with transparent edges removed. | — |

## ICC Profile Fields

`outputs[].iccProfile` embeds a color profile in JPEG, PNG, TIFF, and PSD
outputs. Choose a standard profile by name, or supply your own profile file.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `iccProfile.type` | string | No | `standard` | `standard` or `custom`. |
| `iccProfile.name` | string | Yes for `custom` | `sRGB IEC61966-2.1` for `standard` | Standard profile name from the table below, or a label for a custom profile, up to 255 characters. |
| `iccProfile.imageMode` | string | No | — | `rgb` or `grayscale`. With `custom`, `cmyk` is also allowed. |
| `iccProfile.source` | object | Yes for `custom` | — | The `.icc` file, as a [file input](../../getting-started/storage-solutions/index.md). Only with `custom`. |

| Standard `name` | Color Type |
|---|---|
| `Adobe RGB (1998)` | RGB |
| `Apple RGB` | RGB |
| `ColorMatch RGB` | RGB |
| `sRGB IEC61966-2.1` | RGB |
| `Dot Gain 10%` | Grayscale |
| `Dot Gain 15%` | Grayscale |
| `Dot Gain 20%` | Grayscale |
| `Dot Gain 25%` | Grayscale |
| `Dot Gain 30%` | Grayscale |
| `Gray Gamma 1.8` | Grayscale |
| `Gray Gamma 2.2` | Grayscale |

A standard and a custom profile:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    {
      "destination": { "url": "<ADOBE_RGB_JPEG_PUT_URL>" },
      "mediaType": "image/jpeg",
      "iccProfile": { "type": "standard", "name": "Adobe RGB (1998)", "imageMode": "rgb" }
    },
    {
      "destination": { "url": "<PRINT_TIFF_PUT_URL>" },
      "mediaType": "image/tiff",
      "iccProfile": {
        "type": "custom",
        "name": "Press Profile",
        "imageMode": "cmyk",
        "source": { "url": "<PROFILE_ICC_GET_URL>" }
      }
    }
  ]
}
```

## Destinations

Each `destination` uses exactly one of these forms.

| Form | Fields | Result |
|---|---|---|
| [Pre-signed URL](../shared-reference/input-files-and-storage.md#create-signed-urls) | `url` (HTTPS), `storageType` required for Azure or Dropbox (`azure` or `dropbox`; see [storage type](../shared-reference/output-formats-and-options.md#url-destination)) | The file is uploaded to your URL. |
| [Creative Cloud](../shared-reference/output-formats-and-options.md#creative-cloud-destination) | `creativeCloudPath`, optional `creativeCloudProjectId` (starts with `urn:aaid:`) | The file is saved to Creative Cloud storage. |
| [Hosted](../shared-reference/output-formats-and-options.md#hosted-destination) | `validityPeriod`: seconds, 60 to 86400, default 3600 | The job status returns a temporary download URL. |
| [Embedded](../shared-reference/output-formats-and-options.md#embedded-destination) | `embedded`: `string`, `base64`, or `json`, default `string` | The job status returns the file content. |

A hosted output that stays available for 2 hours:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "outputs": [
    { "destination": { "validityPeriod": 7200 }, "mediaType": "image/png" }
  ]
}
```

## Next Steps

- [Create Composite Overview](index.md)
- [Crop, Resize, And Trim Documents](document-edits.md)
