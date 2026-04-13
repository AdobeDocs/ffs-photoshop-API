---
title: Text Layer Operations Migration (V1 to V2)
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

# Text Layer Operations Migration (V1 to V2)

This guide helps you migrate text layer operations from V1's `/documentCreate` and `/documentOperations` endpoints to V2's unified `/create-composite` endpoint.

## Overview

**V1 Endpoints:**

- `/pie/psdService/documentCreate` - Create documents with text layers
- `/pie/psdService/documentOperations` - Add/edit text layers

**V2 Endpoint:** `/v2/create-composite` with `edits.layers` containing text layer operations

### What Changed

| Aspect                | V1                                 | V2                                                           |
| --------------------- | ---------------------------------- | ------------------------------------------------------------ |
| **Layer Type**        | `"textLayer"`                      | `"text_layer"`                                               |
| **Request Structure** | `options.layers`                   | `edits.layers`                                               |
| **Text Content**      | `text.content`                     | `text.content` (same)                                        |
| **Character Styles**  | `characterStyles` array            | `characterStyles` array (expanded properties)                |
| **Font Size**         | In pixels                          | In points                                                    |
| **Font Management**   | `manageMissingFonts`, `globalFont` | `fontOptions.missingFontStrategy`, `fontOptions.defaultFont` |

