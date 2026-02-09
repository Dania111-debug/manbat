from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import difflib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    official_name = db.Column(db.String(200), unique=True, nullable=False)

class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    entered_name = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    device_id = db.Column(db.String(200), unique=True)

    school = db.relationship("School")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if Participation.query.filter_by(device_id=data['device_id']).first():
        return jsonify({"error": "تم التسجيل مسبقًا من هذا الجهاز"}), 400

    entered = data['school']
    names = [s.official_name for s in School.query.all()]

    match = difflib.get_close_matches(entered, names, n=1, cutoff=0.6)

    if match:
        school = School.query.filter_by(official_name=match[0]).first()
    else:
        school = School(official_name=entered)
        db.session.add(school)
        db.session.commit()

    p = Participation(
        school_id=school.id,
        entered_name=entered,
        lat=data['lat'],
        lng=data['lng'],
        device_id=data['device_id']
    )
    db.session.add(p)
    db.session.commit()

    return jsonify({"message": "تمت الإضافة بنجاح"})

@app.route('/count')
def count():
    return jsonify({"count": Participation.query.count()})

@app.route('/schools')
def schools():
    rows = db.session.query(
        School.official_name,
        func.count(Participation.id),
        func.avg(Participation.lat),
        func.avg(Participation.lng)
    ).join(Participation).group_by(School.id).all()

    return jsonify([
        {
            "school": r[0],
            "count": r[1],
            "lat": r[2],
            "lng": r[3]
        } for r in rows
    ])

@app.route('/schools/top')
def top():
    rows = db.session.query(
        School.official_name,
        func.count(Participation.id)
    ).join(Participation)\
     .group_by(School.id)\
     .order_by(func.count(Participation.id).desc())\
     .limit(10).all()

    return jsonify([
        {"school": r[0], "count": r[1]} for r in rows
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
app.run(host="0.0.0.0", port=10000)
