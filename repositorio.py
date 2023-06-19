from flask import jsonify
import sqlite3
import os


caminho = f"{os.path.dirname(__file__)}\\db\\produtos.db"

#id generator
def gerar_id():
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='produtos'")
    id = cursor.fetchone()[0]
    conn.close()
    return id + 1

#create
def criar_produto(nome:str, descricao:str, preco:float, imagem:str):
    try:
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        sql_insert = "INSERT INTO produtos (nome_produto, descricao_produto, preco_produto, imagem_produto) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (nome, descricao, preco, imagem))
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return id
    except Exception as ex:
        print(ex)
        return 0

#update
def atualizar_produto(id:int, nome:str, descricao:str, preco:float, imagem:str):
    try:
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        sql_update = "UPDATE produtos SET nome_produto = ?, descricao_produto = ?, preco_produto = ?, imagem_produto = ? WHERE id_produto = ?"
        cursor.execute(sql_update, (nome, descricao, preco, imagem, id))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False
    
#delete
def remover_produto(id:int):
    try:
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        sql_delete = "DELETE FROM produtos WHERE id_produto = ?"
        cursor.execute(sql_delete, (id, ))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False

#read
def retornar_produto(id:int) -> tuple: 
    try:
        if id == 0:
            return gerar_id(), "", "", "", ""
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        sql_select = "SELECT * FROM produtos WHERE id_produto = ?"
        cursor.execute(sql_select, (id, ))
        id, nome, descricao, preco, imagem = cursor.fetchone()
        
        
        produto ={'id':id, 'nome':nome, 'descricao':descricao, 'preco':preco, 'imagem':imagem}
        conn.close()
        print(produto)
        return jsonify(produto)
    except Exception as ex:
        print(ex)
        return False

def retornar_produtos() -> list:
    try:
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        sql_select = "SELECT * FROM produtos"
        cursor.execute(sql_select)
        dados = cursor.fetchall()
        conn.close()
        produtos = []
        for item in dados:
            produto = {}
            produto['id'] = item[0]
            produto['nome'] = item[1]
            produto['descricao'] = item[2]
            produto['preco'] = item[3]
            produto['imagem'] = item[4]
            produtos.append(produto)
            print(produtos)
            print(type(produtos))   
        return jsonify(produtos)
    except Exception as ex:
        print(ex)
        return False



