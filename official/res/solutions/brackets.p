label_main:
ssp 12
sep wat? hoe moet ik dit nu weten?
ldc i 5
ldc i 4
add i
ldc i 3
mul i
str i 0 8
ldc i 3
ldc i 5
ldc i 4
add i
mul i
str i 0 8
ldc i 5
str i 0 12
ldc i 3
str i 0 16
main_while_0:
lod i 0 8
lod i 0 12
grt i
lod i 0 12
lod i 0 16
grt i
lod i 0 16
lod i 0 12
les i
or
not
and
fjp main_while_0_false
lod i 0 12
ldc i 1
add i
str i 0 12
ujp main_while_0
main_while_0_false:
ldc i 5
str i 0 12
main_while_1:
lod i 0 12
lod i 0 16
grt i
lod i 0 16
lod i 0 12
les i
or
lod i 0 8
lod i 0 12
grt i
and
fjp main_while_1_false
lod i 0 12
ldc i 1
add i
str i 0 12
ujp main_while_1
main_while_1_false:
retf
