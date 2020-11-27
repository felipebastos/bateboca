from bateboca import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(1000), nullable=False)
    

