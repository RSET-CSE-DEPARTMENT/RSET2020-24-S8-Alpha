import asyncio
import websockets
import json
import mysql.connector

async def hello(websocket, path):
    # Receive data from the client
    data = await websocket.recv()
    # Parse the JSON data received
    data_dict = json.loads(data)
    text = data_dict.get('text', '')
    website = data_dict.get('website', '')
    timestamp = data_dict.get('timestamp', '')

    # Print the received data
    print(f"Received data from client - Text: {text}, Website: {website}, Timestamp: {timestamp}")


    
# Configure your MySQL connection
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '12345',
        'database': 'major_project',
    }

    # Create a connection to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    #@app.route('/storeData', methods=['POST'])
    #def store_data():
    #   try:
    #      data = request.get_json()
    #     text = data['text']
        #    website = data['website']
        #   timestamp = data['timestamp']
        #  print(f"Received Text: {text}, Website: {website}, Timestamp: {timestamp}")

    # Check the website and choose the appropriate table
    if website == 'www.instagram.com':
        table_name = 'insta_data'
    elif website == 'www.facebook.com':
        table_name = 'fb_data'
    elif website == 'www.reddit.com':
        table_name = 'reddit_data'
    elif website == 'www.google.com':
        table_name = 'google_data'
    else:
        table_name = 'other_data'

    # Store the text into the appropriate MySQL table
    insert_query = f'INSERT INTO {table_name} (text,timestamp,processed) VALUES (%s,%s,%s);'
    cursor.execute(insert_query, (text,timestamp,"NO"))
    conn.commit()

    response = {'success': True, 'message': 'Text received and stored successfully'}
    


#------------------------------------------------------------

start_server = websockets.serve(hello, '0.0.0.0', 8765)

print("WebSocket server is waiting for connections...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# app.py
#from flask import Flask, request, jsonify
#from flask_cors import CORS


#app = Flask(__name__)
#CORS(app)  # Enable CORS for all routes


#    except Exception as e:
 #       print(f"Error: {e}")
  #      response = {'success': False, 'message': 'Error processing the request'}
   #     return jsonify(response), 500

#if __name__ == '__main__':
 #   app.run(host='localhost', port=5000)



#--------------------------------------------------------------
    # Send a response back to the client
   # response = "Data received successfully!"
    #await websocket.send(response)

#start_server = websockets.serve(hello, '0.0.0.0', 8765)

#print("WebSocket server is waiting for connections...")

#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()
