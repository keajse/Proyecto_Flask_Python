import re
from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect

from .models.ModeloLibro import ModeloLibro
from .models.entities.Usuario import Usuario
from .models.ModeloUsuario import ModeloUsuario

app = Flask(__name__)

csrf = CSRFProtect()
db= MySQL(app)

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
        usuario= Usuario(None, request.form['usuario'], request.form['password'], None)
        logeado = ModeloUsuario.login(db, usuario)
        if logeado:        
       # print(request.form['usuario'])
       # print(request.form['password'])
            return redirect(url_for('index'))
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

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
    


def pagina_no_encontrada(error):
    return render_template('errores/404.html'),404

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
