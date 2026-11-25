---
title: Edit Images
description: Apply automatic, light, color, effects, detail, geometry, preset, and XMP edits to an image
keywords:
  - auto tone
  - auto straighten
  - edit
  - presets
  - xmp
hideBreadcrumbNav: true
---

# Edit Images

Use `POST /v2/edit` to apply photo edits to one image and write the result as
JPEG, PNG, DNG, or XMP. Send adjustments as JSON fields, as an XMP settings
file, as Lightroom presets, or as automatic corrections.

## Before You Start

Get an [access token and API key](../../getting-started/index.md), and a
download URL for the image. The URL must stay readable while the job runs. For
accepted image types and storage options, see
[Input Files And Storage](../shared-reference/input-files-and-storage.md).

## Submit A Request

Replace `<SIGNED_GET_URL_FOR_IMAGE>` with your image's download URL. This
request applies auto tone and returns a hosted JPEG:

```shell
curl -X POST https://photoshop-api.adobe.io/v2/edit \
  -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
    "edits": { "autoTone": true },
    "outputs": [
      {
        "destination": { "validityPeriod": 3600 },
        "mediaType": "image/jpeg"
      }
    ]
  }'
```

The service returns `202 Accepted` with a `statusUrl`. Acceptance means the
request passed validation, not that the edit succeeded.

## Check The Result

