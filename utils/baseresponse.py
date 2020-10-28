class BaseResponse:
    def generateBaseResponse(data, responseCode, responseMessage):
        return {
            "responseCode": responseCode,
            "responseMessage": responseMessage,
            "data": data
        }
