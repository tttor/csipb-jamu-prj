title 		: Analisis Efek Sinergis Tanaman Obat untuk DIabetes Mellitus Tipe 2 Menggunakan Metode *Network Target-Based of Multicomponent Synergy*
author   	: Dhaba Widhikari
reference 	: Ramadhan GD. 2017

#Latar Belakang
Analisis efek sinergis dari kombinasi antar senyawa dilakukan dengan eksperimen biasanya membutuhkkan waktu yang lama, serta memakan biya dan etnaga yang besar. Sehingga diusulkan metode *Network Target-based Identification of Multicomponent Synergy (NIMS)* untuk menganalisis tingkat kesinergian antar komponen yang terdapat pada tanaman obat. Metode NIMS juga digunakan untuk memprioritaskan kominasi sinergis pada tanaman obat, sehingga didapat kombinasi komponen yang memiliki efek signifikan terhadap suatu penyakit.

#Tahapan
1. Praproses Data
Dilakukan reduksi terhadap data yang tidak diperlukan, antara lain data esnyawa atau protein yang tidak terdkomentasi pada suatu pangkalan data tertentu

2. Prediksi Jejaring Protein Target dengan Metode drugCIPHER
Zhao dan Li (2010) mengusulkan metode drugCIPHER untuk memprediksi profil protein target dari suatu senyawa. Prinsip metode drugCIPHER menggabungkan informasi kemiripan struktur kimia senyawa dengan interaksi protein pada tubuh manusia. Informasi kemiripan struktur kimiawi antar senyawa dihitung dengan menggunakan algoritmen *Fingerprint*. Algoritma *FIngerprint* mengukur kemiripan antara dua buah senyawa yang dihitung dengan menggunakan koefisien Tanimoto. Semakin besar maka semakin mirip dua buah senyawa tersebut.

Setelah itu dilakukan pencarian jarak terpendek dengan menggunakan *Bidirectional Search*. Profil protein target dari senyawa ditentukan dengan menghitung skor *concordance*. Profil protein target yang menyusun suatu jejaring didpat dari skor *concordance* yang tertinggi pada masing-masing senyawa aktif.

3. Prediksi Kekuatan Efek Sinergis dengan Metode NIMS
Metode NIMS diusulkan Li *et al.* (2010) untuk mengevaluasi efek sinergis antar senyawa pada tanaman. Konsep dasar NIMS yait melakukan pendekatan komputasi antar senyawa berdasarkan topologi jejaring protein target pada senyawa dan earing PPI (Syahrir 2015). Pendekatan komputasi NIMS dilakukan berdasarkan dua aspek, yaitu skor topologi dan skor agen. Skor topologi yaitu melihat kedekatan senyawa berdasarkan kedekatan protein penting masing-masing senyawa dalam jejaring protein target (Syahrir 2015). Menentukan kepentingannya menggunakan nilai *node importance* (IP(v), v = vertex/node). *Node dalam hal ini yaitu protein target. Nilai IP(v) didapat dengan mengintegrasikan tiga sentrais pada jearing, yaitu derajat (*degree*), keantaraan(*betweenness*), dan kedekatan (*closeness*) (Li *et al.* 2010)

Derajat (degree) didefinisikan sebagai jumlah interaksi/edge pada suatu node (Wasserman dan Faust 1994). Semakin besar nilai degree, maka semakin banyak tetangga yang berhubungan langsung dengan node tersebut.

Keantaraan (betweenness) adalah parameter untuk menghitung berapa kali sebuah node menjembatani sepanjang lintasan terpendek antar dua node lain. Betweenness didapat dari persamaan berikut:

Kedekatan (closeness) yaitu parameter sentralitas yang melihat seberapa dekat suatu node ke semua node yang ada pada jejaring (Wasserman dan Fraud 1994) diukur dengan panjang rata-rata jalur terpendek untuk mengakses seluruh node pada jejaring.

Skor agen digunakan untuk mengukur skor kesamaan dua senyawa berdasarkan fenotipe dari protein target. Agen-agen dalam hal ini senyawa, dengan mekanisme yang independen namun mengobat penyakit serupa akan lebih memungkinkan untuk menghasilkan efek sinergis (Li *et al.* 2010).

Kesamaan fenotipe didasarkan ada struktur *Human Phenotype Ontology* (HPO) yang berbentuk *Directed Acyclyc Graph* (DAG) (Robinson *et al.* 2008)

Metode NIMS digunakan untuk menghitung skor sinergi antar senyawa yang menarget protein dari penyakit. Langkah-langkah pengaplikasian NIMS adalah sebagai berikut:
A. Membuat jejaring topologi yang terdiri atas jejaring protein target dan jejaring PPI.
B. Menghitung tiga nilai sentralitas, yaitu degree, betweenness, dan closeness.
C. Menghitung nilai IP(v) dengan mengintegrasikan tiga nilai sentralitas.
D. Menghitung minimum shortest path antar protein target kombinasi senyawa.
E. Menghitung matriks skor topologi (TS).
F. Menghitung kesamaan fenotipe (PS).
G. Menghitung matriks skor agen (AS).


** NIMS
* Network target for screening synergistic drug combinations with application to traditional Chinese medicine (NIMS Theory)
	* Li, S. (2010)
* Herb Network Analysis for a Famous TCM Doctor’s Prescriptions on Treatment of Rheumatoid Arthritis
	* Li, Y. (2015)
* Network-based drug discovery by integrating systems biology and computational technologies
	* Leung, E. (2012)

hpo_imilarity dapat didownload di https://github.com/jeremymcrae/hpo_similarity
	pada directory hpo_similarity/hpo_similarity/data replace file hp.obo dengan file yang dapat diunduh di http://purl.obolibrary.org/obo/hp.obo