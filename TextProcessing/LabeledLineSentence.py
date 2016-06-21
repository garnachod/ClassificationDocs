from gensim.models.doc2vec import TaggedDocument
from collections import deque
import fileinput

class LabeledLineSentence:
    """
        ides:
            Number
            String
    """

    def __init__(self, source, ides="String", multiTag=False):
        """

        :param source: localizacion en disco que se leera
        :param ides: puede ser un valor Number o String,
        :param multiTag: Multietiqueta, por defecto coge la primera, seapradas por espacios
        """
        self.source = source
        self.sentences = None
        self.ides = ides
        self.doc2vec = None
        # self.fileOpened = utils.smart_open(self.source)
        self.fileOpened = fileinput.input([self.source])
        self.dq = deque(maxlen=10000)
        self.finishedDoc = False
        self.multiTag = multiTag

    def __iter__(self):
        return self

    def reloadDoc(self):
        self.finishedDoc = False
        self.fileOpened.close()
        self.fileOpened = fileinput.input([self.source])

    def next(self):
        if len(self.dq) == 0:
            # Load data
            self.loadData()
            if len(self.dq) == 0:
                #
                raise StopIteration()
            else:
                return self.dq.pop()
        else:
            # pop out an element at from the right of the queue
            return self.dq.pop()

    def loadData(self):
        if self.finishedDoc == True:
            return

        while len(self.dq) < self.dq.maxlen:
            last_identif = 0
            try:
                line = self.fileOpened.readline()
            except:
                self.finishedDoc = True
                print "Documento terminado"
                break

            if len(line) < 1:
                self.finishedDoc = True
                print "Documento terminado"
                break

            if self.ides == "Number":
                last_identif = long(line)
            else:
                ides = line.replace("\n", "").split(" ")
                if self.multiTag == False:
                    last_identif = [str(ides[0])]
                else:
                    last_identif = [str(elem) for elem in ides]

            line = self.fileOpened.readline()

            palabras = line.split()
            palabras_clean = []
            for palabra in palabras:
                if len(palabra) > 1:
                    palabras_clean.append(palabra)

            if len(palabras_clean) > 0:
                self.dq.appendleft(TaggedDocument(palabras_clean, last_identif))