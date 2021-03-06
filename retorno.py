"""
Módulo para tratar se há ou não peça(s) para retornar, verificando
a condição e realizando o retorno, caso esse seja válido. Em caso
de sobrar ainda um dado para ser usado em movimento, será sinali-
zado e a jogada será executada conforme o dado que sobrou dentro
do módulo jogadas.py

Funções:
    * dado_valido(d1, d2):
        Recebe os valores dos dados e retorna se os dados são 
        válidos e para quais condições (casa vazia, captura ou
        casa com peças do jogador)
    
    * peca_retorno(casa_cond, dado, pc_cap_cl, pc_cap_es):
        Recebe o tipo de condição de retorno, o valor do dado e,
        se há peça para capturar, sua posição. Realiza a permuta
    
    * peca_capturada(d1, d2):
        Recebe os valores dos dados e determina se há peças capturadas
        para que elas possam ser retornadas
"""

# Função escrita para o programa
from def_cores import *
import tabuleiro

###############################################
def dado_valido(d1, d2, jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA):
    """Verificação de quais dados são válidos para retornar a peça ao tabuleiro, conforme
       três possíveis condições de retorno: casa vazia, captura do oponente e casa com
       peças do jogador"""
    d1_val = False
    d2_val = False
    casa_d1_cond = 0
    casa_d2_cond = 0
    for cont in range(6):
        # Jogador 1 e Condição 1: Dado válido para retorno se a casa for vazia
        if jog_1 and pecas_posi[cont][0] == PC_NULA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 1
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 1
        # Jogador 2 e Condição 1:: Dado válido para retorno se a casa for vazia
        elif jog_2 and pecas_posi[23-cont][0] == PC_NULA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 1
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 1
        # Jogador 1 e Condição 2: Dado válido para retorno se a casa somente tiver uma
        # peça adversária, a qual será capturada
        elif jog_1 and pecas_posi[cont][0] == PC_ESCURA and pecas_posi[cont][1] == PC_NULA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 2
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 2
        # Jogador 2 e Condição 2: Dado válido para retorno se a casa somente tiver uma
        # peça adversária, a qual será capturada
        elif jog_2 and pecas_posi[23-cont][0] == PC_CLARA and pecas_posi[23-cont][1] == PC_NULA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 2
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 2
        # Jogador 1 e Condição 3: Dado válido para retorno em uma casa que contém peças suas (brancas)
        elif jog_1 and pecas_posi[cont][0] == PC_CLARA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 3
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 3
        # Jogador 2 e Condição 3: Dado válido para retorno em uma casa que contém peças suas (pretas)
        elif jog_2 and pecas_posi[23-cont][0] == PC_ESCURA:
            if d1 == (cont+1):
                d1_val = True
                casa_d1_cond = 3
            if d2 == (cont+1):
                d2_val = True
                casa_d2_cond = 3
    return d1_val, d2_val, casa_d1_cond, casa_d2_cond

