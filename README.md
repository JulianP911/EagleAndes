# EagleAndes

📊 Codefest Ad Astra 2023
<h1>Libreria - Reto 1 - Indetificación de objetos de interés en videos</h1>

<h3>Instrucciones para correr la librería de python:</h3>
<ul>
  <li>Clonar el repositorio en la carpeta de su preferencia.</li>
  <li>Abrir el proyecto en el editor de preferencia (recomendado <b>Visual Studio Code</b>).</li>
  <li>Abrir la consola e ingresar el comando <code>pip3 install . o pip install .</code> (dependiendo del sistema operativo) para instalar las dependencias asociadas a los recursos empleados definidos en el archivo <code>setup.py</code>.
  <li>Una vez descargado las dependencias necesarias crear un archivo py en la cual se importe la libreria y las funciones requeridas que se quiere aceder. A continuación, se muestra un ejemplo correspondientemente:
    <ul>
      <li><code>from EagleAndes import detect_objects_in_video</code><br><code>detect_objects_in_video('./video_path', './output_path', cantidad_fotogramas)</code>
      </li>
    </ul>
  </li>
  <li> Esta función recibe como parámetros de entrada el video a analizar, la ruta donde se va a almacenar el archivo de salida, y la cantidad de fotogramas que quiere analizar. La función halla la cantidad inicial de fotogramas del video ingresado por parámetro, estos fotogramas se guardan como imágenes y se realizan dos labores principales, la primera es el calculo de coordenadas por medio del análisis de texto de la imagen, y la segunda es la segmentación de este para ver si identifica algún tipo de construcción, vehículo o vía en el fotograma. Los resultados del análisis de coordenadas se almacenana en un .csv, además, si se llega a encontrar algún tipo de objeto durante la segmentación, la imagen de este fotograma segmentado se almacenará en una carpeta.
  </li>
</ul>

<h3>Desarrollo del reto 1:</h3>

<ol>
  <li>En primer lugar, de los videos que poseíamos, se obtuvieron los fotogramas cada 300 fotogramas y se segmentaron a mano para poder identificar viviendas, vehiculos, vías, otros.
</li>
  <li>En segundo lugar, después de segmentar estas imágenes, se realizó un código para poder generar una imagen segmentada que pueda ser entendida por la rede nueronal de arquitectura UNET. De esta manera, se entrenó una red neuronal con esta arquitectura para obtener un modelo que pudiera segmentar.
</li>
  <li> En tercer lugar, se guardó este modelo para ser utilizado posteriormente en la solución final.
  </li>
  <li> Para el análisis de coordenadas en las imágenes, se utilizó un modelo preentranado de texto que permitía obtener de manera precisa y sencilla el texto que contenían los fotogramas.
  </li>
  <li> Por último, se unificó tanto el modelo como el analizador de textos en imágentes en la librería para resolver el reto 1.
  </li>
</ol>

<h1>Libreria - Reto 2 - Procesamiento de lenguage (Clasificación y NER)</h1>

<h3>Instrucciones para correr la librería de python:</h3>
<ul>
  <li>Clonar el repositorio en la carpeta de su preferencia.</li>
  <li>Abrir el proyecto en el editor de preferencia (recomendado <b>Visual Studio Code</b>).</li>
  <li>Abrir la consola e ingresar el comando <code>pip3 install . o pip install .</code> (dependiendo del sistema operativo) para instalar las dependencias asociadas a los recursos empleados definidos en el archivo <code>setup.py</code>. Asimismo, ingresar el comando para instalar el modelo para el manejo de NER con <code>python -m spacy download es_core_news_md o python3 -m spacy download es_core_news_md</code> dependiendo del sistema operativo.</li>
  <li>Una vez descargado las dependencias necesarias crear un archivo py en la cual se importe la libreria y las funciones requeridas que se quiere aceder. A continuación, se muestra un ejemplo correspondientemente:
    <ul>
      <li><code>from EagleAndes import ner_from_str</code><br><code>ner_from_str('Texto ejemplo', './output.json')</code>
      </li>
    </ul>
  </li>
  <li>Como se especificaba en la guía se desarrollaron tres metodos los cuales retornan json con el clasificación. del texto en base a las etiquetas y la identificación de entidades de nombre.
    <ul>
      <li>def ner_from_str(text, output_path)</li>
      <li>def ner_from_file(text_path, output_path)</li>
      <li>def ner_from_url(url, output_path)</li>
    </ul>
  </li>
</ul>

<h3>Desarrollo del reto 2:</h3>

<ol>
  <li>En primer lugar empezamos por el problema de predición de categoria del textos en cuatro categorías: MINERIA, CONTAMINACION, DEFORESTACION, NINGUNA para esto empezamos por un proceso de limpieza de datos, clasificación de textos sin etiquetas en base del contexto para mejorar la precisión de predición a la hora de entrenar el modelo, 
</li>
  <li>En segundo lugar continuamos con el procesamiento de lenguage aplicando NER (Identificación de entidades con nombre) para esto utilizamos la libreria de SpaCy con el modelo de es_core_news_md que tiene un f1 89.54 lo cual indica un buen porcentaje de prección en base al recall y accurancy. 
</li>
</ol>
