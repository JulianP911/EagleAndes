#from EagleAndes import ner_from_str
from EagleAndes import detect_objects_in_video

# ner_from_str('Según monitoreos de la Alianza Regional Amazónica para la Reducción de los Impactos de la Minería de Oro en 1 de enero de 2015, integrada por varias organizaciones de la sociedad civil, se ha identificado un aumento de lanchas, balsas y dragones en ríos como Puré, Cotuhé y Caquetá, en donde la explotación de oro puede estar realizándose tanto por mineros colombianos como brasileños. En el río Puré (ubicado en el departamento del Amazonas, entre los ríos Caquetá y Putumayo) durante 2022 se identificaron 357 balsas y dragones, un incremento de más del 1.000 % con respecto a 2020, cuando se reportaron 25. Estos registros se llevan a cabo, entre otros recursos, gracias a imágenes satelitales', './output.json')

video_path = 'data/videos/VideoCodefest_005-2min.mpg'
output_path = "pruebas_output"

detect_objects_in_video(video_path, output_path)