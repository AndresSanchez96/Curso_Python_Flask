from flask import Flask, render_template, url_for, redirect, jsonify, request, session
from werkzeug.exceptions import abort

app = Flask(__name__)

app.secret_key = 'Mi_llave_secreta'


# La ruta que estamos declarando es:
# http://localhost:5000/
# para ejcutar en modo de desarrollo es (terminal):
# set FLASK_APP = app.py
# set FLASK_ENV=development
@app.route('/')
def inicio():
    if 'username' in session:
        return f'El usuario {session["username"]} ha hecho login'
    # app.logger.info('Mensaje a nivel info')
    return 'No ha hecho login...'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Omitamos validacion de usuario y password
        usuario = request.form['username']
        # Agregamos el usuario a la sesion
        session['username'] = usuario
        # session['username'] = request.form['username']
        return redirect(url_for('inicio'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('inicio'))


@app.route('/saludar/<nombre>')
def saludar(nombre):
    return f'Saludos {nombre}'


@app.route('/edad/<int:edad>')
def mostrar_edad(edad):
    return f'Tu edad es: {edad}'


@app.route('/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_nombre(nombre):
    return render_template('mostrar.html', nombre=nombre)


@app.route('/redireccionar')
def redireccionar():
    return redirect(url_for('mostrar_nombre', nombre='Andres'))


@app.route('/salir')
def salir():
    return abort(404)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error_404.html', error=error), 404


# REST codigo JSON
@app.route('/api/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_json(nombre):
    valores = {'nombre': nombre, 'method_http': request.method}
    return jsonify(valores)


if __name__ == '__main__':
    app.run(debug=True)
