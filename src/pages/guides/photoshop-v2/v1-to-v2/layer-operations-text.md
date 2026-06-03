---
title: Text Layer Operations Migration
description: Migrate text layer operations from V1 /documentCreate and /documentOperations to V2 /create-composite
hideBreadcrumbNav: true
keywords:
  - text layers
  - typography
  - fonts
  - character styles
  - migration
  - v1 to v2
---

# Text Layer Operations Migration

This guide helps you migrate text layer operations from V1's `/documentCreate` and `/documentOperations` endpoints to V2's unified `/create-composite` endpoint.

## Overview

**V1 Endpoints:**

- `/pie/psdService/documentCreate` - Create documents with text layers
- `/pie/psdService/documentOperations` - Add/edit text layers

**V2 Endpoint:** `/v2/create-composite` with `edits.layers` containing text layer operations

## Creating text layers

### V1 approach: documentCreate

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentCreate \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "options": {
    "document": {
      "width": 1000,
      "height": 1000,
      "resolution": 72,
      "fill": "white",
      "mode": "rgb"
    },
    "layers": [
      {
        "type": "textLayer",
        "name": "My Title",
        "text": {
          "content": "Hello World",
          "characterStyles": [
            {
              "fontSize": 48,
              "fontName": "Arial-BoldMT",
              "fontColor": {
                "rgb": {
                  "red": 255,
                  "green": 0,
                  "blue": 0
                }
              }
            }
          ],
          "paragraphStyles": [
            {
              "alignment": "center"
            }
          ]
        }
      }
    ]
  },
  "outputs": [{
    "href": "<SIGNED_POST_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

### V2 approach

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "document": {
    "width": 1000,
    "height": 1000,
    "resolution": {"unit": "density_unit", "value": 72},
    "fill": {
      "solidColor": {
        "red": 255,
        "green": 255,
        "blue": 255
      }
    },
    "mode": "rgb"
  },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "My Title",
        "text": {
          "content": "Hello World",
          "antiAliasing": "smooth",
          "textOrientation": "horizontal",
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 48,
                "font": {
                  "postScriptName": "ArialMT"
                },
                "fontColor": {
                  "rgb": {
                    "red": 255,
                    "green": 0,
                    "blue": 0
                  }
                }
              }
            }
          ],
          "paragraphStyles": [
            {
              "paragraphStyle": {
                "alignment": "center"
              }
            }
          ]
        },
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

## Key migration changes

### 1. Layer type name

**V1:** `"type": "textLayer"`

**V2:** `"type": "text_layer"`

> **`type` is required on every layer entry in `edits.layers[]`.** V1 allowed omitting `type` for simple visibility or property-only edits on existing layers; V2 always requires it. Error when omitted: `Missing required field 'type' for edit operation at path 'edits.layers[N]'`.

### 2. Character styles structure

<InlineAlert variant="warning" slots="text"/>

**Breaking change: character (and paragraph) style range semantics differ between V1 and V2.** In V1, the `to` field on a character or paragraph style range entry was interpreted as a **length** — so `from: 0, to: 5` meant "5 characters starting at index 0" (indices 0-4). In V2, `apply.to` is an **inclusive end index** (0-based) — so `apply: {from: 0, to: 4}` means "characters at indices 0, 1, 2, 3, 4" (the first 5 characters). When migrating V1 ranges to V2, set `apply.to` to the **last character index** you want to style, not a length.

**Off-by-one example** — styling the word "Hello" in "Hello World":

```json
// V1: to=5 means length 5 → characters 0,1,2,3,4
{"from": 0, "to": 5, "fontName": "Arial-BoldMT"}

// V2: to=4 is the inclusive end index → characters 0,1,2,3,4 (same result)
{"apply": {"from": 0, "to": 4}, "characterStyle": {"font": {"postScriptName": "Arial-BoldMT"}}}
```

**characterStyles with no range (implicit full-string in V1):** If a V1 `characterStyle` entry has **neither** `from` nor `to` (applies to the entire content implicitly), `apply` is optional in V2. Omitting `apply` applies the style to the entire text content. You may include `apply: {from: 0, to: len(text.content) - 1}` explicitly if you prefer, but it is not required.

