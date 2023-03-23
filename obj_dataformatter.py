import pandas as pd
import datetime
from shapely.geometry import Point,LineString,Polygon
import matplotlib.pyplot as plt
import random
from objs import *

time_gap = 30 #Seconds between two gps fetches

dataset = pd.read_csv('Dotti.csv', sep=';')
data = []
device_checker = []
segments = []


def intersection_time(row,point):
    return (point[0]-row['lat'])/row['lat_slope']

for i in range(len(dataset)-1):
    DevNo = dataset['DevNo'][i]
    time = datetime.datetime.strptime(dataset['time'][i], '%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(dataset['time'][i+1], '%Y-%m-%d %H:%M:%S') 
    if DevNo != dataset['DevNo'][i+1] or time != time2- datetime.timedelta(seconds=time_gap):
        lat = dataset['lat'][i]
        lng = dataset['lng'][i]
        lat_slope = 0
        lng_slope = 0
        A = Point(lat,lng)
        line = LineString([A,A])
        device_checker.append(DevNo)
        segment=Segment(DevNo, lat, lng, time, lat2, lng2, time_gap)
        segments.append(segment)
        data.append([DevNo,race_no,time,time,lat,lat_slope,lng, lng_slope, line,segment])
        continue
    race_no = device_checker.count(DevNo)
    lat = dataset['lat'][i]
    lat2 = dataset['lat'][i+1]
    lng = dataset['lng'][i]
    lng2 = dataset['lng'][i+1]
    A = Point(lat,lng)
    B = Point(lat2,lng2)
    line = LineString([A,B])
    lat_slope = (lat2 - lat)/time_gap
    lng_slope = (lng2 - lng)/time_gap
    segment=Segment(DevNo, lat, lng, time, lat2, lng2, time_gap)
    segments.append(segment)
    data.append([DevNo,race_no,time,time2,lat,lat_slope,lng, lng_slope, line, segment])

tab2 = pd.DataFrame(data, columns=['DevNo', 'race_number', 'start_time','end_time', 'lat','lat_slope', 'lng','lng_slope','line_obj'])

devices = tab2['DevNo'].unique()
paths = {}  
for device in devices:
    paths[device] = tab2[tab2['DevNo']==device].copy()

devices_obj = []
for df in paths.values():
    races = df['race_number'].unique()
    race_objs = []
    race_segments = []
    for race in races:
        for i, row in df[df['race_number']==race]:
            race_segments.append(row['segment'])
        race_objs.append(Race(df['DevNo'], race, race_segments))
    devices_obj.append(Device(df['DevNo'], race_objs))