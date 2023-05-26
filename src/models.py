from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

 # def __repr__(self):
    #     return '<Usuario %r>' % self.id

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         # do not serialize the password, its a security breach
    #     }


class Usuario(db.Model):
    #__tablename__ = 'usuario'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
         return '<Usuario %r>' % self.id

    def serialize(self):
         return {
             "id": self.id,
             "nombre": self.nombre,
             "apellido": self.apellido,
             "email": self.email,
             "password":self.password,
             # do not serialize the password, its a security breach
         }
    

class Personas(db.Model):
    #      __tablename__ = 'personas' 
    #     # Here we define columns for the table person
    #      # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), unique=True, nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    year_nacimiento = db.Column(db.String(10), nullable=False)
    color_de_ojos = db.Column(db.String(20), nullable=False)
    color_de_piel = db.Column(db.String(20), nullable=False)
    color_de_pelo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    # personas = db.relationship('Favoritos_personas', backref='personas', lazy=True)

     
    def __repr__(self):
        return '<Personas %r>' % self.id

    def serialize(self):
        return {
             "id": self.id,
             "nombre": self.nombre,
             "genero": self.genero,
             "year_nacimiento": self.year_nacimiento,
             "color_de_ojos":self.color_de_ojos,
             "color_de_piel":self.color_de_piel,
             "color_de_pelo":self.color_de_pelo,
             "peso":self.peso,
             "altura":self.altura,
             # do not serialize the password, its a security breach
         }

class Planetas(db.Model):
#     __tablename__ = 'planetas' 
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), unique=True, nullable=False)
    diametro = db.Column(db.Integer, nullable=False)
    periodo_rotacion = db.Column(db.Integer, nullable=False)
    periodo_orbital = db.Column(db.Integer, nullable=False)
    gravedad = db.Column(db.String(60), nullable=False)
    poblacion = db.Column(db.Integer, nullable=False)
    clima = db.Column(db.String(80), nullable=False)
    terreno = db.Column(db.String(100), nullable=False)
    superficie_liquida = db.Column(db.Integer, nullable=False)
    # planetas = db.relationship('Favoritos_planetas', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
         return {
             "id": self.id,
             "nombre": self.nombre,
             "diametro": self.diametro,
             "periodo_rotacion": self.periodo_rotacion,
             "periodo_orbital":self.periodo_orbital,
             "gravedad":self.gravedad,
             "poblacion":self.poblacion,
             "clima":self.clima,
             "terreno":self.terreno,
             "superficie_liquida ":self.superficie_liquida ,
             # do not serialize the password, its a security breach
         }    


class Vehiculos(db.Model):
#     __tablename__ = 'vehiculos' 
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), unique=True, nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    clase = db.Column(db.String(120), nullable=False)
    constructor = db.Column(db.String(120), nullable=False)
    coste = db.Column(db.Integer, nullable=False)
    longitud = db.Column(db.Integer, nullable=False)
    tripulacion = db.Column(db.Integer, nullable=False)
    pasajeros = db.Column(db.Integer, nullable=False)
    velocidad_maxima = db.Column(db.Integer, nullable=False)
    capacidad_carga = db.Column(db.Integer, nullable=False)
    provisiones = db.Column(db.String(100), nullable=False)
    # vehiculos = db.relationship('Favoritos_vehiculos', backref='vehiculos', lazy=True)


    def __repr__(self):
        return '<Vehiculos %r>' % self.id

    def serialize(self):
            return {
                "id": self.id,
                "nombre": self.nombre,
                "modelo": self.modelo,
                "clase": self.clase,
                "constructorl":self.constructor,
                "coste":self.coste,
                "longitud":self.longitud,
                "tripulacion":self.tripulacion,
                "pasajeros":self.pasajeros,
                "velocidad_maxima":self.velocidad_maxima,
                "capacidad_carga":self.capacidad_carga,
                "provisiones":self.provisiones,
                # do not serialize the password, its a security breach
            }        
    

# class Favoritos_personas(db.Model):
#     __tablename__ = 'favoritos_personas' 
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(db.Integer, primary_key=True)
#     usuario_id = db.Column(db.Integer, nullable=False)
#     personas_id = db.Column(db.Integer, nullable=True)
#     usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
#     personas_id = db.Column(db.Integer, ForeignKey('personas.id'))

# class Favoritos_planetas(db.Model):
#     __tablename__ = 'favoritos_planetas' 
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(db.Integer, primary_key=True)
#     usuario_id = db.Column(db.Integer, nullable=False)
#     planetas_id = db.Column(db.Integer, nullable=True)
#     usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
#     planetas_id = db.Column(db.Integer, ForeignKey('planetas.id'))

#    class Favoritos_vehiculos(db.Model):
#     __tablename__ = 'favoritos_vehiculos' 
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#    id = db.Column(db.Integer, primary_key=True)
#    usuario_id = db.Column(db.Integer, nullable=False)
#     vehiculos_id = db.Column(db.Integer, nullable=True)
#     # 
####    vehiculos_id = db.Column(db.Integer, ForeignKey('vehiculos.id'))
#     usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))


   