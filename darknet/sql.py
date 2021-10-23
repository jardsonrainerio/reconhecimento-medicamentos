
# -*- coding: utf-8 -*-
"""Exemplo de CRUD com Python 3 e SQLite3"""

import sqlite3


class ConectarDB:
    """Classe."""

    def __init__(self):
        """Construtor.
        O construtor é executado sempre que a classe é instanciada.
        """
        # Criar banco na memória (assim que a execução termina o banco é eliminado).
        # self.con = sqlite3.connect(':memory:')

        # Criar banco localmente.
        # Também pode ser passado o path/caminho onde o banco será criado.
        # self.con é responsável por manter uma conexão aberta com o banco (commit, rollback, close, etc).
        self.con = sqlite3.connect('db.sqlite3')

        # Criando o cursor que irá executar os comandos SQL (instruções DML, DDL, etc).
        self.cur = self.con.cursor()

        # Criando a tabela.
        self.criar_tabela()

    def criar_tabela(self):
        """Cria a tabela caso a mesma não exista."""
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS ALERTA (
                nome TEXT)''')
        except Exception as e:
            print(f'[x] Falha ao criar tabela [x]: {e}')
        else:
            print('[!] Tabela criada com sucesso [!]\n')

    def inserir_registro(self, usuario):

        try:
            self.cur.execute(
                '''INSERT INTO ALERTA VALUES (?)''', [usuario])
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            # rollback reverte/desfaz a operação.
            self.con.rollback()
        else:
            # commit registra a operação/transação no banco.
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')

    def inserir(self):
        try:
            with open("myfile.txt", "r") as f:
                rows = f.readlines()
                for row in rows:
                    fields = row.replace('\n', '').split(',')
                    self.cur.execute(f'INSERT INTO ALERTA (nome)' \
                              f"VALUES ('{fields[0]}')")
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            # rollback reverte/desfaz a operação.
            self.con.rollback()
        else:
            # commit registra a operação/transação no banco.
            self.con.commit()


            #print('\n[!] Registro inserido com sucesso [!]\n')
    def inserir_varios_registros(self, usuarios):

        try:
            self.cur.executemany(
                '''INSERT INTO ALERTA VALUES (?, ?)''', usuarios)
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')

    def consultar_registro_pela_id(self, rowid):

        return self.cur.execute('''SELECT * FROM ALERTA WHERE rowid=?''', (rowid,)).fetchone()

    def consultar_alerta(self, limit=10):

        return self.cur.execute('''SELECT nome FROM ALERTA LIMIT ?''', (limit,)).fetchall()

    def consultar_medicamentos(self, limit=10):

        return self.cur.execute('''SELECT nome FROM MEDICAMENTOS LIMIT ?''', (limit,)).fetchall()

    def consultar_hora(self, hora):

        return self.cur.execute('''SELECT * FROM MEDICAMENTOS WHERE HORA=?''', (hora,)).fetchall()

    def alterar_registro(self, rowid, nome, sexo):

        try:
            self.cur.execute(
                '''UPDATE ALERTA SET id=?, nome=? WHERE rowid=?''', (nome, sexo, rowid))
        except Exception as e:
            print('\n[x] Falha na alteração do registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro alterado com sucesso [!]\n')

    def remover_registro(self, rowid):
        """Remove uma linha da tabela com base na id da linha.
        :param rowid (id): id da linha que se deseja remover.
        """
        try:
            self.cur.execute(
                f'''DELETE FROM ALERTA WHERE rowid=?''', (rowid,))
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            self.con.rollback()
        else:
            self.con.commit()
            #print('\n[!] Registro removido com sucesso [!]\n')

    def remover_registros(self):
        """Remove uma linha da tabela com base na id da linha.
        :param rowid (id): id da linha que se deseja remover.
        """
        try:
            self.cur.execute(
                f'''DELETE FROM ALERTA''')
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
            self.con.rollback()
        else:
            self.con.commit()
            #print('\n[!] Registro removido com sucesso [!]\n')


if __name__ == '__main__':
    # Dados
    usuario = ('Cetoprofeno')
    usuarios = [(1,'Cetoprofeno'), (2,'Proflox')]

    # Criando a conexão com o banco.
    banco = ConectarDB()

    # Inserindo um registro tabela.
    #banco.inserir_registro(usuario=usuario)

    # Inserindo vários registros na tabela.
    #banco.inserir_varios_registros(usuarios=usuarios)

    # Consultando com filtro.
    # print(banco.consultar_registro_pela_id(rowid=1))

    # Consultando todos (limit=10).
    # print(banco.consultar_registros())

    # Alterando registro da tabela.
    # Antes da alteração.
    # print(banco.consultar_registro_pela_id(rowid=1))
    # Realizando a alteração.
    # banco.alterar_registro(rowid=1, nome='Rafaela', sexo='Feminino')
    # Depois da alteração.
    # print(banco.consultar_registro_pela_id(rowid=1))

    # Removendo registro da tabela.
    # Antes da remoção.
    print(banco.consultar_alerta())
    # Realizando a remoção.
    #banco.remover_registros()
    # banco.remover_registro(rowid=1)
    # Depois da remoção.
    # print(banco.consultar_registros())