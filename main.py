from ultralytics import YOLO
import cv2
import urllib.request
import serial.tools.list_ports
import serial
import numpy as np
from time import sleep

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

serialInst.baudrate = 9600
serialInst.port = "COM4"
serialInst.open()

# url = 'http://192.16/8.1.128/240x240.jpg'
url = 'http://192.168.61.61/240x240.jpg'

model = YOLO('best.pt')

while True:
    try:
        cap = cv2.VideoCapture(url)
        ret, frame = cap.read()
        
        results = model.track(frame)
        
        for box in results[0].boxes:
            class_id = int(box.cls)  # Get class ID
            class_label = results[0].names[class_id]  # Get class label from class ID
            print(f'Detected class: {class_label}')  # Print class label
        
        # anno = results[0].plot()

        if "organic" in class_label:
            angle = "0"
            serialInst.write(angle.encode('utf-8'))
            sleep(5)
        elif "glass" in class_label:
            angle = "90"
            serialInst.write(angle.encode('utf-8'))
            sleep(5)
        
        elif class_label == "plastic":
            angle = "180"
            serialInst.write(angle.encode('utf-8'))
            sleep(5)
        
        elif class_label == "paper":
            angle = "270"
            serialInst.write(angle.encode('utf-8'))
            sleep(5)

        
        class_label = ""
        
        
        # cv2.imshow('', anno)
        # cv2.waitKey(1)
    except Exception as ex:
        print(ex)
