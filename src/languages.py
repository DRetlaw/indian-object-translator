# India's 22 Scheduled Languages.
# Google NMT support is tracked separately because provider coverage can change.

SCHEDULED_LANGUAGES = [
    {"name": "Assamese", "code": "as"},
    {"name": "Bengali", "code": "bn"},
    {"name": "Bodo", "code": "brx"},
    {"name": "Dogri", "code": "doi"},
    {"name": "Gujarati", "code": "gu"},
    {"name": "Hindi", "code": "hi"},
    {"name": "Kannada", "code": "kn"},
    {"name": "Kashmiri", "code": "ks", "google_supported": False},
    {"name": "Konkani", "code": "gom"},
    {"name": "Maithili", "code": "mai"},
    {"name": "Malayalam", "code": "ml"},
    {"name": "Manipuri", "code": "mni-Mtei"},
    {"name": "Marathi", "code": "mr"},
    {"name": "Nepali", "code": "ne"},
    {"name": "Odia", "code": "or"},
    {"name": "Punjabi", "code": "pa"},
    {"name": "Sanskrit", "code": "sa"},
    {"name": "Santali", "code": "sat", "google_supported": False},
    {"name": "Sindhi", "code": "sd"},
    {"name": "Tamil", "code": "ta"},
    {"name": "Telugu", "code": "te"},
    {"name": "Urdu", "code": "ur"},
]

for language in SCHEDULED_LANGUAGES:
    language.setdefault("google_supported", True)
