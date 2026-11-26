---
title: Output Formats And Options
description: Choose where Photoshop V2 requests write outputs, which formats they produce, and which export options apply.
keywords:
  - outputs
  - destination
  - media type
  - JPEG
  - PNG
  - PSD
  - signed URL
hideBreadcrumbNav: true
---

# Output Formats And Options

Each Photoshop V2 request has an `outputs` array of 1 to 25 output objects.
Each output object names a destination and a file format. The service writes
every output when the job succeeds.

## Output Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `destination` | object | Yes | None | Where to write the file. One of the types in [Choose A Destination](#choose-a-destination). |
| `mediaType` | string | See [Media Types By Endpoint](#media-types-by-endpoint) | See [Media Types By Endpoint](#media-types-by-endpoint) | Output file format. |

Format-specific fields are in [Format Options](#format-options). Export fields
for resizing, cropping, layers, and color profiles are in
[Resize, Crop, And Layer Export](#resize-crop-and-layer-export) and
[ICC Profiles](#icc-profiles).

## Choose A Destination

Use one of these `destination` objects. Include the fields of only one type.
The service selects the type from the fields present.

| Destination Type | Use When |
|---|---|
| [Creative Cloud Destination](#creative-cloud-destination) | You want the file in Creative Cloud storage. |
| [Embedded Destination](#embedded-destination) | You want the file content in the job status response. |
| [Hosted Destination](#hosted-destination) | You want a temporary download URL without managing storage. |
| [URL Destination](#url-destination) | You want the file in your own storage through a signed URL. |

### Creative Cloud Destination

```json
{ "destination": { "creativeCloudPath": "<CREATIVE_CLOUD_PATH>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `creativeCloudPath` | string | Yes | None | Path to write in Creative Cloud storage. Must not be blank. |
| `creativeCloudProjectId` | string | No | None | Project that contains the path. Starts with `urn:aaid:` (case-insensitive). |

The access token must belong to an account that can write to the path.

### Embedded Destination

```json
{ "destination": { "embedded": "string" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `embedded` | string | Yes | None | Encoding of the content in the status response. Values: `base64`, `json`, `string`. Include this field to select an embedded destination. |

| Value | Use For | `content` Type |
|---|---|---|
| `base64` | Binary files | string (Base64) |
| `json` | JSON outputs | object |
| `string` | Text outputs, such as XMP | string (UTF-8) |

XMP outputs from Edit don't accept `json`.

For Create Composite image outputs, use a [URL destination](#url-destination)
or a [hosted destination](#hosted-destination).

### Hosted Destination

```json
{ "destination": { "validityPeriod": 3600 } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `validityPeriod` | integer | Yes | None | Seconds the download URL stays valid. From 60 to 86,400. Include this field to select a hosted destination. |

Download the file with `GET` from the returned URL before the period ends.
Follow redirects; the URL needs no authentication.

### URL Destination

```json
{ "destination": { "url": "<SIGNED_PUT_URL>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `storageType` | string | Required for Azure or Dropbox | None | Storage that issued the URL. Values: `azure`, `dropbox`. Omit for other URLs that accept an HTTP `PUT`, such as an Amazon S3 presigned `PUT` URL. |
| `url` | string | Yes | None | Signed HTTPS URL that accepts the file. Same host and port rules as [input URLs][input-url-requirements]. |

| Storage | `storageType` | URL To Supply |
|---|---|---|
| Amazon S3 or another `PUT` URL | Omit | Presigned `PUT` URL |
| Azure Blob Storage | `azure` | Blob URL with a SAS token that grants create and write (`cw`) |
| Dropbox | `dropbox` | Temporary upload link from the Dropbox `files/get_temporary_upload_link` API |

If your signed URL restricts the content type, sign it for the output's
`mediaType`. Keep the URL valid until the job finishes. To create signed URLs,
see [Create Signed URLs][create-signed-urls].

## Read Output Results

When the job succeeds, [Get Job Status][job-status] lists outputs in
`result.outputs`, one element per written file.

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `result.outputs[].destination.content` | object or string | Embedded destinations | File content, encoded as requested in `embedded`. |
| `result.outputs[].destination.url` | string | Destinations with a URL | For hosted destinations, the temporary download URL, valid for `validityPeriod` seconds. |

For URL and Creative Cloud destinations, read the file from your storage. If an
embedded output has no `content`, write that output to a URL or hosted
destination instead.

## Media Types By Endpoint

| Endpoint | `mediaType` Values | Default |
|---|---|---|
| Create Artboard | `image/jpeg`, `image/png`, `image/tiff`, `image/vnd.adobe.photoshop` | `image/jpeg` |
| Create Composite | `image/jpeg`, `image/png`, `image/tiff`, `image/webp`, `image/vnd.adobe.photoshop` | `image/jpeg` |
| Edit | `application/rdf+xml` (XMP), `image/jpeg`, `image/png`, `image/x-adobe-dng` (DNG) | None; required |
| Execute Actions | `application/json`, `image/jpeg`, `image/png`, `image/tiff`, `image/vnd.adobe.photoshop` | `image/jpeg` |
| Generate Manifest | `application/json` | `application/json` |

Set `mediaType` explicitly on every output. An unsupported value is rejected
when you submit the request (HTTP 422).

For Execute Actions `application/json` outputs and script outputs, see
[Execute Actions][execute-actions].

## Format Options

Add these fields to an output object with the matching `mediaType`.

### JPEG Options

Applies to `image/jpeg` outputs from Create Artboard, Create Composite, Edit,
and Execute Actions.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `quality` | string | No | `photoshop_max` | Compression quality. Values: `very_poor`, `poor`, `low`, `medium`, `high`, `maximum`, `photoshop_max`. |
| `scan` | object | No | Baseline standard | Create Artboard and Create Composite only. A [JPEG Scan Object](#jpeg-scan-object). |

#### JPEG Scan Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `optimized` | boolean | No | `false` | Optimized baseline encoding. Only with `type` `baseline`. |
| `scans` | integer | No | `3` | Number of progressive scans: 3, 4, or 5. Only with `type` `progressive`. |
| `type` | string | No | `baseline` | Encoding. Values: `baseline`, `progressive`. |

### PNG Options

Applies to `image/png` outputs from Create Artboard, Create Composite, Edit,
and Execute Actions.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `compression` | string | No | `medium` for Edit; `default` for the other endpoints above | Compression level. Values: `none`, `very_low`, `low`, `medium_low`, `medium`, `medium_high`, `default`, `high`, `very_high`, `maximum`. |

### WebP Options

Applies to `image/webp` outputs from Create Composite only.

WebP exports use `compression: "lossy"` (the default) or `"lossless"`.
For lossy compression, `quality` is an integer from 0 to 100 and defaults
to 100; omit `quality` for lossless compression. Optional `includeEXIFData`,
`includePsExtras`, and `includeXMPData` booleans default to `false`.
Resizing, ICC profiles, animation, and content credential signing are not
supported for WebP.

### PSD And TIFF Options

`image/vnd.adobe.photoshop` and `image/tiff` outputs have no format-specific
fields.

### XMP Options

Applies to `application/rdf+xml` outputs from Edit.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `preset` | boolean | No | `false` | `true` writes a Lightroom preset instead of an XMP sidecar of the applied settings. |

DNG outputs have no format-specific fields.

## Resize, Crop, And Layer Export

Applies to outputs from Create Artboard, Create Composite, and Execute Actions.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `cropMode` | string | No | None | Crop of the exported image. Values: `document_bounds`, `layer_bounds`, `trim_to_transparency`. `layer_bounds` requires exactly one element in `layers`. |
| `height` | integer | No | None | Output height in pixels. Minimum 0. |
| `layers` | array of [Export Layer](#export-layer-object) objects | No | None | Layers to export instead of the whole document. Up to 100 elements. |
| `maxWidth` | integer | No | None | Maximum output width in pixels. A wider result is scaled down to this width. Minimum 0. |
| `resample` | string | No | `bicubic_sharper` when `width` or `maxWidth` is set | Resampling method. Values: `bicubic`, `bicubic_sharper`, `bicubic_smoother`, `bilinear`, `nearest_neighbor`. |
| `width` | integer | No | None | Output width in pixels. Minimum 0. |

### Export Layer Object

Identify each layer by `id`, `name`, or both. Use Generate Manifest to find
layer IDs and names.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `id` | integer | One of `id`, `name` | None | Layer ID. |
| `name` | string | One of `id`, `name` | None | Layer name. Use a unique name. |
| `shouldIncludeChildren` | boolean | No | `true` | For a group, whether to include its child layers. |

## ICC Profiles

Applies to JPEG, PNG, PSD, and TIFF outputs from Create Artboard,
Create Composite, and Execute Actions.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `iccProfile` | object | No | None | A [Standard ICC Profile Object](#standard-icc-profile-object) or a [Custom ICC Profile Object](#custom-icc-profile-object). |

### Custom ICC Profile Object

```json
{
  "iccProfile": {
    "type": "custom",
    "name": "<PROFILE_NAME>",
    "imageMode": "cmyk",
    "source": { "url": "<SIGNED_GET_URL_FOR_ICC_FILE>" }
  }
}
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `imageMode` | string | No | None | Color mode of the output. Values: `cmyk`, `grayscale`, `rgb`. |
| `name` | string | Yes | None | Descriptive profile name. Up to 255 characters. |
| `source` | object | Yes | None | ICC profile file (`.icc` or `.icm`). A [source object][input-sources]. |
| `type` | string | Yes | None | Must be `custom`. |

### Standard ICC Profile Object

```json
{ "iccProfile": { "type": "standard", "name": "Adobe RGB (1998)", "imageMode": "rgb" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `imageMode` | string | No | None | Color mode of the output. Values: `grayscale`, `rgb`. |
| `name` | string | No | `sRGB IEC61966-2.1` | Profile name. Values are listed below. |
| `type` | string | Yes | None | Must be `standard`. |

Standard profile names:

- `Adobe RGB (1998)`
- `Apple RGB`
- `ColorMatch RGB`
- `Dot Gain 10%`
- `Dot Gain 15%`
- `Dot Gain 20%`
- `Dot Gain 25%`
- `Dot Gain 30%`
- `Gray Gamma 1.8`
- `Gray Gamma 2.2`
- `sRGB IEC61966-2.1`

## Write Multiple Outputs

Add one output object per file. Outputs can use different destinations and
formats. This Create Composite request writes a PSD and a PNG to your storage
and a JPEG to a hosted URL:

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_INPUT_PSD>" } },
  "outputs": [
    {
      "destination": { "url": "<SIGNED_PUT_URL_FOR_PSD>" },
      "mediaType": "image/vnd.adobe.photoshop"
    },
    {
      "destination": { "validityPeriod": 3600 },
      "mediaType": "image/jpeg",
      "quality": "high",
      "maxWidth": 1200
    },
    {
      "destination": { "url": "<SIGNED_PUT_URL_FOR_PNG>" },
      "mediaType": "image/png"
    }
  ]
}
```

Use a different signed URL for each URL destination.

## Troubleshoot Outputs

| Symptom | Likely Cause | Fix |
|---|---|---|
| Embedded output has no `content` | The endpoint doesn't return that output inline. | Write the output to a [URL](#url-destination) or [hosted](#hosted-destination) destination. |
| HTTP 422 for `cropMode` | `layer_bounds` is used without exactly one layer in `layers`. | Export one layer, or use `document_bounds` or `trim_to_transparency`. |
| HTTP 422 for `destination` | The fields match no destination type, or `storageType` isn't `azure` or `dropbox`. | Use the fields of one [destination type](#choose-a-destination). |
| HTTP 422 for `iccProfile` | The profile or image mode is unsupported for the selected output. | Use a supported profile and output format. |
| HTTP 422 for `mediaType` | The endpoint doesn't support the value. | Use a value from [Media Types By Endpoint](#media-types-by-endpoint). |
| HTTP 422 for `validityPeriod` | The value is below 60 or above 86,400. | Use a value from 60 to 86,400. |
| Job fails writing an output | The signed URL expired, lacks write access, or has the wrong `storageType`. | Create a new signed URL with write access and a longer expiry; match `storageType` to the storage. |

[//]: # (Links)
[create-signed-urls]: input-files-and-storage.md#create-signed-urls
[execute-actions]: ../execute-actions/index.md
[input-sources]: input-files-and-storage.md#specify-a-source
[input-url-requirements]: input-files-and-storage.md#url-requirements
[job-status]: ../get-job-status/index.md
