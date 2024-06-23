import cv2
import numpy as np
from PIL import Image
import streamlit as st

class ObjectDetection:
    def __init__(self):
        self.MODEL = "E:/Workspaces/My Projects/WCODC/experimental/MobileNetSSD_deploy.caffemodel"
        self.PROTOTXT = "E:/Workspaces/My Projects/WCODC/experimental/MobileNetSSD_deploy.prototxt.txt"

    def __process_image(self, image):
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        net = cv2.dnn.readNetFromCaffe(self.PROTOTXT, self.MODEL)
        net.setInput(blob)
        detections = net.forward()
        return detections

    def annotate_image(self, image, detections, confidence_threshold=0.5):
        # loop over the detections
        (h, w) = image.shape[:2]
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > confidence_threshold:
                # extract the index of the class label from the 'detections'
                # then compute the (x,y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(image, (startX, startY), (endX, endY), 70, 2)
        return image

    def display(self):
        st.title("Object Detection for Images")
        file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if file is not None:
            st.image(file, caption='Upload Image')

            image = Image.open(file)
            image = np.array(image)
            detections = self.__process_image(image)
            proccesed_image = self.annotate_image(image, detections)
            st.image(proccesed_image)

