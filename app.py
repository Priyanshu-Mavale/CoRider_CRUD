from flask import Flask
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_pymongo import PyMongo

app= Flask(__name__)
app.secret_key="secretKey"
app.config["MONGO_URI"]="mongodb://localhost:27017/CoRiderDatabase"
mongo=PyMongo(app)

# @app.route('/add',methods=['POST'])
# def add_user():
#     _json=request.json
#     _name=_json['name']
#     _email=_json['email']
#     _password=_json['password']

#     if _name and _email and _password and request.method=='POST':
#         _hashed_password=generate_password_hash(_password)

#         id=mongo.db.Users.insert_one({'name':_name,'email':_email,'password':_hashed_password})
#         resp=jsonify("User added Successfully")
#         resp.status_code=200
#         return resp
#     else:
#         return not_found()
    
@app.route('/users',methods=['POST','GET'])
def users():
    if request.method=='POST':
        _json=request.json
        _name=_json['name']
        _email=_json['email']
        _password=_json['password']

        if _name and _email and _password and request.method=='POST':
            _hashed_password=generate_password_hash(_password)

            id=mongo.db.Users.insert_one({'name':_name,'email':_email,'password':_hashed_password})
            resp=jsonify("User added Successfully")
            resp.status_code=200
            return resp
        else:
            return not_found()     
    elif request.method=='GET':
        users=mongo.db.Users.find()
        resp=dumps(users)
        return resp

@app.route('/users/<id>',methods=['GET','PUT','DELETE'])
def user(id):
    if request.method=='GET':
        users=mongo.db.Users.find_one({'_id':ObjectId(id)})
        resp=dumps(users)
        return resp
    elif request.method=='PUT':
        _id=id
        _json=request.json
        _name=_json['name']
        _email=_json['email']
        _password=_json['password']

        if _name and _email and _password and _id and request.method=='PUT':
            _hashed_password=generate_password_hash(_password)
            mongo.db.Users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'password':_hashed_password}})
            resp=jsonify("User updates successfully")
            resp.status_code=200
            return resp
        else:
            return not_found()
    elif request.method=='DELETE':
        mongo.db.Users.delete_one({'_id':ObjectId(id)})
        resp=jsonify("User deleted successfully")
        resp.status_code=200
        return resp

# @app.route("/delete/<id>",methods=['DELETE'])
# def delete_user(id):
#     mongo.db.Users.delete_one({'_id':ObjectId(id)})
#     resp=jsonify("User deleted successfully")
#     resp.status_code=200
#     return resp

# @app.route("/update/<id>",methods=['PUT'])
# def update_user(id):
#     _id=id
#     _json=request.json
#     _name=_json['name']
#     _email=_json['email']
#     _password=_json['password']

#     if _name and _email and _password and _id and request.method=='PUT':
#         _hashed_password=generate_password_hash(_password)
#         mongo.db.Users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'password':_hashed_password}})
#         resp=jsonify("User updates successfully")
#         resp.status_code=200
#         return resp
#     else:
#         return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not Found'+request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp


if __name__=="__main__":
    app.run(debug=True)