---
title: Technical usage notes
description: Learn about current limitations, rate limits, and best practices for implementing the Photoshop API.
hideBreadcrumbNav: true
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
  - https://github.com/AEAbreu-hub
keywords:
  - limitations
  - rate limits
  - retries
  - compatibility
  - webhooks
  - events
---

# Technical Usage Notes

This document has details about what's currently supported, limitations, and workarounds
 for the Photoshop API to help optimize your API implementations and understand service boundaries.

## Known limitations

These are known limitations to the Photoshop APIs:

- Multi-part uploads and downloads aren't yet supported.
- All endpoints only support a single file input.
- Error handling is a work in progress; you may not always see the most helpful error messages. Apologies.

## Compatibility with Photoshop versions

- The APIs will open any PSD created with Photoshop 1.0 or later.
- When the API saves files as PSD, it will create PSDs compatible with the current version of Photoshop.
- Regarding "maximize compatibility" referenced in the [Photoshop file formats documentation][1], the APIs default to "yes".
  
## About retries

For increased reliability and stability, there's a retry mechanism for all API calls:

- The service will retry status codes of `429`, `502`, `503`, `504` three times.
- You should only retry requests that have a 5xx response code. This indicates a problem processing the request on the server. You shouldn't retry requests for any other response code.
- Implement an exponential back-off retry strategy with three retry attempts.

## Rate limits

To ensure equitable peak performance with Firefly APIs, Adobe places limits on the volume, frequency, and concurrency of API calls, and monitors API usage to proactively contact you and resolve any risks.

You may encounter an HTTP 429 "Too Many Requests" error if usage exceeds these limit. Use the 'retry-after' header to determine the number of seconds to wait before trying again.

<InlineAlert variant="info" slots="text1" />

Usage limits apply to **your entire organization**.

These are the API usage limits:

### General service limits

**Hard limit**

- POST: 16 requests/3 secs or 320 requests/minute.
- GET: 310 requests/3 secs.

**Soft limit**

- POST: 15 requests/3 secs or 300 requests/minute.
- GET: 300 requests/3 secs.

### Remove background service limits

**Hard limit**

- POST: 6 requests/3 secs.
- GET: 1000 requests/3 secs.

**Soft limit**

- POST: 2 requests/3 secs.
- GET: 500 requests/3 secs.

### Masking service limits

- 60 requests/min.
- 9000 requests/day.

<!-- Links -->
[1]: https://helpx.adobe.com/photoshop/using/file-formats.html#maximize_compatibility_for_psd_and_psb_files
[2]: /guides/code_sample/index.md#generate-remove-background-result-as-photoshop-path
