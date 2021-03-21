import numpy as np
from PIL import Image, ImageOps
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
def encrypt(file_name, save_name,key_name, max_iters):
    
    file_name_proper = os.path.splitext(file_name)[0]

    img = Image.open('images/' + file_name)
    img = ImageOps.grayscale(img)
    img.save(file_name + 'gray.png')
    img = np.array(img)
    if not os.path.exists('keys'):
        os.mkdir('keys')

    key_file = open('keys/' + key_name, 'wb')


    print(img.shape)

    n_rows = img.shape[0]
    n_cols = img.shape[1]

    K_r = np.random.randint(0, 255, size = n_rows)
    K_c = np.random.randint(0, 255, size = n_cols)
    keys = []
    keys.append(K_r)
    keys.append(K_c)
    keys.append(max_iters)

    for x in range(max_iters):
        for i in range(n_rows):

            alpha_i = np.sum(img[i])
            m_alpha_i = alpha_i % 2
            shift_amt = - K_r[i] if m_alpha_i else K_r[i]
            np.roll(img[i], shift_amt)
        for i in range(n_cols):

            beta_i = 0
            for j in range (n_rows):
                beta_i += img[j][i]
            m_beta_i = beta_i % 2
            shift_amt = K_c[i] if m_beta_i else - K_c[i]
            shift(img, i, shift_amt)

        for i in range(n_rows):
            for j in range(n_cols):
                if (i%2):
                        img[i][j] ^= K_c[j]
                else:
                        xor_amt = "{0:b}".format(K_c[j])
                        xor_amt = int(xor_amt[::-1],2)
                        img[i][j] ^= xor_amt

        for j in range(n_cols):
            for i in range(n_rows):
                if (j%2 == 0):
                        img[i][j] ^= K_r[i]
                else:
                        xor_amt = "{0:b}".format(K_r[i])
                        xor_amt = int(xor_amt[::-1],2)
                        img[i][j] ^= xor_amt
                        
    if not os.path.exists('enc_imgs'):
        os.mkdir('enc_imgs')

    img = Image.fromarray(img)
    img.save('enc_imgs/' + save_name)

    if not os.path.exists('keys'):
        os.mkdir('keys')

    pickle.dump(keys, key_file)
    key_file.close()

