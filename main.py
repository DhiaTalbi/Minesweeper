import pygame
import random


def grid_gen(size=10, mine_count=15):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    all_positions = [(i, j) for i in range(size) for j in range(size)]
    mine_positions = random.sample(all_positions, mine_count)

    for (i, j) in mine_positions:
        grid[i][j] = 1

    return grid         
def mines_count(cell, grid):
    rows = len(grid)
    cols = len(grid[0])
    row, col = cell
    mine_count = 0

    for i in range(max(0, row - 1), min(row + 2, rows)):
        for j in range(max(0, col - 1), min(col + 2, cols)):
            if (i, j) != cell and grid[i][j] == 1:
                mine_count += 1

    return mine_count
def reveal_clear_cells(start, grid):
    rows = len(grid)
    cols = len(grid[0])
    row, col = start
    to_reveal = set()
    queue = [(row, col)]
    visited = set()

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        mine_count = mines_count((r,c), grid)
        if mine_count == 0:
            for i in range(max(0, r - 1), min(r + 2, rows)):
                for j in range(max(0, c - 1), min(c + 2, cols)):
                    if (i, j) != (r, c) and (i, j) not in visited:
                        queue.append((i, j))
        to_reveal.add((r, c))

    return to_reveal 

    grid = grid_gen()
    play_grid = [['#' for _ in range(10)] for _ in range(10)]
    while True :
        print_grid(grid)
        print("\nChoose a cell")
        row = int(input("Enter row: ")) 
        col = int(input("Enter column: ")) 
        cell = (row,col)
        
        if grid[cell[0]][cell[1]] == 1 :
            print("You stepped on a mine !")
        elif grid[cell[0]][cell[1]] == 0:
            for revcell in reveal_clear_cells(cell,grid):
                play_grid[revcell[0]][revcell[1]] = mines_count(revcell,grid)
        print_grid(play_grid)



# Initialize Pygame
pygame.init()

# Set up display
size = 10
cell_size = 70
width, height = size * cell_size, size * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


# Font
font = pygame.font.SysFont(None, 30)

# Load images
flag_img = pygame.image.load('flag.png')
flag_img = pygame.transform.scale(flag_img, (cell_size, cell_size))

mine_img = pygame.image.load('mine.png')
mine_img = pygame.transform.scale(mine_img, (cell_size * 0.75, cell_size * 0.75))

def draw_grid():
    for row in range(size):
        for col in range(size):
            color = WHITE if grid[row][col] == 2 else LIGHT_BLUE
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)
            if grid[row][col] == 2:
                text_surf = font.render(str(mines_count((row,col),grid)), True, BLACK)
                text_rect = text_surf.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                screen.blit(text_surf, text_rect)
            elif grid[row][col] == 3:
                screen.blit(mine_img, (col * cell_size + cell_size /8, row * cell_size + cell_size /8))
            elif (row, col) in flags:
                screen.blit(flag_img, (col * cell_size, row * cell_size))

            

def show_mines():
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 1:
                grid[row][col] = 3


grid = grid_gen(size, 15)
flags = set()

lost = False
won = False
GameOver = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid = grid_gen(size, 15)
                flags = set()
                lost = False
                won = False
                GameOver = False
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // cell_size
            row = mouse_y // cell_size
            if event.button == 1: # Left click
                if grid[row][col] == 1:
                    GameOver = True
                    lost = True
                    
                else:
                    for revcell in reveal_clear_cells((row,col),grid):
                        grid[revcell[0]][revcell[1]] = 2 
            elif event.button == 3:
                if (row,col) in flags:
                    flags.remove((row,col))
                else:
                    flags.add((row,col))
            
            if sum([grid[i].count(2) for i in range(10)]) == 85 :
                GameOver = True
                won = True
                   
    if not GameOver:
        screen.fill(BLACK)
        draw_grid()
        pygame.display.flip()
    else:
        show_mines()
        if lost:
            screen.fill(BLACK)
            draw_grid()
            text_surf = font.render("Game Over!", True, RED)
            text_rect = text_surf.get_rect(center=(width // 2, height // 2))  
            screen.blit(text_surf, text_rect)
            replay_text = font.render("Press R to Play Again", True, BLUE)
            screen.blit(replay_text,replay_text.get_rect(center=(width // 2, height // 2 + 30)))
            pygame.display.flip()
        else:
            screen.fill(BLACK)
            draw_grid()
            won_text = pygame.font.SysFont(None, 100).render("You Won!", True, GREEN)
            screen.blit(won_text, won_text.get_rect(center=(width // 2, height // 2)))
            replay_text = font.render("Press R to Play Again", True, BLUE)
            screen.blit(replay_text,replay_text.get_rect(center=(width // 2, height // 2 + 40)))
            pygame.display.flip()
            

pygame.quit()