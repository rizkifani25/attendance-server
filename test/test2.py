import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(
    'cascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    'cascade/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
index = 0


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


while(True):
    # Capture frame-by-frame
    rect, frame = cap.read()

    # Our operations on the frame come here
    frame = rescale_frame(frame, percent=100)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_frame = frame[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.5,
            minNeighbors=10,
            minSize=(5, 5),
        )

        for (ex, ey, ew, eh) in eyes:
            if index == 0:
                eye_1 = (ex, ey, ew, eh)
            elif index == 1:
                eye_2 = (ex, ey, ew, eh)

            cv2.rectangle(
                roi_frame,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 0, 255),
                3
            )
            index = index + 1

            # Display the resulting frame
            cv2.imshow('frame', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
