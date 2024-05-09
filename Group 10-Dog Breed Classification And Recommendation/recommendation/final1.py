import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to convert numerical representation back to text
def convert_numerical_to_text(concatenated_ascii):
    ascii_str = str(concatenated_ascii)
    ascii_codes = [int(ascii_str[i:i+3]) for i in range(0, len(ascii_str), 3)]
    text = ''.join(chr(code) for code in ascii_codes)
    return text

# Function to convert text to numerical representation
def convert_text_to_numerical(word):
    ascii_codes = [ord(char) for char in word]
    concatenated_ascii = int(''.join(map(str, ascii_codes)))
    return concatenated_ascii

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Query the database to retrieve dogs' details
cursor.execute("SELECT * FROM dogs")
dogs_data = cursor.fetchall()

# Convert the textual features to numerical representations and store in a list of dictionaries
dogs_data_numerical1 = []
dogs_data_numerical = []
for row in dogs_data:
    row_dict1 = {
        'id': row[0],  # Assuming the first column is the ID
        'breed': str(row[1]),
        'name':row[2],
        'gender': str(row[3]),
        'age': row[4],
        'height': row[8],
        'weight': row[9],
        'expectancy': row[10],
        'group': row[11],
        'grooming_frequency_value': row[12],
        'grooming_frequency_category': str(row[13]),
        'shedding_value': row[14],
        'shedding_category': str(row[15]),
        'energy_level_value': row[16],
        'energy_level_category': str(row[17]),
        'trainability_value': row[18],
        'trainability_category': str(row[19]),
        'demeanor_value': row[20],
        'demeanor_category': str(row[21]),
        'ps':0
    }
    row_dict = {
        #'id': row[0],  # Assuming the first column is the ID
        'breed': convert_text_to_numerical(str(row[1])),
        'gender': convert_text_to_numerical(str(row[3])),
        'age': row[4],
        'height': row[8],
        'weight': row[9],
        'expectancy': row[10],
        'group': convert_text_to_numerical(str(row[11])),
        'grooming_frequency_value': row[12],
        'grooming_frequency_category': convert_text_to_numerical(str(row[13])),
        'shedding_value': row[14],
        'shedding_category': convert_text_to_numerical(str(row[15])),
        'energy_level_value': row[16],
        'energy_level_category': convert_text_to_numerical(str(row[17])),
        'trainability_value': row[18],
        'trainability_category': convert_text_to_numerical(str(row[19])),
        'demeanor_value': row[20],
        'demeanor_category': convert_text_to_numerical(str(row[21]))
    }
    dogs_data_numerical.append(row_dict)
    dogs_data_numerical1.append(row_dict1)
    #print(dogs_data_numerical1)
# Convert user input to numerical representation
user_input = {'breed': 'Affenpinscher',
              'gender': 'female',
              'age': 8,
              'height': 45,
              'weight': 40,
              'group': 'HerdingGroup',
              'grooming_frequency_value': '0.4',
              'grooming_frequency_category': 'Weekly Brushing',
              'shedding_value': 0.8,
              'shedding_category': 'WeeklyBrushing',
              'energy_level_value': 0.8,
              'energy_level_category': 'RegularExercise',
              'trainability_value': 1.0,
              'trainability_category': 'EagertoPlease',
              'demeanor_value': 1,
              'demeanor_category': 'Alert/Responsive'}

user_input_numerical = {
    'breed': convert_text_to_numerical(user_input['breed']),
    'gender': convert_text_to_numerical(user_input['gender']),
    'age': user_input['age'],
    'height': user_input['height'],
    'weight': user_input['weight'],
    'group': convert_text_to_numerical(user_input['group']),
    'grooming_frequency_value': user_input['grooming_frequency_value'],
    'grooming_frequency_category': convert_text_to_numerical(user_input['grooming_frequency_category']),
    'shedding_value': user_input['shedding_value'],
    'shedding_category': convert_text_to_numerical(user_input['shedding_category']),
    'energy_level_value': user_input['energy_level_value'],
    'energy_level_category': convert_text_to_numerical(user_input['energy_level_category']),
    'trainability_value': user_input['trainability_value'],
    'trainability_category': convert_text_to_numerical(user_input['trainability_category']),
    'demeanor_value': user_input['demeanor_value'],
    'demeanor_category': convert_text_to_numerical(user_input['demeanor_category'])
}
# Compute similarity scores using cosine similarity
# Convert dogs_data_numerical and user_input_numerical to numpy arrays for compatibility with sklearn
dogs_data_numerical_array = np.array([list(row.values())[1:] for row in dogs_data_numerical])  # Exclude the 'id' column
user_input_numerical_array = np.array(list(user_input_numerical.values())).reshape(1, -1)  # Reshape to match sklearn input format
similarity_scores = cosine_similarity(dogs_data_numerical_array, user_input_numerical_array)

# Store results in a list of tuples with ID and similarity score
results = []
for i, row in enumerate(dogs_data_numerical1):
    row['ps'] = similarity_scores[i][0]
    results.append(row)

# Sort the results based on the 'ps' value in descending order
sorted_results = sorted(results, key=lambda x: x['ps'], reverse=True)

# Print the sorted results
# Print the sorted results with only the required fields
for row in sorted_results[:10]:
    print("Breed:", row['breed'])
    print("Gender:", row['gender'])
    print("Age:", row['age'])
    print("Height:", row['height'])
    print("Weight:", row['weight'])
    print("Group:", row['group'])
    print("Grooming Frequency Value:", row['grooming_frequency_value'])
    print("Grooming Frequency Category:", row['grooming_frequency_category'])
    print("Shedding Value:", row['shedding_value'])
    print("Shedding Category:", row['shedding_category'])
    print("Energy Level Value:", row['energy_level_value'])
    print("Energy Level Category:", row['energy_level_category'])
    print("Trainability Value:", row['trainability_value'])
    print("Trainability Category:", row['trainability_category'])
    print("Demeanor Value:", row['demeanor_value'])
    print("Demeanor Category:", row['demeanor_category'])
    print("ps:", row['ps'])
    print()  # Add a newline for better readability between records

