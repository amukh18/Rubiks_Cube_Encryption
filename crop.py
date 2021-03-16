import numpy as np
from PIL import Image
import argparse
import os


parser = argparse.ArgumentParser(description='cropping')

parser.add_argument('--file_name',
                    type = str,
                    dest = 'file_name',
                    help = 'image file to crop')

arguments = parser.parse_args()

img = Image.open(arguments.file_name)
img = np.array(img)

n_rows = img.shape[0]
n_cols = img.shape[1]

row_start = int(n_rows/3)
row_end = int(2*n_rows/3 + 1)
col_start = int(n_cols/3)
col_end = int(2*n_cols/3 + 1)

for i in range(row_start, row_end):
    for j in range(col_start, col_end):
        img[i][j] = 0

if not os.path.exists('cropped_imgs'):
    os.mkdir('cropped_imgs')

img = Image.fromarray(img)
img.save('cropped_imgs/' + 'cropped_' + arguments.file_name)