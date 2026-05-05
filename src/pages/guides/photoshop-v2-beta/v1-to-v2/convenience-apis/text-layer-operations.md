---
title: Text Layer Operations Migration
description: Migrate from V1 /pie/psdService/text to V2 execute-actions for text layer editing via ActionJSON or UXP scripts
hideBreadcrumbNav: true
keywords:
  - text layer
  - edit text
  - convenience API
  - ActionJSON
  - UXP
  - migration
  - v1 to v2
---

# Text Layer Operations Migration

Migrate from the v1 API's `/pie/psdService/text` endpoint to the v2 API.

## Overview

The Edit Text convenience API allows you to modify text layers within Photoshop files (PSD files). This guide shows how to migrate from V1's `/pie/psdService/text` endpoint to V2's `/v2/execute-actions` endpoint.

**Key benefits of V2:**

- Execute text edits via ActionJSON or UXP scripts for full control over Photoshop operations
- Use **Actions** for declarative, step-by-step edits; use **UXP** when you need conditional logic, layer iteration, or data-driven changes
- Chain text layer operations with other actions in a single request
- Access low-level text style properties (font, size, color, etc.)

## V1 API (deprecated)

**Endpoint:** `/pie/psdService/text`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/text \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "external"
    }
  ],
  "options": {
    "layers": [
      {
        "name": "your-text-layer-name",
        "text": {
          "orientation": "horizontal",
          "characterStyles": [
            {
              "size": 100,
              "orientation": "horizontal",
              "fontPostScriptName": "BrushScriptMT",
              "fontName": "Brush Script MT",
              "fontStyleName": "Regular",
              "color": {
                "red": 255,
                "green": 207,
                "blue": 104
              }
            }
          ]
        }
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "storage": "external",
      "type": "image/vnd.adobe.photoshop"
    }
  ]
}'
```

## V2 API (current)

**Endpoint:** `/v2/execute-actions`

In V2, text layer operations are performed through the `execute-actions` endpoint using either **Actions** (ActionJSON) or **UXP scripts**. Instead of a dedicated `/text` endpoint with a layers-based request structure, you pass ActionJSON or a UXP script that performs the equivalent Photoshop operations: selecting the text layer(s), then setting text style properties.

### Example: editing font and color

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/execute-actions \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"select\",\"_target\":[{\"_name\":\"your-text-layer-name\",\"_ref\":\"layer\"}],\"makeVisible\":true},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"size\":{\"_unit\":\"pointsUnit\",\"_value\":100},\"textOverrideFeatureName\":808465458,\"typeStyleOperationType\":3}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"fontPostScriptName\":\"BrushScriptMT\",\"fontName\":\"Brush Script MT\",\"fontStyleName\":\"Regular\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"color\":{\"_obj\":\"RGBColor\",\"red\":255,\"green\":207,\"blue\":104}}}]",
          "contentType": "application/json"
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

## ActionJSON definition

The example action performs four operations:

1. **Select** the text layer by name and make it visible
2. **Set** the text size to 100pt
3. **Set** the font to Brush Script MT Regular
4. **Set** the text color to peach/gold (RGB 255, 207, 104)

```json
[
  {
    "_obj": "select",
    "_target": [
      {
        "_name": "your-text-layer-name",
        "_ref": "layer"
      }
    ],
    "makeVisible": true
  },
  {
    "_obj": "set",
    "_target": [
      {
        "_property": "textStyle",
        "_ref": "property"
      },
      {
        "_enum": "ordinal",
        "_ref": "textLayer",
        "_value": "targetEnum"
      }
    ],
    "to": {
      "_obj": "textStyle",
      "size": {
        "_unit": "pointsUnit",
        "_value": 100
      },
      "textOverrideFeatureName": 808465458,
      "typeStyleOperationType": 3
    }
  },
  {
    "_obj": "set",
    "_target": [
      {
        "_property": "textStyle",
        "_ref": "property"
      },
      {
        "_enum": "ordinal",
        "_ref": "textLayer",
        "_value": "targetEnum"
      }
    ],
    "to": {
      "_obj": "textStyle",
      "fontPostScriptName": "BrushScriptMT",
      "fontName": "Brush Script MT",
      "fontStyleName": "Regular"
    }
  },
  {
    "_obj": "set",
    "_target": [
      {
        "_property": "textStyle",
        "_ref": "property"
      },
      {
        "_enum": "ordinal",
        "_ref": "textLayer",
        "_value": "targetEnum"
      }
    ],
    "to": {
      "_obj": "textStyle",
      "color": {
        "_obj": "RGBColor",
        "red": 255,
        "green": 207,
        "blue": 104
      }
    }
  }
]
```

### Action structure explained

| Step | Operation | Description |
|------|------------|-------------|
| 1 | `select` | Targets the layer by name. Use `_name` to match your text layer. `makeVisible: true` ensures the layer is visible before editing. |
| 2 | `set` (textStyle) | Applies font size: `size` (points). |
| 3 | `set` (textStyle) | Applies font: `fontPostScriptName`, `fontName`, `fontStyleName`. |
| 4 | `set` (textStyle) | Applies color: `color` with `RGBColor` (red, green, blue). |

**Customizing actions:** Change `_name` to match your layer. Adjust each `set` step's `to` object for size, font (`fontPostScriptName`, `fontName`, `fontStyleName`), or color (`RGBColor`). Add, reorder, or omit steps as needed. For multiple layers, repeat the `select` + `set` pattern.

## Bounds and visibility-only edits

When a V1 `/pie/psdService/text` payload only changes layer bounds or visibility — with no text content or style modifications — V2 still requires a non-empty `options` object containing ActionJSON or UXP. An empty `options` object is rejected:

```
options: At least one of actions or uxp must be provided
```

Generate ActionJSON that selects each target layer by `_name` and applies the appropriate operation:

**Visibility toggle (show/hide):**

```json
[
  {
    "_obj": "select",
    "_target": [{"_ref": "layer", "_name": "My Text Layer"}],
    "makeVisible": false
  },
  {
    "_obj": "hide",
    "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]
  }
]
```

To show a hidden layer, use `"_obj": "show"` instead of `"hide"`.

**Bounds change (translate/move):**

```json
[
  {
    "_obj": "select",
    "_target": [{"_ref": "layer", "_name": "My Text Layer"}],
    "makeVisible": false
  },
  {
    "_obj": "move",
    "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
    "to": {
      "_obj": "offset",
      "horizontal": {"_unit": "pixelsUnit", "_value": 50},
      "vertical": {"_unit": "pixelsUnit", "_value": 30}
    }
  }
]
```

Wrap this ActionJSON as a stringified string in `options.actions[].source.content` with `contentType: "application/json"`.

## Using UXP scripts

In V2, you can also use **UXP scripts** for text layer operations. UXP is ideal when you need:

- **Conditional logic** – Edit only layers that match certain criteria (e.g., text layers, layers by name)
- **Layer iteration** – Loop over all layers (including nested groups) and apply edits selectively
- **State-based changes** – Toggle properties based on current values (e.g., bold → regular, italic → regular)

### Example: conditional text layer edits

This UXP script selects each layer, and for every text layer, toggles bold and italic (if not bold → set bold; if bold → set regular; same for italic). It uses `core.executeAsModal()` for document modifications.

**Script**

```javascript
const { app, core } = require("photoshop");

