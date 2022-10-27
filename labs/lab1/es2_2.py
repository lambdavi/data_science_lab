import json
from math import cos, acos, sin
from random import choice 

with open("citybik.json") as f:
    obj = json.load(f)

active_stations = []
available_bikes = 0
available_empty_slots = 0

def distance_coords(lat1, lng1, lat2, lng2):
    """Compute the distance among two points."""
    deg2rad = lambda x: x * 3.141592 / 180
    lat1, lng1, lat2, lng2 = map(deg2rad, [ lat1, lng1, lat2, lng2 ])
    R = 6378100 # Radius of the Earth, in meters
    return R * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lng1 - lng2))


for station in obj['network']['stations']:
    if station['extra']['status'] == 'online':
        active_stations.append(station)
    available_bikes += station['free_bikes']
    available_empty_slots += station['empty_slots']

print(len(active_stations))
print(f'Available free bikes: {available_bikes}, Available free spots: {available_empty_slots}')

distance = 9999
x0,y0 = (45.074512,7.694419)
best_station = choice(obj['network']['stations'])
for station in obj['network']['stations']:
    if station['free_bikes'] > 0:
        computed_distance = distance_coords(x0,y0, station['latitude'], station['longitude'])
        if computed_distance < distance:
            distance = computed_distance
            best_station = station

print(f'Best distance: {distance}, Station {best_station}')
