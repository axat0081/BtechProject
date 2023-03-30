import math

import numpy as np
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt


def cal(xcord, ycord, timeInstant):
    return (math.sin(3.2 * 3.14 * 0.00005 * timeInstant) + 1) * (math.sin(2 * 0.1 * xcord)) + 30 + (
            math.sin(3.2 * 3.14 * 0.00005 * timeInstant) + 1) * (math.sin(2 * 0.1 * ycord)) + 20


x = []
y = []
time = []

i = 0
while i <= 50:
    x.append(i)
    y.append(i)
    i += 1

i = 0
while i <= 99:
    time.append(i)
    i += 1

groundTruth = np.zeros((100, 51, 51))
for z in range(0, 100):
    for i in range(0, 51):
        for j in range(0, 51):
            groundTruth[z][i][j] = cal(x[i], y[j], time[z])

r = 16
c = 16
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
pts5 = []
pts6 = []
pts7 = []
pts8 = []
pts9 = []
for i in range(0, len(pts1)):
    pts2.append([pts1[i][0], pts1[i][1] + 16])
    pts3.append([pts1[i][0], pts1[i][1] + 32])
    pts4.append([pts1[i][0] + 16, pts1[i][1]])
    pts5.append([pts1[i][0] + 16, pts1[i][1] + 16])
    pts6.append([pts1[i][0] + 16, pts1[i][1] + 32])
    pts7.append([pts1[i][0] + 32, pts1[i][1] + 32])
    pts8.append([pts1[i][0] + 32, pts1[i][1] + 16])
    pts9.append([pts1[i][0] + 32, pts1[i][1] + 32])

XYTPts = []
print(len(pts1))
print(len(pts2))
print(len(pts3))
print(len(pts4))
print(len(pts5))
print(len(pts6))
print(len(pts7))
print(len(pts8))
print(len(pts9))
t = 0
i = 0
while t < 100:
    XYTPts.append([pts1[i][0], pts1[i][1], t])
    XYTPts.append([pts2[i][0], pts2[i][1], t])
    XYTPts.append([pts3[i][0], pts3[i][1], t])
    XYTPts.append([pts4[i][0], pts4[i][1], t])
    XYTPts.append([pts5[i][0], pts5[i][1], t])
    XYTPts.append([pts6[i][0], pts6[i][1], t])
    XYTPts.append([pts7[i][0], pts7[i][1], t])
    XYTPts.append([pts8[i][0], pts8[i][1], t])
    XYTPts.append([pts9[i][0], pts9[i][1], t])
    i += 2
    i %= len(pts1)
    t += 1

print(XYTPts)

nineDrones = []
for i in range(0, len(XYTPts)):
    nineDrones.append(cal(XYTPts[i][0], XYTPts[i][1], XYTPts[i][2]))

interpolateNearest = NearestNDInterpolator(XYTPts, nineDrones)
interpolateLinear = LinearNDInterpolator(XYTPts, nineDrones, 50)

nineDronesNearestInterpolated = np.zeros((100, 51, 51))
nineDronesLinearInterpolated = np.zeros((100, 51, 51))

for z in range(0, 100):
    print(z)
    for i in range(0, 51):
        for j in range(0, 51):
            nineDronesNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
            nineDronesLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

nineDroneNearestError = 0
nineDroneLinearError = 0
for z in range(0, 100):
    for i in range(0, 51):
        for j in range(0, 51):
            nineDroneLinearError += (nineDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    nineDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j])
            nineDroneNearestError += (nineDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    nineDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j])

nineDroneNearestError /= (51 * 51 * 100)
nineDroneNearestError = math.sqrt(nineDroneNearestError)
nineDroneLinearError /= (51 * 51 * 100)
nineDroneLinearError = math.sqrt(nineDroneLinearError)

print(f"Nine drones Root mean square error Nearest Neighbour = {nineDroneNearestError}")
print(f"Nine drones Root mean square error Linear Neighbour = {nineDroneLinearError}")

xPoints = np.linspace(0, 50, num=51)
yPoints = np.linspace(0, 50, num=51)
X, Y = np.meshgrid(xPoints, yPoints, indexing='ij')

fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10 = ax1.plot_surface(X, Y, groundTruth[20], color='blue')  # purple

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
surf2At10 = ax2.plot_surface(X, Y, nineDronesLinearInterpolated[20], color='purple')  # green

fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
surf3At10 = ax3.plot_surface(X, Y, nineDronesNearestInterpolated[20], color='yellow')  # blue

plt.show()
