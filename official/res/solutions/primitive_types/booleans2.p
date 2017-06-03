ssp 5
ujp main
label_testing:
ssp 6
sep 1
ldc b f
str b 0 0
lod a 0 5
ldc b f
sto b
lod a 0 5
ind b
not
str b 0 0
retf
retf
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 8
sep 1
ldc i 0
str i 0 0
ldc i 5
str i 0 5
lod i 0 5
ldc i 5
geq i
str b 0 6
mst 1
lda 0 6
cup 1 label_testing
str b 0 7
lod b 0 6
ldc b f
equ b
fjp main_ifelse_0_false
lod i 0 5
str i 0 0
retf
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
ldc i 3
str i 0 0
retf
retf
