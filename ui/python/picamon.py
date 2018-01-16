import sys
import wx
import epics.wx

prefix = "D100X"

def onCameraSelection(event):
    widget = event.GetEventObject()
    camera = widget.GetStringSelection()
    monitor = widget.GetName()
    epics.caput("%s:%s:CAMERA" % (prefix, monitor),"%s" % camera)

app = wx.App()

bigfont = wx.Font(24, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
boldfont = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
normalfont =  wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
smallfont =  wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)

frame = wx.Frame(None, -1, 'PiCaMon', size=(350, 250))
panel = wx.Panel(frame, -1)
vbox = wx.BoxSizer(wx.VERTICAL)

#header with name and logo
header = wx.BoxSizer(wx.HORIZONTAL)

name = wx.StaticText(panel, label = "PiCaMon", style = wx.ALIGN_CENTRE)
name.SetFont(bigfont)
header.Add(name, wx.ALL|wx.CENTER, 5)

img = wx.Bitmap.ConvertToImage(wx.Bitmap("./picamon.png")).Scale(75,75, wx.IMAGE_QUALITY_HIGH)
logo = wx.Bitmap(img)
logo_widget = wx.StaticBitmap(panel, -1, logo, (10, 5), (logo.GetWidth(), logo.GetHeight()))
header.Add(logo_widget, wx.ALL|wx.RIGHT, 5)

vbox.Add(header)

# get the list of monitors
monitor_pv = epics.PV("%s:LIST:MONITOR" % prefix)
if monitor_pv.wait_for_connection() == False: 
    print "Cannot connect to PVs"
    sys.exit(1)



for monitor in list(filter(lambda x: x!="", monitor_pv.get())):

    hbox = wx.BoxSizer(wx.HORIZONTAL)

    three = wx.StaticText(panel, label = monitor, style = wx.ALIGN_CENTRE)
    three.SetFont(boldfont)
    hbox.Add(three, 0, wx.ALL|wx.CENTER, 5)

    five = wx.Choice(panel, id=wx.ID_ANY, name=monitor)
    five.SetFont(normalfont)
    five.Bind(wx.EVT_CHOICE, onCameraSelection)
    camera_pv = epics.PV("%s:LIST:CAMERA" % prefix)
    for camera in list(filter(lambda x: x!="", camera_pv.get())): five.Append(str(camera))
    hbox.Add(five, 0, wx.ALL|wx.CENTER, 5)

    four = epics.wx.PVText(panel, pv="%s:%s:CAMERA" % (prefix, monitor), fg=wx.Colour(0,0,255))
    four.SetFont(smallfont)

    epics.poll()
    hbox.Add(four, 0, wx.ALL|wx.CENTER, 5)

    vbox.Add(hbox, 1, wx.ALL|wx.EXPAND)

panel.SetSizer(vbox)

frame.Show()
app.MainLoop()


 