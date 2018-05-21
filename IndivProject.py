# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:49:11 2018

@author: Joy Nwarueze
"""
from PIL import Image, ImageDraw, ImageColor
import matplotlib.pyplot as plt
import numpy as np
import random as rand
import Tower

global superset
global count
global area_Remaining
global area_Covered
global num_Figures

def main():
    print 'hello world'
    while True:
        try:
            X,Y = input(
                    "How large do you want your region to be? (X,Y) in integers, however to plot correctly these conditions apply, X >=4 and Y >=5: \n")
            assert isinstance(X,int) and isinstance(Y, int) and (X >=4) and (Y>=5)
        except ValueError:
           print("Sorry, I didn't understand that.")
           continue
        except AssertionError:
           print("One or more of your values was not an integer, or under the specified range")
        else:
               break
    print "The size of your region will be: {0} by {1} ".format(X,Y)
    return X,Y
    
def getRegion(X, Y):
    '''
    Builds the starting region
    '''
    #print "Building Region"
    region = Image.new('RGB', (X,Y), (255,255,255))
    plt.figure(1)
    plot = np.asarray(region)
    plt.imshow(plot)  
    #returns final image
    plot = np.asarray(region)
    plt.imshow(plot)    
    return region

def get_rect(region, X, Y):
    '''
    creates a new tower with coords, draws it and returns the tower
    '''
    global count
    plt.figure(2)
    draw = ImageDraw.Draw(region)
    print "Adding Rectangle"
 
    fillcolor = ImageColor.getcolor("lightgreen", "RGB")
    xzero = rand.randint(0, X-1)
    yzero = rand.randint(0, Y-1)
    xone = rand.randint(xzero+1, X)
    yone = rand.randint(yzero+1, Y)
    print "Your rectangle coords are ({0},{1}) to ({2},{3})".format(xzero,yzero,xone,yone) 
    t = Tower.Tower(xzero, yzero,xone,yone)
    if (t.get_Index() == -1):
        t.set_Index(count)
        print '-----tower index is {0}-----'.format(t.get_Index())
    count += 1
    draw.rectangle(t.get_Tower_Coords(), fillcolor)
    return t
    
    
def add_Rect_To_Total(rect, region):
    '''
    adds newest (and if necessary trimmed) rectangle to superset
    '''
    global superset
    print 'adding rect to superset'
    #plt.figure(num_Figures) #3
    superset[str(rect.get_Index())] = rect
    #print superset
    fillcolor = ImageColor.getcolor("gray", "RGB")
    draw = ImageDraw.Draw(region)
    draw.rectangle(rect.get_Tower_Coords(), fillcolor)
    return
    
def trim_Current_Rect(rect, check_Rect):
    '''
    Trims newest addition rectangle
    '''
    print "Trimming a rect"
    print "index of rectangle violated: {0}".format(check_Rect.get_Index())
    top_Violated = False
    bot_Violated = False
    left_Violated = False
    right_Violated = False
    if (rect.xleft < check_Rect.xright and rect.xright > check_Rect.xright):
        print "Right violation"
        right_Violated = True
    if (rect.xright > check_Rect.xleft and rect.xleft < check_Rect.xleft):
        print "left violation"
        left_Violated = True
    if (rect.ytop > check_Rect.ybot and rect.ybot < check_Rect.ybot):
        print "Bot violation"
        bot_Violated = True
    if (rect.ybot < check_Rect.ytop and rect.ytop > check_Rect.ytop):
        print "Top violation"
        top_Violated = True
    
    #so original rect remains untouched until measurements complete
    vcopy_Rect = Tower.Tower(rect.xzero, rect.yzero, rect.xone, rect.yone)
    vcopy_Rect.set_Index(rect.get_Index())
    hcopy_Rect = Tower.Tower(rect.xzero, rect.yzero, rect.xone, rect.yone)
    hcopy_Rect.set_Index(rect.get_Index())
    
    vtrim = False
    htrim = False
    
    if (left_Violated or right_Violated):
        htrimmed_Rect = trim_Horiz_Overlap(
                vcopy_Rect, check_Rect, left_Violated,right_Violated)
        htrim = True
    if (top_Violated or bot_Violated):
        vtrimmed_Rect = trim_Vertical_Overlap(
                hcopy_Rect, check_Rect, top_Violated, bot_Violated)
        vtrim = True

    if (vtrim and htrim):
        print 'vertical trim and horiz trim made'
        if (vtrimmed_Rect.get_Tower_Area() >= htrimmed_Rect.get_Tower_Area()):
            trimmed_Rect = vtrimmed_Rect
        else:
            trimmed_Rect = htrimmed_Rect
    elif (vtrim):
        print 'only vertical trim made'
        trimmed_Rect = vtrimmed_Rect
    elif (htrim):
        print 'only horiz trim made'
        trimmed_Rect = htrimmed_Rect
    else:
        print 'should not be here? might be completely encompassed'
        print 'So turn it into a rect with no length or width'
        trimmed_Rect = Tower.Tower(rect.xone, rect.yone, rect.xone, rect.yone)
    return trimmed_Rect

def trim_Horiz_Overlap(rect, check_Rect, left_Violated, right_Violated):
    print 'Trimming Horizontally'
    if (right_Violated):
        print 'check_Rect violated on the right'
    if (left_Violated):
        print 'check_Rect violated on the left'
    return rect#htrim_Area,htrimmed_Rect

def trim_Vertical_Overlap(rect, check_Rect, top_Violated, bot_Violated):
    
    if (top_Violated):
        print 'check rect has top violated'
    if (bot_Violated):
        print 'check rect has bot violated'
    
    return rect#vtrim_Area,vtrimmed_Rect
    
def check_For_Overlap(rect):
    '''
    if there is a horizontal AND vertical overlap
    '''
    index = 0
    collisions = 0
    while index < len(superset):
        hoverlaps = True
        voverlaps = True
        check_Rect = superset[str(index)]
        if (rect.xleft >= check_Rect.xright) or (rect.xright <= check_Rect.xleft):
            hoverlaps = False
        if (rect.ytop <= check_Rect.ybot) or (rect.ybot >= check_Rect.ytop):
            voverlaps = False
        index +=1
        if (hoverlaps and voverlaps):
            collisions+=1
            print "num of collisions detected is now {0}".format(collisions)
            print "The rectangle is touching the superset"
            rect = trim_Current_Rect(rect, check_Rect) #assume trimmed in that location
    return
   
    

if __name__ == "__main__":
    #TODO - remember to add () to end of functions
    X,Y = main()
    global count
    global superset
    global area_Remaining
    global area_Covered
    global num_Figures
    num_Figures = 1
    area_Covered = 0
    count = 0 #starts indexing each rect
    superset = {} #initializes the total claimed area
    region = getRegion(X,Y)
    area_Remaining = X*Y
    #start filling with rectangles
    i = 0 #run 10 times 
    while (i<10 and area_Remaining >0):
        i +=1
        rect = get_rect(region, X, Y)
        # plot of before added to superset
        
        plot = np.asarray(region)
        plt.figure(num_Figures)
        plt.imshow(plot)
        if (rect.get_Index() == 0):
            add_Rect_To_Total(rect, region)
        else:
            check_For_Overlap(rect)
            #print 'index of trimmed rect is {0}'.format(rect.get_Index())
            add_Rect_To_Total(rect, region)
        area_Remaining = area_Remaining - rect.get_Tower_Area()
        area_Covered += rect.get_Tower_Area()   
        print 'current number of rectangles: {0}'.format(count)
        #plot of after added to superset
        num_Figures +=1
        plot = np.asarray(region)
        plt.figure(num_Figures)
        plt.imshow(plot) 
        
    
    