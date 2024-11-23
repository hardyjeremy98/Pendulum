import pygame
import math
import sys
import screeninfo

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Pendulum")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Pendulum settings
pivot = (WIDTH // 2, 100)  # Pivot point
slider = (pivot[0] - 50, pivot[1] - 25, 100, 50)
rail_start = (100, 100)
rail_end = (WIDTH - 100, 100)
L = 400  # Length of the pendulum
L_m = 400 * 0.0025  # Length of the pendulum in meters for calculations
theta = math.radians(45)  # Initial angle
omega = 0  # Angular velocity
g = 9.81  # Gravity
damping = 0.999  # Damping factor (0.9=critical damping)
mouse_held_bob = False  # Whether the mouse is holding the pendulum
mouse_held_slider = False  # Whether the mouse is holding the slider
mouse_velocity = (0, 0)
mouse_acceleration = (0, 0)

# Simulation parameters
fps = 60
dt = 1 / fps


def calculate_pendulum_position():
    """Calculate the x, y position of the pendulum bob."""
    x = pivot[0] + L * math.sin(theta)
    y = pivot[1] + L * math.cos(theta)
    return int(x), int(y)


def update_pendulum_physics():
    """Update pendulum physics: calculate angular acceleration, velocity, and position."""
    global alpha, omega, theta
    alpha = -(g / L_m) * math.sin(theta)  # Angular acceleration
    omega += alpha * dt  # Update angular velocity
    omega *= damping  # Apply damping
    theta += omega * dt  # Update angle


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mouse interaction
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    mouse_vx, mouse_vy = mouse_dx / dt, mouse_dy / dt
    mouse_dvx, mouse_dvy = mouse_vx - mouse_velocity[0], mouse_vy - mouse_velocity[1]
    mouse_velocity = (mouse_vx, mouse_vy)

    mouse_ax, mouse_ay = mouse_dvx / dt, mouse_dvy / dt
    mouse_ax_m, mouse_ay_m = mouse_ax * 0.0025, mouse_ay * 0.0025
    mouse_acceleration = (mouse_ax, mouse_ay)
    print(mouse_acceleration)

    mouse_pressed = pygame.mouse.get_pressed()[0]

    if mouse_pressed and not mouse_held_bob and not mouse_held_slider:
        # If the mouse is clicked near the pendulum, hold it
        bob_x, bob_y = calculate_pendulum_position()
        if math.hypot(mouse_x - bob_x, mouse_y - bob_y) < 30:
            mouse_held_bob = True
            mouse_bob_diff_x = mouse_x - bob_x
            mouse_bob_diff_y = mouse_y - bob_y
            # print("Holding bob")
        if (mouse_x > slider[0] and mouse_x < slider[0] + slider[2]) and (
            mouse_y > slider[1] and mouse_y < slider[1] + slider[3]
        ):
            mouse_held_slider = True
            mouse_pivot_diff_x = mouse_x - pivot[0]
            # print("Holding slider")

    if mouse_held_bob:
        # Update pendulum angle based on mouse position
        theta = math.atan2(
            (mouse_x - mouse_bob_diff_x) - pivot[0],
            (mouse_y - mouse_bob_diff_y) - pivot[1],
        )
        omega = 0  # Reset angular velocity when being dragged

        # Release the pendulum when the mouse button is released
        if not mouse_pressed:
            mouse_held_bob = False

    if mouse_held_slider:
        # Update slider position based on mouse position
        pivot_x = min(rail_end[0], max(rail_start[0], mouse_x - mouse_pivot_diff_x))
        pivot = (pivot_x, pivot[1])
        slider = (pivot[0] - 50, pivot[1] - 25, 100, 50)

        alpha = -(g / L_m) * math.sin(theta)  # Angular acceleration
        omega += alpha * dt  # Update angular velocity
        omega *= damping  # Apply damping
        theta += omega * dt  # Update angle

        if not mouse_pressed:
            mouse_held_slider = False

    if not mouse_held_bob and not mouse_held_slider:
        # Pendulum physics
        # print("Not holding")
        alpha = -(g / L_m) * math.sin(theta)  # Angular acceleration
        omega += alpha * dt  # Update angular velocity
        omega *= damping  # Apply damping
        theta += omega * dt  # Update angle

    # Drawing
    screen.fill(WHITE)
    pygame.draw.line(
        screen, (200, 200, 200), rail_start, rail_end, width=10
    )  # draw rail
    pygame.draw.circle(
        screen, (200, 200, 200), rail_start, radius=10
    )  # draw rail start point
    pygame.draw.circle(
        screen, (200, 200, 200), rail_end, radius=10
    )  # draw rail end point
    pygame.draw.rect(screen, (100, 200, 200), slider)  # Draw rectangle
    pygame.draw.circle(screen, BLACK, pivot, 5)  # Draw pivot
    bob_pos = calculate_pendulum_position()
    pygame.draw.aaline(screen, BLACK, pivot, bob_pos)  # Draw rod
    pygame.draw.circle(screen, RED, bob_pos, 25)  # Draw pendulum bob

    # Update display
    pygame.display.flip()
    clock.tick(fps)
