from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

INSTAGRAM_LINK = "https://www.tiktok.com/@manazelmashaertravels?_t=ZS-8zGwtLtSu29&_r=1"  # 👈 Replace this

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True)

@app.route('/')
def scan():
    device_id = request.cookies.get('device_id')
    if not device_id:
        device_id = str(uuid.uuid4())

    existing = Scan.query.filter_by(device_id=device_id).first()

    if existing:
        return render_template("denied.html")

    new_scan = Scan(device_id=device_id)
    db.session.add(new_scan)
    db.session.commit()

    # Set cookie and show redirecting page
    resp = make_response(render_template("redirect.html", link=INSTAGRAM_LINK))
    resp.set_cookie('device_id', device_id, max_age=60*60*24*365)
    return resp

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


