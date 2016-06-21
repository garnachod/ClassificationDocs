# gensim modules
from gensim.models import Doc2Vec
from LabeledLineSentence import LabeledLineSentence
import gensim
import time
import numpy as np




class Doc2Vec(object):
    """docstring for Doc2Vec"""

    def __init__(self):
        super(Doc2Vec, self).__init__()
        self.doc2vec = None

    def train(self, sentences, save_location, dimension=50, epochs=20, method="DBOW"):
        total_start = time.time()
        dm_ = 1
        if method == "DBOW":
            dm_ = 0
        model = gensim.models.Doc2Vec(min_count=2, window=11, size=dimension, dm=dm_, sample=1e-5, negative=10, workers=10,
                                      alpha=0.02)

        print "inicio vocab"
        model.build_vocab(sentences)
        sentences.reloadDoc()
        print "fin vocab"
        first_alpha = model.alpha
        last_alpha = 0.0001
        # model.min_alpha = 0.0001
        next_alpha = first_alpha
        for epoch in xrange(epochs):
            start = time.time()
            print "iniciando epoca DBOW:"
            print model.alpha
            next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch + 1)) + last_alpha)
            model.min_alpha = next_alpha
            model.train(sentences)
            sentences.reloadDoc()
            end = time.time()
            model.alpha = next_alpha
            print "tiempo de la epoca " + str(epoch) + ": " + str(end - start)

        model.save(save_location)

        total_end = time.time()

        print "tiempo total:" + str((total_end - total_start) / 60.0)

    def simulateVectorsFromVectorText(self, vectorText, modelLocation=None):
        if self.doc2vec is None and modelLocation is None:
            raise Exception("Se tiene que cargar el modelo")

        if self.doc2vec is None:
            self.doc2vec = gensim.models.Doc2Vec.load(modelLocation)

        vector = np.array(self.doc2vec.infer_vector(vectorText, steps=3, alpha=0.1))
        return vector / np.linalg.norm(vector)

    def loadModel(self, modelLocation):
        self.doc2vec = gensim.models.Doc2Vec.load(modelLocation)

    def getNormalizedTagsVectors(self):
        doctags = self.doc2vec.docvecs.doctags
        ret = {}
        for doctag in doctags:
            vector = np.array(self.doc2vec.docvecs[doctag])
            ret[doctag] = vector / np.linalg.norm(vector)

        return ret