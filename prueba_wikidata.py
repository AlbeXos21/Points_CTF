from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

client = MongoClient(f'{app.config['MONGO_URI']}',server_api=ServerApi('1'))
db = client['PointsCTF']
collection = db['PointsCTF']


@app.route('/', methods=['GET'])
def hello():
   return f"Hola guapo"


@app.route('/insertar', methods=['POST'])
def insertar():
    data = request.json  # Obtener JSON enviado
    if data:
        # Insertar datos en MongoDB
        result = collection.insert_one(data)
        return jsonify({"mensaje": "Datos insertados con éxito", "id": str(result)})
    else:
        return jsonify({"error": "No se enviaron datos"}), 400


@app.route('/insertar_muchos', methods=['POST'])
def insertar_muchos():
    data = request.json  # Obtener JSON enviado
    if data:
        # Insertar datos en MongoDB
        result = collection.insert_many(data)
        return jsonify({"mensaje": "Datos insertados con éxito", "id": str(result)})
    else:
        return jsonify({"error": "No se enviaron datos"}), 400


@app.route('/id/', methods=['GET'])
def obtener_datos():
    elementos = list(collection.find())
    for elemento in elementos:
        elemento['_id'] = str(elemento['_id'])  # Convertir ObjectId a string
    return jsonify(elementos)
   
@app.route('/id/buscar', methods=['GET'])
def buscar_por_id():
    try:
        # Obtener el valor del campo a buscar (por ejemplo, nombre)
        nombre = request.args.get('id')  # Usar /usuarios/buscar?id=Jesús
        if not nombre:
            return jsonify({"error": "El campo 'id' es obligatorio"}), 400
        
        # Buscar por el campo 'nombre'
        documento = collection.find_one({"id": nombre})
        
        # Verificar si se encontró el documento
        if documento:
            documento['_id'] = str(documento['_id'])  # Convertir ObjectId a string
            return jsonify(documento)
        else:
            return jsonify({"error": "No se encontró ningún elemento con esa id"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500