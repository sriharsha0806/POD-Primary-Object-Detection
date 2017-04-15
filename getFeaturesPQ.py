# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 15:07:09 2016

@author: Sriharsha
"""

from glob import glob
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io, color
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

frames = glob('./frames/*')
framesTotal = np.size(frames)

proposals = np.load('./5proposals.npy')#.round()
proposals = proposals[:,0:4,:].astype(int)
proposalsTotal = proposals.shape[0]


bgdMasks = np.load('./bgdMasks.npy')
fgdMasks = np.load('./fgdMasks.npy')

for t in range(framesTotal):
    frame = img_as_float(io.imread(frames[t]))
    frameLAB = color.rgb2lab(frame)
    segments = slic(frame, n_segments = 1000, sigma = 8.89, \
    convert2lab = "True")+1
    labAvg = np.zeros((segments.max(),3))
    for n in range(segments.max()):
        maskLAB=segments.copy()
        maskLAB[maskLAB!=n+1]=0
        labValTemp=frameLAB*maskLAB[:,:,np.newaxis]
        labAvg[n]=[labValTemp[:,:,0].sum(),labValTemp[:,:,1].sum(),\
        labValTemp[:,:,2].sum()]
        labAvg[n]/=np.count_nonzero(maskLAB)
        
    kMeans=KMeans(n_clusters=100).fit(labAvg)
    codeWords=kMeans.labels_+1
    maskCW=segments.copy()        
        
    for r in range(np.size(codeWords)):
        maskCW=np.where(maskCW==r+1,-codeWords[r],maskCW)
        
    maskCW=-maskCW
    numLabels=np.size(np.unique(codeWords))
    
    if (t == 0):
        p = np.zeros((numLabels,proposalsTotal,framesTotal))        
        q = np.zeros((numLabels,proposalsTotal,framesTotal))
        
    for m in range(proposalsTotal):
        tempFgdCW = maskCW*fgdMasks[m,:,:,t]
        tempBgdCW = maskCW*bgdMasks[m,:,:,t]
        
        tempFgdPropCW = np.array(tempFgdCW[proposals[m,1,t]:proposals[m,3,t],\
        proposals[m,0,t]:proposals[m,2,t]])        
        tempBgdPropCW = np.array(tempBgdCW[proposals[m,1,t]:proposals[m,3,t],\
        proposals[m,0,t]:proposals[m,2,t]])
        
        tempFgdPropCWnoZs = np.delete(tempFgdPropCW.flatten(), \
        np.where(tempFgdPropCW.flatten()==0))
        tempBgdPropCWnoZs = np.delete(tempBgdPropCW.flatten(), \
        np.where(tempBgdPropCW.flatten()==0))
        
        tempFgdHist, tempFgdBins = np.histogram(tempFgdPropCWnoZs, numLabels, \
        density="True")
        p[:,m,t] = tempFgdHist*np.diff(tempFgdBins)
        
        tempBgdHist, tempBgdBins = np.histogram(tempBgdPropCWnoZs, numLabels, \
        density="True")
        q[:,m,t] = tempBgdHist*np.diff(tempBgdBins)
        
        
    
