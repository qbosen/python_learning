import pyperclip, re

# 大陆手机号码正则表达式
cn_mobile_phone_regex = re.compile(r'''(
    (\+86|86)?              # 大陆区号
    (\s|-)?                 # 分隔符
    (1\d{2})                # 前三位
    (\s|-)?                 # 分隔符
    (\d{4})                 # 中间四位
    (\s|-)?                 # 分隔符
    (\d{4})                 # 末尾四位
)''', re.VERBOSE)

# 通用号码
common_phone_regex = re.compile(r'''(
    (\d{3}|\(\d{3}\))       # 区号
    (\s|-)?                 # 分隔符
    (\d{3})                 # 中间三位
    (\s|-)?                 # 分隔符
    (\d{4})                 # 末尾位
    (\s*(ext|x|ext\.)?\s*(\d{2,5}))?         # 扩展分机号
)''', re.VERBOSE)

# 邮箱正则表达式
email_regex = re.compile(r'''(
    [\w.%+-]+               # 用户名
    @                       # @ 符号
    [a-zA-Z0-9.-]+          # 域名
    (\.[a-zA-Z]{2,4})       # dot-something
)''', re.VERBOSE)


def phone_email_extract(text):
    """查找传入文本中的所有手机号，座机号，邮箱地址。复制结果到剪贴板"""
    match_results = []
    # 手机号
    for groups in cn_mobile_phone_regex.findall(text):
        phone_num = '-'.join([groups[1], groups[3], groups[5], groups[7]])
        match_results.append(phone_num)

    # 座机号
    for groups in common_phone_regex.findall(text):
        phone_num = '-'.join([groups[1], groups[3], groups[5]])
        if groups[8] != '':
            phone_num += ' x' + groups[8]
        match_results.append(phone_num)

    # 邮箱
    for groups in email_regex.findall(text):
        match_results.append(groups[0])

    if len(match_results) > 0:
        pyperclip.copy('\n'.join(match_results))
        print('Copies ', len(match_results), ' result to clipboard:')
        print('\n'.join(match_results))
    else:
        print('No phone numbers or email addresses found.')


if __name__ == '__main__':
    # 从剪贴板获取文本，查找联系信息
    phone_email_extract(text=str(pyperclip.paste()))
