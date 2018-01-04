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

    def __init__(self, pv, default=DEFAULT):
        self.default = default
        self.value = default
        self.stringvalue = str(default)
        self.pv = epics.PV(pv) if isinstance(pv, basestring) else pv
        self.pv.add_callback(self.onPVChanges)

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):
        print "onPVChanges"
        self.value = value
        self.stringvalue = ', '.join(map(str, self.value)) if self.pv.nelm > 1 else str(self.value)
        wx.CallAfter(self.updateContent)
       
    def updateContent(self): pass

    def getValue(self): return self.value
    def getPV(self): return self.pv


class PVTextUpdate(wx.StaticText, PVWidget):
    
    def __init__(self, parent, pv, **kw):
        cargs = PVWidget.processArgs(kw)
        PVWidget.__init__(self, pv, default=cargs['default'])
        wx.StaticText.__init__(self, parent, id=wx.ID_ANY, **kw)
        self.SetLabel(self.default)
       
    def updateContent(self): 
        self.SetLabel(self.stringvalue)

class PVDropdownList(wx.Choice, PVWidget):

    def __init__(self, parent, pv, writetopv=None, condition=lambda x: x!="", onSelection=None, **kw):

        cargs = PVWidget.processArgs(kw)
        PVWidget.__init__(self, pv, default=cargs['default'])
        wx.Choice.__init__(self, parent, id=wx.ID_ANY, **kw)
        self.condition = condition
        self.writetopv = writetopv

        if onSelection: self.Bind(wx.EVT_CHOICE, onSelection)
        else: self.Bind(wx.EVT_CHOICE, self.onSelection)

    def updateContent(self):
        wx.Choice.Clear(self)       
        for choice in list(filter(self.condition, self.value)): wx.Choice.Append(self, str(choice))

    def onSelection(self, event):
        if self.writetopv: self.writetopv.put(event.GetEventObject().GetStringSelection())

    def setWriteToPV(self, writetopv):
        self.writetopv = writetopv


class PiCaMonApp(wx.Frame):

    def __init__(self, prefix):

        self.prefix = prefix

        # prepare frame + main panel
        wx.Frame.__init__(self, None, wx.ID_ANY, "PiCaMon", size=(300, 150))
        panel = wx.Panel(self, wx.ID_ANY) 

        # create PV objects
        monitors_pv = epics.PV("%s:LIST:MONITOR" % self.prefix)
        cameras_pv = epics.PV("%s:LIST:CAMERA" % self.prefix)

        # create wx widgets
        self.monitors = PVDropdownList(panel, monitors_pv, onSelection=self.onMonitorSelection)
        self.cameras = PVDropdownList(panel, cameras_pv)

        # place in UI layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        monitors_list = monitors_pv.get()
        self.selected_pv = {}
        for monitor in list(filter(lambda x: x!="", monitors_list)):
            self.selected_pv[monitor] = epics.PV("%s:%s:CAMERA" % (self.prefix, monitor))

        # display the list of monitor/camera pairs
        for monitor in list(filter(lambda x: x!="", monitors_list)):
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(panel, label = monitor, style = wx.ALIGN_CENTRE)
            hbox.Add(st, 0, wx.ALL|wx.CENTER, 5) 
            tu = PVTextUpdate(panel, self.selected_pv[monitor])  
            hbox.Add(tu, 0, wx.ALL|wx.CENTER, 5)
            vbox.Add(hbox, 1, wx.ALL|wx.EXPAND)

        # dropdown lists to select monitor/camera. 
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.monitors, 0, wx.ALL|wx.CENTER, 5)
        hbox2.Add(self.cameras, 0, wx.ALL|wx.CENTER, 5)
        vbox.Add(hbox2, 1, wx.ALL|wx.EXPAND)
        
        panel.SetSizer(vbox)    

    def onMonitorSelection(self, event):
        monitor = event.GetEventObject().GetStringSelection()
        self.cameras.setWriteToPV(self.selected_pv[monitor])


if __name__ == '__main__':
    
    app = wx.App()
    PiCaMonApp("D100X").Show()
    app.MainLoop()
 