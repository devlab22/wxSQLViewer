# -*- coding: utf-8 -*-

import wx
from MySQLViewer import MySQLGui

def main():
    
    app = wx.App()
    frame = MySQLGui(parent=None, title="SQL Viewer", size=(960,480))
    frame.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()