# Librerias necesarias con el fin de cumplir los requerimientos determinados para el procesamiento de texto
import random
from sklearn.ensemble import RandomForestClassifier
import spacy, re, json, nltk, urllib, joblib,es_core_news_md, numpy
from spacy.matcher import Matcher
from spacy import displacy
from collections import Counter
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import re, string, unicodedata
import contractions
import inflect # Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words.
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path

from bs4 import BeautifulSoup
from urllib.request import urlopen

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Expresiones regular para las fechas
__expression = r"(?i)((((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+(\s+|\s+|\s+(?=\s))?(de|/|\\|-|)?(\s+|\s+|\s+(?=\s))?((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+(\s+|\s+|\s+(?=\s))?(de|/|\\|-|)?(\s+|\s+|\s+(?=\s))?((ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|enero|febrero|marzo|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|([0-9]?[0-9]?[0-9]?[0-9])))+))"
# Nuevo patron para reconoicer palabras de los daños amazonicos
__patterns = [{"label": "MISC", "pattern": "minería ilegal"}, {"label": "MISC", "pattern": "mercurio"}, {"label": "MISC", "pattern": "oro"}, {"label": "MISC", "pattern": "deforestación"}, {"label": "MISC", "pattern": "árboles talados"}, {"label": "MISC", "pattern": "ecosistema"}, {"label": "MISC", "pattern": "dragas"}, {"label": "MISC", "pattern": "explotación ilegal de la minería"}, {"label": "MISC", "pattern": "cultivos de coca"}, {"label": "MISC", "pattern": "coca"}, {"label": "MISC", "pattern": "cultivos de uso ilícito"}, {"label": "MISC", "pattern": "reservas indígenas"}, {"label": "MISC", "pattern": "hectáreas de bosque"}, {"label": "MISC", "pattern": "hectáreas"}, {"label": "MISC", "pattern": "toneladas de carbono"}, {"label": "MISC", "pattern": "presidencia"}]


# Paso 1: Convertir todos los caracteres a minúsculas
def to_lowercase(words):
    """Convierte todos los caracteres de una lista de palabras tokenizadas a minúsculas"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

# Paso 2: Reemplazar los números
def replace_numbers(words):
    """Reemplaza todas las ocurrencias de números enteros en una lista de palabras tokenizadas con su representación textual"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

# Paso 3: Eliminar la puntuación
def remove_punctuation(words):
    """Elimina la puntuación de una lista de palabras tokenizadas"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

# Paso 4: Eliminar caracteres no ASCII
def remove_non_ascii(words):
    """Elimina los caracteres no ASCII de una lista de palabras tokenizadas"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

# Paso 5: Remover stopwords
def remove_stopwords(words, stopwords=stopwords.words('spanish')):
    """Elimina las palabras vacías de una lista de palabras tokenizadas"""
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
    return new_words

# Paso 6: Aplicar la raíz
def stem_words( words):
    """Palabras clave en la lista de palabras tokenizadas"""
    stemmer = SnowballStemmer('spanish')
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

# Paso 7: Aplicar la lematización
def lemmatize_verbs( words):
    """Lematizar verbos en lista de palabras tokenizadas"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

# Aplicar la raíz y la lematización: Pasos 6 y 7
def stem_and_lemmatize( words):
    words = stem_words(words)
    words = lemmatize_verbs(words)
    return words


# Preprocesamiento: Pasos 1-5
def preproccesing(words):
    words = to_lowercase(words) # 1
    words = replace_numbers(words) # 2
    words = remove_punctuation(words) # 3
    words = remove_non_ascii(words) # 4    
    words = remove_stopwords(words) # 5
    return words


# Función: Encargada del procesamiento de texto con enfoque a NER (Reconocimiento de entidades de nombre)
def __ner(text):
    # Cargar el modelo de spaCY con f1 89.54
    nlp = spacy.load("es_core_news_md")

    # Cargar reglas nuevas para el reconocimiento de entidades
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(__patterns)

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

    # nltk.download('all')
    
    # Ubicación relativa: ./video_detection.pt
    ubicacion = Path(__file__).parent
    ubicacion = ubicacion / './modelo_clasificacion_texto_final_V2.pkl'
    ubicacion1 = Path(__file__).parent
    ubicacion1 = ubicacion1 / "vectorizer_modelo_V2.pkl"
    model = joblib.load(ubicacion)
    vectorizer = joblib.load(ubicacion1)

    X_data= text
    new_X_train = pd.Series(X_data)
    nltk.download('all')
    try:
        new_X_train = new_X_train.apply(contractions.fix) # Corregir las contracciones
        new_X_train = new_X_train.apply(word_tokenize) #  Tokenizar
        new_X_train = new_X_train.apply(lambda x: preproccesing(x)) # Preprocesamiento
        new_X_train = new_X_train.apply(lambda x: stem_and_lemmatize(x)) # Aplicar la raíz y la lematización
        new_X_train = new_X_train.apply(lambda x: ' '.join(map(str, x))) # Convertir la lista de palabras en una cadena de texto
    except:
        print("Instalando dependencia necesaria... / Solo ocurre una vez")
        nltk.download('all')
        new_X_train = new_X_train.apply(contractions.fix) # Corregir las contracciones
        new_X_train = new_X_train.apply(word_tokenize) #  Tokenizar
        new_X_train = new_X_train.apply(lambda x: preproccesing(x)) # Preprocesamiento
        new_X_train = new_X_train.apply(lambda x: stem_and_lemmatize(x)) # Aplicar la raíz y la lematización
        new_X_train = new_X_train.apply(lambda x: ' '.join(map(str, x))) # Convertir la lista de palabras en una cadena de texto
    vectors = vectorizer.transform(new_X_train)
    copia=vectors
    copia=pd.DataFrame.sparse.from_spmatrix(copia)

    pred_mod= model.predict(copia.iloc[0:1])[0] #predicir el impacto

    print(model.predict_proba(copia.iloc[0:1])[0])

    dictionary['impact'] = pred_mod

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
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    lista = soup.findAll('p')
    text=""
    for i in lista:
            if len(str(i.get_text())) >= 250:
                text= text + i.get_text()
    dictionary = __ner(text=text)
    __save_file(output_path, dictionary)