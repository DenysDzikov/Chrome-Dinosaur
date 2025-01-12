import pygame
import random
import sys

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = BLACK
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = 100
        self.y = WINDOW_HEIGHT - self.height - 50
        self.jump_speed = -15
        self.gravity = 0.8
        self.velocity = 0
        self.is_jumping = False
        self.lives = 3
    def jump(self):
        if not self.is_jumping:
            self.velocity = self.jump_speed
            self.is_jumping = True 
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > WINDOW_HEIGHT - self.height - 50:
            self.y = WINDOW_HEIGHT - self.height - 50
            self.velocity = 0
            self.is_jumping = False 
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
class Obstacle:
    def __init__(self, x):
        self.width = 30
        self.height = 50
        self.x = x
        self.y = WINDOW_HEIGHT - self.height - 50
        self.speed = 5 
    def update(self):
        self.x -= self.speed
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chrome Dinosaur")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    def reset_game(self):
        self.player = Player()
        self.obstacles = []
        self.game_state = "start"
        self.start_button = Button(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT//2 - 5, 100, 50, "Старт")
        self.score = 0
        self.timer = 60
        self.last_time = pygame.time.get_ticks()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state in ["start", "game_over", "win"]:
                    if self.start_button.is_clicked(event.pos):
                        self.reset_game()
                        self.game_state = "playing"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state == "playing":
                    self.player.jump()
        return True
    def update(self):
        if self.game_state == "playing":
            self.player.update()
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time >= 1000:
                self.timer -= 1
                self.last_time = current_time 
            if len(self.obstacles) == 0 or self.obstacles[-1].x < WINDOW_WIDTH - 300:
                self.obstacles.append(Obstacle(WINDOW_WIDTH)) 
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.x < -obstacle.width:
                    self.obstacles.remove(obstacle)
                    self.score += 1  
                if self.player.get_rect().colliderect(obstacle.get_rect()):
                    self.player.lives -= 1
                    self.obstacles.remove(obstacle)
                    if self.player.lives <= 0:
                        self.game_state = "game_over"      
            if self.timer <= 0:
                self.game_state = "win"
    def draw(self):
        self.screen.fill(WHITE)
        
        if self.game_state == "playing":
            self.player.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            score_text = self.font.render(f"Бали: {self.score}", True, BLACK)
            lives_text = self.font.render(f"Життів: {self.player.lives}", True, BLACK)
            timer_text = self.font.render(f"Час: {self.timer}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(timer_text, (10, 90))
        elif self.game_state in ["start", "game_over", "win"]:
            if self.game_state == "game_over":
                message = "Ти програв!\nНатисни 'Старт' щоб продовжити"
            elif self.game_state == "win":
                message = f"Ти переміг! Бали: {self.score}"
            else:
                message = "Chrome Dinosaur"
        
            lines = message.split('\n')
            for i, line in enumerate(lines):
                text = self.font.render(line, True, BLACK)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + i * 40))
                self.screen.blit(text, text_rect)

            self.start_button.draw(self.screen)
    
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
