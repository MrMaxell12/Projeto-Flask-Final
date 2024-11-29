from app import db

class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    codigo_barras = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
