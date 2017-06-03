ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 17
sep 3
ldc i 0
str i 0 0
lda 0 7
str a 0 5
ldc a 0
str a 0 7
ldc a 0
str a 0 8
ldc a 0
str a 0 9
ldc a 0
str a 0 10
ldc a 0
str a 0 11
ldc a 0
str a 0 12
ldc a 0
str a 0 13
ldc a 0
str a 0 14
ldc a 0
str a 0 15
ldc a 0
str a 0 16
ldc i 20
str i 0 6
lod a 0 5
ldc i 5
ixa 1
lda 0 6
sto a
lod a 0 5
ldc i 5
ixa 1
ind a
ldc i 25
sto i
ldc c 'N'
out c
ldc c 'e'
out c
ldc c 'w'
out c
ldc c ' '
out c
ldc c 'v'
out c
ldc c 'a'
out c
ldc c 'l'
out c
ldc c 'u'
out c
ldc c 'e'
out c
ldc c ' '
out c
ldc c 'f'
out c
ldc c 'o'
out c
ldc c 'r'
out c
ldc c ' '
out c
ldc c 'b'
out c
ldc c ':'
out c
ldc c ' '
out c
lod i 0 6
out i
ldc c '.'
out c
ldc c '\n'
out c
retf
