from hashlib import new
import re
from flask import Flask
from flask_pymongo import PyMongo
from pymongo.collection import ReturnDocument

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

try:
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/attendance'
    mongo = PyMongo(app)
    room = mongo.db.room
except:
    print("Error Handled | No Internet Access")


class Room:
    q = {}
    projection = {}

    def __init__(self, query):
        self.q = query

    # findById
    def findRoomById(self):
        query = {}
        result = False
        if "roomId" in self.q:
            query = {
                "roomId": self.q["roomId"]
            }
            result = room.find_one(query, self.projection)
        else:
            result = False
        return True if result else False

    # get next sequence value
    def getNextSequenceValue(self, sequenceName):
        sequenceDocument = room.find_and_modify(
            {"_id": sequenceName},
            {"$inc": {"sequence_value": 1}},
            new=True
        )
        return sequenceDocument["sequence_value"]

    # findByCustom
    def findByCustom(self):
        query = {}
        result = False
        if "roomId" in self.q:
            roomId = self.q["roomId"]
            query["roomId"] = roomId
        elif "roomName" in self.q:
            roomName = self.q["roomName"]
            query["roomName"] = roomName
        elif "time1" in self.q:
            time1 = self.q["time1"]
            query["time1"] = time1
        elif "time2" in self.q:
            time2 = self.q["time2"]
            query["time2"] = time2
        elif "time3" in self.q:
            time3 = self.q["time3"]
            query["time3"] = time3
        elif "time4" in self.q:
            time4 = self.q["time4"]
            query["time4"] = time4
        elif "date" in self.q:
            date = self.q["date"]
            query["date"] = date
        else:
            query = {}

        result = list(room.find(query))

        return {
            "status": True,
            "message": "Listing success.",
            "data": result
        } if len(result) > 0 else {
            "status": False,
            "message": "Listing failed. Empty data.",
        }

    # register
    def register(self):
        query = {}
        result = False
        if "roomName" in self.q and "time1" in self.q and "time2" in self.q and "time3" in self.q and "time4" in self.q and "date" in self.q:
            nextSequence = self.getNextSequenceValue("roomId")
            roomName = self.q["roomName"]
            time1 = self.q["time1"]
            time2 = self.q["time2"]
            time3 = self.q["time3"]
            time4 = self.q["time4"]
            date = self.q["date"]
            roomId = str(nextSequence) + "-" + roomName
            query = {
                "_id": nextSequence,
                "roomId": roomId,
                "roomName": roomName,
                "time1": time1,
                "time2": time2,
                "time3": time3,
                "time4": time4,
                "date": date
            }
            room.insert(query)
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
                "Fields can not be empty."
            ]
        }

    # update
    def update(self):
        query = {}
        result = False
        if "_id" in self.q and "roomId" in self.q and "roomName" in self.q and "time1" in self.q and "time2" in self.q and "time3" in self.q and "time4" in self.q and "date" in self.q:
            _id = self.q["_id"]
            roomId = self.q["roomId"]
            roomName = self.q["roomName"]
            time1 = self.q["time1"]
            time2 = self.q["time2"]
            time3 = self.q["time3"]
            time4 = self.q["time4"]
            date = self.q["date"]
            query = {
                "time1": time1,
                "time2": time2,
                "time3": time3,
                "time4": time4,
            }
            result = room.find_one_and_update(
                {
                    "_id": _id,
                    "roomId": roomId,
                    "roomName": roomName,
                    "date": date
                },
                {
                    "$set": query
                },
                None,
                None,
                False,
                ReturnDocument.AFTER
            )
            False if result == None else True
        else:
            result = False
        return {
            "status": True,
            "message": "Update success."
        } if result else {
            "status": False,
            "message": "Update failed.",
            "reasons": [
                "Fields can not be empty.",
                "Class not found."
            ]
        }

    # delete
    def delete(self):
        query = {}
        result = False
        if "_id" in self.q and "roomId" in self.q:
            _id = self.q["_id"]
            roomId = self.q["roomId"]
            query = {
                "_id": _id,
                "roomId": roomId
            }
            result = room.delete_one(query)
            result = int(result.deleted_count)
            True if result == 1 else False
        else:
            result = False
        return {
            "status": True,
            "message": "Delete success."
        } if result else {
            "status": False,
            "message": "Delete failed.",
            "reasons": [
                "Fields can not be empty.",
                "Class not found or already deleted."
            ]
        }
