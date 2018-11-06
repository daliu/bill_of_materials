
# To start the server:
Make sure you have Python3, pip, and virtualenv
> source venv/bin/activate to start the virtual environment
> pip install -r requirements.txt
> python app.py (Server should be running on localhost:5000)

## Note: When using curl, make sure URLs always end in backslash


# To Create a Part object:
(Must specify correct API route, header, and at least a name in data dictionary. ID will be automatically specified.)
> curl -X POST http://localhost:5000/create/ --header "Content-Type: application/json" -d '{"name": "phone", "color":"silver", "model": "iPhone"}'


# To Update a Part Object:
> curl -X PUT http://localhost:5000/update/<int:part_id>/ --header "Content-Type: application/json" -d '{"color": "orange"}'


# To Delete a Part Object:
###### WARNING: ANYONE CAN DELETE
###### May want to install API key for permissions
> curl -X DELETE http://localhost:5000/delete/<int:ID>/


# Listing Parts:
### To list all parts in BoM:
> curl -X GET http://localhost:5000/bom/

### To list all assemblies:
> curl -X GET http://localhost:5000/assemblies/

### To list all top level assemblies (assemblies that are not children of another assembly):
> curl -X GET http://localhost:5000/toplevel/

### To list all subassemblies (assemblies that are children of another assembly):
> curl -X GET http://localhost:5000/subassems/

### To list all component parts (parts that are not subassemblies, but are included in a parent assembly):
> curl -X GET http://localhost:5000/components/

### To list all orphan parts (parts with neither parents nor children):
> curl -X GET http://localhost:5000/orphans/

### To list all the first-level children of a specific assembly:
> curl -X GET http://localhost:5000/assembly/children/<int: ID>

### To list all parts in a specific assembly:
> curl -X GET http://localhost:5000/parts/ID/

### To list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly):
> curl -X GET http://localhost:5000/dependencies/ID/


# Future Improvements:
##### We should store static values until we add/update/delete values, at which point only then would we need to make updates to our relational "database".
##### Ultimately though, if we really wanted to be efficient, using a database management system would likely abstract-away solutions to our inefficient accessors and checking methods.
##### If we cannot abstract-away accessors to be more efficient, then at least we can take inspiration from common database management algorithms.