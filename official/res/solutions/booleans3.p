ssp 5
ujp main
label_test1:
ssp 5
sep 1
ldc b f
str b 0 0
ldc b t
str b 0 0
retf
retf
label_test2:
ssp 5
sep 1
ldc b f
str b 0 0
mst 1
cup 0 label_test1
not
str b 0 0
retf
retf
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
cup 0 label_test2
ldc b f
equ b
fjp main_ifelse_0_false
ldc i 10
str i 0 0
retf
ujp main_ifelse_0_end
main_ifelse_0_false:
ldc i 15
str i 0 0
retf
main_ifelse_0_end:
retf
