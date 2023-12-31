from ._task import Task


class BigDataAnalytics(Task):
    """
    BigDataAnalytics class implements Task and provides public facing methods to
    access BigDataAnalytics API endpoints
    """

    _id = ""
    _gis = None
    _util = None
    _item = None

    def __init__(self, gis, util, item=None):
        self._gis = gis
        self._util = util

        if item:
            self._item = item
            self._id = item["id"]

    # ----------------------------------------------------------------------
    def __repr__(self):
        return "<%s id:%s label:%s>" % (
            type(self).__name__,
            self._id,
            self._item["label"],
        )

    # ----------------------------------------------------------------------
    def start(self):
        """
        Start the Big Data Analytics for the given id
        :return: response of bigdata_analytics start
        """
        return self._util._start("analytics/bigdata", self._id)

    # ----------------------------------------------------------------------
    def stop(self):
        """
        Stop the Big Data Analytics for the given id
        Return True if the Big Data Analytics was successfully stopped.
        :return: boolean
        """
        return self._util._stop("analytics/bigdata", self._id)

    # ----------------------------------------------------------------------
    @property
    def status(self):
        """
        Get the status of the running Big Data Analytics for the given id
        :return: response of Big Data Analytics status
        """
        return self._util._status("analytics/bigdata", self._id)

    # ----------------------------------------------------------------------
    @property
    def metrics(self):
        """
        Get the metrics of the running Big Data Analytics for the given id
        :return: response of Big Data Analytics metrics
        """
        return self._util._metrics("analytics/bigdata/metrics", self._id)

    # ----------------------------------------------------------------------
    def delete(self):
        """
        Deletes an existing Big Data Analytics instance
        :return: A boolean containing True (for success) or
         False (for failure) a dictionary with details is returned.
        """
        return self._util._delete("analytics/bigdata", self._id)
