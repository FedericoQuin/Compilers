ssp 5
ujp main
main:
mst 0
ldc c ' '
ldc r 0.0
ldc i 0
cup 3 label_main
hlt
label_main:
ssp 9
sep 1
ldc i 0
str i 0 0
ldc r 3.5
str r 0 8
retf
label_getThePointOfLife:
ssp 6
sep 2
lod i 0 5
ldc i 100
grt i
fjp getThePointOfLife_ifelse_0_false
retp
ujp getThePointOfLife_ifelse_0_end
getThePointOfLife_ifelse_0_false:
getThePointOfLife_while_1:
lod i 0 5
ldc i 100
les i
fjp getThePointOfLife_while_1_false
lod i 0 5
ldc i 1
add i
str i 0 5
ujp getThePointOfLife_while_1
getThePointOfLife_while_1_false:
retp
getThePointOfLife_ifelse_0_end:
retp
