from TextProcessing.Cleaner import Cleaner


class TrainObjs(object):
    def __init__(self):
        super(TrainObjs, self).__init__()
        self.hashDictByLang = {}

    def pushTrainObj(self, trainobj):
        lang = trainobj.getLang()
        hash = trainobj.getHash()
        if lang not in self.hashDictByLang:
            self.hashDictByLang[lang] = {}

        if hash not in self.hashDictByLang[lang]:
            self.hashDictByLang[lang][hash] = trainobj

    def cleanAll(self):
        for lang in self.hashDictByLang:
            for hash in self.hashDictByLang[lang]:
                trainobj = self.hashDictByLang[lang][hash]
                text = Cleaner.clean(trainobj.getText(), trainobj.getLang())
                trainobj.setText(text)

    def saveFilesByLang(self, folderToSaveLangs, fileLangs):
        """
        Guarda los elementos de entrenamiento en un fichero por cada idioma
        :param folderToSaveLangs: carpeta donde se almacenaran los entrenamientos.
        :param fileLangs: Fichero abierto
        """
        for lang in self.hashDictByLang:
            fileLangs.write(lang + "\n")
            with open(folderToSaveLangs + "/" +lang, "w") as fout:
                for hash in self.hashDictByLang[lang]:
                    trainobj = self.hashDictByLang[lang][hash]
                    text = trainobj.getText()
                    id = trainobj.getHbaseDocumentId()
                    categories = trainobj.getCategories()
                    headTrainObj = str(id)
                    for cat in categories:
                        headTrainObj += " " + cat.replace(" ", "_")
                    fout.write(headTrainObj + "\n")
                    fout.write(text + "\n")
