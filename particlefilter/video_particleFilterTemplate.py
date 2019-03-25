#!/usr/bin/env python

import numpy as np
from scipy.stats import multivariate_normal as mvn
import scipy.stats
import matplotlib.pyplot as plt
import math
import random
from matplotlib import animation

#########################################################
# This file is a template for a simple particle filter.
# Fill in the necessary blocks of code where indicated.
# Note - this file only localizes one landmark (landmark 0)
#########################################################
# Open the data file, parse data, store
data = open('sensorData.txt', 'r')
lines = data.readlines()
imagelist = []
dataSet = []  # Total list of all x/y readings
dataSet1 = []
dataSet2 = []
dataSet3 = []
# Evaluate data
imagenum = 0
for line in lines:
    landmarkNo, location = line.split(':')
    if landmarkNo == '0':
        xVal, yVal = location.split(',')
        xVal = float(xVal.split('[')[1])
        yVal = float(yVal.split(']')[0])
        dataSet.append([xVal, yVal])
    elif landmarkNo == '1':
        xVal, yVal = location.split(',')
        xVal = float(xVal.split('[')[1])
        yVal = float(yVal.split(']')[0])
        dataSet1.append([xVal, yVal])
    elif landmarkNo == '2':
        xVal, yVal = location.split(',')
        xVal = float(xVal.split('[')[1])
        yVal = float(yVal.split(']')[0])
        dataSet2.append([xVal, yVal])
    elif landmarkNo == '3':
        xVal, yVal = location.split(',')
        xVal = float(xVal.split('[')[1])
        yVal = float(yVal.split(']')[0])
        dataSet3.append([xVal, yVal])

# Initialize particles
numParticles = 100
particleSet = np.zeros([numParticles, 2])  # empty array of particles
#   Sample uniformly over +/- span in x/y
#spanB = -2
#spanE = 2
spanB = -6
spanE = 6
xSamples = np.random.uniform(spanB, spanE, numParticles)
ySamples = np.random.uniform(spanB, spanE, numParticles)
for i in range(0, numParticles):
    particleSet[i, :] = [xSamples[i], ySamples[i]]
