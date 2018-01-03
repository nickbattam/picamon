import wx
import epics
import time

class PVWidget():

    DEFAULT = "..."

    @staticmethod
    def processArgs(args):
        d = {}
        d['default'] = args.pop('default', PVWidget.DEFAULT)
        return d

    def __init__(self, pvname, default=DEFAULT):
        self.pvname = pvname
        self.default = default
        self.value = default
        self.stringvalue = str(default)
        self.pv = epics.PV(pvname)
        self.pv.add_callback(self.onPVChanges)

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):
        #print "onPVChanges"
        self.value = value
        self.stringvalue = ', '.join(map(str, self.value)) if self.pv.nelm > 1 else str(self.value)
        wx.CallAfter(self.updateContent)
       
    def updateContent(self): pass

    def getValue(self): return self.value
    def getPV(self): return self.pv
    def getPVname(self): return self.pvname


class PVTextUpdate(wx.StaticText, PVWidget):
    
    def __init__(self, parent, pvname, **kw):
        cargs = PVWidget.processArgs(kw)
        PVWidget.__init__(self, pvname, default=cargs['default'])
        wx.StaticText.__init__(self, parent, id=wx.ID_ANY, **kw)
        self.SetLabel(self.default)
       
    def updateContent(self): 
        self.SetLabel(self.stringvalue)

class PVDropdownList(wx.Choice, PVWidget):

    def __init__(self, parent, pvname, writetopv=None, condition=lambda x:True, onSelection=None, **kw):

        cargs = PVWidget.processArgs(kw)
        PVWidget.__init__(self, pvname, default=cargs['default'])
        wx.Choice.__init__(self, parent, id=wx.ID_ANY, **kw)
        self.condition = condition
        self.writetopv = writetopv

        if onSelection: self.Bind(wx.EVT_CHOICE, onSelection)
        else: self.Bind(wx.EVT_CHOICE, self.onSelection)

    def updateContent(self):
        #print "update content"
        wx.Choice.Clear(self)       
        for choice in list(filter(lambda x: x!="", self.value)): wx.Choice.Append(self, str(choice))

    def onSelection(self, event):
        #print "onselection"
        if self.writetopv: epics.PV(self.writetopv).put(self.GetStringSelection())

    def setWriteToPV(self, writetopv):
        self.writetopv = writetopv


class PiCaMonApp(wx.Frame):

    def __init__(self, prefix):

        self.prefix = prefix
        self.selectedMonitor = None

        wx.Frame.__init__(self, None, wx.ID_ANY, "PiCaMon", size=(300, 150))
        panel = wx.Panel(self, wx.ID_ANY) 
        vbox = wx.BoxSizer(wx.VERTICAL)

        monitors = epics.caget("%s:LIST:MONITOR" % self.prefix)

        # display the list of monitor/camera pairs
        for monitor in list(filter(lambda x: x!="", monitors)):
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(panel, label = monitor, style = wx.ALIGN_CENTRE)
            hbox.Add(st, 0, wx.ALL|wx.CENTER, 5)
            tu = PVTextUpdate(panel, "%s:%s:CAMERA" % (self.prefix,monitor))   
            hbox.Add(tu, 0, wx.ALL|wx.CENTER, 5)
            vbox.Add(hbox, 1, wx.ALL|wx.EXPAND)

        # dropdown lists to select monitor/camera. 
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.monitors = PVDropdownList(panel, "%s:LIST:MONITOR" % self.prefix, onSelection=self.onMonitorSelection, condition=lambda x: x!="")
        hbox2.Add(self.monitors, 0, wx.ALL|wx.CENTER, 5)

        self.cameras = PVDropdownList(panel, "%s:LIST:CAMERA" % self.prefix, condition=lambda x: x!="")
        hbox2.Add(self.cameras, 0, wx.ALL|wx.CENTER, 5)

        vbox.Add(hbox2, 1, wx.ALL|wx.EXPAND)
        panel.SetSizer(vbox)    

    def onMonitorSelection(self, event):
        self.cameras.setWriteToPV("%s:%s:CAMERA" % (self.prefix, event.GetEventObject().GetStringSelection()))


if __name__ == '__main__':
    
    app = wx.App()
    PiCaMonApp("D100X").Show()
    app.MainLoop()
 