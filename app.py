from flask import Flask, render_template, session, request, redirect, url_for, flash
from datos import reglas, evaluacion, habilidades, fechas_clave

app = Flask(__name__)
app.secret_key = 'clave_secreta'
secciones = ["reglas", "evaluacion", "habilidades"]
contenido = {"reglas": reglas, "evaluacion": evaluacion, "habilidades": habilidades}

@app.route('/')
def index():
    session.clear()
    session['desbloqueadas'] = []
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', desbloqueadas=session.get('desbloqueadas', []), secciones=secciones)

@app.route('/calabozo/<seccion>', methods=['GET', 'POST'])
def calabozo(seccion):
    if seccion == 'reglas' or secciones[secciones.index(seccion)-1] in session.get('desbloqueadas', []):
        if request.method == 'POST':
            session['desbloqueadas'].append(seccion)
            flash(f'¡{seccion} desbloqueada!', 'success')
            return redirect(url_for('mapa'))
        return render_template('calabozo.html', titulo=contenido[seccion]['titulo'], contenido=contenido[seccion]['contenido'])
    flash('Debes desbloquear la sección anterior', 'error')
    return redirect(url_for('mapa'))

if __name__ == '__main__':
    app.run(debug=True)
