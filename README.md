# Indian Object Translator

A hands-on AI project that:

1. Accepts an image.
2. Uses YOLO object detection to identify objects in English.
3. Translates each detected object label into India's 22 Scheduled Languages.
4. Uses Google Cloud Translation Basic/v2 as the translation provider.
5. Provides a Gradio web UI.
6. Includes a Google Colab notebook for step-by-step experimentation.

## Architecture

```text
                 Image
                   |
                   v
             +-----------+
             |    YOLO   |
             | detection |
             +-----+-----+
                   |
             English labels
                   |
                   v
          +-------------------+
          | Translation Layer |
          +---------+---------+
                    |
                    v
             Google Cloud
             Translation API
                    |
                    v
       22 Scheduled Languages
                    |
                    v
              Gradio UI
```

## Important Google Cloud note

Google Cloud Translation is a cloud service and may require billing/credits depending on your account and current Google Cloud terms. This project uses the Basic/v2 REST API with an API key for simplicity.

Google's current language documentation lists most of India's Scheduled Languages in its NMT support. Kashmiri and Santali are not currently listed in the NMT language list, so the application marks those two as `google_unsupported` instead of pretending a translation was produced.

Official documentation:
- https://cloud.google.com/translate/docs
- https://cloud.google.com/translate/docs/languages
- https://cloud.google.com/translate/docs/authentication

## Project structure

```text
indian-object-translator/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── src/
│   ├── __init__.py
│   ├── detector.py
│   ├── languages.py
│   └── translator.py
├── notebooks/
│   └── 01_colab_object_translator.ipynb
└── tests/
    └── test_languages.py
```

## 1. Google Cloud setup

Create a Google Cloud project, for example:

`indian-object-translator`

Enable the Cloud Translation API.

For the Basic/v2 REST API:

1. Open Google Cloud Console.
2. Create/select your project.
3. Enable **Cloud Translation API**.
4. Go to **APIs & Services -> Credentials**.
5. Create an **API key**.
6. Restrict the API key to the Cloud Translation API where possible.

Do not commit the real key to GitHub.

## 2. Local setup

Python 3.10+ is recommended.

```bash
git clone <your-repository-url>
cd indian-object-translator

python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GOOGLE_TRANSLATE_API_KEY=your_google_api_key_here
YOLO_MODEL=yolo26n.pt
CONFIDENCE_THRESHOLD=0.40
```

`.env` is ignored by Git.

## 3. Run the application

```bash
python app.py
```

Open the Gradio URL printed in the terminal.

## 4. Google Colab

Open:

`notebooks/01_colab_object_translator.ipynb`

The notebook demonstrates the project in stages:

1. Install dependencies.
2. Load YOLO.
3. Upload an image.
4. Detect objects.
5. Configure the Google API key through Colab Secrets.
6. Test translation.
7. Translate detections into the supported Scheduled Languages.
8. Display a final table.

### Colab Secret

In Colab:

`Secrets -> Add new secret`

Name:

`GOOGLE_TRANSLATE_API_KEY`

The notebook reads it using:

```python
from google.colab import userdata
api_key = userdata.get("GOOGLE_TRANSLATE_API_KEY")
```

## 5. Supported language configuration

The application keeps the language list in `src/languages.py`.

The 22 Scheduled Languages are:

- Assamese
- Bengali
- Bodo
- Dogri
- Gujarati
- Hindi
- Kannada
- Kashmiri
- Konkani
- Maithili
- Malayalam
- Manipuri
- Marathi
- Nepali
- Odia
- Punjabi
- Sanskrit
- Santali
- Sindhi
- Tamil
- Telugu
- Urdu

The Google provider currently supports 20 of these through its documented NMT language list. Kashmiri and Santali are retained in the application so the output always has all 22 rows, with an explicit unsupported status.

## 6. Example output

For an image containing a cat:

```text
Detected object: cat
Confidence: 0.94

Language       Translation       Status
------------------------------------------------
Assamese       ...               translated
Bengali        ...               translated
Bodo           ...               translated
...
Hindi          ...               translated
...
Kashmiri       --                google_unsupported
...
Santali        --                google_unsupported
...
Tamil          ...               translated
Telugu         ...               translated
Urdu           ...               translated
```

## 7. Security

Never commit:

```text
.env
*.key
*.json
service-account*.json
```

The repository contains `.env.example`, not your real credentials.

## 8. Next engineering improvements

After the basic POC works:

- batch translation requests
- cache repeated object labels
- add retry/backoff
- add API rate-limit handling
- add structured JSON output
- add object bounding-box visualization
- add translation provider abstraction
- add IndicTrans2/other provider as fallback for unsupported languages
- add unit/integration tests
- add Docker support
- deploy the Gradio app
