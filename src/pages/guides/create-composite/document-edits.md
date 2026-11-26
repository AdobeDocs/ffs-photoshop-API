---
title: Crop, Resize, And Trim Documents
description: Crop, resize, and trim a whole document with the Create Composite API.
keywords:
  - create composite
  - document edits
  - crop
  - resize
  - trim
hideBreadcrumbNav: true
---

# Crop, Resize, And Trim Documents

Use `edits.document` in `POST /v2/create-composite` to change the whole
canvas. For the rest of the request, see the
[Create Composite Overview](index.md).

## Order Of Edits

Document edits run after every layer operation in `edits.layers`. They run
in this fixed order, whatever their order in the JSON:

1. `crop`
2. `resize`
3. `trim`

Crop bounds are therefore measured on the original canvas, and a resize
applies to the cropped canvas.

## Document Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `edits.document` | object | No | — | Contains any of `crop`, `resize`, and `trim`. |
| `edits.document.crop` | object | No | — | See [Crop Fields](#crop-fields). |
| `edits.document.resize` | object | No | — | See [Resize Fields](#resize-fields). |
| `edits.document.trim` | object | No | — | See [Trim Fields](#trim-fields). |

In the `Default` column, `—` means no default is documented for an optional
field, or that a required field must be supplied. Omit an edit operation
when you do not want that change.

## Crop A Document

This request crops a 1200 × 600 pixel PSD to its central 800 × 400 pixels and
saves the edited PSD:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "document": {
      "crop": { "bounds": { "left": 200, "top": 100, "right": 1000, "bottom": 500 } }
    }
  },
  "outputs": [
    { "destination": { "url": "<CROPPED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Bounds are pixel coordinates from the top-left corner of the canvas. The
result is `right − left` wide and `bottom − top` high:

| Result | Calculation | Pixels |
|---|---|---:|
| Width | 1000 − 200 | 800 |
| Height | 500 − 100 | 400 |

### Crop Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `crop.bounds` | object | Yes | — | Area to keep, in pixels. |
| `crop.bounds.left` | integer | Yes | — | Left edge. At least 0 and less than `right`. |
| `crop.bounds.top` | integer | Yes | — | Top edge. At least 0 and less than `bottom`. |
| `crop.bounds.right` | integer | Yes | — | Right edge. At most the canvas width. |
| `crop.bounds.bottom` | integer | Yes | — | Bottom edge. At most the canvas height. |
| `crop.hide` | boolean | No | `false` | `false` deletes pixels outside the bounds. `true` hides them so they can be recovered in the PSD. |

Bounds outside the canvas, negative values, reversed edges, or a zero-sized
area make the job fail.

## Resize A Document

This request scales a PSD to 50% of its width and 75% of its height:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "document": {
      "resize": {
        "width": { "value": 50, "unit": "percent_unit" },
        "height": { "value": 75, "unit": "percent_unit" },
        "constrainProportions": false
      }
    }
  },
  "outputs": [
    { "destination": { "url": "<RESIZED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

For a 1200 × 600 pixel document, the result is 600 × 450 pixels:

| Result | Calculation | Pixels |
|---|---|---:|
| Width | 1200 × 50 ÷ 100 | 600 |
| Height | 600 × 75 ÷ 100 | 450 |

Set `constrainProportions` to `false` when width and height change by
different amounts. With the default `true`, the width-to-height ratio is
kept.

### Resize In Points

With `points_unit`, the value is converted to pixels using the document's
resolution: `round(points × resolution ÷ 72)`. The `resize.resolution` field
does not affect this conversion.

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "document": {
      "resize": {
        "width": { "value": 144, "unit": "points_unit" },
        "height": { "value": 108, "unit": "points_unit" },
        "constrainProportions": false
      }
    }
  },
  "outputs": [
    { "destination": { "url": "<RESIZED_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

| Document resolution | Width | Height |
|---|---:|---:|
| 72 ppi | round(144 × 72 ÷ 72) = 144 px | round(108 × 72 ÷ 72) = 108 px |
| 300 ppi | round(144 × 300 ÷ 72) = 600 px | round(108 × 300 ÷ 72) = 450 px |

A converted value above 32,000 pixels makes the job fail.

### Resize Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `resize.width` | object | No | — | Target width. See [Dimension Fields](#dimension-fields). |
| `resize.height` | object | No | — | Target height. See [Dimension Fields](#dimension-fields). |
| `resize.resolution` | object | No | — | New resolution. Contains `value` and `unit`. |
| `resize.resolution.value` | integer | Yes, in `resolution` | — | Pixels per inch, at least 1. |
| `resize.resolution.unit` | string | No | `density_unit` | Only `density_unit`. |
| `resize.resample` | string | No | `bilinear` | `nearest_neighbor`, `bilinear`, `bicubic`, `bicubic_smoother`, or `bicubic_sharper`. |
| `resize.constrainProportions` | boolean | No | `true` | `true` keeps the width-to-height ratio. |
| `resize.scaleStyles` | boolean | No | `true` | `true` scales layer effects with the document. |
| `resize.rasterize` | boolean | No | — | `true` rasterizes layers when needed to resize them. |

#### Dimension Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `value` | integer | Yes | — | Size, at least 0, in `unit`. |
| `unit` | string | No | `pixels_unit` | `pixels_unit`, `percent_unit` (of the current size), or `points_unit`. |

## Trim A Document

This request removes transparent pixels from the edges of a document:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "document": { "trim": { "trimUpon": "transparent_pixels" } }
  },
  "outputs": [
    { "destination": { "url": "<TRIMMED_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

### Trim Fields

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `trim.trimUpon` | string | Yes | — | Only `transparent_pixels`. A missing, empty, or other value fails the request or the job. |

## Combine Document Edits

This request crops, then resizes, then trims, in that order:

```json
{
  "image": { "source": { "url": "<INPUT_PSD_GET_URL>" } },
  "edits": {
    "document": {
      "trim": { "trimUpon": "transparent_pixels" },
      "resize": { "width": { "value": 400, "unit": "pixels_unit" } },
      "crop": { "bounds": { "left": 0, "top": 0, "right": 800, "bottom": 800 } }
    }
  },
  "outputs": [
    { "destination": { "url": "<EDITED_PNG_PUT_URL>" }, "mediaType": "image/png" }
  ]
}
```

For a source of at least 800 × 800 pixels, the crop keeps the top-left
800 × 800 pixels, the resize scales them to 400 pixels wide with the ratio
kept, and the trim removes transparent edges from the result.

## Next Steps

- [Create Composite Overview](index.md)
- [Export Documents And Layers](export-documents-and-layers.md)
