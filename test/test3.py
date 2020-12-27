import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(
    'cascade/haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    if cv2.waitKey(27) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
