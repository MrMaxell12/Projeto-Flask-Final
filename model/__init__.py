from model.user import *
from app import app
from .product import Produto  # Adicione o modelo Produto

with app.app_context():
    db.create_all()