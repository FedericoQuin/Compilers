ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 13
sep 2
ldc i 0
str i 0 0
main_for_0:
ldc b t
fjp main_for_0_false
ujp main_for_0
main_for_0_false:
ldc i 0
str i 0 5
ldc i 0
str i 0 6
main_for_1:
lod i 0 6
ldc i 5
les i
fjp main_for_1_false
ldc i 5
str i 0 7
lod i 0 6
ldc i 1
add i
str i 0 6
ujp main_for_1
main_for_1_false:
main_for_2:
lod i 0 5
ldc i 5
les i
fjp main_for_2_false
ldc i 6
str i 0 8
lod i 0 5
ldc i 1
add i
str i 0 5
ujp main_for_2
main_for_2_false:
ldc i 0
str i 0 9
main_for_3:
ldc b t
fjp main_for_3_false
ldc i 7
str i 0 10
lod i 0 9
ldc i 1
add i
str i 0 9
ujp main_for_3
main_for_3_false:
ldc i 0
str i 0 11
main_for_4:
lod i 0 11
ldc i 5
les i
fjp main_for_4_false
ldc i 8
str i 0 12
lod i 0 11
ldc i 1
add i
str i 0 11
ujp main_for_4
main_for_4_false:
retf
