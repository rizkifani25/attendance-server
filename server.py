import json

from flask import Flask, request
from utils.baseresponse import BaseResponse
from utils.getaction import Action
from controller.admin import Admin
from controller.student import Student

app = Flask(__name__)

# config file
fileConfig = open('config/config.json')
config = json.load(fileConfig)


# universal route
@app.route("/", methods=['GET', 'POST'])
def universal():
    finalResponse = {}
    body = request.get_json()

    if body == None:
        return BaseResponse.generateBaseResponse(data=finalResponse, responseCode='400', responseMessage='Bad Request.')

    if "action" in body and "query" in body:
        action = str(body["action"]).lower()
        query = body["query"]

        if query == None or query == {} or query == "" or action == None:
            return BaseResponse.generateBaseResponse(data=finalResponse, responseCode='400', responseMessage='Bad Request.')
    else:
        return BaseResponse.generateBaseResponse(data=finalResponse, responseCode='400', responseMessage='Bad Request.')

    if request.method == 'POST':
        data = {"action": action, "query": query}
        getAction = Action(data)
        finalQuery = getAction.generateQuery2()
        if finalQuery != None:
            finalResponse = finalQuery
        else:
            finalResponse = {"message": "Action not yet implemented."}

        return BaseResponse.generateBaseResponse(data=finalResponse, responseCode="200", responseMessage="success")
    else:
        return BaseResponse.generateBaseResponse(data=finalResponse, responseCode="405", responseMessage="Method Not Allowed.")


if __name__ == '__main__':
    app.run(debug=True, port=config["port"], host='0.0.0.0')
