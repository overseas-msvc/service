from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/service", methods=["GET"])
def get_service():
	data = request.json
	return jsonify(f"reply from endpoint get_service, data = {data}")

@app.route("/service", methods=["POST"])
def create_service():
	data = request.json
	return jsonify(f"reply from endpoint create_service, data = {data}")

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)