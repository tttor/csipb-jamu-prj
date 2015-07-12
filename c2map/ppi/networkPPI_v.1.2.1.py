import networkx as nx
import xlwt as xl
import random


'''
 nama fungsi : gabung_2_fppi(ls_nm_file)
 7an         : menggabung dua file PPI 
 input       : list nama file PPI dan nama file PPI gabungan
 output      : ---
'''
def gabung_2_fppi(ls_nm_file):
    ff = open(ls_nm_file[2],'w')
    for i in range(0,len(ls_nm_file)-1):
        f = open(ls_nm_file[i])
        ln = f.readline()
        while ln:
            ff.write(ln)
            ln = f.readline()
        f.close()
    ff.close()


'''                  
 nama fungsi : fProt_to_lsProt(nm_fprot)
 7an         : memindahkan seed protein dari file --> list seed protein & list pasangan biner protein
 input       : nama file seed protein
 output      : list prot (lsProt)                : [p1, p2, p3, ..., pn]
'''
def fProt_to_lsProt(nm_fprot):
    f = open(nm_fprot)
    listProt = []
    sprot = f.readline()  # membaca line pertama dalam file
    while sprot:
        sprot = sprot.replace('\n','')
        listProt = listProt + [sprot]
        sprot = f.readline() # membaca line berikutnya dalam file
    return listProt

'''                  
 nama fungsi : lsProt_to_lsBProt(lsProt)
 7an         : membentuk pasangan biner protein dari list protein
 input       : list protein (lsProt)
 output      : list pasangan biner prot (lsBProt): [(p1,p2),(p1,p3),...,(p1,pn),...,(p5,p6),(p5,p7),...,(p5,pn),...,(pn-1,pn)]               
'''
def lsProt_to_lsBProt(lsProt):
    listBProt = []
    temp = '';
    for i in range(0,len(lsProt)):
        temp = lsProt[i]
        for j in range(i+1, len(lsProt)):
            listBProt = listBProt + [(temp,lsProt[j])]
    return listBProt


'''
 nama fungsi : fPPI_to_lsPPI(nm_fppi)
 7an         : memindahkan file interaksi biner protein yg diperoleh dari STRING.db atau HPRD --> list interaksi biner antar protein
 input       : nama file ppi
 output      : list PPI (lsPPI) : [('a','b'),('b','d'),...,('y','z')]
 peruntukan output : lsPPI : dipergunakan untuk membangun jaringan PPI 
'''
def fPPI_to_lsPPI(nm_fppi):
    f = open(nm_fppi)
    fileOk = True
    listPPI = [] # list interaksi biner antar protein
    bppi = f.readline()  # membaca line pertama interaksi biner protein (ppi) dlm file
    while bppi:
        bppi = bppi.replace('\n','')
        p = p1 = p2 = '' # p: protein, p1: protein1, p2: protein2
        for i in range(0,len(bppi)):
            ch = bppi[i]
            if ch != '\t':
                p = p + ch
            if ch == '\t':
                p1 = temp = p
                p = ''
            if i == len(bppi)-1:
                p2 = temp = p
                p = ''
        p1 = p1.replace('-','')
        p1 = p1.replace(' ','')
        p2 = p2.replace('-','')
        p2 = p2.replace(' ','')
        if (p1 != p2) and not((p1,p2) in listPPI) and not((p2,p1) in listPPI) and p1!= '' and p2!='' :
            listPPI = listPPI + [(p1,p2)]
        else:
            fileOk = False
        bppi = f.readline()
    f.close()
    if not fileOk:
        f = open(nm_fppi,'w')
        for i in range(0,len(listPPI)):
            dt = listPPI[i]
            f.write(dt[0]+'\t'+dt[1]+'\n')
        f.close()  
    return (listPPI)    


'''
 nama fungsi : empty_graph()
 7an         : menciptakan sebuah graph G yang masih kosong
 input       : ---
 output      : sebuah graph G kosong  
'''
def empty_graph():
    return nx.Graph()

