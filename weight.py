import numpy as np

def squash(x):
    # Sigmoidal: Cannot have f(0) = 0 exactly because this means that
    # an exact match in key or bpm alone would be sufficient.
    sigmoidtight = 3.
    return np.exp(x) / (1. + np.exp(sigmoidtight - 2. * sigmoidtight * x))

def bpm_diff(firstbpm, nextbpm, slowestbpm, fastestbpm):
    # Scores compatibility of BPMs using relative difference in BPMs
    # 0 for perfect match (same BPM), 1 for worst possible match
    # TODO IF ALLOW BPM TO DROP, IT CANNOT DROP CONSECUTIVELY
    bpmrange = fastestbpm - slowestbpm
    slowpenalty = 5.
    bpmdropthreshold = 0.99
    if nextbpm >= firstbpm:
        return squash((nextbpm - firstbpm) / bpmrange)
    elif (firstbpm - nextbpm) < bpmdropthreshold:  # if reduction in BPM is small it doesn't matter
        return squash((nextbpm - firstbpm) / bpmrange)
    else:  # otherwise penalise reduction in BPM
        return squash(slowpenalty * (firstbpm - nextbpm) / bpmrange)

def key_cam_diff(firstkint, nextkint):
    # Scores compatibility of keys using heuristics based on Camelot's wheel
    # 0 for perfect match (same key), 1 for all incompatible matches
    diffkint = np.mod(nextkint - firstkint, 120)
    energypenalty = 0.025  # penalise drop in energy level associated with pitch drops
    if diffkint == 0:
        return squash(0.)
    elif (diffkint == 10 or diffkint == -110):
        return squash(0.1)
    elif (diffkint == -10 or diffkint == 110):
        return squash(0.1 + energypenalty)
    elif (diffkint == 5 or diffkint == -115) and (firstkint // 10 == nextkint // 10):
        return squash(0.2)
    elif (diffkint == -5 or diffkint == 115) and (firstkint // 10 == nextkint // 10):
        return squash(0.2 + energypenalty)
    elif (diffkint == 5 or diffkint == -115) and (firstkint // 10 != nextkint // 10):
        return squash(0.25)
    elif (diffkint == -5 or diffkint == 115) and (firstkint // 10 != nextkint // 10):
        return squash(0.25 + energypenalty)
    elif (diffkint == 15 or diffkint == -105):
        return squash(0.3)
    elif (diffkint == -15 or diffkint == 105):
        return squash(0.3 + energypenalty)
    elif (diffkint == 20 or diffkint == -100):
        return squash(0.3)
    elif (diffkint == 35 or diffkint == -85) and (firstkint % 10 == 0):
        return squash(0.4)
    elif (diffkint == -30 or diffkint == 90) and (firstkint % 10 == 0):
        return squash(0.425 + energypenalty)
    elif (diffkint == 70 or diffkint == -50):
        return squash(0.5)
    else:
        return squash(1.)

def key_diss_diff(firstfreq, nextfreq):
    # Scores compatibility of keys using Vassilakis' dissonance equation (2005)
    # 0 for perfect match (same key), 1 for all incompatible matches
    scalingfactor = 0.2
    maxfreq = max(firstfreq, nextfreq)
    minfreq = min(firstfreq, nextfreq)
    s1 = 0.0207; s2 = 18.96
    s = 0.24 / (s1 * minfreq + s2)
    b1 = 3.5; b2 = 5.75
    diss = squash((np.exp(-b1 * s * (maxfreq - minfreq)) - np.exp(-b2 * s * (maxfreq - minfreq))) / scalingfactor)
    return diss

def key_diff(firstkint, nextkint, firstfreq, nextfreq):
    # Combines compatibility of keys using Camelot's wheel and Vassilakis' equation
    # using a Cobb-Douglas form with assigned weights
    camweight = 2. / 3.  # larger weight, higher emphasis
    dissweight = 1. - camweight
    keydiff = (key_cam_diff(firstkint, nextkint) ** camweight) * (key_diss_diff(firstfreq, nextfreq) ** dissweight)
    return keydiff