## Creating Text Layers

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
    "resolution": 72,
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
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 48,
                "fontName": "Arial-BoldMT",
                "fontColor": {
                  "type": "rgb",
                  "red": 255,
                  "green": 0,
                  "blue": 0
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

## Key Migration Changes

### 1. Layer Type Name

**V1:** `"type": "textLayer"`

**V2:** `"type": "text_layer"`

### 2. Character Styles Structure

**V1:** Direct properties in characterStyles array

```json
{
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
  ]
}
```

**V2:** Wrapped in `characterStyle` object with expanded options

```json
{
  "characterStyles": [
    {
      "characterStyle": {
        "fontSize": 48,
        "fontName": "Arial-BoldMT",
        "fontColor": {
          "type": "rgb",
          "red": 255,
          "green": 0,
          "blue": 0
        }
      }
    }
  ]
}
```

### 3. Paragraph Styles Structure

**V1:** Direct properties

```json
{
  "paragraphStyles": [
    {
      "alignment": "center"
    }
  ]
}
```

**V2:** Wrapped in `paragraphStyle` object

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

### 4. Font Management

**V1:**

```json
{
  "options": {
    "globalFont": "ArialMT",
    "manageMissingFonts": "useDefault"
  }
}
```

**V2:**

```json
{
  "fontOptions": {
    "defaultFont": "ArialMT",
    "missingFontStrategy": "use_default"
  }
}
```

## Adding Text to Existing Document

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
    "layers": [
      {
        "type": "textLayer",
        "name": "New Text",
        "text": {
          "content": "Added Text",
          "characterStyles": [
            {
              "fontSize": 36,
              "fontName": "ArialMT"
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
  "edits": {
    "layers": [
      {
        "type": "text_layer",
        "name": "New Text",
        "text": {
          "content": "Added Text",
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 36,
                "fontName": "ArialMT"
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

## Editing Existing Text Layers

### V1 approach

```json
{
  "options": {
    "layers": [
      {
        "name": "Existing Text Layer",
        "text": {
          "content": "Updated Text"
        }
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

<InlineAlert variant="info" slots="text"/>

In V2, when editing existing text layers, you must include characterStyles even if only changing content. Omit the operation type - it's implicit for existing layers.

## Common Migration Patterns

### Multi-Style Text

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

**V2:** (Same pattern, wrapped in characterStyle)

```json
{
  "text": {
    "content": "Bold and Italic",
    "characterStyles": [
      {
        "from": 0,
        "to": 4,
        "characterStyle": {
          "fontSize": 48,
          "fontName": "Arial-BoldMT"
        }
      },
      {
        "from": 9,
        "to": 15,
        "characterStyle": {
          "fontSize": 48,
          "fontName": "Arial-ItalicMT"
        }
      }
    ]
  }
}
```

### Multi-line Text

Both V1 and V2 use `\r` for line breaks:

```json
{
  "text": {
    "content": "Line 1\rLine 2\rLine 3"
  }
}
```

### Custom Fonts

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

## Character Style Properties

V2 has expanded character style options beyond V1:

| Property          | V1 Support  | V2 Support  | Notes               |
| ----------------- | ----------- | ----------- | ------------------- |
| `fontSize`        | ✅ (pixels) | ✅ (points) | Unit change         |
| `fontName`        | ✅          | ✅          | PostScript names    |
| `fontColor`       | ✅          | ✅          | Structure changed   |
| `orientation`     | ✅          | ✅          | horizontal/vertical |
| `syntheticBold`   | ❌          | ✅          | New in V2           |
| `syntheticItalic` | ❌          | ✅          | New in V2           |
| `tracking`        | ❌          | ✅          | New in V2           |
| `leading`         | ❌          | ✅          | New in V2           |
| `baselineShift`   | ❌          | ✅          | New in V2           |

<InlineAlert variant="info" slots="text"/>

V2 offers more text styling options than V1. See the [V2 API Reference](https://developer.adobe.com/photoshop/api/v2/) for complete property lists.

## Paragraph Style Properties

| Property          | V1 Support | V2 Support |
| ----------------- | ---------- | ---------- |
| `alignment`       | ✅         | ✅         |
| `spaceBefore`     | ❌         | ✅         |
| `spaceAfter`      | ❌         | ✅         |
| `firstLineIndent` | ❌         | ✅         |

## Text Positioning

### Using Bounds

**V1:**

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
  "text": {...}
}
```

**V2:** (Same pattern)

```json
{
  "type": "text_layer",
  "name": "Positioned Text",
  "bounds": {
    "left": 100,
    "top": 50,
    "width": 800,
    "height": 200
  },
  "text": {...}
}
```

### Alignment Options

**V1:** Used `horizontal_align` and `vertical_align` properties

```json
{
  "horizontal_align": "center",
  "vertical_align": "center"
}
```

**V2:** Uses `placement` object with `align` properties

```json
{
  "operation": {
    "type": "add",
    "placement": {
      "type": "custom",
      "horizontalAlignment": "center",
      "verticalAlignment": "center"
    }
  }
}
```

## Migration Checklist

When migrating text layer operations from V1 to V2:

- [ ] Change `type: "textLayer"` to `type: "text_layer"`
- [ ] Wrap character style properties in `characterStyle` object
- [ ] Wrap paragraph style properties in `paragraphStyle` object
- [ ] Update font color structure (`rgb` object → `type` + color properties)
- [ ] Convert font size from pixels to points if needed
- [ ] Update font management properties (`manageMissingFonts` → `missingFontStrategy`)
- [ ] Update custom fonts structure (`fonts` → `fontOptions.additionalFonts`)
- [ ] Update storage syntax (`href`/`storage` → `url`/`storageType`)
- [ ] Add explicit `operation.type: "add"` for new layers
- [ ] Update alignment properties if using relative positioning

## Common Migration Issues

### Issue: Character styles required in V2

**Problem:** V2 requires character styles even for simple text

**Solution:** Always include at least fontSize in characterStyles

```json
{
  "text": {
    "content": "Simple Text",
    "characterStyles": [
      {
        "characterStyle": {
          "fontSize": 48
        }
      }
    ]
  }
}
```

### Issue: Font size units

**Problem:** V1 used pixels, V2 uses points

**Solution:** Convert if needed (72 points = 1 inch, depends on document resolution)

For 72 dpi documents: pixels ≈ points

### Issue: Font color structure

**Problem:** Different color object structures

**V1:**

```json
{
  "fontColor": {
    "rgb": {
      "red": 255,
      "green": 0,
      "blue": 0
    }
  }
}
```

**V2:**

```json
{
  "fontColor": {
    "type": "rgb",
    "red": 255,
    "green": 0,
    "blue": 0
  }
}
```

## Feature Availability

### Currently Available in V2

- ✅ Add text layers
- ✅ Edit text content
- ✅ Character styles (font, size, color, orientation)
- ✅ Paragraph styles (alignment)
- ✅ Multi-style text (from/to ranges)
- ✅ Custom fonts
- ✅ Text positioning (bounds)
- ✅ Expanded character properties (tracking, leading, etc.)

### V1 Features Not Yet in V2

- ⏳ `fill_to_canvas` property
- ⏳ Some advanced text effects

<InlineAlert variant="info" slots="text"/>

If you rely on V1 features not yet in V2, contact the Adobe DI ART Service team to discuss alternatives or timeline.

## Complete Migration Example

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
          "characterStyles": [
            {
              "characterStyle": {
                "fontSize": 72,
                "fontName": "Arial-BoldMT",
                "fontColor": {
                  "type": "rgb",
                  "red": 0,
                  "green": 0,
                  "blue": 0
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
        "bounds": {
          "left": 0,
          "top": 100,
          "width": 1920,
          "height": 150
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

## Need Help?

Contact the Adobe DI ART Service team for technical support with text layer migration.
