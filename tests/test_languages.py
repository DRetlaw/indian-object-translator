from src.languages import SCHEDULED_LANGUAGES


def test_exactly_22_scheduled_languages():
    assert len(SCHEDULED_LANGUAGES) == 22


def test_unique_language_names():
    names = [item["name"] for item in SCHEDULED_LANGUAGES]
    assert len(names) == len(set(names))


def test_google_fallback_languages_are_explicit():
    unsupported = {
        item["name"]
        for item in SCHEDULED_LANGUAGES
        if not item["google_supported"]
    }

    assert "Kashmiri" in unsupported
    assert "Santali" in unsupported
