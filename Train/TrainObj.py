import hashlib

class TrainObj(object):
    """
    Encapsulacion de objetos
    """
    def __init__(self, hbasedocumentid, text, lang, categories):
        super(TrainObj, self).__init__()
        self.HbaseDocumentId = hbasedocumentid
        self.categories = categories
        self.setText(text)
        self.setLang(lang)
        self.hashText = None

    def addCategory(self, category):
        self.categories.append(category)

    def getCategories(self):
        return self.categories

    def setText(self, text):
        self.text = text
        self.hashText = hashlib.sha256(self.text.encode('utf-8')).hexdigest()

    def getText(self):
        return self.text

    def setLang(self, lang):
        self.lang = lang

    def getLang(self):
        return self.lang

    def getHbaseDocumentId(self):
        return self.HbaseDocumentId

    def getHash(self):
        return self.hashText

    def __str__(self):
        str = "{id:%s,categories:%s}"%(self.HbaseDocumentId,self.categories)
        return str