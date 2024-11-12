import pygame
import math
from communication.server import Server
# Initialize pygame
pygame.init()

# Define window size
WINDOW_SIZE = 1000
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# Set the window title
pygame.display.set_caption("Line from Origin")

# Function to draw a line from the origin with specified length and angle
def draw_line_from_origin(length, angle):
    # Convert angle from degrees to radians
    angle = angle % 360
    angle_rad = math.radians(angle)
    
    # Calculate the end point of the line using polar to Cartesian conversion
    x_end = length * math.cos(angle_rad) + 500
    y_end = length * math.sin(angle_rad) + 500

    # Draw the line (origin is (0, 0) and the end point is (x_end, y_end))
    pygame.draw.line(window, (0, 0, 0), (500, 500), (x_end, y_end), 2)
    window.set_at((int(x_end), int(y_end)), (255, 0, 0))
    # pygame.draw.circle(window, (255, 0, 0), (x_end, y_end), 2)

# Main loop
running = True
server = Server()

try:

    window.fill((0, 0, 0))
    window.set_at((500, 500), (0, 255, 0))
    for message in server:
        for data in message:
            if not running:
                break

            length, angle = data

            length *= 2
            print(length, angle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            draw_line_from_origin(length, angle)
                   
            pygame.display.flip()

except Exception as e:
    print(e)
finally:
    server.exit()
# Quit pygame
pygame.quit()

