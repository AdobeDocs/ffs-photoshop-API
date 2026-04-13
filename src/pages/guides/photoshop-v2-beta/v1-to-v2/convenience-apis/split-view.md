---
title: Split View Migration (v1 to v2)
description: Migrate from V1 splitView to V2 execute-actions for before/after comparisons with divider
hideBreadcrumbNav: true
keywords:
  - split view
  - convenience API
  - migration
  - v1 to v2
---

# Split View Migration (v1 to v2)

Migrate from the v1 API's `/pie/psdService/splitView` endpoint to the v2 API.

The Split View convenience API creates a professional before/after comparison with a vertical divider line and branded logo overlay. This guide shows how to migrate from V1's `/pie/psdService/splitView` to V2's `/v2/execute-actions`.

**Key Features:**

- Masked side-by-side comparison with center divider
- Automatic resizing to 1200px width
- Product logo overlay in top-right corner
- Professional presentation for demonstrating image processing results

## Required Images

This action requires **THREE images total**:

1. **Base Image** (provided in `image.source`): The original/before image
2. **Additional Image 0** (`__ADDITIONAL_IMAGES_0__`): The edited/after image
3. **Additional Image 1** (`__ADDITIONAL_IMAGES_1__`): Your product logo

## V1 API (Deprecated)

**Endpoint:** `/pie/psdService/splitView`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/splitView \
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
          "content": "[{\"_obj\":\"set\",\"_target\":[{\"_property\":\"background\",\"_ref\":\"layer\"}],\"layerID\":7,\"to\":{\"_obj\":\"layer\",\"mode\":{\"_enum\":\"blendMode\",\"_value\":\"normal\"},\"opacity\":{\"_unit\":\"percentUnit\",\"_value\":100}}},{\"_obj\":\"canvasSize\",\"horizontal\":{\"_enum\":\"horizontalLocation\",\"_value\":\"center\"},\"width\":{\"_unit\":\"percentUnit\",\"_value\":150}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSLefts\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"ID\":8,\"_obj\":\"placeEvent\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_IMAGES_0__\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":0}}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSRights\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"transparencyEnum\"}},{\"_obj\":\"inverse\"},{\"_obj\":\"select\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\",\"_value\":\"backwardEnum\"}],\"layerID\":[7],\"makeVisible\":false},{\"_obj\":\"make\",\"at\":{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"mask\"},\"new\":{\"_class\":\"channel\"},\"using\":{\"_enum\":\"userMaskEnabled\",\"_value\":\"revealSelection\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"transparencyEnum\"}},{\"_obj\":\"inverse\"},{\"_obj\":\"select\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\",\"_value\":\"forwardEnum\"}],\"layerID\":[8],\"makeVisible\":false},{\"_obj\":\"make\",\"at\":{\"_enum\":\"channel\",\"_ref\":\"channel\",\"_value\":\"mask\"},\"new\":{\"_class\":\"channel\"},\"using\":{\"_enum\":\"userMaskEnabled\",\"_value\":\"revealSelection\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSLefts\"}},{\"_obj\":\"trim\",\"bottom\":true,\"left\":true,\"right\":true,\"top\":true,\"trimBasedOn\":{\"_enum\":\"trimBasedOn\",\"_value\":\"transparency\"}},{\"_obj\":\"imageSize\",\"constrainProportions\":true,\"interfaceIconFrameDimmed\":{\"_enum\":\"interpolationType\",\"_value\":\"automaticInterpolation\"},\"scaleStyles\":true,\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":1200}},{\"_obj\":\"make\",\"_target\":[{\"_ref\":\"layer\"}],\"layerID\":9},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_obj\":\"rectangle\",\"bottom\":{\"_unit\":\"pixelsUnit\",\"_value\":10000.0},\"left\":{\"_unit\":\"pixelsUnit\",\"_value\":0},\"right\":{\"_unit\":\"pixelsUnit\",\"_value\":5},\"top\":{\"_unit\":\"pixelsUnit\",\"_value\":0}}},{\"_obj\":\"fill\",\"color\":{\"_obj\":\"HSBColorClass\",\"brightness\":100,\"hue\":{\"_unit\":\"angleUnit\",\"_value\":0},\"saturation\":0},\"mode\":{\"_enum\":\"blendMode\",\"_value\":\"normal\"},\"opacity\":{\"_unit\":\"percentUnit\",\"_value\":100},\"using\":{\"_enum\":\"fillContents\",\"_value\":\"color\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSCentersH\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"_obj\":\"flattenImage\"},{\"ID\":10,\"_obj\":\"placeEvent\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_IMAGES_1__\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":0}}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"allEnum\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSRights\"}},{\"_obj\":\"align\",\"_target\":[{\"_enum\":\"ordinal\",\"_ref\":\"layer\"}],\"alignToCanvas\":false,\"using\":{\"_enum\":\"alignDistributeSelector\",\"_value\":\"ADSTops\"}},{\"_obj\":\"set\",\"_target\":[{\"_property\":\"selection\",\"_ref\":\"channel\"}],\"to\":{\"_enum\":\"ordinal\",\"_value\":\"none\"}},{\"_obj\":\"transform\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":-20},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":20}}}]",
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

