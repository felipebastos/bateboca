from flask import Flask
import click
import os

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

# banco+driver://usuario:senha@servidor:porta_tcp/banco_criado_no_servidor

# sqlite:///bateboca.db

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Nunca torne sua secret_key pública num repositório
    # deixei o default aqui apenas para simplificar
    # demonstraçoes do projeto, já que não é algo
    # comercialmente sério.
    app.secret_key = os.getenv('SECRET_KEY', default='123456')
    
    # Também não deixe ir para repositório público
    # a URI de seus bancos, e muito menos dados de login
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path,'bateboca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Diretório da instância onde colocaremos os
    # arquivos de upload dos usuários.
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path,'uploads')

    # Iniciando as extensões e plugins
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Registro de comandos
    app.cli.add_command(init_dirs_command)
    app.cli.add_command(init_db_command)
    
    # Registro de rotas e blueprints
    with app.app_context():
        from . import routes
        from . import upload
        app.register_blueprint(upload.bp)
    return app

@click.command('init-db')
@with_appcontext
def init_db_command():
    from . import entidades
    db.create_all()
    click.echo('Criei o banco com sucesso.')

@click.command('init-dirs')
@with_appcontext
def init_dirs_command():
    app = create_app()
    try:
        os.makedirs(app.instance_path)
        click.echo('Diretório de instância criado.')
    except OSError:
        click.echo('Diretório de instância já existia.')
        pass
    
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
        click.echo('Diretório de upload criado.')
    except OSError:
        click.echo('Diretório de upload já existia.')
        pass

