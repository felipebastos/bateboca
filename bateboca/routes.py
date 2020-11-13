from flask import current_app as app, render_template

@app.route('/')
def inicio():
    return render_template('index.html')
    
@app.route('/e_aih')
def eaih():
    return 'Abestadoh!'
