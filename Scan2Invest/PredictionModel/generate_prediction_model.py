import tensorflow as tf
from keras.applications import MobileNetV2
from keras import layers, models
from keras.preprocessing.image import ImageDataGenerator
import os
# Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'Scan2Invest\\PredictionModel\\data\\train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    'Scan2Invest\\PredictionModel\\data\\validation',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Model Definition
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(27, activation='softmax')  # Adjust this to the number of classes
])

# Compile the Model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the Model
history = model.fit(
    train_generator,
    epochs=6,
    validation_data=validation_generator
)
current_folder = os.path.abspath(os.path.dirname(__file__))
os.makedirs(current_folder + "\prediction_model", exist_ok=True)
save_path = os.path.join(current_folder, "prediction_model\logo_recognition_model.keras")
print(f"FilePath {save_path}")
# Save the Model
model.save(save_path)
