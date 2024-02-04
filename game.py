import pygame
import sys

from game_board import GameBoard
from draw_functions import draw_text

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship Game")
clock = pygame.time.Clock()


def main_menu():

    screen.blit(pygame.transform.scale(pygame.image.load("menu_bg.jpg"), (WIDTH, HEIGHT)), (0, 0))

    draw_text(screen, "Battleship Game", None, 120, (101, 88, 130), WIDTH // 2, HEIGHT // 4)
    start_text_rect = draw_text(screen, "Start", None, 70, (101, 88, 130), WIDTH // 2, HEIGHT // 3 + 100)
    quit_text_rect = draw_text(screen, "Quit", None, 70, (101, 88, 130), WIDTH // 2, HEIGHT // 3 + 200)

    while True:

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_text_rect.collidepoint(pygame.mouse.get_pos()):
                    place_ships_screen()
                elif quit_text_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


def place_ships_screen():

    ships_placed = False

    # game background
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.blit(pygame.transform.scale(pygame.image.load("game_bg.jpg"), (WIDTH, HEIGHT)), (0, 0))

    # upper text background
    brown_rect = pygame.Rect(560, 0, 800, 140)
    pygame.draw.rect(background_surface, (82, 53, 38), brown_rect)

    # back to main menu
    left_bottom_circle = pygame.draw.circle(background_surface, (82, 53, 38), (20, HEIGHT - 20), 120)
    home_icon = pygame.transform.scale(pygame.image.load("home-icon.png"), (60, 60))
    home_icon_rect = home_icon.get_rect(center=(50, HEIGHT - 50))
    background_surface.blit(home_icon, home_icon_rect)

    # accept positions
    right_bottom_circle = pygame.draw.circle(background_surface, (82, 53, 38), (WIDTH - 20, HEIGHT - 20), 120)
    check_icon = pygame.transform.scale(pygame.image.load("check-icon.png"), (60, 60))
    check_icon_rect = check_icon.get_rect(center=(WIDTH - 50, HEIGHT - 50))
    background_surface.blit(check_icon, check_icon_rect)

    # create game board
    player_board = GameBoard(80, 560, 250)
    player_board.draw_board(screen)

    while True:

        screen.blit(background_surface, (0, 0))

        draw_text(screen, "Prepare for battle", None, 70, (255, 255, 255), WIDTH // 2, 20)
        player_board.draw_board(screen)
        player_board.asign_axes(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_bottom_circle.collidepoint(pygame.mouse.get_pos()):
                    main_menu()
                elif right_bottom_circle.collidepoint(pygame.mouse.get_pos()) and ships_placed:
                    pass

        while not ships_placed:
            ships_placed = player_board.place_ships(screen, background_surface)

        pygame.display.flip()


main_menu()
