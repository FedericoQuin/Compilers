mst 0
cup 0 label_main
hlt
label_getCookies:
ssp 5
sep 40
ldc i 0
str i 0 0
retf
retf
label_getCookies2:
ssp 6
sep 40
lod i 0 5
str i 0 0
retf
retf
label_getCookies3:
ssp 8
sep 40
lod r 0 6
ldc r 5.0
equ r
fjp getCookies3_ifelse_0_false
lod i 0 7
str i 0 0
retf
ujp getCookies3_ifelse_0_end
getCookies3_ifelse_0_false:
lod i 0 7
ldc i 1
add i
str i 0 0
retf
getCookies3_ifelse_0_end:
retf
label_getOtherCookies:
ssp 8
sep 40
ldc i 9001
str i 0 0
retf
retf
label_main:
ssp 8
sep 40
ldc i 5
str i 0 5
mst 1
cup 0 label_getCookies
mst 1
lod i 0 5
cup 1 label_getCookies2
mst 1
ldc c ''a''
ldc r 2.9
ldc i 8
cup 3 label_getCookies3
ldc c ''a''
str c 0 6
ldc i 5
mst 1
lod i 0 5
lod c 0 6
ldc r 0.9
cup 3 label_getOtherCookies
add i
str i 0 7
retf
