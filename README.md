
Date: Nov. 11, 2021

Author: Allen Xiang

The two files both contain two classes: Point, PointList.

A Point object has three attributes: x, y, and pos.

x, y: x and y coordinates of the object in a two-dimensional space,

pos: the object's relation with other Point objects created from a given dataset.

A PointList object keeps a list of Point objects.
It provides methods for analyzing the Point objects.

Methods differ in datafit.py and datatrend.py.

datafit.py aims at making a piecewise linear regression of the dataset.

datatrend.py aims at finding significant turning points of the dataset.

To utilize the methods provided in each file, follow these steps:
1. Import the file.
2. Construct a PointList Object with two lists as input.
3. Call methods.

For more detailed explanations, please see docstrings in the files.
