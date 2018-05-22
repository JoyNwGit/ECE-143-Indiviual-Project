# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:49:11 2018

@author: Joy Nwarueze

This is a python script that adds random rectangles of various sizes and
locations to a region specified by the user. Each new rectangle appears as 
green then changes to gray when integrated into the total coverage area.

Note:
    Because of ImageDraw, you'll notice that the axes are slightly shifted
     - You'll see a coordinate that looks like (6.5, 3.5) for example, that's because
     ImageDraw draws by pixel rather than exact values. In other words - Round down 
     where you think the coordinate is unless it's showing below 0 (another problem with ImageDraw)
     because in that case round up
     
**Major Note**:
    ImageDraw draws the axes upside down on the region. It follows the format of a 2-D array
    where [0][0] is top left rather than bottom left. This is really confusing to the eyes on
    which ends are trimmed so it's easier to not output that information to the user and instead
    just show the trim.


Terminology that might be unclear:
    region - its the plot image of size X by Y. Think of it as the background without the rectangles 
    
    plot - its the grid that the plot image is using. Plot is attached to region
    so it can manipulate it
    
    superset - Its the accumulated tower coverage (after trimming where necessary)
    
"""
import PIL
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
    '''
    This function just takes in valid user input
    
    @return X,Y: int - The length (X) and width (Y) of the region
    '''
    #print 'hello world'
    while True:
        try:
            X,Y = input(
                    "How large do you want your region to be? (X, Y) in integers, however to plot correctly these conditions apply, X (length) >=4 and Y (width) >=5: \n")
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
    
    @param X,Y: int - The length (X) and width (Y) of the region
    @return region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    #print "Building Region"
    assert isinstance(X,int) and isinstance(Y, int) and (X >=4) and (Y>=5)
    region = Image.new('RGB', (X,Y), (255,255,255))  
    assert isinstance(region, PIL.Image.Image)
    return region

def get_rect(region, X, Y):
    '''
    Creates a new tower (in the form of a rectangle) with random coords, draws it (but doesn't plot it) and returns the tower
    
    @param X,Y:  int - The length (X) and width (Y) of the region
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    @return t: Tower instance - returns a tower of a random size and specified index
    '''
    assert isinstance(region, PIL.Image.Image)
    assert isinstance(X,int) and isinstance(Y, int) and (X >=4) and (Y>=5)
    global count
    assert isinstance(count, int)
    #plt.figure(2)
    draw = ImageDraw.Draw(region)
    #print "Adding Rectangle"
 
    fillcolor = ImageColor.getcolor("lightgreen", "RGB")
    xzero = rand.randint(0, X-1)
    yzero = rand.randint(0, Y-1)
    xone = rand.randint(xzero+1, X)
    yone = rand.randint(yzero+1, Y)
    #print "Your rectangle coords are ({0},{1}) to ({2},{3})".format(xzero,yzero,xone,yone) 
    t = Tower.Tower(xzero, yzero,xone,yone)
    if (t.get_Index() == -1):
        t.set_Index(count)
        #print '-----tower index is {0}-----'.format(t.get_Index())
    count += 1
    draw.rectangle(t.get_Tower_Coords(), fillcolor)
    return t
    
    
def add_Rect_To_Total(rect, region):
    '''
    Adds newest (and if necessary trimmed) rectangle to superset
    
    @param rect: Tower - instance of a Tower class
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    assert isinstance(region, PIL.Image.Image)
    global superset
    assert isinstance(superset, dict)
    #print 'adding rect to superset'
    #plt.figure(num_Figures) #3
    superset[str(rect.get_Index())] = rect
    #print superset
    #fillcolor = ImageColor.getcolor("lightgreen", "RGB")
    draw = ImageDraw.Draw(region)
    #draw.rectangle(rect.get_Tower_Coords(), fillcolor)
    fillcolor = ImageColor.getcolor("gray", "RGB")
    draw.rectangle(rect.get_Tower_Coords(), fillcolor)
    return
    


def trim_Current_Rect(rect, check_Rect, region):
    '''
    Trims newest addition rectangle when there is an overlap or completely encompassed by superset coverage.
    Where edge comparisons are made to determine where to trim
    
    @param rect: Tower - instance of a Tower class
    @param check_Rect: Tower - instance of a Tower class found in superset to compare against
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    
    @return trimmed_Rect: Tower - It's the input rectangle but scaled back along specific edges
    '''
    assert isinstance(region, PIL.Image.Image)
    #print "Trimming a rect"
    #print "index of rectangle violated: {0}".format(check_Rect.get_Index())
    top_Violated = False
    bot_Violated = False
    left_Violated = False
    right_Violated = False
    if (rect.xleft < check_Rect.xright and rect.xright > check_Rect.xright):
        right_Violated = True
    if (rect.xright > check_Rect.xleft and rect.xleft < check_Rect.xleft):
        left_Violated = True
    if (rect.ytop > check_Rect.ybot and rect.ybot < check_Rect.ybot):
        bot_Violated = True
    if (rect.ybot < check_Rect.ytop and rect.ytop > check_Rect.ytop):
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
        #print 'vertical trim and horiz trim made'
        if (vtrimmed_Rect.get_Tower_Area() >= htrimmed_Rect.get_Tower_Area()):
            trimmed_Rect = vtrimmed_Rect
        else:
            trimmed_Rect = htrimmed_Rect
    elif (vtrim):
        #print 'only vertical trim made'
        trimmed_Rect = vtrimmed_Rect
    elif (htrim):
        #print 'only horiz trim made'
        trimmed_Rect = htrimmed_Rect
    else:
        #print '^^^might be completely encompassed^^^'
        #print 'So turn it into a rect with no length or width'
        trimmed_Rect = Tower.Tower(rect.xone, rect.yone, rect.xone, rect.yone)
        trimmed_Rect.set_Index(vcopy_Rect.get_Index())
        
    #show_Plot(region)
    return trimmed_Rect





def trim_Horiz_Overlap(rect, check_Rect, left_Violated, right_Violated):
    '''
    Helper function for trim_Current_Rect: Trims a rectangle horizontally and returns it
    
    @param rect:  Tower - instance of a Tower class
    @param check_Rect: Tower - instance of a Tower class found in superset to compare against
    @param left_Violated, right_Violated: Boolean - True when that spefic edge of the check_Rect is violated
    
    @return rect: Tower - instance of a Tower class but trimmed along the opposite violated edge
     --> left_violation of check_Rect means scale back right side of rect
    
    '''
    assert isinstance(left_Violated, bool) and isinstance(right_Violated, bool)
    #print 'Trimming Horizontally'
    if (right_Violated and left_Violated):
        vertical_Delta = rect.yone-rect.yzero
        right_Delta = rect.xone - check_Rect.xone
        left_Delta = check_Rect.xzero - rect.xzero
        left_Area = left_Delta*vertical_Delta
        right_Area = right_Delta*vertical_Delta
        if (right_Area >= left_Area):
            #scale back back left 
            rect.xzero = check_Rect.xone
        else:
            #scale back right
            rect.xone = check_Rect.xzero
    elif (right_Violated):
        #print 'check_Rect violated on the right so scale back rect left'
        rect.xzero = check_Rect.xone
    elif (left_Violated):
        #print 'check_Rect violated on the left so scale back rect right'
        rect.xone = check_Rect.xzero
    return rect

def trim_Vertical_Overlap(rect, check_Rect, top_Violated, bot_Violated):
    '''
    Helper function for trim_Current_Rect: Trims a rectangle vertically and returns it
    
    @param rect:  Tower - instance of a Tower class
    @param check_Rect: Tower - instance of a Tower class found in superset to compare against
    @param top_Violated, bot_Violated: Boolean - True when that spefic edge of the check_Rect is violated
    
    @return rect: Tower - instance of a Tower class but trimmed along the opposite violated edge
     --> top_violation of check_Rect means scale back bottom side of rect
    '''
    assert isinstance(top_Violated, bool) and isinstance(bot_Violated, bool)
    if (top_Violated and bot_Violated):
        horiz_Delta = rect.xone-rect.xzero
        top_Delta = rect.yone - check_Rect.yone
        bot_Delta = check_Rect.yzero - rect.yzero
        top_Area = top_Delta*horiz_Delta
        bot_Area = bot_Delta*horiz_Delta
        if (top_Area >= bot_Area):
            #sclae back bot
            rect.yzero = check_Rect.yone
        else:
            #scale back top
            rect.yone = check_Rect.yzero 
    elif (top_Violated):
        #print 'check rect has top violated - scale back rect bot'
        rect.yzero = check_Rect.yone
    elif (bot_Violated):
        #print 'check rect has bot violated - scale back rect top'
        rect.yone = check_Rect.yzero
    return rect
    
def check_For_Overlap(rect, region):
    '''
    Checks if there is a horizontal AND vertical overlap meaning the rectangle overlaps another
    superset rectangle
    
    @param rect:  Tower - instance of a Tower class
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    
    @return rect: Tower - Either the trimmed version of the rectangle if an overlap was found, or the original rectangle
    '''
    assert isinstance(region, PIL.Image.Image)
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
            #print "num of collisions detected is now {0}".format(collisions)
            #print "The rectangle is touching the superset"
            recolor_Rect_White(rect, region)
            rect = trim_Current_Rect(rect, check_Rect, region) #returns trimmed Rect area
            recolor_Trimmed_Rect_Green(rect, region)
            recolor_check_Rect_Gray(check_Rect, region)
    return rect
   
def show_Plot(region):
    '''
    Plots the region with the drawn rectangles on a new figure window. Called when the final output needs to be seen
    
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    assert isinstance(region, PIL.Image.Image)
    global num_Figures
    plot = np.asarray(region)
    plt.figure(num_Figures)
    plt.imshow(plot) 
    num_Figures +=1
    return
    
def recolor_Rect_White(rect, region):
    '''
    Once a rectangle overlaps check_Rect (the rectangle to check against), whiteout offending rectangle.
    This is used to draw over the original green rectangle that each new rectangle starts with to match 
    the background color.
    
    @param rect:  Tower - instance of a Tower class
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    #print 'Whiting out newest rectangle'
    assert isinstance(region, PIL.Image.Image)
    draw = ImageDraw.Draw(region)
    fillcolor = ImageColor.getcolor("white", "RGB")
    draw.rectangle(rect.get_Tower_Coords(), fillcolor)
    #show_Plot(region)
    return

def recolor_Trimmed_Rect_Green(trimmed_Rect, region):
    '''
    Recolors the trimmed rectangle green. 
    
    @param trimmed_Rect:  Tower - The trimmed version of the overlapping rectangle
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    assert isinstance(region, PIL.Image.Image)
    draw = ImageDraw.Draw(region)
    fillcolor = ImageColor.getcolor("lightgreen", "RGB")
    draw.rectangle(trimmed_Rect.get_Tower_Coords(), fillcolor)
    show_Plot(region)
    #print 'coloring in trimmed rect'
    return

def recolor_check_Rect_Gray(check_Rect, region):
    '''
    Recolors the overlapped check_Rect (the rectangle to check against) to gray.
    This is meant to make it look like the superset takes precedence on the region
    
    @param check_Rect: Tower - instance of a Tower class found in superset to compare against
    @param region: PIL.Image.Image - Its a background image based off a length, width and (R,G,B) color pallete (set to white)
    '''
    assert isinstance(region, PIL.Image.Image)
    draw = ImageDraw.Draw(region)
    fillcolor = ImageColor.getcolor("gray", "RGB")
    draw.rectangle(check_Rect.get_Tower_Coords(), fillcolor)
    show_Plot(region)
    #print 'coloring in the overlapped rect'
    return 

if __name__ == "__main__":
    #TODO - remember to add () to end of functions
    '''
    Runs the program once. Things to keep in mind: 
        - Program might hang on first run-through. Why? I don't know but runs 
        pretty fine each time after I believe
        - Hit Ctrl+C if it hangs or whatever key binding force stops a running program
    '''
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
    total_Area = X*Y
    percent_Covered = 0
    plt.close('all')
    print "Percentage of region covered: {0}".format(percent_Covered)
    show_Plot(region)
    #start filling with rectangles
    i = 0 #run n times. Less than 10 for DEBUG 
    while (area_Remaining >0 and percent_Covered < 75):
        i +=1
        rect = get_rect(region, X, Y)
        # plot of before added to superset
        show_Plot(region)
        if (rect.get_Index() == 0):      
            add_Rect_To_Total(rect, region)
        else:
            rect = check_For_Overlap(rect, region)   
            add_Rect_To_Total(rect, region)
        show_Plot(region)
        area_Remaining = area_Remaining - rect.get_Tower_Area()
        area_Covered += rect.get_Tower_Area()   
        percent_Covered = float(float(area_Covered)/float(total_Area))*100
        print 'current number of rectangles: {0}'.format(count)
        print "Percentage of region covered: {0:.1f}%".format(percent_Covered)
        print "{0} units of area remaining out of {1}".format(area_Remaining, total_Area)
    
    