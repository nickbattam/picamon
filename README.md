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
             +-----------+            +---------------------------------+          |
             |           |            | CONTROLLER                      |          |
             | INTERFACE +<---------->+  IOC: CONTROLLER                +----------+
             |           |            |  PVs: <monitorID> = <cameraIOC> |           
             +-----------+            |                                 |           
                                      +---------------------------------+           
```
