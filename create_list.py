# %%
import openpyxl
import re

# 读取txt文件
with open('data.txt') as f:
    lines = f.readlines()


# 创建excel工作簿
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['abbreviation', 'replacement'])

rules = ""
for line in lines:
    rules = rules + " " + line
rules = rules.replace("\n", "")
rules = rules.split('.')
for rule in rules:
    if len(rule) <= 3:
        continue
    # 使用正则表达式去除开头和末尾空格
    pattern = r'^\s*(.*?)\s*$'
    rule = re.match(pattern, rule).group(1) + "."
    print(rule)
    parts = rule.split(" ")
    if '(' in rule:
        pattern = r'(.*?)\((.*?)\)'
        match = re.match(pattern, parts[0])
        if match:
            xxxx = match.group(1)
            aaa = match.group(2)
        ws.append([xxxx, parts[1]])
        ws.append([xxxx + aaa, parts[1]])
    elif "," in rule:
        ws.append([parts[0][:-1], parts[2]])
        ws.append([parts[1], parts[2]])
    else:
        ws.append([parts[0], parts[1]])

# 保存excel文件
wb.save('abbreviation.xlsx')
