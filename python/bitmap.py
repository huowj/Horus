#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 21:43:46 2017

@author: hwj
"""

from PIL import Image
from pylab import *

#just a test 
im=array(Image.open("/hwj/yahoo/python/caixuan.jpeg").convert('L'))
#print(im.shape,im.dtype)
#print(im[100,100,0])
#print(im[100,100,1])


im2=255-im
im3=(100.0/255)*im+100
im4=255.0*(im/255.0)**2

subplot(221)
gray()
imshow(im)

subplot(222)
gray()
imshow(im2)

subplot(223)
gray()
imshow(im3)

subplot(224)
gray()
imshow(im4)

#test end