###############################################
def peca_retorno(casa_cond, dado, pc_cap_cl, pc_cap_es, jog_1, pecas_posi, pecas_capturadas_claras, pecas_capturadas_escuras, PC_CLARA, PC_ESCURA):
    """Função para permutar a peça que será retornada ao tabuleiro, conforme a condição possível"""
    pecas_casa = 0
    # Se jogador 1
    if jog_1:
        # Dado válido para retorno se a casa for vazia
        if casa_cond == 1:
            pecas_posi[dado-1][0], pecas_capturadas_claras[pc_cap_cl-1] = pecas_capturadas_claras[pc_cap_cl-1], pecas_posi[dado-1][0]
        # Dado válido para retorno se a casa somente tiver uma peça adversária,
        # a qual será capturada
        elif casa_cond == 2:
            pecas_posi[dado-1][0], pecas_capturadas_escuras[pc_cap_es] = pecas_capturadas_escuras[pc_cap_es], pecas_posi[dado-1][0]
            pecas_posi[dado-1][0], pecas_capturadas_claras[pc_cap_cl-1] = pecas_capturadas_claras[pc_cap_cl-1], pecas_posi[dado-1][0]
        # Dado válido para retorno em uma casa que contém peças suas (brancas)
        elif casa_cond == 3:
            for cont in range(len(pecas_posi[dado-1])):
                if pecas_posi[dado-1][cont] == PC_CLARA:
                    pecas_casa += 1
            pecas_posi[dado-1][pecas_casa], pecas_capturadas_claras[pc_cap_cl-1] = pecas_capturadas_claras[pc_cap_cl-1], pecas_posi[dado-1][pecas_casa]
        return
    # Jogador 2
    else:
        # Dado válido para retorno se a casa for vazia
        if casa_cond == 1:
            pecas_posi[24-dado][0], pecas_capturadas_escuras[pc_cap_es-1] = pecas_capturadas_escuras[pc_cap_es-1], pecas_posi[24-dado][0]
        # Dado válido para retorno se a casa somente tiver uma peça adversária,
        # a qual será capturada
        elif casa_cond == 2:
            pecas_posi[24-dado][0], pecas_capturadas_claras[pc_cap_cl] = pecas_capturadas_claras[pc_cap_cl], pecas_posi[24-dado][0]
            pecas_posi[24-dado][0], pecas_capturadas_escuras[pc_cap_es-1] = pecas_capturadas_escuras[pc_cap_es-1], pecas_posi[24-dado][0]
        # Dado válido para retorno em uma casa que contém peças suas (brancas)
        elif casa_cond == 3:
            for cont in range(len(pecas_posi[dado-1])):
                if pecas_posi[24-dado][cont] == PC_ESCURA:
                    pecas_casa += 1
            pecas_posi[24-dado][pecas_casa], pecas_capturadas_escuras[pc_cap_es-1] = pecas_capturadas_escuras[pc_cap_es-1], pecas_posi[24-dado][pecas_casa]
        return

