import tensorflow as tf

# Define the path to the input and output files
input_model_path = 'digit_model.h5'
output_model_path = 'digit_model.tflite'

# Load the Keras model
model = tf.keras.models.load_model(input_model_path)

# Convert the model to a TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model to disk
with open(output_model_path, 'wb') as f:
  f.write(tflite_model)