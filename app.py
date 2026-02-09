from flask import Flask, render_template, request, jsonify
from collections import defaultdict

app = Flask(__name__)

schools = []
counts = defaultdict(int)
devices = set()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    device = data.get("device_id")

    if device in devices:
        return jsonify({"error": "تم التسجيل من هذا الجهاز مسبقًا"})

    devices.add(device)

    school = data["school"]
    lat = data["lat"]
    lng = data["lng"]

    schools.append({
        "school": school,
        "lat": lat,
        "lng": lng
    })

    counts[school] += 1

    return jsonify({"success": True})

@app.route("/schools")
def get_schools():
    result = []
    for s in schools:
        result.append({
            "school": s["school"],
            "lat": s["lat"],
            "lng": s["lng"],
            "count": counts[s["school"]]
        })
    return jsonify(result)

@app.route("/count")
def count():
    return jsonify({"count": sum(counts.values())})

@app.route("/schools/top")
def top():
    top5 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return jsonify([{"school": k, "count": v} for k, v in top5])

if __name__ == "__main__":
    app.run(debug=True)
