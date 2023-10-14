import tensorflow as tf
import numpy as np
from PIL import Image

# Replace with the path to your model
MODEL_PATH = 'prediction_model\logo_recognition_model.keras'

# Replace with the path to the image you want to predict
IMAGE_PATH = 'data\\validation\\Starbucks\\2421111243.jpg'

# Load the pre-trained model
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels in order they were trained on, replace with actual labels
CLASS_LABELS = [
    "Adidas", "Apple", "BMW", "Citroen", "Cocacola",
    "DHL", "Fedex", "Ferrari", "Ford", "Google",
    "Heineken", "HP", "Intel", "McDonalds", "Mini",
    "Nbc", "Nike", "Pepsi", "Porsche", "Puma",
    "RedBull", "Sprite", "Starbucks", "Texaco", "Unicef",
    "Vodafone", "Yahoo"
]

# Load, resize and preprocess the image
img = Image.open(IMAGE_PATH)
img = img.resize((224, 224))  # Replace with size model was trained on
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.  # If model was trained with normalized images

# Model prediction
predictions = model.predict(img_array)

# Getting the predicted class label
predicted_class = CLASS_LABELS[np.argmax(predictions[0])]
confidence = np.max(predictions[0])

# Displaying the result
print(f"The image is most likely the Brand: {predicted_class} with {confidence*100:.2f}% confidence. \n")

# Getting top 5 predictions
top_5_indices = np.argsort(predictions[0])[-5:][::-1]  # Get indices of top 5 predictions
top_5_labels = [CLASS_LABELS[i] for i in top_5_indices]  # Get label names
top_5_confidence = [predictions[0][i] for i in top_5_indices]  # Get confidence scores

# Displaying the confidence score for top 5 predictions
print("Top 5 Brand predictions:")
for i in range(5):
    print(f"{top_5_labels[i]}: {top_5_confidence[i]*100:.2f}%")


