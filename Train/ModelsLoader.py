from MetaModel import MetaModel
from Config.Conf import Conf

class ModelsLoader(object):
    def __init__(self):
        self.langs = {}
        self.folder = Conf().getModelSave()
        self.load()

    def load(self):
        with open(self.folder + "/langs", "r") as fin:
            for line in fin:
                self.langs[line.replace("\n", "")] = None

    def __getitem__(self, key):
        if key not in self.langs:
            raise UnboundLocalError("lang not trained")

        if self.langs[key] == None:
            self.langs[key] = MetaModel(key, self.folder)
            self.langs[key].setSaveLocation(self.folder)
            self.langs[key].load()

        return self.langs[key]


if __name__ == '__main__':
    """
        Test ModelsLoader
    """
    m = ModelsLoader()
    print m["es"]