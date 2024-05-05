import numpy as np #pip install numpy
import pygame #pip install pygame
import sys #pip install sys
import math #pip install math

#Variáveis para definir tamanho do jogo:
linha = 6
coluna = 7
tamanhoTela = 100
larguraTela = coluna * tamanhoTela
alturaTela = (linha + 1) * tamanhoTela
tamanho = (larguraTela, alturaTela)
circulos = int(tamanhoTela / 2 - 5)

#Variáveis Cores:
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def soltar_peca(tabuleiro, linha, coluna, peca):
    tabuleiro[linha][coluna] = peca

def coluna_valida(tabuleiro, coluna):
    return tabuleiro[linha - 1][coluna] == 0

def proxima_linha_livre(tabuleiro, coluna):
    for r in range(linha):
        if tabuleiro[r][coluna] == 0:
            return r

def desenhar_tabuleiro(tabuleiro):
    for c in range(coluna):
        for r in range(linha):
            pygame.draw.rect(screen, BLUE, (c * tamanhoTela, r * tamanhoTela + tamanhoTela, tamanhoTela, tamanhoTela))
            pygame.draw.circle(screen, WHITE, (
            int(c * tamanhoTela + tamanhoTela / 2), int(r * tamanhoTela + tamanhoTela + tamanhoTela / 2)), circulos)

    for c in range(coluna):
        for r in range(linha):
            if tabuleiro[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * tamanhoTela + tamanhoTela / 2), alturaTela - int(r * tamanhoTela + tamanhoTela / 2)), circulos)
            elif tabuleiro[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * tamanhoTela + tamanhoTela / 2), alturaTela - int(r * tamanhoTela + tamanhoTela / 2)), circulos)
    pygame.display.update()

def desenhar_mensagem(texto):
    myfont = pygame.font.Font(None, 36)
    text = myfont.render(texto, True, (255, 255, 255))  # Branco
    screen.blit(text,(0, 0))
    pygame.display.update()

def verifica_vitoria(tabuleiro):
    for r in range(linha):
        for c in range(coluna):
            #Verifica horizontalmente:
            if c <= coluna - 4:
                if tabuleiro[r][c] == tabuleiro[r][c+1] == tabuleiro[r][c+2] == tabuleiro[r][c+3] != 0:
                    desenhar_mensagem(f"Player {tabuleiro[r][c]} ganhou")
                    return True
            #Verifica verticalmente:
            if r <= linha - 4:
                if tabuleiro[r][c] == tabuleiro[r+1][c] == tabuleiro[r+2][c] == tabuleiro[r+3][c] != 0:
                    desenhar_mensagem(f"Player {tabuleiro[r][c]} ganhou")
                    return True
            #Verifica diagonalmente (direita):
            if c <= coluna - 4 and r <= linha - 4:
                if tabuleiro[r][c] == tabuleiro[r+1][c+1] == tabuleiro[r+2][c+2] == tabuleiro[r+3][c+3] != 0:
                    desenhar_mensagem(f"Player {tabuleiro[r][c]} ganhou")
                    return True
            #Verifica diagonalmente (esquerda):
            if c >= 3 and r <= linha - 4:
                if tabuleiro[r][c] == tabuleiro[r+1][c-1] == tabuleiro[r+2][c-2] == tabuleiro[r+3][c-3] != 0:
                    desenhar_mensagem(f"Player {tabuleiro[r][c]} ganhou")
                    return True
    return False

tabuleiro = np.zeros((linha, coluna))
game_over = False
turn = 0
pygame.init()
screen = pygame.display.set_mode(tamanho)
desenhar_tabuleiro(tabuleiro)

#Parte onde ocorre o local que o jogador vai colocar as peças:
while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx / tamanhoTela))

            if coluna_valida(tabuleiro, col):
                lin = proxima_linha_livre(tabuleiro, col)
                if turn == 0:
                    soltar_peca(tabuleiro, lin, col, 1)
                    if(verifica_vitoria(tabuleiro)):
                        game_over = True
                else:
                    soltar_peca(tabuleiro, lin, col, 2)
                    if (verifica_vitoria(tabuleiro)):
                        game_over = True

                desenhar_tabuleiro(tabuleiro)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
