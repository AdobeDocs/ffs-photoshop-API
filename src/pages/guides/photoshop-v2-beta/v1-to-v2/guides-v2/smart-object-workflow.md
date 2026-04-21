---
title: Smart Object Workflow
description: Add linked smart objects and replace smart object content, then verify with generate-manifest
hideBreadcrumbNav: true
keywords:
  - smart objects
  - linked smart objects
  - create-composite
  - generate-manifest
---

# Smart Object Workflow

For authentication, API key, and storage setup, see [Using these guides](/guides/index.md).

## Example 1: Adding a linked smart object

Add a linked smart object layer, then call generate-manifest to confirm it appears as linked in the manifest.

### Placeholders for step 1

Replace these placeholders in the request payload below:

| Placeholder | Description |
|-------------|-------------|
| `<SIGNED_INPUT_ASSET_GET_URL>` | Presigned GET URL for your input asset (a PSD file). |
| `<SIGNED_SMART_OBJECT_ASSET_GET_URL>` | Presigned GET URL for the external file (PNG, JPEG, PSD, etc) to add as a new linked smart object layer. Placement is at the top of the layer stack, as specified by the placement field. |
| `<SIGNED_OUTPUT_POST_URL>` | Presigned POST (or PUT) URL where the output asset will be uploaded. In this example, the output is a PSD file as specified by the mediaType field |

### Step 1 — Create composite (add linked smart object)

**Endpoint:** `POST /v2/create-composite`

**Request payload:**

```json
{
    "image": {
        "source": {
            "url": "<SIGNED_INPUT_ASSET_GET_URL>"
        }
    },
    "edits": {
        "layers": [
            {
                "type": "smart_object_layer",
                "name": "Linked Added Smart Object",
                "operation": {
                    "type": "add",
                    "placement": {
                        "type": "top"
                    }
                },
                "smartObject": {
                    "isLinked": true,
                    "smartObjectFile": {
                        "source": {
                            "url": "<SIGNED_SMART_OBJECT_ASSET_GET_URL>"
                        }
                    }
                }
            }
        ]
    },
    "outputs": [
        {
            "destination": {
                "url": "<SIGNED_OUTPUT_POST_URL>"
            },
            "mediaType": "image/vnd.adobe.photoshop"
        }
    ]
}
```

The generated output is a PSD with a linked smart object layer added on top, as shown in the image below.

**Before:** Original PSD.
![Before adding linked smart object](../../../../assets/add-linked-before.png?raw=true "Original PSD")
**After:** PSD with linked smart object layer on top.
![After adding linked smart object](../../../../assets/add-linked-after.png?raw=true "PSD with linked smart object layer on top")

### Step 2 — Generate manifest

Use the presigned GET URL of the output PSD from Step 1 as `image.source.url` below. That URL points to the PSD you just created.

### Placeholders for step 2

Replace these placeholders in the request payload below:

| Placeholder | Description |
|-------------|-------------|
| `<SIGNED_OUTPUT_PSD_GET_URL>` | Presigned GET URL of the output PSD from Step 1. Use this to read the PSD for manifest generation. |

**Endpoint:** `POST /v2/generate-manifest`

**Request payload:**

```json
{
    "image": {
        "source": {
            "url": "<SIGNED_OUTPUT_PSD_GET_URL>"
        }
    },
    "outputs": [
        {
            "destination": {
                "embedded": "json"
            },
            "mediaType": "application/json"
        }
    ]
}
```

Use the generated PSD's URL from Step 1 as `image.source.url`.
A call to this API initiates an asynchronous job and returns a response containing a URL. Use the value in the `href` field to [poll for the status of the job](/guides/get-job-status/index.md) and the same response will also contain the JSON manifest.

### Step 3 — Result: linked smart object in manifest

Relevant layer snippet from the manifest JSON:

```json
"smartObject": {
    "isSmartObject": true,
    "isLinked": true,
    "isValid": true,
    "smartObjectData": {
        "type": "smartObject",
        "transform": [
            0,
            0,
            1000,
            0,
            1000,
            1000,
            0,
            1000
        ],
        "fileInfo": {
            "relative": "../../df06670e-467a-4880-a697-cfc162f313c3/downloads/c89b3884-3df6-444e-9540-a0c26af33ddc.png",
            "name": "c89b3884-3df6-444e-9540-a0c26af33ddc.png",
            "path": "/tmp/df06670e-467a-4880-a697-cfc162f313c3/downloads/c89b3884-3df6-444e-9540-a0c26af33ddc.png",
            "fileType": "png",
            "linked": true
        }
    }
}
```

As seen from the manifest snippet above — for linked smart objects, the `linked` property is `true` along with the `path` information to the linked file.

## Example 2: Replacing a smart object with a linked file

Edit an existing smart object layer and replace its content with a different linked file. The input PSD must already contain the smart object layer you want to replace. In this example, we use the output PSD from Example 1 and replace its linked smart object with another one.

### Placeholders for example 2

Replace these placeholders in the request payload below:

| Placeholder | Description |
|-------------|-------------|
| `<SIGNED_INPUT_ASSET_GET_URL>` | Presigned GET URL for your input PSD. This PSD must contain an existing smart object layer. |
| `<EXISTING_SMART_OBJECT_LAYER_NAME>` | The exact name of the smart object layer to replace (as it appears in the Layers panel). Use the manifest to find the layer name if needed. |
| `<SIGNED_NEW_SMART_OBJECT_GET_URL>` | Presigned GET URL for the new file to use as the smart object content. |
| `<SIGNED_OUTPUT_POST_URL>` | Presigned POST (or PUT) URL where the output PSD will be uploaded. |

### Step 1 — Create composite (replace with a linked smart object)

**Endpoint:** `POST /v2/create-composite`

**Request payload:**

```json
{
    "image": {
        "source": {
            "url": "<SIGNED_INPUT_ASSET_GET_URL>"
        }
    },
    "edits": {
        "layers": [
            {
                "type": "smart_object_layer",
                "name": "<EXISTING_SMART_OBJECT_LAYER_NAME>",
                "operation": {
                    "type": "edit"
                },
                "smartObject": {
                    "isLinked": true,
                    "smartObjectFile": {
                        "source": {
                            "url": "<SIGNED_NEW_SMART_OBJECT_GET_URL>"
                        }
                    }
                }
            }
        ]
    },
    "outputs": [
        {
            "destination": {
                "url": "<SIGNED_OUTPUT_POST_URL>"
            },
            "mediaType": "image/vnd.adobe.photoshop"
        }
    ]
}
```

The generated output is a PSD with the replaced linked smart object, as shown in the image below.

**Before:** PSD with linked smart object (from Example 1).
![Before replacing with linked smart object](../../../../assets/add-linked-after.png?raw=true "Original PSD")
**After:** PSD with replaced linked smart object.
![After replacing with linked smart object](../../../../assets/replace-after.png?raw=true "PSD with replaced linked smart object")
