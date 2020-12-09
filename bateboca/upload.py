# Neste arquivo apenas replico adaptando o tutorial de upload
# da documentação oficial.

import os

from werkzeug.utils import secure_filename

from flask import Blueprint, current_app as app, render_template, request, redirect, session, send_from_directory

from bateboca import db
from bateboca.entidades import Usuario

from flask_login import login_required


bp = Blueprint('upload', __name__, url_prefix='/upload')


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/imagens/<path:filename>')
@login_required
def base_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@bp.route('/')
@login_required
def upload():
    imgs = os.listdir(app.config['UPLOAD_FOLDER'])
    print(f'Arquivos no servidor: {len(imgs)}')
    return render_template('upload.html', imagens=imgs)
      
@bp.route('/file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        session['mensagem'] = 'Não havia arquivo no envio'
        return redirect('/upload')
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        session['mensagem'] = 'Não havia arquivo para upload'
        return redirect('/upload')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        imgs = os.listdir(app.config['UPLOAD_FOLDER'])
        filename = f'{len(imgs)+1:08}.{filename.rsplit(".", 1)[1].lower()}'
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        id = request.form['id']
        quem = Usuario.query.get(id)
        quem.profile_img = filename
        db.session.add(quem)
        db.session.commit()
        return redirect('/upload')
    return redirect('/upload')
