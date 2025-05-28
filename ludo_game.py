import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 600
DICE_SIZE = 100
PLAYER_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)

# Player colors
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]

# Create the screen with resizable flag
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
pygame.display.set_caption('Ludo Game')

# Load images
def load_images():
    # We'll create our own board using drawing functions
    dice_images = []
    for i in range(1, 7):
        # Create dice faces programmatically
        dice_surface = pygame.Surface((DICE_SIZE, DICE_SIZE))
        dice_surface.fill(WHITE)
        pygame.draw.rect(dice_surface, BLACK, (0, 0, DICE_SIZE, DICE_SIZE), 2)
        
        # Draw dots based on dice value
        if i == 1:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
        elif i == 2:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
        elif i == 3:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
        elif i == 4:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
        elif i == 5:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
        elif i == 6:
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, DICE_SIZE//2), 8)
            pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, DICE_SIZE//2), 8)
            pygame.draw.circle(dice_surface, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
        
        dice_images.append(dice_surface)
    
    return dice_images

# Game board class
class LudoBoard:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = min(screen_width, screen_height) - 100
        self.cell_size = self.board_size // 15
        self.board_offset_x = (screen_width - self.board_size) // 2
        self.board_offset_y = (screen_height - self.board_size) // 2
        
        # Path coordinates for each player
        self.paths = self._create_paths()
        
        # Home positions for each player's tokens
        self.home_positions = [
            [(3*self.cell_size, 3*self.cell_size), 
             (3*self.cell_size, 5*self.cell_size),
             (5*self.cell_size, 3*self.cell_size), 
             (5*self.cell_size, 5*self.cell_size)],  # Red
            
            [(9*self.cell_size, 3*self.cell_size), 
             (9*self.cell_size, 5*self.cell_size),
             (11*self.cell_size, 3*self.cell_size), 
             (11*self.cell_size, 5*self.cell_size)],  # Green
            
            [(9*self.cell_size, 9*self.cell_size), 
             (9*self.cell_size, 11*self.cell_size),
             (11*self.cell_size, 9*self.cell_size), 
             (11*self.cell_size, 11*self.cell_size)],  # Blue
            
            [(3*self.cell_size, 9*self.cell_size), 
             (3*self.cell_size, 11*self.cell_size),
             (5*self.cell_size, 9*self.cell_size), 
             (5*self.cell_size, 11*self.cell_size)]   # Yellow
        ]
        
        # Final positions (center)
        self.final_positions = [
            [(1*self.cell_size, 7*self.cell_size), 
             (2*self.cell_size, 7*self.cell_size),
             (3*self.cell_size, 7*self.cell_size), 
             (4*self.cell_size, 7*self.cell_size)],  # Red
            
            [(7*self.cell_size, 1*self.cell_size), 
             (7*self.cell_size, 2*self.cell_size),
             (7*self.cell_size, 3*self.cell_size), 
             (7*self.cell_size, 4*self.cell_size)],  # Green
            
            [(13*self.cell_size, 7*self.cell_size), 
             (12*self.cell_size, 7*self.cell_size),
             (11*self.cell_size, 7*self.cell_size), 
             (10*self.cell_size, 7*self.cell_size)],  # Blue
            
            [(7*self.cell_size, 13*self.cell_size), 
             (7*self.cell_size, 12*self.cell_size),
             (7*self.cell_size, 11*self.cell_size), 
             (7*self.cell_size, 10*self.cell_size)]   # Yellow
        ]
    
    def _create_paths(self):
        # Create the path coordinates for each player
        # This is a simplified version - in a real game, you'd need more precise paths
        paths = []
        
        # Common path (outer ring)
        common_path = []
        
        # Bottom row (left to right)
        for i in range(1, 6):
            common_path.append((i * self.cell_size, 7 * self.cell_size))
        
        # Right column (top to bottom)
        for i in range(1, 6):
            common_path.append((6 * self.cell_size, i * self.cell_size))
        
        # Top row (left to right)
        for i in range(6, 9):
            common_path.append((i * self.cell_size, 1 * self.cell_size))
        
        # Right column (top to bottom)
        for i in range(1, 6):
            common_path.append((8 * self.cell_size, i * self.cell_size))
        
        # Right row (left to right)
        for i in range(9, 14):
            common_path.append((i * self.cell_size, 7 * self.cell_size))
        
        # Bottom column (top to bottom)
        for i in range(8, 14):
            common_path.append((13 * self.cell_size, i * self.cell_size))
        
        # Bottom row (right to left)
        for i in range(12, 7, -1):
            common_path.append((i * self.cell_size, 13 * self.cell_size))
        
        # Left column (bottom to top)
        for i in range(12, 7, -1):
            common_path.append((7 * self.cell_size, i * self.cell_size))
        
        # Left row (right to left)
        for i in range(6, 1, -1):
            common_path.append((i * self.cell_size, 7 * self.cell_size))
        
        # Top column (bottom to top)
        for i in range(6, 1, -1):
            common_path.append((1 * self.cell_size, i * self.cell_size))
        
        # Create paths for each player by rotating the common path
        for i in range(4):
            player_path = common_path[13*i:] + common_path[:13*i]
            paths.append(player_path)
        
        return paths
    
    def draw(self, screen):
        # Draw the board background
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x, self.board_offset_y, 
                          self.board_size, self.board_size))
        
        # Draw the colored home areas
        # Red (top-left)
        pygame.draw.rect(screen, RED, 
                         (self.board_offset_x, self.board_offset_y, 
                          6*self.cell_size, 6*self.cell_size))
        
        # Green (top-right)
        pygame.draw.rect(screen, GREEN, 
                         (self.board_offset_x + 9*self.cell_size, self.board_offset_y, 
                          6*self.cell_size, 6*self.cell_size))
        
        # Blue (bottom-right)
        pygame.draw.rect(screen, BLUE, 
                         (self.board_offset_x + 9*self.cell_size, self.board_offset_y + 9*self.cell_size, 
                          6*self.cell_size, 6*self.cell_size))
        
        # Yellow (bottom-left)
        pygame.draw.rect(screen, YELLOW, 
                         (self.board_offset_x, self.board_offset_y + 9*self.cell_size, 
                          6*self.cell_size, 6*self.cell_size))
        
        # Draw the white inner areas
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x + 2*self.cell_size, self.board_offset_y + 2*self.cell_size, 
                          2*self.cell_size, 2*self.cell_size))
        
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x + 11*self.cell_size, self.board_offset_y + 2*self.cell_size, 
                          2*self.cell_size, 2*self.cell_size))
        
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x + 11*self.cell_size, self.board_offset_y + 11*self.cell_size, 
                          2*self.cell_size, 2*self.cell_size))
        
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x + 2*self.cell_size, self.board_offset_y + 11*self.cell_size, 
                          2*self.cell_size, 2*self.cell_size))
        
        # Draw the center area
        pygame.draw.rect(screen, WHITE, 
                         (self.board_offset_x + 6*self.cell_size, self.board_offset_y + 6*self.cell_size, 
                          3*self.cell_size, 3*self.cell_size))
        
        # Draw colored paths to center
        # Red path
        for i in range(5):
            pygame.draw.rect(screen, RED, 
                            (self.board_offset_x + (1+i)*self.cell_size, 
                             self.board_offset_y + 7*self.cell_size, 
                             self.cell_size, self.cell_size))
        
        # Green path
        for i in range(5):
            pygame.draw.rect(screen, GREEN, 
                            (self.board_offset_x + 7*self.cell_size, 
                             self.board_offset_y + (1+i)*self.cell_size, 
                             self.cell_size, self.cell_size))
        
        # Blue path
        for i in range(5):
            pygame.draw.rect(screen, BLUE, 
                            (self.board_offset_x + (9+i)*self.cell_size, 
                             self.board_offset_y + 7*self.cell_size, 
                             self.cell_size, self.cell_size))
        
        # Yellow path
        for i in range(5):
            pygame.draw.rect(screen, YELLOW, 
                            (self.board_offset_x + 7*self.cell_size, 
                             self.board_offset_y + (9+i)*self.cell_size, 
                             self.cell_size, self.cell_size))
        
        # Draw grid lines
        for i in range(16):
            # Vertical lines
            pygame.draw.line(screen, BLACK, 
                            (self.board_offset_x + i*self.cell_size, self.board_offset_y), 
                            (self.board_offset_x + i*self.cell_size, self.board_offset_y + self.board_size), 1)
            
            # Horizontal lines
            pygame.draw.line(screen, BLACK, 
                            (self.board_offset_x, self.board_offset_y + i*self.cell_size), 
                            (self.board_offset_x + self.board_size, self.board_offset_y + i*self.cell_size), 1)
        
        # Draw the outer border
        pygame.draw.rect(screen, BLACK, 
                         (self.board_offset_x, self.board_offset_y, 
                          self.board_size, self.board_size), 3)

