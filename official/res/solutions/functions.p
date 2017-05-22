label_main:
ssp 16
sep wat? hoe moet ik dit nu weten?
ldc r 3.5
str r 0 20
retf
label_getThePointOfLife:
ssp 4
sep wat? hoe moet ik dit nu weten?
lod i 0 8
ldc i 100
grt i
fjp getThePointOfLife_ifelse_0_false
retp
ujp getThePointOfLife_ifelse_0_end
getThePointOfLife_ifelse_0_false:
getThePointOfLife_while_1:
lod i 0 8
ldc i 100
les i
fjp getThePointOfLife_while_1_false
lod i 0 8
ldc i 1
add i
str i 0 8
ujp getThePointOfLife_while_1
getThePointOfLife_while_1_false:
retp
getThePointOfLife_ifelse_0_end:
retp
