#!venv/bin/python
from flask import Flask, request, abort, jsonify
# from models import Assembly, Part
import json
import requests
app = Flask(__name__)

# List of physical parts
bills_of_materials = [
    {
        'id': 1,
        'name': 'pen assembly',
        'color': 'red',
        'model': 'metal barrel',
        'parent_id': 'None',
        'children': [],
        'is_subassembly': False,
    },
    {
        'id': 2,
        'name': 'pen assembly',
        'color': 'blue',
        'model': 'plastic barrel',
        'parent_id': 'None',
        'children': [],
        'is_subassembly': False,
    },
    {
        'id': 3,
        'name': 'pen assembly',
        'color': 'green',
        'model': 'plastic barrel',
        'parent_id': 'None',
        'children': [],
        'is_subassembly': False,
    },
    {
        'id': 4,
        'name': 'pen assembly',
        'color': 'gold',
        'model': 'plastic barrel',
        'parent_id': 'None',
        'children': [5,6],
    },
    {
        'id': 5,
        'name': 'top barrel assembly',
        'color': 'gold',
        'model': 'plastic barrel',
        'parent_id': 'None',
        'children': [],
        'is_subassembly': False,
    },
    {
        'id': 6,
        'name': 'pocket clip',
        'color': 'gold',
        'model': 'plastic barrel',
        'parent_id': 5,
        'children': [],
        'is_subassembly': True,
    },
    
    
]

def find_part(part_id):
    return [part for part in bills_of_materials if part['id'] == part_id]

@app.route('/')
def index():
    return "Index"

@app.route('/create/', methods=['GET', 'POST'])
def create_part():
    if not request.json:
        print("Not JSON")
        abort(400)

    for column in ['name', 'color', 'model']:
        if column not in request.json:
            print(column + " not in json")
            abort(400)

    if 'parent_id' not in request.json:
        request.json['parent_id'] = None
    if 'children' not in request.json:
        request.json['children'] = []

    part = {
        'id': bills_of_materials[-1]['id'] + 1,
        'name': request.json['name'],
        'color': request.json['color'],
        'model': request.json['model'],
        'parent_id': request.json['parent_id'],
        'children': request.json['children'],
        'is_subassembly': False,
        }
    bills_of_materials.append(part)
    return jsonify(part), 201

@app.route('/delete/<int:part_id>/', methods=['DELETE'])
def delete_part(part_id):
    delete_part = find_part(part_id)
    if len(delete_part) == 0:
        abort(404)
    bills_of_materials.remove(delete_part[0])
    return jsonify({'result': True})

@app.route('/update/<int:part_id>/', methods=['PUT'])
def update_part(part_id):
    old_part = find_part(part_id)
    if len(old_part) != 1 or not request.json:
        abort(404)
    bills_of_materials.remove(old_part[0])
    update_part = {
        'id': old_part['id'],
        'name': request.json['name'] if 'name' in request.json else old_part['name'],
        'color': request.json['color'] if 'color' in request.json else old_part['color'],
        'model': request.json['model'] if 'model' in request.json else old_part['model'],
        'parent_id': request.json['parent_id'] if 'parent_id' in request.json else old_part['parent_id'],
        'children': request.json['children'] if 'children' in request.json else old_part['children'],
        'is_subassembly': request.json['is_subassembly'] if 'is_subassembly' in request.json else old_part['is_subassembly'],
    }
    bills_of_materials.add(update_part)
    return jsonify({'result': True})



### GET Routes ###

@app.route('/bom/', methods=['GET'])
def get_parts():
    # parts.append(part.to_json())
    return jsonify({'bills_of_materials': bills_of_materials}), 201

@app.route('/assemblies/<int:part_id>/', methods=['GET'])
def get_assemblies(part_id):
    
    parts.append(part.to_json())
    return jsonify({'part': part}), 201

@app.route('/toplevel/', methods=['GET'])
def get_toplevel():
    top_assems = []
    for part in bills_of_materials:
        if part["parent_id"] is None:
            top_assems.append(part)
    return jsonify({'top_level_assemblies': top_assems}), 201

@app.route('/subassems/', methods=['GET'])
def get_subassems():
    subassems = []
    for part in bills_of_materials:
        if part["parent_id"] is not None:
            subassems.append(part)
    return jsonify({'sub_assemblies': subassems}), 201

@app.route('/components/', methods=['GET'])
def get_components():
    part = []
    parts.append(part.to_json())
    return jsonify({'part': part}), 201

@app.route('/orphans/', methods=['GET'])
def get_orphans():
    orphan_parts = []
    for part in bills_of_materials:
        if part['parent_id'] is None and part['children'] == []:
            orphan_parts.append(part)
    return jsonify({'orphan_parts': orphan_parts}), 201

@app.route('/first_children/', methods=['GET'])
def get_first_children():
    first_children = []
    for part in bills_of_materials:
        parent_id = part['parent_id']
        if parent_id is not None and find_part(parent_id)['parent_id'] is None:
            first_children.append(part)
    return jsonify({'first_level_children': first_children}), 201



if __name__ == '__main__':
    app.run(debug=True)

