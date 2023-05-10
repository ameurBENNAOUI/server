import base64
import io
import json
import os

import flask
import requests



import base64
import datetime
import os
import tempfile

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
# from flask import current_app

from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = 'hello'



db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# db.create_all()


socketio = SocketIO(app)



@socketio.on('audio_data')
def handle_audio_data(data):
    # TODO: Implement real-time transcription here
    print(data)

    # Emit the transcribed text to the client
    emit('transcription', {'transcription': 'Transcribed text'})


@app.before_first_request
def setup_database():
    db.create_all()
    create_example_user()

def create_example_user():
    user_exists = User.query.filter_by(username='a').first()
    if user_exists is None:
        hashed_password = generate_password_hash('a')
        user = User(username='a', password=hashed_password)
        db.session.add(user)
        db.session.commit()





@app.route('/auth', methods=['POST'])
def authenticate():
    # return "aa"
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


# /////
@app.route('/auth/google', methods=['POST'])
def authenticate_with_google():
    data = request.get_json()
    name = data['name']
    email = data['email']

    # Check if the user exists in your database using their email
    user = User.query.filter_by(email=email).first()

    # If they don't exist, create a new user with the received name and email
    if user is None:
        hashed_password = generate_password_hash('')  # You can generate a random password or use an empty string
        user = User(username=name, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()

    # Generate an access token for the user
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


def save_audio(base64_data):
    # Decode the base64 data
    audio_data = base64.b64decode(base64_data)

    # Create a temporary directory if it doesn't exist
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)

    # Get the current timestamp as a string
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    # Write the data to a temporary file with a timestamp in the name
    file_path = os.path.join(temp_dir, f'audio_{timestamp}.mp3')
    with open(file_path, 'wb') as f:
        f.write(audio_data)

    # Return the path of the temporary file
    return file_path



job_services = [
    {
        "free_plan": False,
        "service_name":"Linkdin",
        "service": "linkedin",
        "logo": "/static/img/linkedin.png",
        "checked": False,
        "cost": 148
    },
    {
        "free_plan": True,
        "service_name":"Linkdin",

        "service": "linkdin",
        "logo": "/static/img/indeed.png",
        "checked": False,
        "cost": 0
    },
    {
        "free_plan": False,
        "service_name":"cv library",

        "service": "cv_library",
        "logo": "/static/img/cv_library.png",
        "checked": False,
        "cost": 50
    },
    
    
]

@app.route('/job_service', methods=['GET'])
def job_service():
    return jsonify(job_services)


schedular = {
    "social":["facebook", "instagram"],
    "schedular":[
    {
        "service_name":"Linkdin",
        "title": "social media text auto generated here ...",
        "image_url": "/static/img/schedular/1.jpg",
        "time": "Today ASAP",
    },
    {
        "service_name":"Linkdin",
        "title": "social media text auto generated here ...",
        "image_url": "/static/img/schedular/2.jpg",
        "time": "Today ASAP",
    },    
    {
        "service_name":"Linkdin",
        "title": "social media text auto generated here ...",
        "image_url": "/static/img/schedular/3.jpg",
        "time": "Today ASAP",
    },
     {
        "service_name":"Linkdin",
        "title": "social media text auto generated here ...",
        "image_url": "/static/img/schedular/4.jpg",
        "time": "Today ASAP",
    },
    
]}


@app.route('/schedular', methods=['GET'])
def schedular_service():
    return jsonify(schedular)


election = {
                "jobElection":"fgddf", 
                "isSwitched":True,
                # "isSwitched":True
                "premiumJob":    [
                {
                    "free_plan": False,
                    "service_name":"Linkdin",
                    "service": "linkedin",
                    "logo": "/static/img/linkedin.png",
                    "checked": False,
                    "cost": 148
                },

                {
                    "free_plan": False,
                    "service_name":"cv library",

                    "service": "cv_library",
                    "logo": "/static/img/cv_library.png",
                    "checked": False,
                    "cost": 50
                },
                
                
            ]
    }

@app.route('/election', methods=['GET'])
def election_service():!
    return jsonify(election)

success = {
                "jobElection":"fgddf", 
                # "isSwitched":True,
           
    }


@app.route('/success', methods=['GET'])
def success_service():
    return jsonify(success)



# app = flask.Flask(__name__)


# from flask import Flask, render_template


# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)



@app.route('/transcribe', methods=['POST'])
def transcribe():
    
    request_data = flask.request.data.decode()
    
    request_json = json.loads(request_data)

    audio_base64 = request_json.get('audio_data')
    # print(audio_base64)
    if not audio_base64:
        return flask.abort(400, 'No audio data found')
    
    
    audio_file = save_audio(audio_base64)


    
    try:

        transcription="As an IT Specialist, you will be responsible for providing technical support and assistance to our organization's computer systems, networks, and software applications. Your primary tasks will include troubleshooting hardware and software issues, setting up and maintaining computer systems, and ensuring the security and efficiency of our IT infrastructure."
        # transcription="jjjjjjjjjj"
        return {'transcription': transcription}
    except Exception as e:
        return flask.abort(500, str(e))



def transcribe_audio(audio_base64):
    api_key = os.environ['OPENAI_API_KEY']
    api_url = 'http://localhost:5000/transcribe'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {'audio_data': audio_base64}
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        raise Exception(f'OpenAI API returned {response.status_code}')
    
    return response.json()




@app.route('/text', methods=['POST'])
def text():
    
    # return {
    #     "ff":"kgkg"
    # }
    
    return {
  "numberOfHires": ["1", "2", "3"],
  "jobTitles": ["Developer", "Designer", "Manager"],
  "locations": ["New York", "Los Angeles", "Chicago"],
  "genericJobDetails": ["Full-time", "Part-time", "Freelance"],
  "industries": ["Software", "Design", "Marketing"],
  "postcode": "12345",
  "description": "Job description text..."
}


@app.route('/send_audio_and_data', methods=['POST'])
def send_audio_and_data():
    
    request_data = flask.request.data.decode()
    
    # request_json = json.loads(request_data)
    
    # print(request_data)
    
    return {
  "numberOfHires": ["1", "2", "3"],
  "jobTitles": ["Developer", "Designer", "Manager"],
  "locations": ["New York", "Los Angeles", "Chicago"],
  "genericJobDetails": ["Full-time", "Part-time", "Freelance"],
  "industries": ["Software", "Design", "Marketing"],
  "postcode": "12345",
  "description": "New Data Job description text..."
}    
    

    audio_base64 = request_json.get('audio_data')
    print(audio_base64)
    if not audio_base64:
        return flask.abort(400, 'No audio data found')
    
    
    audio_file = save_audio(audio_base64)


    
    try:

        transcription="As an IT Specialist, you will be responsible for providing technical support and assistance to our organization's computer systems, networks, and software applications. Your primary tasks will include troubleshooting hardware and software issues, setting up and maintaining computer systems, and ensuring the security and efficiency of our IT infrastructure."
        # transcription="jjjjjjjjjj"
        return {'transcription': transcription}
    except Exception as e:
        return flask.abort(500, str(e))







if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    
    #     # Add example user
    # hashed_password = generate_password_hash('example_password')
    # user = User(username='example_username', password=hashed_password)
    # db.session.add(user)
    # db.session.commit()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    # socketio.run(app, host='0.0.0.0', port=5000, debug=True)