Poll the `statusUrl` until `status` is `succeeded` or `failed`; see
[Job Status Response](../get-job-status/index.md#job-status-response). A
successful job lists one entry per requested output, in request order. This
excerpt omits other fields:

```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "destination": { "url": "<HOSTED_OUTPUT_URL>" },
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `result.outputs[].destination.content` | string | Embedded destinations | File content, encoded as requested in `embedded`. XMP outputs use `string`. |
| `result.outputs[].destination.url` | string | Hosted destinations | Temporary download URL, valid for `validityPeriod` seconds. |
| `result.outputs[].mediaType` | string | Always | Media type of this output, as requested. |

Download hosted outputs before the URL expires. For URL and Creative Cloud
destinations, read the file from your storage. See
[Read Output Results](../shared-reference/output-formats-and-options.md#read-output-results).

## Complete Request Examples

These are complete Edit request bodies; replace `{{INPUT_URL}}` and other
placeholder URLs with your own. Other endpoint examples are in their guides.

- [Auto Straighten](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/auto-straighten.json), [Auto Tone](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/auto-tone.json), [Color](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/color.json), [Effects](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/effects.json)
- [Light](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/light.json), [Noise And Sharpening](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/noise-and-sharpening.json), [Outputs](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/outputs.json), [Presets](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/presets.json)
- [XMP Crop](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/xmp-crop.json), [XMP Orientation](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/xmp-orientation.json), [XMP To Preset](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/xmp-to-preset.json), [XMP With Mask](https://developer.adobe.com/firefly-services/docs/photoshop/examples/edit/xmp-with-mask.json)

## Request Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `edits` | [Edits](#edits-object) object | No | None | Adjustments to apply. Omit to export the image with its existing settings. |
| `image` | [Image](#image-object) object | Yes | None | The image to edit. |
| `outputs` | array of [output](#outputs) objects | Yes | None | 1–25 outputs. See [Outputs](#outputs). |

### Image Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `source` | [source](../shared-reference/input-files-and-storage.md#where-sources-are-used) object | Yes | None | Where to read the image: `url`, `creativeCloudPath`, or `creativeCloudFileId`. See [Where Sources Are Used](../shared-reference/input-files-and-storage.md#where-sources-are-used). |

Edit reads JPEG, PNG, TIFF, WebP, PSD, DNG, and camera raw files. Raw files give the
widest editing range.

### Edits Object

Each field links to its section. Fields can be combined; see
[How Settings Combine](#how-settings-combine).

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `autoStraighten` | [Auto Straighten](#auto-straighten-object) object | No | None | Level the image automatically. |
| `autoTone` | boolean | No | `false` | `true` sets tone values automatically. See [Automatic Adjustments](#automatic-adjustments). |
| `color` | [Color](#color-object) object | No | None | Saturation, vibrance, and white balance. |
| `effects` | [Effects](#effects-object) object | No | None | Clarity, dehaze, texture, and vignette. |
| `light` | [Light](#light-object) object | No | None | Exposure and tone. |
| `noiseReduction` | [Noise Reduction](#noise-reduction-object) object | No | None | Luminance and color noise reduction. |
| `presets` | array of [source](../shared-reference/input-files-and-storage.md#where-sources-are-used) objects | No | None | 0–10 Lightroom preset files. Avoid conflicting values across presets. See [Presets](#presets). |
| `sharpen` | [Sharpen](#sharpen-object) object | No | None | Sharpening radius, detail, and edge masking. |
| `sharpness` | integer | No | `0` | Sharpening amount, 0–150. |
| `xmp` | [XMP](#xmp-object) object | No | None | XMP settings file to apply. Prefer XMP or JSON adjustment fields for a setting, not both. |

#### Neutral Starting Point

`color`, `effects`, `light`, `noiseReduction`, `sharpen`, and `sharpness` are
the JSON adjustment fields. If you send any of them, editing starts from
neutral settings: every adjustment you don't send uses the default in its
table, not the value saved with the image. An empty object, such as
`"light": {}`, also starts from neutral settings. Omit all six fields to keep
the image's own settings.

Raw files usually carry camera defaults, such as some sharpening and color
noise reduction. Set those fields explicitly when you send JSON adjustments.

Don't send `null` for an adjustment; omit the field instead.

## Automatic Adjustments

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `autoStraighten` | [Auto Straighten](#auto-straighten-object) object | No | None | Level the image. See [Geometry](#geometry). |
| `autoTone` | boolean | No | `false` | `true` sets exposure, contrast, highlights, shadows, whites, and blacks for the image. `false` and omission are equivalent. |

Auto tone runs after all other settings, so it replaces tone values from
`light`, `xmp`, or `presets`. It doesn't change the output dimensions.

The request in [Submit A Request](#submit-a-request) applies auto tone. For a
5212 × 3468 JPEG, the output is a 5212 × 3468 JPEG with corrected brightness
and contrast. To compare, submit the same request with `"autoTone": false`.

## Color

### Color Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `saturation` | integer | No | `0` | Intensity of all colors equally. −100 (grayscale) to 100. |
| `vibrance` | integer | No | `0` | Intensity of muted colors, with less effect on saturated colors and skin tones. −100 to 100. |
| `whiteBalance` | string | No | `As Shot` | White balance mode. See [White Balance Values](#white-balance-values). |

#### White Balance Values

Values are case-sensitive and include spaces.

| Value | Meaning |
|---|---|
| `As Shot` | Keep the white balance recorded with the image. |
| `Auto` | Estimate a neutral white balance from the image. |
| `Cloudy` | Light-source preset for raw files. |
| `Custom` | Use temperature and tint from an XMP file or preset. |
| `Daylight` | Light-source preset for raw files. |
| `Flash` | Light-source preset for raw files. |
| `Fluorescent` | Light-source preset for raw files. |
| `Shade` | Light-source preset for raw files. |
| `Tungsten` | Light-source preset for raw files. |

For JPEG, PNG, and TIFF inputs, use `As Shot` or `Auto`. This object has no
temperature or tint fields; to set exact values, use an [XMP file](#xmp-object)
or a [preset](#presets).

### Example: Balance Muted Colors

```json
{
  "edits": {
    "color": {
      "saturation": -20,
      "vibrance": 35,
      "whiteBalance": "Auto"
    }
  }
}
```

Use this `edits` object in the request from
[Submit A Request](#submit-a-request). Muted colors become stronger while
already saturated colors are toned down, and color casts are neutralized.

## Effects

### Effects Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `clarity` | integer | No | `0` | Midtone contrast. Positive values add punch; negative values soften. −100 to 100. |
| `dehaze` | integer | No | `0` | Positive values remove haze; negative values add it. −100 to 100. |
| `texture` | integer | No | `0` | Fine detail, such as skin or foliage. Negative values smooth it. −100 to 100. |
| `vignette` | integer | No | `0` | Negative values darken the edges; positive values lighten them. Applied after any crop. −100 to 100. |

### Example: Add Depth To A Landscape

```json
{
  "edits": {
    "effects": {
      "clarity": 25,
      "dehaze": 15,
      "texture": 20,
      "vignette": -30
    }
  }
}
```

Distant detail becomes crisper, haze is reduced, and the corners darken
slightly. Output dimensions don't change.

## Geometry

Edit can straighten an image, apply an XMP crop, and rotate or flip it. Edit
outputs have no resize fields; the output size follows the input and the crop.

| Change | How | Output Size |
|---|---|---|
| Crop | Apply an XMP file that contains a crop. | The crop size. |
| Rotate or flip | Set [`xmp.orientation`](#orientation-values). | Width and height swap for 90° rotations. |
| Straighten | Set `autoStraighten.enabled` to `true`. | Smaller than the input when `constrainCrop` is `true`. |

### Auto Straighten Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `constrainCrop` | boolean | No | `true` | `true` crops the straightened image to remove blank edges. |
| `enabled` | boolean | Yes, when `autoStraighten` is supplied | `false` | `true` straightens the image. `null` is rejected. |
| `uprightMode` | string | No | None | Perspective correction. Values: `auto`, `full`, `level`, `vertical`. Omit to level the image only. |

`{"enabled": false}` does not straighten the image. The published API
schema requires `enabled` whenever `autoStraighten` is supplied; always
set it explicitly.

### Example: Straighten A Tilted Photo

```json
{
  "edits": {
    "autoStraighten": {
      "enabled": true
    }
  }
}
```

A horizon tilted by a few degrees becomes level. The output is cropped to
remove the blank corners, so it is slightly smaller than the input.

### Example: Crop With An XMP File

Save the crop in Lightroom or Camera Raw, export the settings as an XMP file,
and apply it:

```json
{
  "edits": {
    "xmp": {
      "source": {
        "url": "<SIGNED_GET_URL_FOR_XMP>"
      }
    }
  }
}
```

The output has the crop's dimensions. All other settings in the XMP file are
applied too.

### Example: Rotate A Portrait Image

```json
{
  "edits": {
    "xmp": {
      "orientation": "right_top",
      "source": {
        "url": "<SIGNED_GET_URL_FOR_XMP>"
      }
    }
  }
}
```

`right_top` rotates the image 90° clockwise, so a 4000 × 3000 input becomes a
3000 × 4000 output, before any crop.

## Light

### Light Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `blacks` | integer | No | `0` | Black point. Negative values deepen the darkest tones. −100 to 100. |
| `contrast` | integer | No | `0` | Difference between light and dark tones. −100 to 100. |
| `exposure` | number | No | `0` | Overall brightness in stops. `1.0` doubles brightness; `-1.0` halves it. −5.0 to 5.0. |
| `highlights` | integer | No | `0` | Bright tones. Negative values recover highlight detail. −100 to 100. |
| `shadows` | integer | No | `0` | Dark tones. Positive values reveal shadow detail. −100 to 100. |
| `whites` | integer | No | `0` | White point. Positive values brighten the lightest tones. −100 to 100. |

### Example: Brighten A Backlit Portrait

```json
{
  "edits": {
    "light": {
      "blacks": -10,
      "contrast": 15,
      "exposure": 0.5,
      "highlights": -40,
      "shadows": 30,
      "whites": 10
    }
  }
}
```

The image is half a stop brighter, the shadowed face is lifted, and the bright
sky keeps its detail. Output dimensions don't change.

## Noise Reduction And Sharpening

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `noiseReduction` | [Noise Reduction](#noise-reduction-object) object | No | None | Reduce grain and color speckles. |
| `sharpen` | [Sharpen](#sharpen-object) object | No | None | Shape the sharpening. Has no visible effect while `sharpness` is `0`. |
| `sharpness` | integer | No | `0` | Sharpening amount. 0–150. |

### Noise Reduction Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `color` | integer | No | `0` | Removes color speckles. 0–100. |
| `luminance` | integer | No | `0` | Smooths grain. High values can soften detail. 0–100. |

### Sharpen Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `detail` | integer | No | `25` | How much fine detail is sharpened. Higher values sharpen texture. 0–100. |
| `edgeMasking` | integer | No | `0` | Limits sharpening to edges. Higher values leave flat areas, such as skies, unsharpened. 0–100. |
| `radius` | number | No | `1.0` | Size of the sharpened detail, in pixels. 0.5 to 3.0. |

### Example: Clean Up A Low-Light Photo

```json
{
  "edits": {
    "noiseReduction": {
      "color": 25,
      "luminance": 30
    },
    "sharpen": {
      "detail": 30,
      "edgeMasking": 40,
      "radius": 1.2
    },
    "sharpness": 60
  }
}
```

Grain and color speckles are reduced, then edges are sharpened while smooth
areas stay clean.

## Presets And XMP

Use an XMP file to apply a complete set of saved edits, and presets to layer
reusable looks on top.

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `presets` | array of [source](../shared-reference/input-files-and-storage.md#where-sources-are-used) objects | No | None | Lightroom preset files (`.xmp`), 0–10 elements. Each element is a source object, such as `{ "url": "..." }`. Avoid conflicting values across presets. |
| `xmp` | [XMP](#xmp-object) object | No | None | XMP settings file for this image. |

### XMP Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `masks` | array of [Mask](#mask-object) objects | No | None | Mask files that the XMP file's local adjustments reference. |
| `orientation` | string | No | Orientation in the XMP file | Overrides the orientation. See [Orientation Values](#orientation-values). |
| `source` | [source](../shared-reference/input-files-and-storage.md#where-sources-are-used) object | Yes | None | Where to read the XMP file: `url`, `creativeCloudPath`, or `creativeCloudFileId`. Inline content is not accepted. |

For predictable results, use either XMP or JSON adjustment fields for a
setting, not both.

#### Mask Object

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `digest` | string | Yes | None | The digest that the XMP file uses to reference this mask. |
| `source` | [source](../shared-reference/input-files-and-storage.md#where-sources-are-used) object | Yes | None | Where to read the mask file. |

#### Orientation Values

| Value | Result |
|---|---|
| `bottom_left` | Flip vertically. |
| `bottom_right` | Rotate 180°. |
| `left_bottom` | Rotate 90° counterclockwise. |
| `left_top` | Flip horizontally, then rotate 90° counterclockwise. |
| `right_bottom` | Flip horizontally, then rotate 90° clockwise. |
| `right_top` | Rotate 90° clockwise. |
| `top_left` | No rotation or flip. |
| `top_right` | Flip horizontally. |

### Presets

Each preset can provide values for image settings. If multiple presets set the
same field, inspect the output before relying on which value takes effect.

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL_FOR_IMAGE>"
    }
  },
  "edits": {
    "presets": [
      {
        "url": "<SIGNED_GET_URL_FOR_PRESET_1>"
      },
      {
        "url": "<SIGNED_GET_URL_FOR_PRESET_2>"
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "validityPeriod": 3600
      },
      "mediaType": "image/png",
      "compression": "medium"
    }
  ]
}
```

This request supplies two presets. Check the returned image to confirm how
they combine for your settings.

### Example: Apply Local Adjustments

```json
{
  "edits": {
    "xmp": {
      "masks": [
        {
          "digest": "<MASK_DIGEST>",
          "source": {
            "url": "<SIGNED_GET_URL_FOR_MASK>"
          }
        }
      ],
      "source": {
        "url": "<SIGNED_GET_URL_FOR_XMP>"
      }
    }
  }
}
```

Send one `masks` element for each mask file the XMP file references.

## Outputs

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `compression` | string | No | `medium` | `image/png` only. See [PNG Options](../shared-reference/output-formats-and-options.md#png-options). |
| `destination` | [destination](../shared-reference/output-formats-and-options.md#choose-a-destination) object | Yes | None | See [Choose A Destination](../shared-reference/output-formats-and-options.md#choose-a-destination). |
| `mediaType` | string | Yes | None | Values: `application/rdf+xml`, `image/jpeg`, `image/png`, `image/x-adobe-dng`. |
| `preset` | boolean | No | `false` | `application/rdf+xml` only. `true` writes a Lightroom preset; `false` writes an XMP file of the applied settings. |
| `quality` | string | No | `photoshop_max` | `image/jpeg` only. See [JPEG Options](../shared-reference/output-formats-and-options.md#jpeg-options). |

| `mediaType` | Writes |
|---|---|
| `application/rdf+xml` | The applied settings as XMP. Use an `embedded` destination with `string`, or a file destination. `json` is rejected. |
| `image/jpeg` | The edited image as JPEG. |
| `image/png` | The edited image as PNG. |
| `image/x-adobe-dng` | The edited image as DNG. No format options. |

### Example: Write Several Formats

The first request uses the default JPEG quality. To set it explicitly, use:

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "edits": { "autoTone": true },
  "outputs": [
    {
      "destination": { "validityPeriod": 3600 },
      "mediaType": "image/jpeg",
      "quality": "photoshop_max"
    }
  ]
}
```

To request multiple formats instead:

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL_FOR_IMAGE>"
    }
  },
  "edits": {
    "autoTone": true
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_PUT_URL>"
      },
      "mediaType": "image/jpeg",
      "quality": "high"
    },
    {
      "destination": {
        "validityPeriod": 3600
      },
      "mediaType": "image/png",
      "compression": "medium"
    },
    {
      "destination": {
        "validityPeriod": 3600
      },
      "mediaType": "image/x-adobe-dng"
    },
    {
      "destination": {
        "embedded": "string"
      },
      "mediaType": "application/rdf+xml"
    }
  ]
}
```

The JPEG is written to your URL. The PNG and DNG get hosted download URLs. The
XMP is returned as text in `result.outputs[3].destination.content`.

### Example: Save An XMP File As A Preset

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL_FOR_IMAGE>"
    }
  },
  "edits": {
    "xmp": {
      "source": {
        "url": "<SIGNED_GET_URL_FOR_XMP>"
      }
    }
  },
  "outputs": [
    {
      "destination": {
        "validityPeriod": 3600
      },
      "mediaType": "image/jpeg",
      "quality": "photoshop_max"
    },
    {
      "destination": {
        "embedded": "string"
      },
      "mediaType": "application/rdf+xml",
      "preset": true
    }
  ]
}
```

The first output is the edited JPEG. The second is a Lightroom preset that you
can pass in `presets` to apply the same look to other images:

```xml
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="" ...>
      ...
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
```

## How Settings Combine

For predictable results, avoid competing values across XMP, JSON adjustments,
presets, and automatic tone settings.

| Combination | Result |
|---|---|
| `autoStraighten` and an XMP crop | Both can affect output dimensions. Use one crop source per request. |
| `autoTone` and explicit tone settings | Use auto tone for automatic values. If you need exact tone values, avoid combining it with explicit tone settings. |
| `presets` and JSON adjustments | Avoid setting the same field in both; inspect the output when combining them. |
| `presets` and `xmp` | Avoid conflicting values across presets and XMP; inspect the output when combining them. |
| `sharpen` without `sharpness` | No visible sharpening, because `sharpness` defaults to `0`. |
| `xmp` and JSON adjustments | Use one source for each setting. Do not rely on both sources to apply or override the same value. |

| Value | Same As Omitting? |
|---|---|
| `"autoStraighten": {"enabled": false}` | Yes. |
| `"autoTone": false` | Yes. |
| `"light": {}` or any empty JSON adjustment object | No. Starts from [neutral settings](#neutral-starting-point). |
| `"presets": []` | Yes. |
| `null` for any field | No. `"enabled": null` is rejected; omit fields instead. |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `422` response | A field is out of range, misspelled, or has the wrong type. Check the tables above. White balance values are case-sensitive. |
| Adjustments have unexpected values | Avoid sending the same setting through XMP, presets, and JSON. Check one source at a time. |
| Exposure or contrast differ from the request | `autoTone` is `true`; it replaces tone values. |
| Job fails with `download_error` | The image, XMP, preset, or mask URL is not readable. Use a fresh URL. |
| Raw image looks softer or noisier than expected | JSON adjustments start from neutral settings. Set `sharpness` and `noiseReduction`. |

For error codes, retries, and limits, see
[Errors And Limits](../errors-and-limits/index.md).
