import pygame
import sys

# ----- CONFIG -----
WIDTH, HEIGHT = 500, 500
FLOORS = 9

# ----- INIT -----
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Delivery Robot")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

floor_height = HEIGHT // FLOORS
robot_floor = 0
target_floor = None
status = "Idle"
move_delay = 30  # frames between floor changes
move_timer = 0

def draw_building():
    screen.fill((250, 250, 250))

    for i in range(FLOORS):
        y = HEIGHT - (i + 1) * floor_height
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y), 2)
        label = font.render(f"Lab {i}", True, (50, 50, 50))
        screen.blit(label, (WIDTH - 80, y + 5))  # Draw label on right side

    # Robot
    ry = HEIGHT - (robot_floor + 1) * floor_height + floor_height // 2 - 10
    pygame.draw.circle(screen, (0, 120, 255), (WIDTH // 2, ry), 20)

    # Status
    stat_txt = font.render(f"Status: {status}", True, (0, 100, 0))
    loc_txt = font.render(f"Current Floor: {robot_floor}", True, (0, 0, 0))
    screen.blit(stat_txt, (10, 10))
    screen.blit(loc_txt, (10, 40))

# ----- MAIN LOOP -----
running = True
while running:
    draw_building()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                             pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                target_floor = int(event.unicode)
                if target_floor != robot_floor:
                    status = f"Moving to Lab {target_floor}"

    # Move step-by-step
    if target_floor is not None and robot_floor != target_floor:
        move_timer += 1
        if move_timer >= move_delay:
            if robot_floor < target_floor:
                robot_floor += 1
            elif robot_floor > target_floor:
                robot_floor -= 1
            move_timer = 0

    if target_floor == robot_floor and status != "Idle" and target_floor is not None:
        status = f"Arrived at Lab {robot_floor}"
        target_floor = None

pygame.quit()
sys.exit()