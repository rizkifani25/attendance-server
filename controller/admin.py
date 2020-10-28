import hashlib
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

try:
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/attendance'
    mongo = PyMongo(app)
    admin = mongo.db.admin
except:
    print("Error Handled | No Internet Access")


class Admin():
    q = {}
    projection = {'_id': False, 'password': False}

    def __init__(self, query):
        self.q = query

    # find all
    def findAllData(self):
        return admin.find({}, self.projection)

    # login
    def login(self):
        query = {}
        result = False
        if "username" in self.q and "password" in self.q:
            username = self.q["username"]
            password = self.q["password"]
            query = {
                "username": username,
                "password": hashlib.md5(str(password).encode()).hexdigest()
            }
            result = admin.find_one(query, self.projection)
        else:
            result = False
        return {
            "status": True,
            "message": "Login success."
        } if result else {
            "status": False,
            "message": "Login failed."
        }

    # register
    def register(self):
        query = {}
        result = False
        if "username" in self.q and "password" in self.q:
            username = self.q["username"]
            password = self.q["password"]
            result = self.findByUsername()
            query = {
                "username": username,
                "password": hashlib.md5(str(password).encode()).hexdigest()
            }
            if result:
                result = False
            else:
                admin.insert(query)
                result = True
        else:
            result = False
        return {
            "status": True,
            "message": "Register success."
        } if result else {
            "status": False,
            "message": "Register failed.",
            "reasons": [
                "Username already exist.",
                "Username can not be empty.",
                "Password can not be empty."
            ]
        }

    # findByUsername
    def findByUsername(self):
        query = {}
        result = False
        if "username" in self.q:
            query = {
                "username": self.q["username"]
            }
            result = admin.find_one(query, self.projection)
        else:
            result = False
        return True if result else False

    # update Data
    def update(self):
        username = self.q["username"]
        password = self.q["password"]
        updatedData = self.q["updatedData"]
        result = admin.update_one({
            "username": username,
            "password": hashlib.md5(str(password).encode()).hexdigest()
        }, {
            "$set": {
                "username": updatedData.username,
                "password": hashlib.md5(str(updatedData.password).encode()).hexdigest()
            }
        })
        if result.modified_count == 1 and result.matched_count == 1:
            return True
        else:
            return False
