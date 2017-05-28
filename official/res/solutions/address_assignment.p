ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 18
sep 3
ldc i 0
str i 0 0
ldc i 5
str i 0 5
lda 0 5
str a 0 6
lda 0 8
str a 0 7
ldc i 0
str i 0 8
ldc i 0
str i 0 9
ldc i 0
str i 0 10
ldc i 0
str i 0 11
ldc i 0
str i 0 12
ldc i 0
str i 0 13
ldc i 0
str i 0 14
ldc i 0
str i 0 15
ldc i 0
str i 0 16
ldc i 0
str i 0 17
lod a 0 7
ldc i 5
ixa 1
str a 0 6
retf
