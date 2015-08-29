Construct_ConnectivityMap
http://bio.informatics.iupui.edu/cmaps/
http://rdc02.uits.iu.edu:7777/pls/apex/f?p=208:11:897863672555780::NO

GOAL:
Construct C­Map by connecting each possible pair of 
significant proteins and enriched chemical/drugs.


INPUT:
(1) Significant proteins in disease­specific network;
(2) Enriched drugs in retrieved texts

More:
Construct Connectivity Map Component takes two inputs, 
(1) disease­related protein list from protein interaction network analysis and 
(2) enriched drug list from text retrieval and extraction analysis, and 
outputs a connectivity map.

We assign an association score for each possible pair of ranked proteins 
$\{ p_1, p_2, ..., p_k \}$ and enriched drugs $\{ d_1, d_2, ..., d_g \}$,
using a regularized log­-odds function:

\begin{equation}
	score_{pd} = ln (df_{pd} \times N + \lambda) - ln (df_p \times df_d + \lambda)
\end{equation}

\begin{itemize}
\item
$df_p$ and $df_d$ are the total number of documents in which protein $p$ and drug $d$ are mentioned, respectively, 

\item
df_{pd} is the total number of documents in which protein $p$ and drug $d$ are co­mentioned in the same document.

\item 
$N$ is the size of the entire PubMed abstract collection.

\item
$\lamda$ is a small constant ($λ =1$ here) introduced to avoid out­of­bound errors if any of $df_p$, $df_d$, or $df_{pd}$ values are 0.

\item 
The resulting $score_{pd}$ is positive for when the protein­drug pair is over­represented and negative when the protein­drug is under­ represented.
The higher the $score_{pd}$ is, the more significant the over­representation of connection becomes. 
\end{itemize}

Totally, $k \times g$ connection scores are calculated to built C­Map in which statistical data cleaning and filtering and clustering analysis are applied.
The clustered disease­ specific C­Map contains novel knowledge (hypothesis), subject to validation.

===
Text(Literature)-mining

http://stackoverflow.com/questions/5410151/download-pubmed-abstracts-in-java
http://stackoverflow.com/questions/17409107/obtaining-data-from-pubmed-using-python
http://stackoverflow.com/questions/25740582/script-for-downloading-medline-abstracts-with-pmid
http://biology.stackexchange.com/questions/21404/how-can-i-text-mine-full-text-articles-from-pubmed
http://www.ncbi.nlm.nih.gov/books/NBK179288/

1) the protein list to search for in abstracts
2) the compound list to search for in abstracts

Extracts
Medicinal plant
Natural products
Bioactivity
Bioassay
Drugs
Diabetes mellitus  + natural products
Dm + extracts