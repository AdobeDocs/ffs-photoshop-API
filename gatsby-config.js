/*
 * Copyright 2020 Adobe. All rights reserved.
 * This file is licensed to you under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License. You may obtain a copy
 * of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */

module.exports = {
  pathPrefix: process.env.PATH_PREFIX || '/firefly-services/docs/photoshop/',
  siteMetadata: {
    pages: [
      {
        title: 'All Firefly Services',
        path: 'https://developer.adobe.com/firefly-services/docs/guides/?aio_internal'
      },
      {
        title: 'About Photoshop API',
        path: '/'
      },
       {
        title: 'Getting Started',
        path: '/getting_started/'
      },
      {
        title: 'Guides',
        path: '/guides/'
      },
      {
        title: 'API Reference',
        path: '/api/index.md'
          },
    ],
    subPages: [
      {
        title: 'What\'s New',
        path: '/getting_started/whats_new/',
        header: true,
        pages: [
          {
            title: 'Deprecation Announcement',
            path: '/getting_started/deprecation_announcement/'
          }
        ]
      },
      {
        title: 'Getting Started',
        path: '/getting_started/',
        header: true,
        pages: [
          {
            title: 'Authentication',
            path: '/getting_started/'
          },
          {
            title: 'Storage Solutions',
            path: '/getting_started/storage_solutions'
          },
          {
            title: 'Technical Usage Notes',
            path: '/getting_started/technical_usage_notes'
          },
          {
            title: 'Webhooks and Events',
            path: '/getting_started/webhooks/'
          }
        ]
      },
      {
        title: 'Learn More',
        path: '/getting_started/concepts/',
        header: true,
        pages: [
          {
            title: 'Photoshop Concepts',
            path: '/getting_started/concepts/'
          }
        ]
      },
      {
        title: 'Guides',
        path: '/guides/',
        header: true,
        pages: [
          {
            title: 'Using these guides',
            path: '/guides/'
          },
          {
            title: 'Photoshop Actions',
            path: '/guides/photoshop_actions/'
          },
          {
            title: 'Using the ActionJSON endpoint',
            path: '/guides/actionjson_endpoint/'
          },
          {
            title: 'Using Smart Objects',
            path: '/guides/smart_objects_and_the_api/'
          },
          {
            title: 'Edit Text',
            path: '/guides/edit_text/'
          },
          {
            title: 'Product Crop',
            path: '/guides/product_crop/'
          },
          {
            title: 'Using Depth Blur',
            path: '/guides/depthblur/'
          },
          {
            title: 'PSD Renditions and Conversions',
            path: '/guides/rendering_and_conversions/'
          },
          {
            title: 'Layer level edits',
            path: '/guides/layer_level_edits/'
          },
          {
            title: 'Document level edits',
            path: '/guides/document_level_edits/'
          },
          {
            title: 'Artboards',
            path: '/guides/artboards/'
          },
          {
            title: 'Remove Background',
            path: '/guides/remove_background/'
          },
          {
            title: 'Triggering an event',
            path: '/guides/triggering_an_event/'
          },
          {
            title: 'Get job status',
            path: '/guides/get_job_status/'
          },
          {
            title: 'Retrieve a PSD manifest',
            path: '/guides/retrieve_manifest/'
          },
          {
            title: 'Create a mask',
            path: '/guides/create_mask/'
          },
          {
            title: 'Inpainting with Fill Mask',
            path: '/guides/using-fill-mask/'
          },
          {
            title: 'Enhance image mask quality with Refine Mask',
            path: '/guides/using-refine-mask/'
          }
        ]
      }
    ]
  },
  plugins: [`@adobe/gatsby-theme-aio`]
};
