import os
import json
import numpy as np
from descriptor import glcm, bitdesc

def process_datasets(root_folder):
    all_features = []
    
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                folder_name = os.path.basename(os.path.dirname(image_path))
                features = glcm(image_path)
                all_features.append(features + [folder_name, image_path])

    with open('signatures.json', 'w') as f:
        json.dump(all_features, f)

if __name__ == '__main__':
    process_datasets('datasets/database')
