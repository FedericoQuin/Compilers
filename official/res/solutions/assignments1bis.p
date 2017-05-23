mst 0
ldc i 0
ldc c 'a'
cup 2 label_main
hlt
label_main:
ssp 9
sep 40
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
