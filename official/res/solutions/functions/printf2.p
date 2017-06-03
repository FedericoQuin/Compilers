ssp 5
ujp main
label_printMyFloat:
ssp 6
sep 1
ldc c 'T'
out c
ldc c 'h'
out c
ldc c 'i'
out c
ldc c 's'
out c
ldc c ' '
out c
ldc c 'i'
out c
ldc c 's'
out c
ldc c ' '
out c
ldc c 'm'
out c
ldc c 'y'
out c
ldc c ' '
out c
ldc c 's'
out c
ldc c 'p'
out c
ldc c 'e'
out c
ldc c 'c'
out c
ldc c 'i'
out c
ldc c 'a'
out c
ldc c 'l'
out c
ldc c ' '
out c
ldc c 'f'
out c
ldc c 'l'
out c
ldc c 'o'
out c
ldc c 'a'
out c
ldc c 't'
out c
ldc c ':'
out c
ldc c ' '
out c
lod a 0 5
ind r
out r
ldc c '.'
out c
ldc c '\n'
out c
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 12
sep 3
ldc i 0
str i 0 0
lda 0 7
str a 0 5
ldc c ' '
str c 0 7
ldc c ' '
str c 0 8
ldc c ' '
str c 0 9
ldc c ' '
str c 0 10
ldc c ' '
str c 0 11
lod a 0 5
ldc i 0
ixa 1
ldc c 'H'
sto c
lod a 0 5
ldc i 1
ixa 1
ldc c 'e'
sto c
lod a 0 5
ldc i 2
ixa 1
ldc c 'l'
sto c
lod a 0 5
ldc i 3
ixa 1
ldc c 'l'
sto c
lod a 0 5
ldc i 4
ixa 1
ldc c 'o'
sto c
ldc c 'T'
out c
ldc c 'h'
out c
ldc c 'i'
out c
ldc c 's'
out c
ldc c ' '
out c
ldc c 'i'
out c
ldc c 's'
out c
ldc c ' '
out c
ldc c 'm'
out c
ldc c 'y'
out c
ldc c ' '
out c
ldc c 'w'
out c
ldc c 'o'
out c
ldc c 'r'
out c
ldc c 'd'
out c
ldc c ':'
out c
ldc c ' '
out c
lod a 0 5
ldc i 0
ixa 1
ind c
out c
lod a 0 5
ldc i 1
ixa 1
ind c
out c
lod a 0 5
ldc i 2
ixa 1
ind c
out c
lod a 0 5
ldc i 3
ixa 1
ind c
out c
lod a 0 5
ldc i 4
ixa 1
ind c
out c
ldc c '\n'
out c
ldc r 5.3684
str r 0 6
mst 1
lda 0 6
cup 1 label_printMyFloat
ssp 12
retf
