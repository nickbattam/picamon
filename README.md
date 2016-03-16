
# PiCaMon

A Raspberry Pi based camera monitoring system. The idea is to be able to display EPICS camera feed (based on AreaDetector) on Raspberry Pi controlled monitors from a remote interface.

## Concept

[![Concept](https://j.gifs.com/82Ozxr.gif)](https://www.youtube.com/watch?v=pTWhWKSA5Z8)

## Setup overview

```
+-----------------------------+           +---------+     +--------------------+    
| CAMERA 1                    |           |         |     | MONITOR 1          |    
|  IOC: CAM1                  |           |         |     |  IP: 192.168.2.2   +<--+
|  PVs: :xsize                +---------->+         +---->+  ID: MON1          |   |
|       :ysize                |           |         |     |                    |   |
|       :arrayData            |           |         |     +--------------------+   |
+-----------------------------+           |         |                              |
                                          |         |                              |
+-----------------------------+           | SWITCH  |     +--------------------+   |
| CAMERA 2                    |           |         |     | MONITOR 2          |   |
|  IOC: CAM2                  |           |         |     |  IP: 192.168.2.3   +<--+
|  PVs: :xsize                +---------->+         +---->+  ID: MON2          |   |
|       :ysize                |           |         |     |                    |   |
|       :arrayData            |           |         |     +--------------------+   |
+-----------------------------+           |         |                              |
                                          |         |                              |
+-----------------------------+           |         |     +--------------------+   |
| CAMERA M                    +---------->+         +---->+ MONITOR N          +<--+
+-----------------------------+           +---------+     +--------------------+   |
                                                                                   |
             +-----------+            +---------------------------------------+    |
             |           |            | CONTROLLER                            |    |
             |    GUI    +<---------->+  IOC: CONTROLLER                      +----+
             |           |            |  PVs: <monID> = <cameraIOC>           |
             +-----------+            |       <monID>:RATE = refresh rate(Hz) |
                                      |       <monID>:COLMAP = colourmap name |
                                      |       COLORMAPS = list of all colmaps |
                                      +---------------------------------------+
```
