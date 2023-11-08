# %%
import pandas as pd
import re

# 读取缩写替换规则
df = pd.read_excel('abbreviation.xlsx')
abbreviations = df['abbreviation'].tolist()
replacements = df['replacement'].tolist()


reference = 'Proceedings of the 2020 conference on Computer Vision'

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


print(reference)