initialSet = particleSet  # Save initial set for plotting later
particleSet1 = particleSet
particleSet2 = particleSet
particleSet3 = particleSet
####################################################################################################
# *** Your code here -> define an array (np.array) of covariance values. This reflects the sensor properties.
sigma = np.array([0.2])
####################################################################################################
# Implement particle filter
for i in range(0, len(dataSet)):
    xSensor = dataSet[i][0]
    ySensor = dataSet[i][1]
    xSensor1 = dataSet1[i][0]
    ySensor1 = dataSet1[i][1]
    xSensor2 = dataSet2[i][0]
    ySensor2 = dataSet2[i][1]
    xSensor3 = dataSet3[i][0]
    ySensor3 = dataSet3[i][1]
    # Generate particle weights
    particleWeights = np.zeros(numParticles)
    particleWeights1 = np.zeros(numParticles)
    particleWeights2 = np.zeros(numParticles)
    particleWeights3 = np.zeros(numParticles)
    #   For each data point, determine a weight
    for j in range(0, len(particleSet)):
        ####################################################################################################
        # *** Your code here -> p(z|x)
        particleWeights[j] = math.sqrt((particleSet[j][0]-xSensor)**2 + (particleSet[j][1]-ySensor)**2)
        particleWeights[j] = scipy.stats.norm(0,sigma).pdf(particleWeights[j])
        particleWeights1[j] = math.sqrt((particleSet1[j][0]-xSensor1)**2 + (particleSet1[j][1]-ySensor1)**2)
        particleWeights1[j] = scipy.stats.norm(0,sigma).pdf(particleWeights1[j])
        particleWeights2[j] = math.sqrt((particleSet2[j][0]-xSensor2)**2 + (particleSet2[j][1]-ySensor2)**2)
        particleWeights2[j] = scipy.stats.norm(0,sigma).pdf(particleWeights2[j])
        particleWeights3[j] = math.sqrt((particleSet3[j][0]-xSensor3)**2 + (particleSet3[j][1]-ySensor3)**2)
        particleWeights3[j] = scipy.stats.norm(0,sigma).pdf(particleWeights3[j])
        ####################################################################################################
    ####################################################################################################
    # *** Your code here -> re-scale the particle weights so that the sum of weights = 1
    particleWeights = particleWeights / sum(particleWeights)
    particleWeights1 = particleWeights1 / sum(particleWeights1)
    particleWeights2 = particleWeights2 / sum(particleWeights2)
    particleWeights3 = particleWeights3 / sum(particleWeights3)

    ####################################################################################################
    # Weighted Sampling
    newParticles = np.zeros([numParticles, 2])
    newParticles1 = np.zeros([numParticles, 2])
    newParticles2 = np.zeros([numParticles, 2])
    newParticles3 = np.zeros([numParticles, 2])

    particleIndices = range(0, numParticles)  # np.random.choice only selects from 1D arrays - select by index
    selectedIndices = np.random.choice(particleIndices, numParticles, p=particleWeights)
    selectedIndices1 = np.random.choice(particleIndices, numParticles, p=particleWeights1)
    selectedIndices2 = np.random.choice(particleIndices, numParticles, p=particleWeights2)
    selectedIndices3 = np.random.choice(particleIndices, numParticles, p=particleWeights3)

    for j in range(0, len(selectedIndices)):
        ####################################################################################################
        # *** Your code here -> add to 'newParticles'
        # NB: Add a small (SMALL!) amount of noise here to allow the particle set to converge to the solution
        # Add the particle associated with each index in 'selectedIndices" to the new particle set
        newParticles[j] = particleSet[selectedIndices[j]] + [random.uniform(-0.2, 0.2),random.uniform(-0.2, 0.2)]
        newParticles1[j] = particleSet1[selectedIndices1[j]] + [random.uniform(-0.2, 0.2),random.uniform(-0.2, 0.2)]
        newParticles2[j] = particleSet2[selectedIndices2[j]] + [random.uniform(-0.2, 0.2),random.uniform(-0.2, 0.2)]
        newParticles3[j] = particleSet3[selectedIndices3[j]] + [random.uniform(-0.2, 0.2),random.uniform(-0.2, 0.2)]
        ####################################################################################################
    particleSet = newParticles
    particleSet1 = newParticles1
    particleSet2 = newParticles2
    particleSet3 = newParticles3

    plotData = True
    if plotData:
        plt.figure(1)
        plt.plot(0.8, 0.87, 's', color='r',markersize=10)
        #plt.plot(1.8, 5.2, 's', color='r',markersize=10)
        for i in range(0, len(particleSet)):
            mSize = 3
            plt.plot(particleSet[i, 0], particleSet[i, 1], 'o', color='b', markersize=3)
            plt.plot(particleSet1[i, 0], particleSet1[i, 1], 'o', color='y', markersize=3)
            plt.plot(particleSet2[i, 0], particleSet2[i, 1], 'o', color='orange', markersize=3)
            plt.plot(particleSet3[i, 0], particleSet3[i, 1], 'o', color='pink', markersize=3)
        for i in range(0, len(initialSet)):
            mSize = 3
            plt.plot(initialSet[i, 0], initialSet[i, 1], 'o',color='g',markersize=3)
        plt.axis([-6, 6, -6, 6])
        plt.savefig(str(imagenum)+'.png')
        imagenum = imagenum + 1
        plt.clf()

def redraw_fn(f, axes):
    img = imagelist[f]
    if not redraw_fn.initialized:
        redraw_fn.im = axes.imshow(img, animated=True)
        redraw_fn.initialized = True
    else:
        redraw_fn.im.set_array(img)
redraw_fn.initialized = False

videofig(len(imagelist), redraw_fn, play_fps=30)
