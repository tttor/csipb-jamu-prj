import util
import fitness_func as ff

s = 'pDiv(mul(a, a), sub(d, d))'
# s = 'sub(pDiv(a, c), sub(a, c))'

s = util.expandFuncStr(s)
print s

f = ff.getZeroDivFitness(s)
print f
