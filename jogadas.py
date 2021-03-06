"""
Módulo que trata de tudo relacionado as jogadas de movimento das peças
e suas retiradas

Funções:
    * selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA):

    * contar_pecas_na_casa(casa, jog_1, jog_2, pecas_posi, pc_clara, pc_escura, pc_nula):

    * jogador_pode_retirar_pecas(jog_1, pc_clara, pc_escura, pecas_posi)

    * definir_tipo_de_jogada(casa, dado, jog_1, pc_clara, pc_escura, pc_nula, pecas_posi):

    * peca_movimento(casa, movimento, d1, d2):

    * jogada_dados_diff(opcao, d1, d2):

    * jogada_dados_igual(opcao, d1, d2):

    * jogada_opcoes(d1, d2):
"""

# Função das variáveis globais
from re import T
import var_global
from def_cores import *
import tabuleiro

###############################################
def selecionar_casa(jog_1, jog_2, pecas_posi, pc_clara, pc_escura, pc_nula):
    """Função que verifica se o valor escolhido para a casa da peça a ser movimentada está correto"""
    while True:
            casa = int(input("Selecione a casa correspondente a peça que você deseja mover: "))
            
            if casa == 0 or casa > 24:
                print("\n" + COR_FUNDO_VERMELHO + "Valor inválido:" + COR_RESETALL + " Fora da faixa de 1 até 24. Repita a operação.\n")
            elif pecas_posi[24 - casa][0] == pc_nula:
                print("\n" + COR_FUNDO_VERMELHO + "Jogada inválida:" + COR_RESETALL + " Você selecionou uma casa vazia. Tente novamente\n")
            elif jog_1 and pecas_posi[24 - casa][0] == pc_escura:
                print("\n" + COR_FUNDO_VERMELHO + "Jogada inválida:" + COR_RESETALL + " Você selecionou a casa do adversário. Tente novamente\n")
            elif jog_2 and pecas_posi[24 - casa][0] == pc_clara:
                print("\n" + COR_FUNDO_VERMELHO + "Jogada inválida:" + COR_RESETALL + " Você selecionou a casa do adversário. Tente novamente\n")
            else:
                return casa

###############################################
def contar_pecas_na_casa(casa, jog_1, jog_2, pecas_posi, pc_clara, pc_escura, pc_nula):
    """Função da contagem de peças na casa"""
    #FIXME: Bug na condição "var_global.pecas_posi[casa_posi][cont].isnumeric()"
    #ex.: [o, o, o, o, 2], p/ jogador 2, isso conta 2 peças escuras. Quando na verdade há
    # 6 peças claras do jogador 1.

    quant = 0
    casa_posi = 24 - casa

    for cont in range(5):
        if jog_1 and pecas_posi[casa_posi][cont] == pc_clara:
            quant += 1
        elif jog_2 and pecas_posi[casa_posi][cont] == pc_escura:
            quant += 1
        elif pecas_posi[casa_posi][cont] == pc_nula:
            break
        elif pecas_posi[casa_posi][cont].isnumeric():
            quant += pecas_posi[casa_posi][cont]

    return quant

###############################################
def jogador_pode_retirar_pecas(jog_1, pc_clara, pc_escura, pecas_posi):
    """Teste da condição para retiradas de peças do jogo"""

    peca_alvo = 0
    casa_inicial = 0
    if jog_1:
        peca_alvo = pc_clara
        casa_inicial = 0
    else:
        peca_alvo = pc_escura
        casa_inicial = 18

    contagem_pecas = 0
    for casa in range(6):
        for linha in range(5):
            if pecas_posi[casa_inicial + casa][linha] == peca_alvo:
                contagem_pecas += 1
            elif pecas_posi[casa_inicial + casa][linha].isnumeric():
                contagem_pecas += pecas_posi[casa_inicial + casa][linha]

    return contagem_pecas == 15

