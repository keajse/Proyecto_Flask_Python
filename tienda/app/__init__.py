from flask import Flask, render_template, request, redirect, url_for, session, flash
import flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from .models.ModeloLibro import ModeloLibro
from .models.entities.Usuario import Usuario
from .models.ModeloUsuario import ModeloUsuario

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app= LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db,id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    print(request.method)
    print(request.form['usuario'])
    print(request.form['password'])
    """
    
    if request.method == 'POST':
        administrador=request.form['usuario']=='KEAJSE' and request.form['password']=='admin123*'
        invitado=request.form['usuario']=='ADRIANA' and request.form['password']=='123456'
        if administrador:
            #login_user(administrador)
            return redirect(url_for('index'))
        else:
            if invitado:
                #login_user('ADRIANA')
                return redirect(url_for('index'))
            else:  
                flash('Credenciales inválidas')          
                return render_template('auth/login.html')
    else:
        flash('Credenciales inválidas')
        return render_template('auth/login.html')

   
"""
    if request.method == 'POST':
        usuario = Usuario(
           None, request.form['usuario'], request.form['password'], None)
        usuario_logeado= ModeloUsuario.login(db, usuario)

        if usuario_logeado != None:
           return redirect(url_for('index'))
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    """
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/libros')
def listar_libros():
    try:
        libros= ModeloLibro.listar_libros(db)
        data={
            'libros': libros
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        print(ex)

    return render_template('')
    
@app.route('/password/<password>')
def generate_password(password):
    encriptado = generate_password_hash(password)
    coincide= check_password_hash(encriptado, password)
    return "Encriptado:{0} | Coincide: {1}".format(encriptado, coincide)

def pagina_no_encontrada(error):
    return render_template('errores/404.html'),404

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
