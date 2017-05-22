label_testing:
ssp 4
sep wat? hoe moet ik dit nu weten?
lod i 0 8
ldc i 5
sto i
retp
retp
label_main:
ssp 4
sep wat? hoe moet ik dit nu weten?
ldc i 10
str i 0 8
mst 1
lda i 0 8
cup 4 testing
retf
