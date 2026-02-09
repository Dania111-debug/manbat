from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

schools = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_school', methods=['POST'])
def add_school():
    data = request.json
    schools.append({
        "name": data['name'],
        "lat": data['lat'],
        "lng": data['lng']
    })
    return jsonify({"message": "تمت الإضافة"})

@app.route('/schools')
def get_schools():
    return jsonify(schools)

@app.route('/count')
def count():
    return jsonify({"count": len(schools)})

if __name__ == '__main__':
    app.run()
