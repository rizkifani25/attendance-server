import cv2
import face_recognition


# recognition process
# imgBaseOri = face_recognition.load_image_file('base.jpg')
imgBaseOri = cv2.imread(
    'validate6.jpg', cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
# imgBase = face_recognition.load_image_file(imgBaseOri)
# imgBaseOri = cv2.cvtColor(imgBaseOri, cv2.COLOR_BGR2RGB)

# imgValidateOri = face_recognition.load_image_file('validate.jpg')
imgValidateOri = cv2.imread(
    'validate9.jpg', cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
# imgValidate = face_recognition.load_image_file(imgValidateOri)
# imgValidateOri = cv2.cvtColor(imgValidateOri, cv2.COLOR_BGR2RGB)

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

cv2.imshow('Base Face', imgBaseOri)
cv2.imshow('Validate Face', imgValidateOri)
cv2.waitKey(0)

# cv2.imwrite('validate-done.jpg', imgValidateOri)
