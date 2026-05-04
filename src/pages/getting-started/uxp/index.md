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
main().catch(err => {
  console.error("Script failed:", err);
  process.exit(1);
});
```

### Common Modules

| Module | Import | Purpose |
|--------|--------|---------|
| `photoshop` | `require("photoshop")` | Core Photoshop app and document API |
| `uxp.storage` | `require("uxp").storage` | File system access |
| `fs` | `require("fs")` | Node.js-style file operations |
| `batchPlay` | `app.batchPlay()` | Execute action descriptors (same as Actions) |

## Running UXP Scripts

There are two primary ways to run UXP scripts in Photoshop:

### Method 1: UXP Plugin

Package your script as a UXP plugin for distribution, marketplace deployment, or adding UI elements.

#### Plugin Structure

```
my-plugin/
├── manifest.json         # Plugin metadata and configuration
├── index.html            # UI (optional)
├── index.js              # Main plugin code
└── icons/
    └── icon.png          # Plugin icon
```

#### Basic manifest.json

```json
{
  "id": "com.yourcompany.myplugin",
  "name": "My Automation Plugin",
  "version": "1.0.0",
  "host": {
    "app": "PS",
    "minVersion": "23.0.0"
  },
  "entrypoints": [
    {
      "type": "command",
      "id": "runAutomation",
      "label": "Run My Automation"
    }
  ],
  "manifestVersion": 5
}
```

#### Plugin Code (index.js)

```javascript
const { app } = require("photoshop");
const { entrypoints } = require("uxp");

entrypoints.setup({
  commands: {
    runAutomation: async () => {
      try {
        // Your automation code
        await app.activeDocument.flatten();
        console.log("Automation complete!");
      } catch (error) {
        console.error("Error:", error);
      }
    }
  }
});
```

#### Loading Your Plugin

1. **Enable Developer Mode**:
   - **Mac**: Photoshop → Preferences → Plugins → Enable Developer Mode
   - **Windows**: Edit → Preferences → Plugins → Enable Developer Mode

2. **Load Plugin**:
   - Go to **Plugins → Development → UXP Developer Tool**
   - Click **Add Plugin** and select your plugin folder
   - Click **Load**

3. **Run Plugin**:
   - Access via **Plugins** menu or assigned keyboard shortcut

### Method 2: Direct Script Execution

Run UXP scripts directly without packaging them as plugins. This is ideal for quick automation tasks and testing.

#### Using the File Menu

1. **Save your script** with a `.psjs` extension (Photoshop JavaScript)
2. **Open Photoshop**
3. Go to **File → Scripts → Browse...**
4. Select your `.psjs` file
5. The script executes immediately

```javascript
// Example: resize.psjs
const { app } = require("photoshop");

async function main() {
  const doc = app.activeDocument;
  
  await app.batchPlay([{
    "_obj": "imageSize",
    "width": { "_unit": "pixelsUnit", "_value": 1920 },
    "constrainProportions": true
  }], {});
  
  console.log("Resize complete!");
}

main();
```

#### Drag and Drop (Windows)

On Windows, you can also run scripts by:

1. **Save your script** as `.psjs`
2. **Drag the file** onto the Photoshop application
3. The script runs automatically

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
    
    // Write metadata to output
    fs.writeFileSync(
      "<YOUR_OUTPUT_DIRECTORY>/metadata.json",
      JSON.stringify(metadata, null, 2)
    );
    
    console.log("Processing complete!");
    
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

main().catch(err => {
  console.error("Script failed:", err);
  process.exit(1);
});
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
    
    // Export processing report
    const report = {
      originalSize: { width, height },
      finalSize: { width: doc.width, height: doc.height },
      resizeApplied: resizeNeeded,
      blurApplied: blurApplied,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync("<YOUR_OUTPUT_DIRECTORY>/report.json", JSON.stringify(report, null, 2));
    
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

main().catch(err => {
  console.error("Script failed:", err);
  process.exit(1);
});
```
