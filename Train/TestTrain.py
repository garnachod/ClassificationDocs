from DBWrapper.I3Queries import I3Queries
from TrainObjs import TrainObjs
from MetaModel import MetaModel
import os

if __name__ == '__main__':
    Qs = I3Queries()
    trs = Qs.getTrainFiles()
    objs = TrainObjs()
    for tr in trs:
        objs.pushTrainObj(tr)

    objs.cleanAll()
    if not os.path.exists("test"):
        os.mkdir("test")

    with open("test/langs", "w") as fout:
        objs.saveFilesByLang("test", fout)

    mt = MetaModel("es", "test")
    mt.setSaveLocation("test")
    mt.train()
