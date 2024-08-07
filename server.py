from flask import Flask, request, jsonify
import os
import sys
import numpy as np
import json
from descriptor import glcm, bitdesc
from distances import euclidean, manhattan, chebyshev, canberra

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    top_k = int(request.form.get('top_k', 10))  # Default to 10 if not provided
    descriptor = request.form.get('descriptor', 'GLCM')
    distance = request.form.get('distance', 'Manhattan')
    upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Extract features based on the chosen descriptor
    if descriptor == 'GLCM':
        query_features = glcm(file_path)
    elif descriptor == 'BitDesc':
        query_features = bitdesc(file_path)
    else:
        return jsonify({'error': 'Invalid descriptor choice'}), 400

    # Load the precomputed signatures

    try:
        with open('signatures.json', 'r') as file:
            signatures = json.load(file)
    except FileNotFoundError:
        return jsonify({'error': 'Signatures file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding JSON'}), 500


    #signatures = np.load('signatures.json')

    # Perform the search based on the chosen distance
    try:
        similar_images = calculate_distances(signatures, query_features, distance, top_k)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    # Calculate the class distribution
    class_distribution = {}
    for result in similar_images:
        class_name = result['class']
        if class_name in class_distribution:
            class_distribution[class_name] += 1
        else:
            class_distribution[class_name] = 1

    return jsonify({'similar_images': similar_images, 'class_distribution': class_distribution})

def calculate_distances(signature_db, query_features, distance_type, num_results):
    distances = []
    for instance in signature_db:
        signature_features, label, img_path = instance[:-2], instance[-2], instance[-1]
        if distance_type == 'Manhattan':
            dist = manhattan(query_features, signature_features)
        elif distance_type == 'Euclidean':
            dist = euclidean(query_features, signature_features)
        elif distance_type == 'Chebyshev':
            dist = chebyshev(query_features, signature_features)
        elif distance_type == 'Canberra':
            dist = canberra(query_features, signature_features)
        else:
            raise ValueError('Invalid distance type')
        distances.append({'image_path': img_path, 'distance': dist, 'class': label})
    distances.sort(key=lambda x: x['distance'])
    return distances[:num_results]

if __name__ == '__main__':
    app.run(debug=True, port=5001)
