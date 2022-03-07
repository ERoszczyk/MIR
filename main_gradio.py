# tutorial: https://gradio.app/image_classification_in_tensorflow/
import tensorflow as tf
import requests
import gradio as gr
import cv2

def classify_image(image):
  image = image.reshape((-1, 224, 224, 3))
  image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
  prediction = inception_net.predict(image).flatten()
  confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
  return confidences

def convert_photo_to_Sketch(image):
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
    return sketch

def photo_actions(image):
    return classify_image(image), convert_photo_to_Sketch(image)

if __name__ == "__main__":
    inception_net = tf.keras.applications.MobileNetV2()
    response = requests.get("https://git.io/JJkYN") # human-readable labels for ImageNet
    labels = response.text.split("\n")
    gr.Interface(fn=photo_actions, 
             inputs=gr.inputs.Image(shape=(224, 224)),
             outputs=[
             gr.outputs.Label(num_top_classes=3),
             gr.outputs.Image(label='Sketched Image',type='pil'),
             ],
             examples=["./photos_examples/apple.jpg", "./photos_examples/cat.jpg"]).launch()
