from flask import Flask, request, jsonify
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials, db, storage
import uuid
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Initialize Firebase
cred = credentials.Certificate("time-61aca-firebase-adminsdk-j9cab-0bb5dd0706.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://time-61aca-default-rtdb.firebaseio.com/',
    'storageBucket': 'time-61aca.appspot.com'
})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Get additional input fields
    name = request.form.get('name')
    course = request.form.get('course')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Load the uploaded image
        image = face_recognition.load_image_file(filename)
        
        # Find all the faces in the image
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 0:
            os.remove(filename)  # Remove the file if no face is detected
            return jsonify({'error': 'No face detected in the image. Please upload an image containing a face.'}), 400
        elif len(face_locations) > 1:
            os.remove(filename)  # Remove the file if multiple faces are detected
            return jsonify({'error': 'Multiple faces detected. Please upload an image with only one face.'}), 400
        else:
            # Generate a unique ID for the user
            user_id = str(uuid.uuid4())

            # Upload image to Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f'user_images/{user_id}/{file.filename}')
            blob.upload_from_filename(filename)
            blob.make_public()

            # Save user data to Firebase Realtime Database
            user_ref = db.reference(f'users/{user_id}')
            user_ref.set({
                'name': name,
                'course': course,
                'image_url': blob.public_url
            })

            # Remove the temporary file
            os.remove(filename)

            return jsonify({
                'message': 'Face image and user data successfully uploaded and verified',
                'user_id': user_id
            }), 200

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<user_id>', methods=['GET'])
def download_image(user_id):
    # Get user data from Firebase Realtime Database
    user_ref = db.reference(f'users/{user_id}')
    user_data = user_ref.get()

    if not user_data or 'image_url' not in user_data:
        return jsonify({'error': 'User or image not found'}), 404

    image_url = user_data['image_url']

    # Instead of downloading the image, we'll just return the URL
    return jsonify({
        'message': 'Image URL retrieved successfully',
        'image_url': image_url,
        'user_data': user_data
    }), 200

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0')