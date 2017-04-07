#!/usr/bin/python2

c[][]
def lcs(x, y, i, j):
    if c[i][j] == 0:
        if x[i] == y[j]:
            c[i][j] = c[i-1][j-1] + 1
        else:
            c[i][j] = max(lcs(x, y, i-1, j), lcs(x, y, i, j-1))
    return c[i][j]

if __name__ == 'main':
    x = "abcd"
    y = "abcd"
    c[i][j] = lcs(x, y, 3, 3)

    print "c[i][j] = ", c[3][3]
