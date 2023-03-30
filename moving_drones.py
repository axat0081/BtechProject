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

r = 50
c = 50
r_beg = 0
r_end = r
c_beg = 0
c_end = c
pts0 = []
while r_beg < r_end and c_beg < c_end:
    for i in range(c_beg, c_end):
        pts0.append([r_beg, i])
    for i in range(r_beg + 1, r_end):
        pts0.append([i, c_end - 1])
    for i in range(c_end - 1, c_beg - 1, -1):
        if r_end - 1 - r_beg <= 0:
            break
        pts0.append([r_end - 1, i])
    for i in range(r_end - 2, r_beg, -1):
        if c_end - 1 - c_beg <= 0:
            break
        pts0.append([i, c_beg])
    r_beg += 1
    r_end -= 1
    c_beg += 1
    c_end -= 1

temp = [pts0[0]]
for i in range(1, len(pts0)):
    if temp[len(temp) - 1] == pts0[i]:
        continue
    temp.append(pts0[i])
pts0 = temp

t = 0
i = 0
XYT1Drone = []
while t < 100:
    XYT1Drone.append([pts0[i][0], pts0[i][1], t])
    i += 2
    i %= len(pts0)
    t += 1

oneDrone = []
for i in range(0, len(XYT1Drone)):
    oneDrone.append(cal(XYT1Drone[i][0], XYT1Drone[i][1], XYT1Drone[i][2]))

interpolateNearest = NearestNDInterpolator(XYT1Drone, oneDrone)
interpolateLinear = LinearNDInterpolator(XYT1Drone, oneDrone, 50)
oneDroneNearestInterpolated = np.zeros((100, 50, 50))
oneDroneLinearInterpolated = np.zeros((100, 50, 50))
for z in range(0, 100):
    print(z)
    for i in range(0, 50):
        for j in range(0, 50):
            oneDroneNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
            oneDroneLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

r = 25
c = 50
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
print(pts1)

pts2 = []
for i in range(0, len(pts1)):
    pts2.append([pts1[i][0] + 25, pts1[i][1]])

XYT2Drones = []

t = 0
i = 0
while t < 100:
    XYT2Drones.append([pts1[i][0], pts1[i][1], t])
    XYT2Drones.append([pts2[i][0], pts2[i][1], t])
    i += 2
    i %= len(pts1)
    t += 1

twoDrones = []
for i in range(0, len(XYT2Drones)):
    twoDrones.append(cal(XYT2Drones[i][0], XYT2Drones[i][1], XYT2Drones[i][2]))

print(XYT1Drone)
print(XYT2Drones)

interpolateNearest = NearestNDInterpolator(XYT2Drones, twoDrones)
interpolateLinear = LinearNDInterpolator(XYT2Drones, twoDrones, 50)
print(XYT2Drones)
twoDronesNearestInterpolated = np.zeros((100, 50, 50))
twoDronesLinearInterpolated = np.zeros((100, 50, 50))
for z in range(0, 100):
    print(z)
    for i in range(0, 50):
        for j in range(0, 50):
            twoDronesNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
            twoDronesLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

oneDroneErrorNearest = 0
twoDronesErrorNearest = 0
oneDroneErrorLinear = 0
twoDronesErrorLinear = 0
for z in range(0, 100):
    for i in range(0, 50):
        for j in range(0, 50):
            oneDroneErrorNearest += (oneDroneNearestInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    oneDroneNearestInterpolated[z][i][j] - groundTruth[z][i][j])
            twoDronesErrorNearest += (twoDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    twoDronesNearestInterpolated[z][i][j] - groundTruth[z][i][j])
            oneDroneErrorLinear += (oneDroneLinearInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    oneDroneLinearInterpolated[z][i][j] - groundTruth[z][i][j])
            twoDronesErrorLinear += (twoDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j]) * (
                    twoDronesLinearInterpolated[z][i][j] - groundTruth[z][i][j])


oneDroneErrorNearest /= (50 * 50 * 100)
oneDroneErrorNearest = math.sqrt(oneDroneErrorNearest)
twoDronesErrorNearest /= (50 * 50 * 100)
twoDronesErrorNearest = math.sqrt(twoDronesErrorNearest)
oneDroneErrorLinear /= (50 * 50 * 100)
oneDroneErrorLinear = math.sqrt(oneDroneErrorLinear)
twoDronesErrorLinear /= (50 * 50 * 100)
twoDronesErrorLinear = math.sqrt(twoDronesErrorLinear)

print(f"One drones Root mean square error Nearest Neighbour = {oneDroneErrorNearest}")
print(f"Two drones Root mean square error Nearest Neighbour = {twoDronesErrorNearest}")
print(f"One drones Root mean square error Linear = {oneDroneErrorLinear}")
print(f"Two drones Root mean square error Linear = {twoDronesErrorLinear}")

xPoints = np.linspace(0, 49, num=50)
yPoints = np.linspace(0, 49, num=50)
X, Y = np.meshgrid(xPoints, yPoints, indexing='ij')

fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10 = ax1.plot_surface(X, Y, groundTruth[20], color='blue')  # purple
surf2At10 = ax1.plot_surface(X, Y, oneDroneNearestInterpolated[20], color='purple')  # green
surf3At10 = ax1.plot_surface(X, Y, oneDroneNearestInterpolated[40], color='red')  # blue

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
surf1At50 = ax2.plot_surface(X, Y, groundTruth[40], cmap='copper')  # brown
surf2At50 = ax2.plot_surface(X, Y, oneDroneNearestInterpolated[40], cmap='pink')  # light yellow
surf3At50 = ax2.plot_surface(X, Y, twoDronesNearestInterpolated[40], cmap='hot')  # bright orange

# fig3 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10_2 = ax1.plot_surface(X, Y, groundTruth[10], cmap='summer')  # purple
surf2At10_2 = ax1.plot_surface(X, Y, oneDroneLinearInterpolated[10], cmap='winter')  # green
surf3At10_2 = ax1.plot_surface(X, Y, twoDronesLinearInterpolated[10], cmap='cool')  # blue

fig4 = plt.figure()
ax2 = plt.axes(projection='3d')
surf1At50_2 = ax2.plot_surface(X, Y, groundTruth[40], cmap='copper')  # brown
surf2At50_2 = ax2.plot_surface(X, Y, oneDroneLinearInterpolated[40], cmap='pink')  # light yellow
surf3At50_2 = ax2.plot_surface(X, Y, twoDronesLinearInterpolated[40], cmap='hot')  # bright orange

plt.show()
