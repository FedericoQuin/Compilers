ssp 5
ujp main
label_doNotReturn:
ssp 6
sep 1
ldc i 5
str i 0 5
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 5
sep 1
ldc i 0
str i 0 0
mst 1
ldc i 85
cup 1 label_doNotReturn
ssp 5
retf
