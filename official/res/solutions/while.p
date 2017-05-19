label_main:
ssp 8
sep wat? hoe moet ik dit nu weten?
ldc i 5
str i 0 8
ldc i 0
str i 0 12
main_while_0:
lod i 0 12
ldc i 5
les i
fjp main_while_0_false
lod i 0 12
ldc i 1
add i
str i 0 12
ujp main_while_0
main_while_0_false:
main_while_1:
lod i 0 12
ldc i 0
grt i
fjp main_while_1_false
main_while_2:
lod i 0 8
ldc i 0
grt i
fjp main_while_2_false
lod i 0 8
ldc i 1
sub i
str i 0 8
lod i 0 12
ldc i 1
sub i
str i 0 12
ujp main_while_2
main_while_2_false:
ujp main_while_1
main_while_1_false:
retf
