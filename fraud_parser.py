from os import listdir, path
from objects import Component, Prop, Metadata
from utils import logger

import re


def getComponents(file):
    # Finds all the imported components in a file and returns a list of component objects
    components = []
    with open(file, "r") as f:
        for line in f:
            if line.startswith("require_once"):
                # Get the contents of the require_once statement inside parenthesis
                component = line.split("(")[1].split(")")[0].replace('"', "")
                # Get the name of the component by removing the extension and getting last part of the path
                name = component.split("/")[-1].split(".")[0]
                # Get the path of the component replace {$_SERVER['DOCUMENT_ROOT']} with the path to the root directory
                component_path = component.replace(
                    "{$_SERVER['DOCUMENT_ROOT']}", "C:/xampp/htdocs"
                )
                # Create new component object
                component = Component(name, component_path, file)
                components.append(component)
    return components


def getPageCode(file):
    # Reads the code of a page
    with open(file, "r") as f:
        # Read contents of file and start at the line of <<<HTML to the line of HTML;
        rawCode = f.read().split("<<<HTML")[1].split("HTML;")[0]
        return rawCode


def getFullPageCode(file):
    with open(file, "r") as f:
        rawCode = f.read()
        return rawCode


def getPageMetadata(file):
    code = getFullPageCode(file)
    metadata = {}
    # Find all occurrences of $PAGE_TITLE, $PAGE_KEYWORDS, and $PAGE_DESCRIPTION and their values
    pattern = r'\$(PAGE_TITLE|PAGE_KEYWORDS|PAGE_DESCRIPTION)\s*=\s*"(.*?)"'
    matches = re.findall(pattern, code, re.IGNORECASE)
    for match in matches:
        if match[0].lower() == "page_title":
            metadata["title"] = match[1]
        elif match[0].lower() == "page_keywords":
            metadata["keywords"] = match[1]
        elif match[0].lower() == "page_description":
            metadata["description"] = match[1]
    return Metadata(
        metadata.get("title"), metadata.get("keywords"), metadata.get("description")
    )


def getComponentsInPage(file):
    # Finds all the component locations in a page to replace them with actual component codes.
    importedComponents = getComponents(file)
    code = getPageCode(file)
    # Find all occurrences of {$componentName}
    pattern = r"{\$([A-Z][a-zA-Z]*)}"
    potential_components = re.findall(pattern, code, re.IGNORECASE)
    # remove unnecessary spaces from components
    potential_components = [prop.strip() for prop in potential_components]
    # Check if component starts with capital letter if not throw error
    for component in potential_components:
        if not component[0].isupper():
            logger.error(
                f"Error 101: Component {component} in {file} is not a valid Fraud Component. It must start with a capital letter."
            )
            exit(101)
    # Check if component is imported if not throw error
    for component in potential_components:
        if component not in [c.name for c in importedComponents]:
            logger.error(
                f"Error 103: Component {component} in {file} is not imported. Please import it first."
            )
            exit(103)
    return potential_components


def getPropsInPage(file):
    php_code = getFullPageCode(file)
    # Extract all associative arrays from PHP code using regular expressions
    pattern = r"\$props\s*=\s*\[\s*([\s\S]*?)\s*\]\s*;"
    matches = re.findall(pattern, php_code)

    # Create a Prop object for each associative array
    props = []
    for match in matches:
        array_str = match
        keys = []
        values = []
        for line in array_str.split(",\n"):
            key, value = line.strip().split(" => ")
            keys.append(key.strip().strip("'"))
            values.append(value.strip().strip("'"))
        props.append(Prop(keys, values))
    return props


def getAllPages(directory_path):
    directories = []
    files = []
    for filename in listdir(directory_path):
        file_path = path.join(directory_path, filename)
        if path.isfile(file_path):
            if filename.endswith(".php"):
                files.append(file_path)
        elif path.isdir(file_path):
            directories.append(file_path)
            nested_directories, nested_files = getAllPages(file_path)
            directories.extend(nested_directories)
            files.extend(nested_files)
    return directories, files
