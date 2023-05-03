from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# configuracion de la base de datos
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Inicializacion del objeto db de sqlalchemy
#db = SQLAlchemy(app)
db.init_app(app)

# Configuracion de flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuramos de flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'

# se crea migrate desde terminal con: flask db init
# flask db migrate y flask db upgrade

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    # Listado de personas
    personas = Persona.query.order_by('id') # consultar y regresa todos los objetos de tipo persona
    total_personas = Persona.query.count() # consulta y retonar el conteo total
    app.logger.debug(f'Listado de personas_ {personas}')
    app.logger.debug(f'Total de personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    # Rucuperamos la persona segun el id proporcionado
    #persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    # para trabajar con formularios flask tiene WTForms que se debe instalar desde terminal
    #python -m pip install flask-wtf
    # se debe configurar una llave secreta para evitar malos usos se hace en el inicio
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a insertar {persona}')
            # insertamos el nuevo registro en la base de datos
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=personaForm)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get_or_404(id) # con esto recuperamos el obj persona a editar
    personaForma = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f'Persona a editar {persona}')
            # editamos registro en la base de datos
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)  # con esto recuperamos el obj persona a editar
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)