**V1:** Direct properties in `characterStyles` array. The range is given with `from` and `to` on each item (no `apply` wrapper):

```json
{
  "characterStyles": [
    {
      "fontName": "Arial-BoldMT",
      "fontSize": 60,
      "from": 0,
      "to": 3,
      "fontColor": {
        "rgb": {
          "red": 255,
          "green": 0,
          "blue": 0
        }
      }
    }
  ]
}
```

**V2:**

- Put style properties inside a `characterStyle` object.
- Use `apply.from` and `apply.to` for the character range (0-based, **inclusive**).
- Use `font.postScriptName` instead of `fontName`.

```json
{
  "characterStyles": [
    {
      "apply": {
        "from": 0,
        "to": 11
      },
      "characterStyle": {
        "font": {
          "postScriptName": "Arial-BoldMT"
        },
        "fontSize": 48,
        "syntheticBold": false,
        "syntheticItalic": false,
        "underline": false,
        "capsOption": "all_caps",
        "fontColor": {
          "rgb": {
            "red": 255,
            "green": 0,
            "blue": 0
          }
        }
      }
    }
  ]
}
```

<InlineAlert variant="info" slots="text"/>

In V2, `apply.from` and `apply.to` are **inclusive**: the style applies to characters at indices `from` through `to` (0-based). For example, `"from": 0, "to": 4` applies to the first five characters (indices 0, 1, 2, 3, 4).

### 3. Paragraph styles structure

**V1:** Range-based: each array item has `from`, `to`, and direct properties (e.g. `alignment`).

```json
{
  "paragraphStyles": [
    {
      "from": 0,
      "to": 20,
      "alignment": "center"
    }
  ]
}
```

<InlineAlert variant="info" slots="text"/>

**V1 paragraph style range:** In V1, `to` was incorrectly interpreted as **length**. In V2, `apply.from` and `apply.to` are both inclusive 0-based indices. When migrating, use the last character index for `apply.to`, not a length.

**V2:** Each item is a paragraph style range with optional `apply.from`/`apply.to` (0-based inclusive character indices) and a `paragraphStyle` object.

```json
{
  "paragraphStyles": [
    {
      "paragraphStyle": {
        "alignment": "center"
      }
    }
  ]
}
```

With a range (V2 only): use `apply.from` and `apply.to` to apply the paragraph style to a specific character range (same inclusive 0-based indexing as character styles).

```json
{
  "paragraphStyles": [
    {
      "apply": { "from": 0, "to": 20 },
      "paragraphStyle": {
        "alignment": "left",
        "writingDirection": "left_to_right",
        "firstLineIndent": 0,
        "startIndent": 0,
        "endIndent": 0,
        "spaceBefore": 0,
        "spaceAfter": 6
      }
    }
  ]
}
```

### 4. Font management and font options

Font management covers how you supply custom fonts (e.g. `.ttf`, `.otf`), set a default or fallback font when a referenced font is missing, and choose whether to fail the job or substitute the default.

#### V1 font options

| Property | Description |
|----------|-------------|
| `options.fonts` | Array of custom font inputs. Each item has `href` (URL) and `storage` (e.g. `"external"`). |
| `options.globalFont` | PostScript name of the font to use as fallback when a text layer references a missing font. Optional. |
| `options.manageMissingFonts` | `"useDefault"` or `"fail"`. When `"useDefault"`, missing fonts are replaced by `globalFont` if set, otherwise **ArialMT**. |

**Example (V1):**

```json
{
  "options": {
    "fonts": [
      { "href": "<SIGNED_GET_URL>", "storage": "external" }
    ],
    "globalFont": "ArialMT",
    "manageMissingFonts": "useDefault"
  }
}
```

#### V2 font options

| Property | Description |
|----------|-------------|
| `fontOptions.additionalFonts` | Array of custom font sources. Each item has `source.url`. Downloaded before the document is opened. |
| `fontOptions.defaultFontPostScriptName` | PostScript name used as fallback when a requested font is missing. Optional; if omitted, worker uses **ArialMT**. |
| `fontOptions.missingFontStrategy` | `"use_default"` or `"fail"`. Default is `"use_default"`. |

**Example (V2):**