# Player class
class Player:
    def __init__(self, player_id, color):
        self.id = player_id
        self.color = color
        self.tokens = [Token(player_id, i, color) for i in range(4)]
        self.finished = False
    
    def has_won(self):
        return all(token.has_finished for token in self.tokens)
    
    def can_move_any_token(self, dice_value):
        return any(token.can_move(dice_value) for token in self.tokens)
    
    def get_movable_tokens(self, dice_value):
        return [token for token in self.tokens if token.can_move(dice_value)]

# Token class
class Token:
    def __init__(self, player_id, token_id, color):
        self.player_id = player_id
        self.token_id = token_id
        self.color = color
        self.position = -1  # -1 means in home
        self.has_finished = False
    
    def can_move(self, dice_value):
        # If token is in home, need a 6 to move out
        if self.position == -1:
            return dice_value == 6
        
        # If token has finished, it can't move
        if self.has_finished:
            return False
        
        # Otherwise, it can move
        return True
    
    def move(self, dice_value, board):
        # If token is in home and dice is 6, move to start position
        if self.position == -1 and dice_value == 6:
            self.position = 0
            return True
        
        # If token is already on board, move it forward
        if self.position >= 0 and not self.has_finished:
            new_position = self.position + dice_value
            
            # Check if token has reached the end
            if new_position >= len(board.paths[self.player_id]):
                # Check if it can enter the final area
                overflow = new_position - len(board.paths[self.player_id])
                if overflow < 4:  # Can enter final area
                    self.position = new_position
                    self.has_finished = True
                    return True
                else:
                    # Can't move (would overshoot)
                    return False
            
            # Regular move
            self.position = new_position
            return True
        
        return False
    
    def draw(self, screen, board):
        if self.position == -1:  # In home
            x, y = board.home_positions[self.player_id][self.token_id]
            x += board.board_offset_x
            y += board.board_offset_y
            pygame.draw.circle(screen, self.color, (x, y), PLAYER_SIZE//2)
            pygame.draw.circle(screen, BLACK, (x, y), PLAYER_SIZE//2, 2)
        elif self.has_finished:  # In final position
            x, y = board.final_positions[self.player_id][self.token_id]
            x += board.board_offset_x
            y += board.board_offset_y
            pygame.draw.circle(screen, self.color, (x, y), PLAYER_SIZE//2)
            pygame.draw.circle(screen, BLACK, (x, y), PLAYER_SIZE//2, 2)
        else:  # On the path
            x, y = board.paths[self.player_id][self.position]
            x += board.board_offset_x
            y += board.board_offset_y
            pygame.draw.circle(screen, self.color, (x, y), PLAYER_SIZE//2)
            pygame.draw.circle(screen, BLACK, (x, y), PLAYER_SIZE//2, 2)

# Game class
class LudoGame:
    def __init__(self, screen, num_players=4):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.num_players = num_players
        self.board = LudoBoard(self.screen_width, self.screen_height)
        self.players = [Player(i, PLAYER_COLORS[i]) for i in range(num_players)]
        self.current_player = 0
        self.dice_value = 1
        self.dice_images = load_images()
        self.dice_rolled = False
        self.game_over = False
        self.winner = None
        
        # UI elements
        self.dice_rect = pygame.Rect(self.screen_width - 150, 100, DICE_SIZE, DICE_SIZE)
        self.roll_button = pygame.Rect(self.screen_width - 150, 220, 100, 40)
        self.font = pygame.font.SysFont('Arial', 20)
    
    def update_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.board = LudoBoard(width, height)
        self.dice_rect = pygame.Rect(width - 150, 100, DICE_SIZE, DICE_SIZE)
        self.roll_button = pygame.Rect(width - 150, 220, 100, 40)
    
    def roll_dice(self):
        self.dice_value = random.randint(1, 6)
        self.dice_rolled = True
        
        # Check if current player can move any token
        if not self.players[self.current_player].can_move_any_token(self.dice_value):
            # If player can't move, wait for a moment and then move to next player
            pygame.time.delay(1000)
            self.next_player()
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % self.num_players
        self.dice_rolled = False
    
    def handle_click(self, pos):
        # Check if roll button was clicked
        if self.roll_button.collidepoint(pos) and not self.dice_rolled:
            self.roll_dice()
            return
        
        # If dice has been rolled, check if a token was clicked
        if self.dice_rolled:
            movable_tokens = self.players[self.current_player].get_movable_tokens(self.dice_value)
            
            for token in movable_tokens:
                # Get token position
                if token.position == -1:  # In home
                    x, y = self.board.home_positions[token.player_id][token.token_id]
                elif token.has_finished:  # In final position
                    x, y = self.board.final_positions[token.player_id][token.token_id]
                else:  # On the path
                    x, y = self.board.paths[token.player_id][token.position]
                
                x += self.board.board_offset_x
                y += self.board.board_offset_y
                
                # Check if token was clicked
                distance = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5
                if distance <= PLAYER_SIZE:
                    # Move token
                    token.move(self.dice_value, self.board)
                    
                    # Check if player has won
                    if self.players[self.current_player].has_won():
                        self.game_over = True
                        self.winner = self.current_player
                    
                    # If dice value is 6, player gets another turn
                    if self.dice_value != 6:
                        self.next_player()
                    else:
                        self.dice_rolled = False
                    
                    return
    
    def draw(self):
        # Fill the background
        self.screen.fill(GREY)
        
        # Draw the board
        self.board.draw(self.screen)
        
        # Draw all tokens
        for player in self.players:
            for token in player.tokens:
                token.draw(self.screen, self.board)
        
        # Draw the dice
        self.screen.blit(self.dice_images[self.dice_value - 1], self.dice_rect)
        
        # Draw the roll button
        pygame.draw.rect(self.screen, WHITE, self.roll_button)
        pygame.draw.rect(self.screen, BLACK, self.roll_button, 2)
        roll_text = self.font.render('Roll Dice', True, BLACK)
        self.screen.blit(roll_text, (self.roll_button.x + 10, self.roll_button.y + 10))
        
        # Draw current player indicator
        player_text = self.font.render(f'Player {self.current_player + 1}\'s turn', True, PLAYER_COLORS[self.current_player])
        self.screen.blit(player_text, (self.screen_width - 150, 50))
        
        # Draw game over message if game is over
        if self.game_over:
            game_over_text = self.font.render(f'Player {self.winner + 1} wins!', True, PLAYER_COLORS[self.winner])
            self.screen.blit(game_over_text, (self.screen_width - 150, 300))
            
            restart_text = self.font.render('Press R to restart', True, BLACK)
            self.screen.blit(restart_text, (self.screen_width - 150, 330))

# Player selection screen
class PlayerSelection:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font_large = pygame.font.SysFont('Arial', 36)
        self.font = pygame.font.SysFont('Arial', 24)
        self.selected_players = 4
        
        # Create buttons for player selection
        button_width = 200
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        
        self.player_buttons = []
        for i in range(2, 5):  # 2-4 players
            button_y = 200 + (i-2) * 70
            self.player_buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))
        
        # Start button
        self.start_button = pygame.Rect(button_x, 400, button_width, button_height)
    
    def update_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        
        # Update button positions
        button_width = 200
        button_height = 50
        button_x = (width - button_width) // 2
        
        self.player_buttons = []
        for i in range(2, 5):  # 2-4 players
            button_y = 200 + (i-2) * 70
            self.player_buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))
        
        # Update start button
        self.start_button = pygame.Rect(button_x, 400, button_width, button_height)
    
    def handle_click(self, pos):
        # Check if player selection buttons were clicked
        for i, button in enumerate(self.player_buttons):
            if button.collidepoint(pos):
                self.selected_players = i + 2  # 2-4 players
                return False
        
        # Check if start button was clicked
        if self.start_button.collidepoint(pos):
            return True
        
        return False
    
    def draw(self):
        # Fill the background
        self.screen.fill(GREY)
        
        # Draw title
        title_text = self.font_large.render('Ludo Game', True, BLACK)
        self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) // 2, 50))
        
        # Draw player selection text
        select_text = self.font.render('Select number of players:', True, BLACK)
        self.screen.blit(select_text, ((self.screen_width - select_text.get_width()) // 2, 150))
        
        # Draw player selection buttons
        for i, button in enumerate(self.player_buttons):
            num_players = i + 2
            color = WHITE
            if num_players == self.selected_players:
                color = (200, 255, 200)  # Light green for selected
            
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, BLACK, button, 2)
            
            button_text = self.font.render(f'{num_players} Players', True, BLACK)
            self.screen.blit(button_text, (button.x + (button.width - button_text.get_width()) // 2, 
                                          button.y + (button.height - button_text.get_height()) // 2))
        
        # Draw start button
        pygame.draw.rect(self.screen, (200, 200, 255), self.start_button)  # Light blue
        pygame.draw.rect(self.screen, BLACK, self.start_button, 2)
        
        start_text = self.font.render('Start Game', True, BLACK)
        self.screen.blit(start_text, (self.start_button.x + (self.start_button.width - start_text.get_width()) // 2, 
                                     self.start_button.y + (self.start_button.height - start_text.get_height()) // 2))

# Main game loop
def main():
    # Initialize pygame
    pygame.init()
    
    # Create the screen with resizable flag
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
    pygame.display.set_caption('Ludo Game')
    
    clock = pygame.time.Clock()
    
    # Start with player selection screen
    player_selection = PlayerSelection(screen)
    game = None
    in_selection = True
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                # Handle window resize
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                if in_selection:
                    player_selection.update_screen_size(event.w, event.h)
                else:
                    game.update_screen_size(event.w, event.h)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if in_selection:
                        # Handle clicks on player selection screen
                        if player_selection.handle_click(event.pos):
                            # Start button clicked, create game with selected number of players
                            game = LudoGame(screen, player_selection.selected_players)
                            in_selection = False
                    else:
                        # Handle clicks in the game
                        game.handle_click(event.pos)
            elif event.type == KEYDOWN:
                if not in_selection and event.key == K_r and game.game_over:
                    # Restart the game
                    game = LudoGame(screen, game.num_players)
        
        # Draw the current screen
        if in_selection:
            player_selection.draw()
        else:
            game.draw()
        
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
