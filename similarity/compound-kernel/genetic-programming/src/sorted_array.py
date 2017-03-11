import numpy as np

# x = np.matrix([[1, 2, 7],
#                [3, 4, 5],
#                [2, 4, 2]])
# print x
# print np.where( x == 4 )
dataset = 'zoo'
n_data = 10
MAX = False

savedir = '/home/banua/xprmt/xprmt-icacsis16/'

fname1 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixFitness-'+dataset+'-100-1.csv'
fname2 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixFitness-'+dataset+'-100-2.csv'

fname_acc1 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixAccuracy-'+dataset+'-100-1.csv'
fname_acc2 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixAccuracy-'+dataset+'-100-2.csv'

fname_ind1 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixFitnessInd-'+dataset+'-100-1.csv'
fname_ind2 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset+'/matrixFitnessInd-'+dataset+'-100-2.csv'

data1 = np.loadtxt(fname1,delimiter='\t')
data2 = np.loadtxt(fname2,delimiter='\t')

data_acc1 = np.loadtxt(fname_acc1,delimiter='\t')
data_acc2 = np.loadtxt(fname_acc2,delimiter='\t')

data_ind1 = np.loadtxt(fname_ind1,delimiter='\t', dtype=str)
data_ind2 = np.loadtxt(fname_ind2,delimiter='\t', dtype=str)


col_tres = data1.shape[1]

data = np.hstack([data1, data2])
data_acc = np.hstack([data_acc1, data_acc2])
data_ind = np.hstack([data_ind1, data_ind2])

sorted_data = np.round(sorted(np.sort(data, axis=None), reverse=MAX), 3)
unique_data = np.round(sorted(np.unique(sorted_data[0:n_data]), reverse=MAX), 3)

print unique_data[0:n_data]

idx_data = np.asarray([])

for i in unique_data :
    row_col = np.where(data == i)

    idx_data = np.hstack([idx_data, np.asarray(row_col)]) \
        if idx_data.size else np.asarray(row_col)

print 'idx_data', idx_data
print idx_data.shape

data_table = ()
for i, j in np.transpose(idx_data):
    ket = 'Scenario 1' if j < col_tres else 'Scenario 2'
    data_table += ( (data_ind[i, j], data[i, j], data_acc[i, j], ket) ),

print data_table


np.savetxt(savedir+dataset+'/'+dataset+'_table_'+str(MAX)+'.csv', np.asarray(data_table), fmt="%s", delimiter='\t')
