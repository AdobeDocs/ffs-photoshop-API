# Using Adobe Fonts with Photoshop API v2

Photoshop API v2 supports rendering text layers using fonts from the Adobe Fonts library. This lets you reference fonts by PostScript name directly in your API request without uploading or hosting font files yourself. Font access is resolved automatically through your Adobe entitlement.

## Prerequisites

- A valid Firefly Services API key and access token
- An Adobe entitlement that includes Adobe Fonts access
- A Fonts product profile configured in the Adobe Admin Console and added to your credential in the Adobe Developer Console
- A PSD file with one or more text layers

## Admin Console setup

Before you can use Adobe Fonts in API calls, your organization must have a Fonts service enabled on a product profile in the Adobe Admin Console, and that profile must be associated with your API credential.

### Step 1: Create a product profile with Fonts enabled

1. Sign in to the [Adobe Admin Console](https://adminconsole.adobe.com)
2. Go to **Products** and select **Firefly Creative Production for Enterprise**
3. Click **New profile** and follow the setup steps
4. On the **Enable services** step, ensure the **Fonts** toggle is turned on
5. Click **Save**

For detailed instructions on creating product profiles, see [Create product profiles](https://helpx.adobe.com/business/enterprise/products-entitlements/manage-product-profiles/create-product-profiles.html).

### Step 2: Add the product profile to your project in Developer Console

1. Sign in to the [Adobe Developer Console](https://developer.adobe.com/console)
2. Open your project. You will land on the project overview page showing your products and credentials
3. Under **Products & services**, click the **Photoshop API - Firefly Services** title to open the API detail page
4. On the API detail page, click **Edit product profiles**
5. Add the Fonts-enabled profile you created in Step 1 and save

Once the profile is linked to your project, API calls made with that credential will have access to Adobe Fonts.

## How it works

When your request includes a font PostScript name in `fontOptions` or `characterStyles`, the service resolves the font through Adobe Fonts at render time. No file URL is required. If the font cannot be resolved because the PostScript name is incorrect or the font is not covered by your entitlement, the job will fail or fall back to a default font depending on your `missingFontStrategy` setting.

## Request structure

Use the `fontOptions` object to specify the font at the document level, and reference the same PostScript name in `characterStyles` at the layer level.

```json
{
  "image": {
    "source": {
      "url": "https://your-storage.example.com/input.psd"
    }
  },
  "fontOptions": {
    "defaultFontPostScriptName": "Aboreto-Regular",
    "missingFontStrategy": "fail"
  },
  "edits": {
    "layers": [
      {
        "name": "Your Text Layer Name",
        "type": "text_layer",
        "operation": {
          "type": "edit"
        },
        "text": {
          "content": "Hello from Adobe Fonts",
          "characterStyles": [
            {
              "characterStyle": {
                "font": { "postScriptName": "Aboreto-Regular" },
                "fontSize": 48
              }
            }
          ]
        }
      }
    ]
  },
  "outputs": [
    {
      "mediaType": "image/jpeg",
      "destination": {
        "validityPeriod": 3600
      }
    }
  ]
}
```

## fontOptions reference

| Field | Type | Required | Description |
|---|---|---|---|
| `defaultFontPostScriptName` | string | No | PostScript name of the font to use as the document-level default. |
| `missingFontStrategy` | string | No | What to do when a font cannot be resolved. `fail` returns an error. `use_default` silently substitutes a fallback font. |
| `additionalFonts` | array | No | Custom fonts to supply as file references. Use this for fonts not in the Adobe Fonts library. |

## Finding a font's PostScript name

PostScript names follow the pattern `FamilyName-Weight`, for example `AdobeCaslon-Regular` or `SourceSans3-Bold`.

To find the PostScript name for a specific font:

1. Go to [fonts.adobe.com](https://fonts.adobe.com)
2. Browse or search for the font family you want
3. Click into a specific style (Regular, Bold, Italic, etc.)
4. The PostScript name is listed on the font detail page under the Details tab

## Submitting a request

**Submit the job:**

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/create-composite" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {
      "source": {
        "url": "https://your-storage.example.com/input.psd"
      }
    },
    "fontOptions": {
      "defaultFontPostScriptName": "Aboreto-Regular",
      "missingFontStrategy": "fail"
    },
    "edits": {
      "layers": [
        {
          "name": "Your Text Layer Name",
          "type": "text_layer",
          "operation": {
            "type": "edit"
          },
          "text": {
            "content": "Hello from Adobe Fonts",
            "characterStyles": [
              {
                "characterStyle": {
                  "font": { "postScriptName": "Aboreto-Regular" },
                  "fontSize": 48
                }
              }
            ]
          }
        }
      ]
    },
    "outputs": [
      {
        "mediaType": "image/jpeg",
        "destination": {
          "validityPeriod": 3600
        }
      }
    ]
  }'
```

A successful submission returns a `202` response with a `jobId` and `statusUrl`:

```json
{
  "jobId": "a619b1bd-75c8-427f-9660-61b23d2b8dc4",
  "statusUrl": "https://photoshop-api.adobe.io/v2/status/a619b1bd-75c8-427f-9660-61b23d2b8dc4"
}
```

**Poll for status using the `statusUrl` from the response:**

```bash
curl -X GET "https://photoshop-api.adobe.io/v2/status/YOUR_JOB_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-Api-Key: YOUR_API_KEY"
```

A completed job returns a `succeeded` status with an output URL:

```json
{
  "jobId": "a619b1bd-75c8-427f-9660-61b23d2b8dc4",
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "mediaType": "image/jpeg",
        "destination": {
          "url": "https://photoshop-api.adobe.io/v2/short-url/..."
        }
      }
    ]
  }
}
```

## Error handling

| Error | Likely cause |
|---|---|
| `validation_error` Missing required field `type` | The layer object is missing `"type": "text_layer"`. Add it alongside the `operation` field. |
| `unauthorized_forbidden` | Your entitlement does not cover Adobe Fonts access, or the font is not available under your plan. Verify the Fonts service is enabled on the product profile linked to your credential. |
| Font missing or substituted | The PostScript name is incorrect or the font is not in the Adobe Fonts library. Use `missingFontStrategy: "fail"` to surface this as an explicit error rather than a silent fallback. |

## Using custom fonts

If you need a font that is not in the Adobe Fonts library, supply it as a file reference in `additionalFonts`. The font file must be accessible via a pre-signed URL.

```json
"fontOptions": {
  "additionalFonts": [
    {
      "source": {
        "url": "https://your-storage.example.com/fonts/CustomFont-Regular.ttf"
      }
    }
  ],
  "defaultFontPostScriptName": "CustomFont-Regular",
  "missingFontStrategy": "fail"
}
```

Supported font formats are TTF and OTF. The PostScript name you reference must match the name embedded in the font file itself.
