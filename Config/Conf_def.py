from collections import namedtuple

class Conf():
    """docstring for SparkContexto"""
    class __impl:
        """docstring for __impl"""
        def __init__(self):
            #dominio web (sin "http://" ni "/" final)
            self.domain = '0.0.0.0:8000'

            #models save location
            self.models_save = ''
            self.models_save_temp = ''

            #SQL
            self.sql_database = ''
            self.sql_user = ''
            self.sql_password = ''
            self.sql_host = ''
            self.sql_port = ''

            #SQL Tables
            self.classification_t = ''

            #Solr cloud
            self.solr_url = ''
            
            self.solr_collection = ''

            #vectors
            self.dimVectors = 128



        def getDomain(self):
            return self.domain

        def getClassificationTables(self):
            Tables = namedtuple('ClassificationTables', 'classification')
            return Tables(self.classification_t)

        def getSolrUrl(self):
            return self.solr_url

        def getSolrCollection(self):
            return self.solr_collection

        def getSQLInfo(self):
            infoSQL = namedtuple('InfoSQL', 'database, user, password, host')
            return infoSQL(self.sql_database, self.sql_user, self.sql_password, self.sql_host)

        def getDimVectors(self):
            return self.dimVectors

        def getModelSave(self):
            return self.models_save

        def getModelSaveTemp(self):
            return self.models_save_temp

    # storage for the instance reference
    __instance = None

    def __init__(self):
        if Conf.__instance is None:
            Conf.__instance = Conf.__impl()

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)