from werkzeug.security import generate_password_hash, check_password_hash

class Usuario():

    def __init__(self, id, usuario, password, tipousuario):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.tipousuario = tipousuario


    def encriptar_password(password):
      
        encriptado = generate_password_hash(password)
        coincide = check_password_hash(encriptado, password)
        return coincide