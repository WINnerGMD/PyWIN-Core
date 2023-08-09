from typing import Dict

"  Help to create Robtops objects for GD"

def gd_dict_str(d: Dict[int, str], separator: str = ":") -> str:
    """Converts the dict `d` into a Geometry Dash-styled HTTP response.

    Args:
        d (dict): A dictionary of keys to convert. Should be in the format
            key int: str`.
        separator (str): The character to separate all elements of the dict.

    Returns:
        Returns a string from the dict in the format `1:aaa:2:b`
    """

    # Combine them all and send off.
    return separator.join([str(arg[i]) for arg in d.items() for i in (0, 1)])


def parse_to_dict(data: str, separator: str = "~|~") -> dict:
    """Parses a GeometryDash style keyed split response into an easy to work
    with Python dictionary object.

    Args:
        data (str): The data to be parsed into a dict.
    """

    # Bit ugly but reduces function calls and var alloc
    return {key: val for key, val in zip(*[iter(data.split(separator))] * 2)}

class GDCol:
    """Geometry Dash letters corresponding to `FLAlertLayer` colours."""

    BLURPLE = "b"
    GREEN = "g"
    LBLUE = ("l",)
    ORANGE = "o"
    PINK = "p"
    LRED = "r"
    YELLOW = "y"
    RED = ""

    ALL = (BLURPLE, GREEN, LBLUE, ORANGE, PINK, LRED, YELLOW, RED)


def col_tag(text: str, col: GDCol) -> str:
    """Formats the text using the Geometry Dash colour tags.

    Args:
        text (str): The text to be coloured through tags.
        col (GDCol): The Geometry Dash colour to wrap the text around with.

    Returns:
        Col formatted str.
    """

    return f"<c{col}>{text}</c>"
