---
title: Get Job Status
description: Poll a Photoshop API V2 job and read its status, outputs, and errors
keywords:
  - job status
  - polling
  - asynchronous jobs
  - API status
  - job monitoring
hideBreadcrumbNav: true
contributors:
  - https://github.com/AEAbreu-hub
---

# Get Job Status

Every Photoshop API V2 `POST` endpoint runs asynchronously. It accepts the
request, returns a job ID, and processes the job later. Poll
`GET /v2/status/{jobId}` until the job succeeds or fails.

## Submit a Job

These endpoints return `202 Accepted` when they accept a request:

- `POST /v2/create-artboard`
- `POST /v2/create-composite`
- `POST /v2/edit`
- `POST /v2/execute-actions`
- `POST /v2/generate-manifest`

If the `202` response includes a `Retry-After` header, wait that many seconds
before the first poll. If it is absent, wait 2 seconds before the first poll.

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "statusUrl": "https://photoshop-api.adobe.io/v2/status/de2415fb-82c6-47fc-b102-04ad651c5ed4"
}
```

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `jobId` | string (UUID) | Always | Identifier for the accepted job. |
| `statusUrl` | string (URL) | Always | URL to poll for this job. It is not an output download URL. |

Acceptance means the request passed synchronous validation. It does not mean
processing succeeded. A request that fails synchronous validation returns an
error instead of a job; see [Errors and Limits](../errors-and-limits/index.md).

## Fetch the Status of a Job

Call the `statusUrl`, or call `/v2/status/<JOB_ID>` with the returned `jobId`.
Use the same credentials that submitted the job.

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/<JOB_ID> \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "x-api-key: <API_KEY>"
```

