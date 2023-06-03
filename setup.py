import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'Codefest Ad Adstra'
AUTHOR = 'EagleAndes'
AUTHOR_EMAIL = 'eagleandes@uniandes.com'
URL = 'https://github.com/JulianP911/EagleAndes'

LICENSE = 'MIT'
DESCRIPTION = 'Solución retos Codefest Ad Astra 2023'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'listado de librerias'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)