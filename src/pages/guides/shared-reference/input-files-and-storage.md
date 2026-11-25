---
title: Input Files And Storage
description: Specify input files for Photoshop V2 requests with signed URLs or Creative Cloud storage.
keywords:
  - input files
  - source
  - signed URL
  - presigned URL
  - Creative Cloud
  - storage
hideBreadcrumbNav: true
---

# Input Files And Storage

Each input file in a Photoshop V2 request is described by a `source` object.
The service reads the file while processing the job, not when it accepts the
request. Keep each input readable until the job reaches a final status.

## Specify A Source

Use one of these `source` objects. Include the fields of only one type.

| Source Type | Use When |
|---|---|
| [Creative Cloud File ID Source](#creative-cloud-file-id-source) | The file is in Creative Cloud storage and you know its asset ID. |
| [Creative Cloud Path Source](#creative-cloud-path-source) | The file is in Creative Cloud storage and you know its path. |
| [Lightroom Path Source](#lightroom-path-source) | The image is in Lightroom and you have its partial `/v2/` path. |
| [URL Source](#url-source) | The file is in your own storage and you can create a signed HTTPS URL for it. |

For Creative Cloud sources, the access token must belong to an account that
can read the file.

### Creative Cloud File ID Source

```json
{ "source": { "creativeCloudFileId": "<CREATIVE_CLOUD_FILE_ID>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `creativeCloudFileId` | string | Yes | None | Asset ID of the file. Starts with `urn:aaid:` (case-insensitive). |

### Creative Cloud Path Source

```json
{ "source": { "creativeCloudPath": "<CREATIVE_CLOUD_PATH>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `creativeCloudPath` | string | Yes | None | Path of the file in Creative Cloud storage. Must not be blank. |
| `creativeCloudProjectId` | string | No | None | Project that contains the path. Starts with `urn:aaid:` (case-insensitive). |

### Lightroom Path Source

For image inputs, these endpoints accept an asset's partial Lightroom path:
Create Artboard, Create Composite, Edit, Execute Actions, and Generate Manifest.
The host is supplied by the service; provide only the path.

```json
{ "source": { "lightroomPath": "/v2/catalogs/<CATALOG_ID>/assets/<ASSET_ID>/revisions/<REVISION_ID>/proxies/<PROXY_ID>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `lightroomPath` | string | Yes | None | Partial path beginning with `/v2/`. Use letters, digits, `.`, `_`, `-`, and `/`; do not include a host, query, fragment, percent-encoding, or `..` path segment. |

### URL Source

```json
{ "source": { "url": "<SIGNED_GET_URL>" } }
```

| Field | Type | Required | Default | Meaning and Constraints |
|---|---|---|---|---|
| `url` | string | Yes | None | HTTPS URL that returns the file. See [URL Requirements](#url-requirements). |

### Inline Action And Script Content

Execute Actions also accepts action and script content inside the request
instead of a file. See [Execute Actions][execute-actions].

## URL Requirements

A `url` in a `source` object must:

1. Use `https`.
2. Use the default HTTPS port (443) or no port.
3. Use a host name; IP addresses and `localhost` are rejected.
4. Return the file to a `GET` request without extra headers or cookies.
5. Stay valid until the job finishes. Allow for queueing and processing time
   when you choose an expiry.

Redirects to another HTTPS URL are followed. A URL that breaks rules 1–3 is
rejected when you submit the request (HTTP 422). Other access problems fail the
job; see [Troubleshoot Input Access](#troubleshoot-input-access).

## Where Sources Are Used

| Input | Endpoints | Accepted Source Types |
|---|---|---|
| Action and script files | Execute Actions | Creative Cloud file ID, Creative Cloud path, URL, inline content |
| Additional files, brushes, and patterns | Execute Actions | Creative Cloud file ID, Creative Cloud path, URL |
| Custom ICC profiles | Create Artboard, Create Composite, Execute Actions | Creative Cloud file ID, Creative Cloud path, URL |
| Document and image inputs | Create Artboard, Create Composite, Edit, Execute Actions, Generate Manifest | Creative Cloud file ID, Creative Cloud path, Lightroom path, URL |
| Fonts | Create Composite, Execute Actions | Creative Cloud file ID, Creative Cloud path, URL |
| Layer images, masks, and smart-object files | Create Composite | Creative Cloud file ID, Creative Cloud path, URL |
| XMP settings files | Edit | Creative Cloud file ID, Creative Cloud path, URL |

Field names and limits are in each endpoint guide and the
[API Reference][api-reference].

## Supported Input File Types

The service checks each file's type while processing the job. A file of an
unsupported type fails the job.

| Input | Supported File Types |
|---|---|
| Action files (Execute Actions) | ActionJSON (`.json`), Photoshop action (`.atn`) |
| Additional files (Execute Actions) | Execute Actions images, JSON, plain text |
| Brushes (Execute Actions) | Photoshop brush files (`.abr`) |
| Patterns (Execute Actions) | Photoshop pattern files (`.pat`) |
| Custom ICC profiles | ICC profile (`.icc`, `.icm`) |
| Execute Actions images | Photoshop images, BMP, GIF |
| Fonts | OpenType (`.otf`), TrueType (`.ttf`) |
| Photoshop images (Create Artboard, Create Composite, Generate Manifest) | Camera raw, JPEG, PNG, PSD, TIFF |
| UXP script files (Execute Actions) | JavaScript (`.js`, `.jsx`) |
| Smart-object files (Create Composite) | Photoshop images, AI, PDF, SVG |

For Edit inputs, see the [API Reference][api-reference].

## Create Signed URLs

Create signed URLs with your storage provider's tools. Grant read access for
inputs and write access for outputs. Choose an expiry that covers queueing and
processing time.

| Storage | Input (Read) | Output (Write) |
|---|---|---|
| Amazon S3 | Presigned `GET` URL, for example from `aws s3 presign s3://<BUCKET>/<KEY> --expires-in 3600` | Presigned `PUT` URL from an AWS SDK |
| Azure Blob Storage | Blob URL with a SAS token that grants read (`r`) | Blob URL with a SAS token that grants create and write (`cw`) |
| Dropbox | Temporary link from the Dropbox `files/get_temporary_link` API | Temporary upload link from the Dropbox `files/get_temporary_upload_link` API |

Inputs need no storage type. For Azure and Dropbox outputs, set `storageType`;
see [URL Destination][outputs-url-destination].

Signed URLs grant access to anyone who has them. Keep them out of logs and
source control.

## Troubleshoot Input Access

| Symptom | Likely Cause | Fix |
|---|---|---|
| HTTP 422 for a Creative Cloud field | `creativeCloudFileId` or `creativeCloudProjectId` doesn't start with `urn:aaid:`. | Use the asset or project URN. |
| HTTP 422 for `url` | The URL isn't HTTPS, uses a custom port, or uses an IP address or `localhost`. | Use an HTTPS URL with a host name and the default port. |
| Job fails reading an input | The URL expired, lacks read access, or points to a missing file. | Create a new signed URL with read access and a longer expiry. |
| Job fails with an unsupported file type | The file type isn't accepted for that input. | Use a type listed in [Supported Input File Types](#supported-input-file-types). |

Check job failures with [Get Job Status][job-status].

[//]: # (Links)
[api-reference]: ../../api/photoshop-v2/index.md
[execute-actions]: ../execute-actions/index.md
[job-status]: ../get-job-status/index.md
[outputs-url-destination]: output-formats-and-options.md#url-destination
