import cv2 as cv 
import numpy as np 
import os
dataSet = './recorte'
faces  = os.listdir(dataSet)
print(faces)

labels = []
facesData = []
label = 0 

img_size = (100, 100)

for face in faces:
    facePath = dataSet+'/'+face
    for faceName in os.listdir(facePath):
        imgPath = os.path.join(facePath, faceName)
        img = cv.imread(imgPath, 0)
        img_resized = cv.resize(img, img_size)
        labels.append(label)
        facesData.append(img_resized)
    label = label + 1
print(np.count_nonzero(np.array(labels)==0)) 

faceRecognizer = cv.face.EigenFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('Eigenface.xml')
