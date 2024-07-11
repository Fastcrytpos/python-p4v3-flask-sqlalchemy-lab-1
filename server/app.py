# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<id>')
def view_earthquake (id):
    singleres=Earthquake.query.filter(Earthquake.id==id).first()
    if singleres:
        return make_response(singleres.to_dict(), 200)
    else:
        return make_response(jsonify({'error': 'Not Found', 'message': f'Earthquake {id} not found.'}), 404)

@app.route('/earthquakes/magnitude/<magnitude>', methods=['GET'])
def view_magnitude (magnitude):
    
    singleres=Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    
    all=[]
    for i in singleres:
        quake_dict=i.to_dict()
        all.append(quake_dict)
    body={'count': len(all),
            'quakes': all}
    
    if all:
        return make_response(body, 200)
    else:
        body={'count': 0,
            'quakes': all}
        return make_response(body, 200)





if __name__ == '__main__':
    app.run(port=5555, debug=True)
