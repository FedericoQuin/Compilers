label_testing:
ssp 4
sep wat? hoe moet ik dit nu weten?
lod i 0 8
str i 0 0
retf
retf
label_main:
ssp 8
sep wat? hoe moet ik dit nu weten?
mst 1
ldc i 5
cup 4 testing
str i 0 8
lod i 0 8
ldc i 5
equ i
fjp main_ifelse_0_false
ldc i 10
str i 1 12
lod i 1 12
str i 0 0
retf
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
retf
