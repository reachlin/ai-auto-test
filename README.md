# ai-auto-test: Use PaddlePaddle OCR for test automation

We can use pyautogui to control the keyboard and mouse for test automation. But it is hard to find the right position of a button or text input box, especially, when GUI changes a lot from version to verson. Some browser based test automation frameworks will inject a piece of javascript code to search and find intented elements, and the use case of this method is quite limited.

In this solution, we send the screenshot image to an OCR engine. With each text block recognized with its borders, we can use pyautogui to test both browser based or native applications.

[pyautogui](https://pyautogui.readthedocs.io/en/latest/mouse.html#mouse-scrolling)
[PaddlePaddle OCR](https://github.com/PaddlePaddle/PaddleOCR)
