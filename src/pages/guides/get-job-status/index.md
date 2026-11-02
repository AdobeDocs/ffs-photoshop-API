---
title: Get the status of a job
description: Learn how to fetch and poll for job status from the Photoshop API to monitor asynchronous operations
hideBreadcrumbNav: true
keywords:
  - job status
  - polling
  - asynchronous jobs
  - API status
  - job monitoring
contributors:
  - https://github.com/AEAbreu-hub
---

# Get job status

Photoshop API V2 endpoints initiate an asynchronous job and return a response body that contains the job ID and a URL to poll for the status of the job.

## Submit a job

A successfully submitted request returns a response like this:

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "statusUrl": "https://photoshop-api.adobe.io/v2/status/de2415fb-82c6-47fc-b102-04ad651c5ed4"
}
```

## Fetch the status of a job

Poll the `statusUrl`, or call `/v2/status/<JOB_ID>` with the returned `jobId`:

```shell
curl -X GET \
  https://photoshop-api.adobe.io/v2/status/<JOB_ID> \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

## Job status response

**Example response**

```json
{
  "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "status": "succeeded",
  "createdTime": "2025-01-20T10:35:00Z",
  "modifiedTime": "2025-01-20T10:40:00Z",
  "result": {
    "outputs": []
  }
}
```

| Field | Description |
|-------|-------------|
| `jobId` | ID of the job |
| `status` | One of `not_started`, `running`, `succeeded`, or `failed` |
| `createdTime` | Time the job was created, in ISO 8601 format |
| `modifiedTime` | Time the job was last modified, in ISO 8601 format |
| `result.outputs` | List of job outputs. The shape of each output depends on the endpoint that created the job; see that endpoint's [API reference](../../api/photoshop-v2/index.md). |
| `errorDetails` | List of `errorCode` and `message` entries. Present only when the job failed. |

An unknown job ID returns `404`, and an invalid job ID format returns `400`.
