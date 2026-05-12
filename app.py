from flask import Flask
app = Flask(__name__)
app.secret_key = 'clave'
@app.route('/')
def index():
    return 'Hola Mundo'
if __name__ == '__main__':
    app.run()
