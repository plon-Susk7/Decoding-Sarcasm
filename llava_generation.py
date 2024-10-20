import os
import json
from PIL import Image
import torch
from transformers import LlavaNextForConditionalGeneration, LlavaNextProcessor
from tqdm import tqdm 


model = LlavaNextForConditionalGeneration.from_pretrained(
    "llava-hf/llama3-llava-next-8b-hf",
    torch_dtype=torch.float16,
    load_in_4bit=True,
    device_map="auto",
    token='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'
)

processor = LlavaNextProcessor.from_pretrained("llava-hf/llama3-llava-next-8b-hf")
processor.tokenizer.padding_side = "left"

image_folder = os.path.join(os.getcwd(), "images") 


output_file = os.path.join(os.getcwd(), "anxiety_train_llava.json")  

prompt_template = (
    '''Instruction: Analyze the following sarcastic meme image to extract common sense reasoning. 
    These relationships should capture the following elements:

    1. Cause-Effect: Identify concrete causes or results of the situation depicted in the meme.
    2. Figurative Understanding: Capture underlying metaphors, analogies, or symbolic meanings that convey the meme's deeper message, including any ironic or humorous undertones.
    '''
)


results = {}

for filename in tqdm(os.listdir(image_folder), desc="Processing images"):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, filename)
        
        image = Image.open(image_path)
        
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_template},
                    {"type": "image"},
                ],
            },
        ]


        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

        inputs = processor(text=prompt, images=image, return_tensors="pt")

        generate_ids = model.generate(**inputs.to('cuda', torch.float16), max_new_tokens=200, temperature=0.00001)


        output = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        output = output.split("assistant")[1]

        print(output)

        results[filename] = output

with open(output_file, "w") as f:
    json.dump(results, f, indent=4)

print(f"Output has been saved to {output_file}")
