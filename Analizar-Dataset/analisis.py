import pandas as pd
import cv2

df = pd.read_csv('datasetTexto.csv')

print(df.head())
print(df.info())
print(df.describe())

# ID, Categoria, Tituo, Medio, Fecha, Resumen, Comentario_Reaccion