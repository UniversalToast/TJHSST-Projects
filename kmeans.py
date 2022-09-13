# %%

import sys
import sklearn
import numpy as np
import os
from scipy import stats
# %%

from random import uniform,choice,randint
from sklearn.datasets import fetch_openml

mnist = fetch_openml('mnist_784', version=1)
mnist.keys()
data = mnist["data"]
target = mnist["target"]
data_train, data_test, target_train, target_test = data[:60000], data[60000:], target[:60000], target[60000:]
# generate 10 random centers. Centers are 784 dimensional vectors

centers = []
for x in range(10):
    temp = []
    for n in range(randint(0,55000),60000):
        if len(temp)==10:
            break
        if int(target_train[n])==x:
            temp.append(data_train[n])
    centers.append(np.array(temp).sum(axis=0)/10)
# for x in range(10):
#     # temp = []
#     # for y in range(784):
#     #     temp.append(uniform(0, 256))
#     # centers.append(np.array(temp))
#     centers.append(choice(data_train))
convthres = 1
dif = 1.1


def closestcenter(v):  # given vector v return the center it is closest to
    min = np.inf
    minidx = 0
    for idx, center in enumerate(centers):
        a = np.linalg.norm(center - v)
        if a < min:
            min = a
            minidx = idx
    return minidx
# def closestcenter(v):
#     temp = []
#     for center in centers:
#         temp.append(np.linalg.norm(center-v))
#     return temp.index(min(temp))

# while dif > convthres:
for x in range(100):
    if dif==0:
        print(x,dif)
        break
    dif = 0
    # create empty lists
    closestlists = []
    for b in range(10):
        closestlists.append([])
    # classify each training vector
    for a in data_train:
        closestlists[closestcenter(a)].append(a)
    # reclassify centers
    for n, c in enumerate(closestlists):
        closestlists[n] = np.array(c)
        if len(closestlists[n])==0:
            centers[n]=np.array([uniform(0,256) for x in range(784)])
            print("fail"+str(x))
            continue
        newc = closestlists[n].sum(axis=0) / len(closestlists[n])
        dif += np.linalg.norm(centers[n] - newc)
        centers[n] = newc
    print(dif)
# label final centers
closestlists = []
for b in range(10):
    closestlists.append([])
for n, a in enumerate(data_train):
    closestlists[closestcenter(a)].append(int(target_train[n]))
newclose = dict()  # the pointer is position in centers, data is the label
for n, a in enumerate(closestlists):
    closestlists[n] = np.array(a)
    newclose[n] = stats.mode(closestlists[n])[0]
print(newclose)
total = 0
for n,v in enumerate(data_test):
    if newclose[closestcenter(v)][0]==int(target_test[n]):
        total+=1
print(total)
print(total/10000)



