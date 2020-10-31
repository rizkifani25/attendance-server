import re
from controller.admin import Admin
from controller.student import Student
from controller.room import Room


class Action:
    action = ""
    query = {}
    listAction = []

    def __init__(self, data):
        self.action = data["action"]
        self.query = data["query"]

        # self.listAction = [
        #     ["loginadmin", Admin(self.query).login(), ],
        #     ["registeradmin", Admin(self.query).register()],
        #     ["liststudent", Student(self.query).findAllStudent()],
        #     ["loginstudent", Student(self.query).login()],
        #     ["registerstudent", Student(self.query).register()],
        #     ["findroom", Room(self.query).findByCustom()],
        #     ["registerroom", Room(self.query).register()]
        # ]

    # def generateQuery(self):
    #     for x in range(len(self.listAction)):
    #         if str(self.action).lower() == self.listAction[x][0]:
    #             print(self.listAction[x])
    #             return self.listAction[x]

    def generateQuery2(self):
        action = str(self.action).lower()
        if action == "loginadmin":
            return Admin(self.query).login()
        elif action == "registeradmin":
            return Admin(self.query).register()
        elif action == "liststudent":
            return Student(self.query).findAllStudent()
        elif action == "loginstudent":
            return Student(self.query).login()
        elif action == "registerstudent":
            return Student(self.query).register()
        elif action == "findroom":
            return Room(self.query).findByCustom()
        elif action == "registerroom":
            return Room(self.query).register()
        elif action == "updateroom":
            return Room(self.query).update()
        elif action == "deleteroom":
            return Room(self.query).delete()
        else:
            return None
