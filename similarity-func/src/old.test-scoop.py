from scoop import futures as fu

def compute(i):
    return i**2# + b[0] + b[1]

if __name__ == '__main__':
    a = [1,2,3]
    b = [10,20]

    c = list( fu.map(compute,a) )
    print c