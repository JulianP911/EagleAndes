# EagleAndes

📊 Codefest Ad Astra 2023

<h1>Libreria - Reto 1 - Procesamiento de lenguage (Clasificación y NER)</h1>

<h3>Instrucciones para correr la librería de python:</h3>
<ul>
  <li>Clonar el repositorio en la carpeta de su preferencia.</li>
  <li>Abrir el proyecto en el editor de preferencia (recomendado <b>Visual Studio Code</b>).</li>
  <li>Abrir la consola e ingresar el comando <code>pip3 install . o pip install .</code> (dependiendo del sistema operativo) para instalar las dependencias asociadas a los recursos empleados definidos en el archivo <code>setup.py</code></li>
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

<h3>Desarrollo del reto 1:</h3>

<ol>
  <li>En primer lugar empezamos por el problema de predición de categoria del textos en cuatro categorías: MINERIA, CONTAMINACION, DEFORESTACION, NINGUNA para esto empezamos por un proceso de limpieza de datos, clasificación de textos sin etiquetas en base del contexto para mejorar la precisión de predición a la hora de entrenar el modelo, 
</li>
  <li>En segundo lugar continuamos con el procesamiento de lenguage aplicando NER (Identificación de entidades con nombre) para esto utilizamos la libreria de SpaCy con el modelo de es_core_news_md que tiene un f1 89.54 lo cual indica un buen porcentaje de prección en base al recall y accurancy. 
</li>
</ol>