```json
{
  "fontOptions": {
    "additionalFonts": [
      { "source": { "url": "<SIGNED_GET_URL>" } }
    ],
    "defaultFontPostScriptName": "Arial_BoldMT",
    "missingFontStrategy": "use_default"
  }
}
```

#### Property mapping (V1 to V2)

| V1 | V2 |
|----|-----|
| `options.fonts` | `fontOptions.additionalFonts` (use `source.url` instead of `href` + `storage`) |
| `options.globalFont` | `fontOptions.defaultFontPostScriptName` |
| `options.manageMissingFonts` | `fontOptions.missingFontStrategy` |
| `"useDefault"` | `"use_default"` |
| `"fail"` | `"fail"` |

#### Font types

Both V1 and V2 support three font sources:

| Font type | Description |
|-----------|-------------|
| **Custom** | User-supplied font files (e.g. `.ttf`, `.otf`) provided via `fontOptions.additionalFonts`. |
| **System** | Fonts available on the worker |
| **Typekit** | Adobe Typekit fonts |

#### Default font value

- **V1:** If `globalFont` is not set and `manageMissingFonts` is `"useDefault"`, the worker uses **ArialMT** as the fallback.
- **V2:** If `defaultFontPostScriptName` is not set and the strategy is use default, the worker uses **ArialMT** as the fallback.

In both V1 and V2, the default fallback font is **ArialMT** when no global/default is specified.

#### Missing-font strategy

| Strategy | V1 (`manageMissingFonts`) | V2 (`missingFontStrategy`) | Behavior |
|----------|---------------------------|----------------------------|----------|
| Use default | `"useDefault"` | `"use_default"` (default) | Missing fonts are replaced by the default font (or ArialMT). Job completes. |
| Fail | `"fail"` | `"fail"` | Job fails with an error listing the missing fonts. |

#### Improved missing font detection in V2

V2 correctly identifies missing fonts during text layer edits in all cases — whether the edit changes `fontName`, `fontSize`, or any other character attribute. V1 did not reliably detect missing fonts in this context, so the configured strategy was not consistently applied.

**Scenario:** A PSD contains a text layer using `AdobeClean-Regular`. The font is not available on the server. An edit is sent to the layer — for example changing only `fontSize`, or changing `fontName` to another unavailable font:

```json
{
  "characterStyles": [
    { "fontSize": 24 }
  ]
}
```

**V1 behavior:** The missing font is not detected. The job completes without applying `missingFontStrategy`, and the output document silently retains `AdobeClean-Regular` as the font name even though it was unavailable.

**V2 behavior:** The missing font is correctly detected. The configured `missingFontStrategy` is applied:
- `"use_default"` — `AdobeClean-Regular` is replaced by `defaultFontPostScriptName` (or `ArialMT` if unset). Job completes.
- `"fail"` — Job fails with an error identifying `AdobeClean-Regular` as missing.

### 5. Line Height and autoLeading

In V1, `lineHeight` was not supported in character attributes; the line height always defaulted to auto (120% of the font size).

In V2, line height support has been added alongside a new `autoLeading` parameter:

| Parameter | Description |
|-----------|-------------|
| `autoLeading` | `true` — line height is set to auto (120% of `fontSize`). `false` — the custom `lineHeight` value is used. |
| `lineHeight` | Custom line height in pixels. Only applied when `autoLeading` is `false`. |

**Default behavior:** When a text layer is created with the default font size of 30, the line height is automatically calculated as 120% × 30 = 36 pixels.

**V1:** `lineHeight` was not supported; auto-leading was always used.

**V2:** To match V1 auto behavior, use `autoLeading: true`. For custom leading, set `autoLeading: false` with an explicit `lineHeight`:

```json
// V2 — auto-leading (matches V1 behavior)
{
  "characterStyle": {
    "fontSize": 30,
    "autoLeading": true
  }
}
```

```json
// V2 — custom line height
{
  "characterStyle": {
    "fontSize": 30,
    "autoLeading": false,
    "lineHeight": 48
  }
}
```

## Adding text to existing document

