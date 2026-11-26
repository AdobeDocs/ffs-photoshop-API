---
title: Add, Edit, And Delete Text Layers
description: Add, style, edit, and delete text layers in a Photoshop document with the Create Composite API.
keywords:
  - create composite
  - text layers
  - fonts
  - font color
  - character styles
  - paragraph styles
  - photoshop
hideBreadcrumbNav: true
---

# Add, Edit, And Delete Text Layers

Use `POST /v2/create-composite` to add text to a Photoshop document, restyle or
rewrite existing text layers, and delete text layers. One request can add,
edit, and delete several layers and write the result to one or more files.

## Before You Start

You need:

- An access token and client ID exported as `PS_FF_SERVICES_ACCESS_TOKEN` and
  `PS_FF_SERVICES_CLIENT_ID`. See [Authenticate](../../getting-started/index.md#1-authenticate).
- Signed URLs for your files. See
  [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
  Examples use `<SIGNED_GET_URL>` for files the API reads and
  `<SIGNED_PUT_URL>` for files it writes.
- To edit or delete a layer, its `name` or `id`. Run Generate Manifest on the
  PSD to list its layers.

Positions, sizes, and indents are in pixels.

## Request Structure

Text layer changes go in `edits.layers`. Each element is one layer operation.
Operations run in array order, so an element can refer to a layer that an
earlier element added. This request adds one text layer using the default
text styling:

```json
{
  "image": { "width": 1200, "height": 600, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Headline",
        "text": { "content": "Hello, world!" },
        "operation": { "type": "add", "placement": { "type": "top" } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<OUTPUT_PSD_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

For a headline with a specific position, size, and a bold phrase, add only
the styles you need:

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Headline",
        "text": {
          "content": "Summer Sale Starts Friday",
          "frame": { "type": "point", "origin": { "x": 60, "y": 100 } },
          "characterStyles": [
            { "characterStyle": { "font": { "postScriptName": "ArialMT" }, "fontSize": 56 } },
            { "apply": { "from": 0, "to": 10 }, "characterStyle": { "font": { "postScriptName": "Arial-BoldMT" } } }
          ]
        },
        "operation": { "type": "add", "placement": { "type": "top" } }
      }
    ]
  },
  "outputs": [
    { "destination": { "url": "<SIGNED_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" }
  ]
}
```

Save the JSON as `request.json` in your working directory, replace the
placeholders with your signed URLs, and send it:

```shell
curl -X POST https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  -H "Content-Type: application/json" \
  --data @request.json
```

An accepted request, including a delete, returns HTTP `202` and a `statusUrl`.
A successful status request returns HTTP `200`; check its response body to see
whether the job is still running, succeeded, or failed. See
[Get Job Status](../get-job-status/index.md).

### Request Fields

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `image` | `object` | Yes | — | The document to edit. Contains either `source` (`object`) with `url` (`string`), a signed URL to a PSD, or `width` and `height` (`integer`, pixels) and optional `fill` (`string`) for a new blank document. |
| `fontOptions` | `object` | No | No overrides; text without a font uses `ArialMT` | Custom fonts, default font, and missing-font handling. See [Font Options](#font-options). |
| `edits` | `object` | No | No edits | Contains `layers` (`array<object>`): layer operations, run in array order. Each element is described in [Layer Operation Fields](#layer-operation-fields). `edits` can also contain `document` (`object`) for crop, resize, and trim, which run after the layer operations; see the `Document` schema in the [API Reference](../../api/photoshop-v2/index.md). |
| `outputs` | `array<object>` | Yes | — | One to 25 files to write. Each element contains `destination` (`object`, required) with `url` (`string`), a signed URL to write to, and `mediaType` (`string`, default `image/jpeg`). Use `image/vnd.adobe.photoshop` to keep text editable, or `image/png` for a preview. For other destinations and formats, see the [API Reference](../../api/photoshop-v2/index.md). |
| `outputs[].mediaType` | `string` | No | `image/jpeg` | Use `image/vnd.adobe.photoshop` to keep text editable, or `image/png` for a preview. |

In the `Default / Omission` column, `—` means no default is documented for
an optional field, or that a required value must be supplied. On edit, omit
fields you do not want to change; the existing value is retained.

### Layer Operation Fields

Each element of `edits.layers`:

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `type` | `string` | For `add` and `edit` | — | `text_layer` for text. This guide also uses `solid_color_layer`. Not allowed with `delete`. |
| `name` | `string` | `name` or `id` for `edit` and `delete` | No default documented | Layer name. With `add`, sets the new layer's name. |
| `id` | `integer` | `name` or `id` for `edit` and `delete` | — | Layer ID from the document manifest. |
| `operation.type` | `string` | Yes | — | `add`, `edit`, or `delete`, in lowercase. The API also supports `move`; see the [API Reference](../../api/photoshop-v2/index.md). |
| `operation.placement` | `object` | For `add` | — | Where the new layer goes in the layer stack. Contains `type` and `referenceLayer`. |
| `operation.placement.type` | `string` | No | `top` | `top`, `bottom`, `above`, `below`, or `into`. This guide uses `top` and `above`. |
| `operation.placement.referenceLayer` | `object` | For `above`, `below`, and `into` | — | The layer to place relative to. Contains `id` (`integer`) or `name` (`string`). |
| `text` | `object` | For add of `text_layer`; optional for edit | No text changes on edit | Text content and styling. See [Text Fields](#text-fields). |
| `fill` | `object` | For `add` of `solid_color_layer` | — | Contains `solidColor` (`object`) with `rgb` (`object`): `red`, `green`, and `blue` (`integer`, 0 to 255). |
| `isVisible` | `boolean` | No | `true` on add; unchanged if omitted on edit | `false` hides the layer. |

For fields used by other layer types, see the [API Reference](../../api/photoshop-v2/index.md).

## Add A Text Layer

Send `type: "text_layer"`, `text.content`, and an `add` operation with a
`placement`, as in the [Request Structure](#request-structure) example. All
other fields are optional. When you send only `content`, the text is set as
point text that starts at the center of the document, in `ArialMT` at 30
pixels, black, left-aligned.

### Text Fields

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `content` | `string` | For `add` | — | The text. Start a new paragraph with `\r`. `\n` does not start a new line. |
| `frame` | `object` | No | Point text centered in the document | Position and wrapping. See [Frame Fields](#frame-fields). Omit on edit to keep the current frame. |
| `dynamicText` | `object` | No | Disabled on add; unchanged on edit | Automatic text layout and relative spacing controls. See [Dynamic Text](#dynamic-text). |
| `characterStyles` | `array<object>` | No | Default character style for new text | Styles for all or part of the text. See [Character Style Fields](#character-style-fields). |
| `paragraphStyles` | `array<object>` | No | Left-aligned paragraph | Styles for all or some paragraphs. See [Paragraph Style Fields](#paragraph-style-fields). |
| `antiAliasing` | `string` | No | `smooth` | `none`, `sharp`, `crisp`, `strong`, or `smooth`. |
| `textOrientation` | `string` | No | `horizontal` | `horizontal` or `vertical`. |

### Character Style Fields

Each element of `characterStyles` can contain `apply` (`object`, optional)
and `characterStyle` (`object`, optional). Set `characterStyle` to the
properties you want to change. `apply` selects the characters; see
[Range Fields](#range-fields). Without `apply`, the style covers all the text.

| `characterStyle` Property | Type | Default / Omission | Description |
|---|---|---|---|
| `font` | `object` | `ArialMT` for new text unless overridden by font options | Contains `postScriptName` (`string`), such as `Arial-BoldMT`. See [Fonts](#fonts). |
| `fontSize` | `number` | `30` pixels | Size in pixels. Use a positive value. |
| `fontColor` | `object` | Black | Text color. See [Font Colors](#font-colors). |
| `fontAlpha` | `number` | `1` | Opacity from `0` to `1`. |
| `syntheticBold`, `syntheticItalic`, `underline` | `boolean` | `false` | Simulated bold, simulated italic, and underline. |
| `capsOption` | `string` | `normal_caps` | `normal_caps`, `small_caps`, `all_caps`, or `all_small_caps`. |
| `autoLeading` | `boolean` | `false` for new text | `true` sets line height from the font size. |
| `lineHeight` | `number` | `36` pixels | Distance between baselines, in pixels. Used when `autoLeading` is `false`. |
| `letterSpacing` | `number` | `0` pixels | Extra spacing between characters, in pixels. Positive values add space; negative values reduce it. |

For existing text layers with residual scaling, `fontSize` and `lineHeight` are
stored unscaled and rendered with the layer's scale. To get exact rendered
pixel sizes, use `transformMode: "none"` and avoid a scaling transform.

### Range Fields

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `from` | `integer` | Yes | — | Index of the first character. The first character is `0`. Must be `0` or more. |
| `to` | `integer` | Yes | — | Index of the last character, included in the range. Must be `from` or more. |

Spaces and `\r` count as characters.

### Paragraph Style Fields

Each element of `paragraphStyles` can contain `apply` (`object`, optional; see
[Range Fields](#range-fields)) and `paragraphStyle` (`object`, optional).
Set `paragraphStyle` to the properties you want to change. Without `apply`,
the style covers every paragraph.

| `paragraphStyle` Property | Type | Default / Omission | Description |
|---|---|---|---|
| `alignment` | `string` | `left` | `left`, `center`, `right`, `justify`, `justify_left`, `justify_right`, or `justify_center`. |
| `writingDirection` | `string` | `left_to_right` | `left_to_right` or `right_to_left`. |
| `startIndent`, `endIndent` | `number` | `0` | Indent from the start and end edges, in pixels. |
| `firstLineIndent` | `number` | `0` | Extra indent for each paragraph's first line, in pixels. |
| `spaceBefore`, `spaceAfter` | `number` | `0` | Space above and below the paragraph, in pixels. |

### Frame Fields

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `type` | `string` | Yes | `point` when `frame` is omitted | `point` for one line per paragraph, or `area` for text that wraps in a box. |
| `origin` | `object` | For `point` | — | Contains `x` and `y` (`integer`). |
| `bounds` | `object` | For `area` | — | Contains `left`, `top`, `right`, and `bottom` (`integer`), measured from the document's top-left corner. |

## Style Part Of The Text

Ranges are zero-based and inclusive. For plain ASCII text like the examples
in this guide, each letter, digit, space, and punctuation mark is one index, so
a word starts at `from` and ends at `to` = `from` + its length − 1. In the
[Request Structure](#request-structure) example, `"from": 0, "to": 10` covers
`Summer Sale`, the first 11 characters. For text with accented letters, emoji,
or other non-ASCII characters, check the result before relying on computed
indices. Where ranges overlap, later
styles override earlier ones, so put the style for the whole text first.

There are two ways to make text bold:

- Set `font.postScriptName` to a bold face of the font, such as
  `Arial-BoldMT`, as in the Request Structure example. The font must be
  available; see [Fonts](#fonts).
- Set `syntheticBold` to `true` to simulate bold with the current font.

Several ranges can style one layer. This layer bolds `Members` (characters 0
to 6), italicizes `extra` (16 to 20), and underlines `10%` (22 to 24):

```json
{
  "type": "text_layer",
  "name": "Member Offer",
  "text": {
    "content": "Members save an extra 10%",
    "frame": { "type": "point", "origin": { "x": 60, "y": 200 } },
    "characterStyles": [
      { "characterStyle": { "fontSize": 40 } },
      { "apply": { "from": 0, "to": 6 }, "characterStyle": { "syntheticBold": true } },
      { "apply": { "from": 16, "to": 20 }, "characterStyle": { "syntheticItalic": true } },
      { "apply": { "from": 22, "to": 24 }, "characterStyle": { "underline": true } }
    ]
  },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

## Font Colors

Set `fontColor` to one color model. Components are whole numbers where
32768 is full intensity. Omitted components are `0`. A value out of range
returns `422`.

| Model | Properties | Range |
|---|---|---|
| `rgb` | `red`, `green`, `blue` (`integer`) | 0 to 32768 |
| `gray` | `gray` (`integer`), where `0` is black | 0 to 32768 |
| `lab` | `l` (`integer`) | 0 to 32768 |
| `lab` | `a`, `b` (`integer`) | -16384 to 16384 |

The API Reference also lists a `cmyk` model. This guide covers RGB documents;
use `rgb` for them.

To convert a 0 to 255 RGB color, calculate `round(component × 32768 / 255)`
for each component. For example, brand red 232, 70, 43 becomes 29812, 8995,
5526, and gold 255, 214, 0 becomes 32768, 27499, 0.

```json
{
  "type": "text_layer",
  "name": "Produce Banner",
  "text": {
    "content": "Fresh Picks",
    "frame": { "type": "point", "origin": { "x": 60, "y": 300 } },
    "characterStyles": [
      { "characterStyle": { "fontSize": 56, "fontColor": { "rgb": { "red": 29812, "green": 8995, "blue": 5526 } } } }
    ]
  },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

Other models use the same wrapper, for example
`{ "gray": { "gray": 16384 } }` or `{ "lab": { "l": 19661, "a": -9000, "b": -3000 } }`.
For transparency, add `fontAlpha`, such as `0.5`.

### Text Colors Versus Solid Color Layer Colors

Solid color layers use 0 to 255, not 0 to 32768. A value above 255 returns
`422`. This layer is the same red as the `Fresh Picks` text above:

```json
{
  "type": "solid_color_layer",
  "name": "Backdrop",
  "fill": { "solidColor": { "rgb": { "red": 232, "green": 70, "blue": 43 } } },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

## Line Height

The API reference gives new text a default line height of 36 pixels, even if
you set a different font size. For text with more than one line, set the line
height so lines don't overlap. Use `lineHeight` for a fixed distance between
baselines:

```json
{
  "type": "text_layer",
  "name": "Event Details",
  "text": {
    "content": "Doors open at 9 AM\rFree coffee for early birds",
    "frame": { "type": "point", "origin": { "x": 60, "y": 800 } },
    "characterStyles": [ { "characterStyle": { "fontSize": 32, "autoLeading": false, "lineHeight": 70 } } ]
  },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

Or set `"autoLeading": true` instead of `lineHeight` to space lines at about
120% of the font size.

## Letter Spacing

For a 40-pixel font, `letterSpacing: 4` adds 4 pixels between characters.
This edit applies it to an existing 40-pixel text layer:

```json
{
  "type": "text_layer",
  "name": "Tracking Zero",
  "text": { "characterStyles": [ { "characterStyle": { "letterSpacing": 4 } } ] },
  "operation": { "type": "edit" }
}
```

## Paragraph Alignment And Indents

In this area frame, the first paragraph (characters 0 to 82) is centered. The
second paragraph (characters 83 to 145) has 20-pixel start and end indents, a
40-pixel extra first-line indent, and 24 pixels of space above it.

```json
{
  "type": "text_layer",
  "name": "Event Copy",
  "text": {
    "content": "Join us for our biggest weekend of the year with new arrivals in every department.\rBring a friend and both of you save twenty percent at checkout.",
    "frame": { "type": "area", "bounds": { "left": 860, "top": 800, "right": 1500, "bottom": 1100 } },
    "characterStyles": [ { "characterStyle": { "fontSize": 28, "autoLeading": true } } ],
    "paragraphStyles": [
      { "apply": { "from": 0, "to": 82 }, "paragraphStyle": { "alignment": "center" } },
      {
        "apply": { "from": 83, "to": 145 },
        "paragraphStyle": { "alignment": "left", "startIndent": 20, "endIndent": 20, "firstLineIndent": 40, "spaceBefore": 24 }
      }
    ]
  },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

## Point Frames Versus Area Frames

| | Point Frame | Area Frame |
|---|---|---|
| Use for | Headlines and short lines | Body copy that wraps |
| Wrapping | None; each paragraph is one line | Between `left` and `right` |
| Alignment | Relative to `origin.x`: `left` starts there, `center` centers on it, `right` ends there | Relative to the box edges |

This point frame centers its line on `x = 1180`:

```json
{
  "type": "text_layer",
  "name": "Tagline",
  "text": {
    "content": "Centered on the origin",
    "frame": { "type": "point", "origin": { "x": 1180, "y": 1200 } },
    "paragraphStyles": [ { "paragraphStyle": { "alignment": "center" } } ]
  },
  "operation": { "type": "add", "placement": { "type": "top" } }
}
```

## Dynamic Text

A dynamic text layer automatically adjusts its text layout to fit a text
frame. Use it when the copy changes, such as when personalizing a headline
or reusing a campaign template with different text.

Dynamic text is a capability of a regular `text_layer`, not a separate layer
type. Configure it through `text.dynamicText` when adding or editing a text
layer. The `text` object still holds the content, frame, character styles,
and paragraph styles; `dynamicText` controls the layout mode and relative
gaps between lines and words.

### Dynamic Text Fields

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `layoutType` | `string` | Whenever `dynamicText` is supplied | No default | Selects the layout behavior. See [Layout Types](#layout-types). |
| `lineGap` | `number` | No | `0.25` for new dynamic text; unchanged when omitted on edit | Relative line gap, from `0` to `2` inclusive. Only valid with `block_fit`; not a pixel measurement. |
| `wordGap` | `number` | No | `1` for new dynamic text; unchanged when omitted on edit | Relative word gap, from `0` to `3` inclusive. Only valid with `block_fit`; not a pixel measurement. |

### Layout Types

`layoutType` is a parameter of `dynamicText`. It accepts these values:

| Value | Behavior | Requirements |
|---|---|---|
| `block_fit` | Fits the text block to its frame. | When enabling this mode, use an existing area-text layer or supply an area frame in the same operation. Optional `lineGap` and `wordGap` customize its spacing. |
| `none` | Disables dynamic text layout. | Omit `lineGap` and `wordGap`. |

`unknown` is not accepted in requests.

### Add A Dynamic Text Layer

Add a regular text layer and include `text.dynamicText`. This layer operation
selects the `block_fit` layout and supplies the required area frame. It omits
the gap parameters to use their defaults:

```json
{
  "type": "text_layer",
  "name": "Dynamic Headline",
  "operation": { "type": "add", "placement": { "type": "top" } },
  "text": {
    "content": "Make Room For Your Next Big Idea",
    "frame": {
      "type": "area",
      "bounds": { "top": 100, "left": 100, "bottom": 500, "right": 800 }
    },
    "dynamicText": { "layoutType": "block_fit" }
  }
}
```

Place this operation inside `edits.layers` in a
[Create Composite request](#request-structure).

### Edit A Dynamic Text Layer

Select an existing text layer by `name` or `id` and use an `edit` operation.
You can change its content, enable dynamic layout, or update the gap
parameters. This example replaces the content and enables dynamic text with
custom line and word gaps. It supplies an area frame so it can also be used
on a layer that is not already area text:

```json
{
  "type": "text_layer",
  "name": "Headline",
  "operation": { "type": "edit" },
  "text": {
    "content": "A Fresh Headline For Your Campaign",
    "frame": {
      "type": "area",
      "bounds": { "top": 100, "left": 100, "bottom": 500, "right": 800 }
    },
    "dynamicText": { "layoutType": "block_fit", "lineGap": 0.5, "wordGap": 1.5 }
  }
}
```

On an already-dynamic layer, repeat `layoutType: "block_fit"` when changing
only a gap. This operation preserves the content, frame, and current `wordGap`:

```json
{
  "type": "text_layer",
  "name": "Dynamic Headline",
  "operation": { "type": "edit" },
  "text": { "dynamicText": { "layoutType": "block_fit", "lineGap": 0.75 } }
}
```

Omitting `dynamicText` entirely on an edit leaves its current settings unchanged.

### Disable Dynamic Text

Set `layoutType` to `none` and omit both gap parameters:

```json
{
  "type": "text_layer",
  "name": "Dynamic Headline",
  "operation": { "type": "edit" },
  "text": { "dynamicText": { "layoutType": "none" } }
}
```

### Read Dynamic Text In A Manifest

Generate Manifest includes `layers[].text.dynamicText` for active dynamic
text, with its layout type and available line and word gaps. Ordinary text
layers omit this object. See the [Manifest Response Reference][manifest-text].

## Fonts

Refer to fonts by PostScript name, such as `ArialMT` or `Arial-BoldMT`. A
display name such as `Arial Bold` is treated as a missing font.

### Font Options

| Property | Type | Required | Default / Omission | Description |
|---|---|---|---|---|
| `additionalFonts` | `array<object>` | No | No additional fonts | Font files for this request. Each element contains `source` (`object`, required) with `url` (`string`), a signed URL to an OpenType or TrueType file. For other source types, see the [API Reference](../../api/photoshop-v2/index.md). |
| `defaultFontPostScriptName` | `string` | No | `ArialMT` | Font for text that doesn't name one, and the substitute for missing fonts. |
| `missingFontStrategy` | `string` | No | `use_default` | `use_default` or `fail`. See [Missing Fonts](#missing-fonts). |

### Use A Custom Font

Load the font file with `additionalFonts` and refer to its PostScript name.
Include the font in every request that uses it, including later edits of the
output PSD.

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL>" } },
  "fontOptions": { "additionalFonts": [ { "source": { "url": "<SIGNED_GET_URL_FOR_FONT_FILE>" } } ] },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Signature",
        "text": {
          "content": "Handmade with love",
          "frame": { "type": "point", "origin": { "x": 60, "y": 120 } },
          "characterStyles": [ { "characterStyle": { "font": { "postScriptName": "<FONT_POSTSCRIPT_NAME>" }, "fontSize": 64 } } ]
        },
        "operation": { "type": "add", "placement": { "type": "top" } }
      }
    ]
  },
  "outputs": [ { "destination": { "url": "<SIGNED_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" } ]
}
```

### Missing Fonts

A font is missing when its PostScript name isn't available and wasn't loaded
with `additionalFonts`.

| `missingFontStrategy` | Result |
|---|---|
| `use_default`, or not set | The job succeeds. The text uses `defaultFontPostScriptName` if set, otherwise `ArialMT`. |
| `fail` | The job fails with error code `missing_fonts`. |

To choose the substitute, which also applies to new text without a font:

```json
{ "fontOptions": { "defaultFontPostScriptName": "Arial-BoldMT" } }
```

With `"missingFontStrategy": "fail"`, the failed job status names the missing
fonts:

```json
{
  "jobId": "<JOB_ID>",
  "status": "failed",
  "createdTime": "2026-11-05T11:57:28.083165777",
  "modifiedTime": "2026-11-05T11:57:28.728244506",
  "errorDetails": [
    { "errorCode": "missing_fonts", "message": "Missing fonts detected: AcmeBrandSans-Bold. Strategy: FAIL" }
  ]
}
```

Each `errorDetails` element contains `errorCode` (`string`) and `message`
(`string`). For the other status fields, see [Get Job Status](../get-job-status/index.md).

## Edit An Existing Text Layer

Send `type: "text_layer"`, the layer's `name` or `id`, and
`"operation": { "type": "edit" }`, plus only what you want to change.

| You Send | Result |
|---|---|
| `characterStyles` without `apply` | The properties you send apply to all the text. Other properties, including per-range fonts and colors, are kept. |
| `characterStyles` with `apply` | Only that range changes. |
| `paragraphStyles` without `apply` | The properties you send apply to every paragraph. Other paragraph properties are kept. |
| `content` | Replaces all the text. The new text takes the style of the old text's first character, and earlier ranges are removed. To restyle it, send `characterStyles` in the same edit, with ranges that refer to the new text. |
| `frame` | Moves or reshapes the frame. |
| `isVisible: false` | Hides the layer. |

This edit sets the [Request Structure](#request-structure) headline to 72
pixels. `Summer Sale` stays bold because the edit doesn't send `font`:

```json
{
  "type": "text_layer",
  "name": "Headline",
  "text": { "characterStyles": [ { "characterStyle": { "fontSize": 72 } } ] },
  "operation": { "type": "edit" }
}
```

This edit replaces the text and bolds its first word:

```json
{
  "type": "text_layer",
  "name": "Collection Title",
  "text": {
    "content": "Spring Collection",
    "characterStyles": [ { "apply": { "from": 0, "to": 5 }, "characterStyle": { "font": { "postScriptName": "Arial-BoldMT" } } } ]
  },
  "operation": { "type": "edit" }
}
```

## Delete A Text Layer

Send only the layer's `name` or `id` and `"operation": { "type": "delete" }`.
A delete that also sends `type`, `text`, or other fields is rejected, and the
error message lists the extra fields.

The following example shows only `edits`. A complete request still needs `image` and
`outputs`, as in the [Request Structure](#request-structure) example.

```json
{
  "edits": {
    "layers": [
      { "name": "Draft Note", "operation": { "type": "delete" } },
      { "id": 8, "operation": { "type": "delete" } }
    ]
  }
}
```

## Example: Personalize A Banner Template

**Step 1: Create the template.** This request adds a red solid color layer,
two white text layers, and a note for designers. The greeting is placed
directly above the backdrop by name. Save a PSD output to reuse.

```json
{
  "image": { "width": 1200, "height": 600, "fill": "white" },
  "edits": {
    "layers": [
      {
        "type": "solid_color_layer",
        "name": "Backdrop",
        "fill": { "solidColor": { "rgb": { "red": 232, "green": 70, "blue": 43 } } },
        "operation": { "type": "add", "placement": { "type": "top" } }
      },
      {
        "type": "text_layer",
        "name": "Greeting",
        "text": {
          "content": "Hi there, your weekend offer is here",
          "frame": { "type": "area", "bounds": { "left": 60, "top": 60, "right": 1140, "bottom": 200 } },
          "characterStyles": [
            {
              "characterStyle": {
                "font": { "postScriptName": "Arial-BoldMT" },
                "fontSize": 56,
                "autoLeading": true,
                "fontColor": { "rgb": { "red": 32768, "green": 32768, "blue": 32768 } }
              }
            }
          ],
          "paragraphStyles": [ { "paragraphStyle": { "alignment": "left" } } ]
        },
        "operation": { "type": "add", "placement": { "type": "above", "referenceLayer": { "name": "Backdrop" } } }
      },
      {
        "type": "text_layer",
        "name": "Offer",
        "text": {
          "content": "Save 20% on everything until Sunday",
          "frame": { "type": "point", "origin": { "x": 60, "y": 300 } },
          "characterStyles": [
            {
              "characterStyle": {
                "font": { "postScriptName": "ArialMT" },
                "fontSize": 40,
                "fontColor": { "rgb": { "red": 32768, "green": 32768, "blue": 32768 } }
              }
            }
          ]
        },
        "operation": { "type": "add", "placement": { "type": "top" } }
      },
      {
        "type": "text_layer",
        "name": "Draft Note",
        "text": { "content": "Replace before sending", "frame": { "type": "point", "origin": { "x": 60, "y": 520 } } },
        "operation": { "type": "add", "placement": { "type": "top" } }
      }
    ]
  },
  "outputs": [ { "destination": { "url": "<SIGNED_PUT_URL>" }, "mediaType": "image/vnd.adobe.photoshop" } ]
}
```

**Step 2: Personalize it.** Use the template PSD as the input. This request
replaces the greeting, makes `20%` (characters 5 to 7) bold and gold, deletes
the note, and writes a PNG.

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL>" } },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Greeting",
        "text": { "content": "Hi Maya, your weekend offer is here" },
        "operation": { "type": "edit" }
      },
      {
        "type": "text_layer",
        "name": "Offer",
        "text": {
          "characterStyles": [
            {
              "apply": { "from": 5, "to": 7 },
              "characterStyle": {
                "font": { "postScriptName": "Arial-BoldMT" },
                "fontColor": { "rgb": { "red": 32768, "green": 27499, "blue": 0 } }
              }
            }
          ]
        },
        "operation": { "type": "edit" }
      },
      { "name": "Draft Note", "operation": { "type": "delete" } }
    ]
  },
  "outputs": [ { "destination": { "url": "<SIGNED_PUT_URL>" }, "mediaType": "image/png" } ]
}
```

The PNG shows the new greeting in bold white on red; the replacement keeps
the template's style. Below it, `Save 20% on everything until Sunday` is white
with a bold gold `20%`.

## Troubleshooting

Some errors are returned when you send the request. Others, such as
`missing_fonts` and `invalid_parameters`, are only reported in the job status
after the request is accepted with `202`. Check both.

| Symptom | Cause And Fix |
|---|---|
| `422` with `validation_error` | A field is missing or out of range. The `message` names it, for example `edits.layers[0].operation.placement: must not be null`. |
| `Invalid value '...' at path '...'. Accepted values are: ...` | The value at that path isn't allowed. Use one of the accepted values listed in the message, exactly as written. |
| `Missing required field 'type' for edit operation` | Add `"type": "text_layer"`. |
| `Either id or name is required when operation type is edit` | Add the layer's `name` or `id`. |
| `Request payload contains invalid fields` on a delete | Send only `name` or `id` and `operation`. |
| Job fails with `invalid_parameters` and `Reference layer ID or name is required for ABOVE, BELOW, INTO Placement types` | The request was accepted, but the placement has no reference layer. Add `referenceLayer` to `above`, `below`, and `into` placements. |
| Job fails with `missing_fonts` | Load the font with `additionalFonts`, correct the PostScript name, or don't use `"missingFontStrategy": "fail"`. |
| Text appears in Arial instead of your font | The font was missing and replaced. Use the PostScript name and load custom fonts with `additionalFonts`. |
| Lines overlap | Set `lineHeight` or `"autoLeading": true`. |
| A box appears where a line break should be | Use `\r`, not `\n`. |
| `Unexpected token` ... `expected closing END_OBJECT after type information` | `fontColor` contains more than one color model. Send only one, such as `rgb`. |
| `From value must be less than or equal to to value` | In `apply`, `to` is the index of the last character to style, not a length. |
| Text color is much darker than expected | `fontColor` uses 0 to 32768. Convert 0 to 255 values with `round(value × 32768 / 255)`. |
| Edited text lost its bold words | Replacing `content` applies the first character's style to all the text. Send `characterStyles` with `apply` in the same edit. |

## Next Steps

- [Get Job Status](../get-job-status/index.md): poll a job and read its outputs and errors.
- [API Reference](../../api/photoshop-v2/index.md): every Create Composite field, including other layer types and output options.

[//]: # (Links)
[manifest-text]: ../photoshop-v2/manifest-response-reference.md#dynamic-text-layers
