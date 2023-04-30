from fraud_parser import (
    getComponents,
    getAllPages,
    getComponentsInPage,
    getPageCode,
    getPageMetadata,
    getPropsInPage,
)
from utils import getFolderName, logger, SOURCE_PATH, PROPS_OWNER_KEY
from templates import HTML_SKELETON, HTACCESS
from bs4 import BeautifulSoup

from sys import argv, exit
from os import listdir, remove
from shutil import copytree, rmtree
from server import start_server


def getPropsInPageEdited(props):
    keys = []
    values = []
    for prop in props:
        prop_keys = []
        prop_values = []
        if prop.keys[0] != f'"{PROPS_OWNER_KEY}"':
            logger.error(
                f"Prop {prop} is not a valid Fraud Prop. It must have a key named '{PROPS_OWNER_KEY}' and it must be the first key."
            )
            exit()
        for key in prop.keys:
            _key = "{$props[" + key + "]}"
            prop_keys.append(_key)
            prop_values.append(prop.values[prop.keys.index(key)].strip('"'))
        keys.append(prop_keys)
        values.append(prop_values)
    return keys, values


def getComponentsInPageEdited(components):
    result = []
    for component in components:
        if component.props != None:
            a = []
            # Append props into a array that has same component.name, so create multidimensional array
            for prop in component.props:
                a.append(prop)
            result.append([component.name, a])
    return result


def cleanBuildDir():
    consent = None
    while consent != "y" and consent != "n":
        consent = input(
            "Do you want to clean build directory? This action is irreversible. (y/n): "
        )
    if consent == "y":
        logger.warning("Cleaning build directory...")
        # Remove everyting inside build except _fraud folder
        build_files = listdir("build")
        for file in build_files:
            if file != "_fraud":
                try:
                    rmtree(f"build\\{file}")
                except NotADirectoryError:
                    # It is a file, remove it
                    remove(f"build\\{file}")
        # Remove everyting inside _fraud except js/core.js
        fraud_files = listdir("build\\_fraud\\js")
        for file in fraud_files:
            if file != "core.js":
                try:
                    rmtree(f"build\\_fraud\\js\\{file}")
                except NotADirectoryError:
                    # It is a file, remove it
                    remove(f"build\\_fraud\\js\\{file}")
    elif consent == "n":
        logger.error("Operation cancelled by user. Exiting...")
        exit(100)


def putDefaultContent():
    def putFolder(src, dest):
        try:
            copytree(src, dest)
        except FileExistsError:
            rmtree(dest)
            copytree(src, dest)

    # Copy '_fraud' directory
    fraud_dir = f"{SOURCE_PATH}\\_fraud\\js\\exports"
    fraud_dest_dir = "build\\_fraud\\js\\exports"
    putFolder(fraud_dir, fraud_dest_dir)

    # Copy 'src' directory
    src_dir = f"{SOURCE_PATH}/src"
    dest_dir = "build/src"
    putFolder(src_dir, dest_dir)

    # Create .htaccess file
    with open("build/.htaccess", "w") as f:
        f.write(HTACCESS)


def createPages(pages):
    for page in pages:
        pageName = getFolderName(page)
        logger.info(f"Building page: {page} as build\\{pageName}.php")
        components = getComponents(page)
        components_in_page = getComponentsInPage(page)
        props_in_page = getPropsInPage(page)
        page_code = getPageCode(page)
        for component in components:
            if component.name in components_in_page:
                _name = "{$" + component.name + "}"
                component_code = getPageCode(component.path)
                page_code = page_code.replace(_name, component_code)

        # Replace props in page
        replace = getComponentsInPageEdited(components)
        keys, values = getPropsInPageEdited(props_in_page)
        for i in range(len(replace)):
            for j in range(len(replace[i][1])):
                if len(replace[i][1]) != len(keys[i]) - 1:
                    logger.critical(
                        f'Component "{replace[i][0]}" trying to access {len(replace[i][1])} props, but it takes {len(keys[i]) - 1} props in {component.path}'
                    )
                    exit(107)
                if replace[i][1][j] == keys[i][j + 1]:
                    try:
                        page_code = page_code.replace(keys[i][j + 1], values[i][j + 1])
                    except:
                        logger.critical(
                            f'Trying to access a prop that does not exist in component "{replace[i][0]}" in page "{page}"'
                        )
                        exit(107)
                else:
                    logger.critical(
                        f'"{replace[i][1][j]}" does not exist in {component.path}. Did you mean "{keys[i][j + 1]}"?'
                    )
                    exit(107)

        soup = BeautifulSoup(HTML_SKELETON, "html.parser")
        # Add page metadata if declared
        try:
            metadata = getPageMetadata(page)
            if metadata.title:
                soup.title.string = metadata.title
            if metadata.keywords:
                meta_keywords = soup.find("meta", attrs={"name": "keywords"})
                if meta_keywords:
                    meta_keywords["content"] = metadata.keywords
                else:
                    soup.head.append(
                        soup.new_tag("meta", name="keywords", content=metadata.keywords)
                    )
            if metadata.description:
                meta_description = soup.find("meta", attrs={"name": "description"})
                if meta_description:
                    meta_description["content"] = metadata.description
                else:
                    soup.head.append(
                        soup.new_tag(
                            "meta", name="description", content=metadata.description
                        )
                    )
        except:
            pass

        main = soup.find("main")
        main.append(page_code)
        page_html = soup.prettify(formatter=None)
        with open(f"build/{pageName}.html", "w") as f:
            f.write(page_html)


def buildApp(files):
    build_files = listdir("build")
    if len(build_files) == 1 and build_files[0] == "_fraud":
        # Only _fraud folder exists, no need to overwrite
        pass
    else:
        consent = None
        while consent != "y" and consent != "n":
            consent = input(
                "Found previous build. Do you want to overwrite it? (y/n): "
            )
        if consent == "y":
            # Remove everyting inside build except _fraud folder
            for file in build_files:
                if file != "_fraud":
                    try:
                        rmtree(f"build/{file}")
                    except NotADirectoryError:
                        # It is a file, remove it
                        remove(f"build/{file}")

        elif consent == "n":
            logger.error("Operation cancelled by user. Exiting...")
            exit(100)
    logger.info("Build started")
    putDefaultContent()
    createPages(files)
    logger.info("Build finished with no errors!")


directories, files = getAllPages(f"{SOURCE_PATH}\\pages")


if len(argv) != 2:
    print("Usage: python compiler.py build, dev, clean, debug")
else:
    if argv[1] == "build":
        buildApp(files)
    elif argv[1] == "dev":
        start_server()
    elif argv[1] == "clean":
        cleanBuildDir()
    elif argv[1] == "debug":
        for page in files:
            print(getFolderName(page))
            print(page)
