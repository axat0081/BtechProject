import nest_asyncio
import numpy as np
from scipy import interpolate
import asyncio
import aiohttp
import json
import math
import matplotlib.pyplot as plt
import platform

nest_asyncio.apply()
entries = 48
groundTruth = np.zeros((entries, entries, 10))
avg = 0


async def get_temperature(i: int, j: int):
    url = "https://api.weatherapi.com/v1/forecast.json?key=834f4b44da6c4bbd826101530232002&q=" + str(i) + "," + str(
        j) + "&days=10&aqi=no&alerts=no"
    print(url)
    tempList = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            data = json.loads(data.decode())
            forecast = data['forecast']['forecastday']
            for forecast_data in forecast:
                tempList.append(forecast_data['day']['avgtemp_c'])
            return tempList


async def prepare_ground_truth():
    for i in range(entries):
        for j in range(entries):
            tempList = await get_temperature(i, j)
            for z in range(10):
                groundTruth[i][j][z] = tempList[z]
            print(f'{i}, {j}, {tempList[0]}')


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.run_until_complete(prepare_ground_truth())

print('Done!!!')
for i in range(entries):
    for j in range(entries):
        for z in range(10):
            avg += groundTruth[i][j][z]

r = 12
c = 12
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
    pts2.append([pts1[i][0], pts1[i][1] + entries // 2])
    pts3.append([pts1[i][0] + entries // 2, pts1[i][1]])
    pts4.append([pts1[i][0] + entries // 2, pts1[i][1] + entries // 2])

XYTPts = []

t = 0
i = 0
while t < 10:
    XYTPts.append([pts1[i][0], pts1[i][1], t])
    XYTPts.append([pts2[i][0], pts2[i][1], t])
    XYTPts.append([pts3[i][0], pts3[i][1], t])
    XYTPts.append([pts4[i][0], pts4[i][1], t])
    i += 3
    i %= len(pts1)
    t += 1

print(XYTPts)

actualGroundTruth = np.zeros((10, entries, entries))
for z in range(10):
    for i in range(48):
        for j in range(48):
            actualGroundTruth[z][i][j] = groundTruth[i][j][z]
fourDrones = []
for i in range(0, len(XYTPts)):
    fourDrones.append(groundTruth[XYTPts[i][0]][XYTPts[i][1]][XYTPts[i][2]])
interpolateNearest = interpolate.NearestNDInterpolator(XYTPts, fourDrones)
interpolateLinear = interpolate.LinearNDInterpolator(XYTPts, fourDrones, avg / ((entries ** 2) * 10))

fourDronesNearestInterpolated = np.zeros((10, entries, entries))
fourDronesLinearInterpolated = np.zeros((10, entries, entries))

for z in range(0, 10):
    for i in range(0, 48):
        for j in range(0, 48):
            fourDronesNearestInterpolated[z][i][j] = interpolateNearest(z, i, j)
            fourDronesLinearInterpolated[z][i][j] = interpolateLinear(z, i, j)

fourDroneNearestError = 0
fourDroneLinearError = 0
for z in range(0, 10):
    for i in range(0, 48):
        for j in range(0, 48):
            fourDroneLinearError += (fourDronesLinearInterpolated[z][i][j] - actualGroundTruth[z][i][j]) * (
                    fourDronesLinearInterpolated[z][i][j] - actualGroundTruth[z][i][j])
            fourDroneNearestError += (fourDronesNearestInterpolated[z][i][j] - actualGroundTruth[z][i][j]) * (
                    fourDronesNearestInterpolated[z][i][j] - actualGroundTruth[z][i][j])

fourDroneNearestError /= (48 * 48 * 10)
fourDroneNearestError = math.sqrt(fourDroneNearestError)
fourDroneLinearError /= (48 * 48 * 10)
fourDroneLinearError = math.sqrt(fourDroneLinearError)
print(fourDroneLinearError)
print(fourDroneNearestError)

xPoints = np.linspace(0, entries - 1, num=entries)
yPoints = np.linspace(0, entries - 1, num=entries)
X, Y = np.meshgrid(xPoints, yPoints, indexing='ij')

print(f"Four drones Root mean square error Nearest Neighbour = {fourDroneNearestError}")
print(f"Four drones Root mean square error Linear Neighbour = {fourDroneLinearError}")

fig1 = plt.figure()
ax1 = plt.axes(projection='3d')
surf1At10 = ax1.plot_surface(X, Y, actualGroundTruth[5], color='blue')  # blue

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
surf2At10 = ax2.plot_surface(X, Y, fourDronesLinearInterpolated[5], color='purple')  # purple

fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
surf3At10 = ax3.plot_surface(X, Y, fourDronesNearestInterpolated[5], color='yellow')  # yellow

plt.show()
