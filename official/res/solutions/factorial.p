ssp 5
ujp main
label_fac_rec:
ssp 6
sep 2
ldc i 0
str i 0 0
lod i 0 5
ldc i 0
equ i
fjp fac_rec_ifelse_0_false
ldc i 1
str i 0 0
retf
ujp fac_rec_ifelse_0_end
fac_rec_ifelse_0_false:
fac_rec_ifelse_0_end:
lod i 0 5
mst 1
lod i 0 5
ldc i 1
sub i
cup 1 label_fac_rec
mul i
str i 0 0
retf
retf
label_fac_iter:
ssp 8
sep 2
ldc i 0
str i 0 0
ldc i 1
str i 0 6
ldc i 1
str i 0 7
fac_iter_for_1:
lod i 0 7
lod i 0 5
leq i
fjp fac_iter_for_1_false
lod i 0 6
lod i 0 7
mul i
str i 0 6
lod i 0 7
ldc i 1
add i
str i 0 7
ujp fac_iter_for_1
fac_iter_for_1_false:
lod i 0 6
str i 0 0
retf
retf
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 6
sep 1
ldc i 0
str i 0 0
ldc i 0
str i 0 5
ldc c 'E'
out c
ldc c 'n'
out c
ldc c 't'
out c
ldc c 'e'
out c
ldc c 'r'
out c
ldc c ' '
out c
ldc c 'f'
out c
ldc c 'a'
out c
ldc c 'c'
out c
ldc c 't'
out c
ldc c 'o'
out c
ldc c 'r'
out c
ldc c 'i'
out c
ldc c 'a'
out c
ldc c 'l'
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
ldc c ':'
out c
ldc c ' '
out c
in i
str i 0 5
ldc c '\n'
out c
ldc c '\n'
out c
ldc c 'F'
out c
ldc c 'a'
out c
ldc c 'c'
out c
ldc c 't'
out c
ldc c 'o'
out c
ldc c 'r'
out c
ldc c 'i'
out c
ldc c 'a'
out c
ldc c 'l'
out c
ldc c ' '
out c
ldc c 'r'
out c
ldc c 'e'
out c
ldc c 't'
out c
ldc c 'u'
out c
ldc c 'r'
out c
ldc c 'n'
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
ldc c '('
out c
ldc c 'r'
out c
ldc c 'e'
out c
ldc c 'c'
out c
ldc c 'u'
out c
ldc c 'r'
out c
ldc c 's'
out c
ldc c 'i'
out c
ldc c 'v'
out c
ldc c 'e'
out c
ldc c ')'
out c
ldc c ':'
out c
ldc c ' '
out c
mst 1
lod i 0 5
cup 1 label_fac_rec
out i
ldc c '.'
out c
ldc c '\n'
out c
ldc c 'F'
out c
ldc c 'a'
out c
ldc c 'c'
out c
ldc c 't'
out c
ldc c 'o'
out c
ldc c 'r'
out c
ldc c 'i'
out c
ldc c 'a'
out c
ldc c 'l'
out c
ldc c ' '
out c
ldc c 'r'
out c
ldc c 'e'
out c
ldc c 't'
out c
ldc c 'u'
out c
ldc c 'r'
out c
ldc c 'n'
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
ldc c '('
out c
ldc c 'i'
out c
ldc c 't'
out c
ldc c 'e'
out c
ldc c 'r'
out c
ldc c 'a'
out c
ldc c 't'
out c
ldc c 'i'
out c
ldc c 'v'
out c
ldc c 'e'
out c
ldc c ')'
out c
ldc c ':'
out c
ldc c ' '
out c
mst 1
lod i 0 5
cup 1 label_fac_iter
out i
ldc c '.'
out c
ldc c '\n'
out c
ldc i 0
str i 0 0
retf
retf
