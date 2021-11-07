#!/usr/bin/env python
# -*- coding:utf-8 -*-

__all__ = ('PointList')

class Point:

    def __init__(self):
        '''
        '''
        self.x = None
        self.y = None
        self.pos = None
        return

    def get_pos_name(self):
        '''Provides info of the position value.'''
        if self.pos == 0: return 'none'
        if self.pos == 1: return 'peak'
        if self.pos == -1: return 'bottom'
        return

    def __repr__(self):
        '''
        '''
        return self.__class__.__name__ + '(%r, %r, %r)'%(self.x, self.y, self.get_pos_name())

class PointList:

    def __init__(self):
        '''
        '''
        self.plist = []
        return

    def make_list(self, xlist, ylist):
        '''Creates a list of Point objects and calculates the rvalue of the
        linear regression line of peaks and bottoms'''
        
        # Record num of extremums and max differences of ydata and xdata.
        self.ex_num = 0
        self.ydiff = max(ylist) - min(ylist)
        self.xdiff = max(xlist) - min(xlist)

        ylen = len(ylist)
        prev = next = 0
        for i in range(ylen):
            point = Point()
            x = xlist[i]
            y = ylist[i]
            pos = 0
            if i > 0: prev = ylist[i-1]
            if i < ylen-1: next = ylist[i+1]

            # Determine local bottom.
            if prev > y and next > y:
                pos = -1
                self.ex_num += 1

            # Determine local peak.
            if prev < y and next < y:
                pos = 1
                self.ex_num += 1

            # Set point properties.
            point.x = x
            point.y = y
            point.pos = pos

            # Add point to plist.
            self.plist.append(point)

        return
        
    def set_turning_points(self, thresh):
        '''Creates a copy of plist, calculates turning points based on local 
        extremums and thresh, and sets the position values of the turnning 
        points to 2.'''

        pl = []
        p0 = self.plist[0]
        for p in self.plist:
            q = Point()
            q.x = p.x
            q.y = p.y
            q.pos = p.pos
            if q.pos != 0 and abs(q.pos+p0.pos) == 1:
                dy = q.y-p0.y
                dx = q.x-p0.x
                if abs(dy*dx) > thresh:
                    if q.pos == 1:
                        q.pos = 2
                    else: q.pos = -2
                    p0 = q
            pl.append(q)
            
        return pl

    def make_fit(self, thresh):
        '''Creates intervals based on updated position values and
        rthresh, and produces a line for each interval. Returns the
        number of lines to decide whether to update thresh.'''

        # Make a copy of plist and set turning points.
        pl = self.set_turning_points(thresh)
        num = 0

        # Create and record lines.
        self.lines = []
        p0 = pl[0]
        for i in range(len(pl)):
            p = pl[i]
            if abs(p.pos) == 2 or i == len(pl)-1:
                num += 1
                slope = (p.y-p0.y)/(p.x-p0.x)
                intercept = p.y-p.x*slope
                line = [p0.x, p.x, slope, intercept]
                self.lines.append(line)
                p0 = p
        # Return num of lines.
        return num

    def piecewise_fit(self, num_target=None, step=None):
        '''Calls make_fit to calculate intervals and create lines. Uses 
        default values for num_target and step if not provided, and updates
        thresh based on make_fit result.'''

        # Set num_target and step to default value if not provided.
        if num_target == None: n = (self.ex_num + 1)/2
        else: n = num_target
        if step == None: dstep = self.ydiff*self.xdiff/1000
        else: dstep = step

        # Call make_fit and update d to get n intervals and n lines.
        self.calls = 0
        cur_num = self.ex_num + 1
        d = 0
        while cur_num > 1:
            d += dstep
            cur_num = self.make_fit(d)
            self.calls += 1
            if cur_num <= n:
                break
        
        # Record final d value.
        self.dthresh = d

        return

    def __repr__(self):
        '''
        '''
        return self.plist.__repr__()

def main():
    xdata = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    ydata = [1000,2000,3000,5000,2500,500,2500,7000,6000,5400,5000,1000,2000,3000,5000,2500,500,2500,7000,6000,5400,5000]
    plist = PointList()
    plist.make_list(xdata, ydata)
    print(plist)
    print(plist.xdiff)
    print(plist.ydiff)
    print(plist.ex_num)
    plist.piecewise_fit()
    print(plist.lines)
    print(plist.dthresh)
    print(plist.calls)

if (__name__ == "__main__"):
    main()