mst 0
cup 0 label_main
hlt
label_main:
ssp 8
sep 40
ldc i 5
ldc i 4
add i
ldc i 3
mul i
str i 0 5
ldc i 3
ldc i 5
ldc i 4
add i
mul i
str i 0 5
ldc i 5
str i 0 6
ldc i 3
str i 0 7
main_while_0:
lod i 0 5
lod i 0 6
grt i
lod i 0 6
lod i 0 7
grt i
lod i 0 7
lod i 0 6
les i
or
not
and
fjp main_while_0_false
lod i 0 6
ldc i 1
add i
str i 0 6
ujp main_while_0
main_while_0_false:
ldc i 5
str i 0 6
main_while_1:
lod i 0 6
lod i 0 7
grt i
lod i 0 7
lod i 0 6
les i
or
lod i 0 5
lod i 0 6
grt i
and
fjp main_while_1_false
lod i 0 6
ldc i 1
add i
str i 0 6
ujp main_while_1
main_while_1_false:
retf
