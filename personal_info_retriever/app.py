from flask import Flask, request, render_template
import face_recognition
import os
from googlesearch import search

app = Flask(__name__)

# Step 1: Load Known Faces
known_faces = []
known_names = []

# Load images from the known_faces directory
known_faces_dir = 'known_faces'
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(os.path.splitext(filename)[0])  # Use the filename as the name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    # Process the image directly without saving
    person_name = identify_person(file)  # Pass the file directly
    personal_info = get_person_info(person_name)
    
    return render_template('result.html', name=person_name, info=personal_info)

def identify_person(file):
    # Load and encode the uploaded image for recognition
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)
    
    if len(face_encodings) > 0:
        # Compare with known faces
        matches = face_recognition.compare_faces(known_faces, face_encodings[0])
        if True in matches:
            first_match_index = matches.index(True)
            return known_names[first_match_index]
    
    return "Unknown"  # If no match found

def get_person_info(name):
    query = name
    info = []
    for i, url in enumerate(search(query, num_results=10)):
        info.append(url)
        if i >= 9:  # Limit to 10 results
            break
    return info

if __name__ == '__main__':
    app.run(debug=True)
