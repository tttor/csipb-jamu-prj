import util
import numpy
from collections import defaultdict
from operator import itemgetter


def testKendal(toolbox, pop, data):
    valid = False

    # Take n reference from each class

    refIdxList = numpy.array([])
    remIdxList = numpy.array([])

    for i in range(data.keys):
        n_ref = int(0.1 * len(data.values()[i]))

        t = numpy.random.choice(len(data.values()[i]), size=(n_ref, 1), replace=False)
        ref_idx = list(t.flat)
        remaining_idx = [l for l in range(len(data.values()[i])) if l not in t]
        x = numpy.asarray(data.values()[i])

        if i == 0:
            refIdxList = x[ref_idx, :]
            remIdxList = x[remaining_idx, :]
        else:
            tmp = refIdxList
            refIdxList = numpy.vstack((tmp, x[ref_idx, :]))

            tmp = remIdxList
            remIdxList = numpy.vstack((tmp, x[remaining_idx, :]))

    # Calcullate similarity betwreen REM and REF
    recall_matrix = defaultdict(list)
    for individual in pop:
        func = toolbox.compile(expr=individual)

        similarity_pairwise = defaultdict(list)
        list_median = defaultdict(list)
        for ref in refIdxList:
            for rem in remIdxList:
                a = util.getFeatureA(ref[1:], rem[1:])
                b = util.getFeatureB(ref[1:], rem[1:])
                c = util.getFeatureC(ref[1:], rem[1:])

                flg = 1 if (ref[0] == rem[0]) else 0

                '''
                Similarity_pairwise : An defaultDict with 3 column.
                    1-st column indicate label.
                    2-nd column indicate pairwise in same group or not (1 = same class; 0 otherwise).
                    3-th column indicate similarity values.
                '''
                similarity_pairwise[str(ref[0])].append([rem[0], flg, func(a, b, c)])

            # Sorting similarity_pairwise with descending order based on similarities values.
            similarity_pairwise = numpy.matrix(sorted(similarity_pairwise, key=itemgetter(2), reverse=True))

            true_positive = 0
            # Count True Positive (TP)
            for k in range(0, int(len(similarity_pairwise) * 0.1)):
                true_positive += 1 if (similarity_pairwise[k, 0] == 1) else 0

            '''
            list_median : A dictionary which contains true positive value.
            '''
            list_median[str(ref[0])].append(true_positive)

    # Get Recall Matrix
        recall_matrix[str(individual)].append(list_median)

    # Get Ranking Matrix

    # Test significance

    # Infer
    if (signicant):
        valid = True
    return valid