### V1 approach: documentOperations

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentOperations \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [{
    "href": "<SIGNED_GET_URL>",
    "storage": "external"
  }],
  "options": {
    "fonts": [
      {
        "href": "<FONT_FILE_URL>",
        "storage": "external"
      }
    ],
    "layers": [
      {
        "add": { "insertTop": true },
        "type": "textLayer",
        "bounds": {
          "left": 25,
          "top": 42,
          "width": 977,
          "height": 267
        },
        "text": {
          "content": "NEW TEXT LAYER",
          "characterStyles": [
            {
              "fontSize": 56,
              "orientation": "horizontal",
              "fontColor": {
                "rgb": {
                  "red": 0,
                  "green": 0,
                  "blue": 0
                }
              },
              "fontName": "AcerFoco-SemiboldItalic"
            }
          ]
        }
      }
    ]
  },
  "outputs": [{
    "href": "<SIGNED_POST_URL>",
    "storage": "external",
    "type": "image/vnd.adobe.photoshop"
  }]
}'
```

### V2 approach

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/create-composite \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "fontOptions": {
    "additionalFonts": [
      { "source": { "url": "<FONT_FILE_URL>" } }
    ],
    "defaultFontPostScriptName": "Arial_BoldMT",
    "missingFontStrategy": "use_default"
  },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "New Text Layer",
        "operation": {
          "type": "add",
          "placement": {
            "type": "top"
          }
        },
        "text": {
          "content": "NEW TEXT LAYER",
          "antiAliasing": "smooth",
          "textOrientation": "horizontal",
          "frame": {
            "type": "area",
            "bounds": {
              "top": 42,
              "left": 25,
              "right": 1002,
              "bottom": 309
            }
          },
          "characterStyles": [
            {
              "apply": { "from": 0, "to": 13 },
              "characterStyle": {
                "font": { "postScriptName": "AcerFoco-SemiboldItalic" },
                "fontSize": 56,
                "fontColor": {
                  "rgb": {
                    "red": 0,
                    "green": 0,
                    "blue": 0
                  }
                }
              }
            }
          ]
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": { "url": "<SIGNED_POST_URL>" },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

## Editing existing text layers

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Text Layer",
        "text": {
          "content": "Updated Text"
        },
        "edit": {}
      }
    ]
  }
}
```

### V2 approach

```json
{
  "edits": {
    "layers": [
      {
        "name": "Existing Text Layer",
        "operation": {
          "type": "edit"
        },
        "text": {
          "content": "Updated Text",
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 48
              }
            }
          ]
        }
      }
    ]
  }
}
```

## Common migration patterns

### Multi-style text

**V1:**

```json
{
  "text": {
    "content": "Bold and Italic",
    "characterStyles": [
      {
        "from": 0,
        "to": 4,
        "fontSize": 48,
        "fontName": "Arial-BoldMT"
      },
      {
        "from": 9,
        "to": 15,
        "fontSize": 48,
        "fontName": "Arial-ItalicMT"
      }
    ]
  }
}
```

<InlineAlert variant="info" slots="text"/>

