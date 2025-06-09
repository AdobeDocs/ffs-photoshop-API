---
title: Get Job Status
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

# Get Job Status

Each of our Photoshop API endpoints, when invoked, initiates an asynchronous job and returns a response body that contains the href to poll for status of the job.

## Fetch the status of an API

Each of our Photoshop API endpoints, when invoked, initiates an asynchronous job and returns a response body that contains the href to poll for status of the job.

```json
{
    "_links": {
        "self": {
            "href": "https://image.adobe.io/pie/psdService/status/de2415fb-82c6-47fc-b102-04ad651c5ed4"
        }
    }
}
```

Using the job id returned from the response (as above) of a successfully submitted API call, you can poll on the corresponding value in the `href` field, to get the status of the job.

```shell
curl -X GET \
  https://image.adobe.io/pie/psdService/status/de2415fb-82c6-47fc-b102-04ad651c5ed4 \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json"
```


## Poll for job status for all Other APIs

Once your job completes successfully (no errors/failures reported), this will return a response body containing the job status for each requested output. For the `/renditionCreate` API call in [Example 10](/guides/code_sample/index.md#create-a-document-rendition) as illustrated above, a sample response containing the job status is as shown below:

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