import numpy as np
from PIL import Image
import argparse
import pickle
import os

parser = argparse.ArgumentParser(description='encryption')

parser.add_argument('--file_name',
                    type = str,
                    dest = 'file_name',
                    help = 'image file to encrypt')
parser.add_argument('--iters', 
                    type = int,
                    dest = 'iters',
                    help = 'number of iterations')


arguments = parser.parse_args()

file_name_proper = os.path.splitext(arguments.file_name)[0]
main_name = 'enc_' + file_name_proper

key_file = open('keys/' + main_name + '_key.pkl','wb')

img = Image.open('images/' + arguments.file_name)
img = np.array(img)

n_rows = img.shape[0]
n_cols = img.shape[1]

K_r = np.random.randint(0, 256, size = n_rows)
K_c = np.random.randint(0, 256, size = n_cols)
max_iters = arguments.iters
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
        shift_amt = - K_c[i] if m_beta_i else K_c[i]
        np.roll(img[i], shift_amt)

    for i in range(n_rows):
        for j in range(n_cols):
            if (i%2):
                    img[i][j] ^= K_c[j]
            else:
                    xor_amt = "{0:b}".format(K_c[j])
                    xor_amt = int(xor_amt[::-1],2)
                    img[i][j] ^= xor_amt

    for i in range(n_cols):
        for j in range(n_rows):
            if (i%2):
                    img[i][j] ^= K_r[j]
            else:
                    xor_amt = "{0:b}".format(K_r[j])
                    xor_amt = int(xor_amt[::-1],2)
                    img[i][j] ^= xor_amt


if not os.path.exists('enc_imgs'):
    os.mkdir('enc_imgs')

img = Image.fromarray(img)
img.save('enc_imgs/' + 'enc_' + arguments.file_name)

if not os.path.exists('keys'):
    os.mkdir('keys')

pickle.dump(keys, key_file)
key_file.close()

