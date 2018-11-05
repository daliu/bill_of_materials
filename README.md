
# To start the server:
Make sure you have Python3, pip, and virtualenv
> source venv/bin/activate to start the virtual environment
> pip install -r requirements.txt
> python app.py (Server should be running on localhost:5000)

# To Create a Part object:
(Must specify correct API route, header, and data columns)

> curl -X POST http://localhost:5000/create/ --header "Content-Type: application/json" -d '{"name": "phone", "color":"silver", "model": "iPhone"}'

# To List all parts in BoM:
> curl -X GET http://localhost:5000/bom/

# To List...

# To List...

# To List...
# To List...
# To List...
# To List...
# To List...
# To List...



### To Update a Part Object:
> 

# To Delete a Part Object:
###### WARNING: ANYONE CAN DELETE
###### May want to install API key for permissions

> curl -X DELETE http://localhost:5000/delete/ID/