// Recursively collect all layers including those in groups
function getAllLayers(layers, result = []) {
  for (let i = 0; i < layers.length; i++) {
    const layer = layers[i];
    result.push(layer);
    if (layer.layers && layer.layers.length > 0) {
      getAllLayers(layer.layers, result);
    }
  }
  return result;
}

async function main() {
  if (!app.activeDocument) {
    console.error("No active document");
    return;
  }

  await core.executeAsModal(
    async () => {
      const doc = app.activeDocument;
      const allLayers = getAllLayers(doc.layers);
      let editCount = 0;

      for (const layer of allLayers) {
        try {
          // Select the layer
          doc.activeLayers = [layer];

          if (layer.kind === "text" && layer.textItem) {
            const cs = layer.textItem.characterStyle;

            // Toggle bold: if not bold → bold; if bold → regular
            cs.fauxBold = !cs.fauxBold;

            // Toggle italic: if not italic → italic; if italic → regular
            cs.fauxItalic = !cs.fauxItalic;

            editCount++;
          }
        } catch (err) {
          console.warn(`Could not edit layer "${layer.name}":`, err.message);
        }
      }

      console.log(`Toggled bold/italic on ${editCount} text layer(s)`);
    },
    { commandName: "Conditional Text Layer Edits" }
  );
}

