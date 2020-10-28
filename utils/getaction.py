from controller.admin import Admin
from controller.student import Student


class Action:
    action = ""
    query = {}
    listAction = []

    def __init__(self, data):
        self.action = data["action"]
        self.query = data["query"]

        self.listAction = [
            ["loginadmin", Admin(self.query).login(), ],
            ["registeradmin", Admin(self.query).register()],
            ["liststudent", Student(self.query).findAllStudent()],
            ["loginstudent", Student(self.query).login()],
            ["registerstudent", Student(self.query).register()]
        ]

    def generateQuery(self):
        for x in range(len(self.listAction)):
            if self.action == self.listAction[x][0]:
                return self.listAction[x]
