import csv
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator

points = set()
counter = 0
indexDict = dict()
groundTruthDict = dict()
XY = []
avg = 0
with open('nyc_data.csv', mode='r') as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        if len(lines.get('AirTemp')) == 0:
            continue
        temp = float(lines.get('AirTemp'))
        avg += temp
        lat = float(lines.get('Latitude'))
        long = float(lines.get('Longitude'))
        day = str(lines.get('Day'))
        points.add(str([lat, long]))
        if str([lat, long]) in indexDict:
            indexDict[str([lat, long])] += 1
        else:
            indexDict[str([lat, long])] = 0
        groundTruthDict[str([lat, long]) + str(indexDict[str([lat, long])])] = temp
        if indexDict[str([lat, long])] == 2947:
            XY.append(str([lat, long]))
        if len(XY) == 100:
            break
        counter += 1

avg /= counter

XY = sorted(XY)
pointIndexDict = dict()
ix = 0
jx = 0
for i in XY:
    pointIndexDict[i] = [ix, jx]
    jx += 1
    if jx == 10:
        jx = 0
        ix += 1
groundTruth = np.zeros((2948, 10, 10))
for pts in XY:
    for z in range(2948):
        i = pointIndexDict[pts][0]
        j = pointIndexDict[pts][1]
        groundTruth[z][i][j] = groundTruthDict[pts + str(z)]

r = 5
c = 5
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
    pts2.append([pts1[i][0], pts1[i][1] + 5])
    pts3.append([pts1[i][0] + 5, pts1[i][1]])
    pts4.append([pts1[i][0] + 5, pts1[i][1] + 5])

XYTPts = []

t = 0
i = 0
while t < 2948:
    XYTPts.append([pts1[i][0], pts1[i][1], t])
    XYTPts.append([pts2[i][0], pts2[i][1], t])
    XYTPts.append([pts3[i][0], pts3[i][1], t])
    XYTPts.append([pts4[i][0], pts4[i][1], t])
    i += 3
    i %= len(pts1)
    t += 1

fourDrones = []
for i in range(0, len(XYTPts)):
    fourDrones.append(groundTruth[XYTPts[i][2]][XYTPts[i][0]][XYTPts[i][1]])

interpolateNearest = NearestNDInterpolator(XYTPts, fourDrones)
interpolateLinear = LinearNDInterpolator(XYTPts, fourDrones, avg)

fourDronesNearestInterpolated = np.zeros((2948, 10, 10))
fourDronesLinearInterpolated = np.zeros((2948, 10, 10))

for z in range(0, 2948):
    # print(z)
    for i in range(0, 10):
        for j in range(0, 10):
            fourDronesNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
            fourDronesLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

fourDroneNearestError = 0
fourDroneLinearError = 0
for z in range(0, 2948):
    for i in range(0, 10):
        for j in range(0, 10):
            fourDroneLinearError += (fourDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    fourDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j])
            fourDroneNearestError += (fourDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    fourDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j])

fourDroneNearestError /= (2948 * 10 * 10)
fourDroneNearestError = math.sqrt(fourDroneNearestError)
fourDroneLinearError /= (2948 * 10 * 10)
fourDroneLinearError = math.sqrt(fourDroneLinearError)

xPoints = np.linspace(0, 9, num=10)
yPoints = np.linspace(0, 9, num=10)
X, Y = np.meshgrid(xPoints, yPoints, indexing='ij')

print(f"Four drones Root mean square error Nearest Neighbour = {fourDroneNearestError}")
print(f"Four drones Root mean square error Linear Neighbour = {fourDroneLinearError}")

fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10 = ax1.plot_surface(X, Y, groundTruth[25], color='blue')

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
surf2At10 = ax2.plot_surface(X, Y, fourDronesLinearInterpolated[25], color='purple')

fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
surf3At10 = ax3.plot_surface(X, Y, fourDronesNearestInterpolated[25], color='yellow')

plt.show()
