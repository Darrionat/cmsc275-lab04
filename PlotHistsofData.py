# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:38:34 2023
Plotting histograms of data that you load into python
Understanding the Central Limit Theorem
@author: Kerri-Ann Norton based on code from Guttag
"""

import pylab
import random
import math


def non_empty_check(samples):
    if len(samples) == 0:
        raise ArithmeticError("Cannot operate on empty list")


def mean(samples):
    """
    Computes the mean of the given list.
    Uses the typical sum(allElements) / N formula.
    :param samples: A non-empty list of numerical values
    :return: Returns the mean of the given input
    """
    non_empty_check(samples)
    sum = 0
    for x in samples:
        sum += x
    return sum / len(samples)


def sum_squared_deviations_computational(samples):
    """
    Computes the sum of squared deviations from the mean of the given list using the computational formula.
    :param samples: A non-empty list of numerical values.
    :return: Returns the sum of squared deviations from the mean.
    """
    non_empty_check(samples)
    # The sum of all points after being squared
    sum_x_squared = 0
    # The sum of all points
    sum_x = 0
    for x in samples:
        sum_x_squared += pow(x, 2)
        sum_x += x
    # The computational formula
    return sum_x_squared - pow(sum_x, 2) / len(samples)


def variance(samples, population=True):
    """
    Computes the variance of the given list.
    :param samples: A non-empty list of numerical values.
    :param population: If True, then use the population formula for variance; otherwise, use sample formula.
    :return: Returns the variance based upon the given input.
    """
    non_empty_check(samples)
    SS = sum_squared_deviations_computational(samples)
    N = len(samples)
    # Population variance
    if population:
        return SS / N
    # Avoid size 1 samples
    if N == 1:
        raise ArithmeticError('Cannot have sample of length 1')
    return SS / (N - 1)


def std_dev(samples, population=True):
    """
    Computes the standard deviation of the given list.
    :param samples: A non-empty list of numerical values.
    :param population: If True, then use the population formula for standard deviation; otherwise, use sample formula.
    :return: Returns the standard deviation based upon the given input.
    """
    if population:
        return math.sqrt(variance(samples))
    return math.sqrt(variance(samples, False))


# Part 1: Distributions of Samples
#
# Function to load Runner data
def getBMData(filename):
    """Read the contents of the given file. Assumes the file 
    in a comma-separated format, with 6 elements in each entry:
    0. Name (string), 1. Gender (string), 2. Age (int)
    3. Division (int), 4. Country (string), 5. Overall time (float)   
    Returns: dict containing a list for each of the 6 variables."""

    data = {}
    f = open(filename)
    line = f.readline()
    data['name'], data['gender'], data['age'] = [], [], []
    data['division'], data['country'], data['time'] = [], [], []
    while line != '':
        split = line.split(',')
        data['name'].append(split[0])
        data['gender'].append(split[1])
        data['age'].append(int(split[2]))
        data['division'].append(int(split[3]))
        data['country'].append(split[4])
        data['time'].append(float(split[5][:-1]))  # remove \n
        line = f.readline()
    f.close()
    return data


def makeHist(data, bins, title, xLabel, yLabel):
    pylab.hist(data, bins)
    pylab.title(title)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    mean = sum(data) / len(data)
    std = std_dev(data)  # Use the function you created for standard deviation
    pylab.annotate('Mean = ' + str(round(mean, 2)) + \
                   '\nSD = ' + str(round(std, 2)), fontsize=20,
                   xy=(0.65, 0.75), xycoords='axes fraction')

    # RandomSample


# sample = random.sample(data, sampleSize)   Uncomment and use this


# Part 2: Distribution of Sample Means
#
def plotMeans(numDicePerTrial, numDiceThrown, numBins, legend,
              color, style):
    means = []
    numTrials = numDiceThrown // numDicePerTrial
    for i in range(numTrials):
        vals = 0
        for j in range(numDicePerTrial):
            vals += 5 * random.random()
        means.append(vals / numDicePerTrial)
    pylab.hist(means, numBins, color=color, label=legend,
               weights=pylab.array(len(means) * [1]) / len(means),
               hatch=style)
    return sum(means) / len(means), variance(means)


# pylab.figure()
"""
# Part 1
data = getBMData("bm_results2012.txt")
ages = data['age']
rand_ages = random.sample(ages, 1000)
makeHist(rand_ages, 20, "Ages of Randomly Selected Runners", "Age", "Frequency")
pylab.savefig("runnerAgeHist_1000random.pdf")
pylab.show()
"""
# Part 2
num_dice_thrown = 1
num_rolls = 1000
num_bins = 11
if num_dice_thrown == 1:
    mean, var = plotMeans(num_dice_thrown, num_rolls, num_bins, '1 die', 'w', '*')
    print('Mean', mean)
    print('stdev', math.sqrt(var))
if num_dice_thrown > 1:
    mean, var = plotMeans(num_dice_thrown, num_rolls, num_bins, str(num_dice_thrown) + ' dice', 'w', '*')
mean, var = plotMeans(50, 1000, 11, '1 die', 'w', '//')
print('Mean', mean)
print('stdev', math.sqrt(var))
print()
pylab.title('Dice Rolls')
pylab.savefig("dice_rolls.pdf")
pylab.show()
