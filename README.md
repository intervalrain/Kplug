# About KPlug
A simple macro for KLayout

# Manual
## Tool Bar
![toolbar](/images/toolbar.png)
+ AreaCal
  + Calculate the area with the selected layers. (overlapped area won't be summed up)
+ PerimeterCal
  + Calculate the perimeter length with the selected layers. (overlapped area won't be summed up)
+ DensityCal
  + Calculate the density with only two selected layers. 

+ ExportCoordinates
  + Export [85,0] database coordinates with top_cell, x_coordinate, y_coordinate, and rotation.

+ loadLyp
  + Load "default.csv" in ./pymacros directory.
  + Load self-define Layer Mapping and Data Type's naming with *.csv

# Copyright 
@author: [Rain Hu](https://intervalrain.github.io/posts/aboutme/)  
@email: [intervalrain@gmail.com](intervalrain@gmail.com)  
@github: [https://github.com/intervalrain](https://github.com/intervalrain)  
@website: [https://intervalrain.github.io](https://intervalrain.github.io)

# Version
+ Ver. 1.01 first version for area calculate function.
+ Ver. 1.02 separate "object calculate" and "region calculate".
+ Ver. 1.03 update "loadlyp" function.
+ Ver. 1.04 update "PerimeterCal", "DensityCal" and "ExportCoordinate", and set default.csv in the /pymacros as the default lyp.

# Reference
KLayout's Author: [Matthias Köfferlein](https://github.com/klayoutmatthias)