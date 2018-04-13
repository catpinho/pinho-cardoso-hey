# pinho-cardoso-hey
This repository includes some of the scripts used in Pinho, Cardoso and Hey (reference to be added upon publication)

summarizes_replicates.py takes a list of outputs of different clustering methods (BAPS, structure, DAPC - in the write.table R format) and calculates bootstrap support for previously defined clusters based on these replicates

supp.R is an R script that will run the DAPC algorithm in adegenet multiple times in an automated fashion, while keeping track of warnings raised by the program

calculates_rand_index.py is a function that calculates the adjustment between two classifications (e.g. one known and other inferred) based on Rand (1971) index. Useful to study simulated data.
