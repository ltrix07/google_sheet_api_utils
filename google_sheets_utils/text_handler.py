import re


def all_to_low_and_del_spc(string: str) -> str:
    return re.sub(r'[\t\s]', '', string).lower()