###############################################
def definir_tipo_de_jogada(casa, dado, jog_1, pc_clara, pc_escura, pc_nula, pecas_posi):
    """Função para verificar se a movimentação da peça do jogador é válida \n
       Duas ou mais peças do adversário: casa fechada (inválida = 0)\n
       Uma peça do adversário: peça será capturada (válida = 1)\n
       Casa sem peças ou com peças do próprio jogador: casa livre (válida = 1)"""

    movimento = 0
    peca_jogador = -1
    peca_oponente = -1
    if jog_1:
        movimento = 24 - casa + dado
        peca_jogador = pc_clara
        peca_oponente = pc_escura
    else:
        movimento = 24 - casa - dado
        peca_jogador = pc_escura
        peca_oponente = pc_clara

    # Movimento de retirada se casa campo estiver com todas as peças
    if movimento > 23 or movimento < 0:
        if jogador_pode_retirar_pecas(jog_1, pc_clara, pc_escura, pecas_posi):
            return 5
        else:
            print("\nCondição para as retiradas de peças do jogo não atingida. Tente novamente\n")
            return 2
    
    # Movimento válido se casa vazia
    elif pecas_posi[movimento][0] == pc_nula:
        return 1
    
    # Movimento inválido se casa bloqueada
    elif pecas_posi[movimento][1] == peca_oponente:
        print("\n" + COR_FUNDO_VERMELHO + "Jogada inválida:" + COR_RESETALL + " A opção escolhida leva sua peça\n" +
                "para uma casa bloqueada. Tente novamente\n")
        return 2
    
    # Movimento de captura
    elif pecas_posi[movimento][1] == pc_nula and pecas_posi[movimento][0] == peca_oponente:
        print("\nA opção escolhida leva sua peça a capturar a peça do adversário\n")
        return 3
    
    # Movimento válido de sobreposição se peças do jogador
    elif pecas_posi[movimento][0] == peca_jogador:
        return 4

