import os
import sys
import io
import requests
import replicate

from config import REPLICATE_API_TOKEN

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

token = REPLICATE_API_TOKEN
client = replicate.Client(api_token=token)

amazon_img_path = "pinterest reference user/amazon.jpg"

print("[Test] Testing Image-to-Image Product Control on Replicate...")

prompt = (
    "A luxury aesthetic room photo of the 2-pack bird table lamps on a marble tabletop "
    "beside stacked white Kinfolk books and a white ribbed ceramic flower vase with dried white flowers, "
    "warm ambient wall moulding background lighting, soft bokeh, 8k resolution, photorealistic."
)

models_to_try = [
    ("black-forest-labs/flux-depth-pro", {
        "prompt": prompt,
        "control_image": open(amazon_img_path, "rb"),
        "output_format": "jpg"
    }),
    ("black-forest-labs/flux-dev", {
        "prompt": prompt,
        "image": open(amazon_img_path, "rb"),
        "prompt_strength": 0.60,
        "aspect_ratio": "3:4",
        "output_format": "jpg",
        "output_quality": 95
    })
]

for model_name, model_input in models_to_try:
    try:
        print(f"[Test] Trying model: {model_name}...")
        output = client.run(model_name, input=model_input)
        
        # Handle FileOutput or URL
        if isinstance(output, list) and len(output) > 0:
            img_url = str(output[0])
        elif hasattr(output, "url"):
            img_url = output.url
        else:
            img_url = str(output)
            
        print(f"[Test] Output URL from {model_name}: {img_url}")
        
        # Download and save test output
        res = requests.get(img_url)
        save_name = f"output/images/test_{model_name.replace('/', '_')}.jpg"
        with open(save_name, "wb") as f:
            f.write(res.content)
        print(f"[Test] Saved rendered image to: {save_name}")
        break

    except Exception as e:
        print(f"[Test] Model {model_name} failed: {e}")
