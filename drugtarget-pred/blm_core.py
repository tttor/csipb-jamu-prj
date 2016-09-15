'''
BLM Framework by Yamanishi and Beakley
'''
class BLM:
    data = []

    def __init__(self, fpath):
        self._load(fpath)

    def run(self):
        print('hello world')

    def _load(self, fpath):
        content = []
        with open(fpath) as f:
            content = f.readlines()

        drugList = []
        proteinList = []
        for c in content:
            tmp = [i.strip() for i in c.split()]
            proteinList.append(tmp[0])
            drugList.append(tmp[1])

        drugSet = set(drugList)
        proteinSet = set(proteinList)

        data = [(i,j) for i in range(len(drugSet)) for j in range(len(proteinSet))]

        print(len(content))
        print(len(drugSet))
        print(len(proteinSet))
        print(len(data))
