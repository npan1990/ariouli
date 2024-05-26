#!/usr/bin/env python

import time
from lsm303d import LSM303D

import math

declination = -0.00669          #define declination angle of location where measurement going to be done
pi = 3.14159265359 

lsm = LSM303D(0x1d) # Change to 0x1e if you have soldered the address jumper


maxX = 0.4065981148243359
minX = -0.23662627004529319

maxY = 0.3892765332354021
minY = -0.12688211531399193

maxZ = 0.5298078100134656
minZ = -0.03323540213000367

while True:
    xyz = lsm.magnetometer()

    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    heading = (math.atan2(y, x)*180)/pi
    if heading < 0:
        heading += 360
    # if heading>=0 and heading<=180:
    #     pass
    # else:
    #     heading = 180 + heading
    if x > maxX:
        maxX = x
    if x < minX:
        minX = x

    if y > maxY:
        maxY = y
    if y < minY:
        minY = y

    if z > maxZ:
        maxZ = z
    if z < minZ:
        minZ = z

    print(f"{minX},{maxX} {minY},{maxY}, {minZ},{maxZ}")

    avg_delta_x = (maxX - minX) / 2
    avg_delta_y = (maxY - minY) / 2
    avg_delta_z = (maxZ - minZ) / 2


    avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

    scale_x = avg_delta / avg_delta_x
    scale_y = avg_delta / avg_delta_y
    scale_z = avg_delta / avg_delta_z
    
    x = x*scale_x
    y = y*scale_y
    z = z*scale_z

    heading = (math.atan2(y, x)*180)/pi

    if heading < 0:
        heading+=360

    print(heading)

