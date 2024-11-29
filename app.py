from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dynaconf

app = Flask(__name__)
settings = dynaconf.FlaskDynaconf(
    app,
    settings_files=["settings.toml", ".secrets.toml"],
)
db = SQLAlchemy()

db.init_app(app)
from routes import *  # Importa o módulo de rotas


if __name__ == "__main__":
    app.run(debug=True)


