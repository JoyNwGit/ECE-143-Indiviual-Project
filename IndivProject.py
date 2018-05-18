# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:49:11 2018

@author: Joy Nwarueze
"""
from PIL import Image, ImageDraw, ImageColor
import matplotlib.pyplot as plt
import numpy as np
import random as rand
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
    Does all the heavy lifting while it passes data to helper functions 
    to make measurements
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
    plt.figure(2)
    draw = ImageDraw.Draw(region)
    print "Adding Rectangle"
    fillcolor = ImageColor.getcolor("yellow", "RGB")
    outline = ImageColor.getcolor("gold", "RGB")
    xzero = rand.randint(0, X-1)
    yzero = rand.randint(0, Y-1)
    xone = rand.randint(xzero+1, X)
    yone = rand.randint(yzero+1, Y)
    print "Your rectangle coords are ({0},{1}) to ({2},{3})".format(xzero,yzero,xone,yone) 
    draw.rectangle(((xzero,yzero),(xone,yone)), fillcolor)
    plot = np.asarray(region)
    plt.imshow(plot) 
    
def add_Rect_To_SuperRect(num, sub_Area, xzero, yzero, xone, yone):
    return
    
def trim_Current_Rect(xzero,yzero, xone, yone):
    return
    
   
    

if __name__ == "__main__":
    X,Y = main()
    region = getRegion(X,Y)
    get_rect(region, X, Y)