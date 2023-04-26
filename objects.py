from bs4 import BeautifulSoup
from re import findall

from utils import logger


class Component:
    def __init__(self, name, path, parent):
        self.name = name
        self.path = path
        self.parent = parent
        self.props = self.setProps()

    def getComponentCode(self):
        with open(self.path, "r") as f:
            # Read contents of file and start at the line of <<<HTML to the line of HTML;
            rawCode = f.read().split("<<<HTML")[1].split("HTML;")[0]
            return rawCode

    def setProps(self):
        # Find a tag with data-type='fraud-component' attribute and get all the tags inside it
        soup = BeautifulSoup(self.getComponentCode(), "html.parser")
        component = soup.find(True, {"data-type": "fraud-component"})
        # If component doesn't have data-type='fraud-component' attribute throw error
        if component == None:
            logger.error(
                f"Error 102: Component {self.name} in {self.parent} is not a valid Fraud Component. It must have a data-type='fraud-component' attribute."
            )
            exit(102)
        with open(self.path, "r") as f:
            component_code = f.read()
        # Find all occurrences of {$props['any']}
        pattern = r"{\$props\[.*?\]}"
        props = findall(pattern, component_code)
        # Remove unnecessary spaces from props
        props = [prop.strip() for prop in props]
        # If props is empty return None
        return None if len(props) == 0 else props


class Page:
    def __init__(self, title, keywords, description, path, props, content):
        self.title = title
        self.keywords = keywords
        self.description = description
        self.path = path
        self.props = props
        self.content = content


class Metadata:
    def __init__(self, title, keywords, description):
        self.title = title
        self.keywords = keywords
        self.description = description


class Prop:
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values
