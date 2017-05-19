label_main:
ssp 64
sep wat? hoe moet ik dit nu weten?
ldc i 0
str i 0 16
ldc i 0
str i 0 20
lod i 0 16
ldc i 5
les i
not
lod i 0 20
ldc i 6
equ i
and
fjp main_ifelse_0_false
ujp main_ifelse_0_end
main_ifelse_0_false:
main_ifelse_0_end:
lod i 0 16
ldc i 5
leq i
lod i 0 20
ldc i 6
equ i
or
fjp main_ifelse_1_false
ujp main_ifelse_1_end
main_ifelse_1_false:
main_ifelse_1_end:
lod i 0 16
ldc i 5
grt i
lod i 0 20
ldc i 6
equ i
and
fjp main_ifelse_2_false
ujp main_ifelse_2_end
main_ifelse_2_false:
main_ifelse_2_end:
lod i 0 16
ldc i 5
geq i
lod i 0 20
ldc i 6
equ i
not
or
fjp main_ifelse_3_false
ujp main_ifelse_3_end
main_ifelse_3_false:
main_ifelse_3_end:
ldc i 5
str i 0 60
lod i 0 16
ldc i 5
equ i
lod i 0 20
ldc i 6
equ i
not
or
fjp main_ifelse_4_false
ujp main_ifelse_4_end
main_ifelse_4_false:
lod i 0 16
ldc i 8
geq i
fjp main_ifelse_5_false
ldc i 10
str i 0 68
ujp main_ifelse_5_end
main_ifelse_5_false:
main_ifelse_5_end:
main_ifelse_4_end:
retf
