label_testing:
ssp 6
sep wat? hoe moet ik dit nu weten?
lod i 0 5
ldc i 5
sto i
retp
retp
label_main:
ssp 5
sep wat? hoe moet ik dit nu weten?
ldc i 10
str i 0 5
mst 1
lda i 0 5
cup 1 testing
retf
