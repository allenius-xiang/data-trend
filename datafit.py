#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scipy import stats
from pwlf import PiecewiseLinFit as pf

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
        self.rvalue = 0
        return

    def make_list(self, xlist, ylist):
        '''Creates a list of Point objects and calculates the rvalue of the
        linear regression line of peaks and bottoms'''
        
        ylen = len(ylist)

        # Makes lists for recording local extremums.
        xpl = []
        ypl = []

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
                xpl.append(x)
                ypl.append(y)

            # Determine local peak.
            if prev < y and next < y:
                pos = 1
                xpl.append(x)
                ypl.append(y)

            # Set point properties.
            point.x = x
            point.y = y
            point.pos = pos

            # Add point to plist.
            self.plist.append(point)

        # Calculate rvalue of linear regression line of local extremums.
        self.rvalue = stats.linregress(xpl, ypl).rvalue

        return
        
    
    def set_turning_points(self, rthresh):
        '''Creates a copy of plist, calculates turning points based on local 
        extremums and rthresh, and sets the position values of the turnning 
        points to 2.'''

        # Create a copy of plist.
        pl = []
        length = len(self.plist)
        prev = i = pi = 0

        while i < length:
            if prev != None:
                # Create new lists for x, y of local extremums.
                xl = []
                yl = []
            for j in range(i, length):
                # Copy Points from plist.
                p = self.plist[j]
                q = Point()
                q.x = p.x
                q.y = p.y
                q.pos = p.pos
                i += 1
                # Add x, y of local extremums to lists.
                if q.pos != 0:
                    xl.append(q.x)
                    yl.append(q.y)
                    # Calculate regression line of current interval if interval is large enough.
                    if len(yl) > 2:
                        result = stats.linregress(xl, yl)
                        r = abs(result.rvalue)
                    else:
                        result = None
                        r = 0
                    # Stop adding if ravlue of regression line is too small.
                    if r < rthresh and r != 0:
                        del xl[-1]
                        del yl[-1]
                        break
                    # Record result and set pos of end point of interval to 2.
                    prev = result
                    if prev != None and i-pi > 2 and length-i > 2:q.pos = 2
                    pi = i
                pl.append(q)

        return pl

    def make_fit(self, rthresh):
        '''Creates intervals based on updated position values and
        rthresh, and produces a best-fit line for each interval.
        Returns the number of lines to decide whether to update
        rthresh.'''

        pl = self.set_turning_points(rthresh)
        xdata = []
        ydata = []
        breaks = [pl[0].x]

        # Set breakpoints for pwlf.
        for p in pl:
            xdata.append(p.x)
            ydata.append(p.y)
            if p.pos == 2:
                breaks.append(p.x)
        breaks.append(pl[-1].x)

        self.lines = []

        # Uses pwlf module to make lines.
        fit = pf(xdata, ydata)
        fit.fit_with_breaks(breaks)
        slopes = fit.slopes
        intercepts = fit.intercepts
        num = fit.n_segments
        ssr = fit.ssr
        # Get properties of the lines.
        for i in range(len(breaks)-1):
            start = breaks[i]
            end = breaks[i+1]
            slope = slopes[i]
            intercept = intercepts[i]
            line = [start, end, slope, intercept, ssr]
            self.lines.append(line)

        # Return num of lines.
        return num

    def piecewise_fit(self, rthresh=None):
        '''Calls make_fit to calculate intervals and stats of regression lines.
        Uses default value for rthresh if not provided, and updates rthresh
        based on make_fit result.'''

        # Set rthresh to default value if not provided.
        if rthresh == None: r = abs(self.rvalue)
        else: r = rthresh

        self.calls = 0
        # Call make_fit and update r based on result.
        cur_r = r
        min_num = len(self.plist)
        param = min_num/abs(self.rvalue)/100
        while r <= 1:
            r += 0.01
            cur_num = self.make_fit(r)
            self.calls += 1
            if param < cur_num < min_num:
                min_num = cur_num
                cur_r = r
        
        # Record final rthresh value.
        self.num_intervals = self.make_fit(cur_r)
        self.rthresh = round(cur_r, 2)
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
    plist.piecewise_fit()
    print(plist.lines)
    print(plist.rthresh)
    print(plist.calls)

if (__name__ == "__main__"):
    main()