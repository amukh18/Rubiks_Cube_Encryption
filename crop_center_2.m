testimage=imread('enc_imgs/chess_encrypted.png');
imshow(testimage)
H=imrect(gca);
pos=wait(H);
close all
testimage(pos(1,2):pos(1,2)+pos(1,4),pos(1,1):pos(1,1)+pos(1,3))=0;
imshow(testimage)