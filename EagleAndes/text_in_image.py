from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from keras import models
import cv2
import re


def convertir_coordenadas(coordenadas):
    # Extraer las partes numéricas de las coordenadas
    numeros = re.findall(r'\d+', coordenadas)

    resultado = numeros[0] + '°' + numeros[1] + "'" + numeros[2] + "." + numeros[3] + '"' + " N "  + numeros[4] + '°' + numeros[5] + "'" + numeros[6] + "." + numeros[7] + '"' + " W"
    
    return resultado

def detect_objects_in_video(video_path, output_path, num_frames):

  # Carga del modelo de imágenes
  model = models.load_model('/model/modelo.h5')
  # Carga del modelo de texto
  processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
  model_text = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
  model_text = convertir_coordenadas(model_text)

  # Columnas del cv2
  header = ['ID', 'OBJECT_TYPE', 'TIME', 'COORDINATES_TEXT']
  
  csv = []

  # Revisamos por los primeros 10 frames del video
  count = 0
  vidcap = cv2.VideoCapture(video_path)
  success,image = vidcap.read()
  success = True
  while success:
    if count == num_frames:
      break
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
    success,image = vidcap.read()
    print ('Read a new frame: ', success)
    count = count + 1

    # Parte del video que contiene las coordenadas
    template = image[40:60,940:1260,:]
    # Identificar texto
    pixel_values = processor(images=template, return_tensors="pt").pixel_values
    generated_ids = model_text.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
       
    # Predicción de la imagen 
    img_predict = cv2.resize(image, (240, 160))
    img_predict = np.expand_dims(img_predict, axis=0)
    prediccion = model.predict(img_predict)

    # Si no es una matriz totalmente de ceros
    if np.any(prediccion != np.zeros((160,240,3))):
      rta_pred = 1
      cv2.imwrite(f"/predicts/{count}.jpg", prediccion)
    else:
      rta_pred = 0
    
    contenido = [rta_pred, rta_pred, 0, generated_text]
    csv.append(contenido)

  # Guardamos CVS en la ruta propuesta
  df = pd.DataFrame(csv, columns=header)
  df.to_csv(output_path)
