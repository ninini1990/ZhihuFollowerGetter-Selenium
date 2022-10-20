import os
import socket


# 获取系统用户目录名称
def getWinUserName():
    winUserHome = os.path.expanduser('~')
    winUserName =os.path.split(winUserHome)[-1]
    return winUserName


# 获取用户桌面路径, 输出结果"C:\Users\UserName\Desktop\"
def getWinDesktopPath():
    winUserName = getWinUserName()
    winDesktopPath = "C:\\Users\\" + winUserName + "\\Desktop\\"
    return winDesktopPath
