from PyQt5 import uic, QtWidgets
from pathlib import Path
from dados import * #inserir, atualizar, listar, buscar, remover, remover_varios
from random import choice


# Funções do Menu Principal
def carregar_menu(menu):
    menu.show()
    carregar_Inicial(menu)


def carregar_Inicial(menu):
    menu.paginas.setCurrentWidget(menu.paginaInicial)
    carregar_score()
    

def carregar_score():
    lista = [x for x in listar('score')]

    menu.labelPrimeiro.setText('-')
    menu.labelPontosPrimeiro.setText('-')
    menu.labelSegundo.setText('-')
    menu.labelPontosSegundo.setText('-')
    menu.labelTerceiro.setText('-')
    menu.labelPontosTerceiro.setText('-')
    
    if lista:
        for c, v in enumerate(lista):
            if c == 0:
                menu.labelPrimeiro.setText(lista[-1][1])
                menu.labelPontosPrimeiro.setText(str(lista[-1][2]))
            if c == 1:
                menu.labelSegundo.setText(lista[-2][1])
                menu.labelPontosSegundo.setText(str(lista[-2][2]))
            if c == 2:
                menu.labelTerceiro.setText(lista[-3][1])
                menu.labelPontosTerceiro.setText(str(lista[-3][2]))
            if c == 3:
                break


# Funções do Menu de Palavras
def carregar_palavras(menu):
    menu.paginas.setCurrentWidget(menu.paginaPalavras)
    carregar_lista_palavras(menu)


def carregar_lista_palavras(menu):
    menu.listaDePalavras.clear()
    menu.listaDePalavras.addItem(f'ID  -  PALAVRA  -  DICA')
    for id, palavra, dica in listar('palavras'):
        menu.listaDePalavras.addItem(f'{id:>3}  -  {palavra}  -  {dica}')


# Aba de Cadastro
def load_cadastrar_palavras(menu):
    menu.close()
    menu.show()
    menu.inputPalavra.setText('')
    menu.inputDica.setText('')


def cadastrar_palavra(cadastroPalavras, menu):
    palavra = cadastroPalavras.inputPalavra
    dica = cadastroPalavras.inputDica

    if palavra.text() and dica.toPlainText():
        if palavra.text() == 'Insira Uma Palavra!' or dica.toPlainText() == 'Insira Uma Dica!':
            return
        inserir('palavras', palavra.text().upper(), dica.toPlainText().capitalize())
        carregar_lista_palavras(menu)
        palavra.setText('')
        dica.setPlainText('')
    else:
        if not palavra.text():
            palavra.setText('Insira Uma Palavra!')
        if not dica.toPlainText():
            dica.setPlainText('Insira Uma Dica!')


# Aba de remoção
def load_remover_palavras(menu):
    menu.close()
    # menu.showMaximized()
    menu.show()
    menu.inputID.setText('')


def apagar_palavra(removerPalavras, menu):
    id = removerPalavras.inputID.text()

    if id.isnumeric():
        remover('palavras', id)
        removerPalavras.inputID.setText('')
        carregar_lista_palavras(menu)
    else:
        removerPalavras.inputID.setText('Inválido!')


# Funções do Menu do jogo
def carregar_jogo(menu):
    if coletar():
        menu.paginas.setCurrentWidget(menu.paginaGame)
    else:
        carregar_palavras(menu)

def coletar():
    global palavra
    lista = [x for x in listar('palavras')]
    if lista:
        elemento = choice(lista)
        palavra = elemento[1]
        dica = elemento[2]
        chances = 3
        palavra_exibida = '_' * len(palavra)

        menu.labelPalavraSecreta.setText(palavra_exibida)
        menu.labelDica.setText(f'{len(palavra)} Letras - {dica}')
        menu.labelTentativas.setText(str(chances))
        menu.labelVitorias.setText(str(0))
        return True
    return False


