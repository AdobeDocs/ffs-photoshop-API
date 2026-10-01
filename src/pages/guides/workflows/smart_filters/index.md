---
title: Smart Filters with Execute Actions
description: Apply tested Photoshop Smart Filters using the execute-actions endpoint
hideBreadcrumbNav: true
keywords:
  - smart filters
  - smart objects
  - execute-actions
  - actionJSON
  - photoshop actions
---

# Smart Filters with Execute Actions

Use `POST /v2/execute-actions` to apply Photoshop filters nondestructively to a Smart Object. This workflow uses ActionJSON, but you can also use a recorded Photoshop Action (`.atn`) or UXP containing the same operations.

## How the workflow works

1. Prepare a PSD with the target layer converted to a Smart Object.
2. Select the Smart Object layer in ActionJSON or in the recorded Photoshop Action.
3. Apply one or more filters.
4. Submit the action through `/v2/execute-actions`.
5. Request a PSD output to preserve the editable Smart Filter stack.

Raster outputs such as JPEG and PNG contain the rendered effect, but they do not preserve an editable Smart Filter stack.

## Example: Apply Gaussian Blur as a Smart Filter

This example selects a Smart Object layer named `Artwork`, applies Gaussian Blur, and returns a PSD.

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/execute-actions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_INPUT_PSD_GET_URL>"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"select\",\"_target\":[{\"_ref\":\"layer\",\"_name\":\"Artwork\"}]},{\"_obj\":\"gaussianBlur\",\"radius\":{\"_unit\":\"pixelsUnit\",\"_value\":12}}]",
          "contentType": "application/json"
        }
      }
    ]
  },
  "outputs": [
    {
      "mediaType": "image/vnd.adobe.photoshop",
      "destination": {
        "validityPeriod": 3600
      }
    }
  ]
}'
```

Filter descriptors and parameters vary by filter. Record the operation in Photoshop when you need the exact ActionJSON descriptor for a particular configuration.

## Tested Smart Filters

The following 91 filters have been tested with `/v2/execute-actions` using a PSD Smart Object workflow.

### Blur

- Blur More
- Gaussian Blur
- Motion Blur
- Radial Blur
- Smart Blur
- Surface Blur

### Distort

- Pinch
- Perspective Warp
- Polar Coordinates
- Ripple
- Spherize
- Twirl
- Wave
- ZigZag

### Noise

- Add Noise
- Despeckle
- Dust & Scratches
- Median

### Pixelate

- Color Halftone
- Crystallize
- Facet
- Fragment
- Mezzotint
- Mosaic
- Pointillize

### Render

- Clouds
- Difference Clouds
- Lens Flare

### Sharpen

- Sharpen
- Sharpen Edges
- Sharpen More
- Smart Sharpen
- Unsharp Mask

### Stylize

- Diffuse
- Emboss
- Extrude
- Find Edges
- Oil Paint
- Solarize
- Tiles
- Trace Contour
- Wind

### Other

- High Pass
- Maximum
- Minimum
- Offset

### Video

- De-Interlace

### Filter Gallery: Artistic

- Colored Pencil
- Cutout
- Dry Brush
- Film Grain
- Fresco
- Neon Glow
- Paint Daubs
- Palette Knife
- Plastic Wrap
- Poster Edges
- Rough Pastels
- Smudge Stick
- Sponge
- Underpainting
- Watercolor

### Filter Gallery: Brush Strokes

- Accented Edges
- Angled Strokes
- Crosshatch
- Dark Strokes
- Ink Outlines
- Spatter
- Sprayed Strokes

### Filter Gallery: Distort

- Diffuse Glow
- Glass
- Ocean Ripple

### Filter Gallery: Sketch

- Bas Relief
- Chalk & Charcoal
- Charcoal
- Chrome
- Conte Crayon
- Graphic Pen
- Note Paper
- Photocopy
- Plaster
- Reticulation
- Stamp
- Torn Edges
- Water Paper

### Filter Gallery: Stylize

- Glowing Edges

### Filter Gallery: Texture

- Craquelure
- Grain
- Patchwork
- Stained Glass
- Texturizer

## Usage considerations

- Filter behavior depends on the ActionJSON descriptor and parameter values. Record ActionJSON in Photoshop to capture valid settings for your workflow.
- Select the target layer explicitly when a document contains multiple layers.
- Confirm that the target layer is a Smart Object if you need the filter to remain editable.
- Results can vary with document color mode, bit depth, dimensions, layer contents, and Photoshop feature requirements.
- Test representative production assets and parameter ranges before applying a workflow at scale.
