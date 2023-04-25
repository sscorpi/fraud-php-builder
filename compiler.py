from fraud_parser import getComponents, getAllPages, getComponentsInPage, getPageCode
from utils import getFolderName, logger
from templates import HTACCESS
from bs4 import BeautifulSoup

import sys
from os import mkdir, path
import shutil


def putDefaultContent():
    def putFolder(src, dest):
        try:
            shutil.copytree(src, dest)
        except FileExistsError:
            shutil.rmtree(dest)
            shutil.copytree(src, dest)

    # Copy '_fraud' directory
    fraud_dir = r'C:\xampp\htdocs\_fraud'
    fraud_dest_dir = r'build\_fraud'
    putFolder(fraud_dir, fraud_dest_dir)

    # Copy 'src' directory
    src_dir = r'C:\xampp\htdocs\src'
    dest_dir = r'build\src'
    putFolder(src_dir, dest_dir)

    # Copy 'api' directory
    api_dir = r'C:\xampp\htdocs\api'
    api_dest_dir = r'build\api'
    putFolder(api_dir, api_dest_dir)

    # Create .htaccess file in build directory
    with open('build/.htaccess', 'w') as f:
        f.write(HTACCESS)


def createPages(pages):
    for page in pages:
        pageName = getFolderName(page)
        logger.info(
            f"Building page: {page} as build/{pageName}.php")
        page_html = ""
        components = getComponents(page)
        components_in_page = getComponentsInPage(page)
        page_code = getPageCode(page)
        for component in components:
            if component.name in components_in_page:
                _name = "{$" + component.name + "}"
                component_code = getPageCode(component.path)
                page_code = page_code.replace(_name, component_code)

        # Beatufy the code using BeautifulSoup
        soup = BeautifulSoup(page_code, 'html.parser')
        page_html = soup.prettify()
        with open(f'build/{pageName}.php', 'w') as f:
            f.write(page_html)


def buildApp(files):
    logger.info("Started building app...")
    if path.exists('build'):
        consent = input(
            "Build folder already exists. Do you want to overwrite it? (y/n): ")
        while consent != 'y' and consent != 'n':
            consent = input(
                "Build folder already exists. Do you want to overwrite it? (y/n): ")
        if consent == 'y':
            shutil.rmtree('build')
            mkdir('build')
        else:
            logger.error("Build folder already exists. Exiting...")
            exit(100)
    else:
        mkdir('build')
    putDefaultContent()
    createPages(files)


directories, files = getAllPages('C:\\xampp\\htdocs\\pages\\')

index = 'C:\\xampp\\htdocs\\pages\\page.php'

if len(sys.argv) != 2:
    print("Usage: python compiler.py build")
else:
    if (sys.argv[1] == 'build'):
        buildApp(files)
