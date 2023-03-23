import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

number_of_escooter = 10
max_length = 10
path_length = 0
time_gap = 30 #Seconds between two gps fetches
max_displacement = 5

dataset = pd.DataFrame()
data = []

for i in range(number_of_escooter):
    DevNo = random.randint(100,200)
    time = datetime.datetime(2022, 8, 22, random.randint(0,23), random.randint(0,59))
    path_length = random.randint(1,max_length)
    lat = random.randint(-10,10)
    lng = random.randint(-10,10)
    data.append([DevNo,time,lat,lng])
    for j in range(path_length):
        time = time + datetime.timedelta(seconds=time_gap)
        dist= random.uniform(-max_displacement, max_displacement)
        x_direction = random.random()
        y_direction = 1 - x_direction
        lat = round(lat + x_direction*dist,3)
        lng = round(lng + y_direction*dist,3)
        data.append([DevNo,time,lat,lng])

dataset = pd.DataFrame(data, columns=['DevNo', 'time', 'lat', 'lng'])
print(dataset)
dataset.to_csv('dotti.csv', sep=';', index=False)

#with random generated dataset we could have devices teleporting from a race to another, this evidently can't happen with real data
devices = dataset['DevNo'].unique()
paths = {}
for device in devices:
    paths[device] = dataset[dataset['DevNo']==device]
    plt.plot(paths[device].lat, paths[device].lng)
#plt.show()