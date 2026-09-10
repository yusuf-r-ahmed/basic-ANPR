import re

# UK Plate Formats: Current (2001+), Prefix (1983-2001), Suffix (1963-1983)
CURRENT_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{3}$")
PREFIX_PATTERN = re.compile(r"^[A-Z][0-9]{1,3}[A-Z]{3}$")
SUFFIX_PATTERN = re.compile(r"^[A-Z]{3}[0-9]{1,3}[A-Z]$")

CHAR_TO_NUM = {"O": "0", "I": "1", "Z": "2", "S": "5", "B": "8"}
NUM_TO_CHAR = {"0": "O", "1": "I", "2": "Z", "5": "S", "8": "B"}

def disambiguate_current_plate(raw_text: str) -> str:
    #Fix common OCR confusion based on positional rules of 2001+ UK plates.
    if len(raw_text) != 7:
        return raw_text

    chars = list(raw_text)
    # Positions 0, 1: Area code (Letters only)
    for i in (0, 1):
        if chars[i] in NUM_TO_CHAR:
            chars[i] = NUM_TO_CHAR[chars[i]]

    # Positions 2, 3: Age identifier (Digits only)
    for i in (2, 3):
        if chars[i] in CHAR_TO_NUM:
            chars[i] = CHAR_TO_NUM[chars[i]]

    # Positions 4, 5, 6: Random letters (Letters only)
    for i in (4, 5, 6):
        if chars[i] in NUM_TO_CHAR:
            chars[i] = NUM_TO_CHAR[chars[i]]

    return "".join(chars)

def validate_plate(text):
    #Cleans, disambiguates, and validates a candidate plate string.
    clean = re.sub(r"[^A-Z0-9]", "", text.upper())
    
    if len(clean) == 7:
        clean = disambiguate_current_plate(clean)
        if CURRENT_PATTERN.match(clean):
            return True, f"{clean[:4]} {clean[4:]}"

    if PREFIX_PATTERN.match(clean) or SUFFIX_PATTERN.match(clean):
        return True, clean

    return False, clean