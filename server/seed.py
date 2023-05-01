from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

def seed_planets():
    for i in range(10):
        planet = Planet(
            name=fake.word(),
            distance_from_earth='pretty far',
            nearest_star=fake.word(),
            image='https://images.newscientist.com/wp-content/uploads/2017/06/21180000/planet-10-orange-blue-final-small.jpg?crop=4:3,smart&width=1200&height=900&upscale=true'
        )
        db.session.add(planet)
        
def seed_scientists():
    for i in range(10):
        scientist = Scientist(
            name=fake.name(),
            field_of_study=fake.word(),
            avatar='https://images.theconversation.com/files/195534/original/file-20171120-18528-9dhpdr.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=237&fit=clip'
        )
        db.session.add(scientist)
        
def add_oli():
    first_name = ''
    last_name = ''
    while first_name != 'Oliver':
        first_name = fake.last_name()
        name = f'{first_name} {last_name}'
        print(name)
    while last_name != 'Chase':
        last_name = fake.last_name()
        name = f'{first_name} {last_name}'
        print(name)
    scientist = Scientist(
        name=name,
        field_of_study='Alien Slugs',
        avatar='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthumbs.dreamstime.com%2Fz%2Fcartoon-slug-hand-drawn-illustration-retro-style-vector-available-37019395.jpg&f=1&nofb=1&ipt=87455a60d485bcadd29e1cf4873c0ab61fdb43c5e0308532da2050f8ba428be0&ipo=images'
    )
    db.session.add(scientist)
        
def seed_missions():
    for i in range(10):
        mission = Mission(
            name=fake.word(),
            scientist_id=randint(1, 10),
            planet_id=randint(1, 10)
        )
        db.session.add(mission)

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()
        
        print('Seeding planets...')
        seed_planets()
        
        print('Seeding scientists...')
        seed_scientists()
        add_oli()
        
        print('Seeding missions...')
        seed_missions()
        
        print('Committing...')
        db.session.commit()
    
        print("Done seeding!")
