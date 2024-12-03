import subsystem.car as car
import time
from common.constants_params import *
from collections import deque




TURN_SPEED = 200
FORWARD_SPEED = 200
TIMER = 120
YELLOW_CONFIDENCE_COUNT = 6

car = car.Car(debug=False)

def avoid_water(car):
    water_f = car.is_water()
    if water_f[0] == True:
        car.turn_right(TURN_SPEED)
        while water_f[0] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.2)
        car.forward(FORWARD_SPEED)
    if water_f[1] == True:
        car.turn_left(TURN_SPEED)
        while water_f[1] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.2) #important to overturn
        car.forward(FORWARD_SPEED)

def check_cube(car):
    # always detects wall next to cube...
    # if car.avoid_wall(8):
    #     print("wall detected next to cube")
    #     return
    car.update(0.05)
    object = car.mini_scan()
    if object[0] is not None:
        if object[1] == "o" or object[1] == "y":
            print("cube color detected ", object[1], "at sensor ", object[0])
            car.stop()
            # print(object)
            # input("press any to continue")
            car.collect_cube()
            # car.forward(FORWARD_SPEED)
        else:
            print("cube color detected avoiding ", object[1], "at sensor ", object[0])
            avoiding = car.avoid_wall(25)
            if avoiding[0]:
                if avoiding[1] == "right":
                    car.turn_left(TURN_SPEED, 20)
                    if car.is_water()[0]:
                        car.reverse(FORWARD_SPEED, 10)
                        car.wait_for_action()
                    car.wait_for_action()
                elif avoiding[1] == "left":
                    car.turn_right(TURN_SPEED, 20)
                    if car.is_water()[0]:
                        car.reverse(FORWARD_SPEED, 10)
                        car.wait_for_action()
                    car.wait_for_action()
                elif avoiding[1] == "front":
                    car.turn_right(TURN_SPEED, 40)
                    if car.is_water()[0]:
                        car.reverse(FORWARD_SPEED, 10)
                        car.wait_for_action()
                    car.wait_for_action()
            else:
                car.turn_right(TURN_SPEED, 5)
                if car.is_water()[0]:
                        car.reverse(FORWARD_SPEED, 5)
                        car.wait_for_action()
                car.wait_for_action()


def scan(car, duration=10, treshold=25):
    if True: #car.clock % 30 == 0:
        print("---------------scanning ---------------")

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            avoid_water(car)

        car.turn_right(TURN_SPEED)
        for i in range(duration*2):
            check_cube(car)
            avoid_water(car)

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            avoid_water(car)

        car.forward(FORWARD_SPEED)
        time.sleep(0.1)
        car.stop()
    else:
        check_cube(car)

def check_wall(car):
    car.stop()
    avoiding = car.avoid_wall(10)
    if avoiding[0]:
        print("wall detected", avoiding[1])

        # car.reverse(TURN_SPEED, 2)
        car.wait_for_action()

        if avoiding[1] == "front":
            car.reverse(TURN_SPEED, 8)
            car.wait_for_action()
            car.turn_right(TURN_SPEED, 40)
            car.wait_for_action()
        elif avoiding[1] == "right":
            print("turn left for right wall")
            car.turn_left(TURN_SPEED, 20)
            car.wait_for_action()
        else:
            print("turn right for left wall")
            car.turn_right(TURN_SPEED, 20)
            car.wait_for_action()

        scan(car)

        car.forward(FORWARD_SPEED)
        
    else:
        scan(car)

def is_on_orange_line(color):
    """
    Determines if the color sensor is detecting the orange line
    """
    return color == 'o'


def is_confident_yellow(color):
    """
    Ensures the color is confidently yellow, avoiding false positives from green
    """
    return color == 'y'

# def follow_wall(car, wall_side='right'):
#     """
#     Follow a specific wall while scanning for cubes and avoiding water
#     wall_side can be 'right' or 'left'
#     """
#     # Yellow detection tracking
#     yellow_left_queue = deque(maxlen=YELLOW_CONFIDENCE_COUNT)
#     yellow_right_queue = deque(maxlen=YELLOW_CONFIDENCE_COUNT)
#     count = 0
#     while True:        
#         car.update(0.05)
#         # Check for water and avoid
#         avoid_water(car)
        
#         # Track yellow confidence
#         count += 1
#         yellow_left_queue.append(is_confident_yellow(car.state.left_color_sensor[-1]))
#         yellow_right_queue.append(is_confident_yellow(car.state.right_color_sensor[-1]))

