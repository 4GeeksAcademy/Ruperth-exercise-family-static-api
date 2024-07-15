import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json
    member = jackson_family.add_member(new_member)
    if member:
        return jsonify({'msg': 'Nuevo miembro añadido a la familia'}), 201
    return jsonify({'error': 'Error al añadir el miembro'}), 400  

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted_member = jackson_family.delete_member(member_id)
    if deleted_member:
        return jsonify({'msg': 'Miembro eliminado de la familia'}), 200
    return jsonify({'error': 'No se ha podido eliminar el miembro'}), 404

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)