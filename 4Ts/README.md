# 4Ts

**T**kinter, **T**hreading & **T**ext-**T**o-speech.

## Description
This is a simple Python demo showcasing `tkinter` for GUI, `threading` for non-blocking operations, and `pyttsx3` for text-to-speech. 
The script features a flickering title, animated colored globes, and a button/combobox to speak selected phrases.

## Setup
1. Make sure Python is installed.
2. Install required libraries:
```bash
pip install -r requirements.txt
```

## Tkinter basics

* **Frame**: A container to organize widgets; used here to hold the flickering title.
* **Label**: Displays text or images; each letter in the title is a separate label to allow individual color changes.
* **Canvas**: A space for custom drawings/animations; used for animated globes.
* **Button**: Triggers actions; here, it starts the text-to-speech function.
* **Combobox**: Dropdown menu for selecting phrases; implemented using `ttk` (themed widgets) vs `tk` (classic widgets).

## Why threading?

`tkinter` runs everything on a single thread. 
Every computation step is taken one by one, executed and displayed (mostly, some drawing are done using a buffered approach).
This approach raises a problem: if a step takes too long to compute, what happens to the rest of the GUI?
Simply put, _it freezes_.

To avoid this, we can rely on multiple threads, which work in parallel. 
This way, if our computational step takes a long time, the GUI won't just freeze.