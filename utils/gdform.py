from typing import Dict
import time
"  Help to create Robtops objects for GD"

def gd_dict_str(d: Dict[int, str], separator: str = ":") -> str:
    return separator.join([str(arg[i]) for arg in d.items() for i in (0, 1)])


def parse_to_dict(data: str, separator: str = "~|~") -> dict:
    return {key: val for key, val in zip(*[iter(data.split(separator))] * 2)}


def formatted_date():
    """Returns the current fromatted date in the format
    DD/MM/YYYY HH:MM:SS"""

    return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
