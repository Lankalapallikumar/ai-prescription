from paddleocr import PaddleOCR

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image_bytes(image_bytes):
    result = ocr_model.ocr(image_bytes, cls=True)
    text = []
    for line in result:
        for word in line:
            text.append(word[1][0])
    return " ".join(text)
