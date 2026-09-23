import os

import gradio as gr
import pandas as pd
from dotenv import load_dotenv

from src.detector import ObjectDetector
from src.languages import SCHEDULED_LANGUAGES
from src.translator import GoogleTranslator

load_dotenv()

MODEL_NAME = os.getenv("YOLO_MODEL", "yolo26n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.40"))
API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")

detector = ObjectDetector(
    model_name=MODEL_NAME,
    confidence_threshold=CONFIDENCE_THRESHOLD,
)

translator = GoogleTranslator(API_KEY) if API_KEY else None


def process_image(image):
    if image is None:
        return pd.DataFrame(columns=["Object", "Confidence", "Language", "Translation", "Status"])

    detections = detector.detect(image)

    if not detections:
        return pd.DataFrame(
            [{
                "Object": "-",
                "Confidence": "-",
                "Language": "-",
                "Translation": "No objects detected above the confidence threshold.",
                "Status": "no_detection",
            }]
        )

    rows = []

    for detection in detections:
        object_name = detection["object"]
        confidence = detection["confidence"]

        if translator is None:
            for language in SCHEDULED_LANGUAGES:
                rows.append({
                    "Object": object_name,
                    "Confidence": round(confidence, 3),
                    "Language": language["name"],
                    "Translation": "Configure GOOGLE_TRANSLATE_API_KEY",
                    "Status": "missing_api_key",
                })
            continue

        translations = translator.translate_all(object_name)

        for language in SCHEDULED_LANGUAGES:
            result = translations[language["name"]]
            rows.append({
                "Object": object_name,
                "Confidence": round(confidence, 3),
                "Language": language["name"],
                "Translation": result["translation"],
                "Status": result["status"],
            })

    return pd.DataFrame(rows)


with gr.Blocks(title="Indian Object Translator") as demo:
    gr.Markdown(
        """
        # 🇮🇳 Indian Object Translator

        Upload an image. YOLO identifies objects using English labels,
        then the labels are translated into India's 22 Scheduled Languages.

        **Note:** Google currently does not list Kashmiri and Santali in its
        documented NMT language list. Those rows are shown explicitly as
        `google_unsupported`.
        """
    )

    with gr.Row():
        image = gr.Image(type="pil", label="Upload Image")

    run_button = gr.Button("Detect & Translate", variant="primary")

    output = gr.Dataframe(
        headers=["Object", "Confidence", "Language", "Translation", "Status"],
        datatype=["str", "number", "str", "str", "str"],
        interactive=False,
        label="Results",
    )

    run_button.click(
        fn=process_image,
        inputs=image,
        outputs=output,
    )

    gr.Markdown(
        """
        ### Configuration

        Set `GOOGLE_TRANSLATE_API_KEY` in `.env` before running locally.
        For Colab, use a Colab Secret instead of putting the key in notebook code.
        """
    )


if __name__ == "__main__":
    demo.launch()
