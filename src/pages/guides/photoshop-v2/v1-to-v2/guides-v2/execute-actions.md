---
title: Execute Actions Workflow
description: Get started with Photoshop Actions and UXP Scripts using the execute-actions endpoint
hideBreadcrumbNav: true
keywords:
  - actions
  - actionJSON
  - UXP
  - execute-actions
---

# Execute Actions Workflow

Learn how to automate Photoshop operations using Actions and UXP Scripts with the `/v2/execute-actions` endpoint.

The **execute-actions workflow** allows you to execute Photoshop operations programmatically using Actions (JSON-formatted action descriptors and traditional binary `.atn` files) and UXP Scripts (modern JavaScript automation).

Key capabilities include:

* **Actions and UXP Scripts**: Execute both traditional Actions (recorded operations) and modern UXP Scripts (JavaScript automation)
* **Inline or external**: Use inline JSON/JavaScript or reference external `.atn`, `.json`, or `.psjs` files
* **Dynamic placeholders**: Inject file paths at runtime using placeholder syntax
* **Multiple actions**: Chain up to 10 actions in sequence (UXP limited to 1 script per request)
* **Pattern-based outputs**: Capture dynamically generated files using glob patterns

**Recommendation**: Use Actions for image manipulation and effects. Use UXP Scripts when you need conditional logic, data extraction, or complex decision-making.

## Prerequisites

Before you begin, ensure you have:

1. **Authentication token**: Follow the [Authentication guide](/getting-started/index.md) to get your OAuth 2.0 Bearer token
2. **API key**: Your Client ID from the Adobe Developer Console
3. **Image storage**: A publicly accessible URL for your input image (S3, Azure, Dropbox, or any pre-signed URL)

Set up your environment variables:

```bash
export TOKEN="your_access_token"
export API_KEY="your_client_id"
```

## Request structure

All execute-actions requests follow this pattern:

```json
{
  "image": {
    "source": {
      "url": "<INPUT_IMAGE_URL>"
    }
  },
  "options": {
    "actions": [/* Action definitions */],
    "uxp": {/* UXP script */},
    "additionalContents": [/* Additional images */]
  },
  "outputs": [
    {
      "mediaType": "<OUTPUT_FORMAT>",
      "destination": {
        "validityPeriod": 3600
      },
      "scriptOutputPattern": "<FILENAME_OR_PATTERN>"
    }
  ]
}
```

**Key fields:**

- **`image.source.url`**: URL to your input image (required)
- **`options.actions`** (array, max 10) or **`options.uxp`** (single script): At least one is required
- **`options.additionalContents`**: Optional array of additional images (max 25)
- **`outputs.mediaType`**: Output format (`image/jpeg`, `image/png`, `image/vnd.adobe.photoshop`, `application/json`)
- **`outputs.scriptOutputPattern`**: Required for UXP scripts that generate files
- **`destination.validityPeriod`**: URL validity duration in seconds (default: 3600)

## Working with actions

Actions allow you to automate Photoshop operations using JSON-formatted descriptors or traditional `.atn` files. You can provide actions inline or reference external files.

### Example: Warm vintage film look

Apply a warm vintage effect with sepia tones and adjusted levels:

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/execute-actions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "https://your-storage.com/input-image.jpg"
    }
  },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"make\",\"_target\":[{\"_ref\":\"adjustmentLayer\"}],\"using\":{\"_obj\":\"adjustmentLayer\",\"type\":{\"_obj\":\"hueSaturation\",\"colorize\":true,\"hue\":{\"_unit\":\"angleUnit\",\"_value\":30},\"saturation\":{\"_unit\":\"percentUnit\",\"_value\":25},\"lightness\":{\"_unit\":\"percentUnit\",\"_value\":0}}}},{\"_obj\":\"make\",\"_target\":[{\"_ref\":\"adjustmentLayer\"}],\"using\":{\"_obj\":\"adjustmentLayer\",\"type\":{\"_obj\":\"levels\",\"adjustment\":[{\"_obj\":\"levelRecord\",\"channel\":{\"_ref\":\"channel\",\"_enum\":\"channel\",\"_value\":\"composite\"},\"inputFloor\":10,\"inputCeiling\":245,\"outputFloor\":15,\"outputCeiling\":255,\"gamma\":1.1}]}}},{\"_obj\":\"make\",\"_target\":[{\"_ref\":\"adjustmentLayer\"}],\"using\":{\"_obj\":\"adjustmentLayer\",\"type\":{\"_obj\":\"brightnessEvent\",\"brightness\":5,\"contrast\":-5}}}]",
          "contentType": "application/json"
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

## Working with UXP scripts

The execute-actions endpoint supports UXP (Unified Extensibility Platform) scripts, allowing you to leverage modern JavaScript (ES6+) for advanced automation.

### Example: Flatten document and export

