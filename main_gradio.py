# tutorial: https://gradio.app/image_classification_in_tensorflow/
import tensorflow as tf
import requests
import gradio as gr

def classify_image(inp):
  inp = inp.reshape((-1, 224, 224, 3))
  inp = tf.keras.applications.mobilenet_v2.preprocess_input(inp)
  prediction = inception_net.predict(inp).flatten()
  confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
  return confidences

if __name__ == "__main__":
    inception_net = tf.keras.applications.MobileNetV2()
    response = requests.get("https://git.io/JJkYN") # human-readable labels for ImageNet
    labels = response.text.split("\n")
    gr.Interface(fn=classify_image, 
             inputs=gr.inputs.Image(shape=(224, 224)),
             outputs=gr.outputs.Label(num_top_classes=3),
             examples=["./photos_examples/apple.jpg", "./photos_examples/cat.jpg"]).launch()
