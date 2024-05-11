import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import PoseModule1 as pm1
import pickle   
import time  # Import the time module to work with time-related functions
import sqlite3
from datetime import date,datetime
from shared import uid as user_id
import shared
conn = sqlite3.connect('Fitness.db')
et=None
st=None
start_time=None
end_time=None
c = conn.cursor()
cur_date=date.today().strftime("%Y-%m-%d")
# Create the report table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS report (
                user_id TEXT,
                exercise TEXT,
                counter INTEGER,
                start_time TEXT,
                end_time Text,
                work_duration REAL,
                cur_date Text
            )''')

global prediction
# Define global variables to store start and end times
start_time = None
end_time = None
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
def calculate_angle(a,b,c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 

    radians = np.arctan2(c[1]-b[1], c[0]-b[0])-np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle>180.0:
        angle=360-angle
    
    return angle
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier


# from xgboost import XGBClassifier


# Importing visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
#matplotlib inline

np.random.seed(42)
df = pd.read_csv('/Users/aldrinsaji/Documents/train.csv')
# Drop pose_id column
df.drop('pose_id', axis=1, inplace=True)
df.head()
df.isnull().sum().sort_values(ascending=False)
df['exercise'] = np.nan

# If the pose contains the word 'squat' then the exercise is squats
df.loc[df['pose'].str.contains('squat'), 'exercise'] = 'squats'
df.loc[df['pose'].str.contains('jumping_jacks'), 'exercise'] = 'jumping jacks'
df.loc[df['pose'].str.contains('push_up'), 'exercise'] = 'push ups'
df.loc[df['pose'].str.contains('situp'), 'exercise'] = 'sit ups'
df.loc[df['pose'].str.contains('pullups'), 'exercise'] = 'pull ups'
# Checking the new column
df.head()
''' Creating a function that gets the data and cleans it for modeling'''

def get_data():
    # Bring in the data
    df = pd.read_csv('/Users/aldrinsaji/Documents/train.csv')
    # Drop pose_id column
    df.drop('pose_id', axis=1, inplace=True)
    # Creating a new column for the groups
    df['exercise'] = np.nan
    # If the pose contains the word 'squat' then the exercise is squats
    df.loc[df['pose'].str.contains('squat'), 'exercise'] = 'squats'
    df.loc[df['pose'].str.contains('jumping_jacks'), 'exercise'] = 'jumping jacks'
    df.loc[df['pose'].str.contains('pushup'), 'exercise'] = 'push ups'
    df.loc[df['pose'].str.contains('situp'), 'exercise'] = 'sit ups'
    df.loc[df['pose'].str.contains('pullups'), 'exercise'] = 'pull ups'
    # Dropping pose column
    df.drop('pose', axis=1, inplace=True)

    # going to use LabelEncoder to encode the exercise column
    # from sklearn.preprocessing import LabelEncoder
    # le = LabelEncoder()
    # df['exercise'] = le.fit_transform(df['exercise'])

    return df
df=get_data()
print(df.columns)
'''Creating a function that fit a Logistic Regression model and see the accuracy feature importance'''

def decision_tree():
    global start_time
    # Getting the data
    df = get_data()
    # Splitting the data into X and y
    X = df.drop('exercise', axis=1)
    y = df['exercise']
    # Splitting the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Creating a Decision Tree model
    decision_tree = DecisionTreeClassifier()
    # Fitting the model
    decision_tree.fit(X_train, y_train)
    # Getting the accuracy score
    print('The accuracy score is: ', accuracy_score(y_test, decision_tree.predict(X_test)))
    # Creating a confusion matrix
    print('The confusion matrix is: ', confusion_matrix(y_test, decision_tree.predict(X_test)))
    # Creating a classification report
    print('The classification report is: ', classification_report(y_test, decision_tree.predict(X_test)))
    # Putting the feature importance into a dataframe
    feature_importance = pd.DataFrame(decision_tree.feature_importances_, index=X.columns, columns=['Importance'])
    
    # Sorting the values to include top 20
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False).head(20)

    # Plotting the feature importance
    # plt.figure(figsize=(10, 10))
    # sns.barplot(x=feature_importance['Importance'], y=feature_importance.index)
    # plt.title('Feature Importance')
    # plt.xlabel('Importance')
    # plt.ylabel('Feature')
    # plt.show()
    return decision_tree 
tree_model = decision_tree()
def write_landmarks_to_csv(landmarks, frame_number, csv_data):
    print(f"Landmark coordinates for frame {frame_number}:")
    for idx, landmark in enumerate(landmarks):
        print(f"{mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        csv_data.append([frame_number, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])
    print("\n")
global frame_number
frame_number=0
global csv_data
csv_data=[]
existing_window = None
class VideoPlayer:
    def __init__(self, master, video_source):
        self.master = master
        self.video_source = video_source

        # self.canvas = tk.Canvas(master, width=640, height=480)
        # self.canvas.pack()

        self.cap = cv2.VideoCapture(self.video_source)
        
        # self.prediction_label = tk.Label(master, text="Predicted Exercise:", bg="green", fg="white", font=("Arial", 16))
        # self.prediction_label.place(x=10, y=10)  # Adjust the position as needed

        self.display_video()
    def display_video(self): 
        ret, frame = self.cap.read()
        global count
        global prediction,start_time,end_time
        prediction=None
        global frame_number,csv_data  
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                # Recolor img to RGB
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img.flags.writeable = False
                # Make detection
                results = pose.process(img)
            
                # Recolor back to BGR
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    # print(landmarks)
                except:
                    pass
                
                # Render detections
                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) )               
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    # Add the landmark coordinates to the list and print them
                    write_landmarks_to_csv(results.pose_landmarks.landmark, frame_number, csv_data)


                frame_number += 1
                data_list = [
                    [1, 'action1', 0.1, 0.2, 0.3],
                    [2, 'action2', 0.4, 0.5, 0.6],
                    [3, 'action3', 0.7, 0.8, 0.9]
                ]

                # Initialize an empty dictionary to store the data
                data_dict = {}

                # Iterate through each element in the data list
                for row in csv_data:
                    # Extract index, action, and coordinates
                    index = row[0]
                    action = row[1].lower()
                    x, y, z = row[2:]
                    
                    # Construct column names
                    x_col = f'x_{action}'
                    y_col = f'y_{action}'
                    z_col = f'z_{action}'
                    
                    # Add data to the dictionary
                    if index not in data_dict:
                        data_dict[index] = {}
                    data_dict[index][x_col] = x
                    data_dict[index][y_col] = y
                    data_dict[index][z_col] = z

                # Convert the dictionary to a pandas DataFrame
                df = pd.DataFrame.from_dict(data_dict, orient='index')

                # Reset index to make index a regular column
                #df.reset_index(inplace=True)

                # Rename the index column to 'index'
                #df.rename(columns={'index': 'Index'}, inplace=True)

                # Display the DataFrame
                print(df)
                #df = df
                #print(df.head)
                #df
                #X = df.drop('index', axis=1)
                #y = df['exercise']
                # print(f"output:{y}")
                x=df[:1]
                # Debugging code to inspect input data before prediction
                # Debugging code to inspect intermediate steps
                prediction = tree_model.predict(x)
                print(f"predicted: {tree_model.predict(x)}")
                cv2.rectangle(img, (0, 0), (400, 78), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, prediction[0], (25,30), cv2.FONT_HERSHEY_PLAIN,3,
                                        (255, 0, 0), 5)
                # self.prediction_label.config(text="Predicted Exercise: " + tree_model.predict(x))  # Assuming prediction[0] contains the predicted exercise
                
                csv_data=[] 
                # if frame_number==100:
                #     break
                cv2.imshow('Mediapipe self.cap', img)
                csv_data=[]
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()
        csv_data
        np.shape(csv_data)
        global end_time
        if prediction is not None and prediction[0] == 'push ups':
                    self.cap = cv2.VideoCapture(self.video_source)
                    start_time = time.time() 
                    st = datetime.now().strftime('%H:%M:%S')
                    detector = pm.poseDetector()
                    count = 0
                    direction = 0
                    form = 0
                    feedback = "Fix Form"


                    while self.cap.isOpened():
                        ret, img = self.cap.read() #640 x 480
                        #Determine dimensions of video - Help with creation of box in Line 43
                        width  = self.cap.get(3)  # float `width`
                        height = self.cap.get(4)  # float `height`
                        # print(width, height)
                        
                        img = detector.findPose(img, False)
                        lmList = detector.findPosition(img, False)
                        # print(lmList)
                        if len(lmList) != 0:
                            elbow = detector.findAngle(img, 11, 13, 15)
                            shoulder = detector.findAngle(img, 13, 11, 23)
                            hip = detector.findAngle(img, 11, 23,25)
                            
                            #Percentage of success of pushup
                            per = np.interp(elbow, (90, 160), (0, 100))
                            
                            #Bar to show Pushup progress
                            bar = np.interp(elbow, (90, 160), (380, 50))

                            #Check to ensure right form before starting the program
                            if elbow > 160 and shoulder > 40 and hip > 160:
                                form = 1
                        
                            #Check for full range of motion for the pushup
                            if form == 1:
                                if per == 0:
                                    if elbow <= 90 and hip > 160:
                                        feedback = "Up"
                                        if direction == 0:
                                            count += 0.5
                                            direction = 1
                                    else:
                                        feedback = "Fix Form"
                                        
                                if per == 100:
                                    if elbow > 160 and shoulder > 40 and hip > 160:
                                        feedback = "Down"
                                        if direction == 1:
                                            count += 0.5
                                            direction = 0
                                    else:
                                        feedback = "Fix Form"
                                            # form = 0
                                    
                                        
                        
                            print(count)
                            
                            #Draw Bar
                            if form == 1:
                                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                                            (255, 0, 0), 2)


                            #Pushup counter
                            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                                        (255, 0, 0), 5)
                            
                            #Feedback 
                            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
                            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                            cv2.rectangle(img, (0, 0), (400, 78), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, prediction[0], (25,30), cv2.FONT_HERSHEY_PLAIN,3,
                                        (255, 0, 0), 5)
                            
                        cv2.imshow('Pushup counter', img)
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            end_time = time.time()

                                # Convert the time in seconds to a datetime object
                            et = datetime.now().strftime('%H:%M:%S') 
                            break
                    if start_time is not None and end_time is not None:
                        workout_duration = end_time - start_time
                        print("Workout duration:", workout_duration, "seconds")
                    self.cap.release()
                    cv2.destroyAllWindows()
        if prediction is not None and prediction[0]=='sit ups':
                    self.cap = cv2.VideoCapture(self.video_source)
                    start_time = time.time() 
                    st = datetime.now().strftime('%H:%M:%S')
                    global counter
                    global state
                    global range_flag
                    global halfway
                    global body_angles
                    form=0
                    counter = 0
                    state = 'Down'
                    range_flag = True
                    halfway = False
                    feedback = ''
                    frame_count = 0
                    # Plotting variables
                    frames = []
                    left_angle = []
                    right_angle = []
                    body_angles = []
                    WIDTH = 10000
                    HEIGHT = 10000
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
                    width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    with mp_pose.Pose(min_detection_confidence=50, min_tracking_confidence=50) as pose:
                        while self.cap.isOpened():
                            ret, frame = self.cap.read()
                            frame_count += 1
                            frames.append(frame_count)
                            # Mirror frame
                            frame = cv2.flip(frame, 1)
                            # Recolor img from BGR to RGB
                            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img.flags.writeable = False
                            
                            # Pose detection
                            detection = pose.process(img)
                            # Recolor img from RGB back to BGR
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img.flags.writeable = True

                            # Render detections
                            mp_drawing.draw_landmarks(img, detection.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                            
                            try: 
                                landmarks = detection.pose_landmarks.landmark
                                
                                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                                left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                                # CALCULATE ANGLES 
                                angle_knee = calculate_angle(left_hip, left_knee, left_heel)
                                angle_body = calculate_angle(left_shoulder, left_hip, left_knee)
                                body_angles.append(int(angle_body))
                                per = np.interp(elbow, (90, 160), (0, 100))
                            
                            #Bar to show Pushup progress
                                bar = np.interp(elbow, (90, 160), (380, 50))
                            
                                if (angle_body < 80 and angle_body > 50) and state == "Down": #Half-way there (Used for checking bad situps)
                                    halfway = True
                                    form=1

                                if angle_body < 40 and state == "Down": #Complete situp
                                    state = "Up"
                                    range_flag = True
                                    form=1
                                    
                                if angle_body > 90 and angle_knee < 60: #Resting position;to check if situp was done properly
                                    state = "Down"
                                    
                                    if halfway: #Check if a rep was attempted
                                        if range_flag: #Check if a proper rep was performed
                                            counter += 1
                                            feedback = "Good repetition!"
                                            form=1
                                        else:
                                            feedback = "Did not perform sit up completely."
                                            form=0
                                        range_flag = False #Reset vars
                                        halfway = False
                                        
                                if angle_knee > 70: #Triggers anytime the legs are not tucked in
                                    feedback = "Keep legs tucked in closer"
                                    form=0

                            except: 
                                body_angles.append(180)
                            print(counter)
                            
                            #Draw Bar
                            if form == 1:
                                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                                            (255, 0, 0), 2)


                            #Pushup counter
                            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, str(int(counter)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                                        (255, 0, 0), 5)
                            
                            #Feedback 
                            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
                            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                                        (0, 255, 0), 2)

                            
                            cv2.imshow('Pushup counter', img)
                            if cv2.waitKey(10) & 0xFF == ord('q'):
                                end_time = time.time()

                                # Convert the time in seconds to a datetime object
                                et = datetime.now().strftime('%H:%M:%S')
                                break
                    self.cap.release()
                    cv2.destroyAllWindows()
        if start_time is not None and end_time is not None:
                        workout_duration = end_time - start_time
                        print("Workout duration:", workout_duration, "seconds")  
        print("COUNT:",count)
        print("Exercise:",prediction[0]) 
        counter = count
        c.execute("INSERT INTO report (user_id, exercise, counter, start_time,end_time,work_duration,cur_date) VALUES (?, ?, ?,?,?,?, ?)",
          (shared.uid, prediction[0], counter, st,et,workout_duration,cur_date))
# start_time TEXT,
#                 end_time Text,
#                 work_duration REAL,
#                 cur_date Text
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.master.after(10, self.display_video)

def delete():
    print(shared.uid)
    print("Exercise:") 
    global existing_window  # Declare the variable as global to modify it inside the function
    global start_time, end_time
    start_time = None  # Reset start time when a new video is opened
    end_time = None
    if existing_window and existing_window.winfo_exists():  # Check if the existing window exists and is not closed
        existing_window.destroy()
    # global window
    print("Exercise:") 
    window = tk.Toplevel()
    window.title("Video Player")
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected file:", file_path)
    video_source = file_path  # Change this to the path of your video file

    VideoPlayer(window, video_source)
    window.protocol("WM_DELETE_window", on_close)

    existing_window = window  

    window.mainloop()
def on_close():
    global existing_window  # Declare the variable as global to modify it inside the function
    if existing_window:
        existing_window.destroy()  # Destroy the existing window
    existing_window = None  # Reset the reference to the existing window
# delete()
