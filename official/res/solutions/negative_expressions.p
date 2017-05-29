ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 8
sep 1
ldc i 0
str i 0 0
ldc i 20
str i 0 5
lod i 0 5
neg i
ldc i 20
add i
str i 0 6
lod i 0 6
lod i 0 5
neg i
mul i
ldc i 50
neg i
add i
neg i
str i 0 7
lod i 0 5
lod i 0 6
neg i
sub i
str i 0 0
retf
retf
