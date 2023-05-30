"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os , json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Personas,Planetas,Favoritos_personas,Favoritos_planetas,Favoritos_vehiculos #aqui exportar los modelos.

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#empieza aqui los ENDPOINTs

@app.route('/persona', methods=['GET'])
def handle_personas():
    results = Personas.query.all()
    personas_list = list(map(lambda item: item.serialize(),results ))

    response_body = {
        "results": personas_list
    }

    return jsonify(response_body), 200


@app.route('/persona/<int:id>', methods=['GET'])
def get_persona(id): 

    persona = Personas.query.filter_by(id=id).first()
    response_body = {}
   
    if persona == None: 

        response_body["msg"] = "La persona no existe"
        return jsonify(response_body), 404

    response_body = {
         
        "result": persona.serialize(),
        "msg":  "ok"
    }

    return jsonify(response_body), 200 

@app.route('/planeta', methods=['GET'])
def handle_planetas():
    results = Planetas.query.all()
    planetas_list = list(map(lambda item: item.serialize(),results )),

    response_body = {
         "results": planetas_list
    }

    return jsonify(response_body), 200


@app.route('/planeta/<int:id>', methods=['GET'])
def get_planeta(id): 

    planeta = Planetas.query.filter_by(id=id).first()
    response_body = {}
   
    if planeta == None: 

        response_body["msg"] = "El planeta no existe"
        return jsonify(response_body), 404

    response_body = {
         
        "result": planeta.serialize(),
        "msg":  "ok"
    }
    return jsonify(response_body), 200 

@app.route('/usuario', methods=['GET'])
def handle_usuario():
    results = Usuario.query.all()
    usuarios_list = list(map(lambda item: item.serialize(),results))

    response_body = {
         "results": usuarios_list
    }

    return jsonify(response_body), 200

@app.route('/usuario/favoritos', methods=['GET'])
def handle_usuario_favoritos():
    results1 = Favoritos_personas.query.all()
    favoritos_personas_list = list(map(lambda item: item.serialize(),results1 ))
    
    results2 = Favoritos_planetas.query.all()
    favoritos_planetas_list = list(map(lambda item: item.serialize(),results2 ))

    results3 = Favoritos_vehiculos.query.all()
    favoritos_vehiculos_list = list(map(lambda item: item.serialize(),results3 ))

    response_body = {
        "results": favoritos_personas_list + favoritos_planetas_list + favoritos_vehiculos_list
    }

    return jsonify(response_body), 200

# EndPoint creacion de planeta favoritos para un usuario
@app.route('/favorito/planeta/<int:planetas_id>/<int:usuario_id>', methods=['POST'])
def create_planeta_favorito(planetas_id,usuario_id):

    planeta_favorito = Favoritos_planetas.query.filter_by(planetas_id=planetas_id).first()
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    response_body = {}

    if usuario is None:

        response_body["msg"] = "El usuario no existe"
        return jsonify(response_body), 404
   
    if planeta_favorito: 

        response_body["msg"] = "El planeta ya era favorito"
        return jsonify(response_body), 208
    


    favorito_planeta = Favoritos_planetas(usuario_id=usuario_id, planetas_id=planetas_id)
    db.session.add(favorito_planeta)
    db.session.commit()
    
    response_body["msg"] = "El planeta ahora es favorito"

    return jsonify(response_body), 200 

# EndPoint creacion de personas favoritos para un usuario, enviando el id del usuario por el body
@app.route('/favorito/personas/<int:personas_id>', methods=['POST'])
def create_persona_favorito(personas_id,):

    body = json.loads(request.data)

    persona_favorito = Favoritos_personas.query.filter_by(personas_id=personas_id).first()
    usuario = Usuario.query.filter_by(id=body["usuario_id"]).first()
    response_body = {}

    if usuario is None:

        response_body["msg"] = "El usuario no existe"
        return jsonify(response_body), 404
   
    if persona_favorito: 

        response_body["msg"] = "La persona ya era favorito"
        return jsonify(response_body), 208
    


    favorito_persona = Favoritos_personas(usuario_id=body["usuario_id"], personas_id=personas_id)
    db.session.add(favorito_persona)
    db.session.commit()
    
    response_body["msg"] = "La persona ahora es favorito"

    return jsonify(response_body), 200 

# EndPoint para borrado de planeta favoritos para un usuario 
@app.route('/favorito/planeta/<int:planetas_id>/<int:usuario_id>', methods=['DELETE'])
def borrar_planeta_favorito(planetas_id,usuario_id):

    planeta_favorito = Favoritos_planetas.query.filter_by(planetas_id=planetas_id).first()
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    response_body = {}

    if usuario is None:

        response_body["msg"] = "El usuario no existe"
        return jsonify(response_body), 404
   
    if planeta_favorito is None:
        response_body["msg"] = "El Planeta no existe"
        return jsonify(response_body), 404

 
    db.session.delete(planeta_favorito)
    db.session.commit()
    
    response_body["msg"] = "El planeta fue borrado"
    return jsonify(response_body), 200

# EndPoint para borrado de personas favoritos para un usuario 
@app.route('/favorito/personas/<int:personas_id>/<int:usuario_id>', methods=['DELETE'])
def borrar_persona_favorito(personas_id,usuario_id):

    persona_favorito = Favoritos_personas.query.filter_by(personas_id=personas_id).first()
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    response_body = {}

    if usuario is None:

        response_body["msg"] = "El usuario no existe"
        return jsonify(response_body), 404
   
    if persona_favorito is None:
        response_body["msg"] = "La persona no existe"
        return jsonify(response_body), 404

 
    db.session.delete(persona_favorito)
    db.session.commit()
    
    response_body["msg"] = "La persona fue borrado"
    return jsonify(response_body), 200



#  Extra ejercicio

@app.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id): 

    usuario = Usuario.query.filter_by(id=id).first()

   
    if usuario == None: 

         response_body = {
             "msg":  "Usuario no existe"
         }

         return jsonify(response_body), 404

    response_body = {
          
        "result": usuario.serialize(),
        "msg":  "ok"
    }

    return jsonify(response_body), 200 

@app.route('/usuario', methods=['POST'])
def create_usuario():

    body = json.loads(request.data)
    response_body={}

    if body == None:
        response_body["msg"] = "No has enviado información."
        return jsonify(response_body), 404
    
    if not "email" in body:
        response_body["msg"] = "La propiedad email no existe, por favor indiquela."
        return jsonify(response_body), 404
    
    email = Usuario.query.filter_by(email=body["email"]).first()
   
    if email != None: 
         response_body["msg"] = "Existe un usuario con este email"
         return jsonify(response_body), 404
    
    if not "nombre" in body:
        response_body["msg"] = "La propiedad nombre no existe, por favor indiquela."
        return jsonify(response_body), 404
    
    if not "apellido" in body:
        response_body["msg"] = "La propiedad apellido no existe, por favor indiquela."
        return jsonify(response_body), 404
    
    if not "password" in body:
        response_body["msg"] = "La propiedad password no existe, por favor indiquela."
        return jsonify(response_body), 404


    usuario = Usuario(nombre=body["nombre"], apellido=body["apellido"], email=body["email"], password=body["password"])
    
    response_body["msg"] = "Usuario creado"
    
    db.session.add(usuario)
    db.session.commit()

    return jsonify(response_body), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
