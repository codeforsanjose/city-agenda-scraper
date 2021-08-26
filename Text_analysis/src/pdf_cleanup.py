import re


def clean_text(text):
    text = text.decode("UTF-8")
    text = text.replace("\n", " ")
    text = text.replace("\x0c", " ")
    text = re.sub(
        r"-", " ", text
    )  # Split the words with "-" (for example：pre-processing ==> pre processing）
    text = re.sub(r"\d+/\d+/\d+", "", text)  # Take out the dates
    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text)  # Take out the time
    text = re.sub(r"[\w]+@[\.\w]+", "", text)  # Take out the emails
    text = re.sub(
        r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text
    )  # Take out the websites
    pure_text = ""
    # Validate to check if there are any non-text content
    for letter in text:
        # Keep only letters and spaces
        if letter.isalpha() or letter == " ":
            pure_text += letter
    # Join the words are not stand-alone letters
    text = " ".join(word for word in pure_text.split() if len(word) > 1)
    return text
