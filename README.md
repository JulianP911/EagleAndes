# EagleAndes

📊 Codefest Ad Astra 2023

<h1>Instalación</h1>

<h3>Instalación en local:</h3>

  <li>Clonar el repositorio en la carpeta de su preferencia <code>git clone https://github.com/JulianP911/EagleAndes.git</code> .</li> 
  <li>Abrir el proyecto en el editor de preferencia (recomendado <b>Visual Studio Code</b>).</li>
  <li>Abrir la consola e ingresar el comando <code>pip3 install . o pip install .</code> (dependiendo del sistema operativo) para instalar las dependencias asociadas a los recursos empleados definidos en el archivo
  
<h3>Instalación de la librería:</h3>
  <li>Instalar la libreria mediante pip y el repositorio de github <code>pip install git+https://github.com/JulianP911/EagleAndes.git </code>.</li>   

<h1>Reto 1 - Indetificación de objetos de interés en videos</h1>

<h3>Instrucciones para correr la librería de python:</h3>
  <li>Una vez instalada la libería junto con las dependencias necesarias crear un archivo py en la cual se importe la libreria y las funciones requeridas que se quiere aceder. A continuación, se muestra un ejemplo correspondientemente:
    <ul>
      <li><code>from EagleAndes import detect_objects_in_video</code><br><code>detect_objects_in_video('./video_path', './output_path')</code>
      </li>
    </ul>
  </li>
  <li> Esta función recibe como parámetros de entrada el video a analizar y la ruta donde se va a almacenar el archivo de salida. (...)
  </li>
</ul>

<h3>Desarrollo del reto 1:</h3>

<ol>
  <li>En primer lugar, de los videos que poseíamos, se obtuvieron los fotogramas cada 1 segundo. De estos fotogramas se hizo una definición de cuadros delimitadores para la detección de objetos de interés (construcción, vía, vehículo, otros). Al rededor de 1.200 imágenes y 2500 objetos detectados fueron definidos. De esta manera pudimos asegurar una cantidad suficiente de datos para generar un modelo robusto que cumpla con los requerimientos del reto.</li>
  
  <li>Las imágenes fueron utilizadas como insumo para entrenar al modelo de detección de objetos <a href="https://github.com/ultralytics/ultralytics.git">YOLOv8</a>. Inicialmente se cargó un modelo preentrenado y se realizó un reentrenamiento del modelo para acoplarlo a la detección de objetos de interés. Se realizaron 150 iteraciones durante el entrenamiento y el modelo resultante fue probado con 153 imágenes de validación. Las métricas resultantes indican que el modelo tiene una alta precisión al detectar y localizar los objetos de interés en la imagen.</li> 
  <br>
  
  <table>
  <tr>
    <th>Class</th>
    <th>Images</th>
    <th>Instances</th>
    <th>Box(P)</th>
  </tr>
  <tr>
    <td>all</td>
    <td>153</td>
    <td>496</td>
    <td>0.952</td>
  </tr>
  <tr>
    <td>VEHICULO</td>
    <td>153</td>
    <td>59</td>
    <td>0.959</td>
  </tr>
  <tr>
    <td>CONSTRUCCION</td>
    <td>153</td>
    <td>250</td>
    <td>0.981</td>
  </tr>
  <tr>
    <td>VIA</td>
    <td>153</td>
    <td>3</td>
    <td>0.904</td>
  </tr>
  <tr>
    <td>OTROS</td>
    <td>153</td>
    <td>184</td>
    <td>0.963</td>
  </tr>
</table>

  <li>Para el análisis de coordenadas en las imágenes, se utilizó el modelo preentrenado de texto <a href="https://www.jaided.ai/easyocr/install/">EasyOCR</a> que permitía obtener de manera precisa y sencilla el texto que contenían los fotogramas. Cabe resaltar que para lograr un mejor reconocimiento de las coordenadas se hizo un preprocesamiento de las imágenes que permitió resaltar las carácteristicas de los textos presentes en ellas.</li>
  <li>Por último, tanto el modelo como el analizador de textos en imágenes fueron unificados en la librería para resolver el reto 1.</li>
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
  <li>En primer lugar empezamos por el problema de predición de categoria del textos en cuatro categorías: MINERIA, CONTAMINACION, DEFORESTACION, NINGUNA para esto empezamos por un proceso de limpieza de datos, re-clasificación de textos que tenían etiquetas distintas a las que estaban establecidas para la solución en base del contexto para mejorar la precisión de predición a la hora de entrenar el modelo, que en este caso nos centramos en un RandomForestClassifier que fue el que mejor nos proporcionó resultados por medio de búsqueda de hiperparámetros con un accuracy con los datos de entrenamiento del 99% y un accuracy con los datos de test de un 84%.
</li>
  <li>Un punto intermedio entre el etiquetado de datos y el modelado de un RandomForest fue el preprocesamiento , en el cuál se realizó todo los tipos de procesos necesarios de limpieza para un modelo lo más óptimo posible cuando se trata de texto. Se realizaron procesos de convertir todos los carácteres a minísculas, convertir a lenguaje natural los números que aparecen en el texto, eliminar la puntuación de las palabras, eliminar los carácteres ASCII, eliminar palabras que no son relevantes en el contexto del problema como por ejemplo artículos personales, se aplicó un proceso de lematización de las palabras  y finalmente se listaron las palabras de manera tokenizada. Todo lo anterior para poder tener un modelo de RandomForest de la mejor manera construida.
</li> 
  <li>En tercer lugar, continuamos con el procesamiento de lenguage aplicando NER (Identificación de entidades con nombre) para esto utilizamos la libreria de SpaCy con el modelo de es_core_news_md que tiene un f1 89.54 lo cual indica un buen porcentaje de prección en base al recall y accuracy para 4 de las 5 clases que se pedían obtener una posible clasificación. 
</li>
  
 <li>Finalmente, para la identificación de fechas se creó una fórmula regex para poder identificar este tipo de entidades que tienen muchísimas tipo de variables posibles.
</li>
</ol>
