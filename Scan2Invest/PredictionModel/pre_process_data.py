import os
import shutil
import pandas as pd

# Create data structure
data_dir = 'Scan2Invest\\PredictionModel\\flickr_logos_27_dataset\\flickr_logos_27_dataset_images'
train_annotation_file = 'Scan2Invest\\PredictionModel\\flickr_logos_27_dataset\\flickr_logos_27_dataset_training_set_annotation.txt'
train_dir = 'Scan2Invest\\PredictionModel\\data\\train'
validation_dir = 'Scan2Invest\\PredictionModel\\data\\validation'

# Read annotations
annotations = pd.read_csv(train_annotation_file ,
                          sep=r'\s+',
                          header=None,
                          names=['filename', 'brand', 'some_number', 'x1', 'y1', 'x2', 'y2'])

print(annotations.head())
annotations = annotations.drop(columns=['some_number'])
annotations['brand'] = annotations['brand'].astype(str).str.replace(' ', '_')

# Creating brand directories under train and validation
brands = annotations['brand'].unique()
for brand in brands:
    os.makedirs(os.path.join(train_dir, brand), exist_ok=True)
    os.makedirs(os.path.join(validation_dir, brand), exist_ok=True)

# Split into train and validation and move files
split_ratio = 0.8  # 80% for training,
for brand in brands:
    brand_files = annotations[annotations['brand'] == brand]['filename'].unique()
    train_files = brand_files[:int(len(brand_files)*split_ratio)]
    validation_files = brand_files[int(len(brand_files)*split_ratio):]
    
    for file in train_files:
        shutil.copy(os.path.join(data_dir, file), os.path.join(train_dir, brand))
    for file in validation_files:
        shutil.copy(os.path.join(data_dir, file), os.path.join(validation_dir, brand))
