from flask import Flask, request, render_template
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def hello():

    
    if request.method == 'POST':
        caption = request.form['caption']
        imageUrl = request.form['image_url']
        getDescriptionPrompt = "Explain the image in one to two sentences."
        # Connect to Together API
        client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
        try:
            stream = client.chat.completions.create(
                model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": getDescriptionPrompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": imageUrl,
                                },
                            },
                        ],
                    }
                ],
                stream=False,
            )

            common_sense_explanation = stream.choices[0].message.content.strip()
            prompt = f"Explain this caption: {caption} and this explanation that I got after image processing: {common_sense_explanation}, in just one sentence"
            
            stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                messages=[
                    {
                        "role" : "system",
                        "content" : "You are a helpful assistant who explains hidden sarcasm in images based on image explanations and captions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=512,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False  
            )
            
            result = stream.choices[0].message.content.strip()
            
            return render_template('index.html', result=result)

        except Exception as e:
            print(e)
            return "Error"
    
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