'''    
 nama fungsi : const_network(dtlsPPI)
 7an         : menciptakan graph G kemudian membangun network G PPI dari sebuah list PPI : [(p1,p7),(p3,p6),(p10,p22),...]
 input       : sebuah list PPI : dtlsPPI : [(p1,p7),(p3,p6),(p10,p22),...]
 output      : sebuah network graph PPI : G  
 peruntukan output : G PPI: untuk dilakukan analisis topologi
'''
def const_network(lsPPI):
    # menciptakan empty graph G
    G = empty_graph() 
    # konstruksi network PPI dari sebuah list PPI [(p1,p7),(p3,p6),(p10,p22),...]
    G.add_edges_from(lsPPI)
    return G


'''
 nama fungsi : get_allshortespath(G, lsBProtAsal, tipe)
 7an         : mencari semua jalur terpendek dari pasangan biner protein asal
 input       : G: sebuah network yang terbentuk dari list PPI
               lsBProtAsal: list pasangan biner protein asal
               tipe == 1: mencari semua shortest_path default networkx
               tipe == 2: mencari semua shortest_path dengan algoritma dijstra
               tipe == 3: mencari semua shortest_path berdasarkan akumalasi nilai degree terbesar
                          dari semua alternatif jalur yang ditemukan untuk tiap pasangan biner protein asal
 output      : list shortest_path dari semua pasangan biner protein asal 
 peruntukan output : untuk membangun subnetwork PPI dari network PPI
'''
def get_allshortespath(G, lsBProtAsal, tipe):
    lsShortestPath = []
    ok = True
    if tipe == 1:
        for i in range(0,len(lsBProtAsal)):
            bpa = lsBProtAsal[i] # biner protein asal
            try:
                tempshortest_path = nx.shortest_path(G,bpa[0],bpa[1])
                lsShortestPath = lsShortestPath + [tempshortest_path]
            except:
                lsShortestPath = lsShortestPath + ['']
    elif tipe == 2:
        for i in range(0,len(lsBProtAsal)):
            bpa = lsBProtAsal[i] # biner protein asal
            try:
                tempshortest_path = nx.dijkstra_path(G,bpa[0],bpa[1])
                lsShortestPath = lsShortestPath + [tempshortest_path]
            except:
                lsShortestPath = lsShortestPath + ['']
    elif tipe == 3:
        for i in range(0,len(lsBProtAsal)):
            bpa = lsBProtAsal[i] # biner protein asal
            try:
                lsProt = G.nodes() # list semua node (protein) pada graph G
                protDegree = G.degree() # nilai degree semuan node (protein) pada graph G
                #print('bProtAsal : ',bpa[0],',',bpa[1])
                lsallshortest_paths = []
                lsAcDegree = []
                allshortest_paths = nx.all_shortest_paths(G,bpa[0],bpa[1])
                for path in allshortest_paths:
                    lsallshortest_paths = lsallshortest_paths + [path]
                    #print(path)
                    acDegree = 0
                    for k in range(0,len(path)):
                        acDegree = acDegree + protDegree[path[k]]
                    #print(acDegree)
                    lsAcDegree = lsAcDegree + [acDegree]
                #print(lsAcDegree)

                tempshortest_path = lsallshortest_paths[lsAcDegree.index(max(lsAcDegree))]
                lsShortestPath = lsShortestPath + [tempshortest_path]
            except:
                lsShortestPath = lsShortestPath + [[]]
    else:
        ok = False
    if ok:
        return lsShortestPath
    else:
        return 'Terjadi kesalahan tipe, pilih tipe : 1 / 2 / 3 ..!'


'''
 nama fungsi : shortetspath_to_lsPPI(lsShortestPath)
 7an         : convert all shortest_path menjadi lsit_PPI
 input       : list semua shortest_path dari sebuah jaringan (lsShortestPath)
 output      : sebuah list PPI (lsPPI)
'''
def shortetspath_to_lsPPI(lsShortestPath):
    listPPI = []
    for i in range(0,len(lsShortestPath)):
        path = lsShortestPath[i]
        for j in range(1,len(path)):
            tPPI1 = (path[j-1],path[j])
            tPPI2 = (path[j],path[j-1])
            if not(tPPI1 in listPPI) and not(tPPI2 in listPPI):
                listPPI = listPPI + [tPPI1]
    return listPPI
    

