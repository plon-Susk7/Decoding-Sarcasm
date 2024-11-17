from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        # Get text input
        text_data = request.form['text_input']

        # Handle image upload
        image = request.files.get('image_file')
        if image:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            # You can process the image and text here as needed
            # For example, process image_path and text_data
            result = f"Image saved at {image_path}, Text: {text_data}"

        return render_template('index.html', result=result)
    
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