###############################################
def peca_movimento(casa, movimento, dado):
    """Função que irá movimentar a peça conforme a situação"""

    posi_casa = 24-casa
    movimento_clara = 24-casa+dado
    movimento_escura = 24-casa-dado
    quant_ori = contar_pecas_na_casa(casa, var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)

    # Movimento para casa vazia
    if movimento == 1:
        # Jogador 1 e peças na casa de 5 a menos
        if var_global.jog_1 and quant_ori <= 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_clara][0] = var_global.pecas_posi[movimento_clara][0], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 1 e peças na casa mais de 5
        elif var_global.jog_1 and quant_ori > 5:
            var_global.pecas_posi[posi_casa][4] -= 1
            if var_global.pecas_posi[posi_casa][4] == 1:
                var_global.pecas_posi[posi_casa][4], var_global.pecas_extras[posi_casa][0] = var_global.pecas_extras[posi_casa][0], var_global.pecas_posi[posi_casa][4]
                var_global.pecas_posi[posi_casa][4], var_global.pecas_posi[movimento_clara][0] = var_global.pecas_posi[movimento_clara][0], var_global.pecas_posi[posi_casa][4]
            #else:
        # Jogador 2 e peças na casa de 5 a menos
        elif var_global.jog_2 and quant_ori <= 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_escura][0] = var_global.pecas_posi[movimento_escura][0], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 2 e peças na casa mais de 5
        elif var_global.jog_2 and quant_ori > 5:
            var_global.pecas_posi[posi_casa][4] -= 1
            if var_global.pecas_posi[posi_casa][4] == 1:
                var_global.pecas_posi[posi_casa][4], var_global.pecas_extras[posi_casa][0] = var_global.pecas_extras[posi_casa][0], var_global.pecas_posi[posi_casa][4]
                var_global.pecas_posi[posi_casa][4], var_global.pecas_posi[movimento_escura][0] = var_global.pecas_posi[movimento_escura][0], var_global.pecas_posi[posi_casa][4]
            #else:
    
    # Movimento para captura da peça adversária
    elif movimento == 3:
        pecas_capturadas = [0, 0]
        for cont in range(5):
            if var_global.pecas_capturadas_claras[cont] == var_global.PC_CLARA:
                pecas_capturadas[0] += 1
            if var_global.pecas_capturadas_escuras[cont] == var_global.PC_ESCURA:
                pecas_capturadas[1] += 1

        # Jogador 1 e peças na casa de 5 a menos
        if var_global.jog_1 and quant_ori <= 5:
            var_global.pecas_posi[movimento_clara][0], var_global.pecas_capturadas_escuras[pecas_capturadas[1]] = var_global.pecas_capturadas_escuras[pecas_capturadas[1]], var_global.pecas_posi[movimento_clara][0]
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_clara][0] = var_global.pecas_posi[movimento_clara][0], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 1 e peças na casa mais de 5
        elif var_global.jog_1 and quant_ori > 5:
            var_global.pecas_posi[posi_casa][4] -= 1
            if var_global.pecas_posi[posi_casa][4] == 1:
                var_global.pecas_posi[posi_casa][4], var_global.pecas_extras[posi_casa][0] = var_global.pecas_extras[posi_casa][0], var_global.pecas_posi[posi_casa][4]
                var_global.pecas_posi[movimento_clara][0], var_global.pecas_capturadas_escuras[pecas_capturadas[1]] = var_global.pecas_capturadas_escuras[pecas_capturadas[1]], var_global.pecas_posi[movimento_clara][0]
                var_global.pecas_posi[posi_casa][4], var_global.pecas_posi[movimento_clara][0] = var_global.pecas_posi[movimento_clara][0], var_global.pecas_posi[posi_casa][4]
        # Jogador 2 e peças na casa de 5 a menos
        elif var_global.jog_2 and quant_ori <= 5:
            var_global.pecas_posi[movimento_escura][0], var_global.pecas_capturadas_claras[pecas_capturadas[0]] = var_global.pecas_capturadas_claras[pecas_capturadas[0]], var_global.pecas_posi[movimento_escura][0]
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_escura][0] = var_global.pecas_posi[movimento_escura][0], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 2 e peças na casa mais de 5
        elif var_global.jog_2 and quant_ori > 5:
            var_global.pecas_posi[posi_casa][4] -= 1
            if var_global.pecas_posi[posi_casa][4] == 1:
                var_global.pecas_posi[posi_casa][4], var_global.pecas_extras[posi_casa][0] = var_global.pecas_extras[posi_casa][0], var_global.pecas_posi[posi_casa][4]
                var_global.pecas_posi[movimento_escura][0], var_global.pecas_capturadas_claras[pecas_capturadas[0]] = var_global.pecas_capturadas_claras[pecas_capturadas[0]], var_global.pecas_posi[movimento_escura][0]
                var_global.pecas_posi[posi_casa][4], var_global.pecas_posi[movimento_escura][0] = var_global.pecas_posi[movimento_escura][0], var_global.pecas_posi[posi_casa][4]
    
    # Movimento para sobrepor a peça do jogador
    elif movimento == 4:
        if var_global.jog_1:
            quant_des = contar_pecas_na_casa(casa - dado, var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        else:
            quant_des = contar_pecas_na_casa(casa + dado, var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        # Jogador 1 e peças na casa de origem e destino menos de 5
        if var_global.jog_1 and quant_ori < 5 and quant_des < 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_clara][quant_des] = var_global.pecas_posi[movimento_clara][quant_des], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 1 e peças na casa de origem menos de 5 e casa de destino com 5 ou mais peças
        elif var_global.jog_1 and quant_ori < 5 and quant_des >= 5:
            if var_global.pecas_posi[movimento_clara][4] == var_global.PC_CLARA:
                var_global.pecas_sobre_quant[movimento_clara] += 1
        # Jogador 2 e peças na casa de origem e destino menos de 5
        if var_global.jog_2 and quant_ori < 5 and quant_des < 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_posi[movimento_escura][quant_des] = var_global.pecas_posi[movimento_escura][quant_des], var_global.pecas_posi[posi_casa][quant_ori-1]
        # Jogador 2 e peças na casa de origem menos de 5 e casa de destino com 5 ou mais peças
        elif var_global.jog_2 and quant_ori < 5 and quant_des >= 5:
            if var_global.pecas_posi[movimento_escura][4] == var_global.PC_ESCURA:
                var_global.pecas_sobre_quant[movimento_escura] += 1

    # Movimento para retirar a peça do jogador
    elif movimento == 5:
        quant_ret = 0
        if var_global.jog_1:
            for cont in range(15):
                if var_global.pecas_retiradas_claras[cont] == var_global.PC_CLARA:
                    quant_ret += 1
        else:
            for cont in range(15):
                if var_global.pecas_retiradas_escuras[cont] == var_global.PC_ESCURA:
                    quant_ret += 1

        # Jogador 1 e peças na casa de 5 a menos
        if var_global.jog_1 and quant_ori <= 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_retiradas_claras[quant_ret] = var_global.pecas_retiradas_claras[quant_ret], var_global.pecas_posi[posi_casa][quant_ori-1]
            var_global.pecas_retiradas_claras_quant = quant_ret+1
        # Jogador 1 e peças na casa de 5 a menos
        elif var_global.jog_2 and quant_ori <= 5:
            var_global.pecas_posi[posi_casa][quant_ori-1], var_global.pecas_retiradas_escuras[quant_ret] = var_global.pecas_retiradas_escuras[quant_ret], var_global.pecas_posi[posi_casa][quant_ori-1]
            var_global.pecas_retiradas_escuras_quant = quant_ret+1

    return

###############################################
def jogada_dados_diff(opcao, d1, d2):
    """Função que verifica se a peça pode ser deslocada, para dados com valores diferentes,
       conforme seu valor. Se for válida, a peça será deslocada"""
    movimento = [0, 0]
    # Mover uma peça: usando D1 primeiro e depois D2
    if opcao == 1:
        # Validade das duas jogadas
        casa = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            if var_global.jog_1:
                movimento[1] = definir_tipo_de_jogada(casa-d1, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
            else:
                movimento[1] = definir_tipo_de_jogada(casa+d1, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Se um dos dois movimentos for inválido
        if movimento[1] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        # Se não há movimentos inválidos
        else:
            peca_movimento(casa, movimento[0], d1)
            if var_global.jog_1:
                peca_movimento(casa-d1, movimento[1], d2)
            else:
                peca_movimento(casa+d1, movimento[1], d2)
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

            return True

    # Mover uma peça: usando D2 primeiro e depois D1
    elif opcao == 2:
        # Validade das duas jogadas
        casa = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            if var_global.jog_1:
                movimento[1] = definir_tipo_de_jogada(casa-d2, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
            else:
                movimento[1] = definir_tipo_de_jogada(casa+d2, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Se um dos dois movimentos for inválido
        if movimento[1] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        # Se não há movimentos inválidos
        else:
            peca_movimento(casa, movimento[0], d2)
            if var_global.jog_1:
                peca_movimento(casa-d2, movimento[1], d1)
            else:
                peca_movimento(casa+d2, movimento[1], d1)
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

            return True

    # Mover duas peças: a primeira com D1 e a segunda com D2
    elif opcao == 3:
        # Peça 1
        casa_1 = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa_1, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Testa jogada inválida com D1 e retorna à função Opções caso verdade
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            peca_movimento(casa_1, movimento[0], d1)
            var_global.dado_usado = 1
            var_global.cont_jogadas += 1
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        # Testa se a peça é a mesma. Se for, chama exceção
        while True:
            try:
                # Peça 2
                casa_2 = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
                movimento[1] = definir_tipo_de_jogada(casa_2, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[1] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
                elif var_global.jog_1:
                    if (casa_2 + d1) == casa_1:
                        raise ValueError
                elif var_global.jog_2:
                    if (casa_2 - d1) == casa_1:
                        raise ValueError
                peca_movimento(casa_2, movimento[1], d2)
                tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

                return True
            except ValueError:
                print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")

    # Mover duas peças: a primeira com D2 e a segunda com D1
    elif opcao == 4:
        # Peça 1
        casa_1 = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa_1, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Testa jogada inválida com D2 e retorna à função Opções caso verdade
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            peca_movimento(casa_1, movimento[0], d2)
            var_global.dado_usado = 2
            var_global.cont_jogadas += 1
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        # Testa se a peça é a mesma. Se for, chama exceção
        while True:
            try:
                # Peça 2
                casa_2 = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
                movimento[1] = definir_tipo_de_jogada(casa_2, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[1] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
                elif var_global.jog_1:
                    if (casa_2 + d2) == casa_1:
                        raise ValueError
                elif var_global.jog_2:
                    if (casa_2 - d2) == casa_1:
                        raise ValueError
                peca_movimento(casa_2, movimento[1], d1)
                tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

                return True
            except ValueError:
                print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")

    # Mover uma peça: usando somente D1
    elif opcao == 5:
        # Validade da jogada única
        casa = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa, d1, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            peca_movimento(casa, movimento[0], d1)
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

            return True

    # Mover uma peça: usando somente D2
    elif opcao == 6:
        # Validade da jogada única
        casa = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa, d2, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False
        else:
            peca_movimento(casa, movimento[0], d2)
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

            return True

###############################################
def jogada_dados_igual(opcao, dado):
    """Função que verifica se a peça pode ser deslocada, para dados com valores iguais,
       conforme seu valor. Se for válida, a peça será deslocada"""
    movimento = [0, 0, 0, 0]
    casa_x = [0, 0, 0, 0]

    # Mover uma peça: usando 4*D1
    if opcao == 1:
        # Validade das quatro jogadas
        casa_x[0] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        if var_global.jog_1:
            for cont in range(4):
                movimento[cont] = definir_tipo_de_jogada(casa_x[0]-cont*dado, dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[cont] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
        else:
            for cont in range(4):
                movimento[cont] = definir_tipo_de_jogada(casa_x[0]+cont*dado, dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[cont] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
        
        # Se não há movimentos inválidos
        if var_global.jog_1:
            for cont in range(4):
                peca_movimento(casa_x[0]-cont*dado, movimento[cont], dado)
        else:
            for cont in range(4):
                peca_movimento(casa_x[0]+cont*dado, movimento[cont], dado)
        
        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        return True
    
    # Mover duas peças: usando 2*D1 e 2*D1
    elif opcao == 2:
        # Peça 1
        casa_x[0] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa_x[0], 2*dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Testa jogada inválida com D1 e retorna à função Opções caso verdade
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False

        # Testa se a peça é a mesma. Se for, chama exceção
        while True:
            try:
                # Peça 2
                casa_x[1] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
                movimento[1] = definir_tipo_de_jogada(casa_x[1], 2*dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[1] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
                elif var_global.jog_1:
                    if (casa_x[1] + 2*dado) == casa_x[0]:
                        raise ValueError
                    else:
                        break
                elif var_global.jog_2:
                    if (casa_x[1] - 2*dado) == casa_x[0]:
                        raise ValueError
                    else:
                        break
            except ValueError:
                print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")
        
        peca_movimento(casa_x[0], movimento[0], 2*dado)
        peca_movimento(casa_x[1], movimento[1], 2*dado)
        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        return True

    # Mover duas peças: usando 3*D1 e D1
    elif opcao == 3:
        # Peça 1
        casa_x[0] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
        movimento[0] = definir_tipo_de_jogada(casa_x[0], 3*dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
        # Testa jogada inválida com D1 e retorna à função Opções caso verdade
        if movimento[0] == 2:
            tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
            return False

        # Testa se a peça é a mesma. Se for, chama exceção
        while True:
            try:
                # Peça 2
                casa_x[1] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
                movimento[1] = definir_tipo_de_jogada(casa_x[1], dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                if movimento[1] == 2:
                    tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                    return False
                elif var_global.jog_1:
                    if (casa_x[1] + 2*dado) == casa_x[0]:
                        raise ValueError
                    else:
                        break
                elif var_global.jog_2:
                    if (casa_x[1] - dado) == casa_x[0]:
                        raise ValueError
                    else:
                        break
            except ValueError:
                print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")

        peca_movimento(casa_x[0], movimento[0], 3*dado)
        peca_movimento(casa_x[1], movimento[1], dado)
        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        return True

    # Mover três peças: usando 2*D1, D1 e D1
    elif opcao == 4:
        # Testa se a peça é a mesma. Se for, chama exceção
        # Peça 1, 2 e 3
        for cont in range(3):
            casa_x[cont] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
            while True:
                try:
                    if cont == 0:
                        movimento[cont] = definir_tipo_de_jogada(casa_x[cont], 2*dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                    else:
                        movimento[cont] = definir_tipo_de_jogada(casa_x[cont], dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                    
                    if movimento[cont] == 2:
                        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                        return False
                    elif var_global.jog_1 and cont == 1:
                        if (casa_x[cont] + dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_1 and cont == 2:
                        if (casa_x[cont] + 2*dado) == casa_x[cont-2] or (casa_x[cont] + dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_2 and cont == 1:
                        if (casa_x[cont] - dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_2 and cont == 2:
                        if (casa_x[cont] - 2*dado) == casa_x[cont-2] or (casa_x[cont] - dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                except ValueError:
                    print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")

        peca_movimento(casa_x[0], movimento[0], 2*dado)
        peca_movimento(casa_x[1], movimento[1], dado)
        peca_movimento(casa_x[2], movimento[2], dado)
        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        return True

    # Mover quatro peças: usando D1, D1, D1 e D1
    elif opcao == 5:
        # Testa se a peça é a mesma. Se for, chama exceção
        # Peça 1, 2, 3 e 4
        for cont in range(4):
            casa_x[cont] = selecionar_casa(var_global.jog_1, var_global.jog_2, var_global.pecas_posi, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA)
            while True:
                try:
                    movimento[cont] = definir_tipo_de_jogada(casa_x[cont], dado, var_global.jog_1, var_global.PC_CLARA, var_global.PC_ESCURA, var_global.PC_NULA, var_global.pecas_posi)
                    
                    if movimento[cont] == 2:
                        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)
                        return False
                    elif var_global.jog_1 and cont == 1:
                        if (casa_x[cont] + dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_1 and cont == 2:
                        if (casa_x[cont] + 2*dado) == casa_x[cont-2] or (casa_x[cont] + dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_1 and cont == 3:
                        if (casa_x[cont] + 3*dado) == casa_x[cont-3] or (casa_x[cont] + 2*dado) == casa_x[cont-2] \
                            or (casa_x[cont] + dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_2 and cont == 1:
                        if (casa_x[cont] - dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_2 and cont == 2:
                        if (casa_x[cont] - 2*dado) == casa_x[cont-2] or (casa_x[cont] - dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                    elif var_global.jog_2 and cont == 3:
                        if (casa_x[cont] - 3*dado) == casa_x[cont-3] or (casa_x[cont] - 2*dado) == casa_x[cont-2] \
                            or (casa_x[cont] - dado) == casa_x[cont-1]:
                            raise ValueError
                        else:
                            break
                except ValueError:
                    print("\nA peça selecionada foi a mesma. Você deve selecionar outra peça.\n")
        
        peca_movimento(casa_x[0], movimento[0], dado)
        peca_movimento(casa_x[1], movimento[1], dado)
        peca_movimento(casa_x[2], movimento[2], dado)
        peca_movimento(casa_x[3], movimento[3], dado)
        tabuleiro.print_tabuleiro(var_global.pecas_posi, var_global.pecas_retiradas_escuras, var_global.pecas_retiradas_claras, var_global.pecas_capturadas_escuras, var_global.pecas_capturadas_claras, var_global.CS_CLARA, var_global.CS_ESCURA, var_global.CS_MEIO)

        return True
        
###############################################
def jogada_opcoes(d1, d2):
    """Função para indicar as várias opções disponíveis do uso dos dados ao jogador"""
    if d1 == d2 and var_global.cont_jogadas == 0:
        while True:
            # Tratamento de exceção quando usuário entra com opção inválida
            try:
                print(COR_SUBLINHADO, end = "")
                if var_global.jog_1:
                    print(var_global.jogador_1, end = "")
                else:
                    print(var_global.jogador_2, end = "")
                print(", selecione uma das opções de jogadas disponíveis abaixo:" + COR_RESETALL + "\n")
                print("1 - Mover uma peça: usando quatro vezes D1 = " + str(d1))
                print("2 - Mover duas peças: a primeira duas vezes D1 = " + str(d1) + " e a segunda duas vezes D1 = " + str(d1))
                print("3 - Mover duas peças: a primeira três vezes D1 = " + str(d1) + " e a segunda uma vez D1 = " + str(d1))
                print("4 - Mover três peças: a primeira duas vezes D1 = " + str(d1) + ", a segunda uma vez D1 = " + str(d1) + " e a terceira uma vez D1 = " + str(d1))
                print("5 - Mover quatro peças: cada peça uma vez com D1 = " + str(d1) + "\n")
                opcao = int(input("Opção: "))
                if opcao < 1 or opcao > 5:
                    raise ValueError
                else:
                    # Movimento de uma peça 4*D1
                        if opcao == 1:
                            if jogada_dados_igual(opcao, d1):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de duas peças 2*D1
                        elif opcao == 2:
                            if jogada_dados_igual(opcao, d1):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de duas peças 3*D1 e D1
                        elif opcao == 3:
                            if jogada_dados_igual(opcao, d1):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de três peças 2*D1, D1 e D1
                        elif opcao == 4:
                            if jogada_dados_igual(opcao, d1):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de quatro peças D1, D1, D1 e D1
                        else:
                            if jogada_dados_igual(opcao, d1):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
            # Exceção
            except ValueError:
                print("\n" + COR_FUNDO_VERMELHO + "Opção inválida." + COR_RESETALL + " Repita a operação.\n")
    
    # Possibilidades em caso de dois dados diferentes
    else:
        while True:
            # Opções para quando não há peça capturada e irá usar os dois dados
            if var_global.dado_usado == 0:
                # Tratamento de exceção quando usuário entra com opção inválida
                try:
                    print(COR_SUBLINHADO, end = "")
                    if var_global.jog_1:
                        print(var_global.jogador_1, end = "")
                    else:
                        print(var_global.jogador_2, end = "")
                    print(", selecione uma das opções de jogadas disponíveis abaixo:" + COR_RESETALL + "\n")
                    print("1 - Mover uma peça: usando D1 = " + str(d1) + " primeiro e depois D2 = " + str(d2))
                    print("2 - Mover uma peça: usando D2 = " + str(d2) + " primeiro e depois D1 = " + str(d1))
                    print("3 - Mover duas peças: a primeira com D1 = " + str(d1) + " e a segunda com D2 = " + str(d2))
                    print("4 - Mover duas peças: a primeira com D2 = " + str(d2) + " e a segunda com D1 = " + str(d1) + "\n")
                    opcao = int(input("Opção: "))
                    # Valor de opção fora da faixa válida -> Chamada da exceção
                    if opcao < 1 or opcao > 4:
                        raise ValueError
                    else:
                        # Movimento de uma peça usando D1 primeiro e depois D2
                        if opcao == 1:
                            if jogada_dados_diff(opcao, d1, d2):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de uma peça usando D2 primeiro e depois D1
                        elif opcao == 2:
                            if jogada_dados_diff(opcao, d1, d2):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        # Movimento de duas peças usando D1 para a primeira e D2 para a segunda
                        elif opcao == 3:
                            if jogada_dados_diff(opcao, d1, d2):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                        else:
                            if jogada_dados_diff(opcao, d1, d2):
                                return
                            else:
                                jogada_opcoes(d1, d2)
                                return
                # Exceção
                except ValueError:
                    print("\n" + COR_FUNDO_VERMELHO + "Opção inválida." + COR_RESETALL + " Repita a operação.\n")
            
            # Opção para quando há somente uma peça capturada e irá usar D1 para movimentar
            elif var_global.dado_usado == 2:
                print(COR_SUBLINHADO, end = "")
                if var_global.jog_1:
                    print(var_global.jogador_1, end = "")
                else:
                    print(var_global.jogador_2, end = "")
                print(", lhe resta somente um movimento com o dado D1 = " + str(d1) + COR_RESETALL + "\n")
                opcao = 5
                if jogada_dados_diff(opcao, d1, d2):
                    return
                else:
                    jogada_opcoes(d1, d2)
                    return
            
            # Opção para quando há somente uma peça capturada e irá usar D2 para movimentar
            elif var_global.dado_usado == 1:
                print(COR_SUBLINHADO, end = "")
                if var_global.jog_1:
                    print(var_global.jogador_1, end = "")
                else:
                    print(var_global.jogador_2, end = "")
                print(", lhe resta somente um movimento com o dado D2 = " + str(d2) + COR_RESETALL + "\n")
                opcao = 6
                if jogada_dados_diff(opcao, d1, d2):
                    return
                else:
                    jogada_opcoes(d1, d2)
                    return