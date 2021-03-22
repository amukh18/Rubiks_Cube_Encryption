I = imread('../enc_imgs/enc_pic2.png');
N=imnoise(I,'speckle', 0.1);
imshow(N) 