from flask import Flask, request, jsonify
from db_manage.mysql_connector.database import Database
from service_funcs.Service import Service
from flask_cors import CORS


app = Flask(__name__)

CORS(app, supports_credentials=True)

# Configure Flask session
CORS(app, supports_credentials=True)


@app.route("/services", methods=["GET"])
def get_services():
	filter = request.args.get("filter")
	db = Database("Service")
	services = db.get_filtered_list_of_objects("Service", filter, include_columns=["name", "service_type"], inJson=True)
	return jsonify(services), 200

@app.route("/service", methods=["GET"])
def get_service():
	service_id = request.args.get("id")
	db = Database("Service")
	service = db.get_object_by_id("Service", service_id)
	service = db.get_object_by_id(service.service_type, service.id, inJson=True)
	return jsonify(service), 200

@app.route("/service", methods=["POST"])
def create_service():
	data = request.json
	service_id = Service.write_to_db(data)
	service = Service(service_id)
	service.create_service()
	return jsonify({"service_id": service_id}), 200

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=5000)