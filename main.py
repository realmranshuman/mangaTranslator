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
    font = ImageFont.truetype("arial.ttf", 36)

    # Get the size of the new text
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(translated_text, font)

    # Get the position of the detected text
    boxes = pytesseract.image_to_boxes(image, config=config)
    height = image.height
    for b in boxes.splitlines():
        b = b.split()
        draw.rectangle(((int(b[1]), height - int(b[2])), (int(b[3]), height - int(b[4]))), fill='red')
    # Draw the new text on the image
    text_x = 10
    text_y = height - 10 - text_height
    draw.text((text_x, text_y), translated_text, font=font, fill=(255, 255, 255))

    # Save the image with the new text
    image.save("new_image.jpg")
    return {"message": "Image has been updated with translated text"}