#         print(car.state.left_color_sensor[-1], car.state.right_color_sensor[-1])
#         time.sleep(0.1)

#         # Check if we've found the home area with high confidence
#         if (all(yellow_left_queue) and all(yellow_right_queue) and count >= YELLOW_CONFIDENCE_COUNT):
#             car.stop()
#             print("Confident home area detected!")
#             if wall_side == 'right':
#                 us_wall = car.state.us_sensor_2 
#                 us_opp = car.state.us_sensor

#                 while True:
#                     car.update()
#                     us_wall = car.state.us_sensor
#                     us_opp = car.state.us_sensor_2
#                     print(us_wall, us_opp)
#                     if us_opp == 255:
#                         break
#                     if us_wall > 8:  # If the wall gets too far
#                         car.turn_right(TURN_SPEED, 2)  # Adjust towards the wall
#                         car.wait_for_action()
#                         car.forward(FORWARD_SPEED)
#                         time.sleep(0.05)
#                     elif us_wall < 8:  # If too close to the wall
#                         car.turn_left(TURN_SPEED, 2)  # Adjust away from the wall
#                         car.wait_for_action()
#                         car.forward(FORWARD_SPEED)
#                         time.sleep(0.05)
#                     else:
#                         car.forward(FORWARD_SPEED)
#                         time.sleep(0.1)
                        
#             else:
#                 us_wall = car.state.us_sensor_2
#                 us_opp = car.state.us_sensor

#                 while True:
#                     car.update()
#                     us_wall = car.state.us_sensor_2
#                     us_opp = car.state.us_sensor
#                     print(us_wall, us_opp)
#                     if us_opp == 255:
#                         break
#                     if us_wall > 8:  # If the wall gets too far
#                         car.turn_left(TURN_SPEED, 2)  # Adjust towards the wall
#                         car.wait_for_action()
#                         car.forward(FORWARD_SPEED)
#                     elif us_wall < 8:  # If too close to the wall
#                         car.turn_right(TURN_SPEED, 2)  # Adjust away from the wall
#                         car.wait_for_action()
#                         car.forward(FORWARD_SPEED)
#                     else:
#                         car.forward(FORWARD_SPEED)
#                         time.sleep(0.1)


        #     return
        # us1, us2 = car.state.us_sensor, car.state.us_sensor_2
        # # Wall following logic
        # if wall_side == 'right':
        #     if us1 > 15:  # If the wall gets too far
        #         car.turn_right(TURN_SPEED, 2)  # Adjust towards the wall
        #         car.wait_for_action()
        #         car.forward(FORWARD_SPEED)
        #     elif us1 < 5:  # If too close to the wall
        #         car.turn_left(TURN_SPEED, 2)  # Adjust away from the wall
        #         car.wait_for_action()
        #         car.forward(FORWARD_SPEED)
        #     else:
        #         car.forward(FORWARD_SPEED)
        #         time.sleep(0.1)
        # else:  # left wall following
        #     if us2 > 15:  # If the wall gets too far
        #         car.turn_left(TURN_SPEED, 2)  # Adjust towards the wall
        #         car.wait_for_action()
        #         car.forward(FORWARD_SPEED)
        #     elif us2 < 5:  # If too close to the wall
        #         car.turn_right(TURN_SPEED, 2)  # Adjust away from the wall
        #         car.wait_for_action()
        #         car.forward(FORWARD_SPEED)
        #     else:
        #         car.forward(FORWARD_SPEED)
        #         time.sleep(0.1)

