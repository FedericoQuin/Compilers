ssp 5
ujp main
main:
mst 0
ldc c ' '
ldc i 0
cup 2 label_main
hlt
label_main:
ssp 9
sep 3
ldc i 0
str i 0 0
ldc i 10
ldc i 5
add i
str i 0 7
ldc i 10
ldc i 5
mul i
lod i 0 7
add i
str i 0 8
retf
