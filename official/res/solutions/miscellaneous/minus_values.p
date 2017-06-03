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
ldc i 5
neg i
str i 0 5
ldc r 2.5
neg r
str r 0 6
ldc r 0.968
neg r
str r 0 7
ldc i 5
neg i
ldc i 9
neg i
add i
str i 0 5
lod i 0 5
str i 0 0
retf
retf
