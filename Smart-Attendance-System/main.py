import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
from keras.models import load_model
import matplotlib.pyplot as plt

emotion_detection_model = load_model('pretrained_emotion_detection_model.h5')
emotion_detection_model.save('emotion_detection.h5')

age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

cap = cv2.VideoCapture(0)


def detect_emotions(frame):
    # Load the pre-trained face detection classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Load the pre-trained emotion detection model
    model = load_model('emotion_detection.h5')

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # For each face detected, predict the emotion
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, (64, 64))
        face_roi = face_roi.astype('float') / 255.0
        face_roi = np.expand_dims(face_roi, axis=0)
        face_roi = np.expand_dims(face_roi, axis=-1)
        emotion_predictions = model.predict(face_roi)[0]
        max_index = np.argmax(emotion_predictions)
        emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        emotion = emotions[max_index]
        emotion_probability = emotion_predictions[max_index]
        # Draw a rectangle around the face and display the predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion + ' ({:.2f}%)'.format(emotion_probability * 100), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return frame


video_capture = cv2.VideoCapture(0)

known_face_encoding = []
known_faces_names = []

faces_directory = "face_images/"

for filename in os.listdir(faces_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(faces_directory, filename)
        face_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encoding.append(face_encoding)
        known_faces_names.append(filename.split(".")[0])

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
        name = ""
        face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
        best_match_index = np.argmin(face_distance)
        if matches[best_match_index]:
            name = known_faces_names[best_match_index]

        if name and name not in face_names:
            face_names.append(name)

        if name in students:
            students.remove(name)
            print(students)
            current_time = now.strftime("%H-%M-%S")
            lnwriter.writerow([name, current_time])

        if name in known_faces_names:
            font = cv2.ACCESS_MASK
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            if name:
                fontColor = (0, 255, 0)  # Green color if present
            else:
                fontColor = (0, 0, 255)  # Red color if absent
            thickness = 6
            lineType = 2

            cv2.putText(frame, name + ' Present', bottomLeftCornerOfText, font, fontScale, fontColor, thickness,
                        lineType)

    # Check posture
    if len(face_locations) > 0:
        top, right, bottom, left = face_locations[0]
        x_diff = right - left
        y_diff = bottom - top
        aspect_ratio = x_diff / y_diff
        if aspect_ratio > 1.9 or aspect_ratio < 1:
            # Posture not straight
            cv2.putText(frame, name + " Please keep your posture straight!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

    # Emotion detection
    frame = detect_emotions(frame)

    cv2.imshow("Advanced Attendance system ©Kushagra & Vaishnavi 2023", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
f.close()
cv2.destroyAllWindows()

