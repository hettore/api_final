from flask import Flask, jsonify, request
import repositorio

app = Flask(__name__)

@app.route("/products", methods=['GET'])
def get_produtos():
    produtos = repositorio.retornar_produtos()
    return produtos, 200

@app.route("/product/<int:id>", methods=['GET'])
def get_produto(id):
    produto = repositorio.retornar_produto(id)
    if produto:
        return produto
    else:
        return jsonify({"message": "Produto não encontrado"}), 404

@app.route("/product", methods=['POST'])
def set_produto():
    produto = request.json
    id = repositorio.criar_produto(**produto)
    if id:
        produto["id"] = id
        return jsonify(produto), 201
    else:
        return jsonify({"message": "não foi possível criar o produto"}), 500

@app.route("/product/<int:id>", methods=['PUT'])
def update_produto(id):
    produto = repositorio.retornar_produto(id)
    if produto:
        dados_atualizados = request.json
        dados_atualizados["id"] = id
        if repositorio.atualizar_produto(**dados_atualizados):
            return jsonify(dados_atualizados), 200
        else:
            return jsonify({"message": "não foi possível atualizar"}), 500
    else:
        return jsonify({"message": "produto não localizado"}), 404
    
@app.route("/product/<int:id>", methods=['DELETE'])
def delete_produto(id):
    produto = repositorio.retornar_produto(id)
    if produto:
        if repositorio.remover_produto(id):
            return jsonify({"message": "produto excluído"}), 200
        else:
            return jsonify({"message": "não foi possível remover o produto"}), 500
    else:
        return jsonify({"message": "produto não localizado"}), 404

app.run(debug=True)