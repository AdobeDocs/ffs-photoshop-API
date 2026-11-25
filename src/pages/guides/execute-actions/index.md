---
title: Execute Actions Workflow
description: Run Photoshop actions and UXP scripts on an image and retrieve the results.
keywords:
  - actions
  - actionJSON
  - UXP
  - execute actions
hideBreadcrumbNav: true
---

# Execute Actions Workflow

Use `POST /v2/execute-actions` to run Photoshop actions or a UXP script on an
image. Supply an action as inline ActionJSON, an ActionJSON file, or a recorded
`.atn` file. A UXP script is JavaScript and uses a separate `uxp` option.

## Before You Start

You need:

- An access token and client ID. See [Authenticate](../../getting-started/index.md#1-authenticate).
- A readable URL for the input image and, when writing to your own storage, a
  writable URL for each output. See [External Storage](../shared-reference/input-files-and-storage.md#create-signed-urls).
- An action or script that is appropriate for the input document.

In the examples, replace the angle-bracketed placeholders with your own URLs
or values. Set `PS_FF_SERVICES_ACCESS_TOKEN` and `PS_FF_SERVICES_CLIENT_ID`
in your environment. Keep access tokens and signed URLs private.

## Apply An Inline Action

This request applies a 10-pixel Gaussian blur to an RGB JPEG and writes a PNG.
The inline `content` is a **string containing a JSON array**, not a JSON array
directly.

```shell
curl -X POST "https://photoshop-api.adobe.io/v2/execute-actions" \
  -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  -H "Content-Type: application/json" \
  --data @- <<'JSON'
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"_obj\":\"gaussianBlur\",\"radius\":{\"_unit\":\"pixelsUnit\",\"_value\":10}}]",
          "contentType": "application/json"
        }
      }
    ]
  },
  "outputs": [
    { "destination": { "validityPeriod": 3600 }, "mediaType": "image/png" }
  ]
}
JSON
```

The descriptor's `_obj` is `gaussianBlur`. Its `radius` object has `_unit`
`pixelsUnit` and numeric `_value` `10`.

An HTTP `202` means the request was accepted, not that the image was
processed. Use the returned `statusUrl` to check the result, as described in
[Get Job Status](../get-job-status/index.md). Retrieve the PNG using the hosted
URL returned in the successful status response.

## How The API Uses Files

- `image.source` identifies the input image. The API opens it as the active
  document before running an action or script. An action can operate on that
  document; a script can access it through `require("photoshop").app.activeDocument`.
- `options.additionalContents` supplies other files needed by an ActionJSON
  action or UXP script. Refer to those files with indexed placeholders, not
  with the input image's URL. See [Additional Contents](#additional-contents).
- To render the document as an image, choose an image `mediaType` and omit
  `scriptOutputPattern`. For a file created by a UXP script, write the file to
  `plugin-temp:/` and select it with `scriptOutputPattern`. See
  [Output Files](#output-files).

URLs for input images, action files, scripts, and additional contents must
allow the API to read those files. For an output written to your storage,
provide a URL that allows writing; use your storage provider's read URL to
retrieve it.

## Request Fields

| Property | Type | Required | Default | Description |
|---|---|---|---|---|
| `image` | `object` | Yes | None | Contains `source`, an external image reference. For a signed URL, use `{ "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } }`; `url` is a `string`. See [File Sources](#file-sources) for alternatives. |
| `options` | `object` | Yes | None | Contains the action, script, and optional resources. Provide a nonempty `actions` array or `uxp`. |
| `outputs` | `array<object>` | Yes | None | One to 25 output definitions. Each element is described in [Output Files](#output-files). |

You can combine up to 10 actions with one UXP script in a single request.
Actions execute first, then the UXP script runs.

The properties of `options` are:

| Property | Type | Required | Default | Description |
|---|---|---|---|---|
| `actions` | `array<object>` | Unless `uxp` is present | No actions | Up to 10 action resources. Each element contains a `source` and can contain `actionName`; see [Action Sources](#action-sources). |
| `additionalContents` | `array<object>` | No | No additional files | Up to 25 external resources referenced by an action or script. Each element contains `source`; see [Additional Contents](#additional-contents). |
| `brushes` | `array<object>` | No | No additional brushes | Up to 10 external brush resources. Each element contains `source`; see [Additional Resources And Fonts](#additional-resources-and-fonts). |
| `fontOptions` | `object` | No | No custom fonts; missing-font strategy `use_default` | Font resources and missing-font handling; see [Additional Resources And Fonts](#additional-resources-and-fonts). |
| `patterns` | `array<object>` | No | No additional patterns | Up to 10 external pattern resources. Each element contains `source`; see [Additional Resources And Fonts](#additional-resources-and-fonts). |
| `uxp` | `object` | Unless `actions` is nonempty | No script | One script resource containing `source`; see [Run A UXP Script](#run-a-uxp-script). |

## File Sources

For a file source, use one of these alternatives:

| Property | Type | Default | Description |
|---|---|---|---|
| `creativeCloudFileId` | `string` | None | Creative Cloud file ID beginning with `urn:aaid:`. |
| `creativeCloudPath` | `string` | None | Creative Cloud asset path. It can be accompanied by `creativeCloudProjectId` (`string`, beginning with `urn:aaid:`). |
| `url` | `string` | None | Readable URL to the file. |

For example, this is a fragment of an `image` object:

```json
{
  "source": {
    "creativeCloudPath": "<CREATIVE_CLOUD_PATH>",
    "creativeCloudProjectId": "<CREATIVE_CLOUD_PROJECT_URN>"
  }
}
```

Or use a file ID:

```json
{ "source": { "creativeCloudFileId": "<CREATIVE_CLOUD_FILE_URN>" } }
```

An image source can also use `lightroomPath` (`string`), a partial Lightroom
asset path starting with `/v2/`, without a host or query string. The path can
contain letters, digits, `.`, `_`, `-`, and `/`; it cannot contain `..`,
percent-encoding, or a fragment. This is not a source for additional contents,
brushes, fonts, or patterns. Use a URL or Creative Cloud source for those
resources and for action and script files.

```json
{
  "source": {
    "lightroomPath": "/v2/catalogs/<CATALOG_ID>/assets/<ASSET_ID>/revisions/<REVISION_ID>/proxies/<PROXY_ID>"
  }
}
```

## Action Sources

Each `actions` element has these properties:

| Property | Type | Required | Default | Description |
|---|---|---|---|---|
| `actionName` | `string` | No | None | Name of a specific action in an action set. |
| `source` | `object` | Yes | None | Inline ActionJSON or an external action file. |

An inline `source` has `content` (`string`, required; maximum 51,200 UTF-16
code units) and `contentType` (`string`, optional). Use `application/json` for
ActionJSON. Its `content` string must decode to an array of action descriptors.

An external `source` can use `url` (`string`) for a readable URL. The file
itself contains the action: a `.json` file contains ActionJSON, while an `.atn`
file is a recorded binary action set. Do not put binary `.atn` data into
inline `content`. To use multiple actions, list them in the order you want in
`actions`.

These are fragments of `options`, not complete requests:

```json
{
  "actions": [
    { "source": { "url": "<SIGNED_GET_URL_FOR_ACTION_JSON>" } }
  ]
}
```

```json
{
  "actions": [
    {
      "actionName": "<ACTION_NAME>",
      "source": { "url": "<SIGNED_GET_URL_FOR_ACTION_SET>" }
    }
  ]
}
```

The second URL identifies an `.atn` file. Supply the actual action name from
your set. If `actionName` is omitted, all actions in the set run in order.
The file representations are different even though both use a URL.

## Run A UXP Script

`uxp` contains a required `source` object. For an inline script, `source`
contains `content` (`string`, required; maximum 51,200 UTF-16 code units) and
`contentType` (`string`, optional). Use `application/javascript` for the
script. For an external script, use `source.url` (`string`) with a readable
URL to a JavaScript file. See [Supported Modules](../../getting-started/uxp/index.md#supported-modules-execute-actions-sandbox)
for available modules and file access.

This complete request writes document dimensions to a JSON file and asks for
that file as a hosted output:

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "options": {
    "uxp": {
      "source": {
        "content": "const fs = require('fs'); const doc = require('photoshop').app.activeDocument; fs.writeFileSync('plugin-temp:/document-metadata.json', JSON.stringify({ width: doc.width, height: doc.height }), 'utf8');",
        "contentType": "application/javascript"
      }
    }
  },
  "outputs": [
    {
      "destination": { "validityPeriod": 3600 },
      "mediaType": "application/json",
      "scriptOutputPattern": "document-metadata.json"
    }
  ]
}
```

The script reads the already-open input through `app.activeDocument`. It
writes a JSON object with numeric `width` and `height` properties to
`plugin-temp:/document-metadata.json`; the output definition selects that
file by its filename, `document-metadata.json`. See
[Find The Results](#find-the-results) for the returned output.

To supply the script from a file instead, replace `uxp.source` with this
fragment:

```json
{ "url": "<SIGNED_GET_URL_FOR_SCRIPT_JS>" }
```

A script that edits the document can request a rendered image output without
`scriptOutputPattern`. Use a pattern when requesting a file created by the
script.

## Additional Contents

Use `additionalContents` for external files needed by inline or file-based
ActionJSON or by a UXP script. These can include images, JSON, or plain-text
files. Each array element is an object containing a required `source` object.
For a signed URL, `source` contains a required `url` string. Even a text or
JSON additional content must use a file source; it cannot be supplied as
inline `content`.

The first element is referenced by `__ADDITIONAL_CONTENTS_PATH_0__`, the second
by `__ADDITIONAL_CONTENTS_PATH_1__`, and so on. The index is zero-based and
refers only to `additionalContents`: the main `image.source` is not an
element of that array. Include both leading and trailing double underscores.
The placeholder represents a file path, not the contents of the file. Use
the placeholder rather than constructing or hard-coding the resolved path.

### Place An Additional Image With ActionJSON

This request opens a base image, places an additional image, and returns a
PNG. The first additional file is referenced by index `0` in the action.

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "options": {
    "actions": [
      {
        "source": {
          "content": "[{\"ID\":3,\"_obj\":\"placeEvent\",\"freeTransformCenterState\":{\"_enum\":\"quadCenterState\",\"_value\":\"QCSAverage\"},\"null\":{\"_kind\":\"local\",\"_path\":\"__ADDITIONAL_CONTENTS_PATH_0__\"},\"offset\":{\"_obj\":\"offset\",\"horizontal\":{\"_unit\":\"pixelsUnit\",\"_value\":0},\"vertical\":{\"_unit\":\"pixelsUnit\",\"_value\":0}}}]",
          "contentType": "application/json"
        }
      }
    ],
    "additionalContents": [
      { "source": { "url": "<SIGNED_GET_URL_FOR_ADDITIONAL_IMAGE>" } }
    ]
  },
  "outputs": [
    { "destination": { "validityPeriod": 3600 }, "mediaType": "image/png" }
  ]
}
```

The string in `options.actions[0].source.content` represents this ActionJSON
array:

```json
[
  {
    "ID": 3,
    "_obj": "placeEvent",
    "null": { "_kind": "local", "_path": "__ADDITIONAL_CONTENTS_PATH_0__" },
    "freeTransformCenterState": { "_enum": "quadCenterState", "_value": "QCSAverage" },
    "offset": {
      "_obj": "offset",
      "horizontal": { "_unit": "pixelsUnit", "_value": 0 },
      "vertical": { "_unit": "pixelsUnit", "_value": 0 }
    }
  }
]
```

Each array element is an action descriptor with `ID` (`number`, `3` here) and
`_obj` (`string`, `placeEvent`). `null` (`object`) identifies the file with
`_kind` (`string`, `local`) and `_path` (`string`, the indexed placeholder).
`freeTransformCenterState` is an object whose `_enum` (`string`) and `_value`
(`string`) specify the placement's transform-center setting. `offset` is an
object with `_obj` (`string`, `offset`) and `horizontal` and `vertical`
objects; each contains `_unit` (`string`, `pixelsUnit`) and `_value` (`number`,
`0` here).

The placeholder convention applies to ActionJSON and UXP script content; do not
assume that a placeholder embedded in a binary `.atn` file will be replaced.

### Read Additional Content In A UXP Script

This request reads a JSON settings file and a text file, then returns their
contents in a hosted JSON report. The files are the first and second entries
in `additionalContents`; the input image is separate. The script is included
in the request as a JSON string. For clarity, the unescaped script is:

```javascript
const fs = require("fs");
const settingsData = fs.readFileSync("__ADDITIONAL_CONTENTS_PATH_0__");
const textData = fs.readFileSync("__ADDITIONAL_CONTENTS_PATH_1__");
function ascii(value) {
  if (typeof value === "string") return value;
  const bytes = typeof value.length === "number" ? value : new Uint8Array(value);
  let result = "";
  for (let i = 0; i < bytes.length; i++) result += String.fromCharCode(bytes[i]);
  return result;
}
const report = { data: JSON.parse(ascii(settingsData)), text: ascii(textData) };
fs.writeFileSync("plugin-temp:/resource-report.json", JSON.stringify(report), "utf8");
```

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "options": {
    "additionalContents": [
      { "source": { "url": "<SIGNED_GET_URL_FOR_SETTINGS_JSON>" } },
      { "source": { "url": "<SIGNED_GET_URL_FOR_NOTES_TEXT>" } }
    ],
    "uxp": {
      "source": {
        "content": "const fs = require(\"fs\");\nconst settingsData = fs.readFileSync(\"__ADDITIONAL_CONTENTS_PATH_0__\");\nconst textData = fs.readFileSync(\"__ADDITIONAL_CONTENTS_PATH_1__\");\nfunction ascii(value) {\n  if (typeof value === \"string\") return value;\n  const bytes = typeof value.length === \"number\" ? value : new Uint8Array(value);\n  let result = \"\";\n  for (let i = 0; i < bytes.length; i++) result += String.fromCharCode(bytes[i]);\n  return result;\n}\nconst report = { data: JSON.parse(ascii(settingsData)), text: ascii(textData) };\nfs.writeFileSync(\"plugin-temp:/resource-report.json\", JSON.stringify(report), \"utf8\");",
        "contentType": "application/javascript"
      }
    }
  },
  "outputs": [
    {
      "destination": { "validityPeriod": 3600 },
      "mediaType": "application/json",
      "scriptOutputPattern": "resource-report.json"
    }
  ]
}
```

For example, if the settings file contains:

```json
{ "title": "Summer Collection", "version": 1, "enabled": true }
```

and the text file contains these two lines, each ending with a newline:

```text
Opens Saturday
Ends Sunday
```

the downloaded report contains:

```json
{
  "data": { "title": "Summer Collection", "version": 1, "enabled": true },
  "text": "Opens Saturday\nEnds Sunday\n"
}
```

This example's `ascii` helper is for ASCII input. For other encodings, use an
appropriate decoder supported by your script. See the
[UXP module reference](../../getting-started/uxp/index.md#supported-modules-execute-actions-sandbox)
for file-access details.

## Additional Resources And Fonts

Each `brushes` or `patterns` element is an object containing a required
external `source`. A URL source contains `url` (`string`). `fontOptions`
supports these optional properties:

| Property | Type | Default | Description |
|---|---|---|---|
| `additionalFonts` | `array<object>` | No additional fonts | Font resources. Each element contains `source` (`object`) with a readable font URL in `url` (`string`). |
| `defaultFontPostScriptName` | `string` | No override | PostScript name of the document's default font. |
| `missingFontStrategy` | `string` | `use_default` | `fail` stops the job if fonts remain missing; `use_default` continues with font substitution. |

This is an `options` fragment; add an action or script and the other required
request fields before submitting it:

```json
{
  "brushes": [ { "source": { "url": "<SIGNED_GET_URL_FOR_BRUSH>" } } ],
  "fontOptions": {
    "additionalFonts": [ { "source": { "url": "<SIGNED_GET_URL_FOR_FONT>" } } ],
    "defaultFontPostScriptName": "<FONT_POSTSCRIPT_NAME>",
    "missingFontStrategy": "fail"
  },
  "patterns": [ { "source": { "url": "<SIGNED_GET_URL_FOR_PATTERN>" } } ]
}
```

## Output Files

Each `outputs` element contains a required `destination` (`object`). Set
`mediaType` (`string`) explicitly: use `image/png` for a PNG image or
`application/json` for the JSON script output above. Other output formats and
export fields are listed in the [API Reference](../../api/photoshop-v2/index.md).

| Property | Type | Required | Default | Description |
|---|---|---|---|---|
| `destination` | `object` | Yes | None | One of the destination types below. |
| `mediaType` | `string` | No | `image/jpeg` | Output format. Set explicitly to make the requested format clear. |
| `scriptOutputPattern` | `string` | No | Render the document | Select files written by a script instead of exporting the document. See [Capture Files Written By A UXP Script](#capture-files-written-by-a-uxp-script). |

For compression, resizing, and profile defaults, see the
[API reference](../../api/photoshop-v2/index.md).

| Destination | Fields | Use |
|---|---|---|
| Creative Cloud | `creativeCloudPath` (`string`, required), `creativeCloudProjectId` (`string`, optional, beginning with `urn:aaid:`) | Write to a Creative Cloud path. |
| Embedded | `embedded` (`string`: `base64`, `json`, or `string`) | Return the content in the status response. |
| Hosted | `validityPeriod` (`integer`, seconds; 60–86400) | Receive a time-limited URL; use `3600` for one hour. |
| Your storage | `url` (`string`, required), `storageType` (`string`, required for Azure or Dropbox: `azure` or `dropbox`) | Write to a signed URL. |

### Capture Files Written By A UXP Script

Write each file to the root of `plugin-temp:/`, for example
`plugin-temp:/document-metadata.json`. In the corresponding output element,
set `scriptOutputPattern` to the **filename**, `document-metadata.json`, not
the `plugin-temp:/` path. Matching considers files at the root, not files in
subdirectories.

`scriptOutputPattern` is an optional `string` of at most 255 characters. It
can be an exact filename or a glob such as `report-*.json`. Use a hosted or
embedded destination for a pattern, not a URL or Creative Cloud destination.
Pattern matching is case-insensitive. The `mediaType` filters matching files
by extension: for example,
`application/json` selects `.json`, `image/png` selects `.png`, and
`image/jpeg` selects `.jpg` or `.jpeg`. Each matching file becomes an output
entry; a pattern with no matching file fails the job.

For example, a script can write two JSON files:

```javascript
const fs = require("fs");
fs.writeFileSync("plugin-temp:/report-1.json", JSON.stringify({ page: 1 }), "utf8");
fs.writeFileSync("plugin-temp:/report-2.json", JSON.stringify({ page: 2 }), "utf8");
```

Each file contains an object with a numeric `page` property. This complete
request returns both files as hosted outputs and also embeds the first file:

```json
{
  "image": { "source": { "url": "<SIGNED_GET_URL_FOR_IMAGE>" } },
  "options": {
    "uxp": {
      "source": {
        "content": "const fs = require(\"fs\");\nfs.writeFileSync(\"plugin-temp:/report-1.json\", JSON.stringify({ page: 1 }), \"utf8\");\nfs.writeFileSync(\"plugin-temp:/report-2.json\", JSON.stringify({ page: 2 }), \"utf8\");",
        "contentType": "application/javascript"
      }
    }
  },
  "outputs": [
    {
      "destination": { "validityPeriod": 3600 },
      "mediaType": "application/json",
      "scriptOutputPattern": "report-*.json"
    },
    {
      "destination": { "embedded": "json" },
      "mediaType": "application/json",
      "scriptOutputPattern": "report-1.json"
    }
  ]
}
```

A successful status response includes three output entries, for example:

```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      { "mediaType": "application/json", "destination": { "url": "<HOSTED_REPORT_1_URL>" } },
      { "mediaType": "application/json", "destination": { "url": "<HOSTED_REPORT_2_URL>" } },
      { "mediaType": "application/json", "destination": { "embedded": "json", "content": { "page": 1 } } }
    ]
  }
}
```

Each match produces a separate `outputs` entry. Include an identifier in the
file contents if you need to distinguish the files; do not depend on their
order. The files are returned as written by the script: rendering options such
as `width`, `height`, `quality`, and `compression` do not modify a
pattern-selected file. To request a rendered image instead, omit the pattern
and choose an image `mediaType` such as `image/png`. Avoid path traversal such
as `..` and control characters; pattern complexity is also limited.

### Find The Results

For the hosted `document-metadata.json` example above, a successful status
response includes an output like this excerpt:

```json
{
  "status": "succeeded",
  "result": {
    "outputs": [
      {
        "mediaType": "application/json",
        "destination": { "url": "<HOSTED_JSON_OUTPUT_URL>" }
      }
    ]
  }
}
```

`result` is an object, `outputs` is an array of output objects, and
`destination.url` is the string URL for the generated file. Download that URL
to read the JSON. For a 128-by-128 input, the file has this form:

```json
{ "width": 128, "height": 128 }
```

To return that JSON in the status response instead, replace the output
definition in the script request with this fragment:

```json
{
  "outputs": [
    {
      "destination": { "embedded": "json" },
      "mediaType": "application/json",
      "scriptOutputPattern": "document-metadata.json"
    }
  ]
}
```

For an embedded JSON destination, the corresponding output contains
`destination.embedded` (`string`, `json`) and `destination.content` (the
parsed JSON value), for example:

```json
{
  "result": {
    "outputs": [
      {
        "mediaType": "application/json",
        "destination": {
          "embedded": "json",
          "content": { "width": 128, "height": 128 }
        }
      }
    ]
  }
}
```

For a successful job, `result.outputs` is an array of output objects. Each
output has `mediaType` (`string`) and `destination` (`object`). A hosted
destination provides a `url` (`string`); an embedded destination provides
`content` (a JSON value for `json`, or a string for `base64` and `string`).
For a URL destination, use the read URL supplied by your storage provider.

For a failed job, `errorDetails` is an array of objects that can include
`errorCode` and `message` (both strings). See [Get Job Status](../get-job-status/index.md)
for polling and status fields.

## Troubleshooting

| Symptom | Cause And Fix |
|---|---|
| A file placeholder is not replaced | Include the file in `additionalContents` and check its zero-based index in the placeholder. |
| Cannot read an input or output | Check that each signed URL grants the appropriate read or write access and remains valid for the job. |
| Inline action is not accepted as ActionJSON | Encode the descriptor array as the `content` string, rather than putting an array directly in `content`. |
| Job fails after HTTP `202` | Poll `statusUrl` and inspect `errorDetails`; acceptance is not processing success. |
| Request is rejected | Check that `image.source`, a nonempty `actions` array or `uxp`, and at least one output are present. |
| Script output is missing | Write the file directly under `plugin-temp:/`, use its filename in `scriptOutputPattern`, set the matching `mediaType`, and use a hosted or embedded destination. |

## Next Steps

- [ActionJSON Structure](../../getting-started/actions/index.md#actionjson-structure): learn more about action descriptors.
- [API Reference](../../api/photoshop-v2/index.md): review output schemas.
- [Get Job Status](../get-job-status/index.md): poll the job and inspect results or errors.
- [Smart Filters With Execute Actions](../workflows/smart_filters/index.md): apply filters to Smart Objects.
