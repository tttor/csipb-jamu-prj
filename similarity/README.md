# similarity _aka_ kernel

## Convention
* self-similarity is **not** inserted in the database,
  it is always assumed to equal 1.0
* similarity not found in the database is assumed to equal 0.0,
  **except** self-similarity

## Integration of multiple kernels
* STITCH's formulas: $CS_{ij} = 1 - \prod_n (1 - cs_{ij}^{(n)})$.
  * Liu, H. (2015)
