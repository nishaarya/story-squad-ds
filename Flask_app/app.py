from decouple import config
from flask import Flask, jsonify, request
from google.cloud import vision
import urllib.request, json
from google.oauth2 import service_account


def create_app():
    app = Flask(__name__)
    
    with urllib.request.urlopen(config('GOOGLE_APPLICATION_CREDENTIALS')) as url:
        data = json.loads(url.read().decode())
    data = service_account.Credentials.from_service_account_info(data)

    @app.route('/')
    def root(methods=['POST']):
        uri = request.args['image_location']

        def transcribe(uri):
            """Detects document features in the file located in Google Cloud
            Storage."""
            client = vision.ImageAnnotatorClient(credentials=data)
            image = vision.types.Image()
            image.source.image_uri = uri
            response = client.document_text_detection(image=image)

            return response.text_annotations[0].description
        
        response = {'Transcription':  transcribe(uri)}
        
        return jsonify(response)
        

    return app