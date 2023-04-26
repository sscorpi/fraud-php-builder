from fraud_parser import getComponents, getAllPages, getComponentsInPage, getPageCode, getPageMetadata
from utils import getFolderName, logger
from templates import HTML_SKELETON
from bs4 import BeautifulSoup

from sys import argv, exit
from os import mkdir, path
from shutil import copytree, rmtree
from server import start_server


def putDefaultContent():
    def putFolder(src, dest):
        try:
            copytree(src, dest)
        except FileExistsError:
            rmtree(dest)
            copytree(src, dest)

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


def createPages(pages):
    for page in pages:
        pageName = getFolderName(page)
        logger.info(
            f"Building page: {page} as build/{pageName}.php")
        components = getComponents(page)
        components_in_page = getComponentsInPage(page)
        page_code = getPageCode(page)
        for component in components:
            if component.name in components_in_page:
                _name = "{$" + component.name + "}"
                component_code = getPageCode(component.path)
                page_code = page_code.replace(_name, component_code)

        soup = BeautifulSoup(HTML_SKELETON, 'html.parser')
        # Add page metadata if declared
        try:
            metadata = getPageMetadata(page)
            if metadata.title:
                soup.title.string = metadata.title
            if metadata.keywords:
                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                if meta_keywords:
                    meta_keywords['content'] = metadata.keywords
                else:
                    soup.head.append(soup.new_tag(
                        'meta', name='keywords', content=metadata.keywords))
            if metadata.description:
                meta_description = soup.find(
                    'meta', attrs={'name': 'description'})
                if meta_description:
                    meta_description['content'] = metadata.description
                else:
                    soup.head.append(soup.new_tag(
                        'meta', name='description', content=metadata.description))
        except:
            pass

        main = soup.find('main')
        main.append(page_code)
        page_html = soup.prettify(formatter=None)
        with open(f'build/{pageName}.html', 'w') as f:
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
            rmtree('build')
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

if len(argv) != 2:
    print("Usage: python compiler.py build")
else:
    if (argv[1] == 'build'):
        buildApp(files)
    elif argv[1] == 'dev':
        start_server()
