ssp 5
ujp main
label_testing:
ssp 6
sep 1
lod a 0 5
ldc i 5
sto i
retp
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 6
sep 2
ldc i 0
str i 0 0
ldc i 10
str i 0 5
mst 1
lda 0 5
cup 1 label_testing
ssp 6
retf
