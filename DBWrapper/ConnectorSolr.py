from Config.Conf import Conf
from solrcloudpy import SolrConnection
from kazoo.client import KazooClient
import psycopg2

class ConnectorSolr():
    """docstring for ConnectorSolr"""

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self):
            self.url = Conf().getSolrUrl()
            self.collection = Conf().getSolrCollection()
            zk = KazooClient(hosts=self.url, read_only=True)
            zk.start()
            self.urls = []
            for node in zk.get_children("/live_nodes"):
                self.urls.append(node.replace('_solr', ''))
            zk.stop()
            self.conn = SolrConnection(self.urls, version="5.4.0", webappdir='solr')

        def getConexion(self):
            """ Test method, return singleton conexion"""
            return self.conn

        def getCollection(self):
            return self.collection

    # storage for the instance reference
    __instance = None

    def __init__(self):
        if ConnectorSolr.__instance is None:
            ConnectorSolr.__instance = ConnectorSolr.__impl()

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)