from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Sample in-memory data store
data_store = {
    1: {"name": "Item 1", "value": 100},
    2: {"name": "Item 2", "value": 200},
}

# GET Request to fetch all data
class GetAllData(Resource):
    def get(self):
        return jsonify(data_store)

# POST Request to add new data
class AddData(Resource):
    def post(self):
        item_id = len(data_store) + 1
        item_data = request.get_json()
        data_store[item_id] = item_data
        return jsonify({"message": "Item added", "item_id": item_id})

# PUT Request to update existing data
class UpdateData(Resource):
    def put(self, item_id):
        if item_id in data_store:
            data_store[item_id] = request.get_json()
            return jsonify({"message": "Item updated", "item_id": item_id})
        else:
            return jsonify({"message": "Item not found"})

# PATCH Request to partially update data
class PatchData(Resource):
    def patch(self, item_id):
        if item_id in data_store:
            updated_data = request.get_json()
            data_store[item_id].update(updated_data)
            return jsonify({"message": "Item partially updated", "item_id": item_id})
        else:
            return jsonify({"message": "Item not found"})

# DELETE Request to delete data
class DeleteData(Resource):
    def delete(self, item_id):
        if item_id in data_store:
            del data_store[item_id]
            return jsonify({"message": "Item deleted", "item_id": item_id})
        else:
            return jsonify({"message": "Item not found"})

# Adding routes
api.add_resource(GetAllData, "/items")
api.add_resource(AddData, "/items")
api.add_resource(UpdateData, "/items/<int:item_id>")
api.add_resource(PatchData, "/items/<int:item_id>")
api.add_resource(DeleteData, "/items/<int:item_id>")

# Swagger UI
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={'app_name': "Personal Budget API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
