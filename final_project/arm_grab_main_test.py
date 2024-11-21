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
color_sensor_left = colorsensor.Color_Sensor2(2)
color_sensor_right = colorsensor.Color_Sensor(3)
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


def align(angle):
    print("angle: ", angle)
    if g_sensor.fetch() < angle:
        nav.turn(MODERATE)
        time.sleep(0.01)
        print(g_sensor.fetch())
        #nav.stop()
    elif g_sensor.fetch() > angle:
        nav.turn(-MODERATE)
        time.sleep(0.01)
        print(g_sensor.fetch())
        #nav.stop()
    
def test_us():
    while True:
        print(us_sensor.fetch())
        time.sleep(0.01)

def test_cs():
    while True:
        print(color_sensor_left.fetch())
        time.sleep(0.05)
        
def check_wall():
    nav.stop()
    nav.move_arm(-240)
    time.sleep(1)
    nav.forward(SLOW)
    time.sleep(1)
    nav.stop()
    color = color_sensor_left.fetch()
    
    while (color == None):
        color = color_sensor_left.fetch()
        print(color)
        time.sleep(0.05)
    
    if color == 'p':
        nav.forward(-SLOW)
        time.sleep(1)
        nav.stop()
        nav.move_arm(240)
        time.sleep(1)
        return True
    nav.forward(-SLOW)
    time.sleep(1)
    nav.stop()
    nav.move_arm(240)
    time.sleep(1)
    return False
        
def find_cube():
    current_dist = us_sensor.fetch()
    nav.stop()
    
    print("current dist: ", current_dist)
    nav.turn(MODERATE)
    time.sleep(0.5)
    nav.stop()
    while current_dist == us_sensor.fetch() :
        time.sleep(0.05)
    
    after_dist = us_sensor.fetch()
    print("after turning: " , after_dist)
    start = time.time()
    direction_angle = g_sensor.fetch() + 20
    while True:
        if abs(after_dist - current_dist) < 10: #wall
            return False
            
        while (abs(after_dist - current_dist ) > 4):
            #time.sleep(0.1)
            nav.turn(-SLOW/2)
            print(current_dist - us_sensor.fetch())
            after_dist = us_sensor.fetch()
            time.sleep(0.1)
            if time.time() - start > 2: # wall or hallucination
                while True:
                    align(direction_angle)
                    if direction_angle == g_sensor.fetch():
                        break
                    time.sleep(0.01)
                return False
            
            #nav.turn(SLOW)
            #current_dist = us_sensor.fetch()
            #time.sleep(0.1) 
            #nav.stop()
        nav.stop()
        direction_angle = g_sensor.fetch()
        print(current_dist - us_sensor.fetch())
        if 1==0:
            continue
        else:
           # nav.turn(-MODERATE)
            print("correcting")
            #time.sleep(0.17)
            nav.stop()
            forward_dist = us_sensor.fetch()
            if forward_dist > 7:
                while forward_dist > 7:
                    align(direction_angle - 7)
                    nav.forward(SLOW)
                    time.sleep(0.05)
                    print("forward")
                    forward_dist = us_sensor.fetch()
                    print(forward_dist)
                    time.sleep(0.05)
            elif forward_dist < 4:
                while forward_dist < 4:
                    align(direction_angle)
                    nav.forward(-SLOW)
                    time.sleep(0.05)
                    print("backward")
                    forward_dist = us_sensor.fetch()
                    print(forward_dist)
                    time.sleep(0.05)

#                 if forward_dist > us_sensor.fetch():
#                     continue
#                 elif forward_dist < us_sensor.fetch():
#                     nav.turn(SLOW) #left
#                     time.sleep(0.05)
#                     left = us_sensor.fetch()
#                     if (left < forward_dist):
#                         continue
                
            nav.stop()
            return True

#Arm Grab Cube function

def grab_cube():
    #nav.dump_start()
    nb_of_tries = 0
    #while nb_of_tries < 2:
    find_cube()
    
    #Read Cube Color
    nav.turn(MODERATE)
    time.sleep(0.2)
    nav.stop()
    #nav.move_arm(-160)
    #time.sleep(1)
    nav.forward(MODERATE)
    time.sleep(0.4)
    nav.stop()
    
    color = None
    
    while (color == 'p' or color == None):
        color = color_sensor_left.fetch()
        print(color)
        time.sleep(0.05)

    nav.stop()
    nav.forward(-MODERATE)
    time.sleep(1)
    nav.stop()
    
    #nav.move_arm(160)
    #time.sleep(1)
    nav.turn(-SLOW)
    time.sleep(0.4)
    nav.stop()
    print(color)
    
    
    
    while True:
        if color == 'o' or color == 'y':
            #Grab Cube
            
            nav.move_arm(-80)
            time.sleep(2)
            #move forward here
            nav.forward(MODERATE)
            time.sleep(0.9)
            nav.stop()
            
            
            nav.move_arm(-220)
            time.sleep(0.7)
            nav.move_arm(220)
            #move back here
            nav.forward(-MODERATE)
            time.sleep(0.9)
            nav.stop()
            
            #time.sleep(1)
            nav.move_arm(80)
            time.sleep(0.2)
            #nav.dump_dump()
            return True
            
        else:
            nav.turn(-MODERATE)
            time.sleep(1)
            nav.stop()
            return False

def avoid_water():
    #nav.forward(MODERATE)
    #try:
    while True:
        if color_sensor_left.fetch() == "b" or color_sensor_left.fetch() == "p":
            nav.forward(-SLOW)
            time.sleep(0.1)
            nav.turn(SLOW)
            time.sleep(0.05)
            print("right")
            print(color_sensor_left.fetch())
        elif color_sensor_right.fetch() == "b" or color_sensor_right.fetch() == "p":
            nav.forward(-SLOW)
            time.sleep(0.1)
            nav.turn(-SLOW)
            time.sleep(0.05)
            print("left")
            print(color_sensor_right.fetch())
        else:
            break
   # finally:
    #    reset_brick()
            
#MAIN LOOP
# try:
#     while True:
#         speed = FAST
#         nav.forward(speed)
#         #avoid_water()
#         while True:
#             #avoid_water()
#             #DISTANCE
#             dist = us_sensor.fetch()
#             print(dist)
#             if dist is None:
#                 print("dist is none")
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
#                 
#                 #if check_wall() is False:
#                 if grab_cube():
#                     break
#                         # add +1 to dump counter
#                 else:
#                     nav.turn(MODERATE)
#                     time.sleep(1)
#                     nav.stop()
#                     dist = us_sensor.fetch()
#                 

#             #COLOR
#             color = color_sensor_left.fetch()
#             if color is None:
#                 nav.stop()
#                 color = wait_for(color_sensor_left.fetch)
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
#                     print("angle ", angle)
#                     if angle is None:
#                         print("angle is none")
#                         nav.stop()
#                         angle = wait_for(g_sensor.fetch)
#                         nav.turn(SLOW)
#                     if abs(angle) > 89:
#                        nav.stop()
#                        break
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
#                 print("dist is none")
#                 nav.stop()
#                 dist = wait_for(us_sensor.fetch)
#                 nav.turn(SLOW)
# 
#             angle = g_sensor.fetch()
#             if angle is None:
#                 print("angle is none")
#                 nav.stop()
#                 angle = wait_for(g_sensor.fetch)
#                 nav.turn(SLOW)
#             break
#             #if abs(angle) > 89 and dist > 40:
#              #   nav.stop()
#               #  break
# 
finally:
  reset_brick()

