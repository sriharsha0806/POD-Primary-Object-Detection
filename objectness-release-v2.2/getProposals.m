imgs = dir('frame*.jpg');
imgs = {imgs.name};
imgCnt = length(imgs);
proposals = zeros(20,5,imgCnt);

for i = 1:imgCnt
    img = imread(char(imgs(i)));
    proposals(:,:,i) = runObjectness(img,20);
end