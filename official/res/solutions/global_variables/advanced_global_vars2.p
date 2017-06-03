ssp 6
ldc i 10
str i 0 5
ujp main
label_getAddressA:
ssp 5
sep 1
ldc a 0
str a 0 0
lda 1 5
str a 0 0
retf
retf
label_manipGlobalVariable:
ssp 6
sep 1
mst 1
cup 0 label_getAddressA
lod i 0 5
sto i
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 5
sep 2
ldc i 0
str i 0 0
mst 1
ldc i 23
cup 1 label_manipGlobalVariable
ssp 5
lod i 1 5
str i 0 0
retf
retf
