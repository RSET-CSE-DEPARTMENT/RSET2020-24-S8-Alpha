import cv2
import numpy as np
from keras.models import model_from_json
from datetime import datetime

# Define emotion labels
emotion_labels = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]

# Load the pre-trained emotion detection model
json_file = open('D:\\Final Project\\Emotion_detection_with_CNN\\emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)
emotion_model.load_weights('D:\\Final Project\\Emotion_detection_with_CNN\\emotion_model.h5')
print("Loaded model from disk")

# Initialize the webcam feed
cap = cv2.VideoCapture(0)

# Initialize a list to store emotion scores
emotion_scores_history = []

# Initialize variables to count the number of frames for each emotion
emotion_frame_counts = {label: 0 for label in emotion_labels}

while True:
    # Read a frame from the webcam feed
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))

    # Break the loop if there is an issue with reading the frame
    if not ret:
        break

    print("Frame read successfully")

    # Detect faces in the frame
    face_detector = cv2.CascadeClassifier('D:\\Final Project\\Emotion_detection_with_CNN\\haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    print("Number of faces detected:", len(num_faces))

    # Process each detected face
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # Predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)

        # Store the emotion scores in the history list
        emotion_scores_history.append(emotion_prediction.reshape(-1))

        # Get the index of the predicted emotion
        predicted_emotion_index = np.argmax(emotion_prediction)
        predicted_emotion_label = emotion_labels[predicted_emotion_index]

        # Update the count for the predicted emotion
        emotion_frame_counts[predicted_emotion_label] += 1

        cv2.putText(frame, predicted_emotion_label, (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Display the frame with the bounding boxes and emotion labels
    cv2.imshow('Emotion Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Convert the emotion scores history list to a NumPy array for analysis
emotion_scores_array = np.array(emotion_scores_history)

# Calculate statistical measures (e.g., mean, standard deviation)
mean_emotion_scores = np.mean(emotion_scores_array, axis=0)
std_dev_emotion_scores = np.std(emotion_scores_array, axis=0)

# Find the most detected emotion
most_detected_emotion_index = np.argmax(np.sum(emotion_scores_array > 0.5, axis=0))
most_detected_emotion = emotion_labels[most_detected_emotion_index]
print("Most Detected Emotion:", most_detected_emotion)

# Generate a timestamp for the file names
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Save the results to the output.txt file with a timestamp
output_filename = f"output.txt"
with open(output_filename, "w") as file:
    file.write("Mean Emotion Scores: [")
    file.write(" ".join(f"{score:.4f} ({label})" for score, label in zip(mean_emotion_scores, emotion_labels)))
    file.write("]\n")

    file.write("Standard Deviation of Emotion Scores: [")
    file.write(" ".join(f"{score:.4f} ({label})" for score, label in zip(std_dev_emotion_scores, emotion_labels)))
    file.write("]\n")

    file.write("Most Detected Emotion: {}\n".format(most_detected_emotion))

    # Write the number of frames recognized for each emotion
    for label, count in emotion_frame_counts.items():
        file.write(f"Frames Recognized ({label}): {count}\n")

# Save the results to the compiled_output.txt file with a timestamp
compiled_output_filename = "compiled_output.txt"
with open(compiled_output_filename, "a") as file:
    file.write("\n\nResults at {}: \n".format(timestamp))

    file.write("Mean Emotion Scores: [")
    file.write(" ".join(f"{score:.4f} ({label})" for score, label in zip(mean_emotion_scores, emotion_labels)))
    file.write("]\n")

    file.write("Standard Deviation of Emotion Scores: [")
    file.write(" ".join(f"{score:.4f} ({label})" for score, label in zip(std_dev_emotion_scores, emotion_labels)))
    file.write("]\n")

    file.write("Most Detected Emotion: {}\n".format(most_detected_emotion))

    # Write the number of frames recognized for each emotion
    for label, count in emotion_frame_counts.items():
        file.write(f"Frames Recognized ({label}): {count}\n")

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
