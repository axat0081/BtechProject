import math

import numpy as np
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt


def cal(xcord, ycord, timeInstant, height=0):
    return (math.sin(3.2 * 3.14 * 0.00005 * timeInstant) + 1) * (math.sin(2 * 0.1 * xcord)) + 30 + (
            math.sin(3.2 * 3.14 * 0.00005 * timeInstant) + 1) * (math.sin(2 * 0.1 * ycord)) + 20 - 0.00649 * height


def Simulate(height):
    fourDrones = []
    for i in range(0, len(XYTPts)):
        fourDrones.append(cal(XYTPts[i][0], XYTPts[i][1], XYTPts[i][2], height))

    interpolateNearest = NearestNDInterpolator(XYTPts, fourDrones)
    interpolateLinear = LinearNDInterpolator(XYTPts, fourDrones, 50)

    fourDronesNearestInterpolated = np.zeros((100, 50, 50))
    fourDronesLinearInterpolated = np.zeros((100, 50, 50))

    for z in range(0, 100):
        for i in range(0, 50):
            for j in range(0, 50):
                fourDronesNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
                fourDronesLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

    fourDroneNearestError = 0
    fourDroneLinearError = 0
    for z in range(0, 100):
        for i in range(0, 50):
            for j in range(0, 50):
                fourDroneLinearError += (fourDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                        fourDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j])
                fourDroneNearestError += (fourDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                        fourDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j])

    fourDroneNearestError /= (50 * 50 * 100)
    fourDroneNearestError = math.sqrt(fourDroneNearestError)
    fourDroneLinearError /= (50 * 50 * 100)
    fourDroneLinearError = math.sqrt(fourDroneLinearError)
    return [fourDroneLinearError, fourDroneNearestError]


x = []
y = []
time = []

i = 0
while i <= 49:
    x.append(i)
    y.append(i)
    i += 1

i = 0
while i <= 99:
    time.append(i)
    i += 1

groundTruth = np.zeros((100, 50, 50))
for z in range(0, 100):
    for i in range(0, 50):
        for j in range(0, 50):
            groundTruth[z][i][j] = cal(x[i], y[j], time[z])

r = 25
c = 25
r_beg = 0
r_end = r
c_beg = 0
c_end = c
pts1 = []
while r_beg < r_end and c_beg < c_end:
    for i in range(c_beg, c_end):
        pts1.append([r_beg, i])
    for i in range(r_beg + 1, r_end):
        pts1.append([i, c_end - 1])
    for i in range(c_end - 1, c_beg - 1, -1):
        if r_end - 1 - r_beg <= 0:
            break
        pts1.append([r_end - 1, i])
    for i in range(r_end - 2, r_beg, -1):
        if c_end - 1 - c_beg <= 0:
            break
        pts1.append([i, c_beg])
    r_beg += 1
    r_end -= 1
    c_beg += 1
    c_end -= 1
temp = [pts1[0]]
for i in range(1, len(pts1)):
    if temp[len(temp) - 1] == pts1[i]:
        continue
    temp.append(pts1[i])
pts1 = temp

pts2 = []
pts3 = []
pts4 = []
for i in range(0, len(pts1)):
    pts2.append([pts1[i][0], pts1[i][1] + 25])
    pts3.append([pts1[i][0] + 25, pts1[i][1]])
    pts4.append([pts1[i][0] + 25, pts1[i][1] + 25])


XYTPts = []

t = 0
i = 0
while t < 100:
    XYTPts.append([pts1[i][0], pts1[i][1], t])
    XYTPts.append([pts2[i][0], pts2[i][1], t])
    XYTPts.append([pts3[i][0], pts3[i][1], t])
    XYTPts.append([pts4[i][0], pts4[i][1], t])
    i += 3
    i %= len(pts1)
    t += 1

temp = []
linearInterpolationErrors = []
nearestInterpolationErrors = []
for i in range(10, 51):
    X, Y = Simulate(i)
    temp.append(i)
    linearInterpolationErrors.append(X)
    nearestInterpolationErrors.append(Y)
    print(f'Height - {i} , Linear Error - {X} , Nearest Neighbour - {Y}')

plt.plot(temp, linearInterpolationErrors,color='green')
plt.plot(temp, nearestInterpolationErrors, color='blue')

plt.show()
