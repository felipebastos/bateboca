from flask import current_app as app, render_template, request, redirect, session

from datetime import datetime

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
    
    if nome_da_pessoa in usuarios:
        if senha == usuarios[nome_da_pessoa]:
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
    nome = request.form['n_user']
    senha = request.form['pass_user']
    s_conf = request.form['pass_user_conf']
    
    if nome in usuarios:
        session['mensagem'] = 'Usuário já cadastrado.'
        return redirect('/cadastro')
    else:
        if senha != s_conf:
            session['mensagem'] = 'Senhas não conferem.'
            return redirect('/cadastro')
        else:
            usuarios[nome] = senha
    if 'mensagem' in session:
        del session['mensagem']
    return redirect('/login')
    
@app.route('/baterboca', methods=['POST'])
def baterboca():
    comentario = request.form['comentario']
    
    discussao[datetime.now()] = {'nome':session['user_name'], 'fala':comentario}
    
    return redirect('/mural')
    
