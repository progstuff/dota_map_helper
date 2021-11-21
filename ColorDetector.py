#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Юзверь
#
# Created:     21.11.2021
# Copyright:   (c) Юзверь 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
from PIL import Image
import colorsys
import PIL.ImageGrab
class ColorDetector:
    def __init__(self):
        self.width = 15
        self.height = 15
        self.dh = 3
        self.dl = 3
        self.ds = 20

        self.hs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ls = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ss = [[0 for x in range(self.width)] for y in range(self.height)]

        self.etalon=[]

        #r = colorsys.rgb_to_hls(90/255,12/255,126/255) # 3
        #r = colorsys.rgb_to_hls(255/255,232/255,1/255) # 4
        r = colorsys.rgb_to_hls(187/255,107/255,19/255) # 5
        self.etalon.append(r[0]*240)
        self.etalon.append(r[1]*240)
        self.etalon.append(r[2]*240);

        x = 20
        y = 20
        w = x*self.dh*2
        h = y*self.dl*2
        img = Image.new('RGB', (w, h))
        for i in range(0,self.dh*2):
            for j in range(0,self.dl*2):
                for k1 in range(0, x):
                    for k2 in range(0,y):
                        a = []
                        r = colorsys.hls_to_rgb((self.etalon[0]-self.dh+i)/240,(self.etalon[1]-self.dl+j)/240,self.etalon[2]/240)
                        a.append(r[0]*255)
                        a.append(r[1]*255)
                        a.append(r[2]*255)
                        img.putpixel( (i*x + k1, j*y + k2), (int(a[0]),int(a[1]),int(a[2])) )
        img.save('tst.png')
        print("generated")


    def isPlayerInArea(self,i1,i2,j1,j2):
        n = self.width
        m = self.height
        cnt = 0
        for i in range(int(i1), int(i2)):
            for j in range(int(j1), int(j2)):
                if(self.hs[i][j] > self.etalon[0] - self.dh and self.hs[i][j] < self.etalon[0] + self.dh):
                    if(self.ls[i][j] > self.etalon[1] - self.dl and self.ls[i][j] < self.etalon[1] + self.dl):
                        if(self.ss[i][j] > 170):
                            cnt = cnt + 1
        return cnt/((i2 - i1)*(j2 - j1))*100

    def checkSavedArea(self):
        r = []
        r.append(self.isPlayerInArea(0, self.width/2, 0, self.height/2))
        r.append(self.isPlayerInArea(self.width/2, self.width, 0, self.height/2))
        r.append(self.isPlayerInArea(0, self.width/2, self.height/2, self.height))
        r.append(self.isPlayerInArea(self.width/2, self.width, self.height/2, self.height))
        r.append(self.isPlayerInArea(self.width/4, self.width/4 + self.width/2, self.height/4, self.height/4 + self.height/2))
        r.append(self.isPlayerInArea(0, self.width/2, self.height/4, self.height/4 + self.height/2))
        r.append(self.isPlayerInArea(self.width/2, self.width, self.height/4, self.height/4 + self.height/2))
        r.append(self.isPlayerInArea(self.width/4, self.width/4 + self.width/2, 0, self.height/2))
        r.append(self.isPlayerInArea(self.width/4, self.width/4 + self.width/2, self.height/2, self.height))
        a = max(r)
        if(a > 1):
            return [True,a]
        return [False,a]


    def getAreaPixels(self, img, xMin, xMax, yMin, yMax):

        for i in range(xMin, xMax):
            for j in range(yMin, yMax):
                #color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), i , j)
                color = img[i,j]
                rcolor = color
                a=[];r = colorsys.rgb_to_hls(rcolor[0]/255,rcolor[1]/255,rcolor[2]/255);a.append(r[0]*240);a.append(r[1]*240);a.append(r[2]*240);
                self.hs[i - xMin][j - yMin] = a[0]
                self.ls[i - xMin][j - yMin] = a[1]
                self.ss[i - xMin][j - yMin] = a[2]
                #print(i - xMin,j - yMin)


    def colorCheckRow(self, img, xLeftUp, yLeftUp, xWidth, yWidth,rez):


        #img = PIL.ImageGrab.grab().load()
        #PIL.ImageGrab.grab().save("test.png")

        xRectRightUp = xLeftUp + self.width
        yRectRightUp = yLeftUp
        while(xRectRightUp < xLeftUp + xWidth):
            areaXLeftUp = xRectRightUp - self.width
            areaYLeftUp = yRectRightUp
            areaXRightDown = xRectRightUp
            areaYLeftDown = yRectRightUp + self.height
            self.getAreaPixels(img, areaXLeftUp, areaXRightDown, areaYLeftUp, areaYLeftDown)
            [isPr, r] = self.checkSavedArea()
            if(isPr):
                x = (areaXLeftUp + areaXRightDown)/2
                y = (areaYLeftDown + areaYLeftUp)/2
                rez.append((x,y))
                #print(xRectRightUp,yRectRightUp,r)
            xRectRightUp = xRectRightUp + self.width

        if(xRectRightUp - self.width < xLeftUp + xWidth):
            xRectRightUp = xLeftUp + xWidth
            areaXLeftUp = xRectRightUp - self.width
            areaYLeftUp = yRectRightUp
            areaXRightDown = xRectRightUp
            areaYLeftUp = yRectRightUp + self.height
            self.getAreaPixels(img,areaXLeftUp, areaXRightDown, areaYLeftUp, areaYLeftDown)
            [isPr, r] = self.checkSavedArea()
            if(isPr):
                x = (areaXLeftUp + areaXRightDown)/2
                y = (areaYLeftDown + areaYLeftUp)/2
                rez.append((x,y))
                #print(xRectRightUp,yRectRightUp,r)

        return rez
        #if(yRectRightUp + self.height > yLeftUp + yWidth):

        #print("stop")

    def colorCheckRows(self, xLeftUp, yLeftUp, xWidth, yWidth):

        img = PIL.ImageGrab.grab().load()
        #PIL.ImageGrab.grab().save("test.png")
        yRectRightUp = yLeftUp
        points = []
        while(yRectRightUp < yLeftUp + yWidth - self.height):
            points = self.colorCheckRow(img, xLeftUp, yRectRightUp, xWidth, yWidth, points)
            yRectRightUp = yRectRightUp + self.height
            #print(yRectRightUp)
        if(yRectRightUp + self.height > yLeftUp + yWidth):
            yRectRightUp = yLeftUp + yWidth - self.height
            points = self.colorCheckRow(img, xLeftUp, yRectRightUp, xWidth, yWidth, points)
            #print(yRectRightUp)
        return points
        #print("stop")

    def rgbint2rgbtuple(self, RGBint):
        blue =  RGBint & 255
        green = (RGBint >> 8) & 255
        red =   (RGBint >> 16) & 255
        return (red, green, blue)
