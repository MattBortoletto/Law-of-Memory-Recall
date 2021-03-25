# -*- coding: utf-8 -*-
"""memory-recall.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1km5lFoKloQBR-K86knzdegC1I2ONjcTo

# Fundamental Law of Memory Recall

## Load packages
"""

import os
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib import cm
import random
import heapq
from collections import Counter
import scipy as sp
import pickle

"""## Model explanation

Item representations are chosen as random binary $\{0,1\}$ vectors where each element of the vector chosen to be 1 with small probability $f \ll 1$ independently of other elements.
Overlaps are defined as scalar products between these
representations.

The proposed recall process is based on two principles:

1. memory items are represented in the brain by overlapping random sparse neuronal ensembles in dedicated memory networks;
2. the next item to be recalled is the one with a largest overlap to the current one, excluding the item that was recalled on the previous step.

Pseudocode:
- find the second largest value in the first row of SM
- go to the row corresponding to its column index
- iterate

## Define the functions
"""

def BuildItems(L, N, f): 
    """
    L = number of items
    N = number of neurons
    f = probability of a neuron to be 1
    """
    #np.random.seed(5) # good example with seed = 5, L = 5, N = 3000, f = 0.1
    return np.random.choice([0, 1], size=(N, L), p=[1-f, f])

def SparseRandomEnsemble(L, N, f):
    items = sp.sparse.random(N, L, density=f).A
    for i in range(N):
        for j in range(L):
            if items[i,j] != 0:
                items[i,j] = 1
    return items

def SimilarityMatrix(items):
    sim = np.dot(items.T, items)
    # change the diagonal elements from 0 to 1 so that it does not interfere when we are
    # searching for the maximum element in a row
    np.fill_diagonal(sim, 0)
    return sim 

def PlotSM(sim, L):
    sns.set_context({"figure.figsize": (12, 12)})
    sns.set_style("white")
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Blues', 20)
    cmap.set_bad('w') # default value is 'k'
    ax1.imshow(sim, cmap=cmap)
    #plt.ylabel("Cluster", size = L)
    #plt.xlabel("Cluster", size = L)
    sns.despine()
    plt.colorbar(ax1.matshow(sim, cmap=cmap), shrink=.75)
    ax1.xaxis.set_label_position('bottom')
    ax1.xaxis.set_ticks_position('bottom')
    plt.xticks(range(0,L,1), size = L)
    plt.yticks(range(0,L,1), size = L)
    #plt.savefig('similarity_matrix.pdf', dpi=220, bbox_inches='tight')

def memory_recall_process(L, N, f, vb='off'):
    items = BuildItems(L, N, f)
    sim = SimilarityMatrix(items)
    if vb == 's': 
        print(sim)
    recall_list = []
    recall_list.append(0)
    recall_list.append(np.where(sim[0, ] == sim[0, ].max())[0][0])
    for i in range(1, L**2): 
        if vb == 'sr':
            print("Recall list =", recall_list)
        recall_list.append(np.where(sim[recall_list[i], ] == sim[recall_list[i], ].max())[0][0])
        if (recall_list[i+1] == recall_list[i-1]):
            sl = heapq.nlargest(2, sim[recall_list[i], ])
            if sl[0] == sl[1]:
                recall_list[i+1] = np.where(sim[recall_list[i], ] == sl[1])[0][1]
                if (recall_list[i+1] == recall_list[i-1]):
                    recall_list[i+1] = np.where(sim[recall_list[i], ] == sl[1])[0][0]
            else:
                recall_list[i+1] = np.where(sim[recall_list[i], ] == sl[1])[0][0]
        ############################################################################################
        # Stopping condition:
        # if two previously visited items are retrieved in the same order then stop.
        for j in range(len(recall_list)-1):
            for k in range(len(recall_list)-1):
                if recall_list[j:j+2] == recall_list[k+j+1:k+j+3]:
                    break
            else:
                continue
            break 
        else:
            continue
        break 
        ############################################################################################
    R = len(set(recall_list))
    return R

def TheoreticalScaling(L):
    return np.sqrt(1.5*np.pi*float(L))


"""## Do the actual computation"""

dirName = 'batch'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory", dirName, "created.")
else:    
    print("Directory", dirName, "already exists.")

os.chdir('batch')

N = 20000
f_val = [0.1, 0.05, 0.01]
L_val = [10, 20, 50, 80, 130, 280, 500]

nruns = 100

R_f01_L10 =  []
R_f01_L20 =  []
R_f01_L50 =  [] 
R_f01_L80 =  []
R_f01_L130 = []
R_f01_L280 = []
R_f01_L500 = [] 

R_f005_L10 =  []
R_f005_L20 =  []
R_f005_L50 =  []
R_f005_L80 =  []
R_f005_L130 = []
R_f005_L280 = []
R_f005_L500 = [] 

R_f001_L10 =  []
R_f001_L20 =  []
R_f001_L50 =  []
R_f001_L80 =  []
R_f001_L130 = []
R_f001_L280 = []
R_f001_L500 = []

