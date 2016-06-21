from Model import Model
from ModelDoc2Vec import ModelDoc2Vec
from ModelClassification import ModelClassification
from TextProcessing.LabeledLineSentence import LabeledLineSentence
from TextProcessing.Doc2Vec import Doc2Vec

import os

class MetaModel(Model):

    def __init__(self, lang, folder):
        """
        initialize method, MetaModel use

        :py:class:: `ModelDoc2Vec
        :py:class:: `ModelClassification`

        :param lang: language of the model, to train, load or test
        :param folder: Path of the folder where the test is located
        """
        super(MetaModel, self).__init__()
        self.lang = lang
        self.folder = folder
        self.doc2vec_folder = "d2v"
        self.classification_folder = "class"
        self.trcl = None

    def train(self):
        """
        Train all the models,
        the trainer method use the save location.

        :func:`~Train.MetaModel.setSaveLocation`
        """
        #control de entrada
        if self.save_loc == None:
            raise UnboundLocalError("Should have set the save path <setSaveLocation>")

        #preparacion
        if not os.path.exists(self.save_loc):
            os.mkdir(self.save_loc)
        if not os.path.exists(self.save_loc + "/" + self.doc2vec_folder):
            os.mkdir(self.save_loc + "/" + self.doc2vec_folder)
        if not os.path.exists(self.save_loc + "/" + self.classification_folder):
            os.mkdir(self.save_loc + "/" + self.classification_folder)

        # primera fase de entrenamiento, D2V
        trd2v = ModelDoc2Vec()
        trd2v.setSaveLocation(self.save_loc + "/" + self.doc2vec_folder+ "/" +self.lang)
        lab = LabeledLineSentence(self.folder+"/"+self.lang)
        trd2v.train(lab)
        trd2v.verosimility(lab)
        trd2v = None
        #segunda fase de entrenamiento, clasificacion pura desde los vectores inferidos
        lab = LabeledLineSentence(self.folder + "/" + self.lang, multiTag=True)
        d2v = ModelDoc2Vec()
        d2v.setSaveLocation(self.save_loc + "/" + self.doc2vec_folder+ "/" +self.lang)
        d2v.load()

        trcl = ModelClassification()
        trcl.setDependenceModel(d2v)
        trcl.setSaveLocation(self.save_loc + "/" + self.classification_folder+ "/" +self.lang)
        trcl.train(lab)

    def load(self):
        """
        Load the meta-model, load doc2vec and the neural network for classification
        """
        #load DOC2VEC
        d2v = ModelDoc2Vec()
        d2v.setSaveLocation(self.save_loc + "/" + self.doc2vec_folder + "/" + self.lang)
        d2v.load()
        #load Class
        self.trcl = ModelClassification()
        self.trcl.setDependenceModel(d2v)
        self.trcl.setSaveLocation(self.save_loc + "/" + self.classification_folder + "/" + self.lang)
        self.trcl.load()

    def predict(self, text):
        """
        predict the tags associated to the text

        :param text: text for the predicction
        :return: a list of tags
        """
        if self.trcl == None:
            raise UnboundLocalError("Should have load the model")

        return self.trcl.predict(text)


    def test(self):
        """
        The error rate is error_count / tags_count
        error_count is the sum of tags not predicted

        :return: error Rate
        """
        lab = LabeledLineSentence(self.folder + "/" + self.lang+ "_test")
        error_count = 0
        tags_count = 0
        for labeled in lab:
            tags = {key: True for key in labeled.tags[1:]}
            text = labeled.words

            tags_pred = self.predict(text)
            for tag_pred in tags_pred:
                if tag_pred not in tags:
                    error_count += 1

            tags_count += len(tags_pred)

        return error_count / float(tags_count)










