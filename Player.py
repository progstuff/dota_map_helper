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

    def setPlayerIndex(self,playerIndex):
        self.playerColor=[]
        if(playerIndex == 1):
            r = colorsys.rgb_to_hls(28/255,59/255,227/255) # 1
        elif(playerIndex == 2):
            r = colorsys.rgb_to_hls(34/255,224/255,181/255) # 2
        elif(playerIndex == 3):
            r = colorsys.rgb_to_hls(90/255,12/255,126/255) # 3
        elif(playerIndex == 4):
            r = colorsys.rgb_to_hls(255/255,232/255,1/255) # 4
        elif(playerIndex == 5):
            r = colorsys.rgb_to_hls(187/255,107/255,19/255) # 5
        elif(playerIndex == 6):
            r = colorsys.rgb_to_hls(138/255,141/255,147/255) # 6
        elif(playerIndex == 7):
            r = colorsys.rgb_to_hls(28/255,59/255,227/255) # 7
        elif(playerIndex == 8):
            r = colorsys.rgb_to_hls(128/255,188/255,229/255) # 8
        elif(playerIndex == 9):
            r = colorsys.rgb_to_hls(25/255,100/255,75/255) # 9
        elif(playerIndex == 10):
            r = colorsys.rgb_to_hls(73/255,37/255,12/255) # 10
        self.playerColor.append(r[0]*240)
        self.playerColor.append(r[1]*240)
        self.playerColor.append(r[2]*240);