for run in range(nruns):
    print("run ", run)
    print("f=0.1")
    R_f01_L10 .append(memory_recall_process(L_val[0], N, f_val[0]))
    R_f01_L20 .append(memory_recall_process(L_val[1], N, f_val[0]))
    R_f01_L50 .append(memory_recall_process(L_val[2], N, f_val[0]))
    R_f01_L80 .append(memory_recall_process(L_val[3], N, f_val[0]))
    R_f01_L130.append(memory_recall_process(L_val[4], N, f_val[0]))
    R_f01_L280.append(memory_recall_process(L_val[5], N, f_val[0]))
    R_f01_L500.append(memory_recall_process(L_val[6], N, f_val[0]))
    print("f=0.05")
    R_f005_L10 .append(memory_recall_process(L_val[0], N, f_val[1]))
    R_f005_L20 .append(memory_recall_process(L_val[1], N, f_val[1]))
    R_f005_L50 .append(memory_recall_process(L_val[2], N, f_val[1]))
    R_f005_L80 .append(memory_recall_process(L_val[3], N, f_val[1]))
    R_f005_L130.append(memory_recall_process(L_val[4], N, f_val[1]))
    R_f005_L280.append(memory_recall_process(L_val[5], N, f_val[1]))
    R_f005_L500.append(memory_recall_process(L_val[6], N, f_val[1])) 
    print("f=0.01")
    R_f001_L10 .append(memory_recall_process(L_val[0], N, f_val[2]))
    R_f001_L20 .append(memory_recall_process(L_val[1], N, f_val[2]))
    R_f001_L50 .append(memory_recall_process(L_val[2], N, f_val[2]))
    R_f001_L80 .append(memory_recall_process(L_val[3], N, f_val[2]))
    R_f001_L130.append(memory_recall_process(L_val[4], N, f_val[2]))
    R_f001_L280.append(memory_recall_process(L_val[5], N, f_val[2]))
    R_f001_L500.append(memory_recall_process(L_val[6], N, f_val[2]))
    if run == 2 or run == 4 or run == 25 or run == 50 or run == 75:
        Rlist = [R_f01_L10, R_f01_L20, R_f01_L50, R_f01_L80, R_f01_L130, R_f01_L280, R_f01_L500,
                 R_f005_L10, R_f005_L20, R_f005_L50, R_f005_L80, R_f005_L130, R_f005_L280, R_f005_L500,
                 R_f001_L10, R_f001_L20, R_f001_L50, R_f001_L80, R_f001_L130, R_f001_L280, R_f001_L500]
        Rlist_names = ['R_f01_L10', 'R_f01_L20', 'R_f01_L50', 'R_f01_L80', 'R_f01_L130', 'R_f01_L280', 'R_f01_L500',
                       'R_f005_L10', 'R_f005_L20', 'R_f005_L50', 'R_f005_L80', 'R_f005_L130', 'R_f005_L280', 'R_f005_L500',
                       'R_f001_L10', 'R_f001_L20', 'R_f001_L50', 'R_f001_L80', 'R_f001_L130', 'R_f001_L280', 'R_f001_L500']
        for l in range(len(Rlist)):
            if run == 2:
                with open(Rlist_names[l]+'.pkl', "wb") as f:
                    pickle.dump(Rlist[l], f)
                    f.close()
            else:
                with open(Rlist_names[l]+'.pkl', "rb") as f:
                    loaded_list = pickle.load(f)
                    f.close()
                Rlist[l] = loaded_list+Rlist[l] 
                with open(Rlist_names[l]+'.pkl', 'wb') as f:
                    pickle.dump(Rlist[l], f)
                    f.close()
        print('Saved.')
        
R_f01  = [R_f01_L10 , R_f01_L20 , R_f01_L50 , R_f01_L80 , R_f01_L130 , R_f01_L280 , R_f01_L500]
R_f005 = [R_f005_L10, R_f005_L20, R_f005_L50, R_f005_L80, R_f005_L130, R_f005_L280, R_f005_L500]
R_f001 = [R_f001_L10, R_f001_L20, R_f001_L50, R_f001_L80, R_f001_L130, R_f001_L280, R_f001_L500]

R_f01_mean  = [np.mean(R_f01_L10), 
               np.mean(R_f01_L20), 
               np.mean(R_f01_L50),
               np.mean(R_f01_L80),
               np.mean(R_f01_L130), 
               np.mean(R_f01_L280), 
               np.mean(R_f01_L500)]

R_f005_mean  = [np.mean(R_f005_L10), 
                np.mean(R_f005_L20), 
                np.mean(R_f005_L50),
                np.mean(R_f005_L80),
                np.mean(R_f005_L130), 
                np.mean(R_f005_L280), 
                np.mean(R_f005_L500)]

R_f001_mean  = [np.mean(R_f001_L10), 
                np.mean(R_f001_L20), 
                np.mean(R_f001_L50),
                np.mean(R_f001_L80),
                np.mean(R_f001_L130), 
                np.mean(R_f001_L280), 
                np.mean(R_f001_L500)]

with open('Rf_01_20000_100runs.pkl', "wb") as f:
    pickle.dump(R_f01, f)
    f.close()
with open('Rf_01_20000_100runs_mean.pkl', "wb") as f:
    pickle.dump(R_f01_mean, f)
    f.close()

with open('Rf_005_20000_100runs.pkl', "wb") as f:
    pickle.dump(R_f005, f)
    f.close()
with open('Rf_005_20000_100runs_mean.pkl', "wb") as f:
    pickle.dump(R_f005_mean, f)
    f.close()

with open('Rf_001_20000_100runs.pkl', "wb") as f:
    pickle.dump(R_f001, f)
    f.close()
with open('Rf_001_20000_100runs_mean.pkl', "wb") as f:
    pickle.dump(R_f001_mean, f)
    f.close()