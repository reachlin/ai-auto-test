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
[[[519.0, 15.0], [833.0, 19.0], [832.0, 59.0], [519.0, 55.0]], ('P Incidents - PagerDuty', 0.9673468470573425)]
[[[978.0, 18.0], [1393.0, 18.0], [1393.0, 55.0], [978.0, 55.0]], ('M Inbox (944) - lin.cai@chowbl', 0.9800806641578674)]
[[[1957.0, 15.0], [2337.0, 19.0], [2337.0, 59.0], [1956.0, 55.0]], (' paddle_test... (2) - Jupyterl', 0.9737967848777771)]
[[[463.0, 29.0], [482.0, 29.0], [482.0, 48.0], [463.0, 48.0]], ('X', 0.637111246585846)]
[[[3532.0, 26.0], [3558.0, 26.0], [3558.0, 52.0], [3532.0, 52.0]], ('v', 0.6642062664031982)]
[[[49.0, 184.0], [276.0, 184.0], [276.0, 221.0], [49.0, 221.0]], (' Your applications', 0.9662941694259644)]
[[[299.0, 192.0], [511.0, 192.0], [511.0, 217.0], [299.0, 217.0]], (' chowbus GOF', 0.9587520956993103)]
[[[541.0, 192.0], [665.0, 192.0], [665.0, 217.0], [541.0, 217.0]], (' Braze', 0.9936092495918274)]
[[[3330.0, 184.0], [3562.0, 184.0], [3562.0, 221.0], [3330.0, 221.0]], (' All Bookmarks', 0.9651249051094055)]
[[[78.0, 247.0], [321.0, 247.0], [321.0, 284.0], [78.0, 284.0]], ('File Edit View', 0.961975634098053)]
[[[336.0, 254.0], [396.0, 254.0], [396.0, 284.0], [336.0, 284.0]], ('Run', 0.9995442032814026)]
[[[422.0, 254.0], [515.0, 254.0], [515.0, 287.0], [422.0, 287.0]], ('Kernel', 0.9960715174674988)]
[[[526.0, 251.0], [825.0, 251.0], [825.0, 287.0], [526.0, 287.0]], ('TabsSettingsHelp', 0.9969504475593567)]
[[[872.0, 308.0], [1039.0, 321.0], [1036.0, 362.0], [869.0, 349.0]], (' 0 Launcher', 0.9261624813079834)]
[[[1240.0, 313.0], [1572.0, 317.0], [1571.0, 358.0], [1239.0, 354.0]], ('x paddle_test.ipynb', 0.9779991507530212)]
[[[385.0, 332.0], [403.0, 332.0], [403.0, 354.0], [385.0, 354.0]], ('+', 0.947018027305603)]
[[[470.0, 324.0], [508.0, 324.0], [508.0, 361.0], [470.0, 361.0]], ('c', 0.5152702331542969)]
[[[157.0, 335.0], [190.0, 335.0], [190.0, 357.0], [157.0, 357.0]], ('+', 0.996977686882019)]
[[[877.0, 372.0], [1232.0, 372.0], [1232.0, 409.0], [877.0, 409.0]], ('0 +x ', 0.7636274099349976)]
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

The chatgpt will return something like this:
```
_complete(): using gpt-4, 0.7
'<OUTPUT>(169, 780)</OUTPUT>'
```
