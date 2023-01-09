from time import sleep


# Muda de cor o texto
def cores(cor='limpa'):
    if cor == 'limpa':
        return '\033[m'
    elif cor == 'vermelho':
        return '\033[31m'
    elif cor == 'azul':
        return '\033[34m'


# Insere uma linha
def linha(quant=60, tipo='='):
    print(tipo * quant)


# Cria um cabeçalho
def cabecario(msg='PROJETO BANCO', tipo='=', ultima=True, red=False, quant=60):
    linha(quant, tipo)
    if red:
        print(cores('vermelho'), end='')
        print(msg.center(quant))
        print('Selecione a opção 2 e crie agora mesmo!'.center(60))
        print(cores(), end='')
    else:
        print(msg.center(quant), '\033[m')
    if ultima:
        linha(quant, tipo)


# Mostra ordenadamente as opções
def opcoes(txt):
    for c in range(len(txt)):
        print(f'{c + 1}. {txt[c]}')
    linha()


# Faz a animação do encerramento do programa
def fim():
    sleep(0.25)

    # Animação
    for c in range(60):
        sleep(0.015)
        print('>', end='')

    # Pular uma linha
    print()

    print(cores('azul'), end='')
    print('PROGRAMA ENCERRADO COM SUCESSO'.center(60))
    print('VOLTE SEMPRE!'.center(60), cores())

    # Animação
    for c in range(60):
        sleep(0.015)
        print('>', end='')
    exit()



