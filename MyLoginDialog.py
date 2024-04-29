# -*- coding: utf-8 -*-

import wx
import os

class MyLoginDialog(wx.Dialog):
    
    def __init__(self, params=None, *args, **kwargs):
        
        super(MyLoginDialog, self).__init__(*args, **kwargs)
        
        self.params = params
        self.InitUi()
        
    def GetValue4Key(self, key:str, default=None):
        
        if self.params is None:
            return None
        
        return self.params.get(key,default)
    
    def InitUi(self):
        
        path = self.GetValue4Key('icon', None)
        if path is not None:
            self.SetIcon(wx.Icon(path))
        panel = wx.Panel(self)
        
        mainVbox = wx.BoxSizer(wx.VERTICAL)
        
        self.loginInput = wx.TextCtrl(panel)
        self.loginInput.SetHint('Login')
        self.loginInput.Bind(wx.EVT_TEXT, self.OnValueChanged)
        
        mainVbox.Add(self.loginInput, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.passwordInput = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.passwordInput.SetHint('Password')
        self.passwordInput.Bind(wx.EVT_TEXT, self.OnValueChanged )
        
        mainVbox.Add(self.passwordInput, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.ipAddressInput = wx.TextCtrl(panel)
        self.ipAddressInput.SetHint('IP Address')
        self.ipAddressInput.SetValue('192.168.178.250')
        self.ipAddressInput.Bind(wx.EVT_TEXT, self.OnValueChanged)
        
        mainVbox.Add(self.ipAddressInput, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.process = wx.ComboBox(panel, value='AD', style=wx.CB_READONLY, choices=["AD", "Intern"], name="process")
        mainVbox.Add(self.process, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        mainVbox.AddSpacer(10)
        line = wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_HORIZONTAL)
        mainVbox.Add(line, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        
        buttonHBox = wx.BoxSizer(wx.HORIZONTAL)
        buttonHBox.AddSpacer(50)
        
        self.okButton = wx.Button(panel, wx.ID_OK, label='Ok')
        self.okButton.Disable()
        self.okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        buttonHBox.Add(self.okButton)
        
        cancelButton = wx.Button(panel, wx.ID_CANCEL, label='Cancel')
        cancelButton.Bind(wx.EVT_BUTTON, self.OnClose)
        buttonHBox.Add(cancelButton, flag=wx.LEFT, border=10)
        
        mainVbox.Add(buttonHBox, flag=wx.ALIGN_RIGHT|wx.TOP| wx.RIGHT, border=10)
        
        panel.SetSizer(mainVbox)
        mainVbox.Fit(panel)
        self.Layout()
        self.Center(wx.BOTH)

        self.loginInput.SetFocus()
        
    def GetPath(self, folder=""):
        
        path = os.path.abspath(os.getcwd())
        if len(folder) > 0:
            path = os.path.join(path,folder)
        return path
    
    def OnClose(self, event):
        
        if(event.EventObject.Id == wx.ID_OK and self.IsValuesValid() == False):
            return
        self.EndModal(event.EventObject.Id)
        
    def OnValueChanged(self, event):
        
        event.Skip()
        
        if(self.IsValuesValid()):
            self.okButton.Enable()
        else:
            self.okButton.Disable()
            
        
    def IsValuesValid(self):
        
        if len(self.loginInput.GetValue()) == 0  or len(self.passwordInput.GetValue()) == 0 or len(self.ipAddressInput.GetValue()) == 0:
            return False
        
        return True
    
    def GetData(self):
        
        return {
            "login": self.loginInput.GetValue(),
            "password": self.passwordInput.GetValue(),
            "ipAddress": self.ipAddressInput.GetValue(),
            "process": self.process.GetValue()
        }