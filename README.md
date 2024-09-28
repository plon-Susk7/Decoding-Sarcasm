## Dataset

1. Get dataset from the following link : https://drive.google.com/file/d/1CR3JIvatybTm3J3ZqLpZ4npq7OyHtcZf/view
2. Extract the dataset and save it in directory named images

## Generate Explanation

1. Run server.py to create a local server. The server contains an endpoint that provides a url for an image in images directory.
```
python server.py
```
2. Use ngrok to make the endpoint visible to together.ai.
```
ngrok https://localhost:5000
```
3. Run the explanation_generator file to generate explanation for all the sarcastic images.
```
python explanation_script.py
```
