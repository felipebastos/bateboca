from flask import Flask
import click

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy

# banco+driver://usuario:senha@servidor:porta_tcp/banco_criado_no_servidor

# http://200.200.200.200:80/cadastro

# mysql://admin:admin@192.0.0.3:1340/biblioteca

# sqlite:///bateboca.db

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = '123456'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bateboca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
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