'''
 nama fungsi : lsProt_n_BC(tG)
 7an         : memdapatkan nilai BC dari semua node (protein) dalam graph tG 
 input       : tG : graph subnetwork
 output      : list Protein dan nilai Betweenness_Centrality tiap Protein (listProt_nBC) dari graph tG  
'''
def lsProt_n_BC(tG):
    listProt_nBC = []
    BCP = nx.betweenness_centrality(tG)
    ndProt = tG.nodes()
    for i in range(0,len(ndProt)):
        Prot = ndProt[i]
        bcValue = BCP[Prot]
        listProt_nBC = listProt_nBC + [(Prot,bcValue)]
    return listProt_nBC
'''
 nama fungsi : lsProt_n_BC005(lsProt_nBC)
 7an         : memdapatkan semua protein dan nilai BC >= 5%
 input       : lsProt_nBC : list protein dan nilai BC-nya "listProt_nBC"
 output      : list protein dan nilai BC >= 5% (listProt_nBC005) 
'''
def lsProt_n_BC005(lsProt_nBC):
    listProt_nBC005 = []
    for i in range(0,len(lsProt_nBC)):
        bcp = lsProt_nBC[i]
        if bcp[1] >= 0.0445:
            listProt_nBC005 = listProt_nBC005 + [bcp]
    return listProt_nBC005
'''
 nama fungsi : lsProt_with_BC005(lsProt_nBC005)
 7an         : memdapatkan protein-protein dengan nilai BC >= 5%
 input       : listProt_nBC005 : list nilai BC semua protein yang diperoleh dari fungsi "lsProt_n_BC(tG)"
 output      : list protein dengan nilai BC >= 5% (listProt_wBC005) 
'''
def lsProt_with_BC005(lsProt_nBC005):
    listProt_wBC005 = []
    for i in range(0,len(lsProt_nBC005)):
        prot = lsProt_nBC005[i][0]
        listProt_wBC005 = listProt_wBC005 + [prot]
    return listProt_wBC005
    

'''
 nama fungsi : CCProt(tG)
 7an         : memdapatkan nilai CC dari semua node (protein)
 input       : tG : graph subnetwork
 output      : list Closeness_Centrality tiap Protein (listCCProt) dari graph tG
'''
def CCProt(tG):
    listCCProt = []
    CCP = nx.closeness_centrality(tG)
    ndProt = tG.nodes()
    for i in range(0,len(ndProt)):
        Prot = ndProt[i]
        ccValue = CCP[Prot]
        listCCProt = listCCProt + [(Prot,ccValue)]
    return listCCProt


'''
 nama fungsi : listDt_to_file(listDt, nmfile)
 7an         : memdapatkan nilai CC dari semua node (protein)
 input       : tG : graph subnetwork
 output      : list Closeness_Centrality tiap Protein (listCCProt) dari graph tG
'''
def listDt_to_file(listDt, nmfile):
    nmfile = nmfile + '.txt'
    f = open(nmfile,'w')
    for i in range(0,len(listDt)):
        tupl = listDt[i]
        item1 = str(tupl[0])
        item2 = str(tupl[1])
        f.write(item1+'\t'+item2+'\n')
    f.close()



'''
'''
def listDt_to_fExcel(listDt, sheet, nm_file):
    #nm_file = nm_file + '.xls' 
    wb = xl.Workbook()
    ws = wb.add_sheet(sheet)
    for i in range(0,len(listDt)):
        tupl = listDt[i]
        ws.write(i,0,tupl[0])
        ws.write(i,1,tupl[1])
    wb.save(nm_file)

'''
'''
def list_protOmit(lsProt,centerProt,n_ofOmitted,n_ofCombination):
    lsP = [] #list protein tanpa protein center
    for i in range(0,len(lsProt)):
        if lsProt[i] != centerProt:
            lsP = lsP + [lsProt[i]]

    protOmit = []
    for i in range(0,n_ofOmitted):
        if i == 0:
            for j in range(0,len(lsProt)):
                protOmit = protOmit + [[lsProt[j]]]
        elif i == 1:
            for j in range(0,len(lsP)):
                protOmit = protOmit + [[centerProt,lsP[j]]]
        else:
            c = 0
            while c < n_ofCombination:
                k = random.sample(lsP,i)
                k = [centerProt] + k
                pjlsP = 1
                ada = False
                while (not ada and (pjlsP <= len(protOmit))):
                    t = protOmit[pjlsP-1]
                    if len(t) == len(k):
                        pjt = 1
                        sama = True
                        while sama and pjt <= lent(t):
                            sama = not k[pjt-1] in t
                            pjt = pjt + 1
                        ada = sama
                    pjlsP = pjlsP + 1
                if not ada:
                    c = c + 1
                    protOmit = protOmit + [k]
    return protOmit


    