Flatten all layers in a PSD file and export as JPEG:

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/execute-actions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "https://your-storage.com/input.psd"
    }
  },
  "options": {
    "uxp": {
      "source": {
        "content": "const { app } = require(\"photoshop\"); async function main() { await app.activeDocument.flatten(); } main();",
        "contentType": "application/javascript"
      }
    }
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

### Sandboxing

UXP scripts run in a sandboxed environment for security. The sandbox restricts file system access (limited to `plugin-temp:/` for output and `additionalContents` for input), blocks network requests, prevents shell command execution, and isolates scripts from system resources.

**Restricted operations:**
- Cannot access arbitrary file paths on the server
- Cannot make network requests (fetch, HTTP calls)
- Cannot execute shell commands or external processes

**Working with files:**

To work with files in UXP scripts, use the `plugin-temp:/` directory for all file I/O operations. Write any output files (JSON, text, logs, metadata) to `plugin-temp:/filename`, and they will be automatically captured as outputs when you specify a matching `scriptOutputPattern`. For reading files, use the `additionalContents` array with placeholder syntax (`__ADDITIONAL_CONTENTS_PATH_0__`) to access external files passed to your script.

**Example: Writing and reading files**

This example demonstrates file I/O within the sandbox by writing processing results and reading configuration data:

```bash
curl -X POST "https://photoshop-api.adobe.io/v2/execute-actions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "image": {
    "source": {
      "url": "https://your-storage.com/input.psd"
    }
  },
  "options": {
    "additionalContents": [
      {
        "source": {
          "url": "https://your-storage.com/config.json"
        }
      }
    ],
    "uxp": {
      "source": {
        "content": "const { app } = require(\"photoshop\"); const fs = require(\"fs\"); async function main() { const configPath = \"__ADDITIONAL_CONTENTS_PATH_0__\"; const config = JSON.parse(fs.readFileSync(configPath, \"utf-8\")); const doc = app.activeDocument; if (config.applyResize && doc.width > config.maxWidth) { await app.batchPlay([{\"_obj\":\"imageSize\",\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":config.maxWidth},\"constrainProportions\":true}], {}); } const report = { originalSize: { width: doc.width, height: doc.height }, configApplied: config, processedAt: new Date().toISOString() }; fs.writeFileSync(\"plugin-temp:/process-report.json\", JSON.stringify(report, null, 2)); } main();",
        "contentType": "application/javascript"
      }
    }
  },
  "outputs": [
    {
      "mediaType": "image/jpeg",
      "destination": {
        "validityPeriod": 3600
      }
    },
    {
      "mediaType": "application/json",
      "destination": {
        "validityPeriod": 3600
      },
      "scriptOutputPattern": "process-report.json"
    }
  ]
}'
```

## Advanced features

### Multiple actions in sequence

Execute up to 10 actions one after another:

```json
{
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"imageSize\",\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":800}}]",
          "contentType": "application/json"
        }
      },
      {
        "source": {
          "url": "https://your-storage.com/color-correction.json"
        }
      },
      {
        "source": {
          "url": "https://your-storage.com/add-watermark.atn"
        }
      }
    ]
  }
}
```

### Combining actions with UXP scripts

You can combine multiple actions with one UXP script in a single request. Actions execute first, then the UXP script runs.

<InlineAlert variant="info" slots="text"/>

Only **one UXP script** is allowed per request, but you can include **up to 10 actions**.

```json
{
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"imageSize\",\"width\":{\"_unit\":\"pixelsUnit\",\"_value\":1920}}]",
          "contentType": "application/json"
        }
      }
    ],
    "uxp": {
      "source": {
        "content": "const app = require('photoshop').app; const doc = app.activeDocument; /* custom UXP code */",
        "contentType": "application/javascript"
      }
    }
  }
}
```

### Using additional contents

Composite multiple images using placeholders. Use `__ADDITIONAL_CONTENTS_PATH_{index}__` in your action JSON or UXP script where `{index}` is the zero-based index of the `additionalContents` array.

```json
{
  "image": {
    "source": {
      "url": "https://your-storage.com/background.jpg"
    }
  },
  "options": {
    "additionalContents": [
      {
        "source": {
          "url": "https://your-storage.com/logo.png"
        }
      },
      {
        "source": {
          "url": "https://your-storage.com/overlay.png"
        }
      }
    ],
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"placeEvent\",\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_CONTENTS_PATH_0__\"}}]",
          "contentType": "application/json"
        }
      }
    ]
  }
}
```

### Script output patterns

Capture files created by UXP scripts using glob patterns:

```json
{
  "outputs": [
    {
      "mediaType": "image/png",
      "destination": {
        "validityPeriod": 3600
      },
      "scriptOutputPattern": "layer-*.png"
    }
  ]
}
```

### Loading custom resources

**Fonts:**
```json
{
  "options": {
    "fontOptions": {
      "additionalFonts": [
        {
          "source": {
            "url": "https://your-storage.com/custom-font.ttf"
          }
        }
      ]
    }
  }
}
```

**Brushes and patterns:**
```json
{
  "options": {
    "brushes": [
      {
        "source": {
          "url": "https://your-storage.com/custom-brush.abr"
        }
      }
    ],
    "patterns": [
      {
        "source": {
          "url": "https://your-storage.com/custom-pattern.pat"
        }
      }
    ]
  }
}
```

## Common issues

### Issue: Invalid content type

**Error**: `Invalid contentType for inline action`

**Solution**: Always specify `"contentType": "application/json"` for actions and `"contentType": "application/javascript"` for UXP scripts.

### Issue: Placeholder not replaced

**Error**: File path contains literal `__ADDITIONAL_CONTENTS_PATH_0__`

**Solution**: Ensure you've provided `additionalContents` array in `options` and the index matches (0-based).

### Issue: Script output not found

**Error**: `No files matching pattern`

**Solution**: Verify your UXP script writes to `plugin-temp:/filename` and `scriptOutputPattern` matches the filename.
