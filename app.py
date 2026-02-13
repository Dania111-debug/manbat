from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# جدول المدارس
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

# إنشاء قاعدة البيانات
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

# جلب المدارس
@app.route('/schools')
def get_schools():
    schools = School.query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "lat": s.lat,
            "lng": s.lng
        } for s in schools
    ])

# عداد المدارس
@app.route('/schools/count')
def schools_count():
    return jsonify({"count": School.query.count()})

# إضافة مدرسة
@app.route('/add_school', methods=['POST'])
def add_school():
    data = request.get_json()

    name = data.get('name')
    lat = data.get('lat')
    lng = data.get('lng')

    if not name:
        return jsonify({"error": "اسم المدرسة مطلوب"})

    # منع التكرار
    existing = School.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "هذه المدرسة مسجلة مسبقاً"})

    new_school = School(name=name, lat=lat, lng=lng)
    db.session.add(new_school)
    db.session.commit()

    return jsonify({"message": "تمت إضافة المدرسة بنجاح"})

if __name__ == '__main__':
    app.run(debug=True)
