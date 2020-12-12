from base64 import encode
import json
import os
from os.path import dirname
import cv2
import face_recognition

from firebase import Firebase

# config file
fileConfig = open('config/config.json')
config = json.load(fileConfig)


# setup directory
download_path = config['download_path']
checkDir = os.path.isdir(config['download_path'])
if checkDir == False:
    try:
        os.mkdir(path=download_path)
        os.mkdir(path=download_path + '/base')
        os.mkdir(path=download_path + '/validate')
    except Exception as e:
        print(e)


# setup firebase
firebase = Firebase(config=config['firebaseConfig'])
fstorage = firebase.storage()


# download image from firebase
def downloadImageFromFirebase(roomDir, studentDir, isOut):
    try:
        if isOut == False:
            fstorage.child('attendance/' + roomDir + '/' + studentDir + '/in/' + studentDir + '.jpg').download(
                download_path + 'validate/' + roomDir + '/' + studentDir + '/in/' + studentDir + '.jpg')
        else:
            fstorage.child('attendance/' + roomDir + '/' + studentDir + '/out/' + studentDir + '.jpg').download(
                download_path + 'validate/' + roomDir + '/' + studentDir + '/out/' + studentDir + '.jpg')
    except Exception as e:
        print(e)
    return True


# check directory for base
def createDirectoryBase(dirName):
    if os.path.isdir(download_path + 'base/' + dirName + '/') == False:
        try:
            os.mkdir(path=download_path + 'base/' + dirName + '/')
        except Exception as e:
            print(e)
        return True
    else:
        return False


# check directory for validate
def createDirectoryValidate(roomDir, studentDir):
    if os.path.isdir(download_path + 'validate/' + roomDir + '/') == False:
        try:
            os.mkdir(path=download_path + 'validate/' + roomDir + '/')
            createDirectoryValidate(roomDir=roomDir, studentDir=studentDir)
        except Exception as e:
            print(e)
    else:
        if os.path.isdir(download_path +
                         'validate/' + roomDir + '/' + studentDir + '/') == False:
            try:
                os.mkdir(path=download_path +
                         'validate/' + roomDir + '/' + studentDir + '/')
                createDirectoryValidate(roomDir=roomDir, studentDir=studentDir)
            except Exception as e:
                print(e)
        else:
            try:
                os.mkdir(path=download_path + 'validate/' +
                         roomDir + '/' + studentDir + '/in/')
                os.mkdir(path=download_path + 'validate/' +
                         roomDir + '/' + studentDir + '/out/')
            except Exception as e:
                print(e)
    return True


def doValidate(data):
    _roomId = data['room_id']
    _studentId = data['student_id']
    _isOut = data['is_out']

    createDirectoryBase(_studentId)

    createDirectoryValidate(
        roomDir=_roomId,
        studentDir=_studentId
    )
    downloadImageFromFirebase(
        roomDir=_roomId,
        studentDir=_studentId,
        isOut=_isOut
    )

    imgValidatePath = ''
    imgValidatedFileName = ''
    imgValidatedFileNameUpload = ''
    if data['is_out'] == False:
        imgValidatePath = download_path + 'validate/' + _roomId + \
            '/' + _studentId + '/in/' + _studentId + '.jpg'
        imgValidatedFileName = download_path + 'validate/' + _roomId + \
            '/' + _studentId + '/in/' + _studentId + '-validated.jpg'
        imgValidatedFileNameUpload = 'attendance/' + _roomId + \
            '/' + _studentId + '/in/' + _studentId + '-validated.jpg'
    else:
        imgValidatePath = download_path + 'validate/' + _roomId + \
            '/' + _studentId + '/out/' + _studentId + '.jpg'
        imgValidatedFileName = download_path + 'validate/' + _roomId + \
            '/' + _studentId + '/out/' + _studentId + '-validated.jpg'
        imgValidatedFileNameUpload = 'attendance/' + _roomId + \
            '/' + _studentId + '/out/' + _studentId + '-validated.jpg'

    imgBasePath = download_path + 'base/' + _studentId + '/' + _studentId + '.jpg'

    # recognition process
    imgValidate = face_recognition.load_image_file(imgValidatePath)
    imgValidate = cv2.cvtColor(imgValidate, cv2.COLOR_BGR2RGB)

    imgBase = face_recognition.load_image_file(imgBasePath)
    imgBase = cv2.cvtColor(imgBase, cv2.COLOR_BGR2RGB)

    # search face location then encode it => imgBase
    imgBaseFaceLoc = face_recognition.face_locations(imgBase)[0]
    encodeBaseFace = face_recognition.face_encodings(imgBase)[0]
    cv2.rectangle(
        imgBase,
        (imgBaseFaceLoc[3], imgBaseFaceLoc[0]),
        (imgBaseFaceLoc[1], imgBaseFaceLoc[2]),
        (255, 0, 255),
        2
    )

    # search face location then encode it => imgValidate
    imgValidateFaceLoc = face_recognition.face_locations(imgValidate)[0]
    encodeValidateFace = face_recognition.face_encodings(imgValidate)[0]
    cv2.rectangle(
        imgValidate,
        (imgValidateFaceLoc[3], imgValidateFaceLoc[0]),
        (imgValidateFaceLoc[1], imgValidateFaceLoc[2]),
        (255, 0, 255),
        2
    )

    result = face_recognition.compare_faces(
        [encodeBaseFace],
        encodeValidateFace
    )
    faceDistance = face_recognition.face_distance(
        [encodeBaseFace],
        encodeValidateFace
    )

    print('=====[LOG RESULT COMPARE START]=====')
    print('Student ID\t:: ' + _studentId)
    print('Room ID\t\t:: ' + _roomId)
    print('Result\t\t::', result, faceDistance)
    print('=====[LOG RESULT COMPARE END]=====')

    cv2.putText(
        imgValidate,
        f'{result} {round(faceDistance[0], 2)}',
        (50, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imwrite(imgValidatedFileName, imgValidate)
    fstorage.child(imgValidatedFileNameUpload).put(imgValidatedFileName)

    finalResult = {
        "result": str(result[0]),
        "face_distance": round(faceDistance[0], 2)
    }

    return finalResult
