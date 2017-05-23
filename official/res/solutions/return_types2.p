mst 0
cup 0 label_main
hlt
label_doNotReturn:
ssp 6
sep 40
ldc i 5
str i 0 5
retp
label_main:
ssp 5
sep 40
mst 1
ldc i 85
cup 1 label_doNotReturn
retf
