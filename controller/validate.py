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


def testing(data):
    roomDir = data['room_id']
    studentDir = data['student_id']
    isOut = data['is_out']

    url = ''
    pathLocalIn = 'attendance/' + roomDir + '/' + \
        studentDir + '/in/' + studentDir + '-validated.jpg'
    pathDownloadIn = download_path + 'validate/' + roomDir + \
        '/' + studentDir + '/in/' + studentDir + '.jpg'
    pathLocalOut = 'attendance/' + roomDir + '/' + \
        studentDir + '/out/' + studentDir + '.jpg'
    pathDownloadOut = download_path + 'validate/' + roomDir + \
        '/' + studentDir + '/out/' + studentDir + '.jpg'
    try:
        if isOut == False:
            url = fstorage.child(pathLocalIn).get_url(None)
        else:
            url = fstorage.child(pathLocalOut).get_url(None)
    except Exception as e:
        print(e)
    return url


# download image from firebase
def downloadImageFromFirebase(roomDir, studentDir, isOut):
    pathLocalIn = 'attendance/' + roomDir + '/' + \
        studentDir + '/in/' + studentDir + '.jpg'
    pathDownloadIn = download_path + 'validate/' + roomDir + \
        '/' + studentDir + '/in/' + studentDir + '.jpg'
    pathLocalOut = 'attendance/' + roomDir + '/' + \
        studentDir + '/out/' + studentDir + '.jpg'
    pathDownloadOut = download_path + 'validate/' + roomDir + \
        '/' + studentDir + '/out/' + studentDir + '.jpg'
    try:
        if isOut == False:
            fstorage.child(pathLocalIn).download(pathDownloadIn)
        else:
            fstorage.child(pathLocalOut).download(pathDownloadOut)
    except Exception as e:
        print(e)
    return True


# download image base from firebase
def downloadImageBaseFromFirebase(studentDir):
    pathBase = 'base/' + studentDir + '/' + studentDir + '.jpg'
    pathDownloadBase = download_path + 'base/' + \
        studentDir + '/' + studentDir + '.jpg'
    try:
        fstorage.child(pathBase).download(pathDownloadBase)
    except Exception as e:
        print(e)
    return True


# check directory for base
def createDirectoryBase(dirName):
    pathBase = download_path + 'base/' + dirName + '/'
    if os.path.isdir(pathBase) == False:
        try:
            os.mkdir(path=pathBase)
        except Exception as e:
            print(e)
        return True
    else:
        return False


# check directory for validate
def createDirectoryValidate(roomDir, studentDir):
    pathDirValidate = download_path + 'validate/' + roomDir + '/'
    pathDirValidateStudent = download_path + \
        'validate/' + roomDir + '/' + studentDir + '/'

    pathStudentValidateIn = download_path + \
        'validate/' + roomDir + '/' + studentDir + '/in/'
    pathStudentValidateOut = download_path + \
        'validate/' + roomDir + '/' + studentDir + '/out/'

    if os.path.isdir(pathDirValidate) == False:
        try:
            os.mkdir(path=pathDirValidate)
            createDirectoryValidate(roomDir=roomDir, studentDir=studentDir)
        except Exception as e:
            print(e)
    else:
        if os.path.isdir(pathDirValidateStudent) == False:
            try:
                os.mkdir(path=pathDirValidateStudent)
                createDirectoryValidate(roomDir=roomDir, studentDir=studentDir)
            except Exception as e:
                print(e)
        else:
            try:
                os.mkdir(path=pathStudentValidateIn)
                os.mkdir(path=pathStudentValidateOut)
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
    downloadImageBaseFromFirebase(studentDir=_studentId)
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
        imgValidatedFileNameUpload = 'attendance/' + _roomId + '/' + \
            _studentId + '/out/' + _studentId + '-validated.jpg'

    imgBasePath = download_path + 'base/' + _studentId + '/' + _studentId + '.jpg'

    # recognition process
    imgValidateOri = cv2.imread(
        imgValidatePath, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    # imgValidate = face_recognition.load_image_file(imgValidateOri)
    # imgValidate = cv2.cvtColor(imgValidate, cv2.COLOR_BGR2RGB)

    imgBaseOri = cv2.imread(
        imgBasePath, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    # imgBase = face_recognition.load_image_file(imgBaseOri)
    # imgBase = cv2.cvtColor(imgBase, cv2.COLOR_BGR2RGB)

    # search face location then encode it => imgBase
    imgBaseFaceLoc = face_recognition.face_locations(imgBaseOri)[0]
    encodeBaseFace = face_recognition.face_encodings(imgBaseOri)[0]
    cv2.rectangle(
        imgBaseOri,
        (imgBaseFaceLoc[3], imgBaseFaceLoc[0]),
        (imgBaseFaceLoc[1], imgBaseFaceLoc[2]),
        (255, 0, 255),
        2
    )
    # cv2.imshow('Base Face', imgBaseOri)

    # search face location then encode it => imgValidate
    imgValidateFaceLoc = face_recognition.face_locations(imgValidateOri)[0]
    encodeValidateFace = face_recognition.face_encodings(imgValidateOri)[0]
    cv2.rectangle(
        imgValidateOri,
        (imgValidateFaceLoc[3], imgValidateFaceLoc[0]),
        (imgValidateFaceLoc[1], imgValidateFaceLoc[2]),
        (255, 0, 255),
        2
    )
    # cv2.imshow('Validate Face', imgValidateOri)
    # cv2.waitKey(0)

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
        imgValidateOri,
        f'{result} {round(faceDistance[0], 2)}',
        (50, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imwrite(imgValidatedFileName, imgValidateOri)
    fstorage.child(imgValidatedFileNameUpload).put(imgValidatedFileName)

    url_validated = fstorage.child(imgValidatedFileNameUpload).get_url(None)

    finalResult = {
        "result": str(result[0]),
        "image_url_validated": url_validated,
        "face_distance": round(faceDistance[0], 2)
    }

    return finalResult
