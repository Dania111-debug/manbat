from flask import Flask, render_template, request, jsonify
from collections import defaultdict

app = Flask(__name__)

# تخزين مؤقت بالذاكرة
schools = []
school_counts = defaultdict(int)
devices = set()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    device = data.get("device_id")

    if device in devices:
        return jsonify({"error": "تم التسجيل من هذا الجهاز مسبقًا"}), 400

    devices.add(device)

    school = data["school"]
    lat = data["lat"]
    lng = data["lng"]

    school_counts[school] += 1
    schools.append({
        "school": school,
        "lat": lat,
        "lng": lng,
        "count": school_counts[school]
    })

    return jsonify({"success": True})

@app.route("/schools")
def get_schools():
    latest = {}
    for s in schools:
        latest[s["school"]] = s
    return jsonify(list(latest.values()))

@app.route("/schools/top")
def top_schools():
    top = sorted(
        school_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    return jsonify([
        {"school": k, "count": v} for k, v in top
    ])

@app.route("/count")
def count():
    return jsonify({"count": sum(school_counts.values())})

if __name__ == "__main__":
    app.run(debug=True)
