#!venv/bin/python
from flask import Flask, request, abort, jsonify
import json
import requests
app = Flask(__name__)

# List of physical parts
bill_of_mats = {
    1: {
        'id': 1,
        'name': 'pen assembly',
        'color': 'red',
        'model': 'metal barrel',
        'parent_ids': None,
        'children': [5, 8],
        'is_subassembly': False,
    },
    2: {
        'id': 2,
        'name': 'pen assembly',
        'color': 'blue',
        'model': 'plastic barrel',
        'parent_ids': None,
        'children': [5, 8],
        'is_subassembly': False,
    },
    3: {
        'id': 3,
        'name': 'pen assembly',
        'color': 'green',
        'model': 'plastic barrel',
        'parent_ids': None,
        'children': [5, 8],
        'is_subassembly': False,
    },
    4: {
        'id': 4,
        'name': 'pen assembly',
        'color': 'gold',
        'model': 'metal barrel',
        'parent_ids': None,
        'children': [5, 8],
    },
    5: {
        'id': 5,
        'name': 'top barrel assembly',
        'color': 'gold',
        'model': 'plastic barrel',
        'parent_ids': 4,
        'children': [6],
        'is_subassembly': True,
    },
    6: {
        'id': 6,
        'name': 'pocket clip',
        'color': 'gold',
        'model': 'plastic barrel',
        'parent_ids': 5,
        'children': [],
        'is_subassembly': False,
    },
    7: {
        'id': 7,
        'name': 'iPhone',
        'color': 'gold',
        'model': 'X',
        'parent_ids': None,
        'children': [],
        'is_subassembly': False,
    },
    8: {
        'id': 8,
        'name': 'bottom barrel assembly',
        'color': 'grey',
        'model': 'polished wood',
        'parent_ids': None,
        'children': [9],
        'is_subassembly': True,
    },
    9: {
        'id': 9,
        'name': 'rubber grip',
        'color': 'gold',
        'model': 'vynaprene',
        'parent_ids': 8,
        'children': [],
        'is_subassembly': False,
    },
    
}

def find_part(part_id):
    """
    This function is defined as an abstraction barrier,
    in case we want to use a different storage object for
    BoM, such as perhaps a read/write database.

    :part_id: the ID of the part specified
    :return: part object specified by part_id, else None if DNE
    """
    return bill_of_mats.get(part_id, None)

def get_bom_max_id():
    """
    This function is defined as an abstraction barrier,
    minimizing the necessary changes if bill_of_mats becomes
    a different type object.

    :return: max ID of "database"
    """
    return max(bill_of_mats.keys())

@app.route('/')
def index():
    return "Index"

### POST Routes ###
@app.route('/create/', methods=['POST'])
def create_part():
    """
    Creating an Assembly JSON object requires at least a name.
    # Name is the only requirement in the JSON, for creating a new Assembly Object.
    # We arbitrarily default to the color "black" and model "default".
    """

    if not request.json or 'name' not in request.json:
        abort(400)

    if 'color' not in request.json:
        request.json['color'] = 'black'
    if 'model' not in request.json:
        request.json['model'] = 'default'
    if 'parent_ids' not in request.json:
        request.json['parent_ids'] = None
    if 'children' not in request.json:
        request.json['children'] = []

    
    new_id = get_bom_max_id(bill_of_mats) + 1
    part = {
        'id': new_id,
        'name': request.json['name'],
        'color': request.json['color'],
        'model': request.json['model'],
        'parent_ids': request.json['parent_ids'],
        'children': request.json['children'],
        'is_subassembly': False,
        }
    bill_of_mats[new_id] = part
    return jsonify(part), 201

### DELETE Routes ###
@app.route('/delete/<int:part_id>/', methods=['DELETE'])
def delete_part(part_id):
    """
    """
    if find_part(part_id) is None:
        abort(404)
    result = bill_of_mats.pop(part_id)
    return jsonify({'Deleted Result': result})

