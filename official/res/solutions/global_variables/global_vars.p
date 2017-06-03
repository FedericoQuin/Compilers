ssp 7
ldc i 0
str i 0 5
ldc r 4.96
str r 0 6
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 6
sep 1
ldc i 0
str i 0 0
ldc i 6
str i 0 5
retf
label_testFunction:
ssp 6
sep 1
ldc r 0.0
str r 0 0
ldc r 2.98
str r 1 6
retf
