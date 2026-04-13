---
title: Status Endpoint Migration (V1 to V2)
description: Migrate from separate v1 status endpoints to the unified /v2/status endpoint
hideBreadcrumbNav: true
keywords:
  - status
  - job status
  - polling
  - migration
  - v1 to v2
---

# Status Endpoint Migration (V1 to V2)

This guide helps you migrate from v1 status checking endpoints to the unified `/v2/status/{jobId}` endpoint.

## Overview

In v1, different services had their own status endpoints. V2 consolidates all job status checking into a single endpoint regardless of the operation type.

**V1 Endpoints:**

- `/lrService/status/{jobId}` - For Lightroom operations
- `/pie/psdService/status/{jobId}` - For Photoshop operations

**V2 Endpoint:**

- `/v2/status/{jobId}` - For all operations

## Benefits of the unified endpoint

- **Single Integration Point:** One endpoint for all job types
- **Consistent Response Format:** Same structure for all operations
- **Simplified Code:** No need to track which service initiated the job
- **Better Error Details:** Enhanced error reporting structure

## Basic migration example

**Key differences**

**Base URL:**

- V1: `https://image.adobe.io` → V2: `https://photoshop-api.adobe.io`

**Endpoint:**

- V1: Service-specific paths → V2: Unified `/v2/status/{jobId}`

**Response Structure:**

- V1: Different structures per service → V2: Consistent structure
- V1: Simpler error details → V2: Enhanced error information

### V1 approach

**Lightroom Status:**

```shell
curl -X GET \
  https://image.adobe.io/lrService/status/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

**Photoshop Status:**

```shell
curl -X GET \
  https://image.adobe.io/pie/psdService/status/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

### V2 approach

**Unified Status (all operations):**

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

## Response format

### Job status values

**Possible Status Values:**

- `pending` - Job is queued but not yet started
- `running` - Job is currently processing
- `succeeded` - Job completed successfully
- `failed` - Job failed with errors

