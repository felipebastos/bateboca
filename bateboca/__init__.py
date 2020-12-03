from flask import Flask
import click
import os

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

# banco+driver://usuario:senha@servidor:porta_tcp/banco_criado_no_servidor

# sqlite:///bateboca.db

db = SQLAlchemy()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '123456'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path,'bateboca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    app.cli.add_command(init_db_command)
    
    with app.app_context():
        from . import routes
    return app

@click.command('init-db')
@with_appcontext
def init_db_command():
    from . import entidades
    db.create_all()
    click.echo('Criei o banco com sucesso.')

