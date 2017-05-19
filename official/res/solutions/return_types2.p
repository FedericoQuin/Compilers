label_doNotReturn:
ssp 4
sep wat? hoe moet ik dit nu weten?
ldc i 5
str i 0 8
retp
label_main:
ssp 0
sep wat? hoe moet ik dit nu weten?
mst 1
ldc i 85
cup 4 doNotReturn
retf
