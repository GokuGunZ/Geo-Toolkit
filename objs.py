from shapely.geometry import Point,LineString
import datetime

class Segment:
    def __init__(self, DevNo, s_lat, s_lng, s_time, e_lat, e_lng, duration):
        self.DevNo = DevNo
        self.start_lat = s_lat
        self.start_lng = s_lng
        self.start_time = s_time
        self.end_lat = e_lat
        self.end_lng = e_lng
        self.end_time = s_time + datetime.timedelta(seconds=duration)
        self.lat_slope = (e_lat-s_lat)/duration
        self.lng_slope = (e_lng-s_lng/duration)
        self.line = LineString([Point(s_lat, s_lng), Point(e_lat, e_lng)])

class Race:
    def __init__(self,DevNo, race_no, segments):
        self.DevNo = DevNo
        self.race_number = race_no
        self.start_lat = segments[0].start_lat
        self.start_lng = segments[0].start_lng
        self.start_time = segments[0].start_time
        self.end_lat = segments[-1].end_lat
        self.end_lng = segments[-1].end_lng
        self.end_time = segments[-1].end_time
        self.segments = segments

class Device:
    def __init__(self,DevNo, races):
        self.DevNo = DevNo
        self.all_races = races
        self.number_of_races = len(races)
        