import mysql.connector
import google.generativeai as genai
API_KEY = "AIzaSyChZs5zo4W5YAc3a5941Okd9aDx0sFw3Uk" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


# Function to connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="major_project"
    )

# Function to fetch emotion values for a given day
def fetch_insta_emotion_values_for_day(date):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute SQL query to fetch emotion values for a given day
    query = "SELECT joy, sadness, anger, fear, neutral FROM insta_results WHERE DATE(date) = %s"
    cursor.execute(query, (date,))
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return rows

# Function to normalize emotion values for a given day


def fetch_fb_emotion_values_for_day(date):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute SQL query to fetch emotion values for a given day
    query = "SELECT joy, sadness, anger, fear, neutral FROM fb_results WHERE DATE(date) = %s"
    cursor.execute(query, (date,))
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return rows




def fetch_reddit_emotion_values_for_day(date):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute SQL query to fetch emotion values for a given day
    query = "SELECT joy, sadness, anger, fear, neutral FROM reddit_results WHERE DATE(date) = %s"
    cursor.execute(query, (date,))
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return rows


def fetch_google_emotion_values_for_day(date):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute SQL query to fetch emotion values for a given day
    query = "SELECT joy, sadness, anger, fear, neutral FROM google_results WHERE DATE(date) = %s"
    cursor.execute(query, (date,))
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return rows




def normalize_emotion_values(emotion_values):
    num_entries = len(emotion_values)
    total_emotions = [0.0] * 5  # Initialize list to store total emotion values
    
    # Calculate total emotion values
    for row in emotion_values:
        for i in range(5):
            total_emotions[i] += float(row[i])
    
    # Normalize emotion values
    normalized_values = [total_emotions[i] / num_entries for i in range(5)]
    
    return normalized_values


def combine_normalized_values(insta_values, fb_values, reddit_values):
    combined_values = [0.0] * 5  # Initialize list to store combined emotion values
    
    # Apply weights for Instagram (1st and 5th elements)
    combined_values[0] += ((insta_values[0] * 0.6 + fb_values[0] * 0.2 + reddit_values[0] * 0.2)) 
    combined_values[1] += ((insta_values[1] * 0.1 + fb_values[1] * 0.6 + reddit_values[1] * 0.3))
    combined_values[2] += ((insta_values[2] * 0.1 + fb_values[2] * 0.6 + reddit_values[2] * 0.3)) 
    combined_values[3] += ((insta_values[3] * 0.1 + fb_values[3] * 0.6 + reddit_values[3] * 0.3)) 
    combined_values[4] += ((insta_values[4] * 0.6 + fb_values[4] * 0.2 + reddit_values[4] * 0.2)) 

    
    return combined_values



# Example usage
if __name__ == "__main__":
    date = "2024-04-12"  # Specify the date for which you want to normalize emotion values
    insta_emotion_values = fetch_insta_emotion_values_for_day(date)
    fb_emotion_values = fetch_fb_emotion_values_for_day(date)
    reddit_emotion_values = fetch_reddit_emotion_values_for_day(date)
    google_emotion_values = fetch_google_emotion_values_for_day(date)
    if insta_emotion_values:
        insta_normalized_values = normalize_emotion_values(insta_emotion_values)
        print("Normalized Emotion Values for instagram", date)
        print("Joy:", insta_normalized_values[0])
        print("Sadness:", insta_normalized_values[1])
        print("Anger:", insta_normalized_values[2])
        print("Fear:", insta_normalized_values[3])
        print("Neutral:", insta_normalized_values[4])
    
    if fb_emotion_values:
        fb_normalized_values = normalize_emotion_values(fb_emotion_values)
        print("Normalized Emotion Values for facebook", date)
        print("Joy:", fb_normalized_values[0])
        print("Sadness:", fb_normalized_values[1])
        print("Anger:", fb_normalized_values[2])
        print("Fear:", fb_normalized_values[3])
        print("Neutral:", fb_normalized_values[4])

    
    if reddit_emotion_values:
        reddit_normalized_values = normalize_emotion_values(reddit_emotion_values)
        print("Normalized Emotion Values for reddit", date)
        print("Joy:", reddit_normalized_values[0])
        print("Sadness:", reddit_normalized_values[1])
        print("Anger:", reddit_normalized_values[2])
        print("Fear:", reddit_normalized_values[3])
        print("Neutral:", reddit_normalized_values[4])


    # if google_emotion_values:
    #     google_normalized_values = normalize_emotion_values(google_emotion_values)
    #     print("Normalized Emotion Values for google", date)
    #     print("Joy:", reddit_normalized_values[0])
    #     print("Sadness:", reddit_normalized_values[1])
    #     print("Anger:", reddit_normalized_values[2])
    #     print("Fear:", reddit_normalized_values[3])
    #     print("Neutral:", reddit_normalized_values[4])


    final_values = combine_normalized_values(insta_normalized_values, fb_normalized_values, reddit_normalized_values)
    print("Normalized Final Emotion Values for", date)
    print("Joy:", final_values[0])
    print("Sadness:", final_values[1])
    print("Anger:", final_values[2])
    print("Fear:", final_values[3])
    print("Neutral:", final_values[4])


    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute SQL query to fetch emotion values for a given day
    query = "insert into final_emotions(date,joy,sadness,anger,fear,neutral) values (%s,%s,%s,%s,%s,%s);"
    cursor.execute(query, (date,str(final_values[0]),str(final_values[1]),str(final_values[2]),str(final_values[3]),str(final_values[4])))

    connection.commit()
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()



    #else:
        #print("No emotion values found for", date)
