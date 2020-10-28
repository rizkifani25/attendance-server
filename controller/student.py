import hashlib
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

try:
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/attendance'
    mongo = PyMongo(app)
    student = mongo.db.student
except:
    print("Error Handled | No Internet Access")


class Student():
    q = {}
    projection = {'_id': False, 'password': False}

    def __init__(self, query):
        self.q = query

    # find all student
    def findAllStudent(self):
        query = {}
        result = False
        projection = {'_id': False, 'password': False}
        if "studentId" in self.q:
            studentId = self.q["studentId"]
            if studentId != "all":
                query = {"studentId": studentId}
            else:
                query = {}
            result = list(student.find(query, projection))
        else:
            result = False
        return {
            "status": True,
            "message": "Listing success.",
            "students": result
        } if len(result) > 0 else {
            "status": False,
            "message": "Listing failed. Empty data."
        }

    # login
    def login(self):
        query = {}
        result = False
        if "studentId" in self.q and "password" in self.q:
            studentId = self.q["studentId"]
            password = self.q["password"]
            query = {
                "studentId": studentId,
                "password": hashlib.md5(str(password).encode()).hexdigest()
            }
            result = student.find_one(query, self.projection)
        else:
            result = False
        return {
            "status": True,
            "message": "Login success."
        } if result else {
            "status": False,
            "message": "Login failed."
        }

    # check studentId exist
    def findStudentById(self):
        query = {}
        result = False
        projection = {'_id': False, 'password': False}
        if "studentId" in self.q:
            studentId = self.q["studentId"]
            query = {"studentId": studentId}
            result = list(student.find(query, projection))
        else:
            result = False
        return {
            "status": True,
            "message": "Listing success.",
            "students": result
        } if len(result) == 1 else {
            "status": False,
            "message": "Duplicate or data cannot be found."
        }

    # register student
    def register(self):
        query = {}
        result = False
        if "studentId" in self.q and "password" in self.q and "studentName" in self.q and "batch" in self.q and "major" in self.q:
            studentId = self.q["studentId"]
            password = self.q["password"]
            studentName = self.q["studentName"]
            batch = self.q["batch"]
            major = self.q["major"]

            result = self.findStudentById()

            if result["status"]:
                result = False
            else:
                query = {
                    "studentId": studentId,
                    "studentName": studentName,
                    "password": hashlib.md5(str(password).encode()).hexdigest(),
                    "batch": batch,
                    "major": major,
                    "additionalData": {}
                }
                student.insert(query)
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
                "StudentId already exist.",
                "Fields can not be empty."
            ]
        }
