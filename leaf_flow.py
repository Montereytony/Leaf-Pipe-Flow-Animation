import pygame
import random
import math
import asyncio
import platform

# Window dimensions (in meters, scaled to pixels)
WIDTH, HEIGHT = 6.0, 4.0  # 6m wide, 4m tall
PIXELS_PER_METER = 100  # 1m = 100 pixels
FPS = 60
FRAME_TIME = 1.0 / FPS  # Seconds per frame

# Perturbation range (m/s)
PERTURBATION_MIN = -0.5  # Minimum perturbation
PERTURBATION_MAX = 0.5   # Maximum perturbation

# Colors
BLUE = (0, 100, 200)  # Water
GRAY = (100, 100, 100)  # Pipe walls
RED = (255, 0, 0)  # Predicted path
GREEN = (0, 255, 0)  # Leaf (actual path)
WHITE = (255, 255, 255)  # Background
BLACK = (0, 0, 0)  # Text

# Pipe boundaries (in meters)
PIPE_TOP = 1.0  # 1m
PIPE_BOTTOM = 3.0  # 3m

# Leaf properties
leaf_pos = [0.5, (PIPE_TOP + PIPE_BOTTOM) / 2]  # Start at x=0.5m, y=2.0m
leaf_radius = 0.05  # 5cm
leaf_speed = 1.0  # No arbitrary scaling

# Path and run tracking
predicted_path = []
actual_path = []
run_count = 0
all_deviations = []  # Store deviations for each run
max_runs = 30
running = True
paused = False  # Pause state

# Font for text
font = pygame.font.SysFont('arial', 20)

# Simplified parabolic velocity field (m/s)
def get_flow_velocity(y):
    center = (PIPE_TOP + PIPE_BOTTOM) / 2
    max_vx = 1.0  # Max x-velocity 1.0 m/s (faster runs)
    vy = 0.0  # No vertical flow
    vx = max_vx * (1 - ((y - center) / ((PIPE_BOTTOM - PIPE_TOP) / 2)) ** 2)
    return vx, vy

# Predict path (meters, seconds)
def predict_path(start_x, start_y, max_steps=500):
    path = []
    x, y = start_x, start_y
    dt = 0.1  # Time step in seconds
    for _ in range(max_steps):
        if x >= WIDTH:
            break
        vx, vy = get_flow_velocity(y)
        x += vx * dt * leaf_speed
        y += vy * dt * leaf_speed
        y = max(PIPE_TOP + leaf_radius, min(PIPE_BOTTOM - leaf_radius, y))
        path.append((x, y))
    if path and path[-1][0] < WIDTH:
        last_x, last_y = path[-1]
        vx, vy = get_flow_velocity(last_y)
        while last_x < WIDTH:
            last_x += vx * dt * leaf_speed
            last_y += vy * dt * leaf_speed
            last_y = max(PIPE_TOP + leaf_radius, min(PIPE_BOTTOM - leaf_radius, last_y))
            path.append((last_x, last_y))
    return path

# Compute statistics
def compute_stats(deviations):
    if not deviations:
        return 0, 0, 0
    flat_deviations = [d for run in deviations for d in run]
    avg_dev = sum(flat_deviations) / len(flat_deviations)
    max_dev = max(flat_deviations)
    variance = sum((d - avg_dev) ** 2 for d in flat_deviations) / len(flat_deviations)
    std_dev = math.sqrt(variance) if variance > 0 else 0
    return avg_dev, max_dev, std_dev

