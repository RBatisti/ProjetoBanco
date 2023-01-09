from lib import Arquivo
from lib import Estetico

# Define o nome do arquivo
arquivo = 'dados.txt'

# Se o arquivo não exite
if not Arquivo.arquivo_existe(arquivo):

    # Cria o arquivo
    Arquivo.criararquivo(arquivo)


while True:
    Estetico.cabecario()

    # Mostrar as opções
    Estetico.opcoes(['Visualizar contas cadastradas', 'Cadastrar nova conta', 'Realizar saque',
                     'Realizar depósito', 'Realizar transferência', 'Dados do Banco', 'Apagar todos os dados',
                     'Sair do programa'])

    opc = Arquivo.leiaint('Sua opção: ')

    if opc == 1:
        Arquivo.lerarquivo(arquivo)

    elif opc == 2:
        Arquivo.cadastrar(arquivo)

    elif opc == 3:
        Arquivo.sacar(arquivo)

    elif opc == 4:
        Arquivo.depositar(arquivo)

    elif opc == 5:
        Arquivo.transferir(arquivo)

    elif opc == 6:
        Arquivo.dados_banco(arquivo)

    elif opc == 7:
        Arquivo.apagar_arquivo(arquivo)

    elif opc == 8:
        Estetico.fim()

    # Se a opção inserida não estiver entre as opções
    else:
        Estetico.linha()
        print(Estetico.cores('vermelho'), end='')
        print('FAVOR SELECIONE DE 1 A 8!'.center(60), Estetico.cores())