### PUT (Update) Routes ###
@app.route('/update/<int:part_id>/', methods=['PUT'])
def update_part(part_id):
    """
    """
    old_part = find_part(part_id)
    if old_part is None or not request.json:
        abort(404)

    # Updating parent_id and children requires modifying/updating their dependencies.
    # 1) Check that parent ID(s) is/are valid
    # 2) Add the current part to the parent's children
    if 'parent_ids' in request.json:
        new_parent_ids = request.json['parent_ids']
        for parent_id in new_parent_ids:
            if parent_id is None:
                abort(404) # We abort instead of "pass"ing to signify an issue. Consider "pass" for convenience.
            parent = find_part(parent_id)
            parent['children'].append(part_id)
    
    # Updating children means either adding or removing some dependencies
    # All children (add or remove) will need to update their parent id.
    if 'children' in request.json:
        deleted_children = [child_id for child_id in old_part['children'] if child_id not in request.json['children']]
        for child_id in deleted_children:
            find_part(child_id)['parent_ids'] = None
        
        new_children = [child_id for child_id in request.json['children'] if child_id not in old_part['children']]
        for child_id in new_children:
            find_part(child_id)['parent_ids'].append(part_id)

    updated_part = {
        'id': part_id,
        'name': request.json['name'] if 'name' in request.json else old_part['name'],
        'color': request.json['color'] if 'color' in request.json else old_part['color'],
        'model': request.json['model'] if 'model' in request.json else old_part['model'],
        'parent_ids': request.json['parent_ids'] if 'parent_ids' in request.json else old_part['parent_ids'],
        'children': request.json['children'] if 'children' in request.json else old_part['children'],
        'is_subassembly': request.json['is_subassembly'] if 'is_subassembly' in request.json else old_part['is_subassembly'],
    }

    bill_of_mats[part_id] = updated_part
    return jsonify({'result': True})


### GET Routes ###
@app.route('/bom/', methods=['GET'])
def get_bom():
    """
    Returns jsonified list of Bill of Materials (BoM)
    """
    return jsonify({'bill_of_mats': bill_of_mats}), 201

@app.route('/assemblies/', methods=['GET'])
def get_assemblies():
    """
    Gets all assemblies in BoM
    Returns jsonified list of assemblies
    """
    assemblies = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['children'] != []:
            assemblies.append(part)
    return jsonify({'assemblies': assemblies}), 201

@app.route('/toplevel/', methods=['GET'])
def get_toplevel():
    """
    Gets Top-level assemblies (assemblies that are not children of another assembly)
    Returns jsonified list of top-level assemblies
    """
    top_assems = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['parent_ids'] is None and part['children'] != []:
            top_assems.append(part)
    return jsonify({'top_level_assemblies': top_assems}), 201

@app.route('/subassems/', methods=['GET'])
def get_subassems():
    """
    Gets subassemblies
    Returns jsonified list of subassems
    """
    subassems = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['is_subassembly']:
            subassems.append(part)
    return jsonify({'sub_assemblies': subassems}), 201

@app.route('/components/', methods=['GET'])
def get_components():
    """
    Gets components of data
    Returns jsonified list of components
    """
    components = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['parent_ids'] and not part['is_subassembly']:
            components.append(bill_of_mats[part_id])
    return jsonify({'components': components}), 201

@app.route('/orphans/', methods=['GET'])
def get_orphans():
    """
    Gets orphans
    Returns jsonified list of orphans
    """
    orphan_parts = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['parent_ids'] is None and part['children'] == []:
            orphan_parts.append(part)
    return jsonify({'orphan_parts': orphan_parts}), 201

@app.route('/assembly/children/<int:assembly_id>', methods=['GET'])
def get_first_children(assembly_id):
    """
    Gets first children of a specific assembly 
    Returns jsonified list of first_children
    """
    first_children = []
    for part_id in bill_of_mats:
        part = find_part(part_id)
        if part['parent_ids'] == assembly_id:
            first_children.append(part)
    return jsonify({'first_level_children': first_children}), 201

@app.route('/parts/<int:part_id>/', methods=['GET'])
def get_part_by_id(part_id):
    """
    Gets Part by ID number
    Returns jsonified list of part information.
    """
    return jsonify({'Part ' + str(part_id): find_part(part_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)

