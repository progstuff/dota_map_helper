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
import Clicker
import time
def main():
    pass

if __name__ == '__main__':
    main()


clicker = Clicker.Clicker()
clicker.readDataFromConfigFile()
clicker.startClickRoutine()

