
import tensorflow as tf
import tensorflow_hub as hub
import sklearn.preprocessing
import json
import warnings
import tensorflow_text as text
import numpy as np
import csv


# Assuming label_binarizer is defined somewhere in your code
label_binarizer = sklearn.preprocessing.LabelBinarizer()
classes = ['Acne', 'Allergy', 'Arthritis', 'Bronchial Asthma', 'Cervical Spondylosis', 'Chicken Pox', 'Common Cold', 'Dengue', 'Diabetes', 'Dimorphic Hemorrhoids', 'Drug Reaction', 'Fungal Infection', 'Gastroesophageal Reflux Disease', 'Hypertension', 'Impetigo', 'Jaundice', 'Malaria', 'Migraine', 'Peptic Ulcer Disease', 'Pneumonia', 'Psoriasis', 'Typhoid', 'Urinary Tract Infection', 'Varicose Veins']

# Load the trained model
model = tf.keras.models.load_model(r'C:\Users\HP\Desktop\medibot\mymodels')

# Assuming label_binarizer.classes_ is not available, manually set the classes list
label_binarizer.classes_ = classes

# Assuming your prediction function remains the same, using label_binarizer.classes_
def predict_with_test_results(symptoms):
    feature = {'text': symptoms}
    input_dict = {name: tf.convert_to_tensor([value]) for name, value in feature.items()}
    predictions = model.predict(input_dict, verbose=0)
    
    # Assuming predictions has shape (2, 1, 24)
    predictions_array = np.array(predictions)
    
    predictions_dict = {}
    for i in range(len(classes)):
        # Access elements along axis 2 (24 elements)
        predictions_dict[classes[i]] = predictions_array[0][0][i] * 100

    sorted_predictions = sorted(predictions_dict.items(), key=lambda x: x[1], reverse=True)
    predictions_dict = dict(sorted_predictions)
    
    count = 0
    finaldisease=""
    for disease, prediction in predictions_dict.items():
        if count == 1:
            break
        print(f"Based on the symptoms provided, there exists a {prediction:.2f}% chance that you are suffering from {disease}\n")
        finaldisease=disease

        count += 1

    return finaldisease


# Now you can use predict_with_test_results(symptoms) function to get predictions
symptoms = input("Enter symptoms: ")
disease = predict_with_test_results(symptoms)
print(disease)


# ------To find the test for the disease------

def find_test_for_disease(csv_file, disease):
    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == disease:
                    return row[1]  # Assuming the test information is in the second column
        return None  # Return None if disease not found in the CSV
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

csv_file_path = r'C:\Users\HP\Desktop\medibot\test.csv'

test_result = find_test_for_disease(csv_file_path, disease)
if test_result:
    print(f"The recommended test for {disease} is {test_result}")
else:
    print(f"No test information found for {disease}.")


# --------- To map the test to its attributes --------

def mapping_test(csv_file, test):
    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == test:
                    return row[1]  # Assuming the test information is in the second column
        return None  # Return None if disease not found in the CSV
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

csv_file_path = r'C:\Users\HP\Desktop\medibot\test-details.csv'

test_attributes = find_test_for_disease(csv_file_path, test_result)
print(test_attributes)


