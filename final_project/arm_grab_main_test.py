"""
main.py

DESCRIPTION: A robot that avoids wall and water
"""
from utils.brick import reset_brick
import time
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor, color_sensor2
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
from components import engine
import components.object_detection as od

#CONSTANTS

TIMEOUT = 10

SLOW = 90
MODERATE = 180
FAST = 360

#apply median filter to sensor with a window of 10
us_sensor = engine.us_sensor
color_sensor_left = color_sensor
color_sensor_right = color_sensor2
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
    
    if color == 'unkown':
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
    #time.sleep(0.5)
    start = time.time()
    direction_angle = g_sensor.fetch() + 20
    while (abs(us_sensor.fetch() - current_dist) < 4) :
        time.sleep(0.1)
        if time.time() - start > 3:
            while True:
                    align(direction_angle)
                    if direction_angle == g_sensor.fetch():
                        break
                    time.sleep(0.01)
            return False
    nav.stop()
    
    after_dist = us_sensor.fetch()
    print("after turning: " , after_dist)
    start = time.time()
    direction_angle = g_sensor.fetch() + 20
    while True:
        #if abs(after_dist - current_dist) < 10: #wall
         #   return False
            
        while (abs(after_dist - current_dist ) > 4):
            #time.sleep(0.1)
            nav.turn(-SLOW/2)
            print(current_dist - us_sensor.fetch())
            after_dist = us_sensor.fetch()
            time.sleep(0.1)
            if time.time() - start > 3: # wall or hallucination
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
    if True:
        od.scan(3)
    
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
        
        while (color == 'unkown' or color == None):
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
                time.sleep(1)
                #move forward here
                nav.forward(MODERATE)
                time.sleep(0.7)
                nav.stop()
                
                
                nav.move_arm(-220)
                time.sleep(0.7)
                nav.move_arm(220)
                #move back here
                nav.forward(-MODERATE)
                time.sleep(0.7)
                nav.stop()
                
                #time.sleep(1)
                nav.move_arm(80)
                time.sleep(0.2)
                nav.reset_dump()
                return True
                
            else:
                nav.turn(-MODERATE)
                time.sleep(1)
                nav.stop()
                return False
    else:
        nav.stop()
        return False

def avoid_water():
    nav.forward(MODERATE)
#     try:
    while True:
        if color_sensor_left.fetch() == None or color_sensor_right.fetch() == None or color_sensor_left.fetch() == "unkown" or color_sensor_right.fetch() == "unkown":
            print("left: ",color_sensor_left.fetch())
            print("right: ", color_sensor_right.fetch())
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
            nav.forward(MODERATE)
#     finally:
#         reset_brick()
            
#MAIN LOOP
def main():
    try:
        while True:
            speed = FAST
            nav.forward(speed)
            #avoid_water()
            while True:
                #avoid_water()
                #DISTANCE
                dist = us_sensor.fetch()
                print(dist)
                
                if dist is None:
                    print("dist is none")
                    nav.stop()
                    dist = wait_for(us_sensor.fetch)
                    nav.forward(speed)

                if color_sensor_left.fetch() == "y" and us_sensor.fetch() < 30:
                    nav.forward(MODERATE)
                    time.sleep(1)
                    nav.stop()
                    nav.turn(MODERATE) # turn right
                    time.sleep(0.25)
                    nav.stop()
                    nav.forward(MODERATE)
                    time.sleep(0.3)
                    nav.stop()
                    nav.turn(MODERATE) # turn right
                    time.sleep(0.25)
                    nav.stop()
                    nav.forward(MODERATE)
                    time.sleep(0.3)
                    nav.stop()
                    nav.dump_dump()
                    nav.reset_dump()
                     

                if speed != FAST:
                    if dist >= 30:
                        speed = FAST
                        nav.forward(speed)
                elif dist < 30: #speed must be FAST too
                    speed = MODERATE
                    nav.forward(speed)

                if dist < 15:          
                    
                    #if check_wall() is False:
                    #if grab_cube():
                     #   break
                            # add +1 to dump counter
                    #else:
                     nav.turn(MODERATE) # turn right
                     time.sleep(0.25)
                     nav.stop()
                     dist = us_sensor.fetch()

    finally:
      engine.end()

