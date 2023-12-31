import time as _time
import uuid
from arcgis.gis import GIS
from .._con import Connection
from arcgis._impl.common._mixins import PropertyMap
from arcgis import env as _env
from arcgis.gis._impl._jb import StatusJob
from arcgis.gis import Item
import concurrent.futures

###########################################################################
class PortalDataStore(object):
    """

    The ``PortalDatastore`` provides access to operations that allow you to do the
    following:

    - Validate a data store against your server.
    - Register a data store to your server.
    - Retrieve a list of servers your data store is registered to.
    - Refresh your data store registration information in the server.
    - Unregister a data store from your server.

    .. note::
        Users also have the ability to bulk publish layers from a :class:`~arcgis.gis.Datastore` object,
        retrieve a list of previously published layers, and delete bulk-published layers.

    """

    _con = None
    _gis = None
    _url = None
    _properties = None
    # ----------------------------------------------------------------------
    def __init__(self, url, gis):
        """Constructor"""
        self._url = url
        self._gis = gis
        self._con = gis._con

    # ----------------------------------------------------------------------
    def __str__(self):
        return "< PortalDataStore @ {url} >".format(url=self._url)

    # ----------------------------------------------------------------------
    def __repr__(self):
        return "< PortalDataStore @ {url} >".format(url=self._url)

    # ----------------------------------------------------------------------
    def describe(self, item, server_id, path, store_type="datastore"):
        """
        The ``describe`` method is used to list the contents of a data store. A
        client can use it multiple times to discover the contents of the
        data store incrementally. For example, the client can request a
        description of the root, and then request sub-folders.


        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item. The :class:`~arcgis.gis.Item` to describe.
        ------------------     --------------------------------------------------------------------
        server_id              Optional String. The unique id of the registered server.
        ------------------     --------------------------------------------------------------------
        path                   Optional String. The path to examine the data in.
        ------------------     --------------------------------------------------------------------
        store_type             Optional String. For root resource the object type should be `datastore`,
                               and for sub-folders, the object type should be listed as `folder`.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.describe(item= datastore_object1, server_id="server_name", path = "path_name")

        :return:
            A :class:`~arcgis.gis._impl..StatusJob` object

        """
        if isinstance(item, Item):
            item = item.id
        params = {
            "datastoreId": item,
            "serverId": server_id,
            "path": path,
            "type": store_type,
            "f": "json",
        }
        url = f"{self._url}/describe"
        res = self._con.get(url, params)
        _time.sleep(0.5)
        executor = concurrent.futures.ThreadPoolExecutor(1)
        futureobj = executor.submit(
            self._status, **{"job_id": res["jobId"], "key": res["key"]}
        )
        executor.shutdown(False)
        return StatusJob(
            future=futureobj,
            op="Describe DataStore",
            jobid=res["jobId"],
            gis=self._gis,
            notify=_env.verbose,
            extra_marker="",
        )

    # ----------------------------------------------------------------------
    def _status(self, job_id, key=None):
        """
        Checks the status of an export job

        :return: dict
        """
        params = {}
        if job_id:
            url = f"{self._gis._portal.resturl}portals/self/jobs/{job_id}"
            params["f"] = "json"
            res = self._con.post(url, params)
            while res["status"] not in ["completed", "complete", "succeeded"]:
                res = self._con.post(url, params)
                if res["status"] == "failed":
                    raise Exception(res)
            count = 0
            while (
                res["status"] in ["completed", "complete", "succeeded"]
                and not "result" in res
                and count < 10
            ):
                res = self._con.post(url, params)
                if "result" in res:
                    return res
                count += 1
            return res
        else:
            raise Exception(res)

    # ----------------------------------------------------------------------
    @property
    def properties(self):
        """
        The ``properties`` property retrieves the properties of the current :class:`~arcgis.gis.DataStore` object

        :return:
           A list of the :class:`~arcgis.gis.DataStore` object properties
        """
        if self._properties is None:
            params = {"f": "json"}
            res = self._con.get(self._url, params)
            self._properties = PropertyMap(res)
        return self._properties

    # ----------------------------------------------------------------------
    def register(self, item, server_id, bind=False):
        """

        The ``register`` method allows for :class:`~arcgis.gis.Datastore` objects to be added to an ArcGIS Server
        instance.

        .. note::
            Before registering a :class:`~arcgis.gis.Datastore`, it is recommended that you validate your
            :class:`~arcgis.gis.Datastore` with the given server.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required :class:`~arcgis.gis.Item` object or Item Id (as string). The item Id or Item of
                               the data store to register with the server. Note that a data store can be
                               registered on multiple servers.
        ------------------     --------------------------------------------------------------------
        server_id              Required String. The unique id of the server you want to register
                               the datastore with.
        ------------------     --------------------------------------------------------------------
        bind                   Optional Boolean. Specifies whether to bind the data store item to
                               the federated server. For more information about binding a data
                               store to additional federated servers, see the note below.
                               The default value is `False`.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.register(datastore_object1, "server_name")

        :return:
            A boolean indicating success (True), or failure (False)

        .. note::
            To create a :class:`~arcgis.gis.Datastore` object from an existing :class:`~arcgis.gis.dataStore`,
            see the `Create a data store item from an existing data store <https://enterprise.arcgis.com/en/portal/latest/administer/windows/create-item-from-existing-data-store.htm#ESRI_SECTION1_58D081604CF841AC80D527D34A67660C>`_
            page in the ArcGIS Online resources.

        """
        if isinstance(item, Item):
            item_id = item.id
        elif isinstance(item, str):
            item_id = item
        url = "{base}/addToServer".format(base=self._url)
        params = {"f": "json", "datastoreId": item_id, "serverId": server_id}
        if not bind is None:
            params["bindToServerDatastore"] = bind
        res = self._con.post(url, params)
        if "success" in res:
            return res["success"]
        return res

    # ----------------------------------------------------------------------
    @property
    def _all_datasets(self):
        """
        The _all_datasets resource page provides access to bulk publishing
        operations. These operations allow users to publish and synchronize
        datasets from a given data store, return a list of published layers,
        and remove all previously published layers in preparation for the
        deregistration of a data store.

        :return: Boolean

        """
        url = "{base}/allDatasets".format(base=self._url)
        params = {"f": "json"}
        res = self._con.post(url, params)
        if "success" in res:
            return res["success"]
        elif "status" in res:
            return res["status"] == "success"
        return res

    # ----------------------------------------------------------------------
    def delete_layers(self, item):
        """
        The ``delete_layers`` method removes all layers published from the :class:`~arcgis.gis.Datastore` object.

        .. note::
            Before a :class:`~arcgis.gis.Datastore` object can be unregistered from a server, all of its
            bulk-published layers must be deleted.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item. The :class:`~arcgis.gis.Datastore` to delete all published layers.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.delete_layers(datastore_object)

        :return:
            A boolean indicating success (True), or failure (False)

        """
        if isinstance(item, Item):
            item_id = item.id
        else:
            item_id = item
            item = self._gis.content.get(item_id)
        params = {"f": "json", "datastoreId": item_id}
        url = f"{self._url}/allDatasets/deleteLayers"
        res = self._con.post(url, params)
        if res["success"] == True:
            status = item.status(self, job_id=res["jobId"])
            while status["status"].lower() != "completed":
                status = item.status(self, job_id=res["jobId"])
                if status["status"].lower() == "failed":
                    return False
                else:
                    _time.sleep(2)
            return True
        return False

    # ----------------------------------------------------------------------
    def layers(self, item):
        """
        The ``layers`` operation returns a list of layers bulk published from a
        :class:`~arcgis.gis.Datastore` with the
        :attr:`~arcgis.gis._impl._datastores._ds.PortalDataStore.publish_layers` method.

        .. note::
            The ``layers`` method returns an list of tuples, with each tuple containing two
            objects: a layer and the dataset it was published from.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item. The Data Store `Item` to list all published layers
                               and registered datasets.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.layers(datastore_object1)

        :return: A List of bulk-published :class:`~arcgis.gis.Layer` objects

        """

        if isinstance(item, Item):
            item_id = item.id
        else:
            item_id = item
            item = self._gis.content.get(item_id)

        url = "{base}/allDatasets/getLayers".format(base=self._url)
        params = {"f": "json", "datastoreId": item_id}
        res = self._con.post(url, params)
        if "layerAndDatasets" in res:
            return res["layerAndDatasets"]
        return []

    # ----------------------------------------------------------------------
    def publish(
        self, config: dict, server_id, folder=None, description=None, tags: list = None
    ):
        """
        The ``publish`` operation is used to publish scene layers by reference to data in a
        :class:`~arcgis.gis.Datastore`.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        config                 Required Dictionary.  This is the service configuration property
                               and it must contain the reference to the data in the data store. It
                               specifies the data store Id and the path of the data.  A client can
                               discover the proper paths of the data by using the `describe` method.

                               Example: {"type":"SceneServer","serviceName":"sonoma","properties":{"pathInCachedStore":"/v17_i3s/SONOMA_LiDAR.i3srest","cacheStoreId":"d7b0722fb42c494392cb1845dacc00d9"}}
        ------------------     --------------------------------------------------------------------
        server_id              Required String. The unique Id of the server to publish to.
        ------------------     --------------------------------------------------------------------
        folder                 Optional String. The name of the folder on server to place the service.  If none is provided, it is placed in the root.
        ------------------     --------------------------------------------------------------------
        description            Optional String. An optional string to attached to the `Item` generated.
        ------------------     --------------------------------------------------------------------
        tags                   Optional list. An array of descriptive words that describes the newly published dataset.  This will be added to the `Item`
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.publish(config= {"required" : "dictionary"}, server_id= "server_name")

        :return:
            A :class:`~arcgis.gis._impl._jb.StatusJob` object

        """
        url = f"{self._url}/publish"
        if isinstance(tags, list):
            tags = ",".join([str(t) for t in tags])

        params = {
            "serviceConfiguration": config,
            "serverId": server_id,
            "serverFolder": folder,
            "description": description,
            "tags": tags,
            "f": "json",
        }
        res = self._con.post(url, params)
        executor = concurrent.futures.ThreadPoolExecutor(1)
        futureobj = executor.submit(
            self._status, **{"job_id": res["jobId"], "key": res["key"]}
        )
        executor.shutdown(False)
        return StatusJob(
            future=futureobj,
            op="Publish",
            jobid=res["jobId"],
            gis=self._gis,
            notify=_env.verbose,
            extra_marker="",
        )

    # ----------------------------------------------------------------------
    def servers(self, item):
        """
        The ``servers`` property returns a list of your servers that a given
        data store has been registered to. This operation returns the
        serverId, the server name, both the server and admin URLs, and
        whether or not the server is hosted.


        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item. The DataStore :class:`~arcgis.gis.Item` object to list all registered servers.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.servers(datastore_object1)

        :return:
            A List with the serverID, server name, server URL, and admin URLs

        """

        if isinstance(item, Item):
            item_id = item.id
        else:
            item_id = item
            item = self._gis.content.get(item_id)

        url = self._url + "/getServers"
        params = {"f": "json", "datastoreId": item_id}
        res = self._con.post(url, params)
        if "servers" in res:
            return res["servers"]
        return res

    # ----------------------------------------------------------------------
    def publish_layers(
        self,
        item,
        srv_config: dict,
        server_id,
        folder=None,
        server_folder=None,
        future=False,
    ):
        """
        The ``publish_layers`` operation publishes, or syncs, the datasets from a
        :class:`~arcgis.gis.DataStore` object onto your ArcGIS Server, resulting in at least one
        :attr:`~arcgis.gis.Layer` per dataset. It is quite similar to the
        :attr:`~arcgis.gis._impl._datastores._ds.PortalDataStore.publish` method.

        .. note::
            When this operation is called for the first time, every parameter in
            the operation must be passed through. On subsequent calls,
            publish_layers will synchronize the datasets and created layers, which
            includes both publishing layers from new datasets and removing layers
            for datasets no longer found in the data store.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item. The Data Store `Item` to publish from.
        ------------------     --------------------------------------------------------------------
        srv_config             Required Dict. The JSON that will be used as a template for all the
                               services that will be published or synced. This JSON can be used to
                               change the properties of the data store's map and feature services.
                               Only map service configurations with feature services enabled are
                               supported by this parameter.
        ------------------     --------------------------------------------------------------------
        server_id              Required String. The serverId that the datasets will be published to.
        ------------------     --------------------------------------------------------------------
        folder                 Optional String. The folder to which the datasets will be published.
        ------------------     --------------------------------------------------------------------
        server_folder          Optional String. The name of the server folder.
        ------------------     --------------------------------------------------------------------
        future                 Optional Boolean.  If False, the value is returned, else a
                               `StatusJob` is returned.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.publish_layers(datastore_object1, srv_config= {"required" : "dictionary"})

        :return:
            Boolean when `future=False` else a :class:`~arcgis.gis._impl._jb.StatusJob` object

        """
        if server_folder is None:
            base = "buld_pub_"
            if isinstance(item, Item):
                base = item.title.lower().replace(" ", "")
            server_folder = f"{base}{uuid.uuid4().hex[:3]}"
        if folder is None:
            from arcgis.gis import UserManager, User, ContentManager

            isinstance(self._gis, GIS)
            cm = self._gis.content
            folder = cm.create_folder(folder=f"srvc_folder_{uuid.uuid4().hex[:5]}")[
                "id"
            ]
        if isinstance(item, Item):
            item_id = item.id
        else:
            item_id = item
            item = self._gis.content.get(item_id)
        url = self._url + "/allDatasets/publishLayers"
        params = {
            "f": "json",
            "datastoreId": item_id,
            "templateSvcConfig": srv_config,
            "portalFolderId": folder,
            "serverId": server_id,
            "serverFolder": server_folder,
        }
        res = self._con.post(url, params)
        if res["success"] == True:
            status = item.status()
            while status["status"].lower() != "completed":
                status = item.status()
                if status["status"].lower() == "failed":
                    return False
                else:
                    _time.sleep(2)
            return True
        return False

    # ----------------------------------------------------------------------
    def unregister(self, item, server_id):
        """
        The ``unregister`` method removes the :class:`~arcgis.gis.Datastore` association from a server.

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.unregister(datastore_object1, "server_id")

        :return:
            A boolean indicating success (True), or failure (False)

        """
        if isinstance(item, Item):
            item_id = item.id
        elif isinstance(item, str):
            item_id = item
        url = self._url + "/removeFromServer"
        params = {"f": "json", "datastoreId": item_id, "serverId": server_id}
        res = self._con.post(url, params)
        if "success" in res:
            return res["success"]
        return res

    # ----------------------------------------------------------------------
    def refresh_server(self, item, server_id):
        """
        Th ``refresh_server`` method updates the server with newly configured inforamtion.

        .. note::
            After a :class:`~arcgis.gis.Datastore` has been registered, there may be times in which
            the :class:`~arcgis.gis.Datastore` object's registration information may be changed. When
            changes like these occur, the server will need to be updated with
            the newly configured information so that your users will still be
            able to access the data store items without interruption.

        .. warning::
            This operation can only be performed after the data
            store information has been updated.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        item                   Required Item/Item Id (as string). The item Id or Item of the data
                               store to register with the server. Note that a data store can be
                               registered on multiple servers.
        ------------------     --------------------------------------------------------------------
        server_id              Required String. The unique id of the server you want to register
                               the datastore with.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.refresh_server(datastore_object1, "server_id")

        :return:
            A boolean indicating success (True), or failure (False)

        """
        if isinstance(item, Item):
            item_id = item.id
        elif isinstance(item, str):
            item_id = item

        url = self._url + "/refreshServer"
        params = {"f": "json", "datastoreId": item_id, "serverId": server_id}
        res = self._con.post(url, params)
        if "success" in res:
            return res["success"]
        return res

    # ----------------------------------------------------------------------
    def validate(self, server_id, item=None, config=None, future=False):
        """
        The ``validate`` method ensures that your ArcGIS Server can connect and use
        the datasets stored within a given data store. A :class:`~arcgis.gis.Datastore` can be validated by using either
        its datastoreId or the JSON for an unregistered :class:`~arcgis.gis.Datastore`.

        .. note::
            While this operation
            can be called before or after the :class:`~arcgis.gis.Datastore` has been registered
            with your server, it is recommended that the validate operation is
            performed beforehand.

        ==================     ====================================================================
        **Argument**           **Description**
        ------------------     --------------------------------------------------------------------
        server_id              Required String. The unique id of the server you want to register
                               the datastore with.
        ------------------     --------------------------------------------------------------------
        item                   Optional Item/Item Id (as string). The item Id or Item of the data
                               store to register with the server. Note that a data store can be
                               registered on multiple servers.
        ------------------     --------------------------------------------------------------------
        config                 Optional dict. The connection information for a new datastore.
        ==================     ====================================================================

        .. code-block:: python

            # Usage Example

            >>> datastore_manager.validate("server_name")

        :return:
            A boolean indicating success (True), or failure (False)

        """

        if item and isinstance(item, Item):
            item_id = item.id
        elif item and isinstance(item, str):
            item_id = item
        else:
            item_id = None

        url = self._url + "/validate"
        params = {"f": "json", "serverId": server_id}
        if item:
            params["datastoreId"] = item_id
        elif config:
            import json

            params["datastore"] = json.dumps(config)
        else:
            raise ValueError("Invalid parameters, an item or config is required.")
        res = self._con.post(url, params)
        if "status" in res:
            if res["status"] == "success":
                return True
            return res["status"]
        return res
