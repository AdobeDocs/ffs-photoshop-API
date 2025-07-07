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

Photoshop API endpoints initiate an asynchronous job and return a response body that contains the URL to poll for the status of the job.

## Fetch the status of a job

Each of our Photoshop API endpoints, when invoked, initiates an asynchronous job and returns a response body that contains the URL to poll for the status of the job.

Using the job ID returned in the response of a successfully submitted API call, you can poll on the corresponding value in the `href` field, to get the status of the job:

```shell
curl -X GET \
  https://image.adobe.io/pie/psdService/status/<JOB_ID> \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json"
```

## Poll for job status for all other APIs

Once your job completes successfully, a response body containing the job status for each requested output is returned.

**Example response**

```json
{
  "jobId":"de2415fb-82c6-47fc-b102-04ad651c5ed4",
  "outputs":[
    {
      "input":"<SIGNED_GET_URL>",
      "status":"succeeded",
      "created":"2018-01-04T12:57:15.12345:Z",
      "modified":"2018-01-04T12:58:36.12345:Z",
      "_links":{
        "renditions":[
          {
            "href":"<SIGNED_GET_URL>",         
            "width": 512,
            "storage":"<storage>",
            "type":"image/jpeg"   
          },
          {
            "href":"<SIGNED_GET_URL>",
            "storage":"<storage>",
            "type":"image/png"
          }
        ]
      }
    }
  ],
  "_links":{
    "self":{
      "href":"https://image.adobe.io/pie/psdService/status/de2415fb-82c6-47fc-b102-04ad651c5ed4"
    }
  }
}
```
