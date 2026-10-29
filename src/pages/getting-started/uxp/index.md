---
title: UXP Scripts
description: Automate Photoshop using UXP Scripts with modern JavaScript (ES6+)
hideBreadcrumbNav: true
keywords:
  - UXP
  - scripts
  - automation
  - JavaScript
---

# UXP Scripts

UXP (Unified Extensibility Platform) Scripts provide a modern, powerful way to automate and extend Photoshop using JavaScript. UXP scripts use modern JavaScript (ES6+) and provide access to contemporary web APIs.

## What are UXP Scripts?

UXP Scripts are JavaScript files that interact directly with Photoshop's application layer using the UXP scripting API. They run in a modern JavaScript environment and can perform complex operations, make decisions based on document state, and even access external resources like web APIs or local files.

## UXP Script Structure

UXP Scripts use modern JavaScript and the Photoshop UXP API.

### Basic Script Template

```javascript
// Import required modules
const { app } = require("photoshop");
const { storage } = require("uxp").storage;
const fs = require("fs");

// Main async function
async function main() {
  try {
    // Your Photoshop automation code here
    console.log("Document name:", app.activeDocument.name);
    
    // Perform operations
    await app.activeDocument.flatten();
    
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

// Execute main function
main();
```

### Supported Modules (execute-actions sandbox)

When running UXP scripts via the execute-actions API, only the following `require()` modules are available. These are UXP shims — not full Node.js built-ins. Everything else (e.g. `crypto`, `util`, `events`, `http`, `child_process`) throws `Module not found`.

| Module | Import | What's available |
|--------|--------|-----------------|
| `photoshop` | `require("photoshop")` | Core Photoshop app, document, action, and batchPlay API |
| `uxp` | `require("uxp")` | UXP platform — `storage.localFileSystem`, shell, etc. |
| `fs` | `require("fs")` | `writeFileSync`, `readFileSync`, `readdirSync`, `unlinkSync` — writes are limited to **`plugin-temp:/`** paths; reads also work with `additionalContents` placeholder paths (`__ADDITIONAL_CONTENTS_PATH_0__`); absolute/relative paths throw `Route not found` |
| `path` | `require("path")` | `resolve`, `basename` only — `join`, `dirname`, `extname` are not available |
| `os` | `require("os")` | `platform()` only — returns `"win32"`; `tmpdir()`, `hostname()` not available |
| `process` | `require("process")` | `version` (e.g. `"uxp-9.4.1-0"`), `platform` only — `env`, `argv`, `exit()` not available |

<InlineAlert variant="info" slots="text1" />

`node:` prefix imports (e.g. `node:fs`, `node:path`) are **not** supported. Use the bare module names above.

## Running UXP Scripts

The execute-actions API supports direct UXP script execution only. UXP plugins are not supported.

## Examples

### Example 1: Flatten Document and Export Metadata

```javascript
const { app } = require("photoshop");
const fs = require("fs");

async function main() {
  try {
    const doc = app.activeDocument;
    
    // Collect document info before flattening
    const metadata = {
      originalName: doc.name,
      width: doc.width,
      height: doc.height,
      resolution: doc.resolution,
      originalLayerCount: doc.layers.length,
      colorMode: doc.mode
    };
    
    // Flatten document
    await doc.flatten();
    
    // Add processing info
    metadata.processedAt = new Date().toISOString();
    metadata.finalLayerCount = doc.layers.length;
    
    // Write to plugin-temp:/ — captured as output via scriptOutputPattern
    fs.writeFileSync("plugin-temp:/metadata.json", JSON.stringify(metadata, null, 2), "utf8");
    
    console.log("Processing complete!");
    
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

main();
```

### Example 2: Conditional Processing Based on Image Size

```javascript
const { app } = require("photoshop");
const fs = require("fs");

async function main() {
  try {
    const doc = app.activeDocument;
    
    const width = doc.width;
    const height = doc.height;
    
    let resizeNeeded = false;
    let blurApplied = false;
    
    // Resize if image is too large
    if (width > 2000 || height > 2000) {
      await app.batchPlay([
        {
          "_obj": "imageSize",
          "width": {
            "_unit": "pixelsUnit",
            "_value": Math.min(width, 2000)
          },
          "height": {
            "_unit": "pixelsUnit",
            "_value": Math.min(height, 2000)
          },
          "constrainProportions": true,
          "interfaceIconFrameDimmed": {
            "_enum": "interpolationType",
            "_value": "bicubic"
          }
        }
      ], {});
      
      resizeNeeded = true;
    }
    
    // Apply blur for very high-resolution images
    if (width > 3000 || height > 3000) {
      await app.batchPlay([
        {
          "_obj": "gaussianBlur",
          "radius": {
            "_unit": "pixelsUnit",
            "_value": 2
          }
        }
      ], {});
      
      blurApplied = true;
    }
    
    // Write to plugin-temp:/ — captured as output via scriptOutputPattern
    const report = {
      originalSize: { width, height },
      finalSize: { width: doc.width, height: doc.height },
      resizeApplied: resizeNeeded,
      blurApplied: blurApplied,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync("plugin-temp:/report.json", JSON.stringify(report, null, 2), "utf8");
    
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

main();
```