A successful lookup returns `200 OK` with a [job status response](#job-status-response).

## Poll for Completion

1. Honor `Retry-After` when the `202` response includes it; otherwise wait 2 seconds.
2. Poll while `status` is `not_started` or `running`.
3. Increase the interval between polls up to 30 seconds; do not poll in a tight loop.
4. Stop on `succeeded` or `failed`. These states are final.
5. On `429` or `5xx`, honor `Retry-After` when present; otherwise retry with
   increasing delays from 2 to 30 seconds.
6. Set a client deadline. Reaching it does not mean the job failed; you can poll again later.

## Status Values

| Value | Final | Meaning | Next Action |
|---|---|---|---|
| `failed` | Yes | Processing stopped with an error. | Read `errorDetails`, fix the request, and submit a new job. |
| `not_started` | No | The job is accepted and waiting to start. | Keep polling. |
| `running` | No | The job is processing. | Keep polling. |
| `succeeded` | Yes | Processing finished. | Read `result.outputs`. |

Status moves forward only: `not_started` → `running` → `succeeded` or `failed`.
A fast job can reach a final state before you observe `running`. A final status
never changes.

## Job Status Response

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `jobId` | string (UUID) | Always | Identifier of this job, matching the acknowledgement. |
| `status` | string | Always | One of `not_started`, `running`, `succeeded`, or `failed`. See [Status Values](#status-values). |
| `createdTime` | string | Always | Time the job was created, as an ISO 8601 date-time with no timezone offset. |
| `modifiedTime` | string | Always | Time the job record last changed, in the same format as `createdTime`. It is not a completion estimate. |
| `result` | object | Read only when `status` is `succeeded` | Container for the job outputs. Omitted while the job is pending and when it fails. |
| `result.outputs` | `array<object>` | Present when `result` is present | One entry per produced output. |
| `result.outputs[]` | object | One per output | Endpoint-specific output object. See [Endpoint Outputs](#endpoint-outputs). |
| `errorDetails` | `array<object>` | Only when `status` is `failed`; can be omitted | One or more processing errors. |
| `errorDetails[]` | object | One per error | A processing error with `errorCode` and `message`. |
| `errorDetails[].errorCode` | string | Always, in each entry | Machine-readable code. Codes are case-sensitive. See [Job Errors](../errors-and-limits/index.md#job-errors). |
| `errorDetails[].message` | string | Always, in each entry | Human-readable explanation. Do not parse it. |

Null fields are omitted, never returned as `null`. A missing `result` while the
job is pending is not an empty successful result. A missing `errorDetails` on a
`failed` job means no detail is available; treat the job as failed. Timestamps
carry no timezone offset, and fractional-second precision varies, so do not
require a fixed number of digits. Ignore fields that this page and the endpoint
guides do not document, including fields whose names start with `_`.

### Pending Job

An illustrative job that is still processing:

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "status": "running",
  "createdTime": "2026-11-05T11:47:45.334192051",
  "modifiedTime": "2026-11-05T11:47:46.1093"
}
```

### Succeeded Job

This Create Composite job wrote two hosted outputs. Signed URLs are shortened.

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "status": "succeeded",
  "createdTime": "2026-11-05T11:47:45.334192051",
  "modifiedTime": "2026-11-05T11:47:48.66201325",
  "result": {
    "outputs": [
      {
        "destination": {
          "mediaType": "image/vnd.adobe.photoshop",
          "url": "https://<SIGNED_OUTPUT_URL>"
        },
        "mediaType": "image/vnd.adobe.photoshop"
      },
      {
        "destination": {
          "mediaType": "image/png",
          "url": "https://<SIGNED_OUTPUT_URL>"
        },
        "mediaType": "image/png"
      }
    ]
  }
}
```

### Failed Job

This Create Composite job requested a font that was not available and set
`fontOptions.missingFontStrategy` to `fail`.

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "status": "failed",
  "createdTime": "2026-11-05T11:57:28.083165777",
  "modifiedTime": "2026-11-05T11:57:28.728244506",
  "errorDetails": [
    {
      "errorCode": "missing_fonts",
      "message": "Missing fonts detected: AcmeBrandSans-Bold. Strategy: FAIL"
    }
  ]
}
```

## Endpoint Outputs

Each `result.outputs[]` entry has a `mediaType` string and a `destination`
object. The following shapes were observed in one successful request per
endpoint; each request asked for one output. Values are omitted.

| Endpoint | Observed output fields and types | Reference |
|---|---|---|
| `POST /v2/create-artboard` | `mediaType`: string; `destination.url`: string | [Create Artboard](../artboards/index.md) |
| `POST /v2/create-composite` | `mediaType`: string; `destination.url`: string | [API reference](../../api/photoshop-v2/index.md) |
| `POST /v2/edit` | `mediaType`: string; `destination.url`: string | [API reference](../../api/photoshop-v2/index.md) |
| `POST /v2/execute-actions` | `mediaType`: string; `destination.url`: string | [Execute Actions](../execute-actions/index.md) |
| `POST /v2/generate-manifest` | `mediaType`: string; `destination.content`: object | [Manifest response](../photoshop-v2/manifest-response-reference.md) |

For Generate Manifest, `destination.content` is the embedded manifest object
inside an output entry. It is not the status response's top-level `result`,
which contains the `result.outputs[]` array.

## Status Request Errors

| HTTP Status | `error_code` | Cause | Fix |
|---|---|---|---|
| `401` | `ims_service_token_error` | The access token is missing, invalid, or lacks a required scope. | Send a valid token. |
| `404` | `unknown_job_id` | The job does not exist or belongs to different credentials. | Check the `jobId` and use the credentials that submitted the job. |
| `429` | `unauthorized_rate_limited` | Too many requests. | Honor `Retry-After` when present; otherwise back off before polling again. |
| `500` | `runtime_error` | The status could not be read. | Poll again later. |

```json
{
  "error_code": "unknown_job_id",
  "message": "Job not found"
}
```

For every error code and the error body format, see
[Errors and Limits](../errors-and-limits/index.md).

An invalid job ID format returns `400`.

## Next Steps

- [Errors and Limits](../errors-and-limits/index.md)
- [API reference](../../api/photoshop-v2/index.md)
