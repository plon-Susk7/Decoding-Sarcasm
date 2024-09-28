from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Define the folder where your images are stored
image_folder = "./images"

@app.route('/images/<filename>')
def serve_image(filename):
    print(image_folder, filename)
    return send_from_directory(image_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