The action performs 34 steps to create a professional split-view comparison:

1. **Canvas Expansion** - Expands canvas width by 150% to accommodate both images
2. **Align Original** - Positions original image on the left side
3. **Place Edited Image** - Places the edited image (`__ADDITIONAL_IMAGES_0__`) on the right
4. **Align Edited** - Positions edited image on the right side
5. **Create Masks** - Creates transparency masks for both layers
6. **Mask Left Side** - Masks the original image to show only the left half
7. **Mask Right Side** - Masks the edited image to show only the right half
8. **Trim Canvas** - Removes excess transparent areas
9. **Resize to 1200px** - Standardizes output width to 1200 pixels
10. **Create Divider Layer** - Creates a new layer for the divider line
11. **Draw Divider** - Draws a 5-pixel white vertical line at the center
12. **Center Divider** - Centers the divider line horizontally
13. **Flatten Image** - Merges all layers
14. **Place Logo** - Places the product logo (`__ADDITIONAL_IMAGES_1__`)
15. **Position Logo** - Aligns logo to top-right corner with 20px offset

## Additional Images Placeholder Mapping

In V1, the server automatically handled additional images. In V2, you explicitly provide them and they're referenced in the ActionJSON via placeholders:

- **`__ADDITIONAL_IMAGES_0__`** → The edited/after image (right side of comparison)
- **`__ADDITIONAL_IMAGES_1__`** → Your product logo (top-right overlay)

**Important:** The order of images in `additionalImages` array must match the placeholder indices!

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

- [ ] Replace `/pie/psdService/splitView` endpoint with `/v2/execute-actions`
- [ ] Update request structure from `inputs`/`outputs` to `image`/`outputs`
- [ ] Convert `href` fields to `url` fields
- [ ] Remove `storage` fields
- [ ] Update `type` field to `mediaType`
- [ ] **Add `additionalImages` array with 2 images**
- [ ] Ensure image order matches: [0]=edited, [1]=logo
- [ ] Include the complete ActionJSON in `options.actions[].source.content`
- [ ] Set `contentType` to `"application/json"`
- [ ] Test with actual before/after images and logo

## Use Cases

### Image Processing Demonstrations

- **Before/After**: Show the impact of photo editing, filters, or enhancements
- **Branding**: Include your company logo on the comparison
- **Professional Presentation**: 1200px width standard output

### Marketing Materials

- **Product Showcases**: Compare original vs. enhanced product photos
- **Service Demos**: Demonstrate retouching or color correction services
- **Portfolio Pieces**: Professional presentation of your work

### A/B Testing

- **Design Variations**: Compare different design approaches
- **Filter Comparisons**: Show different filter or style applications
- **Quality Levels**: Compare compression or resolution differences

## Key Differences from Side by Side

The **Split View** action is more complex than **Side by Side**:

| Feature | Split View | Side by Side |
|---------|-----------|--------------|
| **Steps** | 34 actions | 19 actions |
| **Masking** | Yes (complex transparency masks) | No |
| **Divider Line** | Yes (5px white centered line) | No |
| **Output Width** | 1200px | 1195px |
| **Use Case** | Professional demos with clear separation | Simple before/after comparison |

Use **Split View** when you need:

- Clear visual separation with a divider line
- Professional presentation quality
- Complex masking for precise alignment

Use **Side by Side** when you need:

- Simpler implementation
- Faster processing
- Basic comparison without divider

## Tips and Best Practices

### Image Preparation

- Ensure both original and edited images have the same dimensions
- Use square or portrait-oriented images for best results
- Logo should be PNG with transparency for best overlay effect

### Logo Sizing

- Recommended logo size: 200-300px wide
- Logo will be positioned at top-right with 20px offset
- Ensure logo has sufficient contrast against images

### Output Format

- JPEG for photographic content
- PNG if transparency is needed (though this action flattens)
- Consider quality settings for file size optimization

## Additional Resources

- [Actions Migration Overview](../actions-migration.md)
- [V2 Execute Actions API Reference](https://developer.adobe.com/photoshop/photoshop-api-docs/api/#tag/Photoshop/operation/actionJsonCreate)
- [Additional Images Documentation](https://developer.adobe.com/photoshop/photoshop-api-docs/features/#additional-images)

## Support

For questions or issues:

- [Adobe Developer Forum](https://community.adobe.com/t5/photoshop-api/ct-p/ct-photoshop-api)
- [GitHub Issues](https://github.com/AdobeDocs/photoshop-api-docs/issues)
