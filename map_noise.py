#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Юзверь
#
# Created:     07.11.2021
# Copyright:   (c) Юзверь 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import win32api, win32con, win32gui
from win32api import GetKeyState
from win32con import VK_CAPITAL
from win32con import VK_MENU
from win32con import VK_CONTROL
from pathlib import Path
import colorsys
from ctypes import windll
import PIL.ImageGrab
import numpy
import time
import numpy as np
from PIL import Image

def main():
    pass

if __name__ == '__main__':
    main()

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

        #r = colorsys.rgb_to_hls(255/255,232/255,1/255) # 4
        r = colorsys.rgb_to_hls(90/255,12/255,126/255) # 3
        #r = colorsys.rgb_to_hls(187/255,107/255,19/255) # 5
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


class Clicker:

    def isCapsOn(self):
        return GetKeyState(VK_CAPITAL) == 1

    def isAltOn(self):
        return GetKeyState(VK_MENU) == -127 or GetKeyState(VK_MENU) == -128

    def isCtrlOn(self):
        return GetKeyState(VK_CONTROL) == -127 or GetKeyState(VK_CONTROL) == -128

    def isLeftClickUp(self):
        return win32api.GetKeyState(0x01) == 0 or win32api.GetKeyState(0x01) == 1

    def detectCapsOn(self, prevCaps):
        curCaps = self.isCapsOn()
        isDetect = False
        if(curCaps != prevCaps and curCaps == True):
            isDetect = True
        return [curCaps, isDetect]

    def detectCapsOff(self, prevCaps):
        curCaps = self.isCapsOn()
        isDetect = False
        if(curCaps != prevCaps and curCaps == False):
            isDetect = True
        return [curCaps, isDetect]

    def detectLeftClickUp(self, prev):
        cur = self.isLeftClickUp()
        isDetect = False
        if(cur != prev and cur == True):
            isDetect = True
        return [cur, isDetect]

    def click(self, x,y):
        #ctypes.windll.user32.SetCursorPos((x,y))

        win32api.SetCursorPos((x,y))
        time.sleep(0.05)
        for i in range(0,2): # click cnt
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def randomCoordsInArea(self):
        x = round(numpy.random.uniform(self.xLeftUp,self.xLeftUp + self.xWidth,1)[0])
        y = round(numpy.random.uniform(self.yLeftUp,self.yLeftUp + self.yWidth,1)[0])
        return [x,y]

    def setArea(self, xLeftUp, yLeftUp, xWidth, yWidth):
        self.xLeftUp = xLeftUp
        self.yLeftUp = yLeftUp
        self.xWidth = xWidth
        self.yWidth = yWidth
        self.printClickArea()

    def setAreaByClicks(self, xFirst, yFirst, xSecond, ySecond):
        leftX = min(xFirst, xSecond)
        leftY = min(yFirst, ySecond)
        xWidth = max(xFirst, xSecond) - leftX
        yWidth = max(yFirst, ySecond) - leftY
        self.setArea(leftX, leftY, xWidth, yWidth)

    def printClickArea(self):
        print("Area Left Corner ",self.xLeftUp, self.yLeftUp)
        print("Area Width ",self.xWidth, self.yWidth)

    def saveDataToConfigFile(self):
        with open('config.txt','w') as f:
            f.write(str(self.xLeftUp) + "\n")
            f.write(str(self.yLeftUp) + "\n")
            f.write(str(self.xWidth) + "\n")
            f.write(str(self.yWidth) + "\n")
            print("save data to config")

    def readDataFromConfigFile(self):
        my_file = Path("config.txt")
        if my_file.is_file():
            xLeftUp = -1
            yLeftUp = -1
            xWidth = -1
            yWidth = -1
            isError = False
            with open("config.txt",'r') as f:
                xLeftUp = f.readline()
                if(xLeftUp != ''):
                    xLeftUp = int(xLeftUp)
                else:
                    isError = True

                yLeftUp = f.readline()
                if(yLeftUp != ''):
                    yLeftUp = int(yLeftUp)
                else:
                    isError = True

                xWidth = f.readline()
                if(xWidth != ''):
                    xWidth = int(xWidth)
                else:
                    isError = True

                yWidth = f.readline()
                if(yWidth != ''):
                    yWidth = int(yWidth)
                else:
                    isError = True
            if(not(isError)):
                print("set values from config file")
                clicker.setArea(xLeftUp, yLeftUp, xWidth, yWidth)
            else:
                xLeftUp = 100
                yLeftUp = 100
                xWidth = 100
                yWidth = 100
                print("set default values")
                clicker.setArea(xLeftUp, yLeftUp, xWidth, yWidth)
        else:
            xLeftUp = 100
            yLeftUp = 100
            xWidth = 100
            yWidth = 100
            print("set default values")
            clicker.setArea(xLeftUp, yLeftUp, xWidth, yWidth)

    def getCursorPosition(self):
        x, y = win32api.GetCursorPos()
        return [x, y]

    def rgbint2rgbtuple(self, RGBint):
        blue =  RGBint & 255
        green = (RGBint >> 8) & 255
        red =   (RGBint >> 16) & 255
        return (red, green, blue)

    def startClickRoutine(self):
        cd = ColorDetector()

        t1 = time.time()
        t2 = time.time()

        prevCaps1 = self.isCapsOn()
        isDetectCapsOn = False

        prevCaps2 = self.isCapsOn()
        isDetectCapsOff = False

        prevLeftClick = self.isLeftClickUp()
        isDetectLeftClick = False

        isFirstClick = False
        isSecondClick = False
        isJustClick = False

        xFirst = 0
        yFirst = 0
        xSecond = 0
        ySecond = 0
        [x,y] = self.randomCoordsInArea()
        isInitialised = False
        while(True):
            t2 = time.time()
            dt = t2 - t1


            [prevCaps1, isDetectCapsOn] = self.detectCapsOn(prevCaps1)
            [prevCaps2, isDetectCapsOff] = self.detectCapsOff(prevCaps2)


            if(self.isCapsOn()):
                if(dt > 0.5):
                    t1 = time.time()
                    #[x,y] = self.randomCoordsInArea()

                    pnts = cd.colorCheckRows(self.xLeftUp, self.yLeftUp, self.xWidth, self.yWidth)
                    if(len(pnts) > 0):
                        isInitialised = True
                        x = int(pnts[0][0])
                        y = int(pnts[0][1])
                        print(x,y)
                    if(isInitialised):
                        self.click(x,y)


            ## запомнить область 2-х кликов при нажатии alt + ctrl
            elif(self.isAltOn() and self.isCtrlOn()):
                [prevLeftClick, isDetectLeftClick] = self.detectLeftClickUp(prevLeftClick)
                if(isDetectLeftClick):
                    isDetectLeftClick = False
                    if(not(isFirstClick) and not(isSecondClick)):
                        isFirstClick = True
                        isSecondClick = False
                        [xFirst, yFirst] = self.getCursorPosition()
                        print("First Click ", xFirst, yFirst)
                    elif(isFirstClick and not(isSecondClick)):
                        isFirstClick = True
                        isSecondClick = True
                        [xSecond, ySecond] = self.getCursorPosition()
                        print("Second Click ", xSecond, ySecond)
                        self.setAreaByClicks(xFirst, yFirst, xSecond, ySecond)
                        self.saveDataToConfigFile()

            else:
                isFirstClick = False
                isSecondClick = False

                [prevLeftClick, isDetectLeftClick] = self.detectLeftClickUp(prevLeftClick)
                if(isDetectLeftClick):
                    #[x, y] = self.getCursorPosition()
                    #color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x , y)
                    #print(self.rgbint2rgbtuple(color))
                    #print("click")
                    cd.colorCheckRows(self.xLeftUp, self.yLeftUp, self.xWidth, self.yWidth)

            if(isDetectCapsOn):
                isDetectCapsOn = False
                print("Clicker on")
                self.printClickArea()
                win32api.keybd_event(VK_MENU, 0, 0, 0)

            if(isDetectCapsOff):
                isDetectCapsOff = False
                win32api.keybd_event(VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
                print("Off")




clicker = Clicker()
clicker.readDataFromConfigFile()
clicker.startClickRoutine()



