#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,abort, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if hero is None:
        abort(404, description='Hero not found')

    powers = [
        {
            'id': hero_power.power.id,
            'name': hero_power.power.name,
            'description': hero_power.power.description
        }
        for hero_power in hero.powers
    ]

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    response = make_response(jsonify(hero_data))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.errorhandler(404)
def not_found_error(error):
    response = make_response(jsonify({'error': 'Hero not found'}))
    response.headers['Content-Type'] = 'application/json'
    return response, 404



@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    
    powers_data = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in powers
    ]

    return jsonify(powers_data)

# get powers by id
@app.route("/powers/<int:id>", methods=["GET", "PATCH"])
def powers_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)
    else:
        if request.method == "GET":
            return make_response(jsonify(power.to_dict()), 200)
        
        # update description
        elif request.method == "PATCH":
            description = request.form.get("description")
            if description and len(description) < 20:
                return make_response(jsonify({"error":"[validation errors]"}), 400)
            
            setattr(power, "description", description)
            db.session.add(power)
            db.session.commit()
            return make_response(jsonify(power.to_dict()), 200)
        
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if not power or not hero:
        abort(400, description='Invalid power or hero')

    strength = data.get('strength')

    hero_power = HeroPower(strength=strength)
    hero_power.power = power
    hero_power.hero = hero

    try:
        db.session.add(hero_power)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    # Fetch the updated hero data with the associated powers
    updated_hero = Hero.query.get(hero_id)

    powers_data = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in updated_hero.powers
    ]

    hero_data = {
        'id': updated_hero.id,
        'name': updated_hero.name,
        'super_name': updated_hero.super_name,
        'powers': powers_data
    }

    return jsonify(hero_data)

@app.errorhandler(400)
def validation_error(error):
    response = jsonify({'errors': [str(error)]})
    response.status_code = 400
    return response

if __name__ == '__main__':
    app.run(port=5555)
