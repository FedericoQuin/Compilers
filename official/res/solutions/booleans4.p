ssp 5
ujp main
label_just__why____:
ssp 6
sep 1
ldc a 0
str a 0 0
lod a 0 5
ldc b t
sto b
lod a 0 5
str a 0 0
retf
retf
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 7
sep 2
ldc i 0
str i 0 0
ldc b f
str b 0 5
lda 0 5
str a 0 6
mst 1
lod a 0 6
cup 1 label_just__why____
str a 0 6
lod a 0 6
ind b
ldc b t
equ b
fjp main_ifelse_0_false
ldc i 3
str i 0 0
retf
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
ldc i 1
str i 0 0
retf
retf
