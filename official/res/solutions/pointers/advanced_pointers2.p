ssp 5
ujp main
label_doSomething:
ssp 6
sep 2
lod a 0 5
ind a
ldc i 100
sto i
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 7
sep 1
ldc i 0
str i 0 0
ldc a 0
str a 0 5
ldc i 20
str i 0 6
lda 0 6
str a 0 5
mst 1
lda 0 5
cup 1 label_doSomething
ssp 7
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
ldc c 's'
out c
ldc c 'h'
out c
ldc c 'o'
out c
ldc c 'u'
out c
ldc c 'l'
out c
ldc c 'd'
out c
ldc c ' '
out c
ldc c 'b'
out c
ldc c 'e'
out c
ldc c ' '
out c
ldc c '1'
out c
ldc c '0'
out c
ldc c '0'
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