In V1, `to` was treated as length; in V2, `apply.from` and `apply.to` are both inclusive 0-based indices. Use the last character index for `apply.to`, not a length. See [Character styles structure](#2-character-styles-structure).

**V2:** Use `apply.from`/`apply.to` (inclusive) and `characterStyle` with `font.postScriptName`

```json
{
  "text": {
    "content": "Bold and Italic",
    "characterStyles": [
      {
        "apply": { "from": 0, "to": 4 },
        "characterStyle": {
          "fontSize": 48,
          "font": { "postScriptName": "Arial-BoldMT" }
        }
      },
      {
        "apply": { "from": 9, "to": 15 },
        "characterStyle": {
          "fontSize": 48,
          "font": { "postScriptName": "Arial-ItalicMT" }
        }
      }
    ]
  }
}
```

### Multi-line text

Both V1 and V2 use `\r` for line breaks:

```json
{
  "text": {
    "content": "Line 1\rLine 2\rLine 3"
  }
}
```

### Custom fonts

**V1:**

```json
{
  "options": {
    "fonts": [
      {
        "href": "<FONT_FILE_URL>",
        "storage": "external"
      }
    ]
  }
}
```

**V2:**

```json
{
  "fontOptions": {
    "additionalFonts": [
      {
        "source": {
          "url": "<FONT_FILE_URL>"
        }
      }
    ]
  }
}
```

## Character style properties

V2 has expanded character style options beyond V1:

| Property | V1 Support | V2 Support | Notes |
| -------- | ---------- | ---------- | ----- |
| `fontSize` | ✅ (pixels) | ✅ (pixels) | Same in both |
| `fontName` | ✅ | — | V1 only; use `font.postScriptName` in V2 |
| `font.postScriptName` | — | ✅ | V2: inside `characterStyle.font` |
| `fontColor` | ✅ rgb, cmyk, lab, gray | ✅ rgb, cmyk, lab, gray | Same nested shape in both (e.g. `fontColor.rgb`, `fontColor.cmyk`) |
| `orientation` | ✅ | ✅ | V2: `textOrientation` on `text` |
| `syntheticBold` | ❌ | ✅ | V2 only |
| `syntheticItalic` | ❌ | ✅ | V2 only |
| `letterSpacing` | ❌ | ✅ | V2 only |
| `lineHeight` | ❌ | ✅ | V2 only. Custom line height in pixels. Used when `autoLeading` is `false`. |
| `autoLeading` | ❌ | ✅ | V2 only. Default: `false`. When `true`, line height is set to auto (120% of `fontSize`). When `false`, the custom `lineHeight` value is used. |
| `fontAlpha` | ❌ | ✅ | V2 only |
| `capsOption` | ❌ | ✅ | V2 only (e.g. `all_caps`) |

<InlineAlert variant="info" slots="text"/>

V2 offers more text styling options than V1. See the [V2 API Reference](../../../api/photoshop-v2/index.md) for complete property lists.

## Paragraph style properties

In V2, all paragraph style properties below are optional; defaults are applied when omitted.

| Property | V1 Support | V2 Support | Description (V2) |
| -------- | ---------- | ---------- | ----------------- |
| `alignment` | ✅ | ✅ | Text alignment. Values: `left` (default), `center`, `right`, `justify`, `justify_left`, `justify_right`, `justify_center`. |
| `writingDirection` | ❌ | ✅ | Writing direction. Values: `left_to_right` (default), `right_to_left`. |
| `firstLineIndent` | ❌ | ✅ | First line indent in pixels. Default 0. |
| `startIndent` | ❌ | ✅ | Start indent in pixels. Default 0. |
| `endIndent` | ❌ | ✅ | End indent in pixels. Default 0. |
| `spaceBefore` | ❌ | ✅ | Space before paragraph in pixels. Default 0. |
| `spaceAfter` | ❌ | ✅ | Space after paragraph in pixels. Default 0. |

## Text positioning

### Frame types: point vs area

| | V1 | V2 |
|--|----|----|
| **Area frame** | ✅ Only frame type supported. Text layer creation always used an area frame; bounds were required or defaulted. | ✅ Supported. Use `text.frame` with `type: "area"` and `bounds: { top, left, right, bottom }`. |
| **Point frame** | ❌ Not supported in V1. | ✅ Supported. Use `text.frame` with `type: "point"` and `origin: { x, y }`. Single-point text, no wrapping. |

V1 only supported **area** frames. V2 supports both **point** and **area** frames.

### Default bounds when frame is omitted

| | V1 | V2 |
|--|----|----|
| **When bounds/frame not provided** | Default area bounds were used: `left: 0`, `top: 0`, `width: 4`, `height: 4` (pixels). | When `text.frame` is omitted, the default is a **point** frame at the **center of the canvas**. |

In V1 the default was a small area at the top-left; in V2 the default is a point at the middle of the canvas. To get predictable placement in V2, always set `text.frame` (either `type: "area"` with bounds or `type: "point"` with origin).

### Using bounds

**V1:** Layer-level `bounds` with `left`, `top`, `width`, `height`. Only area frame; no point frame support.

```json
{
  "type": "textLayer",
  "name": "Positioned Text",
  "bounds": {
    "left": 100,
    "top": 50,
    "width": 800,
    "height": 200
  },
  "text": {"content": "..."}
}
```

**V2:** Position and size the text using `text.frame` with `type: "area"` and `bounds` as `top`, `left`, `right`, `bottom` (no `width`/`height`). Convert V1 bounds: `right = left + width`, `bottom = top + height`.

```json
{
  "type": "text_layer",
  "name": "Positioned Text",
  "operation": {
    "type": "add",
    "placement": {
      "type": "top"
    }
  },
  "text": {
    "content": "...",
    "frame": {
      "type": "area",
      "bounds": {
        "top": 50,
        "left": 100,
        "right": 900,
        "bottom": 250
      }
    }
  }
}
```

### Font size units

Both V1 and V2 use pixels for `fontSize`. In V2 it goes inside `characterStyle.fontSize`.

### Font color structure

**Supported in both V1 and V2:** rgb, cmyk, lab, and gray. V1 accepted 0–65535 for all components; V2 enforces lower maximums:

| Color Model | V1 Fields | V2 Fields | V1 Range | V2 Range | If V1 value exceeds V2 max |
| ----------- | --------- | --------- | --------- | --------- | -------------------------- |
| `rgb` | `red`, `green`, `blue` | `red`, `green`, `blue` | 0–65535 | 0–32768 | Use 32768 |
| `cmyk` | `cyan`, `magenta`, `yellowColor`, `black` | `cyan`, `magenta`, `yellow`, `black` | 0–65535 | 0–32768 | Use 32768 |
| `lab` | `luminance` | `l` | 0–65535 | 0–32768 | Use 32768 |
| `lab` | `a`, `b` | `a`, `b` | 0–65535 | -16384–16384 | Use 16384 |
| `gray` | `gray` | `gray` | 0–65535 | 0–32768 | Use 32768 |

All components are required and default to `0` when omitted.

<InlineAlert variant="warning" slots="text1"/>

V2 rejects requests where any `fontColor` component exceeds its maximum. If your V1 payload contains a value above the V2 limit, cap it at the maximum before sending:

- `rgb`, `cmyk`, `gray`, `lab.l` — cap at **32768**. Example: V1 `red: 40000` → V2 `red: 32768`
- `lab.a`, `lab.b` — cap at **16384**. Example: V1 `a: 40000` → V2 `a: 16384`

**V2 structure** (updated field names): rgb, cmyk, lab, gray:

```json
{
  "fontColor": {
    "rgb": {
      "red": 32768,
      "green": 0,
      "blue": 0
    }
  }
}
```

```json
{
  "fontColor": {
    "cmyk": {
      "cyan": 32768,
      "magenta": 0,
      "yellow": 0,
      "black": 0
    }
  }
}
```

```json
{
  "fontColor": {
    "lab": {
      "l": 5000,
      "a": 10000,
      "b": -5000
    }
  }
}
```

```json
{
  "fontColor": {
    "gray": {
      "gray": 16384
    }
  }
}
```

## Migration checklist

When migrating text layer operations from V1 to V2:

- [ ] Change `type: "textLayer"` to `type: "text_layer"`
- [ ] Use `apply.from`/`apply.to` for character style ranges (V2); both indices are inclusive (0-based); wrap style properties in `characterStyle`
- [ ] Use `font.postScriptName` (inside `characterStyle.font`) in V2 instead of top-level `fontName`
- [ ] Wrap paragraph style properties in `paragraphStyle` object
- [ ] Font color field renames: `fontColor.cmyk.yellowColor` → `fontColor.cmyk.yellow`; `fontColor.lab.luminance` → `fontColor.lab.l`
- [ ] Font color rgb/cmyk/gray/lab-l: V1 accepted 0–65535; V2 clamps to 0–32768 (any value > 32768 becomes 32768)
- [ ] Font color lab `a`/`b`: V1 accepted 0–65535; V2 range is -16384–16384 (any value > 16384 becomes 16384)
- [ ] Update font management properties (`manageMissingFonts` → `missingFontStrategy`, `globalFont` → `defaultFontPostScriptName`)
- [ ] Update custom fonts: `options.fonts` (href, storage) → `fontOptions.additionalFonts` (source.url)
- [ ] Update inputs/outputs: V1 `inputs[].href` → V2 `image.source.url`; V1 `outputs[].href` → V2 `outputs[].destination.url`, and use `mediaType` instead of `type`
- [ ] Map layer placement: V1 `add.insertTop` (or insertBottom, etc.) → V2 `operation: { type: "add", placement: { type: "top" } }` (or bottom, above, below, into)
- [ ] Convert bounds: V1 layer `bounds` (left, top, width, height) → V2 `text.frame` with `type: "area"` and `bounds: { top, left, right, bottom }` where `right = left + width`, `bottom = top + height`

## Common migration issues

Differences between V1 and V2 that often cause issues when migrating:

- **Character and paragraph style range (`from`/`to`):** In V1, `to` was incorrectly taken as a **length**. In V2, `apply.from` and `apply.to` are both **inclusive** 0-based character indices. When migrating, set `apply.to` to the **last character index** you want to style, not a length. Same applies to paragraph style ranges.
- **Layer type:** V1 uses `"textLayer"`; V2 uses `"text_layer"`.
- **Font name:** V1 uses top-level `fontName`. V2 uses `characterStyle.font.postScriptName`.
- **Bounds:** V1 uses layer-level `bounds` with `left`, `top`, `width`, `height`. V2 uses `text.frame` with `type: "area"` and `bounds: { top, left, right, bottom }` where `right = left + width`, `bottom = top + height`.
- **Default when no frame/bounds given:** V1 default was an area frame (0, 0, 4, 4). V2 default is a **point** frame at the **center of the canvas**. Set `text.frame` explicitly for predictable placement.
- **Font options:** V1 uses `options.fonts` (href, storage), `options.globalFont`, `options.manageMissingFonts`. V2 uses `fontOptions.additionalFonts` (source.url), `fontOptions.defaultFontPostScriptName`, `fontOptions.missingFontStrategy` (e.g. `"use_default"`).

## Feature availability

### Currently available in V2

- ✅ Add text layers
- ✅ Edit text content
- ✅ Character styles (font, size, color: rgb, cmyk, lab, gray)
- ✅ Paragraph styles (alignment)
- ✅ Multi-style text (from/to ranges)
- ✅ Custom fonts
- ✅ Text positioning (bounds)
- ✅ Expanded character properties (tracking, leading, etc.)

### V1 features not yet in V2

- ⏳ `fill_to_canvas` property
- ⏳ Some advanced text effects

## Complete migration example

**V1 documentOperations:**

```json
{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "external"
    }
  ],
  "options": {
    "layers": [
      {
        "type": "textLayer",
        "name": "Headline",
        "text": {
          "content": "Welcome",
          "characterStyles": [
            {
              "fontSize": 72,
              "fontName": "Arial-BoldMT",
              "fontColor": {
                "rgb": {
                  "red": 0,
                  "green": 0,
                  "blue": 0
                }
              }
            }
          ],
          "paragraphStyles": [
            {
              "alignment": "center"
            }
          ]
        },
        "bounds": {
          "left": 0,
          "top": 100,
          "width": 1920,
          "height": 150
        }
      }
    ],
    "manageMissingFonts": "useDefault"
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}
```

**V2 create-composite:**

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "Headline",
        "text": {
          "content": "Welcome",
          "frame": {
            "type": "area",
            "bounds": {
              "top": 100,
              "left": 0,
              "right": 1920,
              "bottom": 250
            }
          },
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 72,
                "font": {
                  "postScriptName": "Arial-BoldMT"
                },
                "fontColor": {
                  "rgb": {
                    "red": 0,
                    "green": 0,
                    "blue": 0
                  }
                }
              }
            }
          ],
          "paragraphStyles": [
            {
              "paragraphStyle": {
                "alignment": "center"
              }
            }
          ]
        },
        "operation": {
          "type": "add"
        }
      }
    ]
  },
  "fontOptions": {
    "missingFontStrategy": "use_default"
  },
  "outputs": [
    {
      "destination": {
        "url": "<SIGNED_POST_URL>"
      },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

## Next steps

- Review [Layer Operations Overview](layer-operations-overview.md) for general concepts
- Check [Document Creation](document-creation-migration.md) for creating new documents with text
- See [Advanced Operations](layer-operations-advanced.md) for text layer transforms and effects
