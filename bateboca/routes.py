from flask import current_app as app, render_template, request, redirect, session

from datetime import datetime

from bateboca import db
from bateboca.entidades import Usuario

usuarios = {'felipebastos': '123456'}
discussao = {}

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
def mural():
    return render_template('feed.html', d=discussao)

@app.route('/logout')
def logout():
    session['user_name'] = 'Visitante'
    return redirect('/')


@app.route('/logar', methods=['POST'])
def logar():
    nome_da_pessoa = request.form['n_user']
    senha = request.form['pass_user']
    
    alguem = Usuario.query.filter_by(nome=nome_da_pessoa).first()
    
    if alguem is not None:
        if senha == alguem.senha:
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
            novo.senha = senha
            
            db.session.add(novo)
            db.session.commit()
            
    if 'mensagem' in session:
        del session['mensagem']
    return redirect('/login')
    
@app.route('/baterboca', methods=['POST'])
def baterboca():
    comentario = request.form['comentario']
    
    discussao[datetime.now()] = {'nome':session['user_name'], 'fala':comentario}
    
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
    

