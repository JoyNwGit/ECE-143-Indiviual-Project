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
    print "Building Region"
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
        print 'tower index is {0}'.format(t.get_Index())
    count += 1
    draw.rectangle(t.get_Tower_Coords(), fillcolor)

    return t
    #plot = np.asarray(region)
    #plt.imshow(plot) 
    
    
def add_Rect_To_Total(rect, region):
    '''
    adds newest (and if necessary trimmed) rectangle to superset
    '''
    print 'adding rect to superset'
    plt.figure(3)
    superset[str(rect.get_Index())] = rect
    #print superset
    fillcolor = ImageColor.getcolor("gray", "RGB")
    draw = ImageDraw.Draw(region)
    draw.rectangle(rect.get_Tower_Coords(), fillcolor)
    return
    
def trim_Current_Rect(rect):
    '''
    Trims newest addition rectangle
    '''
    return
    
def check_For_Overlap(rect):
    return
   
    

if __name__ == "__main__":
    X,Y = main()
    global count
    count = 0
    superset = {}
    region = getRegion(X,Y)
    rect = get_rect(region, X, Y)
    #rect.get_Tower_Area()
    plot = np.asarray(region)
    plt.imshow(plot)
    if (rect.get_Index() == 0):
        add_Rect_To_Total(rect, region)
    print count
    plot = np.asarray(region)
    plt.imshow(plot) 
    
    