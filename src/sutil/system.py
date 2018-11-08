from __future__ import absolute_import

def clip(string):
    import pyperclip
    pyperclip.copy(string)

def paste():
    import pyperclip
    pyperclip.paste()

