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



app = flask.Flask(__name__)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    
    request_data = flask.request.data.decode()
    # print(request_data)
    
    request_json = json.loads(request_data)

    # Get the audio file from the request
    audio_base64 = request_json.get('audio_data')
    print(audio_base64)
    if not audio_base64:
        return flask.abort(400, 'No audio data found')
    
    
    audio_file = save_audio(audio_base64)

    # print (flask.request.files)
    # Get the audio file from the request
    # file = flask.request.files['audio']
    # if not file:
    #     return flask.abort(400, 'No audio file found')
    # audio_bytes = file.read()
    
    # # Convert the audio to base64
    # audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # Call the OpenAI API
    try:
        # response = transcribe_audio(audio_base64)
       
        # transcription = response['transcription']
        
        transcription="jjjjjjjjjj"
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
