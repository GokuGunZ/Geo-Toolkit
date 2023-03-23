from cmath import nan
import pandas as pd
import datetime
from shapely.geometry import Point,LineString,Polygon, MultiLineString
import matplotlib.pyplot as plt
import random

time_gap = 30 #Seconds between two gps fetches

dataset = pd.read_csv(r'G:\Il mio Drive\Computer\Università\Cambridge\Geo-Toolkit\dotti', sep=';')
data = []
device_checker = []


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
        data.append([DevNo,race_no,time,time,lat,lat_slope,lng, lng_slope, line])
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
    data.append([DevNo,race_no,time,time2,lat,lat_slope,lng, lng_slope, line])

tab2 = pd.DataFrame(data, columns=['DevNo', 'race_number', 'start_time','end_time', 'lat','lat_slope', 'lng','lng_slope','line_obj'])

#Collect paths for each device
devices = tab2['DevNo'].unique()
paths = {}  
for device in devices:
    paths[device] = tab2[tab2['DevNo']==device].copy()
    plt.plot(paths[device].lat, paths[device].lng, label=device)

plt.legend()
plt.show()

roi = []
roi.append(Polygon([Point(-5, 6), Point(3,7), Point(4, -2), Point(-4,-3)]))


intersection_data = []
for df in paths.values():
    race_no = 0
    pieces = 0
    for index,row in df.iterrows():
        DevNo = row['DevNo']
        if not row['line_obj'].within(roi) and not row['line_obj'].crosses(roi):  
            continue
        if race_no != row['race_number']:
            pieces = 0
        race_no = row['race_number']
        start_time = row['start_time']
        end_time = row['end_time']
        lat = row['lat']
        lat_slope = row['lat_slope']
        lng = row['lng']
        lng_slope = row['lng_slope']
        line = row['line_obj']
        if row['line_obj'].crosses(roi):            #Manage multiple intersection
            line = row['line_obj'].intersection(roi)
            if type(line) == MultiLineString:
                for i in range(len(line[0].geoms)):
                    lat, lng = line[0].geoms[i].coords[0]
                    start_time = start_time + datetime.timedelta(seconds=intersection_time(row, line[0].geoms[i].coords[0]))
                    end_time = start_time + datetime.timedelta(seconds=intersection_time(row, line[0].geoms[i].coords[1]))
                    intersection_data.append([DevNo,race_no,pieces,start_time,end_time,lat,lat_slope,lng, lng_slope, line])
                    lat, lng = line[0].geoms[i].coords[1]
                    intersection_data.append([DevNo,race_no,pieces,end_time,end_time,lat,nan,lng,nan, line])
                    pieces +=1
            else:
                if (lat, lng) != line[0].coords[0]:  #If it intersects and the beginning of the line changes, it modifies the segment
                    lat, lng = line[0].coords[0]
                    start_time = start_time + datetime.timedelta(seconds=intersection_time(row, line[0].coords[0]))
                    if (lat, lng) != (df['lat'][index+1],df['lng'][index+1]):  #It checks also that the segment does not goes out of the ROI
                        end_time = start_time + datetime.timedelta(seconds=intersection_time(row, line[0].coords[1]))
                        intersection_data.append([DevNo,race_no,pieces,start_time,end_time,lat,lat_slope,lng, lng_slope, line])
                        lat, lng = line[0].coords[1]
                        intersection_data.append([DevNo,race_no,pieces,end_time,end_time,lat,nan,lng,nan, line])
                        pieces +=1
                else :
                    end_time = start_time + datetime.timedelta(seconds=intersection_time(row, line[0].coords[1]))
                    intersection_data.append([DevNo,race_no,pieces,start_time,end_time,lat,lat_slope,lng, lng_slope, line])
                    lat, lng = line[0].coords[1]
                    intersection_data.append([DevNo,race_no,pieces,end_time,end_time,lat,nan,lng,nan, line])
                    pieces +=1
                    continue
        intersection_data.append([DevNo,race_no,pieces,start_time,end_time,lat,lat_slope,lng, lng_slope, line])
        
tab3 = pd.DataFrame(intersection_data, columns=['DevNo', 'race_number', 'pieces', 'start_time','end_time', 'lat','lat_slope', 'lng','lng_slope','line_obj'])

devices_intersection = tab3['DevNo'].unique()
task2a = []
paths = {}
for device in devices_intersection:
    pieces = tab3[tab3['DevNo']==device]['pieces'].unique()
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    plt.plot(*(roi[0].exterior.xy))
    for piece in pieces:
        paths[device] = tab3[tab3['DevNo']==device]
        plt.plot(paths[device][paths[device]['pieces']==piece].lat, paths[device][paths[device]['pieces']==piece].lng, label=f'{device}, piece: #{piece}', c=color)
    task2a.append([device, 0, plt.figure])
    #plt.legend()
    plt.show()
tabtask2a = pd.DataFrame(task2a, columns = ['DevNo', 'race_number', 'intersection_figure'])

#Histogram = number of eScooter inside the POI area per each hour of the day.
histogram = []
for hour in range(24):
    tot_time = 0
    if hour == 23:
        hour1 = datetime.time(hour, 0)
        for index, row in tab3.iterrows():
            if row['start_time'].time() > hour1:
                tot_time += (row['end_time']-row['start_time'])
        histogram.append(tot_time/3600)
        continue
    hour1 = datetime.time(hour, 0)
    hour2 = datetime.time(hour+1, 0)
    for index, row in tab3.iterrows():
        if (row['start_time'].time() > hour1) and (row['start_time'].time() < hour2):
            tot_time += (row['end_time']-row['start_time']).total_seconds()
    histogram.append(tot_time/3600)

plt.bar(range(24),histogram)
plt.show()