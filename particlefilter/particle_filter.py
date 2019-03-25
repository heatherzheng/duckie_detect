'''
suppose we know theta and d(distance)
good learning resource:
https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/12-Particle-Filters.ipynb
'''

from numpy.random import uniform
import matplotlib.pyplot as plt
import numpy as np
import random

#random generation
def init_particle(x_range,y_range,N):
    particles = np.empty((N, 2))
    particles[:, 0] = uniform(x_range[0], x_range[1], size=N)
    particles[:, 1] = uniform(y_range[0], y_range[1], size=N)
    return particles
#predict next state of particles
#assume know moving distance and angle
#add noise
def predict(particles, v, std):
    N = len(particles)
    dist = v + (randn(N) * std[1])
    particles[:, 0] += np.cos(particles[:, 2]) * dist
    particles[:, 1] += np.sin(particles[:, 2]) * dist

#update weight:
def update(particles,weights,z,R,landmarks):
    for i in particles:
        #not sure about this step
        #what should be the std???
        distance =  np.linalg.norm(particles - landmarks)
        weights = scipy.stats.norm(distance, R).pdf(z[i])

#Discard highly improbable particle and replace them with copies of the more probable particles
def resample(particles,weights):
    N  = len(particles)
    pairs = zip(weights,particles)
    sorted_pairs = sorted(pairs, key=lambda t: t[0], reverse=True)
    weights, particles = zip(*sorted_pairs)
    for i in range(3):
        #7:2:1
        particles = np.empty((N, 2))
        particles[0:int(0.7*N), 0] = uniform(0,1, size=int(N*0.7)) + particles[0][0]
        particles[0:int(0.7*N), 1] = uniform(0,1, size=int(N*0.7)) + particles[0][1]
        particles[int(0.7*N):int(0.9*N), 0] = uniform(0,1, size=int(N*0.2)) + particles[1][0]
        particles[int(0.7*N):int(0.9*N), 1] = uniform(0,1, size=int(N*0.2)) + particles[1][1]
        try:
            particles[int(0.9*N):, 0] = uniform(0,1, size=int(N*0.1)) + particles[2][0]
            particles[int(0.9*N):, 1] = uniform(0,1, size=int(N*0.1)) + particles[2][1]
        except:
            print("overflow")
    print(particles)
    #weights.fill(1.0/N)


def main():
    particles  = init_particle((0,5),(0,5),5)
    weights = [1,2,3,4,5]
    print(particles)
    resample(particles,weights)
main()
