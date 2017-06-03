ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 10
sep 1
ldc i 0
str i 0 0
ldc i 5
str i 0 5
ldc i 10
str i 0 6
lod i 0 5
ldc i 5
equ i
lod i 0 6
ldc i 10
equ i
and
str b 0 7
lod i 0 5
ldc i 6
equ i
lod i 0 6
ldc i 10
equ i
and
str b 0 8
lod b 0 7
fjp main_ifelse_0_false
ldc i 20
str i 0 9
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
lod b 0 8
fjp main_ifelse_1_false
ldc i 20
str i 0 5
ujp main_ifelse_1_end
main_ifelse_1_false:
main_ifelse_1_end:
lod i 0 5
str i 0 0
retf
retf
