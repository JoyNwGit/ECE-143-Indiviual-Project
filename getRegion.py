# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:32:49 2018

@author: Joy Nwarueze
"""
def getRegion(X, Y):
    from PIL import Image, ImageDraw, ImageColor
    import matplotlib.pyplot as plt
    import numpy as np

    im = Image.new('RGB', (X,Y), (255,255,255))
    draw = ImageDraw.Draw(im)
    plot = np.asarray(im)
    
    plt.imshow(plot)