###############################################
def peca_capturada(d1, d2, dado_usado, jog_1, jog_2, cont_jogadas, pecas_posi, pecas_capturadas_claras, pecas_capturadas_escuras, pecas_retiradas_escuras, pecas_retiradas_claras, PC_CLARA, PC_ESCURA, PC_NULA, CS_CLARA, CS_ESCURA, CS_MEIO):
    """Função para determinar se há peças capturadas dos jogadores e quais valores valores de dados usará para
       o retorno da peça ao tabuleiro"""

    pecas_capturadas = [0, 0]
    dado_val = [False, False]
    casa_dx_cond = [0, 0]

    for cont in range(5):
        if pecas_capturadas_claras[cont] == PC_CLARA:
            pecas_capturadas[0] += 1
        if pecas_capturadas_escuras[cont] == PC_ESCURA:
            pecas_capturadas[1] += 1

    # Jogador 1
    if jog_1:
        # Teste das condições 
        if pecas_capturadas[0] == 0:
            return True
        else:
            dado_val[0], dado_val[1], casa_dx_cond[0], casa_dx_cond[1] = dado_valido(d1, d2, jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
            # Condições de retorno conforme a validade dos dados:
            # 1 - Ambos os dados podem ser usados e o usuário irá escolher qual
            if dado_usado == 0 and dado_val[0] and dado_val[1]:
                while True:
                    try:
                        print(COR_SUBLINHADO + "O valor ou de D1 ou de D2 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL)
                        dado_x = int(input("Escolha qual dado você deseja usar (1 ou 2): "))
                        if dado_x < 1 or dado_x > 2:
                            raise ValueError
                        else:
                            print()
                            break
                    except ValueError:
                        print("\n" + COR_FUNDO_VERMELHO + "Valor inválido." + COR_RESETALL + " Repita a operação.\n")
                # Escolheu D1
                if dado_x == 1:
                    peca_retorno(casa_dx_cond[0], d1, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                    dado_usado = 1
                # Escolheu D2
                else:
                    peca_retorno(casa_dx_cond[1], d2, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                    dado_usado = 2
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[0] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    peca_capturada(d1, d2, dado_usado, jog_1, jog_2, cont_jogadas, pecas_posi, pecas_capturadas_claras, pecas_capturadas_escuras, pecas_retiradas_escuras, pecas_retiradas_claras, PC_CLARA, PC_ESCURA, PC_NULA, CS_CLARA, CS_ESCURA, CS_MEIO)
                    return False
            # 2 - Somente dado 1 está apto a ser usado
            elif dado_usado != 1 and dado_val[0]:
                print(COR_SUBLINHADO + "O valor de D1 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL + "\n" +
                      "Pressione enter para realizar a jogada: ")
                input()
                peca_retorno(casa_dx_cond[0], d1, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                dado_usado = 1
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[0] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    return False
            # 3 - Somente dado 2 está apto a ser usado
            elif dado_usado != 2 and dado_val[1]:
                print(COR_SUBLINHADO + "O valor de D2 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL + "\n" +
                      "Pressione enter para realizar a jogada: ")
                input()
                peca_retorno(casa_dx_cond[1], d2, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                dado_usado = 2
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[0] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    return False
            # 4 - Nenhum dado está apto a ser usado
            else:
                print(COR_SUBLINHADO + "Nenhum valor dos dados permite retornar a peça capturada ao tabuleiro\n" +
                                "Passe a jogada =(" + COR_RESETALL + "\n")
                return False
    # Jogador 2
    else:
        # Teste das condições 
        if pecas_capturadas[1] == 0:
            return True
        else:
            dado_val[0], dado_val[1], casa_dx_cond[0], casa_dx_cond[1] = dado_valido(d1, d2, jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
            # Condições de retorno conforme a validade dos dados:
            # 1 - Ambos os dados podem ser usados e o usuário irá escolher qual
            if dado_usado == 0 and dado_val[0] and dado_val[1]:
                while True:
                    try:
                        print(COR_SUBLINHADO + "O valor ou de D1 ou de D2 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL)
                        dado_x = int(input("Escolha qual dado você deseja usar (1 ou 2): "))
                        if dado_x < 1 or dado_x > 2:
                            raise ValueError
                        else:
                            print()
                            break
                    except ValueError:
                        print("\n" + COR_FUNDO_VERMELHO + "Valor inválido." + COR_RESETALL + " Repita a operação.\n")
                # Escolheu D1
                if dado_x == 1:
                    peca_retorno(casa_dx_cond[0], d1, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                    dado_usado = 1
                # Escolheu D2
                else:
                    peca_retorno(casa_dx_cond[1], d2, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                    dado_usado = 2
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[1] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    peca_capturada(d1, d2, dado_usado, jog_1, jog_2, cont_jogadas, pecas_posi, pecas_capturadas_claras, pecas_capturadas_escuras, pecas_retiradas_escuras, pecas_retiradas_claras, PC_CLARA, PC_ESCURA, PC_NULA, CS_CLARA, CS_ESCURA, CS_MEIO)
                    return False
            # 2 - Somente dado 1 está apto a ser usado
            elif dado_usado != 1 and dado_val[0]:
                print(COR_SUBLINHADO + "O valor de D1 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL + "\n" +
                      "Pressione enter para realizar a jogada: ")
                input()
                peca_retorno(casa_dx_cond[0], d1, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                dado_usado = 1
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[1] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    return False
            # 3 - Somente dado 2 está apto a ser usado
            elif dado_usado != 2 and dado_val[1]:
                print(COR_SUBLINHADO + "O valor de D2 permite retornar a peça capturada ao tabuleiro" + COR_RESETALL + "\n" +
                      "Pressione enter para realizar a jogada: ")
                input()
                peca_retorno(casa_dx_cond[1], d2, pecas_capturadas[0], pecas_capturadas[1], jog_1, jog_2, pecas_posi, PC_NULA, PC_ESCURA, PC_CLARA)
                dado_usado = 2
                tabuleiro.print_tabuleiro(pecas_posi, pecas_retiradas_escuras, pecas_retiradas_claras, pecas_capturadas_escuras, pecas_capturadas_claras, CS_CLARA, CS_ESCURA, CS_MEIO)

                cont_jogadas += 1
                if pecas_capturadas[1] == 1:
                    if cont_jogadas == 2:
                        return False
                    else:
                        return True
                else:
                    return False
            # 4 - Nenhum dado está apto a ser usado
            else:
                print(COR_SUBLINHADO + "Nenhum valor dos dados permite retornar a peça capturada ao tabuleiro\n" +
                                "Passe a jogada =(" + COR_RESETALL + "\n")
                return False