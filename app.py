from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

schools = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_school():
    data = request.json
    schools.append(data)
    return jsonify({"status": "ok"})

@app.route("/schools")
def get_schools():
    return jsonify(schools)

if __name__ == "__main__":
    app.run(debug=True)
