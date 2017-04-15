# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 14:44:17 2016

@author: Sriharsha
"""

from glob import glob
import numpy as np
import cv2
from matplotlib import pyplot as plt

def getImgMasks(img,rect):
    #img = cv2.imread(f)
    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    #rect = (50,50,450,290)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    fgdMask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    bgdMask = np.where((mask==3)|(mask==1),0,1).astype('uint8')
    #img = img*mask2[:,:,np.newaxis]
    
    return fgdMask, bgdMask
    
frames = glob('./frames/*')

framesTotal = np.size(frames)

proposals = np.load('5proposals.npy')#.round()
proposals = proposals[:,0:4,:].astype(int)

proposalsTotal = proposals.shape[0]

for t in range(1):#framesTotal):
    img = cv2.imread(frames[t])    
    
    if (t==0):
        fgdMasks = np.zeros((proposalsTotal, img.shape[0], img.shape[1], \
        framesTotal),np.uint8)
        bgdMasks = np.zeros((proposalsTotal, img.shape[0], img.shape[1], \
        framesTotal),np.uint8)
    
    for m in range(proposalsTotal):
        rect = (proposals[m,0,t], proposals[m,1,t], proposals[m,2,t]-\
        proposals[m,0,t],proposals[m,3,t]-proposals[m,1,t])
        
        fgdMasks[m,:,:,t], bgdMasks[m,:,:,t] = getImgMasks(img,rect)
        
    

    
