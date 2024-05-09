import pickle
from flask import Flask, request, redirect, url_for, jsonify
from keras.models import load_model
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words
import numpy as np
from gensim import models
from flask_cors import CORS

import nltk
# nltk.download('punkt')

en_stop = get_stop_words('en')

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route("/", methods=["GET"])
def main():
    return jsonify(
        {
            "description": "Welcome to the API!",
            "message": "Please use the form on the Nextjs frontend (http://localhost:3000)",
        }
    )

@app.route("/api/predict", methods=["GET", "POST"])
def predict():
    model2 = models.KeyedVectors.load_word2vec_format('model/GoogleNews-vectors-negative300.bin', binary=True)
    model_textual = load_model('model/model_textual.h5')
    with open('model/Genredict.pckl', 'rb') as f:
        Genre_ID_to_name = pickle.load(f)

    genre_list = sorted(list(Genre_ID_to_name.keys()))
    
    if request.method == "POST":
        name = request.form["name"]
        country = request.form["country"]
        message = request.form["message"]

        tokens = word_tokenize(message.lower())

        print("Tokens:", tokens)

        stopped_tokens = [token for token in tokens if token not in en_stop]
        print("Stopped Tokens:", stopped_tokens)

        word_vectors = []
       
        for token in stopped_tokens:
            encoded_token = token.encode('utf-8')
            if encoded_token in model2.key_to_index:
                word_vectors.append(model2[encoded_token])
            else:
                print(f"Token '{token}' not found in model2's vocabulary")

        print("Number of valid tokens:", len(word_vectors))
        
        if not word_vectors:
            return jsonify({"error": "No valid tokens found in input message"})
        
        input_vectors = np.mean(word_vectors, axis=0).reshape(1, -1)

        if input_vectors.shape != (1, 300):
            return jsonify({"error": "Invalid input shape"})
        
        predicted_genres = model_textual.predict(input_vectors)
        top_predicted_genres_indices = np.argsort(predicted_genres[0])[-3:]
        predicted_genres_list = [Genre_ID_to_name[genre_list[index]] for index in top_predicted_genres_indices]
        first_predicted_genre = predicted_genres_list[0]

        return jsonify({
            "name": name,
            "country": country,
            "prediction": first_predicted_genre,
        })

    else:
        return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()



# import pickle
# from flask import Flask, request, redirect, url_for, jsonify

# # Create an instance of the Flask class
# # with the name of the application’s modules
# app = Flask(__name__, template_folder="templates")


# # Create the / API route to return a welcome message
# @app.route("/", methods=["GET"])
# def main():
#     return jsonify(
#         {
#             "description": "Welcome to the MBPTI API!",
#             "message": "Please use the form on the Nextjs frontend (http://localhost:3000)",
#         }
#     )


# # Create the /predict API route
# @app.route("/api/predict", methods=["GET", "POST"])
# def predict():
#     # Use pickle to load in vectorizer.
#     with open(f"./model/vectorizer.pkl", "rb") as f:
#         vectorizer = pickle.load(f)

#     # Use pickle to load in the pre-trained model.
#     with open(f"./model/model.pkl", "rb") as f:
#         model = pickle.load(f)

#     if request.method == "POST":
#         name = request.form["name"]
#         country = request.form["country"]
#         message = request.form["message"]

#         mbpti_types = {
#             0: "ENFJ (Extroversion, Intuition, Feeling, Judging)",
#             1: "ENFP (Extroversion, Intuition, Feeling, Perceiving)",
#             2: "ENTJ (Extroversion, Intuition, Thinking, Judging)",
#             3: "ENTP (Extroversion, Intuition, Thinking, Perceiving)",
#             4: "ESFJ (Extroversion, Sensing, Feeling, Judging)",
#             5: "ESFP (Extroversion, Sensing, Feeling, Perceiving)",
#             6: "ESTJ (Extroversion, Sensing, Thinking, Judging)",
#             7: "ESTP (Extroversion, Sensing, Thinking, Perceiving)",
#             8: "INFJ (Introversion, Intuition, Feeling, Judging)",
#             9: "INFP (Introversion, Intuition, Feeling, Perceiving)",
#             10: "INTJ (Introversion, Intuition, Thinking, Judging)",
#             11: "INTP (Introversion, Intuition, Thinking, Perceiving)",
#             12: "ISFJ (Introversion, Sensing, Feeling, Judging)",
#             13: "ISFP (Introversion, Sensing, Feeling, Perceiving)",
#             14: "ISTJ (Introversion, Sensing, Thinking, Judging)",
#             15: "ISTP (Introversion, Sensing, Thinking, Perceiving)",
#         }

#         prediction = model.predict(vectorizer.transform([message]))
#         result = mbpti_types[prediction[0]]

#     else:
#         return redirect(url_for("main"))

#     return {
#         "name": name,
#         "country": country,
#         "prediction": result,
#     }


# if __name__ == "__main__":
#     app.run()