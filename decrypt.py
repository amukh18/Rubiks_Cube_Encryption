import numpy as np
from PIL import Image
import argparse
import pickle
import os

def shift(a,index,n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = np.roll(col,n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(j==index):
                a[i][j] = shiftCol[i]

def decrypt(file_name,save_name,key_name):

    file_name_proper = os.path.splitext(file_name)[0]

    key_file = open('keys/' + key_name,'rb')
    keys = pickle.load(key_file)

    K_r = keys[0]
    K_c = keys[1]
    max_iters = keys[2]

    enc_img = Image.open('enc_imgs/' + file_name)
    enc_img = np.array(enc_img)

    n_rows = enc_img.shape[0]
    n_cols = enc_img.shape[1]

    for x in range(max_iters):
        for j in range(n_cols):
            for i in range(n_rows):
                if (j%2==0):
                        enc_img[i][j] ^= K_r[i]
                else:
                        xor_amt = "{0:b}".format(K_r[i])
                        xor_amt = int(xor_amt[::-1],2)
                        enc_img[i][j] ^= xor_amt
        for i in range(n_rows):
            for j in range(n_cols):
                if (i%2):
                        enc_img[i][j] ^= K_c[j]
                else:
                        xor_amt = "{0:b}".format(K_c[j])
                        xor_amt = int(xor_amt[::-1],2)
                        enc_img[i][j] ^= xor_amt
        
        for i in range(n_cols):

            beta_i = 0
            for j in range (n_rows):
                beta_i += enc_img[j][i]
            m_beta_i = beta_i % 2
            shift_amt = - K_c[i] if m_beta_i else K_c[i]
            shift(enc_img, i, shift_amt)
        
        for i in range(n_rows):
            alpha_i = np.sum(enc_img[i])
            m_alpha_i = alpha_i % 2
            shift_amt = K_r[i] if m_alpha_i else -K_r[i]
            np.roll(enc_img[i], shift_amt)
            
    if not os.path.exists('dec_imgs'):
        os.mkdir('dec_imgs')

    img = Image.fromarray(enc_img)
    img.save('dec_imgs/' + save_name)



