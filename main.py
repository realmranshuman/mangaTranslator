from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator

app = FastAPI()

# OCR configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
config = ('-l jpn --oem 1 --psm 3')

@app.post("/image/")
async def image_upload(file: UploadFile):
    # Open the image
    image = Image.open(file.file)

    # Use OCR to detect the text on the image
    text = pytesseract.image_to_string(image, config=config)

    # Translate the text using Google Translate
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text

    # Define the font and new text
    font = ImageFont.truetype("arial.ttf", 10)

    # Get the size of the new text
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(translated_text, font)

    # Get the position of the detected text
    text_x, text_y = (0,0)

    # Draw the new text on the image
    draw.text((text_x, text_y), translated_text, font=font, fill=(255, 0, 0))

    # Save the image with the new text
    image.save("new_image.jpg")
    return {"message": "Image has been updated with translated text"}
