import pandas as pd
import sqlite3

# Read data from CSV file into a DataFrame
csv_file = 'dogprofiles.csv'  # Replace 'your_csv_file.csv' with the path to your CSV file
df = pd.read_csv(csv_file)

# Establish connection to SQLite database
conn = sqlite3.connect('database.db')  # Creates a new SQLite database named 'dogs_database.db'
cursor = conn.cursor()

# Create a table to store the data
create_table_query = '''
CREATE TABLE Dogs (
    ID INT PRIMARY KEY,
    Breed TEXT,
    Name TEXT,
    Gender TEXT,
    Age INT,
    Description TEXT,
    Temperament TEXT,
    Temperament_Score FLOAT,
    Height FLOAT,
    Weight FLOAT,
    Expectancy INT,
    GroupName TEXT,
    Grooming_Frequency_Value INT,
    Grooming_Frequency_Category TEXT,
    Shedding_Value INT,
    Shedding_Category TEXT,
    Energy_Level_Value INT,
    Energy_Level_Category TEXT,
    Trainability_Value INT,
    Trainability_Category TEXT,
    Demeanor_Value INT,
    Demeanor_Category TEXT
);
'''
cursor.execute(create_table_query)

# Insert data from DataFrame into the table
df.to_sql('Dogs', conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted successfully into the database.")
