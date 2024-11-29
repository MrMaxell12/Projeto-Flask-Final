from flask import jsonify, request
from model.product import Produto
from app import app, db
from sqlalchemy import asc

print("fungo!")

@app.route("/joao")
def joao():
    return "joao"

@app.route("/produto", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        "id": produto.id,
        "codigo_barras": produto.codigo_barras,
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque,
        "descricao": produto.descricao
    } for produto in produtos])

@app.route("/produto", methods=["POST"])
def criar_produto():
    dados = request.json
    novo_produto = Produto(
        codigo_barras=dados['codigo_barras'],
        nome=dados['nome'],
        preco=dados['preco'],
        estoque=dados['estoque'],
        descricao=dados.get('descricao', '')
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto criado com sucesso"}), 201

@app.route("/produto/<int:id>", methods=["GET"])
def detalhar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({
        "id": produto.id,
        "codigo_barras": produto.codigo_barras,
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque,
        "descricao": produto.descricao
    })

@app.route("/produto/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = request.json
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    produto.codigo_barras = dados['codigo_barras']
    produto.nome = dados['nome']
    produto.preco = dados['preco']
    produto.estoque = dados['estoque']
    produto.descricao = dados.get('descricao', '')
    db.session.commit()
    return jsonify({"mensagem": "Produto atualizado com sucesso"})

@app.route("/produto/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto deletado com sucesso"})

from model.user import User

print("joao?TOMARAQUEFUNGUE")

@app.route("/users", methods=["GET"])
def list_users():
    query_params = request.args

    page = query_params.get('page', default=0, type=int)
    limit = query_params.get('limit', default=10, type=int)
    offset = page * limit

    filter = {}
    ignored_fields = ['page', 'limit', 'sort_by', 'sort_direction']
    for field, value in query_params.items():
        if field not in ignored_fields:
            filter[field] = value

    sort_by = query_params.get('sort_by', default='id', type=str)
    sort_direction = query_params.get('sort_direction', default='asc', type=str)

    order_by = asc(sort_by) if sort_direction == 'asc' else desc(sort_by)

    users = User.query.filter_by(**filter).order_by(order_by).offset(offset).limit(limit).all()
    if not users:
        return jsonify([]), 200

    status_code = 206 if len(users) == limit else 200

    result = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify(result), status_code