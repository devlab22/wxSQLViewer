# -*- coding: utf-8 -*-

import wx
import wx.grid as grid
import os
from sqlite_helper import MySqlite
from MyLoginDialog import MyLoginDialog

class MySQLGui(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        
        super(MySQLGui, self).__init__(*args, **kwargs)
        
        self.myTools = {
            "ID_OPEN_FILE": 1,
            "ID_TABLE": 2,
            "ID_DISCONNECT": 3
        }
        
        self.appTitle = self.GetTitle()
        self.dbName = ''
        self.SQLHelper = None
        self.table = None
        self.content = None
        self.InitUi()
        
    def InitUi(self):
        
        path = self.GetPath("images")
        self.SetIcon(wx.Icon(os.path.join(path,"db.png")))
        self.AddToolbar()
        
        splitter = wx.SplitterWindow(self, -1) 
        panel1 = wx.Panel(splitter, -1) 
        b = wx.BoxSizer(wx.HORIZONTAL) 
        
        self.CreateTableContent(panel1)
        b.Add(self.content, 1, wx.EXPAND) 
    
        panel1.SetSizerAndFit(b)
        
        panel2 = wx.Panel(splitter, -1) 
        self.CreateTable(panel2)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox1.Add(self.table,1,wx.EXPAND) 
        
        panel2.SetSizerAndFit(hbox1) 
        splitter.SplitVertically(panel2, panel1,500)
        
        self.SetToolsEnable()
        self.Layout()
        self.Center(wx.BOTH)

        dia = MyLoginDialog(parent=self, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER, title='Login')
        if(dia.ShowModal() == wx.ID_OK):
            data = dia.GetData()
            print(data)

    def AddToolbar(self):
        
        self.myToolbar = self.CreateToolBar()
        path = self.GetPath("images")
        
        openFile = self.myToolbar.AddTool(self.myTools["ID_OPEN_FILE"], "open file", wx.Bitmap(os.path.join(path,"open-folder.png")), "open file")
        self.Bind(wx.EVT_TOOL, self.OnOpenFile, openFile)
        
        getTable = self.myToolbar.AddTool(self.myTools["ID_TABLE"], "show table", wx.Bitmap(os.path.join(path,"find.png")), "show table")
        self.Bind(wx.EVT_TOOL, self.OnGetTable, getTable)
        
        self.myToolbar.AddSeparator()
        disconnectTool = self.myToolbar.AddTool(self.myTools["ID_DISCONNECT"], "disconnect", wx.Bitmap(os.path.join(path,"disconnect.png")), "disconnect")
        self.Bind(wx.EVT_TOOL, self.OnDisconnectDB, disconnectTool)
        
        self.myToolbar.Realize()
        
    def GetPath(self, folder=""):
        
        path = os.path.abspath(os.getcwd())
        if len(folder) > 0:
            path = os.path.join(path,folder)
        return path
        
    def OnOpenFile(self, event):
        
        path = self.GetPath()
        wildcard = "files (*.db,*.sqlite)|*.db;*.sqlite|" \
                   "All files (*.*)|*.*"
        
        with wx.FileDialog(self, "Open", path, "", wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL :
                return
            self.filename = fileDialog.GetPath()
            self.dbName = os.path.basename(self.filename)
            self.SetAppTitle()
            self.ConnectDB(self.filename)
            self.ClearTableContent()
        
    def SetAppTitle(self, tableName=''):
        
        title = self.appTitle
        
        if len(self.dbName) > 0:
            title = title + ': ' + self.dbName
            
        if len(tableName) > 0:
            title = title + ' - ' + tableName
            
        self.SetTitle(title)
    def OnGetTable(self,event):
        
        rows = self.table.GetSelectedRows()
        if len(rows) == 0:
            return
        
        line = (
            self.table.GetCellValue(rows[0],0),
            self.table.GetCellValue(rows[0],1),
            self.table.GetCellValue(rows[0],2)
        )
        
        self.SetTableContent(line)
        
    def OnSize(self, event):
        
        self.setColumnsWidth(self.GetClientSize())
        
    def CreateTable(self, parent):
        
        rows = 0
        cols = 3
        self.table = grid.Grid(parent)
        self.table.CreateGrid(rows, cols, wx.grid.Grid.GridSelectRows)
        self.table.EnableEditing(False)
        
        self.table.SetColLabelValue(0,'Type')
        self.table.SetColLabelValue(1,'Name')
        self.table.SetColLabelValue(2,'Description')
        self.table.SetColLabelSize(20)
        self.table.SetRowLabelSize(20)
        self.table.SetColSize(0,100)
        self.table.SetColSize(1,150)
        self.table.SetColSize(2,200)
        
    def CreateTableContent(self, parent):
        
        rows = 0
        cols = 0
        self.content = grid.Grid(parent)
        self.content.CreateGrid(rows, cols, wx.grid.Grid.GridSelectRows)
        self.content.EnableEditing(False)
        self.content.SetColLabelSize(20)
        self.content.SetRowLabelSize(20)
        
    def ConnectDB(self, dbName):
        
        self.SQLHelper = MySqlite(dbName)
        masterData = self.SQLHelper.getMasterData()
        self.RefreshTable(self.table)
        self.AppendData(masterData)
        self.SetToolsEnable()
        
    def RefreshTable(self, table:grid.Grid):
        
        rows = table.GetNumberRows()
        
        if rows > 0:
            table.DeleteRows(0,rows)
            
    def AppendData(self, data:list):
        
        for line in data:
            self.AppendLineData(line)
            
    def AppendLineData(self, line:tuple):
        
        rows = self.table.GetNumberRows()
        self.table.AppendRows()
        
        self.table.SetCellValue(rows,0,str(line[0]))
        self.table.SetCellValue(rows,1,str(line[1]))
        self.table.SetCellValue(rows,2,str(line[2]))
        
    def SetTableContent(self, line:tuple):
        
        if line[0] != 'table':
            return
        
        tableFields = self.SQLHelper.readTableFields(line[1])
        
        header = []
        for data in tableFields:
            header.append(data[1])
            
        self.SetColTableContent(header)
        
        tableContent = self.SQLHelper.readTable(line[1])
        self.AppendDataContent(tableContent)
        self.SetAppTitle(line[2])
        
    def SetColTableContent(self, header:list):
        
        self.RefreshTable(self.content)
        self.RemoveColTableContent()
        self.content.AppendCols(len(header))
        
        for index, col in enumerate(header):
            self.content.SetColLabelValue(index,col)
            
    def RemoveColTableContent(self):
        
        cols = self.content.GetNumberCols()
        if cols > 0:
            self.content.DeleteCols(0,cols)
            
    def AppendDataContent(self, data:list):
        
        for line in data:
            self.AppendLineContent(line)
            
    def AppendLineContent(self, line:tuple):
        
        row = self.content.GetNumberRows()
        cols = self.content.GetNumberCols()
        self.content.AppendRows()
        
        for col in range(cols):
            if col < len(line):
                self.content.SetCellValue(row,col,str(line[col]))
                
    def ClearTableContent(self):
        
        self.RefreshTable(self.content)
        self.RemoveColTableContent()
        
    def SetToolsEnable(self):
        
        enable = False
        
        if self.table.GetNumberRows() > 0:
            enable = True
            
        self.ToolBar.EnableTool(self.myTools["ID_TABLE"], enable)
        
        enable = False
        if self.SQLHelper != None:
            enable = True
            
        self.ToolBar.EnableTool(self.myTools["ID_DISCONNECT"], enable)
        
    def OnDisconnectDB(self,event):
        
        dia = wx.MessageDialog(self,"Do you want to disconnect from database?", "SQL Viewer",  wx.YES_NO | wx.ICON_QUESTION)
        
        if dia.ShowModal() == wx.ID_YES:
            self.RefreshTable(self.table)
            self.ClearTableContent()
            self.SQLHelper = None
            self.dbName = ''
            self.SetAppTitle()
            self.SetToolsEnable()
        