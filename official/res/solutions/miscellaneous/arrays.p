ssp 5
ujp main
label_doSomething:
ssp 6
sep 1
retp
retp
main:
mst 0
cup 0 label_main
hlt
label_main:
ssp 125
sep 5
ldc i 0
str i 0 0
lda 0 10
str a 0 5
ldc i 0
str i 0 10
ldc i 0
str i 0 11
ldc i 0
str i 0 12
ldc i 0
str i 0 13
ldc i 0
str i 0 14
ldc i 0
str i 0 15
ldc i 0
str i 0 16
ldc i 0
str i 0 17
ldc i 0
str i 0 18
ldc i 0
str i 0 19
ldc i 0
str i 0 6
main_for_0:
lod i 0 6
ldc i 10
les i
fjp main_for_0_false
lod a 0 5
lod i 0 6
ixa 1
lod i 0 6
sto i
lod i 0 6
ldc i 1
add i
str i 0 6
ujp main_for_0
main_for_0_false:
lda 0 20
str a 0 7
ldc c ' '
str c 0 20
ldc c ' '
str c 0 21
ldc c ' '
str c 0 22
ldc c ' '
str c 0 23
ldc c ' '
str c 0 24
ldc c ' '
str c 0 25
ldc c ' '
str c 0 26
ldc c ' '
str c 0 27
ldc c ' '
str c 0 28
ldc c ' '
str c 0 29
ldc c ' '
str c 0 30
ldc c ' '
str c 0 31
ldc c ' '
str c 0 32
ldc c ' '
str c 0 33
ldc c ' '
str c 0 34
ldc c ' '
str c 0 35
ldc c ' '
str c 0 36
ldc c ' '
str c 0 37
ldc c ' '
str c 0 38
ldc c ' '
str c 0 39
ldc c ' '
str c 0 40
ldc c ' '
str c 0 41
ldc c ' '
str c 0 42
ldc c ' '
str c 0 43
ldc c ' '
str c 0 44
ldc c ' '
str c 0 45
ldc c ' '
str c 0 46
ldc c ' '
str c 0 47
ldc c ' '
str c 0 48
ldc c ' '
str c 0 49
ldc c ' '
str c 0 50
ldc c ' '
str c 0 51
ldc c ' '
str c 0 52
ldc c ' '
str c 0 53
ldc c ' '
str c 0 54
ldc c ' '
str c 0 55
ldc c ' '
str c 0 56
ldc c ' '
str c 0 57
ldc c ' '
str c 0 58
ldc c ' '
str c 0 59
ldc c ' '
str c 0 60
ldc c ' '
str c 0 61
ldc c ' '
str c 0 62
ldc c ' '
str c 0 63
ldc c ' '
str c 0 64
ldc c ' '
str c 0 65
ldc c ' '
str c 0 66
ldc c ' '
str c 0 67
ldc c ' '
str c 0 68
ldc c ' '
str c 0 69
ldc c ' '
str c 0 70
ldc c ' '
str c 0 71
ldc c ' '
str c 0 72
ldc c ' '
str c 0 73
ldc c ' '
str c 0 74
ldc c ' '
str c 0 75
ldc c ' '
str c 0 76
ldc c ' '
str c 0 77
ldc c ' '
str c 0 78
ldc c ' '
str c 0 79
ldc c ' '
str c 0 80
ldc c ' '
str c 0 81
ldc c ' '
str c 0 82
ldc c ' '
str c 0 83
ldc c ' '
str c 0 84
ldc c ' '
str c 0 85
ldc c ' '
str c 0 86
ldc c ' '
str c 0 87
ldc c ' '
str c 0 88
ldc c ' '
str c 0 89
ldc c ' '
str c 0 90
ldc c ' '
str c 0 91
ldc c ' '
str c 0 92
ldc c ' '
str c 0 93
ldc c ' '
str c 0 94
ldc c ' '
str c 0 95
ldc c ' '
str c 0 96
ldc c ' '
str c 0 97
ldc c ' '
str c 0 98
ldc c ' '
str c 0 99
ldc c ' '
str c 0 100
ldc c ' '
str c 0 101
ldc c ' '
str c 0 102
ldc c ' '
str c 0 103
ldc c ' '
str c 0 104
ldc c ' '
str c 0 105
ldc c ' '
str c 0 106
ldc c ' '
str c 0 107
ldc c ' '
str c 0 108
ldc c ' '
str c 0 109
ldc c ' '
str c 0 110
ldc c ' '
str c 0 111
ldc c ' '
str c 0 112
ldc c ' '
str c 0 113
ldc c ' '
str c 0 114
ldc c ' '
str c 0 115
ldc c ' '
str c 0 116
ldc c ' '
str c 0 117
ldc c ' '
str c 0 118
ldc c ' '
str c 0 119
mst 1
lod a 0 7
ldc i 20
ixa 1
ind c
cup 1 label_doSomething
ssp 125
lda 0 120
str a 0 8
ldc r 0.0
str r 0 120
ldc r 0.0
str r 0 121
ldc r 0.0
str r 0 122
ldc r 0.0
str r 0 123
ldc r 0.0
str r 0 124
lod a 0 8
ldc i 0
ixa 1
ind r
ldc r 0.0
grt r
fjp main_ifelse_1_false
lod a 0 8
ldc i 2
ixa 1
ldc r 50.0
sto r
ujp main_ifelse_1_end
main_ifelse_1_false:
main_ifelse_1_end:
ldc i 10
str i 0 9
lod a 0 7
lod i 0 9
ldc i 2
mul i
ldc i 10
add i
ixa 1
ldc c 'z'
sto c
retf
