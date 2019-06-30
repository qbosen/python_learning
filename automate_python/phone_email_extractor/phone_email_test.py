import unittest

from phone_email_extractor import cn_mobile_phone_regex, common_phone_regex, email_regex
from phone_email_extractor import phone_email_extract


class MobilePhoneNumberTest(unittest.TestCase):
    @staticmethod
    def match_phone_number(phone):
        return cn_mobile_phone_regex.match(phone)

    def test_right_phones(self):
        right_numbers = ['86-138-9999-8888', '18433334444', '136 7777 8888', '+86 158 6666 8888']
        for number in right_numbers:
            self.assertIsNotNone(self.match_phone_number(number))

    def test_wrong_phones(self):
        wrong_numbers = ['-86-138 9999 8888', '133 333 55555']
        for number in wrong_numbers:
            self.assertIsNone(self.match_phone_number(number))


class CommonPhoneNumberTest(unittest.TestCase):
    @staticmethod
    def match_phone_number(phone):
        return common_phone_regex.match(phone)

    def test_right_phones(self):
        right_numbers = ['400-999-8888', '4008889999', '4008889999 5859', '4008889999x5859']
        for number in right_numbers:
            self.assertIsNotNone(self.match_phone_number(number))

    def test_wrong_phones(self):
        wrong_numbers = ['86-138 9999 8888', '133 3333 5555']
        for number in wrong_numbers:
            self.assertIsNone(self.match_phone_number(number))


class EmailTest(unittest.TestCase):
    @staticmethod
    def match_email(email):
        return email_regex.match(email)

    def test_right_emails(self):
        right_emails = ['123456@qq.com', 'petter-new@yahoo.com.cn', 'john%MS@163.com']
        for email in right_emails:
            self.assertIsNotNone(self.match_email(email))

    def test_wrong_emails(self):
        wrong_emails = ['ac count@mail.org', 'tom@new@google.com']
        for email in wrong_emails:
            self.assertIsNone(self.match_email(email))


class ExtractorTest(unittest.TestCase):
    text = '''合作联系  市场合作：upmco@baidu.com 校园合作：campusmaster@baidu.com 战略合作：zhanzhangpingtai@baidu.com
业务联系  百度无线：mbaidu@baidu.com 百度推广售后热线：400-921-9999 百度推广销售热线：400-800-8888
投诉中心  投诉中心网址： http://help.baidu.com'''
    phone_email_extract(text)


if __name__ == '__main__':
    unittest.main()
