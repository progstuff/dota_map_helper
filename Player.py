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
import colorsys
import time
class Player:
    def __init__(self, playerIndex):
        self.setPlayerIndex(playerIndex)
        self.x = 0
        self.y = 0
        self.tm = 0
        self.prevTm = 0
        self.isInitialised = False
        self.isOnMap = False
        self.line = 0
        self.prevLine = 0
        self.prevState = True
        self.lastState = 0
        self.isNeedMessage = False

    def detectStateChanged(self,newState):
        #if(time.time() - self.tm > 2):
        if(newState != self.isOnMap):
            if(newState == True):
                self.prevState = False
                print("пришёл")
                self.prevLine = self.line
            else:
                self.prevState = True
                self.prevTm = time.time()
                print("ушёл")
            self.isOnMap = newState

        if(time.time() - self.prevTm > 2):
            if(self.prevState == True and self.isOnMap == False):
                isNeedMessage = True
                self.lastLine = self.prevLine
                self.prevState = False
                self.isNeedMessage = True
                print("need mes ", self.lastLine)

    def lineName(self):
        if(self.line == 1):
            return "верхняя линия"
        if(self.line == 2):
            return "средняя линия"
        if(self.line == 3):
            return "нижняя линия"
        if(self.line == 0):
            return "карты"

    def currentLine(self, xLeftUp ,yLeftUp, xWidth, yWidth):
        if(self.isOnMap):
            if(self.x < xLeftUp + 70 and self.y < yLeftUp + 100):
                #print("верхняя линия", self.playerIndex)
                self.line = 1
            elif(self.x > xLeftUp + xWidth - 75 and self.y > yLeftUp + yWidth - 90):
                #print("нижняя линия ", self.playerIndex)
                self.line = 3
            else:
                xc = xLeftUp + xWidth/2
                yc = yLeftUp + yWidth/2
                if(self.x > xc - 50 and self.x < xc + 50 and self.y > yc - 35 and self.y < yc + 35):
                    #print("средняя линия", self.playerIndex)
                    self.line = 2
                else:
                    #print("не определено", self.playerIndex)
                    self.line = 0

    def setPlayerIndex(self,playerIndex):
        self.playerColor=[]
        if(playerIndex == 1):
            r = [0,65,250] # 1
        elif(playerIndex == 2):
            r = [22,184,148] # 2
        elif(playerIndex == 3):
            r = [81,0,124]
        elif(playerIndex == 4):
            r = [255,251,1] # 4
        elif(playerIndex == 5):
            r = [245,133,14] # 5
        elif(playerIndex == 6):
            r = [224,89,170] # 6
        elif(playerIndex == 7):
            r = [144,145,146] # 7
        elif(playerIndex == 8):
            r = [128,188,229] # 8
        elif(playerIndex == 9):
            r = [17,101,68] # 9
        elif(playerIndex == 10):
            r = [78,42,4] # 10
        self.playerColor.append(r[0])
        self.playerColor.append(r[1])
        self.playerColor.append(r[2])
        self.playerIndex = playerIndex
        print("set player № ",playerIndex)

    def checkColor(self, r,g,b):
        cnt = 0
        s = float(r) + float(g) + float(b)
        if(s != 0):
            rk = float(r)/s
            gk = float(g)/s
            bk = float(b)/s

            s2 = float(self.playerColor[0]) + float(self.playerColor[1]) + float(self.playerColor[2])
            re = float(self.playerColor[0])/s2
            ge = float(self.playerColor[1])/s2
            be = float(self.playerColor[2])/s2

            if(self.playerIndex == 1):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 2):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 3):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 4):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 5):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(s > 250):
                    if(rk > re - dr and rk < re + dr):
                        if(gk > ge - dg and gk < ge + dg):
                            if(bk > be - db and bk < be + db):
                                cnt = cnt + 1
            elif(self.playerIndex == 6):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 7):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 8):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 9):
                dr = 0.03
                dg = 0.03
                db = 0.03
                if(rk > re - dr and rk < re + dr):
                    if(gk > ge - dg and gk < ge + dg):
                        if(bk > be - db and bk < be + db):
                            cnt = cnt + 1
            elif(self.playerIndex == 10):
                dr = 0.01
                dg = 0.01
                db = 0.01
                if(s <= 140):
                    if(rk > re - dr and rk < re + dr):
                        if(gk > ge - dg and gk < ge + dg):
                            if(bk > be - db and bk < be + db):
                                cnt = cnt + 1
        return cnt

