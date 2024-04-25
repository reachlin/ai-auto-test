# ai-auto-test: Use PaddlePaddle OCR for test automation

We can use pyautogui to control the keyboard and mouse for test automation. But it is hard to find the right position of a button or text input box, especially, when GUI changes a lot from version to verson. Some browser based test automation frameworks will inject a piece of javascript code to search and find intented elements, and the use case of this method is quite limited.

In this solution, we send the screenshot image to an OCR engine. With each text block recognized with its borders, we can use pyautogui to test both browser based or native applications.

Check test.ipynb for usages.

[pyautogui](https://pyautogui.readthedocs.io/en/latest/mouse.html#mouse-scrolling)
[PaddlePaddle OCR](https://github.com/PaddlePaddle/PaddleOCR)

## hook the output of OCR to chatgpt

We can also feed the OCR results into chatgpt or other LLM, so we can use nature language to describe GUI test steps.

For example, the prompt could be like this:
```
auto_gui_prompt = '''
You are an expert on GUI automation testing. You will be given a list of text elements recognized by an OCR system. The list is enclosed in <OCR> and </OCR> tags.
Each element has two parts. The first part is the four corners of the text area, and the second part is the text and its OCR confidence score.
Then, an action will be given in <ACTION> and </ACTION> tags. You need to find the correct element from the list for the action, calculate and return the coordinates in a tuple for the action.
The output must be enclosed in <OUTPUT></OUTPUT> tags.
For example, 
<OCR>
[[[85.0, 23.0], [283.0, 14.0], [284.0, 51.0], [87.0, 60.0]], ('1 | Chowbus', 0.8978967666625977)]
...
[[[78.0, 247.0], [321.0, 247.0], [321.0, 284.0], [78.0, 284.0]], ('File Edit View', 0.961975634098053)]
...
</OCR>
<ACTION>
click on File menu
</ACTION>
Your output: (80, 250)

Another example, the same element list.
<ACTION>
click on Edit menu
</ACTION>
Your output: (104, 250)

If there are some texts appeared in multiple times, use your best judement to figure out which is the best target for the action. Because some texts are on a label, some are on a menu item, and some are on a button.
You should also pay attention the coordinates returned to make sure the action can hit the gui item clickable area not the edge. The formula is like start_position * width_text_box / len(text).
'''
```

And, the psedo code, the `document` is the output from the OCR.
```
from openai import OpenAI
client = OpenAI()
_complete(client, auto_gui_prompt, f"<OCR>{document}<OCR><ACTION>click on File menu</ACTION>")
```

The chatgpt will return something like this below, and the coordinate is exactly where File menu item is.
```
_complete(): using gpt-4, 0.7
'<OUTPUT>(169, 780)</OUTPUT>'
```

Another example to show the power of LLM. It can tell which item is a button with the text "Allow".
```
<OCR>
[
  [[[1180.0, 973.0], [1631.0, 973.0], [1631.0, 1021.0], [1180.0, 1021.0]],
  ('Allow access to your data?', 0.9982532262802124)],
  
  [[[1183.0, 1102.0], [2322.0, 1102.0], [2322.0, 1138.0], [1183.0, 1138.0]],
  ('By choosing Allow, you agree to allow the following for the duration of your valid session.',
   0.9954802989959717)],
  
  [[[2274.0, 1385.0], [2367.0, 1385.0], [2367.0, 1426.0], [2274.0, 1426.0]],
  ('Allow', 0.9995352625846863)]
]
</OCR>
<ACTION>click on the Allow button</ACTION>
```

The output is:
```
_complete(): using gpt-4, 0.7
'<OUTPUT>(2320.5, 1405.5)</OUTPUT>'
```
