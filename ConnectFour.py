import numpy as np
import pygame
import sys
import math

# Constantes
ROW_COUNT = 6
COLUMN_COUNT = 6
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

# Cores
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def criar_tabuleiro():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def soltar_peca(tabuleiro, linha, coluna, peca):
    tabuleiro[linha][coluna] = peca


def coluna_valida(tabuleiro, coluna):
    return tabuleiro[ROW_COUNT - 1][coluna] == 0


def proxima_linha_livre(tabuleiro, coluna):
    for r in range(ROW_COUNT):
        if tabuleiro[r][coluna] == 0:
            return r


def desenhar_tabuleiro(tabuleiro):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if tabuleiro[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif tabuleiro[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def desenhar_mensagem(texto):
    myfont = pygame.font.Font(None, 36)
    text = myfont.render(texto, True, (255, 255, 255))  # Branco
    screen.blit(text,(0, 0))  # Ajuste a posição conforme necessário
    pygame.display.update()


tabuleiro = criar_tabuleiro()
game_over = False
turn = 0

pygame.init()
screen = pygame.display.set_mode(size)
desenhar_tabuleiro(tabuleiro)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


def verifica_vitoria(tabuleiro):
    # Verifica vitória nas linhas
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if tabuleiro[r][c] == 1 and tabuleiro[r][c+1] == 1 and tabuleiro[r][c+2] == 1 and tabuleiro[r][c+3] == 1:
                desenhar_mensagem("Player 1 ganhou - VERMELHO")
                return True
            elif tabuleiro[r][c] == 2 and tabuleiro[r][c+1] == 2 and tabuleiro[r][c+2] == 2 and tabuleiro[r][c+3] == 2:
                desenhar_mensagem("Player 2 ganhou - AMARELO")
                return True

    # Verifica vitória nas colunas
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if tabuleiro[r][c] == 1 and tabuleiro[r+1][c] == 1 and tabuleiro[r+2][c] == 1 and tabuleiro[r+3][c] == 1:
                desenhar_mensagem("Player 1 ganhou - VERMELHO")
                return True
            elif tabuleiro[r][c] == 2 and tabuleiro[r+1][c] == 2 and tabuleiro[r+2][c] == 2 and tabuleiro[r+3][c] == 2:
                desenhar_mensagem("Player 2 ganhou - AMARELO")
                return True

    # Verifica vitória nas diagonais \
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if tabuleiro[r][c] == 1 and tabuleiro[r+1][c+1] == 1 and tabuleiro[r+2][c+2] == 1 and tabuleiro[r+3][c+3] == 1:
                desenhar_mensagem("Player 1 ganhou - VERMELHO")
                return True
            elif tabuleiro[r][c] == 2 and tabuleiro[r+1][c+1] == 2 and tabuleiro[r+2][c+2] == 2 and tabuleiro[r+3][c+3] == 2:
                desenhar_mensagem("Player 2 ganhou - AMARELO")
                return True

    # Verifica vitória nas diagonais /
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            if tabuleiro[r][c] == 1 and tabuleiro[r+1][c-1] == 1 and tabuleiro[r+2][c-2] == 1 and tabuleiro[r+3][c-3] == 1 and tabuleiro[r+3][c-3] == 1:
                desenhar_mensagem("Player 1 ganhou - VERMELHO")
                return True
            elif tabuleiro[r][c] == 2 and tabuleiro[r+1][c-1] == 2 and tabuleiro[r+2][c-2] == 2 and tabuleiro[r+3][c-3] == 2:
                desenhar_mensagem("Player 2 ganhou - AMARELO")
                return True

    return False


while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Pega a entrada do jogador
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if coluna_valida(tabuleiro, col):
                linha = proxima_linha_livre(tabuleiro, col)
                if turn == 0:
                    soltar_peca(tabuleiro, linha, col, 1)
                    if(verifica_vitoria(tabuleiro)):
                        game_over = True

                else:
                    soltar_peca(tabuleiro, linha, col, 2)
                    if (verifica_vitoria(tabuleiro)):
                        game_over = True

                desenhar_tabuleiro(tabuleiro)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