main().catch((err) => {
  console.error("Conditional text edit failed:", err);
  throw err;
});
```

**Request:**

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/execute-actions \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "options": {
    "uxp": {
      "source": {
        "content": "const { app, core } = require(\"photoshop\"); function getAllLayers(layers, result) { result = result || []; for (let i = 0; i < layers.length; i++) { const layer = layers[i]; result.push(layer); if (layer.layers && layer.layers.length > 0) getAllLayers(layer.layers, result); } return result; } async function main() { if (!app.activeDocument) return; await core.executeAsModal(async () => { const doc = app.activeDocument; const allLayers = getAllLayers(doc.layers); for (const layer of allLayers) { try { doc.activeLayers = [layer]; if (layer.kind === \"text\" && layer.textItem) { const cs = layer.textItem.characterStyle; cs.fauxBold = !cs.fauxBold; cs.fauxItalic = !cs.fauxItalic; } } catch (err) { console.warn(\"Could not edit layer:\", layer.name, err.message); } } }, { commandName: \"Conditional Text Layer Edits\" }); } main().catch(err => { console.error(\"Conditional text edit failed:\", err); throw err; });",
        "contentType": "application/javascript"
      }
    }
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

## Migration checklist

**Request envelope:**
- [ ] Replace `/pie/psdService/text` endpoint with `/v2/execute-actions`
- [ ] Move `inputs[0].href` to `image.source.url`
- [ ] Move `outputs[0].href` to `outputs[0].destination.url`
- [ ] Remove `storage` fields (not needed for presigned URLs)
- [ ] Change `outputs[0].type` to `outputs[0].mediaType`
- [ ] Choose **Actions** or **UXP**: Use `options.actions` for declarative edits, or `options.uxp` for conditional logic

**Text content and style (ActionJSON):**
- [ ] `text.content` → `set` on `textLayer` with `textKey`
- [ ] `text.orientation` → `set` on `textLayer` with `orientation` enum
- [ ] `text.antiAlias` → `set` on `textLayer` with `antiAlias` enum
- [ ] `characterStyles.size` → `set textStyle` with `size` (pointsUnit) + `textOverrideFeatureName: 808465458` + `typeStyleOperationType: 3`
- [ ] `characterStyles.fontPostScriptName/fontName/fontStyleName` → `set textStyle`
- [ ] `characterStyles.color` → `set textStyle` with `color._obj: "RGBColor"`
- [ ] `characterStyles.leading` → `set textStyle` with `autoLeading: false` + `leading` (pointsUnit)
- [ ] `characterStyles.tracking` → `set textStyle` with `tracking` (integer, thousandths of em)
- [ ] `characterStyles.syntheticBold/syntheticItalic` → `set textStyle`
- [ ] `characterStyles.fontCaps` → `set textStyle` with `fontCaps` enum
- [ ] `characterStyles.baseline` → `set textStyle` with `baselineDirection` enum
- [ ] `characterStyles.strikethrough` → `set textStyle` with `strikeThrough` enum
- [ ] `characterStyles.underline` → `set textStyle` with `underline` enum
- [ ] `characterStyles.verticalScale/horizontalScale` → `set textStyle` (percentage integers)
- [ ] `characterStyles.ligature` → `set textStyle`
- [ ] `characterStyles.autoKern` → `set textStyle` with `autoKern` enum
- [ ] `characterStyles.stylisticAlternates` → use UXP (ActionJSON equivalent is not standardized)
- [ ] `paragraphStyles.alignment` → `set paragraphStyle` with `align` enum

**Font management:**
- [ ] `options.fonts[].href` → `options.fontOptions.additionalFonts[].source.url`
- [ ] `options.manageMissingFonts: "fail"/"useDefault"` → `options.fontOptions.missingFontStrategy: "fail"/"use_default"`
- [ ] `options.globalFont` → `options.fontOptions.defaultFontPostScriptName`

**When to use Actions vs UXP:**

| Use Case | Prefer |
|----------|--------|
| Fixed edits (font, size, color for known layers) | **Actions** |
| Conditional edits (only if layer is text, only if name contains "title") | **UXP** |
| Iterate over all layers and apply logic | **UXP** |
| Toggle or state-based changes | **UXP** |

## Migration examples

### Basic migration

Both examples change the text color of one layer.

**V1:**

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
        "name": "your-text-layer-name",
        "text": {
          "characterStyles": [
            {"color": {"red": 255, "green": 128, "blue": 64}}
          ]
        }
      }
    ]
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

**V2:**

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"select\",\"_target\":[{\"_name\":\"your-text-layer-name\",\"_ref\":\"layer\"}],\"makeVisible\":true},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"color\":{\"_obj\":\"RGBColor\",\"red\":255,\"green\":128,\"blue\":64}}}]",
          "contentType": "application/json"
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
}
```

