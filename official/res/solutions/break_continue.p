ssp 5
ujp main
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 7
sep 2
ldc i 0
str i 0 0
main_for_0:
ldc b t
fjp main_for_0_false
ujp main_for_0_false
ujp main_for_0
main_for_0_false:
ldc i 5
str i 0 5
main_while_1:
lod i 0 5
ldc i 0
grt i
fjp main_while_1_false
lod i 0 5
ldc i 0
grt i
fjp main_ifelse_2_false
lod i 0 5
ldc i 1
sub i
str i 0 5
ujp main_while_1
ujp main_ifelse_2_end
main_ifelse_2_false:
main_ifelse_2_end:
ldc i 5
str i 0 6
ujp main_while_1
main_while_1_false:
retf
