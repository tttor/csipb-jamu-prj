import gc

a = {1:2,3:4}
del a[1]

print a

collected = gc.collect()
print "Garbage collector: collected %d objects." % (collected)