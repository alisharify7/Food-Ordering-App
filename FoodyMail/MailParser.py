import os
import pathlib
from jinja2 import Template
from FoodyMail import BASE_DIR


def ReadHtmlContent(path: os.path) -> str:
    """
    This function take a html path and return content of that html in string
    """
    path = BASE_DIR / path
    if not os.path.exists(path) or not path.is_file():
        return ""

    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()


def ParseMail(path: os.path, context: dict) -> str:
    """
        this Function take a Html Path and Render the Html in String
            You can Also Use variable in template as well (Jinja2)

    """
    result = ReadHtmlContent(path)
    if not result:
        return ""

    template = Template(result)
    return template.render(**context)
