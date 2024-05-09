import mysql.connector
import google.generativeai as genai
API_KEY = "AIzaSyChZs5zo4W5YAc3a5941Okd9aDx0sFw3Uk" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='major_project'
)

# Create a cursor object to execute queries
cursor = connection.cursor()

# Query to fetch emotion values and scores
sql = 'SELECT * FROM final_emotions'

# Execute the query
cursor.execute(sql)

# Fetch all rows of the result
results = cursor.fetchall()

# Close the cursor and connection
cursor.close()
connection.close()

# Process the fetched data
if results:
    data = results[0]  # Assuming there's only one row returned

    # Extract emotion scores and dominant emotion
    emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Neutral']
    scores = [data[1], data[2], data[3], data[4], data[5]]
    max_score = max(scores)
    max_score_index = scores.index(max_score)
    dominant_emotion = emotions[max_score_index]

    # print("Dominant Emotion:", dominant_emotion)
    # print("Dominant Score:", max_score)
    # print("\n")
else:
    print("No data found.")

#prompt = "joy:"+str(final_values[0])+" sadness:"+str(final_values[1])+" anger:"+str(final_values[2])+" fear:"+str(final_values[3])+" neutral:"+str(final_values[4])+" identify the emotion of the human subject from the above stats and recommend any 3 tasks accordingly to alleviate the subjects mental state"
prompt = "the mental state of the human subject is "+dominant_emotion+" suggest 3 tasks separated each other from numbers to alleviate the mental state of the subject."
#print(prompt)



response = model.generate_content(prompt)
tasks=response.text


task_list = tasks.strip().split("\n")

# Initialize variables to store tasks
task1 = ""
task2 = ""
task3 = ""

task_array = []

# Loop through each task and assign them to variables based on their number
for task in task_list:
    parts = task.split(".", 1)
    if len(parts) == 2:
        number, description = parts
        if number.strip() == "1":
            task1 = description.strip()
        elif number.strip() == "2":
            task2 = description.strip()
        elif number.strip() == "3":
            task3 = description.strip()

# Print the tasks stored in variables
print("Task 1:", task1)
print("Task 2:", task2)
print("Task 3:", task3)