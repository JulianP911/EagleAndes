# Librerias necesarias con el fin de cumplir los requerimientos determinados para el procesamiento de texto
import spacy, re, json, nltk, urllib, joblib,es_core_news_md
from spacy import displacy
from collections import Counter
import pandas as pd

# Expresiones regular para las fechas
__expression = r"(?i)((((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+(\s+|\s+|\s+(?=\s))?(de|/|\\|-|)?(\s+|\s+|\s+(?=\s))?((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+(\s+|\s+|\s+(?=\s))?(de|/|\\|-|)?(\s+|\s+|\s+(?=\s))?((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+))"

# Función: Encargada del procesamiento de texto con enfoque a NER (Reconocimiento de entidades de nombre)
def __ner(text):
    # Cargar el modelo de spaCY con f1 89.54
    nlp = spacy.load("es_core_news_md")

    # Clasificación de entidades por categorias: LOC, ORG, MISC, PER
    document= nlp(text)
    org, loc, per, dates, misc = [], [], [], [], []
    for ent in document.ents:
        if ent.label_ == 'LOC':
            loc.append(ent.text)
        elif ent.label_ == 'ORG':
            org.append(ent.text)
        elif ent.label_ == 'MISC':
            misc.append(ent.text)
        elif ent.label_ == 'PER':
            per.append(ent.text)

    # Clasificación de entidades por categoria: DATES para esto se añade una regla nueva a partir de un expresión regular para la identificación de fechas
    for match in re.finditer(__expression, document.text):
        start, end = match.span()
        span = document.char_span(start, end)
        if span is not None:
            dates.append(span.text)

    # Definir el esquema del diccionario
    dictionary = {
        'text': text,
        'org': org,
        'loc': loc,
        'per': per,
        'dates': dates,
        'misc':misc,
    }

    return dictionary

# Función: Guardar un archvio json con el análisis del procesamiento de texto
def __save_file(output_path, dictionary):
    file = open(output_path, 'w', encoding='utf-8')
    file.write(json.dumps(dictionary, ensure_ascii=False))
    file.close()


# Función: Generar un archivo json con el procesamiento de texto: clasificación de impacto y NER.
# Párametros: text (texto de entrada) y output_path (dirección de salida donde se guarda el resultado)
def ner_from_str(text, output_path):
    dictionary = __ner(text=text)
    # model = joblib.load('/Users/julianpadilla/Desktop/EagleAndes/EagleAndes/model/modelo_clasificacion_texto.pkl')
    __save_file(output_path, dictionary)

# Función: Generar un archivo json con el procesamiento de texto: clasificación de impacto y NER.
# Párametros: text_path (dirección del archivo que contiene el texto) y output_path (dirección de salida donde se guarda el resultado)
def ner_from_file(text_path, output_path):
    file = open(text_path, "r")
    text = file.read()
    dictionary = __ner(text=text)
    __save_file(output_path, dictionary)

# Función: Generar un archivo json con el procesamiento de texto: clasificación de impacto y NER.
# Párametros: url (url donde está alojado el texto) y output_path (dirección de salida donde se guarda el resultado)
def ner_from_url(url, output_path):
    file = urllib.request.urlopen(url)
    text = file.read()
    dictionary = __ner(text=text)
    __save_file(output_path, dictionary)