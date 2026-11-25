---
title: Manifest Response Reference
description: Interpret document, layer, thumbnail, text, smart-object, and gradient manifest fields
keywords:
  - manifest
  - generate-manifest
  - layers
  - thumbnails
  - gradient layer
  - smart objects
hideBreadcrumbNav: true
---

# Manifest Response Reference

Use this reference with [Generate A Document Manifest](../manifest/index.md).
With an embedded JSON destination, the manifest is the object at
`result.outputs[i].destination.content` after the job succeeds; it is not the
job-status wrapper.

Paths below are relative to that manifest. `layers[]` means an element of the
`layers` array, not a literal JSON key. This reference describes useful fields
and examples, not every possible layer-specific property. Other fields may be
returned. A field described as conditional can be absent; `null`, an empty
object, and an empty array are different from an omitted field.

## Document Properties

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `document` | object | In the manifest | Document properties, including the fields below. |
| `document.bounds` | object | In the document | Canvas rectangle in pixels. See [Rectangles](#rectangles). |
| `document.depth` | integer | In the document | Bits per color channel; `8` is not a channel count. |
| `document.iccProfile` | string | When available | Color-profile name, not the profile's binary contents. |
| `document.imageMode` | string | In the document | Color mode, such as `rgb`; not an output file format. |
| `document.resolution` | object | When available | Contains a numeric `value` and a `unit`. |
| `document.resolution.unit` | string | When resolution is returned | Unit label accompanying the resolution. Do not infer a different unit from the value. |
| `document.resolution.value` | number | When resolution is returned | Resolution in the accompanying unit; not the canvas width or height. |
| `document.title` | string | When available | Document title, not a stable asset identifier. |
| `document.xmp` | string | When requested and available | Document XMP as XML. It can contain private metadata. |
| `layers` | array of objects | In the manifest | Top-level layer records. Each element has the fields described under [Layer Identity And Hierarchy](#layer-identity-and-hierarchy). |

## Rectangles

`document.bounds`, layer frames, and mask bounds use rectangle objects with
these fields. Values are pixel coordinates; the coordinate reference depends
on the containing field.

| Field | Type | Meaning |
|---|---|---|
| `left` | number | Left edge. |
| `top` | number | Top edge. |
| `right` | number | Right edge. |
| `bottom` | number | Bottom edge. |

Width is `right - left` and height is `bottom - top`. Document bounds are
measured from the document's top-left origin. A layer's `referenceFrame`,
`compositeFrame.absolute`, and `compositeFrame.relative` can differ; do not
assume they share an origin or represent the canvas rectangle.

## Layer Identity And Hierarchy

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].id` | integer | On a layer | Layer identifier within the document, not its array position. |
| `layers[].index` | integer | On a layer | Layer stacking index, distinct from its ID. |
| `layers[].name` | string | On a layer | Layer name; names need not be unique. |
| `layers[].type` | string | On a layer | Kind, such as `background_layer`, `text_layer`, `smart_object_layer`, or `gradient_layer`. |
| `layers[].visible` | boolean | On a layer | The layer's visibility setting; it does not guarantee visible pixels in the final image. |
| `layers[].protection` | array of strings | When returned | Protection settings, for example `none` or `position`; each item is one setting. |
| `layers[].linked` | array of objects | When returned | Layers linked to this layer; each item has `id`, `name`, and `type` below. An empty array contains no linked layers. |
| `layers[].linked[].id` | integer | On a linked-layer item | ID of the linked layer in the document. |
| `layers[].linked[].name` | string | On a linked-layer item | Name of the linked layer. |
| `layers[].linked[].type` | string | On a linked-layer item | Kind reported for the linked layer. |
| `layers[].children` | array of objects | For a group with children | Child layer records, each with the same applicable fields as a top-level layer. |
| `layers[].layers` | array of objects | For an artboard with children | Child layer records, each with the same applicable fields as a top-level layer. |

Walk both `children` and `layers` recursively when searching a document. The
following group is an excerpt; other layer fields are omitted:

```json
{
  "layers": [
    {
      "id": 10,
      "name": "Product",
      "type": "group_layer",
      "children": [
        { "id": 11, "name": "Headline", "type": "text_layer", "visible": true }
      ]
    }
  ]
}
```

### Layer Frames And Blending

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].compositeFrame` | object | When returned | Contains the `absolute` and `relative` layer rectangles. |
| `layers[].compositeFrame.absolute` | object | With a composite frame | Absolute composite rectangle; see [Rectangles](#rectangles). |
| `layers[].compositeFrame.relative` | object | With a composite frame | Relative composite rectangle; see [Rectangles](#rectangles). |
| `layers[].compositeDimensions` | object | When returned | Bounding rectangle of the layer's composite pixels; see [Rectangles](#rectangles). |
| `layers[].referenceFrame` | object | When returned | Layer reference rectangle; it can differ from `compositeFrame.absolute`. See [Rectangles](#rectangles). |
| `layers[].rotation` | number | When returned | Layer rotation in degrees. |
| `layers[].blendOptions` | object | When returned | Layer blending settings, including the fields below. |
| `layers[].blendOptions.blendMode` | string | With blend options | Blend mode, such as `normal`. |
| `layers[].blendOptions.clipped` | boolean | With blend options | Whether the layer is clipped to the layer below. |
| `layers[].blendOptions.fillOpacity` | number | With blend options | Fill opacity as a percentage. |
| `layers[].blendOptions.opacity` | number | With blend options | Layer opacity as a percentage. |

### Masks

Mask objects are conditional; `null` means no mask object was returned.
Rectangular `bounds` use the [rectangle fields](#rectangles).
The presence of `userMask` settings alone does not establish that a pixel
mask exists; check `pixelMask`.

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].userMask` | object | When returned | User-mask settings, containing `density` and `feather`. |
| `layers[].userMask.density` | number | With user-mask settings | Mask density as a percentage. |
| `layers[].userMask.feather` | number | With user-mask settings | Mask feather amount; the response does not include its unit. |
| `layers[].vectorMask` | object or null | When returned | Vector-mask summary, or `null` when no summary is available. |
| `layers[].vectorMask.hasMask` | boolean | When a vector-mask object is returned | Whether the vector mask is present. |
| `layers[].vectorMask.bounds` | object | When a vector-mask object is returned | Mask bounding rectangle. |
| `layers[].pixelMask` | object or null | When returned | Pixel-mask summary, or `null` when no summary is available. |
| `layers[].pixelMask.hasMask` | boolean | When a pixel-mask object is returned | Whether the pixel mask is present. |
| `layers[].pixelMask.bounds` | object | When a pixel-mask object is returned | Mask bounding rectangle. |
| `layers[].pixelMask.enabled` | boolean | When a pixel-mask object is returned | Whether the mask is enabled. |
| `layers[].pixelMask.extendOpaque` | boolean | When a pixel-mask object is returned | Whether the mask extends as opaque outside its bounds. |
| `layers[].pixelMask.linked` | boolean | When a pixel-mask object is returned | Whether the mask is linked to its layer. |
| `layers[].pixelMask.offset` | object | When a pixel-mask object is returned | Offset from the layer, containing `horizontal` and `vertical`. |
| `layers[].pixelMask.offset.horizontal` | integer | With a pixel-mask offset | Horizontal offset in pixels. |
| `layers[].pixelMask.offset.vertical` | integer | With a pixel-mask offset | Vertical offset in pixels. |

## Layer Thumbnails

With `includeLayerThumbnails: true`, an eligible layer can include:

```json
{
  "thumbnail": {
    "mediaType": "image/png",
    "url": "<THUMBNAIL_DOWNLOAD_URL>"
  }
}
```

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].thumbnail` | object | When a thumbnail was generated for the layer | Thumbnail descriptor with `mediaType` and `url`. |
| `layers[].thumbnail.mediaType` | string | With a thumbnail | Image format, such as `image/jpeg` or `image/png`. |
| `layers[].thumbnail.url` | string | With a thumbnail | Temporary download URL for this layer's preview, not the job-status URL. |

The URL is sensitive and can expire. A missing thumbnail is not the same as a
zero-sized thumbnail. See [Generate Layer Thumbnails](../manifest/index.md#generate-layer-thumbnails)
for request options.

## Text Layers

A `text_layer` can include a `text` object. Positions in character and
paragraph ranges are zero-based, inclusive UTF-16 code-unit indices, not byte
offsets. This illustrative excerpt shows an ordinary text layer with one
character-style range:

```json
{
  "type": "text_layer",
  "name": "Headline",
  "text": {
    "content": "Spring Sale",
    "characterStyles": [
      {
        "font": { "postScriptName": "ArialMT", "isAvailable": true },
        "fontSize": 36,
        "position": { "from": 0, "to": 10 }
      }
    ]
  }
}
```

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].text` | object | On a text layer | Text content and text properties, including the fields below. |
| `layers[].text.content` | string | With text data | The text in the layer. |
| `layers[].text.missingFonts` | array of strings | When fonts are missing | PostScript names of missing fonts; each item is one name. |
| `layers[].text.characterStyles` | array of objects | With text data | Character-style runs. Each item can contain `font`, `fontSize`, and `position`. |
| `layers[].text.characterStyles[].font` | object | On a character-style run | Font information with `postScriptName` and `isAvailable`. |
| `layers[].text.characterStyles[].font.postScriptName` | string | With font information | Font's PostScript name. |
| `layers[].text.characterStyles[].font.isAvailable` | boolean | With font information | Whether that font is available for the document. |
| `layers[].text.characterStyles[].fontSize` | number | When returned on a character-style run | Font size in pixels. |
| `layers[].text.characterStyles[].position` | object | On a character-style run | Inclusive character range with `from` and `to`. |
| `layers[].text.characterStyles[].position.from` | integer | With a position | Index of the first UTF-16 code unit in the run. |
| `layers[].text.characterStyles[].position.to` | integer | With a position | Index of the last UTF-16 code unit in the run, included. |
| `layers[].text.paragraphAttributes` | array of objects | With text data | Paragraph-attribute runs. Each item can contain `alignment` and `position`. |
| `layers[].text.paragraphAttributes[].alignment` | string | When returned on a paragraph run | Paragraph alignment, such as `left`. |
| `layers[].text.paragraphAttributes[].position` | object | On a paragraph run | Inclusive character range with `from` and `to`. |
| `layers[].text.paragraphAttributes[].position.from` | integer | With a position | Index of the first UTF-16 code unit in the run. |
| `layers[].text.paragraphAttributes[].position.to` | integer | With a position | Index of the last UTF-16 code unit in the run, included. |

Style-run objects can contain additional properties; the excerpt is not a
complete text-layer object.

### Dynamic Text Layers

Dynamic text layers use the same `text_layer` type as ordinary text layers.
When dynamic layout is active, the manifest includes `text.dynamicText` with
the selected layout and available relative line and word gaps.

This separate layer excerpt shows dynamic text metadata:

```json
{
  "type": "text_layer",
  "name": "Dynamic Headline",
  "text": {
    "content": "A Fresh Headline For Your Campaign",
    "dynamicText": {
      "layoutType": "block_fit",
      "lineGap": 0.5,
      "wordGap": 1.5
    }
  }
}
```

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].text.dynamicText` | object | Only when dynamic text is active | Dynamic layout metadata; omitted for ordinary text, not returned as `{ "layoutType": "none" }`. |
| `layers[].text.dynamicText.layoutType` | string | With dynamic layout metadata | Active layout, such as `block_fit`. An unrecognized layout can be reported as `unknown`; this is not a writable request value. |
| `layers[].text.dynamicText.lineGap` | number | When available with dynamic layout metadata | Relative line gap, from 0 to 2 inclusive. |
| `layers[].text.dynamicText.wordGap` | number | When available with dynamic layout metadata | Relative word gap, from 0 to 3 inclusive. |

Other text properties, such as character styles, can also be present. Ordinary
text layers omit `dynamicText`, as shown in the preceding text-layer example.

For add and edit requests, see
[Dynamic Text][dynamic-text].

## Smart Object Layers

When extraction is requested and succeeds, an embedded smart object can
contain a descriptor like this illustrative excerpt:

```json
{
  "type": "smart_object_layer",
  "smartObject": {
    "isSmartObject": true,
    "isLinked": false,
    "isValid": true,
    "extracted": {
      "mediaType": "image/png",
      "url": "<EXTRACTED_FILE_DOWNLOAD_URL>"
    }
  }
}
```

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].smartObject` | object | On a smart-object layer | Smart-object flags, data, and optional metadata or extracted content. |
| `layers[].smartObject.isSmartObject` | boolean | With smart-object data | Whether the layer is a smart object. |
| `layers[].smartObject.isLinked` | boolean | With smart-object data | `true` for externally linked content; `false` for embedded content. |
| `layers[].smartObject.isValid` | boolean | With smart-object data | Whether the smart object is reported as valid. |
| `layers[].smartObject.smartObjectData` | object | When available | Additional source and transform information; may be unavailable for an unreadable linked object. |
| `layers[].smartObject.smartObjectData.type` | string | When returned | Data type, such as `smartObject`. |
| `layers[].smartObject.smartObjectData.instanceId` | string | For embedded data when returned | Smart-object instance identifier. Treat it as an identifier, not a download link. |
| `layers[].smartObject.smartObjectData.transform` | array of numbers | When returned | Eight numeric transform coordinates describing the object's placement; no unit is included in this array. |
| `layers[].smartObject.smartObjectData.fileInfo` | object | When available | Source file information with fields such as those below. |
| `layers[].smartObject.smartObjectData.fileInfo.name` | string | When file information is returned | Source file name. |
| `layers[].smartObject.smartObjectData.fileInfo.path` | string | When returned | Stored source path; it is not necessarily a usable download URL. |
| `layers[].smartObject.smartObjectData.fileInfo.fileType` | string | When file information is returned | Source file type. |
| `layers[].smartObject.smartObjectData.fileInfo.linked` | boolean | When file information is returned | Whether the source is linked. |
| `layers[].smartObject.xmp` | string | When requested and available for embedded content | Smart-object XMP as XML. |
| `layers[].smartObject.extracted` | object | When extraction succeeds for embedded content | Descriptor containing `mediaType` and `url`. |
| `layers[].smartObject.extracted.mediaType` | string | With extracted content | Media type of the extracted file. |
| `layers[].smartObject.extracted.url` | string | With extracted content | Temporary download URL for the extracted file. |

Linked content is not extracted by `extractSmartObjectData`. The option does
not guarantee an extracted file for every embedded object; check for
`extracted` before using its URL.

## Gradient Layers

A `gradient_layer` can include a `fill` object. This illustrative partial
example shows a custom-stops gradient; it omits the layer's common fields:

```json
{
  "type": "gradient_layer",
  "fill": {
    "type": "linear",
    "angle": 90,
    "scale": 100,
    "offset": { "horizontal": 0, "vertical": 0 },
    "gradient": {
      "type": "customStops",
      "value": {
        "gradientName": "Sunset",
        "colorStops": [
          {
            "type": "user_stop",
            "location": 0,
            "midpoint": 50,
            "color": { "mode": "rgb", "depth": 16, "components": [32768, 0, 0] }
          },
          {
            "type": "user_stop",
            "location": 4096,
            "midpoint": 50,
            "color": { "mode": "rgb", "depth": 16, "components": [0, 0, 32768] }
          }
        ],
        "transparencyStops": [
          { "location": 0, "midpoint": 50, "opacity": 100 },
          { "location": 4096, "midpoint": 50, "opacity": 0 }
        ],
        "interpolation": 4096
      }
    }
  }
}
```

### Gradient Fill Fields

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].fill` | object | When gradient data is returned | Gradient fill settings. |
| `layers[].fill.type` | string | When returned | Gradient style, such as `linear` or `angle`. |
| `layers[].fill.align` | boolean | When returned | Whether the gradient is aligned with the layer. |
| `layers[].fill.angle` | number | When returned | Gradient angle in degrees. |
| `layers[].fill.dither` | boolean | When returned | Whether dithering is enabled. |
| `layers[].fill.reverse` | boolean | When returned | Whether the gradient direction is reversed. |
| `layers[].fill.scale` | number | When returned | Gradient scale as a percentage. |
| `layers[].fill.gradientAspectRatio` | number | When returned | Reported gradient aspect ratio. |
| `layers[].fill.interpolationMethod` | string | When returned | Interpolation method, such as `smooth`. |
| `layers[].fill.noisePreSeed` | number | When returned | Reported seed used for gradient noise. |
| `layers[].fill.offset` | object | When returned | Contains the `horizontal` and `vertical` offset values. |
| `layers[].fill.offset.horizontal` | number | With an offset | Horizontal offset value. The response does not include its unit. |
| `layers[].fill.offset.vertical` | number | With an offset | Vertical offset value. The response does not include its unit. |
| `layers[].fill.gradient` | object | When returned | Gradient definition with `type` and `value`. |
| `layers[].fill.gradient.type` | string | With a gradient definition | Definition kind; `customStops` uses the value fields below. Other kinds can have a different shape. |
| `layers[].fill.gradient.value` | object | With a gradient definition | Definition details; the following fields describe `customStops`. |

### Custom Stop Fields

Each `colorStops` or `transparencyStops` element is an object. Positions use
the gradient scale from `0` to `4096`; midpoints are percentages from `0` to
`100`.

| Field | Type | Presence | Meaning |
|---|---|---|---|
| `layers[].fill.gradient.value.gradientName` | string | When available | Gradient name. |
| `layers[].fill.gradient.value.colorStops` | array of objects | For `customStops` | Color stops; each element has `type`, `location`, `midpoint`, and `color`. |
| `layers[].fill.gradient.value.colorStops[].type` | string | On a color stop | Stop kind, such as `user_stop`. |
| `layers[].fill.gradient.value.colorStops[].location` | number | On a color stop | Position on the `0`–`4096` gradient scale. |
| `layers[].fill.gradient.value.colorStops[].midpoint` | number | On a color stop | Midpoint to the next stop, `0`–`100` percent. |
| `layers[].fill.gradient.value.colorStops[].color` | object | On a color stop | Color with `mode`, `depth`, and `components`. |
| `layers[].fill.gradient.value.colorStops[].color.mode` | string | With a color | Color mode, such as `rgb`. |
| `layers[].fill.gradient.value.colorStops[].color.depth` | integer | With a color | Color component bit depth. |
| `layers[].fill.gradient.value.colorStops[].color.components` | array of numbers | With a color | Color components in the order for the mode. In the example, `rgb` has red, green, and blue; at depth `16` each ranges from `0` to `32768`. |
| `layers[].fill.gradient.value.transparencyStops` | array of objects | For `customStops` | Transparency stops; each element has `location`, `midpoint`, and `opacity`. |
| `layers[].fill.gradient.value.transparencyStops[].location` | number | On a transparency stop | Position on the `0`–`4096` gradient scale. |
| `layers[].fill.gradient.value.transparencyStops[].midpoint` | number | On a transparency stop | Midpoint to the next stop, `0`–`100` percent. |
| `layers[].fill.gradient.value.transparencyStops[].opacity` | number | On a transparency stop | Opacity from `0` to `100` percent. |
| `layers[].fill.gradient.value.interpolation` | number | For `customStops` | Interpolation value on the `0`–`4096` scale. |

[//]: # (Links)
[dynamic-text]: ../create-composite/text-layers.md#dynamic-text
