from ultralytics import YOLO
import cv2
from pathlib import Path
import easyocr
import numpy as np
from datetime import time
import csv


def detect_objects_in_video(video_path, output_path):
    
    model = YOLO("video_detection.pt")
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    fps = fps if fps!=90000 else 60
    success,image = vidcap.read()
    count = 0
    frame = 0
    reader = easyocr.Reader(["en", "es"])
    answer = [["ID","OBJECT_TYPE","TIME", "COORDINATES_TEXT"]]

    Path(f"{output_path}/IMG").mkdir(parents=True, exist_ok=True)

    while success:
        if count % round(fps*5) == 0:
            results = model(image, classes=[0,1,2,3])
            preds = results[0].boxes.conf.cpu().numpy()
            if(len(preds)>0):
                act = []
                tiempo = calculate_time(int(count/fps))
                texto = get_coords(reader, image)
                annotated_frame = results[0].plot()
                identifier = 0
                for i in results[0].boxes.cls:
                    clase = results[0].names[int(i)]
                    ID = f"{frame}_{identifier}_{clase}"
                    cv2.imwrite(f"{output_path}/IMG/{ID}.jpg", annotated_frame)
                    identifier += 1
                    answer.append([ID, clase, tiempo, texto])
                frame += 1
        success,image = vidcap.read()
        count += 1

    with open(f'{output_path}/results.csv', 'w', newline='') as file:
         writer = csv.writer(file)
         writer.writerows(answer)


def calculate_time(duration):
    hours = duration//3600
    minutes = (duration//60) % 60
    seconds = duration%60
    
    return time(hours, minutes, seconds).isoformat()


def get_coords(reader, image):
    
    lat = image[40:63, 935:1050,:]
    lon = image[40:63, 1095:1219,:]
    
    texto_lat = procesar_imagen_texto(lat, "N", reader)
    texto_lon = procesar_imagen_texto(lon, "W", reader)
    text = texto_lat + "  " + texto_lon
    return text


def procesar_imagen_texto(img, letra, reader):
    
    try:
    
        # Normalización
        norm_img = np.zeros((img.shape[0], img.shape[1]))
        img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
        # Eliminar ruido
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        # Erosionar los bordes
        kernel = np.ones((1,1),np.uint8)
        erosion = cv2.erode(img, kernel, iterations = 1)
        img_gray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
        # Escala de grises
        img_th = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Convertir la imagen a texto
        ocr_result = reader.readtext(img_th, detail=0, paragraph=True, allowlist ='0123456789')
        # Procesar el output del texto
        rta = volver_a_coordenadas(ocr_result, letra)
        
        return rta
        
    except Exception as e:
        print("Exception", e)
        return "No es legible"
    


def volver_a_coordenadas(texto, letra):
    
    texto_copy = "".join(valor for valor in texto)
    texto_copy = list(texto_copy)
        
    if letra == "N":
    
        # Primera posición será igual a °
        texto_copy[1] = '°'

        # La cuarta posición será igual a '
        texto_copy[4] = "'"

        # La septima posición será igual a .
        texto_copy[7] = '.'
        
    elif letra == "W":
        # Segunda posición será igual a °
        texto_copy[2] = '°'

        # La Quinta posición será igual a '
        texto_copy[5] = "'"

        # La octava posición será igual a .
        texto_copy[8] = '.'

    # Lo que va luego de la posición 11 se elimina y se cambia por " letra"
    texto_copy = texto_copy[:11]
    texto_copy.append(f'" {letra}')
    
    print("Texto copy", texto_copy)
    
    texto_copy = ''.join(texto_copy)

    return texto_copy