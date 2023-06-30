from flask import Flask
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_restful import Resource,Api,reqparse,abort
from flask_pymongo import PyMongo

app= Flask(__name__)
app.secret_key="secretKey"

api=Api(app)
app.config["MONGO_URI"]="mongodb://localhost:27017/CoRiderDatabase"
mongo=PyMongo(app)

errors = {
    'NotFoundError': {
        'message':'Not Found',
        'status': 404,
    },
}
api=Api(app,errors=errors)


class Users(Resource):
    def get(self):
        users=mongo.db.Users.find()
        resp=dumps(users)
        return resp
    
    def post(self):
        _json=request.json
        _name=_json['name']
        _email=_json['email']
        _password=_json['password']
        if _name and _email and _password:
            _hashed_password=generate_password_hash(_password)
            id=mongo.db.Users.insert_one({'name':_name,'email':_email,'password':_hashed_password})
            resp=jsonify("User added Successfully")
            resp.status_code=200
            return resp
        
class User(Resource):
    def get(self,id):
        users=mongo.db.Users.find_one({'_id':ObjectId(id)})
        resp=dumps(users)
        return resp
    def put(self,id):
        _id=id
        _json=request.json
        _name=_json['name']
        _email=_json['email']
        _password=_json['password']
        if _name and _email and _password and _id:
            _hashed_password=generate_password_hash(_password)
            mongo.db.Users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'password':_hashed_password}})
            resp=jsonify("User updates successfully")
            resp.status_code=200
            return resp
    def delete(self,id):
        mongo.db.Users.delete_one({'_id':ObjectId(id)})
        resp=jsonify("User deleted successfully")
        resp.status_code=200
        return resp        

api.add_resource(Users,'/users')
api.add_resource(User,'/users/<id>')

if __name__=="__main__":
    app.run(debug=True)