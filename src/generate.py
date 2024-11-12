import torch
import os
from dotenv import load_dotenv
from clipcap import GenerateClipCap
from models import GenerateBLIP, GenerateT5, GenerateBART, GeneratePEGASUS, GenerateGPT2, GenerateFlanT5
from pathlib import Path
from openai import OpenAI
from transformers import pipeline

device = 'cuda' if torch.cuda.is_available() else 'cpu'
curr_path = Path(__file__).parent.absolute()

def create_summary(text: str, model: str) -> str:
    if model == "BART":
        summarizer = GenerateBART()
        summarized_text = summarizer.predict(text)
    elif model == "PEGASUS":
        summarizer = GeneratePEGASUS()
        summarized_text = summarizer.predict(text)
    elif model == "T5":
        summarizer = GenerateT5()
        summarized_text = summarizer.predict(text)
    elif model == "FlanT5":
        summarizer = GenerateFlanT5()
        summarized_text = summarizer.predict(text)
    
    print(f"Summarized Text: {summarized_text}")

    del summarizer
    torch.cuda.empty_cache()
    return summarized_text

def create_caption(img_path: Path, model: str) -> str:
    if model == "BLIP":
        vision_transformer = GenerateBLIP()
        image_caption = vision_transformer.predict(img_path)
    elif model == "GPT2":
        vision_transformer = GenerateGPT2()
        image_caption = vision_transformer.predict(img_path)
    elif model == "CLIPCAP":
        vision_transformer = GenerateClipCap()
        image_caption = vision_transformer.predict(img_path, 'coco', False)

    print(f"Image Caption: {image_caption}")

    del vision_transformer
    torch.cuda.empty_cache()
    return image_caption


def create_alttext(text: str, img_path: Path, image: bool, vision_model: str, nlp_model: str):
    summary = create_summary(text, nlp_model)
    caption = create_caption(img_path, vision_model)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
    
    if not api_key:
        raise ValueError("API Key Missing!")
    client = OpenAI(
            api_key = api_key
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You have two inputs - Summary Context and Image Caption. Create an alt-text from these two inputs. Take note that the image caption might not be accurate. Use only straightforward descriptive language. Avoid terms that imply symbolism. Find correlations between the two inputs. Max character limit is 125 characters."},
            {
                "role": "user",
                "content": f"SUMMARY CONTEXT: {summary}. IMAGE CAPTION: {caption}"
            }
        ]
    )

    print(f"Generated Alt-Text: {completion.choices[0].message.content}")

    return {"alt-text": completion.choices[0].message.content, "image-caption": caption}
