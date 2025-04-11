# Contextual Alt-Text Generator 🖼️📝

A research-driven tool to generate **context-aware alt-text** for images by combining object detection with contextual paragraph summarization. This project aims to improve accessibility by producing meaningful, descriptive alt-text based on the **image content** and its surrounding **textual context**.

## Inspiration

Traditional alt-text generation often lacks **contextual understanding**, leading to generic or unhelpful captions. This project builds on models like **ClipCap** and methods proposed in [Alt-Text with Context (arXiv:2305.14779)](https://arxiv.org/abs/2305.14779), extending them by incorporating both image features and **contextual paragraph summaries** to generate better captions.

---

## Features

- 📸 **Object Detection** via Image Captioning Models
- 🧠 **Context Summarization** using NLP models
- 🔗 **Image-Context Fusion** OpenAI Integration
- 🧾 **Generate high-quality**, contextual alt-text for accessibility
- 😛 **Aggregated Dataset**, comprised of 1000 images, text, and alt-text

---
## Evaluation Dataset

Composed of 1000 items with each item containing full article text, related image header, and alt-text of the image.

All data points were collected via the New York Times API and additional web scraping for alignment of image-text pairs.

Note: Due to copyright restrictions, we cannot release the full dataset. However, we provide:

---

## Technologies

- Python
- PyTorch
- FastAPI
- PostgreSQL
- Hugging Face Transformers (vit-gpt2	clipcap	blip	blip2 | t5 pegasus flanT5 bart)
- OpenAI CLIP / CLIPCap
- Jupyter Notebooks 

---

## Acknowledgments

ClipCap (https://arxiv.org/abs/2111.09734)
Alt-Text with Context [(arXiv:2305.14779)](https://arxiv.org/abs/2305.14779)
Hugging Face Transformers
OpenAI 
