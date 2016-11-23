class DummyPredictor:
    def __init__(self):
        pass
        
    def predict(self, com, pro):
        predictorList = [self.predictorA, self.predictorB, self.predictorC]

        edgeList = []
        srcList = []
        for p in predictorList:
            edge, src = p(com,pro)
            edgeList.append(edge)
            srcList.append(src)

        weight = np.mean(edgeList)
        srcs = '+'.join(srcList)

        return (weight,srcs)

    def predictorA(self,com,pro):
        n = 1; p = 0.5; x = 1
        pred = np.random.binomial(n, p, x)[0]
        predName = 'predictorA'
        return (pred, predName)

    def predictorB(self,com,pro):
        n = 1; p = 0.5; x = 1
        pred = np.random.binomial(n, p, x)[0]
        predName = 'predictorB'
        return (pred, predName)

    def predictorC(self,com,pro):
        n = 1; p = 0.5; x = 1
        pred = np.random.binomial(n, p, x)[0]
        predName = 'predictorC'
        return (pred, predName)