### Multiple layers

This example edits two text layers using both the V1 and V2 APIs.

**V1:**

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
        "name": "first-layer-name",
        "text": {
          "characterStyles": [
            {"color": {"red": 255, "green": 0, "blue": 0}}
          ]
        }
      },
      {
        "name": "second-layer-name",
        "text": {
          "characterStyles": [
            {
              "size": 48,
              "color": {"red": 0, "green": 128, "blue": 255}
            }
          ]
        }
      }
    ]
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

**V2:**

```json
{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"select\",\"_target\":[{\"_name\":\"first-layer-name\",\"_ref\":\"layer\"}],\"makeVisible\":true},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"color\":{\"_obj\":\"RGBColor\",\"red\":255,\"green\":0,\"blue\":0}}},{\"_obj\":\"select\",\"_target\":[{\"_name\":\"second-layer-name\",\"_ref\":\"layer\"}],\"makeVisible\":true},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"textStyle\",\"_ref\":\"property\"},{\"_enum\":\"ordinal\",\"_ref\":\"textLayer\",\"_value\":\"targetEnum\"}],\"to\":{\"_obj\":\"textStyle\",\"size\":{\"_unit\":\"pointsUnit\",\"_value\":48},\"color\":{\"_obj\":\"RGBColor\",\"red\":0,\"green\":128,\"blue\":255}}}]",
          "contentType": "application/json"
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
}
```

The first layer gets red text; the second gets 48pt blue text.

## Complete V1 field reference

The V1 `/psdService/text` endpoint supported more fields than the basic font/size/color covered above. Use the table below to find the V2 equivalent for each V1 `characterStyles` and `paragraphStyles` property.

### text properties

| V1 `text` Field | V2 ActionJSON Equivalent | Notes |
|-----------------|--------------------------|-------|
| `content` | `set` on `textLayer` with `textKey: "new string"` | Target `_ref: "textLayer"`, `_property: "textLayer"`, `to._obj: "textLayer"`, `to.textKey: "..."` |
| `orientation` | `set` on `textLayer` with `orientation: {_enum: "orientation", _value: "horizontal"}` | Values: `"horizontal"`, `"vertical"` |
| `antiAlias` | `set` on `textLayer` with `antiAlias: {_enum: "antiAliasType", _value: "..."}` | Values: `"antiAliasNone"`, `"antiAliasCrisp"`, `"antiAliasStrong"`, `"antiAliasSmooth"`, `"antiAliasLCD"` |

### characterStyles properties

| V1 `characterStyles` Field | V2 ActionJSON `set textStyle` Property | Notes |
|---------------------------|----------------------------------------|-------|
| `size` | `size: {_unit: "pointsUnit", _value: N}` | Also set `textOverrideFeatureName: 808465458`, `typeStyleOperationType: 3` |
| `fontPostScriptName` | `fontPostScriptName: "..."` | Set together with `fontName` and `fontStyleName` |
| `color` | `color: {_obj: "RGBColor", red: N, green: N, blue: N}` | |
| `leading` | `autoLeading: false, leading: {_unit: "pointsUnit", _value: N}` | Set `autoLeading: false` to disable auto leading |
| `tracking` | `tracking: N` | Integer, in thousandths of an em (e.g., `100` = 10% of em) |
| `syntheticBold` | `syntheticBold: true` | Faux bold — prefer a real bold font when available |
| `syntheticItalic` | `syntheticItalic: true` | Faux italic — prefer a real italic font when available |
| `fontCaps` | `fontCaps: {_enum: "fontCaps", _value: "..."}` | Values: `"allCaps"`, `"smallCaps"`, `"normal"` |
| `baseline` | `baselineDirection: {_enum: "baselineDirection", _value: "..."}` | Values: `"subScript"`, `"superScript"`, `"normal"` |
| `strikethrough` | `strikeThrough: {_enum: "strikeThrough", _value: "..."}` | Values: `"classicStrikeThrough"`, `"xHeightStrikeThrough"`, `"noStrikeThrough"` |
| `underline` | `underline: {_enum: "underline", _value: "..."}` | Values: `"underlineOnLeft"`, `"noUnderline"` |
| `verticalScale` | `verticalScale: N` | Percentage integer (e.g., `120` = 120%) |
| `horizontalScale` | `horizontalScale: N` | Percentage integer (e.g., `80` = 80%) |
| `ligature` | `ligature: true` | Standard ligatures (fi, fl, etc.) |
| `autoKern` | `autoKern: {_enum: "autoKern", _value: "..."}` | Values: `"metricsKern"`, `"opticalKern"`, `"manualKern"` |
| `stylisticAlternates` | UXP recommended | ActionJSON equivalent is not standardized; use UXP for reliable access |

