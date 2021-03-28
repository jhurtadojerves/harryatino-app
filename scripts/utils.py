def fix_codification(text):
    conditions = {
        "Ã¡": "á",
        "Ã©": "é",
        "Ã": "í",
        "Ã³": "ó",
        "Ãº": "ú",
        "Ã±": "ñ",
        "Â¿": "¿",
        "í¡": "á",
        "í©": "é",
        "í": "í",
        "í³": "ó",
        "íº": "ú",
        "í±": "ñ",
        "í¿": "¿",
    }
    for i, j in conditions.items():
        text = text.replace(i, j)
    return text
