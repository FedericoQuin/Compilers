label_main:
ssp 8
sep wat? hoe moet ik dit nu weten?
main_for_0:
ldc b true
fjp main_for_0_false
ujp main_for_0_false
ujp main_for_0
main_for_0_false:
ldc i 5
str i 0 8
main_while_1:
lod i 0 8
ldc i 0
grt i
fjp main_while_1_false
lod i 0 8
ldc i 0
grt i
fjp main_ifelse_2_false
lod i 0 8
ldc i 1
sub i
str i 0 8
ujp main_while_1
ujp main_ifelse_2_end
main_ifelse_2_false:
main_ifelse_2_end:
ldc i 5
str i 0 12
ujp main_while_1
main_while_1_false:
retf
