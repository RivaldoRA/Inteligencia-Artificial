import numpy as np
import matplotlib.pyplot as plt

def generar_radar_afinidad(puntajes, autores, nombre_archivo="radar_afinidad_filosofica.png"):
    """
    Crea una gráfica de radar para comparar la afinidad del corpus con autores.
    """
    # Número de variables (autores)
    num_vars = len(autores)

    # Calcular los ángulos de cada eje en el gráfico circular
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Cerrar el polígono repitiendo el primer valor
    puntajes = puntajes + puntajes[:1]
    angles = angles + angles[:1]

    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Dibujar el área sombreada y la línea
    ax.fill(angles, puntajes, color='#26a69a', alpha=0.3)
    ax.plot(angles, puntajes, color='#00897b', linewidth=2)

    # Configurar los ejes y etiquetas
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), autores)

    # Ajustar el rango (0 a 1 para similitud coseno)
    ax.set_ylim(0, 1)
    ax.set_rlabel_position(180 / num_vars)

    plt.title("Afinidad Semántica: Corpus Reddit vs. Marcos Teóricos", size=16, y=1.08)
    
    # Guardar imagen
    plt.savefig(nombre_archivo, bbox_inches='tight')
    print(f"Gráfica guardada como: {nombre_archivo}")
    plt.show()

if __name__ == "__main__":
    # Estos puntajes representan el promedio de similitud detectado por tu RAG
    # 0.85 significa que el discurso de Reddit es muy cercano a la teoría de ese autor
    autores_ejes = [
        'Byung-Chul Han\n(Sociedad del Cansancio)', 
        'Zygmunt Bauman\n(Identidad Líquida)', 
        'Michel Foucault\n(Biopoder/Vigilancia)', 
        'Jean-Paul Sartre\n(Existencialismo)', 
        'Jean-François Lyotard\n(Metarrelatos)'
    ]
    
    # Valores de ejemplo basados en la densidad de tu Grafo de Red anterior
    scores_afinidad = [0.88, 0.72, 0.65, 0.50, 0.42]

    generar_radar_afinidad(scores_afinidad, autores_ejes)