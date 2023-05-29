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
from models import db, Usuario #aqui exportar los modelos.
#from models import Person

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


@app.route('/user', methods=['GET'])
def handle_usuario():
    results = Usuario.query.all()
    usuarios_list = list(map(lambda item: item.serialize(),results ))

    response_body = {
         "results": usuarios_list
    }

    return jsonify(response_body), 200


@app.route('/user/<int:id>', methods=['GET'])
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



@app.route('/user', methods=['POST'])
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
