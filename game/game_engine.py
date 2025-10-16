import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner_text = ""
        self.target_score = 5  # Default winning score

        # Initialize sounds (optional, comment if files missing)
        pygame.mixer.init()
        # self.sound_paddle = pygame.mixer.Sound("sounds/paddle.wav")
        # self.sound_wall = pygame.mixer.Sound("sounds/wall.wav")
        # self.sound_score = pygame.mixer.Sound("sounds/score.wav")

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        collision = self.ball.check_collision(self.player, self.ai)
        # if collision == "paddle":
        #     self.sound_paddle.play()

        # Score update
        if self.ball.x < 0:
            self.ai_score += 1
            self.ball.reset()
            # self.sound_score.play()
        elif self.ball.x > self.width:
            self.player_score += 1
            self.ball.reset()
            # self.sound_score.play()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

        # Check game over
        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.target_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.target_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

        if self.game_over:
            self.show_game_over_menu()

    def show_game_over_menu(self):
        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        # Winner message
        winner_surface = self.font.render(self.winner_text, True, WHITE)
        winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 3))
        screen.blit(winner_surface, winner_rect)

        # Replay options
        options = [
            "Best of 3 (Press 3)",
            "Best of 5 (Press 5)",
            "Best of 7 (Press 7)",
            "Exit (ESC)"
        ]
        for i, text in enumerate(options):
            opt_surface = self.font.render(text, True, WHITE)
            opt_rect = opt_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            screen.blit(opt_surface, opt_rect)

        pygame.display.flip()

        # Wait for player input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.target_score = 2  # Best of 3
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.target_score = 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.target_score = 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Reset for replay
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_text = ""

    def render(self, screen):
        # Draw paddles
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        # Draw ball
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        # Middle line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
        # Scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
