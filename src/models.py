from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    terrain = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    population = db.Column(db.String(250))
    diameter = db.Column(db.String(250))

class Characters(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    homeworld_id = db.Column(db.Integer, db.ForeignKey(Planets.planet_id))
    gender = db.Column(db.String(10))
    hairColor = db.Column(db.String(250))
    skinColor = db.Column(db.String(250))
    eyeColor = db.Column(db.String(250))

class Starships(db.Model):
    starship_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    pilot_id = db.Column(db.Integer, db.ForeignKey(Characters.character_id))
    model = db.Column(db.String(500))
    manufacturer = db.Column(db.String(250))
    cost = db.Column(db.Integer)
    topSpeed = db.Column(db.Integer)
    maxCargo = db.Column(db.Integer)

class Favourites(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey(Characters.character_id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.planet_id))
    starship_id = db.Column(db.Integer, db.ForeignKey(Starships.starship_id))
