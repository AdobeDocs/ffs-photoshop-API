---
title: Side by Side Migration (v1 to v2)
description: Migrate from V1 sideBySide to V2 execute-actions for simple before/after comparisons
hideBreadcrumbNav: true
keywords:
  - side by side
  - convenience API
  - migration
  - v1 to v2
---

# Side by Side Migration (v1 to v2)

Migrate from the v1 API's `/pie/psdService/sideBySide` endpoint to the v2 API.

## Overview

The Side by Side convenience API creates a simple, clean before/after comparison with a branded logo overlay. This guide shows how to migrate from V1's `/pie/psdService/sideBySide` to V2's `/v2/execute-actions`.

**Key Features:**

- Simple side-by-side image placement
- No complex masking or divider lines
- Automatic resizing to 1195px width
- Product logo overlay in top-right corner
- Faster processing than Split View

## Required Images

This action requires **THREE images total**:

1. **Base Image** (provided in `image.source`): The original/before image
2. **Additional Image 0** (`__ADDITIONAL_IMAGES_0__`): The edited/after image
3. **Additional Image 1** (`__ADDITIONAL_IMAGES_1__`): Your product logo

## V1 API (Deprecated)

**Endpoint:** `/pie/psdService/sideBySide`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/sideBySide \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<ORIGINAL_IMAGE_URL>",
      "storage": "external"
    }
  ],
  "outputs": [
    {
      "href": "<OUTPUT_URL>",
      "storage": "external",
      "type": "image/jpeg"
    }
  ]
}'
```

## V2 API (Current)

**Endpoint:** `/v2/execute-actions`

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/execute-actions \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "<ORIGINAL_IMAGE_URL>"
    }
  },
  "options": {
    "additionalImages": [
      {
        "source": {
          "url": "<EDITED_IMAGE_URL>"
        }
      },
      {
        "source": {
          "url": "<PRODUCT_LOGO_URL>"
        }
      }
    ],
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"set\",\"_target\":[{\"_property\":\"background\",\"_ref\":\"layer\"}],\"layerID\":2,\"to\":{\"_obj\":\"layer\",\"mode\":{\"_enum\":\"blendMode\",\"_value\":\"normal\"},\"opacity\":{\"_unit\":\"percentUnit\",\"_value\":100.0}}},{\"_obj\":\"canvasSize\",\"horizontal\":{\"_enum\":\"horizontalLocation\",\"_value\":\"center\"},\"width\":{\"_unit\":\"percentUnit\",\"_value\":200.0}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSLefts\"}},{\"ID\":3,\"_obj\":\"placeEvent\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_IMAGES_0__\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":0.0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":0.0}}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSRights\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"_obj\":\"imageSize\",\"constrainProportions\":true,\"interfaceIconFrameDimmed\":{\"_enum\":\"interpolationType\",\"_value\":\"automaticInterpolation\"},\"scaleStyles\":true,\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":1195.0}},{\"_obj\":\"canvasSize\",\"horizontal\":{\"_enum\":\"horizontalLocation\",\"_value\":\"left\"},\"relative\":true,\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":5}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSRights\"}},{\"ID\":5,\"_obj\":\"placeEvent\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_IMAGES_1__\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":0.0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":0.0}}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSRights\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSTops\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"_obj\":\"transform\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":-20.0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":20.0}}},{\"_obj\":\"flattenImage\"}]",
          "contentType": "application/json"
        }
      }
    ]
  },
  "outputs": [
    {
      "destination": {
        "url": "<OUTPUT_URL>"
      },
      "mediaType": "image/jpeg"
    }
  ]
}'
```

## What This Action Does

The action performs 19 streamlined steps:

1. **Set Background Layer** - Sets background layer properties and opacity
2. **Expand Canvas** - Doubles canvas width (200%) to fit both images
3. **Select All** - Selects entire canvas
4. **Align Original Left** - Positions original image on the left side
5. **Place Edited Image** - Places the edited image (`__ADDITIONAL_IMAGES_0__`)
6. **Select All** - Selects entire canvas again
7. **Align Edited Right** - Positions edited image on the right side
8. **Deselect** - Clears selection
9. **Resize to 1195px** - Standardizes output width to **exactly 1195.0 pixels**
10. **Add Small Padding** - Adds 5-pixel padding on the left for visual balance
11. **Select All** - Selects entire canvas
12. **Align Right** - Ensures proper alignment
13. **Place Logo** - Places the product logo (`__ADDITIONAL_IMAGES_1__`)
14. **Select All** - Selects entire canvas
15. **Align Logo Right** - Aligns logo to the right edge
16. **Align Logo Top** - Aligns logo to the top edge
17. **Deselect** - Clears selection
18. **Offset Logo** - Moves logo 20px left and 20px down from corner
19. **Flatten Image** - Merges all layers into final output

## Key Difference from Split View

Side by Side is the **simpler** alternative to Split View:

