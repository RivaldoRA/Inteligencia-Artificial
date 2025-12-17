# Cargar imagen
# Cambiarla a HSV
# Utilizar el rango de color humbral alto y bajo
# Detectar figuras por color

import cv2 as cv
img = cv.imread('figura.png', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)

# Rojo
umbralRojoBajo=(0, 80, 80)
umbralRojoAlto=(10, 255, 255)
umbralRojoBajoB=(170, 80,80)
umbralRojoAltoB=(180, 255, 255)

mascaraRojo1 = cv.inRange(img3, umbralRojoBajo, umbralRojoAlto)
mascaraRojo2 = cv.inRange(img3, umbralRojoBajoB, umbralRojoAltoB)

mascaraRojo = mascaraRojo1 + mascaraRojo2

# Verde
umbralVerdeBajo=(30, 80, 80)
umbralVerdeAlto=(80, 255, 255)

mascaraVerde = cv.inRange(img3, umbralVerdeBajo, umbralVerdeAlto)

# Azul
umbralAzulBajo=(100, 80, 80)
umbralAzulAlto=(140, 255, 255)

mascaraAzul = cv.inRange(img3, umbralAzulBajo, umbralAzulAlto)

# Amarillo
umbralAmarilloBajo=(15, 80, 80)
umbralAmarilloAlto=(35, 255, 255)

mascaraAmarillo = cv.inRange(img3, umbralAmarilloBajo, umbralAmarilloAlto)

cv.imshow('mascara', mascaraRojo)
contours, _ = cv.findContours(mascaraRojo, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

if contours:
    largest_contour = max(contours, key=cv.contourArea)
    ((x, y), radius) = cv.minEnclosingCircle(largest_contour)
    if radius > 10:
        img2 = img[int(y-radius):int(y+radius), int(x-radius):int(x+radius)]
        cv.imshow('img2', img2)

print("N Figuras Rojas: ")

cv.imshow('mascara', mascaraVerde)
print("N Figuras Verdes: ")

cv.imshow('mascara', mascaraAzul)
print("N Figuras Azules: ")

cv.imshow('mascara', mascaraAmarillo)
print("N Figuras Amarillas: ")

cv.waitKey(0)
cv.destroyAllWindows()