from openai import OpenAI
import base64
from PIL import Image
import io

client = OpenAI(
    base_url="http://127.0.0.1:8045/v1",
    api_key="sk-faa2293c43b4415abd74d7a60d3f5f6d"
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

input_image_path = "input-low.jpg"
base64_image = encode_image(input_image_path)

response = client.chat.completions.create(
    model="gemini-3.1-pro-high",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Create a JSON list containing the vertex coordinates of all the top faces of the wooden dodecahedra."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    extra_body={"modalities": ["text"]}
)

response_message = response.choices[0].message

if response_message.content:
    print(response_message.content)
