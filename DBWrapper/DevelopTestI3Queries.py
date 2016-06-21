from I3Queries import I3Queries

if __name__ == '__main__':
    query = I3Queries()
    trainObjs = query.getTrainFiles()
    for obj in trainObjs:
        print obj