class Usuario:
    def __init__(self, id, nombre, email, password, foto_perfil=None, is_active=True, is_staff=False, is_superuser=False):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.foto_perfil = foto_perfil  
        self.is_active = is_active
        self.is_staff = is_staff
        self.is_superuser = is_superuser
