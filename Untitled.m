data = imread('t8.png');
mapImage = data(780:(780+213),37:(37+257),:);
%imshow(mapImage)

data2 = double(mapImage);
for i = 1:length(mapImage(:,1,1))
    for j = 1:length(mapImage(1,:,1))
        k = double(mapImage(i,j,:));
        data2(i,j,1) = k(1)/sum(k);
        data2(i,j,2) = k(2)/sum(k);
        data2(i,j,3) = k(3)/sum(k);
    end
end
k = [0,65,250];

etalon = data2(42,20,:);
etalon(1,1,:) = k./sum(k);

data3 = mapImage;
for i = 1:length(mapImage(:,1,1))
    for j = 1:length(mapImage(1,:,1))
        if(i > 100 && j > 100)
            l = 1;
        end
        k = data2(i,j,:);
        u1 = k > (etalon - 0.03);
        u2 = k < (etalon + 0.03);
        if(sum(u1) + sum(u2) == 6)
            %if(sum(mapImage(i,j,:)) <= 150)
                data3(i,j,1) = 255;
                data3(i,j,2) = 0;
                data3(i,j,3) = 0;
            %end
        end
    end
end
imshow(data3)
% minVal = 755*min(etalon);
% maxVal = 755*max(etalon);
% n = 10;
% m = length(minVal:5:maxVal)*n;
% 
% d = rand(n,n,3).*0;
% data4 = rand(n,m,3).*NaN;
% j = 1;
% for i = 200:5:maxVal
%     d(:,:,1) = uint8(i*etalon(1));
%     d(:,:,2) = uint8(i*etalon(2));
%     d(:,:,3) = uint8(i*etalon(3));
%     data4(:,(1:n) + (j-1)*n,:) = d;
%     j = j + 1;
% end
