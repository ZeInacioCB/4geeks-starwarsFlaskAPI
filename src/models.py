from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# The blog Users data table
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


# The Planets from Starwars API Datatable
class Planets(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    terrain = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    population = db.Column(db.String(250))
    diameter = db.Column(db.String(250))

    def __repr__(self):
        return '<Planetarium %r>' % self.name

    def serialize(self):
        return {
            "id" : self.planet_id,
            "planet" : self.name,
            "terrain" : self.terrain,
            "climate" : self.climate,
            "population" : self.population,
            "diameter" : self.diameter
        }



# The Characters from Starwars API Datatable
class Characters(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    homeworld_id = db.Column(db.Integer) #db.ForeignKey(Planets.planet_id) 
    gender = db.Column(db.String(10))
    hairColor = db.Column(db.String(250))
    skinColor = db.Column(db.String(250))
    eyeColor = db.Column(db.String(250))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.character_id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hairColor,
            "skin_color": self.skinColor,
            "eye_color": self.eyeColor,
            "homeworld": self.homeworld_id
        }

# The Starships from Starwars API Datatable
class Starships(db.Model):
    starship_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    pilot_id = db.Column(db.Integer) #db.ForeignKey(Characters.character_id)
    model = db.Column(db.String(500))
    manufacturer = db.Column(db.String(250))
    cost = db.Column(db.Integer)
    topSpeed = db.Column(db.Integer)
    maxCargo = db.Column(db.Integer)

    def __repr__(self):
        return '<Starship %r>' % self.name

    def serialize(self):
        return {
            "id": self.starship_id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost": self.cost,
            "topSpeed": self.topSpeed,
            "maxCargo": self.maxCargo,
            "pilot": self.pilot_id
        }



# The user Favourites from Starwars API Datatable. It is a kind of connection Datatable between each userid and its own favourites
class Favourites(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) #db.ForeignKey(User.id), nullable=False
    character_id = db.Column(db.Integer) #db.ForeignKey(Characters.character_id
    planet_id = db.Column(db.Integer) #db.ForeignKey(Planets.planet_id)
    starship_id = db.Column(db.Integer) #db.ForeignKey(Starships.starship_id)

    def __repr__(self):
        return '<Favourite %r>' % self.favourite_id

    def serialize(self):
        return {
            "id": self.favourite_id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "starship_id": self.starship_id
        }
