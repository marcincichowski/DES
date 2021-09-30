import utils
from utils import *
def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)
    pt = permute(pt, initial_perm, 64)
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        right_expanded = permute(right, exp_d, 48)
        xor_x = utils.xor(right_expanded, rkb[i])
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)
        sbox_str = permute(sbox_str, per, 32)
        result = utils.xor(left, sbox_str)
        left = result
        if (i != 15):
            left, right = right, left
    combine = left + right
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text