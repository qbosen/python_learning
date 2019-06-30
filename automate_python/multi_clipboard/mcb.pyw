#! /Users/qiubaisen/PycharmProjects/CrashCourse/venv/bin/python
# 保存和加载文本到剪贴板
"""
Usage:  mcb.pyw -s/--save <keyword>     - Save clipboard to keyword.
        mcb.pyw -d/--del <keyword>      - Delete keyword and clear clipboard.
        mcb.pyw <keyword>               - Load keyword to clipboard.
        mcb.pyw -l/--list               - Load all keywords to clipboard.
        mcb.pyw -c/--clear              - Delete all keywords and clear clipboard.
"""

import shelve, sys, pyperclip, os

# 确保当此脚本导出到环境变量时，数据库不会因为执行位置的不同而变化
working_directory = '/Users/qiubaisen/PycharmProjects/CrashCourse/automate_python/multi_clipboard'
os.chdir(working_directory)
db = shelve.open('mcb.db')
if len(sys.argv) == 3:
    op = sys.argv[1].lower()
    key = sys.argv[2]
    # 保存到剪贴板
    if op == '-s' or op == '--save':
        db[key] = pyperclip.paste()
    # 删除并清空剪贴板
    elif op == '-d' or op == '--del':
        if key in db.keys():
            db.remove(key)
        pyperclip.copy('')
elif len(sys.argv) == 2:
    param = sys.argv[1]
    # 复制所有关键字到剪贴板
    if param == '-l' or param == '--list':
        pyperclip.copy(str(list(db.keys())))
    # 清空数据库，清空剪贴板
    elif param == '-c' or param == '--clear':
        db.clear()
        pyperclip.copy('')
    # 加载关键字
    else:
        if param in db.keys():
            pyperclip.copy(db[param])
