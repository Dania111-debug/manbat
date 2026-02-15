from flask import Flask, render_template, request, jsonify
from collections import defaultdict

app = Flask(__name__)

# تخزين مؤقت
schools = {}
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

    name = data["name"].strip()
    stage = data["stage"]
    gender = data["gender"]
    city = data["city"]
    lat = data["lat"]
    lng = data["lng"]

    # نصنع مفتاح فريد
    key = f"{name}-{stage}-{gender}-{city}"

    school_counts[key] += 1

    schools[key] = {
        "name": name,
        "stage": stage,
        "gender": gender,
        "city": city,
        "lat": lat,
        "lng": lng,
        "count": school_counts[key]
    }

    return jsonify({"success": True})


@app.route("/schools")
def get_schools():
    return jsonify(list(schools.values()))


@app.route("/schools/top")
def top_schools():
    top = sorted(
        schools.values(),
        key=lambda x: x["count"],
        reverse=True
    )[:5]

    return jsonify(top)


@app.route("/count")
def count():
    return jsonify({"count": sum(school_counts.values())})


if __name__ == "__main__":
    app.run(debug=True)