| Feature | Side by Side | Split View |
|---------|-------------|------------|
| **Complexity** | 19 steps | 34 steps |
| **Masking** | No | Yes (complex transparency masks) |
| **Divider Line** | No | Yes (5px white line) |
| **Output Width** | **1195.0px** | 1200px |
| **Processing Time** | Faster | Slower |
| **Use Case** | Clean, simple comparisons | Professional demos with clear separation |

**Choose Side by Side when:**

- You need simple before/after presentation
- Faster processing is important
- You don't need a visual divider line
- Images speak for themselves without separation

**Choose Split View when:**

- You need clear visual separation with a divider
- Professional presentation quality is critical
- You want masked transitions between images

## Additional Images Placeholder Mapping

In V2, you explicitly provide additional images and they're referenced in the ActionJSON via placeholders:

- **`__ADDITIONAL_IMAGES_0__`** → The edited/after image (right side)
- **`__ADDITIONAL_IMAGES_1__`** → Your product logo (top-right overlay)

**Important:** The order in `additionalImages` array must match placeholder indices!

```json
{
  "options": {
    "additionalImages": [
      {
        "source": {"url": "<EDITED_IMAGE>"}  // Index 0
      },
      {
        "source": {"url": "<LOGO_IMAGE>"}    // Index 1
      }
    ]
  }
}
```

## Migration Checklist

- [ ] Replace `/pie/psdService/sideBySide` endpoint with `/v2/execute-actions`
- [ ] Update request structure from `inputs`/`outputs` to `image`/`outputs`
- [ ] Convert `href` fields to `url` fields
- [ ] Remove `storage` fields (V2 auto-detects)
- [ ] Update `type` field to `mediaType`
- [ ] **Add `additionalImages` array with 2 images**
- [ ] Ensure image order: [0]=edited, [1]=logo
- [ ] Include the complete ActionJSON in `options.actions[].source.content`
- [ ] Set `contentType` to `"application/json"`
- [ ] Test with actual images and logo
- [ ] Verify output width is 1195px (not 1200)

## Migration Examples

### Basic Migration

**V1:**

```json
{
  "inputs": [{"href": "s3://before.jpg", "storage": "external"}],
  "outputs": [{"href": "s3://comparison.jpg", "type": "image/jpeg"}]
}
```

**V2:**

```json
{
  "image": {"source": {"url": "s3://before.jpg"}},
  "options": {
    "additionalImages": [
      {"source": {"url": "s3://after.jpg"}},
      {"source": {"url": "s3://logo.png"}}
    ],
    "actions": [{
      "source": {
        "content": "[{...exact ActionJSON...}]",
        "contentType": "application/json"
      }
    }]
  },
  "outputs": [{"destination": {"url": "s3://comparison.jpg"}, "mediaType": "image/jpeg"}]
}
```

### With PNG Output

```json
{
  "image": {"source": {"url": "https://before.png"}},
  "options": {
    "additionalImages": [
      {"source": {"url": "https://after.png"}},
      {"source": {"url": "https://logo.png"}}
    ],
    "actions": [{"source": {"content": "[...]", "contentType": "application/json"}}]
  },
  "outputs": [{
    "destination": {"url": "https://output.png"},
    "mediaType": "image/png",
    "compression": "medium"
  }]
}
```

## Use Cases

### Social Media Content

- **Instagram Posts**: Show before/after transformations
- **Tutorial Content**: Demonstrate photo editing techniques
- **Brand Awareness**: Include logo on all comparison posts

### E-Commerce

- **Product Staging**: Compare plain vs. styled product shots
- **Quality Demonstration**: Show original vs. enhanced images
- **Service Showcase**: Display retouching or enhancement services

### Portfolio & Marketing

- **Case Studies**: Document client work with before/after
- **Service Demos**: Show your editing capabilities
- **Quick Comparisons**: Simple, clean presentation

## Tips and Best Practices

### Image Preparation

- Use images with matching aspect ratios for best results
- Ensure both images have similar brightness/contrast
- Consider cropping to focus on key comparison areas

### Logo Design

- Use PNG with transparency for best overlay
- Recommended size: 150-250px wide
- Ensure good contrast with image backgrounds
- White or light logos work best on dark images

### Output Considerations

- **1195px width** is optimized for most social media platforms
- Choose JPEG for photographs (smaller file size)
- Use PNG if you need to preserve fine details
- Consider quality settings to balance size/quality

### Performance

- Side by Side processes faster than Split View
- Ideal for batch processing multiple comparisons
- Lower complexity means lower API costs

## Additional Resources

- [Actions Migration Overview](../actions-migration.md)
- [Split View Migration](split-view.md) - For comparisons with divider lines
- [V2 Execute Actions API Reference](https://developer.adobe.com/photoshop/photoshop-api-docs/api/#tag/Photoshop/operation/actionJsonCreate)
- [Additional Images Documentation](https://developer.adobe.com/photoshop/photoshop-api-docs/features/#additional-images)

## Support

For questions or issues:

- [Adobe Developer Forum](https://community.adobe.com/t5/photoshop-api/ct-p/ct-photoshop-api)
- [GitHub Issues](https://github.com/AdobeDocs/photoshop-api-docs/issues)
