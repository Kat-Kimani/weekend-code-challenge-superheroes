#!usr/bin/env python3
from random import randint, choice as rc
from faker import Faker
from models import db, Hero, Power, HeroPower
from app import app

fake = Faker()

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    heroes = []
    for i in range(50):
        hero = Hero(
          name= fake.name(),
          super_name = fake.first_name(),  
        )
        heroes.append(hero)
    db.session.add_all(heroes)
    db.session.commit()
    
    
    powers = []
    for i in range(50):
        description = fake.paragraph()
        while len(description) < 20:
            description = fake.paragraph()

        power = Power(
            name=fake.name(),
            description=description
        )
        powers.append(power)
    db.session.add_all(powers)
    db.session.commit()

    
    
 # Creates association between heroes and powers
    hero_powers = []
    for i in range(100):
        hero_power = HeroPower(
            hero_id=rc(heroes).id,
            power_id=rc(powers).id,
            strength=rc(['Strong', 'Weak', 'Average'])
        )
        hero_powers.append(hero_power)
    db.session.add_all(hero_powers)
    db.session.commit()