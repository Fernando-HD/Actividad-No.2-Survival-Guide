from flask import Flask, render_template, session
from datos import reglas, evaluacion, habilidades, fechas_clave

app = Flask(__name__)
app.secret_key = 'clave_secreta'
secciones = ["reglas", "evaluacion", "habilidades"]

@app.route('/')
def index():
    session.clear()
    session['desbloqueadas'] = []
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', desbloqueadas=session.get('desbloqueadas', []), secciones=secciones)

if __name__ == '__main__':
    app.run(debug=True)
