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
        title: 'Firefly Services',
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
          }
        ]
      },
      {
        title: 'Learn More',
        path: '/getting_started/concepts/',
        header: true,
        pages: [
          {
            title: 'Concepts',
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
            title: 'Features',
            path: '/guides/'
          },
          {
            title: 'Using our Guides',
            path: '/guides/code_sample/index.md'
          },
          {
            title: 'Photoshop Actions',
            path: '/guides/photoshop_actions/'
          },
          {
            title: 'ActionJSON Endpoint',
            path: '/guides/actionjson_endpoint/'
          },
          {
            title: 'Smart Objects and the API',
            path: '/guides/smart_objects_and_the_api/'
          },
          {
            title: 'Edit Text',
            path: '/guides/edit_text/'
          },
          {
            title: 'Text layers Edits',
            path: '/guides/text_layers_edits/'
          },
          {
            title: 'Product Crop',
            path: '/guides/product_crop/'
          },
          {
            title: 'DepthBlur',
            path: '/guides/depthblur/'
          },
          {
            title: 'Rendering and Conversions',
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
            title: 'Triggering an Event from the APIs',
            path: '/guides/triggering_an_event/'
          },
          {
            title: 'Create Mask',
            path: '/guides/create_mask/'
          }
        ]
      }
    ]
  },
  plugins: [`@adobe/gatsby-theme-aio`]
};