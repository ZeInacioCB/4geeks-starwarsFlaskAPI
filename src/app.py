"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favourites, Planets, Characters, Starships
from flask_jwt_extended import JWTManager

# Setup the Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)

# Setup PostgresSQL Database ??
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def characters_list():
    # query all characters in the database. But is this really?
    characters = Characters.query.all()
    # prints the representation we have defined. Is each of them a class instance? From the model?
    print(characters)
    characters = list(map(lambda x: x.serialize(), characters))
    print(characters)
    # what does the jsonify do? It looks like it transforms our data into a HTTP request? 
    print(jsonify(characters))
    return jsonify(characters), 200

@app.route("/people/<int:id>", methods=['GET'])
def person_detail(id):
    person = db.get_or_404(Characters, id)
    person = person.serialize()
    return jsonify(person)

@app.route('/planets', methods=['GET'])
def planets_list():
    planets = Planets.query.all()
    # This is what the serialize when defined inside the models.py script
    print(planets)
    def serialize(planet):
        return {
            "id" : planet.planet_id,
            "planet" : planet.name,
            "terrain" : planet.terrain,
            "climate" : planet.climate,
            "population" : planet.population,
            "diameter" : planet.diameter
        }
    planets = list(map(serialize, planets))
    return jsonify(planets), 200

@app.route("/planets/<int:id>", methods=['GET'])
def planet_detail(id):
    planet = db.get_or_404(Planets, id)
    planet = planet.serialize()
    return jsonify(planet)


@app.route('/starships', methods=['GET'])
def starships_list():
    starships = Starships.query.all()
    starships = list(map(lambda x: x.serialize(), starships))
    return jsonify(starships), 200


@app.route("/starships/<int:id>", methods=['GET'])
def starship_detail(id):
    starship = db.get_or_404(Starships, id)
    starship = starship.serialize()
    return jsonify(starship)


@app.route('/users', methods=['GET'])
def users_list():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    return jsonify(users), 200

@app.route('/favourites', methods=['GET'])
def favourites_list():
    favourites = Favourites.query.all()
    favourites = list(map(lambda x: x.serialize(), favourites))
    return jsonify(favourites), 200


@app.route("/users/favourites")
def user_by_username(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    return render_template("show_user.html", user=user)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
