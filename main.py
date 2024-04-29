# -*- coding: utf-8 -*-

import wx
from MySQLViewer import MySQLGui

def main():
    
    app = wx.App()
    displaySize= wx.DisplaySize()
    frame = MySQLGui(parent=None, title="SQL Viewer", size=(displaySize[0]/2, displaySize[1]/2))
    frame.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()