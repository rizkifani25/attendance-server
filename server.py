import json

from flask.globals import request
import controller.validate as vl

from flask import Flask
from utils.baseresponse import BaseResponse

app = Flask(__name__)


# config file
fileConfig = open('config/config.json')
config = json.load(fileConfig)


# face validation
@app.route('/validate', methods=['GET', 'POST'])
def validateFace():
    body = request.get_json()
    result = vl.doValidate(body)
    return BaseResponse.generateBaseResponse(data=result, responseCode=200, responseMessage='success')


if __name__ == '__main__':
    app.run(debug=True, port=config["port"], host='0.0.0.0')