### Successful job response

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "succeeded",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "modifiedTime": "2025-01-15T10:30:45.000Z",
  "result": {
    "outputs": [
      {
        "url": "https://storage.example.com/output.jpg",
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

### Failed job response

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "modifiedTime": "2025-01-15T10:30:45.000Z",
  "errorDetails": [
    {
      "errorCode": "400401",
      "message": "The value provided is not valid."
    }
  ]
}
```

### Running job response

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "modifiedTime": "2025-01-15T10:30:15.000Z"
}
```

## Polling pattern

### Recommended polling strategy

```javascript
async function pollJobStatus(jobId, maxAttempts = 60, intervalMs = 5000) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const response = await fetch(
      `https://photoshop-api.adobe.io/v2/status/${jobId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "x-api-key": apiKey,
        },
      }
    );

    const status = await response.json();

    if (status.status === "succeeded") {
      return status.result;
    }

    if (status.status === "failed") {
      throw new Error(`Job failed: ${JSON.stringify(status.errorDetails)}`);
    }

    // Status is 'pending' or 'running', wait and retry
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }

  throw new Error("Job polling timeout");
}
```

**Best Practices:**

- Start with a 5-second polling interval
- Implement exponential backoff for longer jobs
- Set a reasonable maximum polling time
- Handle all status values (pending, running, succeeded, failed)

### Polling with exponential backoff

```javascript
async function pollWithBackoff(jobId, maxAttempts = 20) {
  let interval = 2000; // Start with 2 seconds
  const maxInterval = 30000; // Cap at 30 seconds

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const response = await fetch(
      `https://photoshop-api.adobe.io/v2/status/${jobId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "x-api-key": apiKey,
        },
      }
    );

    const status = await response.json();

    if (status.status === "succeeded" || status.status === "failed") {
      return status;
    }

    await new Promise((resolve) => setTimeout(resolve, interval));
    interval = Math.min(interval * 1.5, maxInterval);
  }

  throw new Error("Job polling timeout");
}
```

## Output handling

### External storage outputs

When using external storage, outputs contain URLs to download results:

```json
{
  "result": {
    "outputs": [
      {
        "url": "https://storage.example.com/output.jpg",
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

**Downloading Outputs:**

```shell
curl -X GET "https://storage.example.com/output.jpg" -o output.jpg
```

### Hosted storage outputs

With hosted storage, outputs contain temporary Adobe-managed URLs:

```json
{
  "result": {
    "outputs": [
      {
        "url": "https://adobe-hosted-storage.example.com/temp/output.jpg?expires=...",
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

<InlineAlert variant="warning" slots="text"/>

Hosted storage URLs expire based on the `validityPeriod` specified in your request. Download outputs before expiration.

### Embedded storage outputs

With embedded storage, outputs contain data directly in the response:

```json
{
  "result": {
    "outputs": [
      {
        "destination": {
          "embedded": "base64",
          "content": "iVBORw0KGgoAAAANSUhEUgAA..."
        },
        "mediaType": "image/jpeg"
      }
    ]
  }
}
```

or for JSON outputs:

```json
{
  "result": {
    "outputs": [
      {
        "destination": {
          "embedded": "json",
          "content": {
            "document": {...},
            "layers": [...]
          }
        },
        "mediaType": "application/json"
      }
    ]
  }
}
```

## Error handling

### Error response structure

```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "modifiedTime": "2025-01-15T10:30:45.000Z",
  "errorDetails": [
    {
      "errorCode": "400401",
      "message": "The value provided is not valid."
    },
    {
      "errorCode": "400420",
      "message": "Required fields missing on the API request."
    }
  ]
}
```

### Common error codes

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 400400     | Invalid JSON in request payload    |
| 400401     | Invalid value provided             |
| 400410     | Required fields missing            |
| 400411     | Request blocked by content filters |
| 403401     | User not authorized                |
| 403421     | Quota exhausted                    |
| 404        | Job not found                      |
| 422404     | Unable to process outputs          |
| 500600     | Internal server error              |

### Error handling example

```javascript
async function handleJobStatus(jobId) {
  try {
    const status = await pollJobStatus(jobId);

    if (status.status === "failed") {
      console.error("Job failed with errors:");
      status.errorDetails.forEach((error) => {
        console.error(`- ${error.errorCode}: ${error.message}`);
      });
      throw new Error("Job processing failed");
    }

    return status.result.outputs;
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error("Job not found. Invalid job ID.");
    }
    throw error;
  }
}
```

## HTTP status codes

The status endpoint itself can return different HTTP status codes:

| HTTP Status | Meaning                         |
| ----------- | ------------------------------- |
| 200         | Status retrieved successfully   |
| 400         | Invalid job ID format           |
| 401         | Invalid or missing access token |
| 404         | Job not found                   |
| 500         | Internal server error           |

## Job lifecycle

Understanding the job lifecycle helps with proper status handling:

```text
1. Job Submitted
   ↓
2. pending → Job queued, waiting to start
   ↓
3. running → Job actively processing
   ↓
4. succeeded → Job completed successfully
   OR
4. failed → Job encountered errors
```

**Typical Timing:**

- Simple operations (auto tone, auto straighten): 5-15 seconds
- Complex operations (actions, composites): 15-60 seconds
- Large files or multiple operations: 60+ seconds

## Complete polling example

```javascript
// Complete example with proper error handling
async function processJob(jobId) {
  const maxAttempts = 60;
  const pollInterval = 5000;

  console.log(`Starting to poll job ${jobId}`);

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const response = await fetch(
        `https://photoshop-api.adobe.io/v2/status/${jobId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "x-api-key": apiKey,
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`Job ${jobId} not found`);
        }
        throw new Error(`Status check failed: ${response.statusText}`);
      }

      const status = await response.json();
      console.log(`Job status: ${status.status} (attempt ${attempt + 1})`);

      switch (status.status) {
        case "succeeded":
          console.log("Job completed successfully");
          return status.result.outputs;

        case "failed":
          console.error("Job failed:", status.errorDetails);
          throw new Error(
            `Job failed: ${status.errorDetails
              .map((e) => e.message)
              .join(", ")}`
          );

        case "pending":
        case "running":
          // Continue polling
          await new Promise((resolve) => setTimeout(resolve, pollInterval));
          break;

        default:
          throw new Error(`Unknown job status: ${status.status}`);
      }
    } catch (error) {
      console.error(`Error polling job status:`, error);
      throw error;
    }
  }

  throw new Error(
    `Job polling timeout after ${(maxAttempts * pollInterval) / 1000} seconds`
  );
}

// Usage
try {
  const outputs = await processJob(jobId);
  console.log("Outputs:", outputs);
} catch (error) {
  console.error("Job processing failed:", error);
}
```

## Migration checklist

- [ ] Update base URL from `image.adobe.io` to `photoshop-api.adobe.io`
- [ ] Change endpoint path to `/v2/status/{jobId}`
- [ ] Update status value handling (pending, running, succeeded, failed)
- [ ] Implement proper error handling for new error structure
- [ ] Update polling logic with appropriate intervals
- [ ] Handle different output types (external, hosted, embedded)
- [ ] Update error code handling for new error codes
- [ ] Test with all operation types (edit, actions, composite, etc.)

## Common migration issues

### Issue: Using service-specific endpoint

**Problem:** Still using separate endpoints per service

```javascript
// Wrong
const url = `https://image.adobe.io/lrService/status/${jobId}`;
```

**Solution:** Use unified endpoint

```javascript
// Correct
const url = `https://photoshop-api.adobe.io/v2/status/${jobId}`;
```

### Issue: Incorrect status value handling

**Problem:** Only checking for "success" and "failure"

**Solution:** Handle all status values

```javascript
if (status.status === 'succeeded') { ... }
else if (status.status === 'failed') { ... }
else if (status.status === 'running' || status.status === 'pending') {
  // Continue polling
}
```

### Issue: Not handling error details array

**Problem:** Expecting single error message

**Solution:** Handle array of errors

```javascript
if (status.errorDetails) {
  status.errorDetails.forEach((error) => {
    console.error(`${error.errorCode}: ${error.message}`);
  });
}
```

## Next steps

- Review all migration guides to understand different job types
- Update your polling implementation with proper error handling
- Test status checking with development endpoints
- Implement monitoring for job failures in production

## Need help?

Contact the Adobe DI ART Service team for technical support with status endpoint migration.