### paragraphStyles properties

| V1 `paragraphStyles` Field | V2 ActionJSON Equivalent | Notes |
|---------------------------|--------------------------|-------|
| `alignment` | `set` on `paragraphStyle` with `align: {_enum: "alignmentType", _value: "..."}` | Target `_ref: "property"`, `_property: "paragraphStyle"`. Values: `"alignLeft"`, `"alignCenter"`, `"alignRight"`, `"justifyAll"`, `"justifyLeft"`, `"justifyCenter"`, `"justifyRight"` |

**Example — change text content and alignment:**

```json
[
  {
    "_obj": "select",
    "_target": [{"_name": "your-text-layer-name", "_ref": "layer"}],
    "makeVisible": true
  },
  {
    "_obj": "set",
    "_target": [
      {"_property": "textLayer", "_ref": "property"},
      {"_enum": "ordinal", "_ref": "textLayer", "_value": "targetEnum"}
    ],
    "to": {
      "_obj": "textLayer",
      "textKey": "Updated text content"
    }
  },
  {
    "_obj": "set",
    "_target": [
      {"_property": "paragraphStyle", "_ref": "property"},
      {"_enum": "ordinal", "_ref": "textLayer", "_value": "targetEnum"}
    ],
    "to": {
      "_obj": "paragraphStyle",
      "align": {"_enum": "alignmentType", "_value": "alignCenter"}
    }
  }
]
```

## Font management

V1 allowed custom fonts and missing font handling at the request level via `options.fonts`, `options.manageMissingFonts`, and `options.globalFont`. In V2, these map to `options.fontOptions` in the `/v2/execute-actions` request.

### V1 font options

```json
{
  "options": {
    "fonts": [{"href": "<SIGNED_GET_URL_FOR_FONT>", "storage": "external"}],
    "manageMissingFonts": "useDefault",
    "globalFont": "ArialMT"
  }
}
```

### V2 font options

```json
{
  "options": {
    "fontOptions": {
      "additionalFonts": [{"source": {"url": "<SIGNED_GET_URL_FOR_FONT>"}}],
      "missingFontStrategy": "use_default",
      "defaultFontPostScriptName": "ArialMT"
    }
  }
}
```

### Font option field mapping

| V1 Field | V2 Field | Notes |
|----------|----------|-------|
| `options.fonts[].href` | `options.fontOptions.additionalFonts[].source.url` | |
| `options.fonts[].storage` | *(removed)* | Not needed for presigned URLs |
| `options.manageMissingFonts: "fail"` | `options.fontOptions.missingFontStrategy: "fail"` | Job fails if any required font is missing |
| `options.manageMissingFonts: "useDefault"` | `options.fontOptions.missingFontStrategy: "use_default"` | Substitutes the default font |
| `options.globalFont` | `options.fontOptions.defaultFontPostScriptName` | PostScript name of the fallback font |


## Additional resources

- [Edit Text Guide](../../../../guides/edit-text/index.md) (V1 reference)
- [Actions Migration Overview](../actions-migration.md)
- [V2 Execute Actions API Reference](https://developer.adobe.com/firefly-services/docs/photoshop/api/photoshop-v2-beta/#operation/executeActions)
