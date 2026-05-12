from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from datos import reglas, evaluacion, habilidades, fechas_clave
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta'
secciones = ["reglas", "evaluacion", "habilidades"]
contenido = {"reglas": reglas, "evaluacion": evaluacion, "habilidades": habilidades}

@app.route('/')
def index():
    session.clear()
    session['desbloqueadas'] = []
    session['quiz_pasados'] = {}
    return render_template('index.html')

@app.route('/seleccionar_preguntas/<seccion>')
def seleccionar_preguntas(seccion):
    banco = contenido[seccion]['banco_preguntas']
    seleccionadas = random.sample(banco, 2) if len(banco) >= 2 else banco
    session[f'preguntas_{seccion}'] = seleccionadas
    return jsonify([{'pregunta': p['pregunta'], 'tipo': p['tipo'], 'opciones': p.get('opciones', [])} for p in seleccionadas])

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', desbloqueadas=session.get('desbloqueadas', []), secciones=secciones)

@app.route('/calabozo/<seccion>', methods=['GET', 'POST'])
def calabozo(seccion):
    import random
    if seccion not in secciones:
        return redirect(url_for('mapa'))
    idx = secciones.index(seccion)
    if idx > 0 and secciones[idx-1] not in session.get('desbloqueadas', []):
        flash('Debes desbloquear la sección anterior', 'error')
        return redirect(url_for('mapa'))
    ya_desbloqueada = seccion in session.get('desbloqueadas', [])
    data = contenido[seccion]
    preguntas = session.get(f'preguntas_{seccion}', [])
    if request.method == 'POST':
        if not ya_desbloqueada:
            if session.get('quiz_pasados', {}).get(f'{seccion}_quiz', False):
                if request.form.get('compromiso') == 'on':
                    session.setdefault('desbloqueadas', []).append(seccion)
                    flash(f'¡{seccion} desbloqueada!', 'success')
                    return redirect(url_for('mapa'))
            else:
                flash('Primero debes responder las preguntas', 'error')
        return redirect(url_for('calabozo', seccion=seccion))
    quiz_pasado = session.get('quiz_pasados', {}).get(f'{seccion}_quiz', False)
    return render_template('calabozo.html', seccion=seccion, titulo=data['titulo'], contenido=data['contenido'], preguntas=preguntas, quiz_pasado=quiz_pasado, ya_desbloqueada=ya_desbloqueada)

if __name__ == '__main__':
    app.run(debug=True)
