ssp 20
lda 0 10
str a 0 5
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
lda 0 15
str a 0 6
ldc i 0
str i 0 15
ldc i 0
str i 0 16
ldc i 0
str i 0 17
ldc i 0
str i 0 18
ldc i 0
str i 0 19
ldc i 5
str i 0 7
lod a 0 6
ldc i 1
ixa 1
ind i
lod i 0 7
add i
str i 0 8
mst 0
cup 0 label_modifyGlobal
str i 0 9
ujp main
label_modifyGlobal:
ssp 5
sep 4
ldc i 0
str i 0 0
lod a 1 6
ldc i 1
ixa 1
ldc i 3
sto i
lod i 1 8
ldc i 50
add i
lod a 1 6
ldc i 1
ixa 1
ind i
add i
str i 1 8
ldc i 0
str i 0 0
retf
retf
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 5
sep 1
ldc i 0
str i 0 0
lod i 1 8
str i 0 0
retf
retf
