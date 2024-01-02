# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 16:17:44 2021

@author: lilin
已知能量迹取值，以及测量能量迹所用的随机明文，猜测所有可能的密钥，计算每个密钥对应的相关系数，取相关系数的最大值即为对应的正确猜测密钥
"""



S_Box= [ [14, 4,  13, 1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
         [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
	     [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
	     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]]

#补充plaintext
plaintext = [12, 10, 11, 1, 6, 1, 13, 11, 6, 13, 10, 0, 6, 15, 8, 15, 7, 0, 13, 15]

#补充power_std
power_std = [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 3, 2, 2, 1]



def to_bin(value, num):  # 十进制数据，二进制位宽
    bin_chars = ""
    temp = value
    for i in range(num):
        bin_char = bin(temp % 2)[-1]
        temp = temp // 2
        bin_chars = bin_char + bin_chars
    return bin_chars.upper()


def HWfun(num):
    # 统计输入num的汉明重量并返回
    hmweight = []
    for x in num:
        count = 0
        x = to_bin(x, 6)
        for y in x:
            if y == '1':
                count += 1
        hmweight.append(count)
    return hmweight


def Meanfun(n, num):
    total = 0
    for i in range(0, n):
        total = total + num[i]
    return total / n


def sboxout(n, P, key):
    pxork = 0
    cv = 0  # 列
    rv = 0  # 行
    bpxork = 0
    sout = []
    for i in range(0, n):
        pxork = P[i] ^ key
        bpxork = str(to_bin(pxork, 8))[2:]
        cv = 2 * int(bpxork[0]) + int(bpxork[5])
        rv = 8 * int(bpxork[1]) + 4 * int(bpxork[2]) + 2 * int(bpxork[3]) + int(bpxork[4])
        sout.append(S_Box[cv][rv])
    return sout


def DPAfun(n, pstd, ptest):
    # 以2为界，计算不同汉明重量的集合差值
    L = []
    H = []
    for i in range(0, n):
        if ptest[i] > 2:
            H.append(pstd[i])
        else:
            L.append(pstd[i])
    return (sum(H) / len(H)) - (sum(L) / len(L))


if __name__ == "__main__":
    # 猜测密钥
    testkey = 0
    maxdpa = 0
    for key in range(1, 64):
        sout = sboxout(20, plaintext, key)
        hw = HWfun(sout)
        dpa = DPAfun(20, power_std, ptest=hw)
        if dpa > maxdpa:
            maxdpa = dpa
            testkey = key
    print(testkey)






