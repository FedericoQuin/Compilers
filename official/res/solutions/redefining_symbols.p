ssp 5
ujp main
label_testing:
ssp 6
sep 1
ldc i 0
str i 0 0
lod i 0 5
str i 0 0
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
mst 1
ldc i 5
cup 1 label_testing
str i 0 5
lod i 0 5
ldc i 5
equ i
fjp main_ifelse_0_false
ldc i 10
str i 0 6
lod i 0 6
str i 0 0
retf
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
retf
