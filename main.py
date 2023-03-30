import math
import random

import numpy as np
from scipy.interpolate import interpn
import matplotlib.pyplot as plt


temp = np.zeros((100, 50, 50))
uniformXYInterpolated = np.zeros((100, 50, 50))
randomXYInterpolated = np.zeros((100, 50, 50))


def cal(xcord, ycord, t):
    return (math.sin(3.2 * 3.14 * 0.005 * t) + 1) * (math.sin(2 * 0.1 * xcord)) + 30 + (
            math.sin(3.2 * 3.14 * 0.005 * t) + 1) * (math.sin(2 * 0.1 * ycord)) + 20


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
for z in range(0, 100):
    for i in range(0, 50):
        for j in range(0, 50):
            temp[z][i][j] = cal(x[i], y[j], time[z])

xPoints = np.linspace(0, 49, num=50)
yPoints = np.linspace(0, 49, num=50)
X, Y = np.meshgrid(xPoints, yPoints, indexing='ij')

uniformX = []
uniformY = []
uniformX.append(0)
uniformY.append(0)
i = 1
while i <= 49:
    uniformX.append(i)
    uniformY.append(i)
    i += 2

points = (time, uniformX, uniformY)
print(points)

uniformDistTemp = np.zeros((100, len(uniformX), len(uniformY)))
for z in range(0, 100):
    for i in range(0, len(uniformX)):
        for j in range(0, len(uniformY)):
            uniformDistTemp[z][i][j] = cal(uniformX[i], uniformY[j], time[z])

for z in range(0, 100):
    print(z)
    for i in range(0, 50):
        for j in range(0, 50):
            uniformXYInterpolated[z][i][j] = interpn(points, uniformDistTemp, [z, i, j])

randomX = set()
randomY = set()
randomX.add(0)
randomY.add(0)
randomX.add(49)
randomY.add(49)
while len(randomX) < len(uniformX):
    randomX.add(random.randint(0, 49))

while len(randomY) < len(uniformY):
    randomY.add(random.randint(0, 49))

randomXList = []
randomYList = []
for x in randomX:
    randomXList.append(x)

for y in randomY:
    randomYList.append(y)

randomDistTemp = np.zeros((100, len(randomX), len(randomY)))
for z in range(0, 100):
    for i in range(0, len(randomX)):
        for j in range(0, len(randomY)):
            randomDistTemp[z][i][j] = cal(randomXList[i], randomYList[j], time[z])

for z in range(0, 100):
    print(z)
    for i in range(0, 50):
        for j in range(0, 50):
            randomXYInterpolated[z][i][j] = interpn(points, randomDistTemp, [z, i, j])

uniformXYError = 0
randomXYError = 0

for z in range(0, 100):
    for i in range(0, 50):
        for j in range(0, 50):
            uniformXYError += (uniformXYInterpolated[z][i][j]-temp[z][i][j]) * (uniformXYInterpolated[z][i][j]-temp[z][i][j])
            randomXYError += (randomXYInterpolated[z][i][j]-temp[z][i][j]) * (randomXYInterpolated[z][i][j]-temp[z][i][j])

uniformXYError /= (50 * 50 * 100)
uniformXYError = math.sqrt(uniformXYError)

randomXYError /= (50 * 50 * 100)
randomXYError = math.sqrt(randomXYError)

print(f"UniformXY Root mean square error = {uniformXYError}")
print(f"UniformXY Root mean square error = {randomXYError}")

fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10 = ax1.plot_surface(X, Y, temp[10], cmap='summer')  # purple
surf2At10 = ax1.plot_surface(X, Y, uniformXYInterpolated[10], cmap='autumn')  # green
surf3At10 = ax1.plot_surface(X, Y, randomXYInterpolated[10], cmap='cool')  # blue

# fig2 = plt.figure()
# ax2 = plt.axes(projection='3d')
# surf1At50 = ax2.plot_surface(X, Y, temp[50], cmap='copper')  # brown
# surf2At50 = ax2.plot_surface(X, Y, uniformXYInterpolated[50], cmap='pink')  # light yellow
# surf3At50 = ax2.plot_surface(X, Y, randomXYInterpolated[50], cmap='hot')  # bright orange
#
# fig3 = plt.figure()
# ax3 = plt.axes(projection='3d')
# surf1At90 = ax3.plot_surface(X, Y, temp[90], cmap='spring')  # bright pink
# surf2At90 = ax3.plot_surface(X, Y, uniformXYInterpolated[90], cmap='summer')  # purple
# surf3At90 = ax3.plot_surface(X, Y, randomXYInterpolated[90], cmap='cool')  # blue
plt.show()


