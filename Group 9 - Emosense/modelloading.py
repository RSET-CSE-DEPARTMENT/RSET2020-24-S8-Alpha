import ktrain
import mysql.connector
from datetime import datetime
import tensorflow as tf
from transformers import AutoTokenizer
import numpy as np
#import mysql.connector
#from datetime import datetime

# Load the saved predictor
predictor = ktrain.load_predictor(r"C:\Users\Dell\Desktop\emotiondetection\bert_model")
loaded_model = tf.saved_model.load(r"C:\Users\Dell\Desktop\hatespeech\hatespeechmodelfinal")

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

# Define a dictionary to map predicted class indices to their corresponding labels
predict_score_and_class_dict = {
    0: 'Hate Speech',
    1: 'Offensive Language',
    2: 'Neither'
}

# Connect to MySQL database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'major_project',
}

conn = mysql.connector.connect(**db_config)

# Define class names
class_names = ['joy', 'sadness', 'fear', 'anger', 'neutral']

try:
    with conn.cursor() as cursor:
        # Process insta_data
        query = "SELECT text FROM insta_data WHERE processed != 'YES'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                text = row[0]
                # Perform emotion detection on the text
                predictions = predictor.predict_proba(text)
                # Convert predictions to strings
                predictions_str = [str(prob) for prob in predictions]
                # Update processed field to 'YES' for the processed sentence
                inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
                # Perform inference using the loaded model
                preds = loaded_model(inputs)['logits']
                # Get the predicted class index
                class_preds = np.argmax(preds, axis=1)
                update_query = "UPDATE insta_data SET processed = 'YES' WHERE text = %s"
                cursor.execute(update_query, (text,))
                # Insert predictions into insta_results table
                insert_query = "INSERT INTO insta_results (date, joy, sadness, fear, anger, neutral) VALUES (NOW(), %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, tuple(predictions_str))
                insert_query = "INSERT INTO insta_hate (date, text, hate_speech) VALUES (NOW(), %s, %s)"
                cursor.execute(insert_query, (text, predict_score_and_class_dict[class_preds[0]]))
            conn.commit()
            print("Processed insta_data successfully.")
    
    with conn.cursor() as cursor:
        # Process fb_data
        query = "SELECT text FROM fb_data WHERE processed != 'YES'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                text = row[0]
                predictions = predictor.predict_proba(text)
                predictions_str = [str(prob) for prob in predictions]
                inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
                # Perform inference using the loaded model
                preds = loaded_model(inputs)['logits']
                # Get the predicted class index
                class_preds = np.argmax(preds, axis=1)
                update_query = "UPDATE fb_data SET processed = 'YES' WHERE text = %s"
                cursor.execute(update_query, (text,))
                insert_query = "INSERT INTO fb_results (date, joy, sadness, fear, anger, neutral) VALUES (NOW(), %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, tuple(predictions_str))
                insert_query = "INSERT INTO fb_hate (date, text, hate_speech) VALUES (NOW(), %s, %s)"
                cursor.execute(insert_query, (text, predict_score_and_class_dict[class_preds[0]]))
            conn.commit()
            print("Processed fb_data successfully.")
    
    with conn.cursor() as cursor:
        # Process reddit_data
        query = "SELECT text FROM reddit_data WHERE processed != 'YES'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                text = row[0]
                predictions = predictor.predict_proba(text)
                predictions_str = [str(prob) for prob in predictions]
                inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
                # Perform inference using the loaded model
                preds = loaded_model(inputs)['logits']
                # Get the predicted class index
                class_preds = np.argmax(preds, axis=1)
                update_query = "UPDATE reddit_data SET processed = 'YES' WHERE text = %s"
                cursor.execute(update_query, (text,))
                insert_query = "INSERT INTO reddit_results (date, joy, sadness, fear, anger, neutral) VALUES (NOW(), %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, tuple(predictions_str))
                insert_query = "INSERT INTO reddit_hate (date, text, hate_speech) VALUES (NOW(), %s, %s)"
                cursor.execute(insert_query, (text, predict_score_and_class_dict[class_preds[0]]))
            conn.commit()
            print("Processed reddit_data successfully.")


    with conn.cursor() as cursor:
        # Process reddit_data
        query = "SELECT text FROM google_data WHERE processed != 'YES'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                text = row[0]
                predictions = predictor.predict_proba(text)
                predictions_str = [str(prob) for prob in predictions]
                inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
                # Perform inference using the loaded model
                preds = loaded_model(inputs)['logits']
                # Get the predicted class index
                class_preds = np.argmax(preds, axis=1)
                update_query = "UPDATE google_data SET processed = 'YES' WHERE text = %s"
                cursor.execute(update_query, (text,))
                insert_query = "INSERT INTO google_results (date, joy, sadness, fear, anger, neutral) VALUES (NOW(), %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, tuple(predictions_str))
                insert_query = "INSERT INTO google_hate (date, text, hate_speech) VALUES (NOW(), %s, %s)"
                cursor.execute(insert_query, (text, predict_score_and_class_dict[class_preds[0]]))
            conn.commit()
            print("Processed google_data successfully.")

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    # Close the database connection
    conn.close()


