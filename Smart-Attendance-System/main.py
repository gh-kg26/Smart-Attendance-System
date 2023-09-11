import face_recognition  # Importing face_recognition library
import cv2  # Importing OpenCV library
import numpy as np  # Importing NumPy library for numerical operations
import csv  # Importing CSV module for working with CSV files
import os  # Importing OS module for interacting with the operating system
from datetime import datetime  # Importing datetime module for handling dates and times
from keras.models import load_model  # Importing load_model function from Keras for loading a deep learning model
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

emotion_detection_model = load_model('pretrained_emotion_detection_model.h5')  # Load emotion detection model
emotion_detection_model.save('emotion_detection.h5')  # Save the model with a different name

age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')  # Load age detection model
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')  # Load gender detection model

cap = cv2.VideoCapture(0)  # Initialize video capture

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

video_capture = cv2.VideoCapture(0)  # Initialize video capture

known_face_encoding = []  # Initialize list for storing face encodings
known_faces_names = []  # Initialize list for storing face names

faces_directory = "face_images/"  # Define directory for face images

for filename in os.listdir(faces_directory):  # Loop through files in the faces directory
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Check if the file is an image
        image_path = os.path.join(faces_directory, filename)  # Get full image path
        face_image = face_recognition.load_image_file(image_path)  # Load face image
        face_encoding = face_recognition.face_encodings(face_image)[0]  # Get face encoding
        known_face_encoding.append(face_encoding)  # Add face encoding to list
        known_faces_names.append(filename.split(".")[0])  # Add face name to list

students = known_faces_names.copy()  # Create a copy of known face names

face_locations = []  # Initialize list for face locations
face_encodings = []  # Initialize list for face encodings
face_names = []  # Initialize list for face names
s = True  # Initialize s as True (used in face recognition loop)

now = datetime.now()  # Get current date and time
current_date = now.strftime("%Y-%m-%d")  # Format date as string

f = open(current_date + '.csv', 'w+', newline='')  # Open CSV file for writing
lnwriter = csv.writer(f)  # Initialize CSV writer

while True:  # Start infinite loop for video capture
    _, frame = video_capture.read()  # Read a frame from the video capture
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resize frame for faster processing
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB

    if s:  # If s is True
        face_locations = face_recognition.face_locations(rgb_small_frame)  # Get face locations
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)  # Get face encodings
        face_names = []  # Reset face names list

    for face_encoding in face_encodings:  # Loop through face encodings
        matches = face_recognition.compare_faces(known_face_encoding, face_encoding)  # Compare face encodings
        name = ""  # Initialize name as empty string
        face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)  # Calculate face distance
        best_match_index = np.argmin(face_distance)  # Get index of best match
        if matches[best_match_index]:  # If there is a match
            name = known_faces_names[best_match_index]  # Get the name

        if name and name not in face_names:  # If name is not empty and not in face names list
            face_names.append(name)  # Add name to face names list

        if name in students:  # If name is in students list
            students.remove(name)  # Remove name from students list
            print(students)  # Print updated students list
            current_time = now.strftime("%H-%M-%S")  # Get current time
            lnwriter.writerow([name, current_time])  # Write name and time to CSV file

        if name in known_faces_names:  # If name is in known face names list
            font = cv2.ACCESS_MASK  # Set font
            bottomLeftCornerOfText = (10, 100)  # Set position for text
            fontScale = 1.5  # Set font scale
            if name:  # If name is not empty
                fontColor = (0, 255, 0)  # Green color if present
            else:  # If name is empty
                fontColor = (0, 0, 255)  # Red color if absent
            thickness = 6  # Set text thickness
            lineType = 2  # Set line type

            cv2.putText(frame, name + ' Present', bottomLeftCornerOfText, font, fontScale, fontColor, thickness,
                        lineType)  # Put text on frame

    if len(face_locations) > 0:  # If there are face locations
        top, right, bottom, left = face_locations[0]  # Get face coordinates
        x_diff = right - left  # Calculate x difference
        y_diff = bottom - top  # Calculate y difference
        aspect_ratio = x_diff / y_diff  # Calculate aspect ratio
        if aspect_ratio > 1.9 or aspect_ratio < 1:  # If aspect ratio is not within range
            cv2.putText(frame, name + " Please keep your posture straight!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)  # Put posture warning on frame

    # Emotion detection
    frame = detect_emotions(frame)

    cv2.imshow("Advanced Attendance system ©Kushagra & Vaishnavi 2023", frame)  # Display frame
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed, break out of loop
        break

video_capture.release()  # Release video capture
f.close()  # Close CSV file
cv2.destroyAllWindows()  # Destroy all OpenCV windows


