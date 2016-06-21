class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.dependenceModel = None
        self.model = None
        self.save_loc = None

    def train(self, labeledDoc=None):
        raise NotImplementedError("Should have implemented this")

    def setSaveLocation(self, save):
        self.save_loc = save

    def setDependenceModel(self, model):
        """
        Hay modelos que se apoyan en otros para generar su propio entrenamiento.
        Este metodo lo anyade
        :param model: modelo del estilo Doc2Vec por ahora
        """
        self.dependenceModel = model

    def predict(self, text):
        raise NotImplementedError("Should have implemented this")

    def load(self):
        raise NotImplementedError("Should have implemented this")