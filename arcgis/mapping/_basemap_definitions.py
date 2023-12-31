# Note that these may change and need to be updated periodically

basemap_dict = {
    "streets": [
        {
            "id": "streets-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Street Map",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "satellite": [
        {
            "id": "satellite-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Imagery",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "hybrid": [
        {
            "id": "hybrid-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Imagery",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "hybrid-reference-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Boundaries and Places",
            "isReference": True,
            "visibility": True,
            "opacity": 1,
        },
    ],
    "terrain": [
        {
            "id": "terrain-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Terrain",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "terrain-reference-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Reference_Overlay/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Reference Overlay",
            "isReference": True,
            "visibility": True,
            "opacity": 1,
        },
    ],
    "topo": [
        {
            "id": "topo-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Topo Map",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "gray": [
        {
            "id": "gray-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Light Gray Base",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "gray-reference-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Light Gray Reference",
            "isReference": True,
            "visibility": True,
            "opacity": 1,
        },
    ],
    "dark-gray": [
        {
            "id": "dark-gray-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Dark Gray Base",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "dark-gray-reference-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Dark Gray Reference",
            "isReference": True,
            "visibility": True,
            "opacity": 1,
        },
    ],
    "oceans": [
        {
            "id": "oceans-base-layer",
            "url": "https://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Oceans Base",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "oceans-reference-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Oceans Reference",
            "isReference": True,
            "visibility": True,
            "opacity": 1,
        },
    ],
    "national-geographic": [
        {
            "id": "national-geographic-base-layer",
            "url": "https://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "NatGeo World Map",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "osm": [
        {
            "id": "osm-base-layer",
            "styleUrl": "https://cdn.arcgis.com/sharing/rest/content/items/3e1a00aeae81496587988075fe529f71/resources/styles/root.json",
            "layerType": "OpenStreetMap",
            "title": "Open Street Map",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "dark-gray-vector": [
        {
            "id": "dark-gray-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/c11ce4f7801740b2905eb03ddc963ac8/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Dark Gray",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "gray-vector": [
        {
            "id": "gray-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/8a2cba3b0ebf4140b7c0dc5ee149549a/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Light Gray",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "streets-vector": [
        {
            "id": "streets-vector-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/de26a3cf4cc9451298ea173c4b324736/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Light Gray",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "topo-vector": [
        {
            "id": "world-hillshade-layer",
            "url": "https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Hillshade",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "topo-vector-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/7dc6cea0b1764a1f9af2e679f642f0f5/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Topo",
            "visibility": True,
            "opacity": 1,
        },
    ],
    "streets-night-vector": [
        {
            "id": "streets-night-vector-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/86f556a2d1fd468181855a35e344567f/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Streets Night",
            "visibility": True,
            "opacity": 1,
        }
    ],
    "streets-relief-vector": [
        {
            "id": "world-hillshade-layer",
            "url": "https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer",
            "layerType": "ArcGISTiledMapServiceLayer",
            "title": "World Hillshade",
            "visibility": True,
            "opacity": 1,
        },
        {
            "id": "streets-relief-vector-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/b266e6d17fc345b498345613930fbd76/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Streets Relief",
            "visibility": True,
            "opacity": 1,
        },
    ],
    "streets-navigation-vector": [
        {
            "id": "streets-navigation-vector-base-layer",
            "styleUrl": "https://www.arcgis.com/sharing/rest/content/items/63c47b7177f946b49902c24129b87252/resources/styles/root.json",
            "layerType": "VectorTileLayer",
            "title": "World Streets Navigation",
            "visibility": True,
            "opacity": 1,
        }
    ],
}