def follow_wall_with_line(car, wall_side='right'):
    """
    Follow a specific wall while tracking the orange line and scanning for cubes and avoiding water
    wall_side can be 'right' or 'left'
    """
    # Orange line detection tracking
    orange_left_queue = deque(maxlen=1)
    orange_right_queue = deque(maxlen=1)
    
    # Yellow confidence tracking for home area detection
    yellow_left_queue = deque(maxlen=YELLOW_CONFIDENCE_COUNT)
    yellow_right_queue = deque(maxlen=YELLOW_CONFIDENCE_COUNT)
    
    count = 0
    while True:        
        car.update(0.05)
        
        # Check for water and avoid
        avoid_water(car)
        
        # Track orange line confidence
        orange_left_queue.append(is_on_orange_line(car.state.left_color_sensor[-1]))
        orange_right_queue.append(is_on_orange_line(car.state.right_color_sensor[-1]))
        
        # Track yellow line confidence for home area
        yellow_left_queue.append(is_confident_yellow(car.state.left_color_sensor[-1]))
        yellow_right_queue.append(is_confident_yellow(car.state.right_color_sensor[-1]))
        
        count += 1
        
        # Line following and wall following logic
        if wall_side == 'right':
            us1 = car.state.us_sensor
            if us1 > 15:  # If the wall gets too far
                car.turn_right(TURN_SPEED, 2)  # Adjust towards the wall
                car.wait_for_action()
                car.forward(FORWARD_SPEED)
            elif us1 < 5:  # If too close to the wall
                car.turn_left(TURN_SPEED, 2)  # Adjust away from the wall
                car.wait_for_action()
                car.forward(FORWARD_SPEED)
            else:
                # Fine-tune line following based on color sensors
                if all(orange_left_queue) and not all(orange_right_queue):
                    # Drift right to center on line
                    car.turn_right(TURN_SPEED, 1)
                elif all(orange_right_queue) and not all(orange_left_queue):
                    # Drift left to center on line
                    car.turn_left(TURN_SPEED, 1)
                else:
                    car.forward(FORWARD_SPEED)
                    time.sleep(0.1)
        else:  # left wall following
            us2 = car.state.us_sensor_2
            if us2 > 15:  # If the wall gets too far
                car.turn_left(TURN_SPEED, 2)  # Adjust towards the wall
                car.wait_for_action()
                car.forward(FORWARD_SPEED)
            elif us2 < 5:  # If too close to the wall
                car.turn_right(TURN_SPEED, 2)  # Adjust away from the wall
                car.wait_for_action()
                car.forward(FORWARD_SPEED)
            else:
                # Fine-tune line following based on color sensors
                if all(orange_left_queue) and not all(orange_right_queue):
                    # Drift right to center on line
                    car.turn_right(TURN_SPEED, 1)
                elif all(orange_right_queue) and not all(orange_left_queue):
                    # Drift left to center on line
                    car.turn_left(TURN_SPEED, 1)
                else:
                    car.forward(FORWARD_SPEED)
                    time.sleep(0.1)
        
        # Check if we've found the home area with high confidence
        if (all(yellow_left_queue) and all(yellow_right_queue) and count >= YELLOW_CONFIDENCE_COUNT):
            car.stop()
            print("Confident home area detected!")
            
            # Precise wall-following in home area
            if wall_side == 'right':
                us_wall = car.state.us_sensor
                us_opp = car.state.us_sensor_2

                while True:
                    car.update()
                    us_wall = car.state.us_sensor
                    us_opp = car.state.us_sensor_2
                    print(us_wall, us_opp)
                    
                    if us_opp == 255:
                        break
                    
                    if us_wall > 8:  # If the wall gets too far
                        car.turn_right(TURN_SPEED, 2)  # Adjust towards the wall
                        car.wait_for_action()
                        car.forward(FORWARD_SPEED)
                        time.sleep(0.05)
                    elif us_wall < 8:  # If too close to the wall
                        car.turn_left(TURN_SPEED, 2)  # Adjust away from the wall
                        car.wait_for_action()
                        car.forward(FORWARD_SPEED)
                        time.sleep(0.05)
                    else:
                        car.forward(FORWARD_SPEED)
                        time.sleep(0.1)
                        
            else:
                us_wall = car.state.us_sensor_2
                us_opp = car.state.us_sensor

                while True:
                    car.update()
                    us_wall = car.state.us_sensor_2
                    us_opp = car.state.us_sensor
                    print(us_wall, us_opp)
                    
                    if us_opp == 255:
                        break
                    
                    if us_wall > 8:  # If the wall gets too far
                        car.turn_left(TURN_SPEED, 2)  # Adjust towards the wall
                        car.wait_for_action()
                        car.forward(FORWARD_SPEED)
                    elif us_wall < 8:  # If too close to the wall
                        car.turn_right(TURN_SPEED, 2)  # Adjust away from the wall
                        car.wait_for_action()
                        car.forward(FORWARD_SPEED)
                    else:
                        car.forward(FORWARD_SPEED)
                        time.sleep(0.1)

            return
        
