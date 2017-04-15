# POD--Primary-Object-Detection

The project is based on the following paper [link](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Koh_POD_Discovering_Primary_CVPR_2016_paper.pdf)

## Objective of "POD: Discovering Primary Objects..." Paper
The POD algorithm attempts to identify the "primary object" in a set of video frames. 
It breaks up each frame into multiple object proposals from which foreground and
background features are derived and  stochastically analyzed into multiple object
proposals from which foreground and background features are dervied and stochastically
analyzed to generate for each frame an object recurrence, background and primary object models. 
The models developed lead to discovering the bounding boxes of the primary object in each frame.

# Paper Summary
  . Object Proposal Generation  
    To generate proposals per frame the Alexe et al.'s "Objectness" algorithm is employed. 
    the bounding boxes per the number of the objects requested from the Alexe's et.al.'s algorithm 
    are the proposals used to generate foreground and background features per prospal per frame. The 
    foreground and background features per proposal with GrabCuts, each foreground and background masks
    are then used to obtained with probability distribution of the LAB codewords in each frame per proposal
    The LAB colors are encoded into 100 codewords which are derived from 1000 superpixels that are outpus of the SLIC algorithm.

  . Object Recurrence Model
    The object recurrence model is obtained by processsing all the foreground features per frame. 
    Recurrence weights are obtained via evaluation of the Kullback-Leibler divergence relative to entropy
    between the recurrence model at particular weights against the global primary object via convex optimization.
    The optimal weights are used to update the recurrence models for each frame.
    
  . Background Model
    The background model is obtained by finding the weights of each background feature with repect to the chi-square distance 
    to the object recurrence model, per frame
  
  . Primary Object Model
    The primary object model is obtained by finding the weigths for each foreground feature in the frame
    by a ratio of the chi-square distance between the foreground features and the background model over the 
    foreground features and the object recurrence model. The primary Objective model weigths are used to update 
    the primary object model.
    
 All the models are update iteratively until the Euclidean distance between the primary model from current iteration 
 to the prior converges to zero. Once the convergence is acheived, discovering the primary object in each frame can be achieved.
 
 # Implementation Results
 
 . Object Proposal Generation
  1. I obtained proposals with the Alexe et al.'s code provided here: [link](http://groups.inf.ed.ac.uk/calvin/objectness/)
     I created the getProposals.m file file for getting the proposals. I generated one set of 20 proposals in 
     over 100 frame. But due to lack sufficient computational power I generated a sceond set of 5 proposals from 25 frames.
     
  2. getFgdBgdMasks.py script is based on the following: [link](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_grabcut/py_grabcut.html) 
  
     to produce foreground and background masks for each proposal in each frame. Apparently I did this 
     incorrectly since I used the entire frame as instead of the cropped frame per proposal.
     
  3. In getFeatures.py script, I employed SLIC to obtain superpixels for each frame. The superpixels are mapped
     into 100 codeword based on the LAB features of the superpixels which are used in K-Means to obtain the 100
     codewords. I use the foreground an superpixel which are used in K-Means to obtain the 100 codewords. 
     I use the foreground and background masks from step 3 to obtain probability distributions, P and Q respectively, 
     by multiplying each proposals mask to the frame and obtaining the normalized histograms.
   
# Object Recurrence, Background, and Primary Object Models
    getModelsRBP.py script is used to implement the model generation and iterations but I failed to obtain 
    any optimized recurrence weights.
    
NOTE: I have not included the Proposals.npy; as the file is more than 100 MB.


    
     

    
