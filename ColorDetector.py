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
    def __init__(self,player):
        self.width = 8
        self.height = 8
        self.dr = 0.03
        self.dg = 0.03
        self.db = 0.03
        self.rs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.gs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.bs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.setPlayer(player)


    def setPlayer(self, player):
        self.player = player

        #print("set new player color", r_rgb[0], r_rgb[1], r_rgb[2])

    def isPlayerInArea(self,i1,i2,j1,j2):
        n = self.width
        m = self.height
        cnt = 0

        for i in range(int(i1), int(i2)):
            for j in range(int(j1), int(j2)):
                r = self.rs[i][j]
                g = self.gs[i][j]
                b = self.bs[i][j]
                k = self.player.checkColor(r, g, b)
                cnt = cnt + k

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

        if(a > 60):
            print(a)
            return [True,a]
        return [False,a]


    def getAreaPixels(self, img, xMin, xMax, yMin, yMax):

        for i in range(xMin, xMax):
            for j in range(yMin, yMax):
                #color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), i , j)
                color = img[i,j]
                rcolor = color
                self.rs[i - xMin][j - yMin] = rcolor[0]
                self.gs[i - xMin][j - yMin] = rcolor[1]
                self.bs[i - xMin][j - yMin] = rcolor[2]
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
    def getPicture(self):
        self.img = PIL.ImageGrab.grab().load()
    def colorCheckRows(self, xLeftUp, yLeftUp, xWidth, yWidth):
        yRectRightUp = yLeftUp
        points = []
        while(yRectRightUp < yLeftUp + yWidth - self.height):
            points = self.colorCheckRow(self.img, xLeftUp, yRectRightUp, xWidth, yWidth, points)
            yRectRightUp = yRectRightUp + self.height
            #print(yRectRightUp)
        if(yRectRightUp + self.height > yLeftUp + yWidth):
            yRectRightUp = yLeftUp + yWidth - self.height
            points = self.colorCheckRow(self.img, xLeftUp, yRectRightUp, xWidth, yWidth, points)
            #print(yRectRightUp)
        return points
        #print("stop")

    def rgbint2rgbtuple(self, RGBint):
        blue =  RGBint & 255
        green = (RGBint >> 8) & 255
        red =   (RGBint >> 16) & 255
        return (red, green, blue)
