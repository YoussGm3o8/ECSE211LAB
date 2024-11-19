"""
main.py

DESCRIPTION: A robot that avoids wall and water
"""
from utils.brick import reset_brick
import time
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.ultrasonic import us_sensor
from components import colorsensor
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter

#CONSTANTS

TIMEOUT = 10

SLOW = 90
MODERATE = 180
FAST = 360

#apply median filter to sensor with a window of 10
us_sensor = Filtered_Sensor(us_sensor, Median_Filter(10))
color_sensor2 = colorsensor.Color_Sensor2(2)
#NOTE: the other sensors are called g_sensor and color_sensor (they are already initialized)



#TIMEOUT function
def wait_for(func, *args):
    if not callable(func):
        raise TypeError("func must be a function")
    ti = time.time()
    v = func(*args)
    while v is None:
        v = func(*args)
        if time.time() - ti > TIMEOUT:
            if hasattr(func, '__self__'):
                #this if for debugging purposes
                myclass = func.__self__
                raise TimeoutError(str(myclass)+" not responding...")
            raise TimeoutError("Component not responding...")
    return v

def find_cube():
    nav.turn(-MODERATE)
    time.sleep(0.2)
    nav.stop()
    current_dist = us_sensor.fetch()
    start = time.time()
    while True:
        
        if time.time() - start > 10:
            return False
        
        print(current_dist - us_sensor.fetch())
        if ((current_dist - us_sensor.fetch()) > 4 or (current_dist - us_sensor.fetch()) <= 0):
            nav.turn(SLOW)
            current_dist = us_sensor.fetch()
            time.sleep(0.1)
            nav.stop()
        else:
            while us_sensor.fetch() > 7 and us_sensor.fetch() < 25:
                nav.forward(SLOW)
                time.sleep(0.05)
                print("forward")
                print(us_sensor.fetch())
            nav.stop()
            return True

#Arm Grab Cube function

def grab_cube():
    nb_of_tries = 0
    while nb_of_tries < 2:
        find_cube()
        
        #Read Cube Color
        nav.turn(SLOW)
        time.sleep(0.4)
        nav.stop()
        nav.move_arm(-160)
        time.sleep(1)
        nav.forward(SLOW)
        time.sleep(0.7)
        nav.stop()
        
        color = None
        
        while (color == 'p' or color == None):
            color = color_sensor2.fetch()
            print(color)

        nav.stop()
        nav.forward(-SLOW)
        time.sleep(0.7)
        nav.stop()
        
        nav.move_arm(160)
        time.sleep(1)
        nav.turn(-SLOW)
        time.sleep(0.4)
        nav.stop()
        print(color)
        
        
        
        while True:
            if color == 'o' or color == 'y':
                #Grab Cube
                
                nav.move_arm(-90)
                time.sleep(2)
                #move forward here
                nav.forward(SLOW)
                time.sleep(1.8)
                nav.stop()
                
                
                nav.move_arm(-210)
                time.sleep(0.7)
                nav.move_arm(210)
                #move back here
                nav.forward(-SLOW)
                time.sleep(1.8)
                nav.stop()
                
                #time.sleep(1)
                nav.move_arm(90)
                nb_of_tries = 0
                return True
                
            else:
                #nav.turn(SLOW)
                #time.sleep(0.5)
                #nav.stop()
                #color = color_sensor2.fetch()
                if (color != 'o' or color != 'y') and nb_of_tries < 2:
                    #nav.turn(-SLOW)
                    #time.sleep(1)
                   # nav.stop()
                    nb_of_tries +=1
                else:
                    nav.turn(-MODERATE)
                    time.sleep(2)
                    nav.stop()
                    return False
    
#MAIN LOOP
# try:
#     while True:
#         speed = FAST
#         nav.forward(speed)
#         while True:
# 
#             #DISTANCE
#             dist = us_sensor.fetch()
#             print(dist)
#             if dist is None:
#                 nav.stop()
#                 dist = wait_for(us_sensor.fetch)
#                 nav.forward(speed)
# 
#             if speed != FAST:
#                 if dist >= 30:
#                     speed = FAST
#                     nav.forward(speed)
#             elif dist < 30: #speed must be FAST too
#                 speed = MODERATE
#                 nav.forward(speed)
# 
#             if dist < 15:
#                 dist = us_sensor.fetch()
#                 background_distance = 255
#                 object_distance = dist
#                 nav.stop()
#                 nav.turn(-SLOW)
#                 time.sleep(0.5)
#                 nav.stop()
#                 nav.turn(SLOW)
#                 while background_distance > (object_distance + 5):
#                     background_distance = us_sensor.fetch()
#                     #print(background_distance - object_distance)
#                 nav.turn(SLOW)
#                 time.sleep(0.2)
#                 
#                 nav.forward(-SLOW)
#                 time.sleep(0.5)
#                 
#                 while us_sensor.fetch() < 10:
#                     nav.forward(-SLOW)
#                     time.sleep(0.05)
#                     print(us_sensor.fetch())
#                 while us_sensor.fetch() > 10:
#                     nav.forward(SLOW)
#                     time.sleep(0.05)
#                     print(us_sensor.fetch())
#                 nav.stop()
#                 
#                 if grab_cube():
#                     break
#                 else:
#                     nav.turn(SLOW)
#                     time.sleep(2)
#                     nav.stop()
#                     dist = us_sensor.fetch()
                

            #COLOR
#             color = color_sensor.fetch()
#             if color is None:
#                 nav.stop()
#                 color = wait_for(color_sensor.fetch)
#                 nav.forward(speed)
# 
#             if color == 'b':
#                 nav.stop()
#                 g_sensor.reset_measure()
#                 g_sensor.wait_ready()
#                 nav.turn(SLOW)
# 
#                 while True:
#                     angle = g_sensor.fetch()
#                     if angle is None:
#                         nav.stop()
#                         angle = wait_for(g_sensor.fetch)
#                         nav.turn(SLOW)
#                     if abs(angle) > 89:
#                         nav.stop()
#                         break
# 
#         #at this point the car is near something
#         nav.stop()
#         #turn 90 degrees
#         g_sensor.reset_measure()
#         g_sensor.wait_ready()
#         nav.turn(SLOW)
#         while True:
#             dist = us_sensor.fetch()
#             if dist is None:
#                 nav.stop()
#                 dist = wait_for(us_sensor.fetch)
#                 nav.turn(SLOW)
# 
#             angle = g_sensor.fetch()
#             if angle is None:
#                 nav.stop()
#                 angle = wait_for(g_sensor.fetch)
#                 nav.turn(SLOW)
#             if abs(angle) > 89 and dist > 40:
#                 nav.stop()
#                 break

#finally:
#   reset_brick()
