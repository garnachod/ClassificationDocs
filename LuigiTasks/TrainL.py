from DBWrapper.I3Queries import I3Queries
from Train.TrainObjs import TrainObjs
from Config.Conf import Conf
from Train.MetaModel import MetaModel
from TextProcessing.LabeledLineSentence import LabeledLineSentence
import luigi
import os
from datetime import date
import shutil
import math

class trainByLang(luigi.Task):
    lang = luigi.Parameter()

    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/"+ self.lang + ".check")

    def run(self):
        mt = MetaModel(self.lang, self.save_path)
        mt.setSaveLocation(self.save_path)
        mt.train()

        with self.output().open("w") as fout:
            fout.write("OK")

class generateFilesTrain(luigi.Task):
    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/" + "langs")

    def run(self):
        Qs = I3Queries()
        trs = Qs.getTrainFiles()
        objs = TrainObjs()
        for tr in trs:
            objs.pushTrainObj(tr)

        objs.cleanAll()

        with self.output().open("w") as fout:
            objs.saveFilesByLang(self.save_path, fout)

class SplitSimple(luigi.Task):
    train = luigi.IntParameter(default=80)

    def requires(self):
        return generateFilesTrain()

    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/" + "langs_test")

    def run(self):
        with self.output().open("w") as fout_class:
            with self.input().open("r") as langs:
                for line in langs:
                    lang = line.replace("\n", "")
                    fout_class.write(line)
                    lines = []
                    with open(self.save_path + "/" + lang, "r") as fin:
                        for line in fin:
                            lines.append(line)

                    length = len(lines) * (self.train / 100.0)
                    length = int(math.ceil(length))
                    print length
                    if length % 2 != 0:
                        length += 1

                    with open(self.save_path + "/" + lang, "w") as fout:
                        for line in lines[:length]:
                            fout.write(line)

                    with open(self.save_path + "/" + lang + "_test", "w") as fout:
                        for line in lines[length:]:
                            fout.write(line)



class trainAllLangs(luigi.Task):
    """luigi --module LuigiTasks.TrainL trainAllLangs --local-scheduler"""
    def requires(self):
        return SplitSimple()

    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/" + "langs.OK")

    def run(self):
        with self.output().open("w") as check:
            with self.input().open("r") as langs:
                for line in langs:
                    lang = line.replace("\n", "")
                    check.write(line)
                    yield trainByLang(lang)



class train(luigi.Task):
    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/" + "none")

    def requires(self):
        return trainAllLangs()

    def run(self):
        self.save_path = Conf().getModelSaveTemp()
        self.final_path = Conf().getModelSave()
        now = date.today()
        self.oldPath = self.final_path + "_" + str(now.year) + str(now.month) + str(now.day)

        if os.path.exists(self.oldPath):
            shutil.rmtree(self.oldPath)

        if os.path.exists(self.final_path):
            os.rename(self.final_path, self.oldPath)

        os.rename(self.save_path, self.final_path)

class test(luigi.Task):
    def output(self):
        self.save_path = Conf().getModelSaveTemp()
        return luigi.LocalTarget(self.save_path + "/" + "langs.test")

    def run(self):
        with self.output().open("w") as fout_test:
            with self.input().open("r") as langs:
                for line in langs:
                    lang = line.replace("\n", "")
                    mt = MetaModel(lang, Conf().getModelSave())
                    mt.setSaveLocation(Conf().getModelSave())
                    mt.load()
                    error = mt.test()
                    fout_test.write(line + "\t-> Error: " + str(error) + "\n")


if __name__ == '__main__':
    trainAllLangs()


