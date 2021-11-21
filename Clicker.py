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
import win32api, win32con, win32gui
from win32api import GetKeyState
from win32con import VK_CAPITAL
from win32con import VK_MENU
from win32con import VK_CONTROL
from pathlib import Path
import time
from ctypes import windll
import numpy
import ColorDetector
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

    def click(self, x,y, needNoise):
        #ctypes.windll.user32.SetCursorPos((x,y))


        if(needNoise):
            [x1,y1] = self.randomCoordsInArea(x, y, 15, 15)
            #print("Noised")
        else:
            x1 = x
            y1 = y
        print(x1,y1)
        win32api.SetCursorPos((x1,y1))
        time.sleep(0.05)
        for i in range(0,2): # click cnt
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x1,y1,0,0)

    def randomCoordsInArea(self, xRightUp, yLeftUp, xWidth, yWidth):
        if(xRightUp - xWidth < self.xLeftUp):
            x = round(numpy.random.uniform(self.xLeftUp,self.xLeftUp + xWidth,1)[0])
        else:
            x = round(numpy.random.uniform(xRightUp - xWidth,xRightUp,1)[0])
        if(yLeftUp + yWidth > self.yLeftUp + self.yWidth):
            y = round(numpy.random.uniform(self.yLeftUp + self.yWidth - yWidth,self.yLeftUp + self.yWidth,1)[0])
        else:
            y = round(numpy.random.uniform(yLeftUp,yLeftUp + yWidth,1)[0])
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
                self.setArea(xLeftUp, yLeftUp, xWidth, yWidth)
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
        cd = ColorDetector.ColorDetector()

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
        #[x,y] = self.randomCoordsInArea()
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
                    self.click(x,y,True)


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