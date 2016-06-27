from Model import Model
import numpy as np
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.externals import joblib
import json

class ModelClassification(Model):
    def __init__(self):
        super(ModelClassification, self).__init__()
        self.id_tags = None

    def train(self, labeledDoc):
        """
        Entrena el modelo final de clasificacion
        :param labeledDoc: objeto labeledDoc
        :return: True si todo correcto, Raise exception si fallo
        """
        if self.save_loc == None:
            raise UnboundLocalError("Should have set the save path <setSaveLocation>")

        if self.dependenceModel == None:
            raise UnboundLocalError("Should have set the TextProcessing.Doc2Vec model <setDependenceModel>")

        tags_id = {}
        Y = []
        X = []
        for doc in labeledDoc:
            for tag in doc.tags[1:]:
                if tag not in tags_id:
                    tags_id[tag] = len(tags_id)

        labeledDoc.reloadDoc()
        for doc in labeledDoc:
            tags = doc.tags
            text = doc.words
            auxY = np.zeros(len(tags_id))
            for tag in tags[1:]:
                auxY[tags_id[tag]] = 1.

            Y.append(auxY)
            vecX = self.dependenceModel.predict(text)[0]
            X.append(vecX)


        Y = np.array(Y)
        X = np.array(X)

        clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
        clf.fit(X, Y)
        print clf.predict(X)

        joblib.dump(clf, self.save_loc)
        with open(self.save_loc+"_tags_id", "w") as fout:
            fout.write(json.dumps(tags_id))


    def load(self):
        if self.save_loc == None:
            raise UnboundLocalError("Should have set the save path <setSaveLocation>")

        with open(self.save_loc + "_tags_id", "r") as fin:
            tags_id = json.loads(fin.read())

        self.id_tags = {}
        for tag in tags_id:
            self.id_tags[str(tags_id[tag])] = tag

        #print self.id_tags
        self.model = joblib.load(self.save_loc)

    def predict(self, text):
        if self.id_tags == None:
            raise UnboundLocalError("Should have load the model")

        X = self.dependenceModel.predict(text)
        prediction_vector = self.model.predict(X)[0]

        retorno = []
        for index, elem in enumerate(prediction_vector):
            #print index
            if elem == 1:
                retorno.append(self.id_tags[str(index)])

        return retorno

    def predict_proba(self, text):
        if self.id_tags == None:
            raise UnboundLocalError("Should have load the model")

        X = self.dependenceModel.predict(text)
        prediction_vector = self.model.predict_proba(X)[0]

        retorno = []
        for index, elem in enumerate(prediction_vector):
            #print index
            retorno.append({"tag":self.id_tags[str(index)], "probability":elem})

        return sorted(retorno, key = lambda x: x["probability"], reverse=True)

