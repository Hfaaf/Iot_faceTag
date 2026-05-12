import cv2
import os
import numpy as np

class FaceEngine:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.trained = False

    def train(self, people):
        faces = []
        labels = []

        for i, p in enumerate(people):
            img = cv2.imread(p.image_path, cv2.IMREAD_GRAYSCALE)
            detections = self.detector.detectMultiScale(img, 1.3, 5)

            for (x, y, w, h) in detections:
                faces.append(img[y:y+h, x:x+w])
                labels.append(i)
                self.labels[i] = p

        if faces:
            self.recognizer.train(faces, np.array(labels))
            self.trained = True

    def detect_and_recognize(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = self.detector.detectMultiScale(gray, 1.3, 5)

        results = []
        for (x, y, w, h) in detections:
            face = gray[y:y+h, x:x+w]

            if self.trained:
                label, confidence = self.recognizer.predict(face)
                person = self.labels.get(label) if confidence < 80 else None
            else:
                person = None

            results.append((x, y, w, h, person))

        return results