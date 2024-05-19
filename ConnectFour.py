# Equipe 7 - André Felipe, Jean Carlos, Nicole Fernanda e Thais Jandre
# BUSCA COMPETITIVA
import numpy as np
import pygame
import sys
import math

# Variáveis para definir tamanho do jogo:
linha = 6
coluna = 7
tamanhoTela = 100
larguraTela = coluna * tamanhoTela
alturaTela = (linha + 1) * tamanhoTela
tamanho = (larguraTela, alturaTela)
circulos = int(tamanhoTela / 2 - 5)

# Cores:
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
            if tabuleiro[r][c] == 1:  # COMPUTADOR
                pygame.draw.circle(screen, RED, (
                    int(c * tamanhoTela + tamanhoTela / 2), alturaTela - int(r * tamanhoTela + tamanhoTela / 2)),
                                   circulos)
            elif tabuleiro[r][c] == 2:  # HUMANO
                pygame.draw.circle(screen, YELLOW, (
                    int(c * tamanhoTela + tamanhoTela / 2), alturaTela - int(r * tamanhoTela + tamanhoTela / 2)),
                                   circulos)
    pygame.display.update()


def desenhar_mensagem(texto):
    myfont = pygame.font.Font(None, 36)
    text = myfont.render(texto, True, (255, 255, 255))  # Branco
    screen.blit(text, (0, 0))
    pygame.display.update()


def verifica_vitoria(tabuleiro):
    for r in range(linha):
        for c in range(coluna):
            if tabuleiro[r][c] != 0:
                # Verificar horizontalmente
                if (c <= coluna - 4) and (
                        tabuleiro[r][c] == tabuleiro[r][c + 1] == tabuleiro[r][c + 2] == tabuleiro[r][c + 3]):
                    return tabuleiro[r][c]
                # Verificar verticalmente
                if (r <= linha - 4) and (
                        tabuleiro[r][c] == tabuleiro[r + 1][c] == tabuleiro[r + 2][c] == tabuleiro[r + 3][c]):
                    return tabuleiro[r][c]
                # Verificar diagonalmente (direita)
                if (c <= coluna - 4) and (r <= linha - 4) and (
                        tabuleiro[r][c] == tabuleiro[r + 1][c + 1] == tabuleiro[r + 2][c + 2] == tabuleiro[r + 3][
                    c + 3]):
                    return tabuleiro[r][c]
                # Verificar diagonalmente (esquerda)
                if (c >= 3) and (r <= linha - 4) and (
                        tabuleiro[r][c] == tabuleiro[r + 1][c - 1] == tabuleiro[r + 2][c - 2] == tabuleiro[r + 3][
                    c - 3]):
                    return tabuleiro[r][c]

    for r in range(linha):
        for c in range(coluna):
            if tabuleiro[r][c] == 0:
                return 0

    return -2  # Se nao tiver mais nenhum espaço como 0, e ninguém ganhou, houve empate


def avaliar(tabuleiro):
    if verifica_vitoria(tabuleiro) == 1:
        return 1  # Vitória do computador
    elif verifica_vitoria(tabuleiro) == 2:
        return -1  # Vitória do humano
    else:
        return 0


def minimax(tabuleiro, profundidade, maximo):
    resultado = avaliar(tabuleiro)

    # Verifica se o jogo acabou ou se abri o suficiente as possibilidades
    if resultado != 0 or profundidade == 0:
        return resultado

    if maximo == True:
        melhor_pontuacao = -math.inf  # Menor inteiro
        for col in range(coluna):
            if coluna_valida(tabuleiro, col):
                lin = proxima_linha_livre(tabuleiro, col)
                tabuleiro[lin][col] = 1  # Simulo a jogada do computador naquela coluna
                pontuacao = minimax(tabuleiro, profundidade - 1, False)
                tabuleiro[lin][col] = 0  # Retorno para a situação original
                melhor_pontuacao = max(melhor_pontuacao, pontuacao)
        return melhor_pontuacao
    else:
        melhor_pontuacao = math.inf  # Maior inteiro
        for col in range(coluna):
            if coluna_valida(tabuleiro, col):
                lin = proxima_linha_livre(tabuleiro, col)
                tabuleiro[lin][col] = 2
                pontuacao = minimax(tabuleiro, profundidade - 1, True)
                tabuleiro[lin][col] = 0
                melhor_pontuacao = min(melhor_pontuacao, pontuacao)
        return melhor_pontuacao


def melhor_jogada(tabuleiro):
    melhor_pontuacao = -math.inf  # Menor inteiro
    melhor_coluna = None

    for col in range(coluna):
        if coluna_valida(tabuleiro, col):
            lin = proxima_linha_livre(tabuleiro, col)
            tabuleiro[lin][col] = 1
            pontuacao = minimax(tabuleiro, 3, False)
            tabuleiro[lin][col] = 0
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_coluna = col

    return melhor_coluna


screen = pygame.display.set_mode(tamanho)


def main():
    tabuleiro = np.zeros((linha, coluna))  # O jogo inicia com todas as posições zeradas
    game_over = False
    maximo = False  # O jogo inicia como sendo a vez do usuário
    pygame.init()
    desenhar_tabuleiro(tabuleiro)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / tamanhoTela))

                if coluna_valida(tabuleiro, col):

                    lin = proxima_linha_livre(tabuleiro, col)
                    soltar_peca(tabuleiro, lin, col, 2)  # Coloca a peça
                    desenhar_tabuleiro(tabuleiro)

                    if verifica_vitoria(tabuleiro) != 0:  # Verifica se o jogo acabou
                        if verifica_vitoria(tabuleiro) == 1:
                            desenhar_mensagem(f"Que pena, você perdeu!")
                        else:
                            desenhar_mensagem(f"Parabéns! Você ganhou!")
                        game_over = True

                    maximo = True;  # Passa a vez do jogo para o computador

                    if maximo == True:  # Sendo a vez do computador
                        col = melhor_jogada(tabuleiro)  # Procura a coluna a ser escolhida na função de melhor jogada
                        lin = proxima_linha_livre(tabuleiro, col)  # Verifica a linha livre naquela coluna
                        soltar_peca(tabuleiro, lin, col, 1)  # Coloca a peça

                        if verifica_vitoria(tabuleiro) != 0:  # Verifica se o jogo acabou
                            if verifica_vitoria(tabuleiro) == 1:
                                desenhar_mensagem(f"Que pena, você perdeu!")
                            elif verifica_vitoria(tabuleiro) == 2:
                                desenhar_mensagem(f"Parabéns! Você ganhou!")
                            else:
                                desenhar_mensagem(f"O jogo empatou.")
                            game_over = True

                        maximo = False;  # Passa a vez para o humano
                    desenhar_tabuleiro(tabuleiro)

                    if game_over == True:
                        pygame.time.wait(5000)


# Chamada de execução para o jogo
main()
