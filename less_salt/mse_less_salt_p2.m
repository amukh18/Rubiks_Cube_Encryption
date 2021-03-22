ref = imread('../images/pic2.png');
imshow(ref)
A = imread('less_salt_on_pic2encrypted_decrypted.bmp');
imshow(A)
err = immse(A, ref);
fprintf('\n The mean-squared error is %0.4f\n', err);

%The mean-squared error is 2347.5188(output)