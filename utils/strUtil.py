import re


class strUtil:
    @staticmethod
    def containsAlpha(_str):
        if re.findall(re.compile(r'[A-Za-z]', re.S), _str):
            return True
        else:
            return False
