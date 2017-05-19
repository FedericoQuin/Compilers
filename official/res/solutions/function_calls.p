label_getCookies:
ssp 0
sep wat? hoe moet ik dit nu weten?
ldc i 0
str i 0 0
retf
retf
label_getCookies2:
ssp 4
sep wat? hoe moet ik dit nu weten?
lod i 0 8
str i 0 0
retf
retf
label_getCookies3:
ssp 12
sep wat? hoe moet ik dit nu weten?
lod r 0 12
ldc r 5.0
equ r
fjp getCookies3_ifelse_0_false
lod i 0 16
str i 0 0
retf
ujp getCookies3_ifelse_0_end
getCookies3_ifelse_0_false:
lod i 0 16
ldc i 1
add i
str i 0 0
retf
getCookies3_ifelse_0_end:
retf
label_getOtherCookies:
ssp 12
sep wat? hoe moet ik dit nu weten?
ldc i 9001
str i 0 0
retf
retf
label_main:
ssp 12
sep wat? hoe moet ik dit nu weten?
ldc i 5
str i 0 8
mst 1
cup 0 getCookies
mst 1
lod i 0 8
cup 4 getCookies2
mst 1
ldc c 'a'
ldc r 2.9
ldc i 8
cup 12 getCookies3
ldc c 'a'
str c 0 12
ldc i 5
mst 1
lod i 0 8
lod c 0 12
ldc r 0.9
cup 12 getOtherCookies
add i
str i 0 16
retf
