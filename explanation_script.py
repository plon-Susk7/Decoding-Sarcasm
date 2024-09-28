from together import Together
import pandas as pd
import os
from tqdm import tqdm

def generate_explanations(file_name):

    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))


    print(file_name)
    getDescriptionPrompt = "Explain the image in one to two sentences."
    file_name = str(file_name)
    imageUrl = f"https://62b6-103-25-231-125.ngrok-free.app/images/{file_name}"
    # imageUrl = "https://napkinsdev.s3.us-east-1.amazonaws.com/next-s3-uploads/d96a3145-472d-423a-8b79-bca3ad7978dd/trello-board.png"


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

        print(stream)
        return stream.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return "Error"


if __name__ == '__main__':
    os.environ["TOGETHER_API_KEY"] = "*"
    image_files = os.listdir('./images')
    explanation_text = []
    for image_file in tqdm(image_files):
        explanation_text.append(generate_explanations(image_file))

    df = pd.DataFrame({'image': image_files, 'explanation': explanation_text})

    df.to_csv('explanations.csv', index=False)
