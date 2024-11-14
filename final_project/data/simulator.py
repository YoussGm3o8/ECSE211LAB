"""
Simulator for the ultrasonic sensor using Pygame.
"""

import pygame
import random
import math
import os
import sys
import csv

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 800
FPS = 60
CART_SIZE = (40, 40)
CART_COLOR = (0, 255, 0)  # Green color for the cart
BACKGROUND_COLOR = (255, 255, 255)  # White background
BORDER_COLOR = (0, 0, 0)  # Black border
CUBE_COLOR = (255, 0, 0)  # Red color for cubes
LINE_COLOR = (0, 0, 255)  # Blue color for ultrasonic sensor line
SPEED = 4

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultrasonic Sensor Simulator")

# Cart class with rotation and movement along its facing direction
class Cart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CART_SIZE[0]
        self.height = CART_SIZE[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.angle = 0  # Initial facing angle (0 degrees is to the right)

    def move(self, speed):
        # Calculate the movement vector based on the cart's angle
        radian_angle = math.radians(self.angle)
        dx = math.cos(radian_angle) * speed
        dy = math.sin(radian_angle) * speed

        # Move the cart while ensuring it stays within bounds
        if 0 <= self.x + dx <= WIDTH - self.width:
            self.x += dx
        if 0 <= self.y + dy <= HEIGHT - self.height:
            self.y += dy

        self.rect.topleft = (self.x, self.y)

    def rotate(self, direction):
        """Rotate the cart and ultrasonic sensor ray by 5 degrees.

        `direction`: 1 for right (clockwise), -1 for left (counterclockwise)
        """
        self.angle += direction * 5  # Rotate by 5 degrees (clockwise or counterclockwise)
        if self.angle >= 360:
            self.angle -= 360  # Wrap around at 360 degrees
        elif self.angle < 0:
            self.angle += 360  # Wrap around at 0 degrees

    def draw(self):
        pygame.draw.rect(screen, CART_COLOR, self.rect)

# Cube class
class Cube:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        pygame.draw.rect(screen, CUBE_COLOR, self.rect)

# Function to detect collision with walls or cubes
def detect_collision(cart, cubes):
    radian_angle = math.radians(cart.angle)  # Convert cart's angle to radians

    # Calculate the front position of the cart (the front center, where the ultrasonic sensor is located)
    front_x = cart.x + cart.width / 2 + math.cos(radian_angle) * cart.width / 2
    front_y = cart.y + cart.height / 2 + math.sin(radian_angle) * cart.height / 2

    x1, y1 = front_x, front_y  # Start the ray from the front of the cart
    line_length = 0
    # Loop to simulate the ray from the front of the cart until it hits something
    while 0 <= x1 <= WIDTH and 0 <= y1 <= HEIGHT and line_length < 1000:
        # Update the coordinates based on the angle and distance
        x1 = front_x + math.cos(radian_angle) * line_length
        y1 = front_y + math.sin(radian_angle) * line_length
        line_length += 1

        # Check for collision with walls (screen edges)
        if x1 <= 0 or x1 >= WIDTH or y1 <= 0 or y1 >= HEIGHT:
            pygame.draw.line(screen, LINE_COLOR, (front_x, front_y), (x1, y1))
            distance = math.sqrt((front_x - x1)**2 + (front_y - y1)**2)
            return distance  # Return the collision coordinates

        # Check for collision with cubes
        for cube in cubes:
            if cube.rect.collidepoint(x1, y1):
                pygame.draw.line(screen, LINE_COLOR, (front_x, front_y), (x1, y1))
                distance = math.sqrt((front_x - x1)**2 + (front_y - y1)**2)
                return distance

    return None

KEYS = {"K_LEFT": False, "K_RIGHT": False, "K_UP": False, "K_DOWN": False}

timestep = 0
observations = []
cubes = []
# Main function
def main(simulate):
    cart = Cart(WIDTH // 2 - CART_SIZE[0] // 2, HEIGHT // 2 - CART_SIZE[1] // 2)
    clock = pygame.time.Clock()
    running = True
    if simulate:
        KEYS["K_LEFT"] = True
        global FPS
        FPS = 600
    while running:
        screen.fill(BACKGROUND_COLOR)  # Fill the screen with white

        # Draw the border (walls)
        pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), 5)

        # Draw cubes
        for cube in cubes:
            cube.draw()

        # Draw the cart
        cart.draw()

        # Draw the ultrasonic sensor line
        distance = detect_collision(cart, cubes)

        if distance:
            global timestep
            timestep += 1
            print(f"Distance: {distance:.1f}, Timestep: {timestep}")
            observations.append((timestep, distance))

        # Handle events
        if not simulate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # Save the pixels to screenshot
                    global screenshot
                    screenshot = pygame.Surface((WIDTH, HEIGHT))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        KEYS["K_LEFT"] = True
                    elif event.key == pygame.K_RIGHT:
                        KEYS["K_RIGHT"] = True
                    elif event.key == pygame.K_UP:
                        KEYS["K_UP"] = True
                    elif event.key == pygame.K_DOWN:
                        KEYS["K_DOWN"] = True
                    elif event.key == pygame.K_a:  # Add a cube at a random location
                        cube = Cube(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20))
                        cubes.append(cube)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        KEYS["K_LEFT"] = False
                    elif event.key == pygame.K_RIGHT:
                        KEYS["K_RIGHT"] = False
                    elif event.key == pygame.K_UP:
                        KEYS["K_UP"] = False
                    elif event.key == pygame.K_DOWN:
                        KEYS["K_DOWN"] = False
        else:
            if timestep >= 500:
                running = False

        # Handle actions
        if KEYS["K_LEFT"]:
            cart.rotate(-0.5)
        if KEYS["K_RIGHT"]:
            cart.rotate(0.5)
        if KEYS["K_UP"]:
            cart.move(SPEED)
        if KEYS["K_DOWN"]:
            cart.move(-SPEED)

        pygame.display.flip()  # Update the screen
        clock.tick(FPS)  # Maintain the framerate

    pygame.quit()


if __name__ == "__main__":
    """
    ---------------------------
    define cubes positions below
    """
    cubes.append(Cube(100, 100))


    """
    ---------------------------
    """

    if len(sys.argv) < 2:
        print("Usage: python simulator.py <output_file>")
    if len(sys.argv) == 3 and sys.argv[2] == "--simulate":
        main(True)
    else:
        main(False)

    path = os.path.join(os.path.dirname(__file__), "csv", "simulated", f"{sys.argv[1]}")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestep", "Distance"])
        writer.writerows(observations)
    print(f"Observations saved to {path}")

    ss_path = os.path.join(os.path.dirname(__file__), "csv", "simulated", f"{sys.argv[1]}_box_position.csv")
    with open(ss_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"])
        for cube in cubes:
            writer.writerow([cube.x, cube.y])
    print(f"Cube positions saved to {ss_path}")

