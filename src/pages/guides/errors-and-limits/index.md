---
title: Errors and Limits
description: Error responses, job error codes, and request limits for the Photoshop API V2
keywords:
  - errors
  - error codes
  - validation
  - limits
  - retry
hideBreadcrumbNav: true
---

# Errors and Limits

Photoshop API V2 reports errors in two places:

- **Request errors** return immediately with an HTTP error status. No job is created.
- **Job errors** appear later in the [job status response](../get-job-status/index.md#job-status-response)
  as `status: failed` with `errorDetails`.

## Error Response Body

Request errors return a JSON body with one of two shapes. A request to a path
that does not exist is the exception; see [HTTP Errors](#http-errors).

A single error:

```json
{
  "error_code": "invalid_request",
  "message": "Request payload contains invalid fields: type, text"
}
```

A single error for an unsupported `Content-Type`:

```json
{
  "error_code": "invalid_content_type",
  "message": "The Content-Type 'text/plain' is not supported for this endpoint. Supported media types: [application/json]"
}
```

Several validation errors at once:

```json
{
  "errors": [
    {
      "error_code": "validation_error",
      "message": "outputs is required"
    },
    {
      "error_code": "validation_error",
      "message": "image field is required"
    }
  ]
}
```

| JSON Path | Type | Presence | Meaning |
|---|---|---|---|
| `error_code` | string | Single-error body only | Machine-readable code. See [HTTP Errors](#http-errors). |
| `message` | string | Single-error body only | Human-readable explanation. |
| `errors` | `array<object>` | Multiple-error body only | All validation errors found. Order is not guaranteed. |
| `errors[]` | object | One per error | A validation error with `error_code` and `message`. |
| `errors[].error_code` | string | Always, in each entry | Always `validation_error`. |
| `errors[].message` | string | Always, in each entry | Explanation of one validation error. See [Validation Messages](#validation-messages). |

When `errors` is present, the top-level `error_code` and `message` are omitted.
Check for both shapes.

## HTTP Errors

| HTTP Status | `error_code` | Cause | Fix |
|---|---|---|---|
| `400` | `invalid_json` | The body is not valid JSON. | Send well-formed JSON. |
| `400` | `invalid_request` | The body contains fields the endpoint does not accept. The message lists their paths. | Remove or rename the listed fields. |
| `401` | `ims_service_token_error` | The access token is missing, invalid, or lacks a required scope. | Request a new token with the required scopes. |
| `403` | `unauthorized_forbidden` | The credentials are not allowed to call the API, for example because the quota is used up or the account is not entitled. | Check the account's entitlement and quota. If the message reports high traffic, retry after a short wait. |
| `404` | `unknown_job_id` | The job does not exist or belongs to different credentials. | Check the `jobId` and use the credentials that submitted the job. |
| `404` | None | The path does not exist. The body may not be JSON. | Check the endpoint path. |
| `405` | `unsupported_method` | The endpoint does not support the HTTP method. The message lists supported methods. | Use the listed method. |
| `415` | `invalid_content_type` | The `Content-Type` is not supported. | Send `Content-Type: application/json`. |
| `422` | `validation_error` | A field value is missing, has the wrong type, or is out of range. | Fix the field named in the message. See [Validation Messages](#validation-messages). |
| `429` | `unauthorized_rate_limited` | Too many requests. | Wait for `Retry-After` seconds when present, then retry. |
| `451` | `unauthorized_legal_reasons` | The request is blocked for the caller's region. | Contact Adobe support. |
| `500` | `runtime_error` | An unexpected error occurred. | Retry with backoff. If it persists, contact Adobe support. |
| `503` | `service_unavailable` | The service is temporarily overloaded. | Honor `Retry-After` when present; otherwise retry with increasing delays from 2 to 30 seconds. |

Validation runs before the unknown-field check, so a request with both problems
returns `422` first. Fix it and resubmit to see any `400` for unknown fields.

## Validation Messages

`422` messages name the failing field with a JSON path such as
`edits.layers[0].operation.type`. Array indexes start at `0`.

| Format | Example |
|---|---|
| `<path>: <rule>` | `edits.layers[0].operation.placement: must not be null` |
| `<path>: <rule>` | `edits.layers[0].text.characterStyles[0].characterStyle.fontAlpha: Font alpha must be at most 1.0` |
| `Invalid value '<value>' at path '<path>'. Accepted values are: <values>` | `Invalid value 'Add' at path 'edits.layers[0].operation.type'. Accepted values are: add, edit, delete, move` |
| `Missing required field '<field>' ... at path '<path>'` | `Missing required field 'type' for edit operation at path 'edits.layers[0]'` |
| `<field> is required` | `outputs is required` |

Enumerated values are case-sensitive; `Add` is rejected where `add` is accepted.

## Job Errors

A job that fails after acceptance reports one or more `errorDetails[]` entries.
Each entry has an `errorCode` string and a `message` string. Codes are
case-sensitive and use mixed case. Handle an unlisted code as a generic
failure and show its `message`.

| `errorCode` | Meaning | Fix |
|---|---|---|
| `download_error` | An input could not be read from its URL or storage location. | Check that the URL is valid, unexpired, and readable, then submit a new job. |
| `forbidden_action` | The action input contains steps that are not allowed. | Remove the disallowed steps. |
| `invalid_file_type` | The input file type could not be determined. | Send a supported, uncorrupted file. |
| `invalid_parameters` | A parameter is invalid for the document being processed. The message names it. | Fix the parameter. For example, `above`, `below`, and `into` placements need a reference layer `id` or `name`. |
| `JOB_TIMEOUT` | The job did not finish within the allowed time. | Simplify the request or split it into smaller jobs, then submit again. |
| `missing_fonts` | A requested font is not available and the missing-font strategy is `fail`. | Supply the font, correct its PostScript name, or set `fontOptions.missingFontStrategy` to `use_default`. |
| `unknown_error` | An unexpected processing error occurred. | Submit a new job. If it persists, contact Adobe support with the `jobId`. |
| `unsupported_file_type` | An action file is not `.atn` or `.json`. | Supply an `.atn` or `.json` action file. |
| `unsupported_mimetype` | An input's media type is not supported for its role. | Send a supported format for that input. |
| `upload_error` | An output could not be written to its destination. | Check that the destination URL is valid, unexpired, and writable, then submit a new job. |
| `url_not_allowed` | An input or output URL is not allowed. | Use a publicly reachable `https` URL with no credentials in it. |

Example:

```json
{
  "errorCode": "invalid_parameters",
  "message": "create text layer: Reference layer ID or name is required for ABOVE, BELOW, INTO Placement types"
}
```

## Limits

Requests that exceed these limits return `422 validation_error`.

| Limit | Applies To | Value |
|---|---|---|
| Action files per request | `options.actions` in Execute Actions | At most 10 |
| Additional content files per request | `options.additionalContents` in Execute Actions | At most 25 |
| Artboard name length | Create Artboard | 1–255 characters |
| Brush files per request | `options.brushes` in Execute Actions | At most 10 |
| Canvas width and height | `image.width`, `image.height` on a new canvas | 1–32,000 in the configured `image.unit`; pixels by default, or points with `points_unit` |
| Hosted output link lifetime | `outputs[].destination.validityPeriod` | 60–86,400 seconds; default 3,600 |
| Images per artboard request | `images` in Create Artboard | 1–25 |
| Inline content length | Inline action `content` | At most 51,200 characters |
| Layers per Photoshop output | `outputs[].layers` | At most 100 |
| Outputs per request | `outputs` on every `POST` endpoint | 1–25 |
| Pattern files per request | `options.patterns` in Execute Actions | At most 10 |

Jobs that run too long fail with `JOB_TIMEOUT`.

## Retry Guidance

| Situation | Retry? |
|---|---|
| `400`, `401`, `403` (other than high traffic), `404`, `405`, `415`, `422`, `451` | No. Fix the request or credentials first. |
| `429`, `503` | Yes, after `Retry-After` when present; otherwise with increasing delays from 2 to 30 seconds. |
| `500` | Yes, with increasing delays. |
| Job `failed` | Submit a new job only after addressing `errorDetails`. |

Submitting again creates a new job with a new `jobId`.

## Related

- [Get Job Status](../get-job-status/index.md)
- [API reference](../../api/photoshop-v2/index.md)
