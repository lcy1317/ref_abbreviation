# %%
import tkinter as tk
import re
import pandas as pd

def process_text(reference):
    df = pd.read_excel('abbs.xlsx')
    abbreviations = df['abbreviation'].tolist()
    replacements = df['replacement'].tolist()
    prep = ["on", "in", "of", "and", "but", "at", "the"]
    # remove all words in prep in reference to single space
    reference = re.sub(r'\b(?:%s)\b' % '|'.join(prep), '', reference)
    reference = re.sub(r'\s+', ' ', reference)
    # replace word A in string reference to word B
    def replace(str,A,B):
        str = re.sub(r'\b'+A+r'\b',B,str,flags=re.IGNORECASE)
        return str
    for i in range(0,len(df)):
        A = abbreviations[i]
        B = replacements[i]
        reference = replace(reference,A,B)
    return reference

def show_result():
    input_text = text_entry.get()
    result_text = process_text(input_text)
    result_label.config(text=result_text)

root = tk.Tk()
root.title("Text Processor")
root.geometry("400x200")
root.configure(bg='light blue')

text_entry = tk.Entry(root)
text_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

process_button = tk.Button(root, text="Process", command=show_result)
process_button.pack()

root.mainloop()
