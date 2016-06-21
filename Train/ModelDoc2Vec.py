from Model import Model
from TextProcessing.Doc2Vec import Doc2Vec
from Config.Conf import Conf
import numpy as np

class ModelDoc2Vec(Model):
    def __init__(self):
        super(ModelDoc2Vec, self).__init__()

    def train(self, labeledDoc):
        """
        Entrena el modelo Doc2Vec
        :param labeledDoc: localizacion en disco del fichero labeledDoc
        :return: True si todo correcto, Raise exception si fallo
        """
        if self.save_loc == None:
            raise UnboundLocalError("Should have set the save path <setSaveLocation>")

        d2v = Doc2Vec()
        d2v.train(labeledDoc, self.save_loc, dimension=Conf().getDimVectors(), epochs=30, method="DM")

    def verosimility(self, labeledDoc):
        d2v = Doc2Vec()
        d2v.loadModel(self.save_loc)
        vecs = d2v.getNormalizedTagsVectors()

        total_err = 0.0
        count = 0.0

        for doc in labeledDoc:
            text = doc.words
            tag = doc.tags[0]
            vec = d2v.simulateVectorsFromVectorText(text)
            cosine_err = 1.0 - np.dot(vecs[tag], np.array([vec]).T)
            total_err += cosine_err
            count += 1

        print "Error total"
        print total_err
        print "Error relativo"
        print total_err / count

    def load(self):
        if self.save_loc == None:
            raise UnboundLocalError("Should have set the save path <setSaveLocation>")

        self.d2v = Doc2Vec()
        self.d2v.loadModel(self.save_loc)

    def predict(self, text):
        return [self.d2v.simulateVectorsFromVectorText(text)]