
import os
from google.cloud import vision
import re

# Specify language for Google Vision API
language = "en"

# Directory for images to process
directory = 'images'

# Name of document to process (This is just for labeling purposes on the generated document. It can be named anything)
DocumentName = "TestDocument!"

# starting page
page = 1

# Name of file to write text output to.
outputFile = "textFile2.txt"


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(
        image=image,
        image_context={"language_hints": [language]})

    text = response.text_annotations
    text = list(text)[0]

    # Remove any Cyrillic or Greek characters, and other characters that cause problems as they are found (This is a bad way of doing this)
    pattern = re.compile(r'[Α-Ωα-ωА-Яа-яⒸⓒ]+')
    result = pattern.sub(' ', text.description)

    # print("Result = ", result)
    return(result)


def append_to_file(text, DocumentName, page):
    """ Appends detected text to text file. """
    file = open(outputFile, "a")
    file.write(f"\n \n ---------- {DocumentName} Page {page} ---------- ---------- \n")
    try:
        file.writelines(text)
    except Exception as error:
        file.writelines(f"!!!! ERROR OCURRED! {type(error).__name__}")
    file.close

# Main loop
for filename in os.listdir(directory):
    
    f = os.path.join(directory, filename)
    print("Main For Loop!!! ", f)
    data = detect_text(f)
    append_to_file(data, DocumentName, page)
    page = page + 1

    # checking if it is a file
    if os.path.isfile(f):
        print(f)
