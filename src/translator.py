import requests

from .languages import SCHEDULED_LANGUAGES


class GoogleTranslator:
    ENDPOINT = "https://translation.googleapis.com/language/translate/v2"

    def __init__(self, api_key, timeout=20):
        if not api_key:
            raise ValueError("Google Translation API key is required.")
        self.api_key = api_key
        self.timeout = timeout

    def translate(self, text, target_language):
        response = requests.post(
            self.ENDPOINT,
            params={"key": self.api_key},
            json={
                "q": text,
                "source": "en",
                "target": target_language,
                "format": "text",
            },
            timeout=self.timeout,
        )

        response.raise_for_status()
        payload = response.json()

        return payload["data"]["translations"][0]["translatedText"]

    def translate_all(self, text):
        results = {}

        for language in SCHEDULED_LANGUAGES:
            name = language["name"]
            code = language["code"]

            if not language["google_supported"]:
                results[name] = {
                    "translation": "--",
                    "status": "google_unsupported",
                }
                continue

            try:
                translation = self.translate(text, code)
                results[name] = {
                    "translation": translation,
                    "status": "translated",
                }
            except requests.HTTPError as exc:
                results[name] = {
                    "translation": "--",
                    "status": f"translation_error: {exc}",
                }
            except Exception as exc:
                results[name] = {
                    "translation": "--",
                    "status": f"error: {exc}",
                }

        return results
