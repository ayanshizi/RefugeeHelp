import random
import sys
import math

latitude = 35.687782
longitude = 36.786667

def generate_random_data(lat, lon, num_rows):
    for _ in xrange(num_rows):
        hex1 = '%012x' % random.randrange(16**12) # 12 char random string
        flt = float(random.randint(0,100))
        dec_lat = random.random()/10
        dec_lon = random.random()/10
        print '%s %.6f %.6f \n' % (hex1.lower(), lon+dec_lon, lat+dec_lat)

generate_random_data(latitude, longitude, 10)