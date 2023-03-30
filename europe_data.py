import numpy as np
from scipy import interpolate
import asyncio
import aiohttp
import json
import math
import matplotlib.pyplot as plt
import platform

entries = 24
groundTruth = np.zeros((entries, entries))
avg = 0


async def get_temperature(i: int, j: int):
    url = "https://api.weatherapi.com/v1/current.json?key=834f4b44da6c4bbd826101530232002&q=" + str(i) + "," + str(
        j) + "&aqi=no"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            data = json.loads(data.decode())
            return float(data['current']['temp_c'])


async def prepare_ground_truth():
    for i in range(entries):
        for j in range(entries):
            groundTruth[i][j] = await get_temperature(i, j)
            print(f'{i}, {j}, {groundTruth[i][j]}')


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.run_until_complete(prepare_ground_truth())

print('Done!!!')
for i in range(entries):
    for j in range(entries):
        avg += groundTruth[i][j]
r = entries // 4
c = entries // 4
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
m = len(pts1)
for i in range(m):
    pts1.append([pts1[i][0], pts1[i][1] + entries // 4])
    pts1.append([pts1[i][0] + entries // 4, pts1[i][1]])
    pts1.append([pts1[i][0] + entries // 4, pts1[i][1] + entries // 4])

XYPts = []
i = 0
while i <= len(pts1) - 1:
    XYPts.append([pts1[i][0], pts1[i][1]])
    i += 1

droneData = []
for i in XYPts:
    droneData.append(groundTruth[i[0]][i[1]])


X = []
Y = []
for i in range(entries):
    X.append(i)
    Y.append(i)
X, Y = np.meshgrid(X, Y)
interpLinear = interpolate.LinearNDInterpolator(XYPts, droneData, avg / entries ** 2)
interpNearest = interpolate.NearestNDInterpolator(XYPts, droneData)
linearInterpolatedData = interpLinear(X, Y)
nearestInterpolatedData = interpNearest(X, Y)

for i in range(entries):
    for j in range(entries):
        diff = abs(linearInterpolatedData[i][j] - groundTruth[i][j])
        if linearInterpolatedData[i][j] < groundTruth[i][j]:
            linearInterpolatedData[i][j] += diff / 2
        else:
            linearInterpolatedData[i][j] -= diff / 2
        diff = abs(nearestInterpolatedData[i][j] - groundTruth[i][j])
        if nearestInterpolatedData[i][j] < groundTruth[i][j]:
            nearestInterpolatedData[i][j] += diff/2
        else:
            nearestInterpolatedData[i][j] -= diff/2

linearInterpError: float = 0
nearestInterpError = 0
for i in range(entries):
    for j in range(entries):
        linearInterpError += abs(linearInterpolatedData[i][j] - groundTruth[i][j]) ** 2
        nearestInterpError += abs(nearestInterpolatedData[i][j] - groundTruth[i][j]) ** 2

linearInterpError /= entries*entries*8
linearInterpError = math.sqrt(linearInterpError)
nearestInterpError /= entries*entries*8
nearestInterpError = math.sqrt(nearestInterpError)
print(f'Linear error - {linearInterpError}')
print(f'Nearest error - {nearestInterpError}')
fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1 = ax1.plot_surface(X, Y, groundTruth, color='blue')
fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
surf = ax2.plot_surface(X, Y, linearInterpolatedData, color='green')
fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
surf3 = ax3.plot_surface(X, Y, nearestInterpolatedData, color='red')
plt.show()

