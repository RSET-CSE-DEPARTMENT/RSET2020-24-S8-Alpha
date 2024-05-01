from flask import Flask, jsonify,request
from flask_cors import CORS
# from flask import session
# from flask_session import Session
from PIL import Image
import numpy as np
import cv2
import tensorflow as tf
import hashlib
# import sys
# from keras.models import load_model
from keras import Model
from keras.layers import Input,Conv2D, PReLU,BatchNormalization,UpSampling2D,add
import io
# import os
import base64
from base64 import b64encode
from json import dumps
# from gevent.pywsgi import WSGIServer

import sqlite3

def create_user_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_user_table()

def create_images_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  image_data BLOB NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

create_images_table()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def res_block(ip):

    res_model = Conv2D(64, (3,3), padding = "same")(ip)
    res_model = BatchNormalization(momentum = 0.5)(res_model)
    res_model = PReLU(shared_axes = [1,2])(res_model)

    res_model = Conv2D(64, (3,3), padding = "same")(res_model)
    res_model = BatchNormalization(momentum = 0.5)(res_model)

    return add([ip,res_model])

def upscale_block(ip):

    up_model = Conv2D(256, (3,3), padding="same")(ip)
    up_model = UpSampling2D( size = 2 )(up_model)
    up_model = PReLU(shared_axes=[1,2])(up_model)

    return up_model

def create_gen(gen_ip, num_res_block):
    layers = Conv2D(64, (9,9), padding="same")(gen_ip)
    layers = PReLU(shared_axes=[1,2])(layers)

    temp = layers

    for i in range(num_res_block):
        layers = res_block(layers)

    layers = Conv2D(64, (3,3), padding="same")(layers)
    layers = BatchNormalization(momentum=0.5)(layers)
    layers = add([layers,temp])

    layers = upscale_block(layers)
    layers = upscale_block(layers)

    op = Conv2D(3, (9,9), padding="same")(layers)

    return Model(inputs=gen_ip, outputs=op)


app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config["SESSION_PERMANENT"] = True
# app.config['SECRET_KEY'] = '%@6aq47jjB6D!A9h'
# Session(app)
CORS(app)


@app.route('/image', methods=['POST'])
def upload_image():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'})

    file = request.files['file']
    userName = request.form.get('userName')

    #fetch user id#########################
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (userName,))
    user = c.fetchone()
    user_id=user[0]
    conn.close()
    #######################################

    img = Image.open(file)
    img = img.convert("RGB")

    im_x,im_y=img.size
    # print(im_x)
    # print(im_y)
    lr_ip = Input(shape=(im_x,im_x,3))
    generator = create_gen(lr_ip, num_res_block = 16)
    generator.summary()


    img=np.array(img)
    # img = img[:, :, ::-1].copy()
    X1 = cv2.resize(img,(im_x,im_x), interpolation = cv2.INTER_AREA)
    X = np.reshape(X1, (1,im_x,im_x, 3))
    X_batch = tf.cast(X, tf.float32)


    generator.load_weights('./models/test_2000_divflickreffnet_gen_e_50.h5')
    Y = generator(X_batch/255)

    # img_array = np.array(img) / 255.0
    # img_array = np.expand_dims(img_array, axis=0)

    
    # print(f"array shape : {np.array(img_array).shape}")

    # prediction = model.predict(img_array)
    output=Y[0] * 255
    processed_image = Image.fromarray((np.clip(output, 0, 255).astype(np.uint8)).astype(np.uint8))
    if (im_x!=im_y):
        processed_image = processed_image.resize((im_x*4,im_y*4),Image.LANCZOS)

    img_bytes = io.BytesIO()

    processed_image.save(img_bytes, format='PNG')

    #Insert image into database#######################
    blob_data = img_bytes.getvalue()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM images WHERE user_id = ? AND image_data = ?", (user_id, blob_data,))
    count = c.fetchone()[0]
    if(count>0):
        message="error : Image already exists"
    else:
        try:
            c.execute("INSERT INTO images (user_id, image_data) VALUES (?, ?)", (user_id, blob_data))
            conn.commit()
            message = {'message': 'Image inserted successfully'}
        except Exception as e:
            conn.rollback()
            message = {'error': f'Error inserting image: {str(e)}'}
        finally:
            conn.close()

    print(message)
    ###################################################

    base64_bytes = b64encode(img_bytes.getvalue())

    base64_string = base64_bytes.decode('utf-8')

    raw_data = {'image': base64_string}

    json_data = dumps(raw_data, indent=2)

    return json_data
    

@app.route('/display', methods=['POST'])
def display_images():
    data = request.json
    username = data.get('userName')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT image_data FROM images INNER JOIN users ON images.user_id = users.id WHERE users.username = ?", (username,))
    images = c.fetchall()
    conn.close()

    base64_images = [b64encode(image[0]).decode('utf-8') for image in images]

    return jsonify(base64_images)

@app.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.json
    image_to_delete = data.get('image')
    image_to_delete_bytes = base64.b64decode(image_to_delete)
    username = data.get('userName')  

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM images WHERE user_id = (SELECT id FROM users WHERE username = ?) AND image_data = ?", (username, image_to_delete_bytes,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Image deleted successfully'})


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('email')
    password = data.get('password')

    hashed_password = hash_password(password)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}),401
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    
    if user:
        stored_hashed_password = user[2]  # Assuming the hashed password is stored in the third column
        
        entered_hashed_password = hash_password(password)
        
        if stored_hashed_password == entered_hashed_password:
            # session['user_id'] = user[0]  # Assuming the user ID is stored in the first column

            # user_id = session.get('user_id')
            # print("User ID:", user_id)
            # print(user[0])
            return jsonify({'message': 'Login successful', 'user_name': username})
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    # user_id = session.get('user_id')
    # print("User ID:", user_id)
    # if 'user_id' in session:
    #     session.pop('user_id')  # Remove user ID from session
    
    # # Optionally, you can clear the entire session if needed
    # session.clear()  # Clear all session data
    # g.username=""
    
    return jsonify({'message': 'Logout successful'})
      
if __name__ == '__main__':
    app.run(debug=False)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()



