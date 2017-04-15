# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 22:52:04 2016

@author: Sriharsha
"""

def objective(x):
    return entropy(np.dot(p[:,:,t],x),Pbar[:,theta])
 
def constr1(x):
    x
    
def constr2(x):
    1-np.sum(x)    

from glob import glob
from scipy.optimize import fmin_cobyla
from scipy.stats import entropy
import numpy as np

frames = glob('./frames/*')
framesTotal = np.size(frames)

proposals = np.load('./5proposals.npy')#.round()
proposals = proposals[:,0:4,:].astype(int)
proposalsTotal = proposals.shape[0]

pAll = np.load('./pFeature.npy')
qAll = np.load('./qFeature.npy')

# remove frames with nan values in p features
p = np.delete(pAll,np.unique(np.where(np.isnan(pAll))[2]),2)
q = np.delete(qAll,np.unique(np.where(np.isnan(pAll))[2]),2)

# initialize model parameters
P = 1/p.shape[2] * np.sum(p,1)
c = np.ones((p.shape[2],1))
Pbar = np.dot(P,c)/np.sum(c)
Pbar = np.append(np.zeros(Pbar.shape),Pbar,axis=1)
R = np.zeros((Pbar.shape[0],p.shape[2]))
B = np.zeros((Pbar.shape[0],q.shape[2]))

gammaInit = np.random.uniform(0,1,(1,proposalsTotal))
gammaInit = gammaInit/gammaInit.sum()
gamma=np.zeros((p.shape[2],gammaInit.shape[1]))
theta=0

#while(np.linalg.norm(Pbar[:,theta-1]-Pbar[:,theta])!=0):
theta+=1
    
for t in range(0):#p.shape[2]):
    gamma[t,:] = fmin_cobyla(objective, gammaInit.transpose(), [constr1, constr2], \
        rhoend=1e-7)
