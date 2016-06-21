from DBWrapper.I3Queries import I3Queries
from TrainObjs import TrainObjs
from MetaModel import MetaModel
import os

if __name__ == '__main__':
    mt = MetaModel("es", "test")
    mt.setSaveLocation("test")
    mt.load()
    print "ignaci viv madr ignaci citr negr nad"
    print mt.predict("ignaci viv madr ignaci citr negr nad")