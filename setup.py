import pathlib
from setuptools import find_packages, setup
import subprocess
import platform

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'Codefest'
AUTHOR = 'EagleAndes'
AUTHOR_EMAIL = 'eagleandes@uniandes.com'
URL = 'https://github.com/JulianP911/EagleAndes'

LICENSE = 'MIT'
DESCRIPTION = 'Solución retos Codefest Ad Astra 2023'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'urllib3==1.26.6',
    'pandas',
    'spacy',
    'joblib',
    'scikit-learn',
    'contractions',
    'inflect',
    'nltk',
    'wordcloud',
    "dill",
    'numpy',
    'matplotlib',
    'Pillow',
    'opencv-python',
    'transformers',
    'ultralytics',
    'Path',
    'easyocr',
    'datetime',
    'stopwords',
    'inflect',
    'nltk'
]

def setup_package():
    
    os_name = platform.system()
    if os_name == 'Windows':
        # Descargar modelo de Spacy durante la instalación
        spacy_cmd = "python -m spacy download es_core_news_md"
    else:
        spacy_cmd = "python3 -m spacy download es_core_news_md"
    subprocess.call(spacy_cmd, shell=True)

    # Resto del código de configuración
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
        packages=find_packages(include=["EagleAndes"]),
        include_package_data=True
    )

if __name__ == '__main__':
    setup_package()