'''
 Proses_0 = G0 
'''
folder = 'D:/Syaif/program/dtFromSTRING/fHasil/G0/'                         
lsProtAsal = fProt_to_lsProt('D:/Syaif/program/dtFromSTRING/_dtgen.txt')
lsBProtAsal = lsProt_to_lsBProt(lsProtAsal)

lsPPI = fPPI_to_lsPPI('D:/Syaif/program/dtFromSTRING/_fPPI_fromSTRING.txt')
G0 = const_network(lsPPI) # network PPI
lsAllShortestPath = get_allshortespath(G0, lsBProtAsal, 3)
lsPPI_dr_allSPath = shortetspath_to_lsPPI(lsAllShortestPath)
#listDt_to_file(lsPPI_dr_allSPath, 'D:/Syaif/program/dtFromSTRING/fHasil/G0/_fPPI_G0_1_subnetwork.txt')
listDt_to_fExcel(lsPPI_dr_allSPath, '_fPPI_G0_subnet', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_PPI_subnet.xls')

G0_1 = const_network(lsPPI_dr_allSPath) # subnetwork PPI
lsProt_nCC_subnet = sorted(CCProt(G0_1), key=lambda tup: tup[1], reverse=True)
#listDt_to_file(lsProt_nCC_subnet,'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_1_Prot_nCC_subnet.txt')
listDt_to_fExcel(lsProt_nCC_subnet, '_Prot_nCC_G0_subnet', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_Prot_nCC_subnet.xls')

lsProt_nBC_subnet = sorted(lsProt_n_BC(G0_1), key=lambda tup: tup[1], reverse=True)
#listDt_to_file(lsProt_nBC_subnet,'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_1_Prot_nBC_subnet.txt')
listDt_to_fExcel(lsProt_nBC_subnet, '_Prot_nBC_G0_subnet', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_Prot_nBC_subnet.xls')
lsProt_nBC005_subnet = lsProt_n_BC005(lsProt_nBC_subnet)
#listDt_to_file(lsProt_nBC005_subnet,'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_1_Prot_nBC005_subnet.txt')
listDt_to_fExcel(lsProt_nBC005_subnet, '_Prot_nBC005_G0_subnet', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_Prot_nBC005_subnet.xls')
lsProt_wBC005_subnet = lsProt_with_BC005(lsProt_nBC005_subnet)
lsBProt_wBC005_subnet = lsProt_to_lsBProt(lsProt_wBC005_subnet)

lsAllShortestPath_wBC005_subnet = get_allshortespath(G0_1,lsBProt_wBC005_subnet,3)
lsPPI_dr_allSPath_wBC005_subnet = shortetspath_to_lsPPI(lsAllShortestPath_wBC005_subnet)
#listDt_to_file(lsPPI_dr_allSPath_wBC005_subnet,'D:/Syaif/program/dtFromSTRING/fHasil/G0/_fPPI_G0_1_penyangga.txt')
listDt_to_fExcel(lsPPI_dr_allSPath_wBC005_subnet, '_fPPI_G0_penyangga', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_PPI_penyangga.xls')


G0_2 = const_network(lsPPI_dr_allSPath_wBC005_subnet) # jaringan penyanggah
lsProt_nBC_penyangga = sorted(lsProt_n_BC(G0_2), key=lambda tup: tup[1], reverse=True)
listDt_to_fExcel(lsProt_nBC_penyangga, '_Prot_nBC_G0_penyangga', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_Prot_nBC_penyangga.xls')
lsProt_nCC_penyangga = sorted(CCProt(G0_2), key=lambda tup: tup[1], reverse=True)
listDt_to_fExcel(lsProt_nCC_penyangga, '_Prot_nCC_G0_penyangga', 'D:/Syaif/program/dtFromSTRING/fHasil/G0/G0_Prot_nCC_penyangga.xls')

