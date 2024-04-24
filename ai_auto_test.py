# !pip install pyautogui python-dotenv
# !pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
# !pip install "paddleocr>=2.0.1"

import pyautogui
import time
from PIL import Image
from paddleocr import PaddleOCR

DEBUG = False

def scan_image(image):
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang="en",
        show_log=False,
        # det_max_side_len=2000,
        # max_text_length=200,
        ocr_version="PP-OCRv4"
    )  # need to run only once to download and load model into memory
    result = ocr.ocr(image, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)
    return result

def scan_screen():
    from datetime import datetime
    ts = int(datetime.utcnow().timestamp())
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    
    # Save the image
    screenshot_file = f"./screen{ts}.png"
    screenshot.save(screenshot_file)
    print(screenshot_file)
    image = Image.open(screenshot_file)
    w, h = image.size
    
    # send to google for OCR to find the key word
    #pyautogui.moveTo(30, 30, 3)
    document = scan_image(screenshot_file)
    if document and len(document)>0:
        return w, h, document[0]
    return None

def find_and_click(to_find, w=0, h=0, document=None, after=None):
    layout = find_and_move_to(to_find, w, h, document, after)
    if layout:
        pyautogui.click()
    return layout

def find_and_move_to(to_find, w=0, h=0, document=None, after=None):
    if document is None:
        w, h, document = scan_screen()
    layout = find_tokens(document, to_find, after)
    if layout:
        index, x, y, _ = layout
        sw, sh = pyautogui.size()
        cx = x*sw/w
        cy = y*sh/h
        pyautogui.moveTo(cx, cy, 2)
        return index, cx, cy
    return None

import re
def find_tokens(document, to_find, after=None):
    if not document:
        return None
    index = 0
    for item in document:
        text, score = item[1]
        if DEBUG:
            print(f"{score} {text}")
        if score > 0.8:
            match = re.search(to_find, text)
            if match:
                print("Match Found: ", item)
                p0x, p0y = item[0][0]
                p1x, p1y = item[0][1]
                p2x, p2y = item[0][2]
                length_text = len(text)
                bp, ep = match.span()
                x = p0x + (p1x - p0x)*(bp+1)/length_text
                y = p0y + (p2y - p0y)/3
                if after:
                    if index > after:
                        return index, x, y, match.group()
                else:
                    return index, x, y, match.group()
        index += 1
    return None

def wait_for_token(token, retries=3):
    for i in range(retries):
        if DEBUG:
            print(f"wait_for_token: {token} retry {i}")
        w, h, document = scan_screen()
        layout = find_tokens(document, token)
        if layout:
            return layout
        time.sleep(3)
    return None