# Display statistics
def display_stats(avg_dev, max_dev, std_dev):
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, 0, int(WIDTH * PIXELS_PER_METER), int(PIPE_TOP * PIXELS_PER_METER)))
    pygame.draw.rect(screen, GRAY, (0, int(PIPE_BOTTOM * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((HEIGHT - PIPE_BOTTOM) * PIXELS_PER_METER)))
    pygame.draw.rect(screen, BLUE, (0, int(PIPE_TOP * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((PIPE_BOTTOM - PIPE_TOP) * PIXELS_PER_METER)))
    draw_ruler()
    texts = [
        font.render("Predicted Path (Red Line): Ideal Laminar Flow", True, BLACK),
        font.render("Floating Leaf (Green Dot): Actual Path with Perturbations", True, BLACK),
        font.render(f"Runs Completed: {max_runs}", True, BLACK),
        font.render(f"Average Deviation: {avg_dev:.6f} m", True, BLACK),
        font.render(f"Maximum Deviation: {max_dev:.6f} m", True, BLACK),
        font.render(f"Std Deviation: {std_dev:.6f} m", True, BLACK)
    ]
    for i, text in enumerate(texts):
        screen.blit(text, (20, 20 + i * 25))
    pygame.display.flip()

# Draw x-y ruler
def draw_ruler():
    pygame.draw.line(screen, BLACK, (0, int(PIPE_BOTTOM * PIXELS_PER_METER)), (int(WIDTH * PIXELS_PER_METER), int(PIPE_BOTTOM * PIXELS_PER_METER)), 2)
    for x in range(0, int(WIDTH) + 1, 1):
        x_pixel = int(x * PIXELS_PER_METER)
        pygame.draw.line(screen, BLACK, (x_pixel, int(PIPE_BOTTOM * PIXELS_PER_METER)), (x_pixel, int(PIPE_BOTTOM * PIXELS_PER_METER) + 10), 2)
        label = font.render(f"{x}", True, BLACK)
        screen.blit(label, (x_pixel - 10, int(PIPE_BOTTOM * PIXELS_PER_METER) + 15))
    pygame.draw.line(screen, BLACK, (0, int(PIPE_TOP * PIXELS_PER_METER)), (0, int(PIPE_BOTTOM * PIXELS_PER_METER)), 2)
    for y in range(int(PIPE_TOP), int(PIPE_BOTTOM) + 1, 1):
        y_pixel = int(y * PIXELS_PER_METER)
        pygame.draw.line(screen, BLACK, (0, y_pixel), (10, y_pixel), 2)
        label = font.render(f"{y:.1f}", True, BLACK)
        screen.blit(label, (15, y_pixel - 10))

# Initialize
def setup():
    global leaf_pos, actual_path, predicted_path, run_count, all_deviations, running
    leaf_pos = [0.5, (PIPE_TOP + PIPE_BOTTOM) / 2]
    actual_path = [leaf_pos[:]]
    predicted_path = predict_path(leaf_pos[0], leaf_pos[1])
    if run_count < max_runs:
        all_deviations.append([])

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((int(WIDTH * PIXELS_PER_METER), int(HEIGHT * PIXELS_PER_METER)))
pygame.display.set_caption("Leaf in Pipe Flow")
clock = pygame.time.Clock()

def update_loop():
    global leaf_pos, actual_path, run_count, running, paused
    # Handle pause toggle
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused

    if not running:
        avg_dev, max_dev, std_dev = compute_stats(all_deviations)
        display_stats(avg_dev, max_dev, std_dev)
        return

    if paused:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, (0, 0, int(WIDTH * PIXELS_PER_METER), int(PIPE_TOP * PIXELS_PER_METER)))
        pygame.draw.rect(screen, GRAY, (0, int(PIPE_BOTTOM * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((HEIGHT - PIPE_BOTTOM) * PIXELS_PER_METER)))
        pygame.draw.rect(screen, BLUE, (0, int(PIPE_TOP * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((PIPE_BOTTOM - PIPE_TOP) * PIXELS_PER_METER)))
        draw_ruler()
        if predicted_path:
            pygame.draw.lines(screen, RED, False, [(int(x * PIXELS_PER_METER), int(y * PIXELS_PER_METER)) for x, y in predicted_path], 3)
        if len(actual_path) > 1:
            pygame.draw.lines(screen, GREEN, False, [(int(x * PIXELS_PER_METER), int(y * PIXELS_PER_METER)) for x, y in actual_path], 2)
        pygame.draw.circle(screen, GREEN, (int(leaf_pos[0] * PIXELS_PER_METER), int(leaf_pos[1] * PIXELS_PER_METER)), int(leaf_radius * PIXELS_PER_METER))
        texts = [
            font.render("Predicted Path (Red Line): Ideal Laminar Flow", True, BLACK),
            font.render("Floating Leaf (Green Dot): Actual Path with Perturbations", True, BLACK),
            font.render(f"Run: {run_count + 1}/{max_runs}", True, BLACK),
            font.render("Paused (Press Space to Resume)", True, BLACK)
        ]
        for i, text in enumerate(texts):
            screen.blit(text, (20, 20 + i * 25))
        pygame.display.flip()
        return

    # Update position
    vx, vy = get_flow_velocity(leaf_pos[1])
    perturbation = random.uniform(PERTURBATION_MIN, PERTURBATION_MAX)
    leaf_pos[0] += (vx + perturbation) * leaf_speed * FRAME_TIME
    center = (PIPE_TOP + PIPE_BOTTOM) / 2
    distance_from_center = leaf_pos[1] - center
    repulsion = -0.3 * (distance_from_center / ((PIPE_BOTTOM - PIPE_TOP) / 2)) ** 3
    leaf_pos[1] += (vy + perturbation + repulsion * FRAME_TIME) * leaf_speed * FRAME_TIME
    leaf_pos[1] = max(PIPE_TOP + leaf_radius, min(PIPE_BOTTOM - leaf_radius, leaf_pos[1]))
    actual_path.append(leaf_pos[:])
    deviation = abs(leaf_pos[1] - 2.0)
    all_deviations[run_count].append(deviation)
    if leaf_pos[0] > WIDTH:
        run_count += 1
        if run_count >= max_runs:
            running = False
        else:
            setup()

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (0, 0, int(WIDTH * PIXELS_PER_METER), int(PIPE_TOP * PIXELS_PER_METER)))
    pygame.draw.rect(screen, GRAY, (0, int(PIPE_BOTTOM * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((HEIGHT - PIPE_BOTTOM) * PIXELS_PER_METER)))
    pygame.draw.rect(screen, BLUE, (0, int(PIPE_TOP * PIXELS_PER_METER), int(WIDTH * PIXELS_PER_METER), int((PIPE_BOTTOM - PIPE_TOP) * PIXELS_PER_METER)))
    draw_ruler()
    if predicted_path:
        pygame.draw.lines(screen, RED, False, [(int(x * PIXELS_PER_METER), int(y * PIXELS_PER_METER)) for x, y in predicted_path], 3)
    if len(actual_path) > 1:
        pygame.draw.lines(screen, GREEN, False, [(int(x * PIXELS_PER_METER), int(y * PIXELS_PER_METER)) for x, y in actual_path], 2)
    pygame.draw.circle(screen, GREEN, (int(leaf_pos[0] * PIXELS_PER_METER), int(leaf_pos[1] * PIXELS_PER_METER)), int(leaf_radius * PIXELS_PER_METER))
    texts = [
        font.render("Predicted Path (Red Line): Ideal Laminar Flow", True, BLACK),
        font.render("Floating Leaf (Green Dot): Actual Path with Perturbations", True, BLACK),
        font.render(f"Run: {run_count + 1}/{max_runs}", True, BLACK)
    ]
    for i, text in enumerate(texts):
        screen.blit(text, (20, 20 + i * 25))
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(FRAME_TIME)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
