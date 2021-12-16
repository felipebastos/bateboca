from flask import current_app as app, render_template, request, redirect, session

import math

from functools import wraps

from datetime import datetime

from bateboca import db, bcrypt, login_manager
from bateboca.entidades import Usuario, Postagem

from flask_login import login_user, logout_user, login_required, current_user

#usuarios = {'felipebastos': '123456'}
#discussao = {}

login_manager.login_view = '/login'

@app.route('/teste_db')
def teste_db():
    postagens = Postagem.query.join(Usuario).filter_by(Usuario.id == Postagem.usuario_id).all()

    print(postagens[0])
    return 'ok'

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
    

@app.route('/mural')
@login_required
def mural():
    discussao = {}
    postagens = Postagem.query.all()
    for post in postagens:
        quem = Usuario.query.get(post.usuario_id)
        discussao[post.dia] = {'nome': quem.nome, 'fala': post.texto}
    return render_template('feed.html', d=discussao)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect('/')

def role(role):
    def decorator(function):
        @wraps(function)
        def wrapper():
            if current_user.role == role:
                return function()
            else:
                return 'erro', 404
        return wrapper
    return decorator


@app.route('/segredo')
@login_required
@role(role='admin')
def teste_soh_admin():
    if current_user.role == 'admin':
        return 'beleza'
    else:
        return 'Você não tem autorização para vir aqui', 403


@app.route('/logar', methods=['POST'])
def logar():
    nome_da_pessoa = request.form['n_user']
    senha = request.form['pass_user']
    
    alguem = Usuario.query.filter_by(nome=nome_da_pessoa).first()
    
    if alguem is not None:
        if bcrypt.check_password_hash(alguem.senha, senha):
            login_user(alguem)
            session['user_name'] = nome_da_pessoa
            if 'mensagem' in session:
                del session['mensagem']
            return redirect('/mural')
        else:
            session['mensagem'] = 'Senha inválida!'
            return redirect('/login')
    else:
        session['mensagem'] = 'Usuário inexistente!'
        return redirect('/login')

    
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_c = request.form['n_user']
    senha = request.form['pass_user']
    s_conf = request.form['pass_user_conf']
    
    alguem = Usuario.query.filter_by(nome=nome_c).first()
    
    if alguem is not None:
        session['mensagem'] = 'Usuário já cadastrado.'
        return redirect('/cadastro')
    else:
        if senha != s_conf:
            session['mensagem'] = 'Senhas não conferem.'
            return redirect('/cadastro')
        else:
            # usuarios[nome] = senha
            novo = Usuario()
            novo.nome = nome_c
            
            senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
            
            novo.senha = senha_hash
            
            db.session.add(novo)
            db.session.commit()
            
    if 'mensagem' in session:
        del session['mensagem']
    return redirect('/login')
    
@app.route('/baterboca', methods=['POST'])
def baterboca():
    comentario = request.form['comentario']
    
    #discussao[datetime.now()] = {'nome':session['user_name'], 'fala':comentario}
    quem = Usuario.query.filter_by(nome=session['user_name']).first()
    
    post = Postagem()
    post.texto = comentario
    post.usuario_id = quem.id
    
    db.session.add(post)
    db.session.commit()
    
    return redirect('/mural')
    
    
@app.route('/remove/<int:id>')
def remove(id):
    quem = Usuario.query.get(id)
    db.session.delete(quem)
    db.session.commit()
    return 'Removi o usuário {}'.format(quem.nome)
    
@app.route('/atualiza/<int:id>/<nomeNovo>')
def atualiza(id, nomeNovo):
    quem = Usuario.query.get(id)
    quem.nome = nomeNovo
    db.session.add(quem)
    db.session.commit()
    
    return redirect('/')
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)
    
# Exemplo para a Lara
lojas = {'chico': {'lat': -3.7556750000000002, 'lon': -38.5150646, 'area': 10.0, 'ocupacao': 0}}

@app.route('/usuario')
def usuario():
    return render_template('feed_lara.html')

@app.route('/checkin', methods=['POST'])
def checkin():
    lat = float(request.form['lat'])*math.pi/180
    lon = float(request.form['lon'])*math.pi/180
    loja = request.form['loja']
    
    print(loja)
    print(lat)
    print(lon)
    
    l_cad = lojas[loja]
    
    l_lat = l_cad['lat']*math.pi/180
    l_lon = l_cad['lon']*math.pi/180
    l_a = l_cad['area']

    raio = math.sqrt(l_a/math.pi)
    
    # dist**2 = c1**2 + c2**2
    deltaLng = l_lon - lon

    s = math.cos(math.pi/2 - l_lat)*math.cos(math.pi/2 - lat) + math.sin(math.pi/2 - l_lat)*math.sin(math.pi/2 - lat)*math.cos(deltaLng)
    arco = math.acos(s)



		# A distância é o arco em radiano vezes o raio da terra (aproximado).
    distancia = arco*6378*1000
    
    
    #dist = math.sqrt((l_lat - lat)**2 + (l_lon - lon)**2)
    
    if distancia <= raio:
        l_cad['ocupacao'] += 1
        return "Dentro"
    else:
        # o cliente não está na loja
        return "Fora. Distância: {} metros. Raio: {} metros".format(distancia, raio)
    
    return 'Você está na loja {}'.format(loja)

