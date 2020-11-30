from bateboca import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(1000), nullable=False)
    
    postagens = db.relationship('Postagem', backref='usuario', lazy=True)
    
class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(140), nullable=False)
    dia = db.Column(db.DateTime, default=datetime.now)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
