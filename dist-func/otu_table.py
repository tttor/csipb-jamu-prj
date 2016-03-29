import numpy

__author__ = 'andpromobile'


# This file was inpired by bmeasures.r class in R which was created by Sony Hartono Wijaya <sonyhartono@gmail.com>


def mol_count(x, y):
    dx = x.shape
    dy = y.shape

    if dx[0] != dy[0]:
        print("Input memiliki jumlah baris yang berbeda \n")
    elif dx[1] != dy[1]:
        print("Input memiliki jumlah kolom yang  berbeda \n")
    else:
        print(" ")

    input = numpy.vstack((x, y))

    a = b = c = d = 0

    for i in range(0, dx[1]):
        k = input[0, i]
        l = input[1, i]

        if k == 1 and l == 1:
            a += 1
        elif k == 0 and l == 1:
            b += 1
        elif k == 1 and l == 0:
            c += 1
        else:  # k==0 and l==0
            d += 1

    otu_out = [a, b, c, d]

    return otu_out
