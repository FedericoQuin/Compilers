label_main:
ssp 32
sep wat? hoe moet ik dit nu weten?
main_for_0:
ldc b true
fjp main_for_0_false
ujp main_for_0
main_for_0_false:
ldc i 0
str i 0 8
ldc i 0
str i 0 12
main_for_1:
lod i 0 12
ldc i 5
les i
fjp main_for_1_false
ldc i 5
str i 0 16
lod i 0 12
ldc i 1
add i
str i 0 12
ujp main_for_1
main_for_1_false:
main_for_2:
lod i 0 8
ldc i 5
les i
fjp main_for_2_false
ldc i 6
str i 0 20
lod i 0 8
ldc i 1
add i
str i 0 8
ujp main_for_2
main_for_2_false:
ldc i 0
str i 0 24
main_for_3:
ldc b true
fjp main_for_3_false
ldc i 7
str i 0 28
lod i 0 24
ldc i 1
add i
str i 0 24
ujp main_for_3
main_for_3_false:
ldc i 0
str i 0 32
main_for_4:
lod i 0 32
ldc i 5
les i
fjp main_for_4_false
ldc i 8
str i 0 36
lod i 0 32
ldc i 1
add i
str i 0 32
ujp main_for_4
main_for_4_false:
retf
