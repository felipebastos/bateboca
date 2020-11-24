from flask import current_app as app, render_template

@app.route('/')
def inicio():
    return render_template('filha.html')
    
@app.route('/dois')
def dois():
    return render_template('filha2.html')

    
    
    
    
