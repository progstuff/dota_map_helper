data = imread('t8.png');
xlft = 37;
ylft = 780;
xW = 257;
yW = 213;
mapImage = data(ylft:(ylft+yW),xlft:(xlft+xW),:);
imshow(mapImage)

data2 = mapImage;
%up
xw = 70;
yw = 100;
data2(1:yw,1,1) = 255;
data2(1:yw,1,2) = 255;
data2(1:yw,1,3) = 255;
data2(1,1:xw,1) = 255;
data2(1,1:xw,2) = 255;
data2(1,1:xw,3) = 255;

data2(1:yw,1+xw,1) = 255;
data2(1:yw,1+xw,2) = 255;
data2(1:yw,1+xw,3) = 255;
data2(yw,1:xw,1) = 255;
data2(yw,1:xw,2) = 255;
data2(yw,1:xw,3) = 255;

%dn
xw = 75;
yw = 90;
data2((end-yw):end,end,1) = 255;
data2((end-yw):end,end,2) = 255;
data2((end-yw):end,end,3) = 255;
data2((end-yw):end,end-xw,1) = 255;
data2((end-yw):end,end-xw,2) = 255;
data2((end-yw):end,end-xw,3) = 255;

data2(end-yw,(end-xw):end,1) = 255;
data2(end-yw,(end-xw):end,2) = 255;
data2(end-yw,(end-xw):end,3) = 255;
data2(end,(end-xw):end,1) = 255;
data2(end,(end-xw):end,2) = 255;
data2(end,(end-xw):end,3) = 255;

%mid
xc = round(xW/2);
yc = round(yW/2);
xw2 = 50;
yw2 = 35;
data2((yc-yw2):(yc+yw2),(xc-xw2),1) = 255;
data2((yc-yw2):(yc+yw2),(xc-xw2),2) = 255;
data2((yc-yw2):(yc+yw2),(xc-xw2),3) = 255;
data2((yc-yw2):(yc+yw2),(xc+xw2),1) = 255;
data2((yc-yw2):(yc+yw2),(xc+xw2),2) = 255;
data2((yc-yw2):(yc+yw2),(xc+xw2),3) = 255;
data2((yc-yw2),(xc-xw2):(xc+xw2),1) = 255;
data2((yc-yw2),(xc-xw2):(xc+xw2),2) = 255;
data2((yc-yw2),(xc-xw2):(xc+xw2),3) = 255;
data2((yc+yw2),(xc-xw2):(xc+xw2),1) = 255;
data2((yc+yw2),(xc-xw2):(xc+xw2),2) = 255;
data2((yc+yw2),(xc-xw2):(xc+xw2),3) = 255;
imshow(data2)

