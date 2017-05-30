ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 11
sep 3
ldc i 0
str i 0 0
lda 0 6
str a 0 5
ldc c 'a'
str c 0 6
ldc c 'a'
str c 0 7
ldc c 'a'
str c 0 8
ldc c 'a'
str c 0 9
ldc c 'a'
str c 0 10
lod a 0 5
ldc i 0
ixa 1
in c
sto c
lod a 0 5
ldc i 1
ixa 1
in c
sto c
lod a 0 5
ldc i 2
ixa 1
in c
sto c
lod a 0 5
ldc i 3
ixa 1
in c
sto c
lod a 0 5
ldc i 4
ixa 1
in c
sto c
retf
