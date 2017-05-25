ssp 5
ujp main
label_testing:
ssp 5
sep 1
ldc i 0
str i 0 0
retf
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 6
sep 1
ldc i 0
str i 0 0
mst 1
cup 0 label_testing
str i 0 5
retf