def validar_jogo(menu, cadastroJogador):
    global palavra, pontos
    tentativa = menu.inputTentativa.text().upper()
    palavra_exibida = menu.labelPalavraSecreta.text()
    temporario = ''

    if palavra_exibida == 'VOCÊ PERDEU!':
        carregar_Inicial(menu)
        menu.inputTentativa.setText('')
        return

    if tentativa:
        if len(tentativa) < len(palavra):
            tentativa += '_' * (len(palavra) - len(tentativa))
            
        for indice, letra in enumerate(palavra):
            if letra in tentativa[indice] and letra not in palavra_exibida[indice]:
                temporario += letra
            elif letra in palavra_exibida[indice]:
                temporario += letra
            else:
                temporario += '_'

        if temporario:
            menu.labelPalavraSecreta.setText(temporario)
        if temporario == palavra and len(palavra) == len(tentativa):
            carregar_jogo(menu)
            pontos += 1
        else:
            chances = menu.labelTentativas
            chances.setText(str(int(chances.text()) -1))
            if int(chances.text()) == 0:
                menu.labelPalavraSecreta.setText('VOCÊ PERDEU!')
                load_cadastro_jogador(cadastroJogador)
        menu.labelVitorias.setText(str(pontos))
        menu.inputTentativa.setText('')


def load_cadastro_jogador(cadastroJogador):
    cadastroJogador.show()

def salvar_dados(cadastroJogador, menu, pontos):
    nome = cadastroJogador.inputNome.text()
    pontos = pontos

    if nome:
        inserir('score', nome, pontos)
            
        carregar_Inicial(menu)
        carregar_score()
        cadastroJogador.inputNome.setText('')
        cadastroJogador.close()


# Programa Principal
if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    # caminho = Path(__file__).parent

    # Menu Principal
    menu = uic.loadUi('PalavraSecreta.ui') #uic.loadUi(Path.joinpath(caminho, 'PalavraSecreta.ui'))
    menu.btnSair.clicked.connect(lambda: menu.close())
    menu.btnPalavras.clicked.connect(lambda: carregar_palavras(menu))
    menu.btnNovoJogo.clicked.connect(lambda: carregar_jogo(menu))

    # Ininialização do jogo
    pontos = 0
    palavra = ''
    menu.btnTentativa.clicked.connect(lambda: validar_jogo(menu, cadastroJogador))
    menu.btnSairJogo.clicked.connect(lambda: carregar_Inicial(menu))

    # Tela de Cadastro de Jogador
    cadastroJogador = uic.loadUi('CadastroJogador.ui') #uic.loadUi(Path.joinpath(caminho, 'CadastroJogador.ui'))
    cadastroJogador.btnComecar.clicked.connect(lambda: salvar_dados(cadastroJogador, menu, pontos))

    # Menu Palavras
    menu.btnVoltar.clicked.connect(lambda: menu.paginas.setCurrentWidget(menu.paginaInicial))
    menu.btnAdicionar.clicked.connect(lambda: load_cadastrar_palavras(cadastroPalavras))
    menu.btnRemover.clicked.connect(lambda: load_remover_palavras(removerPalavras))

    # Tela de Cadastro de Palavras
    cadastroPalavras = uic.loadUi('CadastroNovaPalavra.ui') #uic.loadUi(Path.joinpath(caminho, 'CadastroNovaPalavra.ui'))
    cadastroPalavras.btnCadastrar.clicked.connect(lambda: cadastrar_palavra(cadastroPalavras, menu))
    cadastroPalavras.btnSair.clicked.connect(lambda: cadastroPalavras.close())

    # Tela de Remoção de Palavras
    removerPalavras = uic.loadUi('RemoverUmaPalavra.ui') #uic.loadUi(Path.joinpath(caminho, 'RemoverUmaPalavra.ui'))
    removerPalavras.btnApagar.clicked.connect(lambda: apagar_palavra(removerPalavras, menu))


    # Iniciando o Aplicativo
    carregar_menu(menu)
    app.exec()

    # Comandos Para Criar o Executável:
    # pip install pyinstaller
    # 1° opção: pyinstaller --onefile --noconsole .\main.py
    # 2° opção: pyinstaller --onefile --windowed --icon=favicon.ico main.py
