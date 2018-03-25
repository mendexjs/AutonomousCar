import time # IMPORTAÇÕES NECESSARIAS, FAÇA DOWNLOAD VIA apt-get SE NECESSARIO
import cv2
import numpy as np
import serial
from picamera.array import PiRGBArray
from picamera import PiCamera
serial= serial.Serial('/dev/ttyACM0', 9600) # PORTA DE CONEXÃO COM O ARDUINO
def auto_canny(image, sigma=0.33): # FUNÇÃO QUE GERA OS CONTORNOS
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

def main(): # PRINCIPAL
    camera = PiCamera() # INICIALIZANDO, E CONFIGURANDO A CAMERA
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    while True:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            OriginalFrame = frame.array
            #TRATANDO A IMAGEM COM FILTROS, E APLICANDO PROPRIEDADES DO OPEN CV
            gray = cv2.cvtColor(OriginalFrame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray,(3,3),0)
            edges = auto_canny(blurred)
            cv2.imshow("Contornos Destacados", edges) #MOSTRANDO EM JANELA A IMAGEM DA CAMERA ( NÃO É NECESSARIO)
            cntr_frame, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            rawCapture.truncate(0)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if (area>15000): # DETECTA FORMAS SOMENTE MAIORES QUE 15000 PIXELS DE AREA ( PODE SER ALTERADO)
                    approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                    if len(approx)==3: #COMPARANDO ARESTAS PARA DESCOBRIR A FORMA
                        serial.write('t') # ENVIANDO PARA O ARDUINO
                        time.sleep(1)
                        break
                    elif len(approx)==5: #COMPARANDO ARESTAS PARA DESCOBRIR A FORMA
                        serial.write('p') # ENVIANDO PARA O ARDUINO
                        time.sleep(1)
                        break
                    elif len(approx)==6: #COMPARANDO ARESTAS PARA DESCOBRIR A FORMA
                        serial.write('h') # ENVIANDO PARA O ARDUINO
                        time.sleep(1)
                        break
                     # COMO NESSE CASO NÃO HÁ FORMAS ACIMA DE HEXAGONO (OCTOGONO, DODECAGONO ),
                     #QUALQUER COISA ACIMA DE HEXAGONO ELE JA CONSIDERA CIRCULO, PARA EVTAR ERROS.
                    elif len(approx)>=8: #COMPARANDO ARESTAS PARA DESCOBRIR A FORMA
                        serial.write('c') # ENVIANDO PARA O ARDUINO
                        time.sleep(1)
                        break
        k = cv2.waitKey(1) & 0xFF
        if k == 27: #ESC FINALIZA O SCRIPT
            break
    cv2.destroyAllWindows()
    serial.close()
#Main
if __name__ == "__main__" :
    main()