def return_home(car):
    """
    Smart return home function that:
    1. Determines which wall is closer to follow
    2. Follows that wall while scanning for cubes, avoiding water, and tracking the orange line
    3. Stops and dumps cubes when home area is detected with high confidence
    """
    # Determine wall distances
    right_wall_dist = car.state.us_sensor
    left_wall_dist = car.state.us_sensor_2
    
    print(f"Wall distances - Right: {right_wall_dist}, Left: {left_wall_dist}")
    
    # Follow the closer wall with line tracking
    if right_wall_dist < left_wall_dist:
        print("Following right wall with line tracking")
        follow_wall_with_line(car, wall_side='right')
    else:
        print("Following left wall with line tracking")
        follow_wall_with_line(car, wall_side='left')
    
    # Once in home area, dump cubes
    print("Home area reached!")

# def return_home(car):
#     """
#     assume you are at a border facing the wall
#     """
#     count = 0
#     while count < 5:
#         car.update(0.05)
#         if (car.state.right_color_sensor[-1] != 'y' and car.state.left_color_sensor[-1] != 'y'):
#             print(car.state.right_color_sensor[-1], car.state.left_color_sensor[-1])
#             if car.avoid_wall(10) == (True, "right"):
#                 car.turn_left(TURN_SPEED, 5)
#                 car.wait_for_action()
#                 car.forward(FORWARD_SPEED)
#             else:
#                 car.turn_right(TURN_SPEED, 5)
#         elif (car.state.right_color_sensor[-1] == 'y' and car.state.left_color_sensor[-1] == 'y'):
#             count += 1
#             print("was yellow at count:", count)
#             print(car.state.right_color_sensor[-1], car.state.left_color_sensor[-1])
#         else:
#             count = 0
    # car.forward(FORWARD_SPEED)
    # while True:
    #     car.update(0.05)
    #     if car.avoid_wall(15):
    #         break
    #     avoid_water(car)

    # car.turn_left(TURN_SPEED)
    # while(car.state.right_color_sensor[-1] != 'o'):
    #     print(car.state.right_color_sensor) #this may be white
    #     car.update(0.05)
    # car.stop()

    # car.turn_right(TURN_SPEED)
    # while(car.state.right_color_sensor[-1] == 'o'):
    #     car.update(0.05)
    # car.stop()

    # while True:
    #     car.update(0.05)
    #     print(car.state.right_color_sensor[-1], car.state.left_color_sensor[-1])
    #     if car.state.right_color_sensor[-1] == 'o':
    #         time.sleep(0.1) #adjust to overshoot
    #         car.turn_left(TURN_SPEED/2) #if this makes no sense its because the ports are wrong so ignore
    #         #car.turn_right(150)
    #     else:
    #         #car.turn_left(150)
    #         car.turn_right(TURN_SPEED/2)
        
    #     if car.state.right_color_sensor[-1] == 'y' and car.state.left_color_sensor[-1] == 'y':
    #         print(car.state.right_color_sensor[-1], car.state.left_color_sensor[-1])
    #         car.stop()
    #         car.dump_cubes()


try:
    ti = time.time()
    car.forward(FORWARD_SPEED)
    while True:
        if time.time() - ti > TIMER:
            print("time to return home!")
            break
        print("flag: ", car.flag)
        car.update(0.025)
        check_wall(car)
        avoid_water(car)
        scan(car)

    # while car.avoid_wall(10)[1] != "right":
    #     time.sleep(0.05)
    #     car.forward(FORWARD_SPEED)
    #     car.scan()
    #     print("not right")

        # if car.avoid_wall(40)[1] == "front":
        #     car.reverse(FORWARD_SPEED, 10)
        #     car.turn_left(TURN_SPEED, 20)
        # if car.avoid_wall(20)[1] == "right":
        #     print("right")
        #     car.turn_right(TURN_SPEED, 10)
        #     car.wait_for_action()
        #     car.forward(FORWARD_SPEED)
        #     time.sleep(0.5)
        #     car.stop() 
        # if car.avoid_wall(40)[1] == "left":
        #     print("left")
        #     car.turn_right(TURN_SPEED, 60)
        #     car.wait_for_action()
        #     car.forward(FORWARD_SPEED)
        #     time.sleep(0.5)
        #     car.stop()
        # else:
        #     car.forward(FORWARD_SPEED)
        #     car.avoid_water()
        #     car.scan()
    # print("wall found, returning home")
    return_home(car)
    car.dump_cubes()
    time.sleep(1)

finally:
    car.kill()

# def scan(car, duration=10):
#     if car.clock % 100 == 0:
#         print("scanning ---------------")
#         car.turn_left(100)
#         for i in range(duration):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.turn_right(100)
#         for i in range(duration*2):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.turn_left(100)
#         for i in range(duration):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.forward(150)
#     else:
#         check_cube(car)

