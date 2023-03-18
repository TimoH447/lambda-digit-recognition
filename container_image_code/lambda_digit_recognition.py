print('outside')
import json
import os
import io
import boto3
import numpy as np
from PIL import Image

import tensorflow as tf


# Function to preprocess image
def preprocess_image(image):
    # Convert image to grayscale
    image = image.convert('L')
    # Resize image to 28x28
    image = image.resize((28, 28))
    # Convert image to array
    image = np.array(image) / 255.0
    image = image.astype('float32')
    # Reshape image to a 4D tensor with shape (1, 28, 28, 1)
    image = np.reshape(image, (1, 28, 28))
    return image

def handler(event, context):
    print("Start handler")
    # Get the bucket and key from the S3 event object
    bucket = event['bucket']
    key = event['image_key']
    print(key)
    print(bucket)
    
    
    # Download image from S3
    # Initialize S3 client
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    print(response)
    img_bytes = response['Body'].read()
    image = Image.open(io.BytesIO(img_bytes))
    
    # Preprocess image
    image = preprocess_image(image)
    
    print('model')
    # Download the TensorFlow model from S3
    model_bucket = 'sudoku-solver-bucket'
    model_key = 'models/digit_model.h5'
    model_response = s3.download_file(Bucket=model_bucket, Key=model_key,Filename='/tmp/digit_model.h5')
    print(model_response)
    #model_bytes = model_response['Body'].read()
    
    # Load the saved model from memory
    model = tf.keras.models.load_model('/tmp/digit_model.h5')
    
    print('start prediction')
    # Use the model to predict the digit
    prediction = model.predict(image)
    predicted_digit = np.argmax(prediction)
    predicted_digit=int(predicted_digit)
    print(predicted_digit)
    
    # Return the predicted digit
    return {
        'statusCode': 200,
        'body': json.dumps({
            'predicted_digit': predicted_digit
        })
    }