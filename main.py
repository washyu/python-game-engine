import pygame
import sys
from player import Player
from monster import Monster

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEADER_HEIGHT = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire Survival Style Game")

clock = pygame.time.Clock()

pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

# Define game states
TITLE, PLAYING, GAME_OVER, PAUSED = "TITLE", "PLAYING", "GAME_OVER", "PAUSED"
game_state = TITLE

player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT)

monsters = [Monster(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT) for _ in range(3)]

score = 0
level = 1

def draw_title_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    title_text = font.render("Vampire Survival", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2))
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press Enter to Start", True, (255, 255, 255))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + title_text.get_height()))

def reset_game(full_reset=True):
    global score, level
    player.reset_position()
    player.stones.clear()
    if full_reset:
        score = 0
        level = 1
        monsters.clear()
        for _ in range(3):
            new_monster = Monster(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT)
            monsters.append(new_monster)
    else:
        num_monsters = len(monsters)
        monsters.clear()
        for _ in range(num_monsters):
            monsters.append(Monster(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == TITLE:
        draw_title_screen()
        if joystick:
            start_button = joystick.get_button(7)
            if start_button:
                game_state = PLAYING

    elif game_state == PLAYING:
        if joystick:
            dx = joystick.get_axis(0)
            dy = joystick.get_axis(1)
            player.move(dx, dy)

            # Shooting direction from the right analog stick
            shoot_dx = joystick.get_axis(2)
            shoot_dy = joystick.get_axis(3)
            if shoot_dx != 0 or shoot_dy != 0:
                player.shoot(shoot_dx, shoot_dy)
        else:
            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            if keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_RIGHT]:
                dx += 1
            if keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_DOWN]:
                dy += 1
            player.move(dx, dy)

        for monster in monsters:
            monster.move_towards(player)
            monster.avoid_collisions(monsters)
        
        for stone in player.stones[:]:
            stone.move()
            if stone.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT):
                player.stones.remove(stone)

        for stone in player.stones[:]:
            for monster in monsters[:]:
                if stone.collides_with(monster):
                    player.stones.remove(stone)
                    monsters.remove(monster)
                    score += 1

                    new_monster = Monster(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT)
                    monsters.append(new_monster)
                    break
                # Check for collisions between player and monsters
        for monster in monsters:
            if (player.x < monster.x + monster.size and
                player.x + player.size > monster.x and
                player.y < monster.y + monster.size and
                player.y + player.size > monster.y):
                player.lives -= 1
                if player.lives > 0:
                    game_state = PAUSED
                    reset_game(full_reset=False)
                else:
                    game_state = GAME_OVER

        if score > 0 and score % 10 == 0:
            level += 1
            for _ in range(2):
                new_monster = Monster(SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT)
                monsters.append(new_monster)
            score += 1
        
        screen.fill((0, 0, 0))
        player.draw(screen)
        for monster in monsters:
            monster.draw(screen)
        for stone in player.stones:
            stone.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
        pygame.draw.line(screen, (255, 255, 255), (0, HEADER_HEIGHT), (SCREEN_WIDTH, HEADER_HEIGHT))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH // 2 - lives_text.get_width() // 2, 10))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    elif game_state == PAUSED:
        font = pygame.font.Font(None, 74)
        paused_text = font.render("Paused", True, (255, 255, 255))
        screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
        if joystick:
            start_button = joystick.get_button(7)
            if start_button:
                game_state = PLAYING

    elif game_state == GAME_OVER:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        if joystick:
            start_button = joystick.get_button(7)
            if start_button:
                reset_game(full_reset=True)
                player.lives = 3
                game_state = TITLE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
