import sqlite3
from contextlib import contextmanager
from pathlib import Path

# CRUD - CREATE, READ, UPDATE, DELETE

# Caminho para o arquivo do banco de dados.
# caminho = Path(__file__).parent
# caminho_db = Path.joinpath(caminho, 'dados.db')


# CRIANDO UM GERENCIADOR DE CONTEXTO DECORANDO A FUNÇÃO CONECTA()
@contextmanager
def conecta():
    # Exemplo Usando PYMYSQL
    # conexao = pymysql.connect(
    #     host='127.0.0.1',
    #     user='cursopython',
    #     password='cursopython@123',
    #     db='clientes',
    #     charset='utf8mb4',
    #     cursorclass=pymysql.cursors.DictCursor
    # )

    # conexao = sqlite3.connect(caminho_db)

    conexao = sqlite3.connect('dados.db')

    try:
        yield conexao
    finally:
        conexao.close()

# CRIA AS TABELAS CASO AINDA NÃO EXISTAM.
with conecta() as conexao:
    cursor = conexao.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS "palavras" ('
                                '"id"	INTEGER,'
                                '"palavra"	TEXT,'
                                '"dica"	TEXT,'
                                'PRIMARY KEY("id" AUTOINCREMENT)'
                            ')')
    cursor.execute('CREATE TABLE IF NOT EXISTS "score" ('
                                '"id"	INTEGER,'
                                '"nome"	TEXT,'
                                '"pontos"	INTEGER,'
                                'PRIMARY KEY("id" AUTOINCREMENT)'
                            ')')


# INSERE UM REGISTRO NA BASE DE DADOS
def inserir(tabela, val01, val02):
    with conecta() as conexao:
        cursor = conexao.cursor()

        if tabela == 'palavras':
            comando = 'INSERT OR IGNORE INTO palavras (palavra, dica) VALUES (?, ?)'
        if tabela == 'score':
            comando = 'INSERT OR IGNORE INTO score (nome, pontos) VALUES (?, ?)'
        
        cursor.execute(comando, (val01, val02))
        conexao.commit()


# DELETA UM REGISTRO DA BASE DE DADOS
def remover(tabela: str, id: int):
    with conecta() as conexao:
        cursor = conexao.cursor()

        if tabela == 'palavras':
            comando = 'DELETE FROM palavras WHERE id=?'
        if tabela == 'score':
            comando = 'DELETE FROM score WHERE id=?'
        
        cursor.execute(comando, (id,))
        conexao.commit()


# DELETA QUANTIDADE DETERMINADA DE REGISTROS
def remover_varios(tabela: str, args: tuple):
    with conecta() as conexao:
        cursor = conexao.cursor()
        
        if tabela == 'palavras':
            comando = 'DELETE FROM palavras WHERE id=?'
        if tabela == 'score':
            comando = 'DELETE FROM score WHERE id=?'
        
        for id in args:
            cursor.execute(comando, (id,))
        conexao.commit()


# ATUALIZA UM REGISTRO NA BASE DE DADOS
def atualizar(tabela, val01, val02, id):
    with conecta() as conexao:
        cursor = conexao.cursor()

        if tabela == 'palavras':
            comando = 'UPDATE palavras SET palavra=?, dica=? WHERE id=?'
        if tabela == 'score':
            comando = 'UPDATE score SET nome=?, pontos=? WHERE id=?'
        
        cursor.execute(comando, (val01, val02, id,))
        conexao.commit()


# ESTE SELECIONA OS DADOS DA BASE DE DADOS
def listar(tabela):
    with conecta() as conexao:
        cursor = conexao.cursor()

        if tabela == 'palavras':
            comando = 'SELECT * FROM palavras ORDER BY id ASC LIMIT 100'
        if tabela == 'score':
            comando = 'SELECT * FROM score ORDER BY pontos ASC LIMIT 100'

        cursor.execute(comando)
        resultado = cursor.fetchall()

        return resultado


# PROCURA TODOS OS VALORES QUE CORRESPONDEREM AO VALOR DO TIPO INFORMADO NA TABELA.
def buscar(tabela, tipo, valor):
    with conecta() as conexao:
        cursor = conexao.cursor()

        if tabela == 'palavras':
            comando = f'SELECT * FROM palavras WHERE {tipo} LIKE ?'
        if tabela == 'score':
            comando = f'SELECT * FROM score WHERE {tipo} LIKE ?'

        cursor.execute(comando, (f'%{valor}%',))
        resultado = cursor.fetchall()
        return resultado


if __name__ == '__main__':
    # inserir('score', 'Pedro', 3)
    # inserir('score', 'marcelo', 5)
    # inserir('score', 'roberta', 2)
    # inserir('score', 'jandira', 10)
    pass
