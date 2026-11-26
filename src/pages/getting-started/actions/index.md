---
title: Photoshop Actions
description: Learn how to automate Photoshop operations using Actions
keywords:
  - actions
  - photoshop actions
  - automation
hideBreadcrumbNav: true
---

# Photoshop Actions

Photoshop Actions provide a powerful way to automate repetitive tasks and complex image processing workflows. Actions record the steps you perform in Photoshop and allow you to replay those same operations on other images automatically.

## What are Photoshop Actions?

Actions are recordings of Photoshop operations that can be saved and replayed to automate your workflow. When you create an action, Photoshop records each step—every tool selection, menu command, layer adjustment, and setting—so you can apply the exact same sequence of operations to any number of images.

### Action Formats

Photoshop actions can be stored and shared in different formats:

- **ActionJSON (.json)**: Human-readable JSON format
- **Action Files (.atn)**: Photoshop's native binary format

## Record Actions in Photoshop

**For Action Files (.atn):**
1. Open the Actions panel (Window → Actions)
2. Click the "Create new action" button
3. Name your action and click "Record"
4. Perform your operations in Photoshop
5. Click the "Stop" button to finish recording
6. Save the action set as a `.atn` file

**For ActionJSON (.json):**
1. Enable Developer Mode in Photoshop:
   - **Mac**: Photoshop → Preferences → Plugins → Enable Developer Mode
   - **Windows**: Edit → Preferences → Plugins → Enable Developer Mode
2. Go to Settings → Plugins → Development → Record Action Commands
3. Choose a save location
4. Perform your operations in Photoshop
5. The ActionJSON file is automatically saved as `.json`

## Running Actions in Photoshop

1. Open the Actions panel (Window → Actions)
2. Load your action file:
   - Click the panel menu (☰) → Load Actions
   - Select your `.atn` file
3. Select the action you want to run
4. Click the "Play" button (▶) or press F12
5. The action will execute on the currently active document

## ActionJSON Structure

ActionJSON uses Photoshop's Action Descriptor format, where each operation is a JSON object with specific properties.

### Basic Structure

```json
[
  {
    "_obj": "operationName",
    "parameter1": "value",
    "parameter2": {
      "_unit": "pixelsUnit",
      "_value": 100
    }
  }
]
```

### Common Properties

| Property | Description | Example |
|----------|-------------|---------|
| `_obj` | Operation type | `"make"`, `"set"`, `"placeEvent"` |
| `_target` | Target object(s) | `[{"_ref": "layer"}]` |
| `_enum` | Enumeration type | `"ordinal"`, `"alignmentType"` |
| `_value` | Enumeration value | `"targetEnum"`, `"left"` |
| `_unit` | Unit of measurement | `"pixelsUnit"`, `"pointsUnit"` |
| `_ref` | Reference type | `"layer"`, `"textLayer"` |

## Common Action Operations

### Resize Image

```json
[
  {
    "_obj": "imageSize",
    "width": {
      "_unit": "pixelsUnit",
      "_value": 1920
    },
    "height": {
      "_unit": "pixelsUnit",
      "_value": 1080
    },
    "constrainProportions": false,
    "interfaceIconFrameDimmed": {
      "_enum": "interpolationType",
      "_value": "bicubic"
    }
  }
]
```

### Apply Gaussian Blur

```json
[
  {
    "_obj": "gaussianBlur",
    "radius": {
      "_unit": "pixelsUnit",
      "_value": 10
    }
  }
]
```

### Flip Horizontal

```json
[
  {
    "_obj": "flip",
    "axis": {
      "_enum": "orientation",
      "_value": "horizontal"
    }
  }
]
```

### Adjust Brightness/Contrast

```json
[
  {
    "_obj": "make",
    "_target": [
      {
        "_ref": "adjustmentLayer"
      }
    ],
    "using": {
      "_obj": "adjustmentLayer",
      "type": {
        "_obj": "brightnessEvent",
        "brightness": 25,
        "contrast": 10
      }
    }
  }
]
```

### Create Text Layer

```json
[
  {
    "_obj": "make",
    "_target": [
      {
        "_ref": "textLayer"
      }
    ],
    "using": {
      "_obj": "textLayer",
      "textKey": "Hello World!",
      "textClickPoint": {
        "_obj": "paint",
        "horizontal": {
          "_unit": "percentUnit",
          "_value": 50
        },
        "vertical": {
          "_unit": "percentUnit",
          "_value": 50
        }
      }
    }
  }
]
```
