from lib.Estetico import *
from time import sleep


# Excluir informações do arquivo
def apagar_arquivo(nome_arquivo):
    confirmacao = input('Digite APAGAR para excluir o arquivo: ')

    if confirmacao.lower() == 'apagar':
        try:
            a = open(nome_arquivo, 'w')
            a.close()
        except Exception as erro:
            linha()
            print('\033[31m', end='')
            print(f'HOUVE UM ERRO {erro} AO TENTAR ABRIR O ARQUIVO'.center(60), '\033[m')
            linha()
        else:
            linha()
            print('Arquivo excluido com sucesso!')


# transformar para float
def trans_din_float(num):
    num = str(num)
    num = num.replace('R$', '').replace(',', '.')
    num = float(num)
    return num


# transformar para dinheiro
def trans_float_din(num):
    num = f'{num:.2f}'
    num = 'R$' + str(num).replace('.', ',')
    return num


# Força usuário inserir um valor float
def leiafloat(msg):
    while True:
        num = (input(msg)).replace(',', '.')
        try:
            num = float(num)
        except ValueError:
            linha()
            print(cores('vermelho'), end='')
            print('DIGITE UM VALOR VÁLIDO!'.center(60), cores())
            linha()
        else:
            return num


# Força usuario reponder
def obrigatorio(resp):
    if resp == '':
        print(cores('vermelho'), 'Item obrigatório, favor preencher com atenção!', cores())
    else:
        return resp


# Força usuário inserir um valor inteiro com tamanho personalizavel em quant
def leiaint(msg, quant=0):
    while True:
        num = input(msg)
        if quant != 0:

            # Verifica o tamanho
            if len(str(num)) != quant:
                linha()
                print(cores('vermelho'), end='')
                print(f'O NÚMERO DEVE CONTER {quant} ALGARISMOS'.center(60), cores())
                linha()
                continue

        # Verifica se é inteiro
        try:
            num = int(num)
        except ValueError:
            linha()
            print(cores('vermelho'), end='')
            print('DIGITE UM NÚMERO INTEIRO VÁLIDO!'.center(60), cores())
            linha()
        else:
            return num


# verificar se a conta existe
def conta_existe(arq, msg):
    try:
        a = open(arq, 'r')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao tentar visualizar o arquivo', cores())
    else:
        unica_str = a.read()
        dividido = unica_str.split(';')

        while True:

            # Solicita o número da conta
            conta = leiaint(msg, 4)

            contador = 0

            # Loop nas contas
            for c in dividido:
                contador += 1
                if contador == 4:

                    # Se a conta do loop é igual a inserida valida
                    if int(c) == conta:
                        a.close()
                        return conta

                    contador = 0

            # Se não encontrou a conta
            linha()
            print(cores('vermelho'), end='')
            print('CONTA NÃO ENCONTRADA'.center(60), cores())
            linha()


# cadastrar um novo cliente
def cadastrar(arq):
    linha()
    nome = obrigatorio(input('Nome completo: '))
    nascimento = obrigatorio(input('Data de nascimento: '))
    email = obrigatorio(input('Email: '))
    valor = obrigatorio(leiafloat('Saldo inicial: R$'))
    valor = f'{valor:.2f}'
    try:
        a = open(arq, 'at')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao abrir o arquivo', cores())
    else:
        b = open(arq, 'r')
        unica_str = b.read()
        b.close()
        numero_cadastro = unica_str.count('\n')
        conta = numero_cadastro + 1000
        try:
            a.write(f'{nome};{nascimento};{email};{conta};R${str(valor.replace(",", "."))}\n')
            a.close()
        except Exception as erro:
            print(cores('vermelho'), f'Houve um erro {erro} ao inserir os dados no arquivo', cores())
        else:
            linha()
            print('Conta cadastrada com sucesso'.center(60))
            print(f'O número da conta é: {conta}'.center(60))


