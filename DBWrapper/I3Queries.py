from ConnectorSQL import ConnectorSQL
from ConnectorSolr import ConnectorSolr
from Config.Conf import Conf
from Train.TrainObj import TrainObj
from itertools import groupby
from operator import itemgetter

class I3Queries(object):
    def __init__(self):
        super(I3Queries, self).__init__()
        #sql
        self.connSQL = ConnectorSQL()
        self.tables = Conf().getClassificationTables()
        #solr
        self.connSolr = ConnectorSolr()
        self.collectionSolr = self.connSolr.getCollection()

    def getTrainFiles(self, limit=-1):
        """
        Consulta los ficheros de la base de datos, de la tabla de clasificacion
        :param
            limit: por defecto -1, no tiene limite, limite de elementos a retornar
        :return: lista de objetos de tipo Entrenamiento
        """
        """
        CREATE TABLE documents_classification (
            submitfileid integer NOT NULL,
            hbasedocumentid character varying(255) NOT NULL,
            categoryid integer NOT NULL,
            categoryname character varying(255),
                CONSTRAINT documents_classification PRIMARY KEY (submitfileid, categoryid))
        """

        query = "SELECT DISTINCT hbasedocumentid, categoryname FROM %s "%self.tables.classification
        cur_sql = self.connSQL.getCursor()

        if limit != -1 and limit > 1:
            query += "LIMIT %s"
            cur_sql.execute(query, [limit, ])
        else:
            cur_sql.execute(query)

        rows = cur_sql.fetchall()
        """
            codigo para simular algo parecido a reduceByKey de Spark
        """
        rows = [(row[0], [row[1]]) for row in rows]
        def my_reduce(obj1, obj2):
            text, lang = self.getTextSolr(obj1[0])
            return (obj1[0], text, lang, obj1[1] + obj2[1])

        docs = [reduce(my_reduce, group) for _, group in groupby(sorted(rows), key=itemgetter(0))]

        trainObjs = [TrainObj(idn, text, lang, cts) for idn, text, lang, cts in docs]
        return trainObjs

    def getTextSolr(self, idSolr, collection=None):
        #self.connSolr
        conn = self.connSolr.getConexion()
        #documents = [(texto, idioma)]

        docs = []
        if collection is None:
            docs = conn[self.collectionSolr].search({'q': "id:" + str(idSolr)}).result.response.docs
        else:
            docs = conn[collection].search({'q': "id:" + str(idSolr)}).result.response.docs
        try:
            for doc in conn[self.collectionSolr].search({'q': "id:" + str(idSolr)}).result.response.docs:
                for key in doc:
                    if key.startswith("content") and len(key) > len("content"):
                        return doc[key], key.split("_")[1]

            return "err", "err"
        except Exception, e:
            return "err", "err"