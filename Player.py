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
class Player:
    def __init__(self, playerIndex):
        self.setPlayerIndex(playerIndex)
        self.x = 0
        self.y = 0
        self.isInitialised = False

    def setPlayerIndex(self,playerIndex):
        self.playerColor=[]
        if(playerIndex == 1):
            r = [28,59,227] # 1
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
            r = [79,47,12] # 10
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

            s = float(self.playerColor[0]) + float(self.playerColor[1]) + float(self.playerColor[2])
            re = float(self.playerColor[0])/s
            ge = float(self.playerColor[1])/s
            be = float(self.playerColor[2])/s
            # написать функцию сравнения для каждого игрока
            dr = 0.03
            dg = 0.03
            db = 0.03
            if(rk > re - dr and rk < re + dr):
                if(gk > ge - dg and gk < ge + dg):
                    if(bk > be - db and bk < be + db):
                        cnt = cnt + 1

        return cnt

