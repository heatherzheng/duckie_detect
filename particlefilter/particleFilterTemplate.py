#!/usr/bin/env python

import numpy as np
from scipy.stats import multivariate_normal as mvn
import scipy.stats
import matplotlib.pyplot as plt
import math
import random

#########################################################
# This file is a template for a simple particle filter.
# Fill in the necessary blocks of code where indicated.
# Note - this file only localizes one landmark (landmark 0)
#########################################################
# Open the data file, parse data, store
data = open('sensorData.txt', 'r')
lines = data.readlines()

dataSet = []  # Total list of all x/y readings
# Evaluate data
for line in lines:
    landmarkNo, location = line.split(':')
    if landmarkNo == '0':
        xVal, yVal = location.split(',')
        xVal = float(xVal.split('[')[1])
        yVal = float(yVal.split(']')[0])
        dataSet.append([xVal, yVal])

# Initialize particles
numParticles = 10
particleSet = np.zeros([numParticles, 2])  # empty array of particles
#   Sample uniformly over +/- span in x/y
spanB = -2
spanE = 2
xSamples = np.random.uniform(spanB, spanE, numParticles)
ySamples = np.random.uniform(spanB, spanE, numParticles)
for i in range(0, numParticles):
    particleSet[i, :] = [xSamples[i], ySamples[i]]
initialSet = particleSet  # Save initial set for plotting later
####################################################################################################
# *** Your code here -> define an array (np.array) of covariance values. This reflects the sensor properties.
sigma = np.array([0.2])
####################################################################################################
# Implement particle filter
for i in range(0, len(dataSet)):
    xSensor = dataSet[i][0]
    ySensor = dataSet[i][1]
    # Generate particle weights
    particleWeights = np.zeros(numParticles)
    #   For each data point, determine a weight
    for j in range(0, len(particleSet)):
        ####################################################################################################
        # *** Your code here -> p(z|x)
        particleWeights[j] = math.sqrt((particleSet[j][0]-xSensor)**2 + (particleSet[j][1]-ySensor)**2)
        particleWeights[j] = scipy.stats.norm(0,sigma).pdf(particleWeights[j])
        ####################################################################################################
    ####################################################################################################
    # *** Your code here -> re-scale the particle weights so that the sum of weights = 1
    particleWeights = particleWeights / sum(particleWeights)

    ####################################################################################################
    # Weighted Sampling
    newParticles = np.zeros([numParticles, 2])
    particleIndices = range(0, numParticles)  # np.random.choice only selects from 1D arrays - select by index
    selectedIndices = np.random.choice(particleIndices, numParticles, p=particleWeights)
    print(particleSet)

    for j in range(0, len(selectedIndices)):
        ####################################################################################################
        # *** Your code here -> add to 'newParticles'
        # NB: Add a small (SMALL!) amount of noise here to allow the particle set to converge to the solution
        # Add the particle associated with each index in 'selectedIndices" to the new particle set
        newParticles[j] = particleSet[selectedIndices[j]] + [random.uniform(-0.02, 0.02),random.uniform(-0.02, 0.02)]
        ####################################################################################################
    particleSet = newParticles

plotData = True
if plotData:
    plt.figure(1)
    plt.plot(0.8, 0.87, 's', color='r',markersize=10)
    for i in range(0, len(particleSet)):
        mSize = 3
        plt.plot(particleSet[i, 0], particleSet[i, 1], 'o', color='b', markersize=3)
    for i in range(0, len(initialSet)):
        mSize = 3
        plt.plot(initialSet[i, 0], initialSet[i, 1], 'o',color='g',markersize=3)
    plt.axis([-2, 8, -2, 8])
    plt.show()