# verificar se arquivo existe
def arquivo_existe(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


# criar arquivo
def criararquivo(nome):
    try:
        _ = open(nome, 'wt+')
    except Exception as erro:
        print(f'Ocorreu um erro {erro} ao criar o arquivo {nome}')
    else:
        print(f'O arquivo {nome} foi criado com sucesso')


# adicionar um ponto a cada 3 algarismos para facilitar a visualização
def mostrar_saldo(valor):

    # Lendo o tamanho do saldo, sem o cifrão e centavos
    caracteres_saldo = len(valor) - 6

    # Quantidade de pontos que deverão ser inseridos
    calculo = caracteres_saldo % 3
    caracteres_saldo -= calculo
    caracteres_saldo /= 3
    contador = -3
    contador_2 = 0
    valor_saldo = valor.replace('.', ',')

    # Invertendo o valor
    valor_saldo = valor_saldo[::-1]

    valor_saldo_pronto = ''

    # loop nos algarimos
    for c in valor_saldo:
        contador += 1
        valor_saldo_pronto += c
        if contador == 3:
            if contador_2 != caracteres_saldo:
                valor_saldo_pronto += '.'
                contador = 0
                contador_2 += 1

    # retorna o valor envertendo-o novamente
    return valor_saldo_pronto[::-1]


# mostrar dados de todos os clientes registrados
def lerarquivo(nome):
    vazio = True
    try:
        a = open(nome, 'rt')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao ler o arquivo')
    else:

        # Verifica se o arquivoi está vazio
        for _ in a:
            vazio = False

        if vazio:
            cabecario('NÃO EXISTE NENHUMA CONTA CADASTRADA', '=', False, True)

        else:
            cabecario('CONTAS CADASTRADAS', '=', False)
        a = open(nome, 'rt')

        # Mostra os dados das contas
        for line in a:
            dado = line.split(';')
            dado[4] = dado[4].replace('\n', '')
            linha()
            valor_saldo_pronto = mostrar_saldo(dado[4])
            sleep(0.4)
            print(f'{"Nome":.<13}{dado[0]}\n{"Conta":.<13}{dado[3]}\n{"Nascimento":.<13}{dado[1]}\n'
                  f'{"Email":.<13}{dado[2]}\n{"Saldo":.<13}{valor_saldo_pronto}')

        # Fecha o arquivo
        a.close()


# sacar valor em uma determinada conta
def sacar(arquivo):
    linha()
    dados = []
    cont = 0
    cont_parado = 0
    conta = conta_existe(arquivo, 'Número da conta: ')
    valor_sacar = leiafloat('Quanto deseja sacar: R$')

    # Abrindo o arquivo
    try:
        a = open(arquivo, 'r')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao visualizar o arquivo', cores())
    else:
        for line in a:
            dado = line.split(';')

            # Retira a quebra de linha
            dado[4] = dado[4].replace('\n', '')
            for c in dado:
                dados.append(c)
                cont += 1
                if c == str(conta):
                    cont_parado = cont

        # Fechando o arquivo
        a.close()

        # Se a cota não foi encontrada
        if cont_parado == 0:
            linha()
            print(cores('vermelho'), '', 'ERRO CONTA NÃO ENCONTRADA'.center(60), '', cores())

        saldo_conta_float = trans_din_float(dados[cont_parado])

        # Se o saldo for menor que o valor do regate
        if saldo_conta_float < valor_sacar:
            print(cores('vermelho'), 'SALDO INSUFICIENTE PARA RESGATE'.center(60))
            print(f'Falta {mostrar_saldo(trans_float_din(valor_sacar - saldo_conta_float))} '
                  f'para concluir o resgate'.center(60), cores())

        # Se for válido
        else:
            linha()
            print(f'{trans_float_din(valor_sacar)} resgatado com sucesso'.center(60))
            print(f'Saldo atual: {mostrar_saldo(trans_float_din(saldo_conta_float - valor_sacar))}'.center(60))

            # Diminuindo saldo
            saldo_conta_atual_float = saldo_conta_float - valor_sacar

            b = open(arquivo, 'r')
            unica_str = b.read()
            unica_str = unica_str.replace('\n', ';  ')
            dividido = unica_str.split(';')
            cont = 0

            for c in dividido:
                cont += 1

                # Corrigindo erro de dois espaços
                if '  ' in c:
                    c = c.replace('  ', '\n')

                if c == str(conta):
                    cont_parado = cont
            dividido[cont_parado] = (trans_float_din(saldo_conta_atual_float)).replace(',', '.')
            cont = 0
            for c in dividido:
                cont += 1
                if cont % 5 == 0:
                    valor = c + '\n'
                    dividido[cont - 1] = valor

            arquivo_pronto = ';'.join(dividido)
            arquivo_pronto = arquivo_pronto.replace(';  ', '')

            # Modificando o arquivo com o saldo atualizado
            b = open(arquivo, 'w')
            b.write(arquivo_pronto)
            b.close()

            # Fechando o arquivo
            b.close()


# depositar valor em uma determinada conta
def depositar(arquivo):
    linha()
    dados = []
    cont = 0
    cont_parado = 0

    # Solicitando dados
    conta = conta_existe(arquivo, 'Número da conta: ')
    valor_depositar = leiafloat('Quanto deseja depositar: R$')

    # verificando valor mínimo
    if valor_depositar < 1:
        linha()
        print(cores('vermelho'), end='')
        print('VALOR MÍNIMO PARA DEPOSITO É R$1,00'.center(60), cores())
        return
    try:
        _ = open(arquivo, 'r')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao visualizar o arquivo', cores())
    else:
        a = open(arquivo, 'r')
        for line in a:
            dado = line.split(';')
            dado[4] = dado[4].replace('\n', '')
            for c in dado:
                dados.append(c)
                cont += 1
                if c == str(conta):
                    cont_parado = cont

        # Saldo
        saldo_conta_float = trans_din_float(dados[cont_parado])

        linha()
        print(f'{trans_float_din(valor_depositar)} depositado com sucesso'.center(60))
        saldo_conta_atual_float = saldo_conta_float + valor_depositar
        print(f'Saldo atual: {mostrar_saldo(trans_float_din(saldo_conta_atual_float))}'.center(60))

        b = open(arquivo, 'r')
        unica_str = b.read()
        unica_str = unica_str.replace('\n', ';  ')
        dividido = unica_str.split(';')
        cont = 0

        for c in dividido:
            cont += 1
            if '  ' in c:

                # Corrigindo erro de dois espaços
                c = c.replace('  ', '\n')

            if c == str(conta):
                cont_parado = cont
        dividido[cont_parado] = (trans_float_din(saldo_conta_atual_float)).replace(',', '.')
        cont = 0
        for c in dividido:
            cont += 1
            if cont % 5 == 0:
                valor = c + '\n'
                dividido[cont - 1] = valor

        arquivo_pronto = ';'.join(dividido)
        arquivo_pronto = arquivo_pronto.replace(';  ', '')

        # Modificando o arquivo com valores atualizados
        b = open(arquivo, 'w')
        b.write(arquivo_pronto)
        b.close()


# transferir valor de uma conta para outra
def transferir(arquivo):
    saldo_conta_origem = ''
    nome_conta_origem = ''

    # Inputs e verificações
    conta_origem = conta_existe(arquivo, 'Conta de origem: ')
    conta_destino = conta_existe(arquivo, 'Conta de destino: ')
    if conta_destino == conta_origem:
        linha()
        print(cores('vermelho'), end='')
        print('CONTA DE ORIGEM E CONTA DE DESTINO DEVEM SER DIFERENTES!'.center(60), cores())
        linha()
        return
    while True:
        valor_tranferir = leiafloat('Valor da transferencia: R$')
        if valor_tranferir < 1:
            linha()
            print(cores('vermelho'), end='')
            print('VALOR MÍNIMO DE TRANSFERÊNCIA É DE RS1,00'.center(60), cores())
            linha()
        else:
            break

    # Retirando dinheiro da conta de origem
    linha()
    dados = []
    cont = 0
    cont_parado = 0

    conta = conta_origem
    valor_sacar = valor_tranferir
    try:
        a = open(arquivo, 'rt')
    except Exception as erro:
        print(cores('vermelho'), f'Houve um erro {erro} ao visualizar o arquivo', cores())
    else:
        for line in a:
            dado = line.split(';')
            dado[4] = dado[4].replace('\n', '')
            for c in dado:
                dados.append(c)
                cont += 1
                if c == str(conta):
                    cont_parado = cont

        # Fechando arquivo
        a.close()

        if cont_parado == 0:
            linha()
            print(cores('vermelho'), '', 'ERRO CONTA NÃO ENCONTRADA'.center(60), '', cores())

        saldo_conta_float = trans_din_float(dados[cont_parado])
        saldo_conta_origem = saldo_conta_float - valor_tranferir
        nome_conta_origem = dados[cont_parado - 4]

        if saldo_conta_float < valor_sacar:
            print(cores('vermelho'), 'SALDO INSUFICIENTE PARA TRANFERÊNCIA'.center(60))
            print(f'FALTA {mostrar_saldo(trans_float_din(valor_sacar - saldo_conta_float))} '
                  f'PARA CONCLUIR A TRANSFERÊNCIA'.center(60), cores())
            return

        else:
            saldo_conta_atual_float = saldo_conta_float - valor_sacar
            b = open(arquivo, 'r')
            unica_str = b.read()
            unica_str = unica_str.replace('\n', ';  ')
            dividido = unica_str.split(';')
            cont = 0

            for c in dividido:
                cont += 1

                if '  ' in c:
                    c = c.replace('  ', '\n')

                if c == str(conta):
                    cont_parado = cont

            dividido[cont_parado] = (trans_float_din(saldo_conta_atual_float)).replace(',', '.')
            cont = 0

            for c in dividido:
                cont += 1
                if cont % 5 == 0:
                    valor = c + '\n'
                    dividido[cont - 1] = valor

            arquivo_pronto = ';'.join(dividido)
            arquivo_pronto = arquivo_pronto.replace(';  ', '')

            # Modificando arquivo com valores atualizados
            b = open(arquivo, 'w')
            b.write(arquivo_pronto)
            b.close()

    # Adicionando dinheiro na conta de destino
    dados = []
    cont = 0
    cont_parado = 0
    conta = conta_destino
    valor_depositar = valor_tranferir
    try:
        a = open(arquivo, 'rt')
    except Exception as erro:
        print(cores('vermelho'), end='')
        print(f'HOUVE UM ERRO {erro} AO VISUALIZAR O ARQUIVO'.center(60), cores())
    else:
        a.close()
        a = open(arquivo, 'rt')
        for line in a:
            dado = line.split(';')
            dado[4] = dado[4].replace('\n', '')
            for c in dado:
                dados.append(c)
                cont += 1
                if c == str(conta):
                    cont_parado = cont
        if cont_parado == 0:
            linha()
            print(cores('vermelho'), '', 'ERRO CONTA NÃO ENCONTRADA'.center(60), '', cores())

        nome_conta_destino = dados[cont_parado - 4]
        saldo_conta_float = trans_din_float(dados[cont_parado])
        print(f'{trans_float_din(valor_depositar)} transferido com sucesso'.center(60))
        saldo_conta_atual_float = saldo_conta_float + valor_depositar

        # Mostrando resultado
        linha()
        print(f'SALDO ATUAL:'.center(60))
        print(f'->Conta {conta_origem} de {nome_conta_origem} é {mostrar_saldo(trans_float_din(saldo_conta_origem))}')
        print(f'->Conta {conta_destino} de {nome_conta_destino} é '
              f'{mostrar_saldo(trans_float_din(saldo_conta_atual_float))}')

        b = open(arquivo, 'r')
        unica_str = b.read()
        unica_str = unica_str.replace('\n', ';  ')
        dividido = unica_str.split(';')
        cont = 0
        for c in dividido:
            cont += 1
            if '  ' in c:
                c = c.replace('  ', '\n')

            if c == str(conta):
                cont_parado = cont
        dividido[cont_parado] = (trans_float_din(saldo_conta_atual_float)).replace(',', '.')
        cont = 0

        for c in dividido:
            cont += 1
            if cont % 5 == 0:
                valor = c + '\n'
                dividido[cont - 1] = valor

        arquivo_pronto = ';'.join(dividido)
        arquivo_pronto = arquivo_pronto.replace(';  ', '')

        # Modificando o arquivo com valores atualizados
        b = open(arquivo, 'w')
        b.write(arquivo_pronto)
        b.close()


# Mostrar dados do banco em geral
def dados_banco(arquivo):
    try:
        a = open(arquivo, 'r')
        a.close()
    except Exception as erro:
        linha()
        print(cores('vermelho'), end='')
        print(f'HOUVE UM ERROU {erro} AO TENTAR VISUALIZAR O ARQUIVO'.center(60), cores())
        return
    else:

        # Lendo o arquivo
        a = open(arquivo, 'r')
        unica_str = a.read()
        quantidade_clinte = unica_str.count('\n')

        linha()

        # Mostrando se não possui nenhum clinte
        if quantidade_clinte == 0:
            print('Não possuimos nenhum dado, pois não há registro de clientes'.center(60))
            return

        # Senão
        print(f'Possuimos {quantidade_clinte} clientes cadastrados em nosso sistema'.center(60))

        unica_str = unica_str.replace('\n', ';')
        dividido = unica_str.split(';')
        valores = []
        contador = 0

        # Loop nos clientes
        for c in dividido:
            contador += 1
            if contador == 5:

                # Somando saldo dos clientes
                valores.append(trans_din_float(c))
                contador = 0

        caixa_banco = float()
        for c in valores:
            caixa_banco += c
        caixa_banco = trans_float_din(caixa_banco)
        print(f'Armazenamos {mostrar_saldo(caixa_banco)} em cofres'.center(60))
