from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt_extended import JWTManager ,jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://:master:password@localhost:5432/my_db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
###########################################
class Puppy(db.Model):
    name = db.Column(db.String(80),primary_key=True)

    def __init__(self,name):
        self.name = name
    
    def json(self):
        return {'name': self.name}
#############################################

migrate = Migrate(app,db)
api = Api(app)
jwt = JWTManager(app)
 
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password',None)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

puppies = []




class PuppyNames(Resource):
    def get(self, name):

       pup =Puppy.query.filter_by(name=name).first()
       if pup:
           return pup.json()
       else:
           return {"name":None},404
        

    def post(self, name):
        pup =Puppy(name=name)
        db.session.add(pup)
        db.session.commit()

        return pup.json()

    def delete(self, name):
        
        pup = Puppy.query.filter_by(name=name).first()
        db.session.delete(pup)
        db.session.commit()
        return {'note':'delete success'}

            

class AllNames(Resource):

    #@jwt_required()
    def get(self):
        #list
        puppies = Puppy.query.all()

        return [pup.json() for pup in puppies]
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')

if __name__=='__main__': 
    app.run(debug=True)
 